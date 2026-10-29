"""Model-lane contract tests.

Each lane must satisfy the same interface and the same fairness constraints.
These tests catch the failure modes that would invalidate a comparison: a lane
that quietly reshapes the data, a lane that is non-deterministic across seeds,
or a lane that receives different columns from its peers.
"""

from __future__ import annotations

import numpy as np
import pytest

from int4096.features.build import build_features
from int4096.models.base import MODEL_REGISTRY, build_estimator, resolve_model_class

# ``mlp`` is gated behind protocol decision D2; the rest are always available.
ACTIVE_LANES = [
    "linear_baseline",
    "ridge",
    "svr",
    "random_forest",
    "hist_gradient_boosting",
]

P2 = {
    "description": "StandardScaler fitted on training indices only",
    "scaler": "standard",
    "imputer": "median",
    "features": "full",
    "missing_indicators": False,
    "winsorize_quantiles": None,
}
P0 = {
    "description": "no scaling",
    "scaler": None,
    "imputer": "median",
    "features": "full",
    "missing_indicators": False,
    "winsorize_quantiles": None,
}
P3 = {
    "description": "reduced feature set",
    "scaler": None,
    "imputer": "median",
    "features": "reduced",
    "missing_indicators": False,
    "winsorize_quantiles": None,
}


@pytest.fixture(scope="module")
def dataset():
    from tests.conftest import make_series

    frame = make_series(n=260, noise=0.012, seed=5)
    X, y = build_features(frame, lookback=30, mode="delta")
    return X.iloc[:180], y.iloc[:180], X.iloc[180:], y.iloc[180:]


@pytest.mark.parametrize("model_id", ACTIVE_LANES)
def test_lane_fits_and_predicts_finite_values(model_id, dataset):
    X_train, y_train, X_test, _ = dataset
    estimator = build_estimator(model_id, {}, 42, P2)
    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_test)
    assert predictions.shape == (len(X_test),)
    assert np.isfinite(predictions).all()


@pytest.mark.parametrize("model_id", ACTIVE_LANES)
def test_lane_receives_identical_columns(model_id, dataset):
    """Every lane must see the same feature names, in the same order."""
    X_train, y_train, _, _ = dataset
    estimator = build_estimator(model_id, {}, 42, P2)
    estimator.fit(X_train, y_train)
    assert list(estimator.feature_names_in_) == list(X_train.columns)


@pytest.mark.parametrize("model_id", ["ridge", "svr", "random_forest"])
def test_lane_is_deterministic_for_a_fixed_seed(model_id, dataset):
    X_train, y_train, X_test, _ = dataset
    first = build_estimator(model_id, {}, 42, P2).fit(X_train, y_train).predict(X_test)
    second = build_estimator(model_id, {}, 42, P2).fit(X_train, y_train).predict(X_test)
    np.testing.assert_allclose(first, second, rtol=1e-10, atol=1e-10)


def test_scaling_barely_changes_random_forest(dataset):
    """Trees are *approximately* invariant to monotone per-feature scaling.

    This is the ablation's built-in negative control. It is not an exact
    invariance: split thresholds are compared in floating point, so a 1-ULP
    change in a scaled value can flip a near-tied split and cascade into a
    slightly different forest. The honest assertion is therefore "materially the
    same", and the comparison against SVR below shows the contrast is real.
    """
    X_train, y_train, X_test, _ = dataset
    unscaled = build_estimator("random_forest", {}, 7, P0).fit(X_train, y_train).predict(X_test)
    scaled = build_estimator("random_forest", {}, 7, P2).fit(X_train, y_train).predict(X_test)

    relative_gap = np.abs(unscaled - scaled).mean() / (np.abs(unscaled).mean() + 1e-12)
    assert relative_gap < 0.10, f"scaling changed the forest by {relative_gap:.1%}"
    assert np.corrcoef(unscaled, scaled)[0, 1] > 0.99


def test_scaling_affects_svr_far_more_than_random_forest(dataset):
    """The core P2 contrast: scale-sensitive vs scale-invariant families.

    Both lanes see identical data; only the scaler changes. The claim tested is
    *relative*: SVR's predictions move much more than the forest's.
    """
    X_train, y_train, X_test, _ = dataset

    forest_gap = np.abs(
        build_estimator("random_forest", {}, 7, P0).fit(X_train, y_train).predict(X_test)
        - build_estimator("random_forest", {}, 7, P2).fit(X_train, y_train).predict(X_test)
    ).mean()

    svr_unscaled = build_estimator("svr", {"C": 1.0}, 7, P0).fit(X_train, y_train).predict(X_test)
    svr_scaled = build_estimator("svr", {"C": 1.0}, 7, P2).fit(X_train, y_train).predict(X_test)
    assert np.isfinite(svr_unscaled).all() and np.isfinite(svr_scaled).all()
    svr_gap = np.abs(svr_unscaled - svr_scaled).mean()

    assert svr_gap > forest_gap, (
        f"expected scaling to affect SVR more than a forest "
        f"(svr={svr_gap:.6g}, forest={forest_gap:.6g})"
    )


def test_reduced_feature_variant_selects_fewer_columns(dataset):
    X_train, y_train, X_test, _ = dataset
    estimator = build_estimator("ridge", {}, 42, P3)
    estimator.fit(X_train, y_train)
    retained = list(estimator.named_steps["select"].columns)
    assert len(retained) < len(X_train.columns)
    assert set(retained) <= set(X_train.columns)
    assert estimator.predict(X_test).shape == (len(X_test),)


def test_registry_paths_are_importable():
    for model_id, dotted in MODEL_REGISTRY.items():
        assert ":" in dotted, model_id
        if model_id == "mlp":
            continue  # optional dependency guard is tested separately
        assert callable(resolve_model_class(dotted)), model_id


def test_mlp_lane_declares_it_needs_approval():
    """The optional lane must carry its own gate, not rely on documentation."""
    from int4096.models import mlp

    assert mlp.REQUIRES_OWNER_APPROVAL is True
    assert "decision_log" in mlp.APPROVAL_REFERENCE


def test_model_failure_is_visible_not_swallowed(dataset):
    """An impossible hyperparameter must raise, not silently degrade."""
    X_train, y_train, _, _ = dataset
    estimator = build_estimator("ridge", {"alpha": -1.0}, 42, P2)
    with pytest.raises(Exception):
        estimator.fit(X_train, y_train)


# ------------------------------------------------------- runner-level leakage
def test_runner_fits_and_tunes_on_training_rows_only(tmp_path):
    """A leak in the runner's slicing would survive every other test (LEAK-013).

    The runner is instrumented to record exactly which row positions reach
    `fit`, both during inner-CV tuning and during the final fit. Every one of
    them must be strictly before the validation block.
    """
    import int4096.experiments.run as runner
    from int4096.config import load_protocol

    protocol = load_protocol()
    prepared = runner.prepare_dataset("AAPL", protocol)
    split = prepared["split"]

    fitted_positions: list[np.ndarray] = []
    original = runner.build_estimator

    class RecordingEstimator:
        def __init__(self, inner, position_of):
            self.inner = inner
            self.position_of = position_of

        def fit(self, X, y=None):  # noqa: N803
            index = list(X.index)
            positions = np.array(
                [self.position_of[ts] for ts in index], dtype=int
            )
            fitted_positions.append(positions)
            self.inner.fit(X, y)
            return self

        def predict(self, X):  # noqa: N803
            return self.inner.predict(X)

        def __getattr__(self, name):
            return getattr(self.inner, name)

    position_of = {ts: i for i, ts in enumerate(prepared["X"].index)}

    def recording_build(model_id, hyperparams, seed, variant, feature_columns=None):
        inner = original(model_id, hyperparams, seed, variant, feature_columns)
        return RecordingEstimator(inner, position_of)

    runner.build_estimator = recording_build
    try:
        manifest = runner.run_cell(
            "AAPL", "ridge", "P2", protocol, max_trials=2, max_seconds=30,
            output_root=tmp_path, human_owner="test",
        )
    finally:
        runner.build_estimator = original

    assert manifest.status == "SUCCESS"
    assert fitted_positions, "no fit call was recorded"
    for positions in fitted_positions:
        assert positions.max() < split.validation_start, (
            "the runner fitted on rows from the validation block"
        )
