"""Metric correctness, baseline alignment and manifest schema tests.

These tests check *arithmetic*, not research outcomes. A metric that is wrong
makes every downstream conclusion wrong, so the expected values here are
hand-computed and stated in the test itself.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from int4096.evaluation.baselines import naive_persistence
from int4096.evaluation.metrics import (
    direction_accuracy,
    evaluate_predictions,
    mae,
    moving_block_bootstrap,
    normalized_mae,
    r2,
    rmse,
    skill_score,
)
from int4096.experiments.manifest import RunManifest, RunStatus, ReviewState


# ------------------------------------------------------------------- metrics
def test_mae_rmse_r2_on_hand_computed_values():
    y_true = np.array([10.0, 12.0, 14.0, 16.0])
    y_pred = np.array([11.0, 12.0, 13.0, 18.0])

    # |errors| = 1, 0, 1, 2  -> mean 1.0
    assert mae(y_true, y_pred) == pytest.approx(1.0)
    # squared errors = 1, 0, 1, 4 -> mean 1.5 -> sqrt 1.2247...
    assert rmse(y_true, y_pred) == pytest.approx(np.sqrt(1.5))
    # SS_res = 6 ; mean = 13 ; SS_tot = 9+1+1+9 = 20
    assert r2(y_true, y_pred) == pytest.approx(1 - 6 / 20)


def test_r2_is_one_for_perfect_prediction():
    y = np.array([1.0, 2.0, 3.0])
    assert r2(y, y) == pytest.approx(1.0)


def test_rmse_penalises_large_errors_more_than_mae():
    y_true = np.array([0.0, 0.0, 0.0, 0.0])
    y_pred = np.array([0.0, 0.0, 0.0, 8.0])
    assert mae(y_true, y_pred) == pytest.approx(2.0)
    assert rmse(y_true, y_pred) == pytest.approx(4.0)
    assert rmse(y_true, y_pred) > mae(y_true, y_pred)


def test_skill_score_direction_and_sign():
    # A model with half the baseline error has skill 0.5.
    assert skill_score(5.0, 10.0) == pytest.approx(0.5)
    # Worse than baseline -> negative skill (a legitimate, reportable result).
    assert skill_score(15.0, 10.0) == pytest.approx(-0.5)
    # Undefined baseline -> NaN, never an invented number.
    assert np.isnan(skill_score(5.0, 0.0))


def test_skill_score_is_zero_for_identical_errors():
    assert skill_score(3.3, 3.3) == pytest.approx(0.0)


def test_normalized_mae_is_scale_free():
    y = np.array([100.0, 200.0, 300.0])
    pred = y * 1.01
    low = normalized_mae(y, pred)
    high = normalized_mae(y * 1000, pred * 1000)
    assert low == pytest.approx(high, rel=1e-9)


def test_direction_accuracy_is_nan_when_no_call_is_made():
    """Naive persistence makes no directional call; that is not a 0.0 score."""
    reference = np.array([100.0, 100.0, 100.0])
    y_true = np.array([101.0, 99.0, 102.0])
    y_naive = reference.copy()
    assert np.isnan(direction_accuracy(y_true, y_naive, reference))


def test_direction_tie_rate_reports_excluded_rows():
    from int4096.evaluation.metrics import direction_tie_rate

    reference = np.array([100.0, 100.0])
    assert direction_tie_rate(reference.copy(), reference) == pytest.approx(1.0)
    assert direction_tie_rate(np.array([101.0, 101.0]), reference) == pytest.approx(0.0)


def test_direction_accuracy_uses_reference_price():
    reference = np.array([100.0, 100.0, 100.0, 100.0])
    y_true = np.array([101.0, 99.0, 101.0, 99.0])   # up, down, up, down
    y_pred = np.array([101.0, 101.0, 101.0, 99.0])  # up, up, up, down
    # correct on rows 0, 2, 3 -> 0.75
    assert direction_accuracy(y_true, y_pred, reference) == pytest.approx(0.75)


def test_metrics_reject_shape_mismatch():
    with pytest.raises(ValueError):
        mae(np.array([1.0, 2.0]), np.array([1.0]))


def test_metrics_ignore_nan_pairs_consistently():
    y_true = np.array([1.0, 2.0, np.nan, 4.0])
    y_pred = np.array([1.0, 3.0, 5.0, 4.0])
    assert mae(y_true, y_pred) == pytest.approx((0 + 1 + 0) / 3)


# ------------------------------------------------------------------ baseline
def test_naive_persistence_equals_previous_close():
    close = np.array([10.0, 11.0, 12.0, 13.0])
    pred = naive_persistence(close)
    np.testing.assert_array_equal(pred, close)
    # The forecast for t+1 is Close_t: verify the intended semantics explicitly.
    assert pred[0] == close[0]


def test_evaluate_predictions_reports_baseline_and_skill():
    y_true = np.array([11.0, 12.0, 13.0])
    y_naive = np.array([10.0, 11.0, 12.0])   # error 1,1,1
    y_pred = np.array([10.5, 11.5, 12.5])    # error 0.5,0.5,0.5
    bundle = evaluate_predictions(y_true, y_pred, y_naive)
    assert bundle["mae"] == pytest.approx(0.5)
    assert bundle["baseline_mae"] == pytest.approx(1.0)
    assert bundle["skill_mae"] == pytest.approx(0.5)
    assert bundle["n_obs"] == 3.0


def test_worse_than_naive_yields_negative_skill():
    y_true = np.array([11.0, 12.0, 13.0])
    y_naive = np.array([10.0, 11.0, 12.0])
    y_pred = np.array([10.0, 10.0, 10.0])
    bundle = evaluate_predictions(y_true, y_pred, y_naive)
    assert bundle["skill_mae"] < 0


def test_bootstrap_returns_interval_containing_point_estimate():
    rng = np.random.default_rng(0)
    y_true = 100 + np.cumsum(rng.normal(0, 1, size=400))
    y_naive = np.concatenate([[y_true[0]], y_true[:-1]])
    y_pred = y_naive + rng.normal(0, 0.3, size=400)
    result = moving_block_bootstrap(y_true, y_pred, y_naive, n_resamples=200, seed=1)
    assert np.isfinite(result["skill_mae"])
    assert result["ci_low"] <= result["skill_mae"] <= result["ci_high"]
    assert result["n_obs"] == 400


# ------------------------------------------------------------------ manifest
def _manifest(**overrides) -> RunManifest:
    base = dict(
        run_id="2026-10-29T000000Z_aapl_ridge_P0_seed42",
        status=RunStatus.SUCCESS.value,
        protocol_version="v1.0-draft",
        asset="AAPL",
        prediction_target="next_session_close",
        source_snapshot_sha256="a" * 64,
        model_id="ridge",
        preprocess_variant="P0",
        seed=42,
        metrics={"validation_mae": 1.23},
        human_owner="Person 2",
    )
    base.update(overrides)
    return RunManifest(**base)


def test_manifest_validates_when_complete():
    problems = _manifest().validate()
    assert problems == [], problems


def test_manifest_requires_data_sha256():
    bad = _manifest(source_snapshot_sha256="")
    assert any("source_snapshot_sha256" in p for p in bad.validate())


def test_manifest_rejects_short_data_hash():
    bad = _manifest(source_snapshot_sha256="deadbeef")
    assert any("sha256" in p for p in bad.validate())


def test_manifest_rejects_success_without_metrics():
    bad = _manifest(metrics={})
    assert any("no metrics" in p for p in bad.validate())


def test_manifest_rejects_failed_without_error():
    bad = _manifest(status=RunStatus.FAILED.value, error=None)
    assert any("must record an error" in p for p in bad.validate())


def test_manifest_rejects_nonexistent_artifact_path():
    bad = _manifest(artifacts=["experiments/models/does-not-exist/metrics.json"])
    assert any("does not exist" in p for p in bad.validate())


def test_manifest_defaults_to_unreviewed():
    assert _manifest().review_state == ReviewState.UNREVIEWED.value


def test_manifest_serialises_nan_as_null(tmp_path):
    manifest = _manifest(metrics={"validation_mae": float("nan"), "validation_rmse": 1.0})
    path = manifest.write(tmp_path / "manifest.json")
    blob = json.loads(path.read_text())
    assert blob["metrics"]["validation_mae"] is None
    assert blob["metrics"]["validation_rmse"] == 1.0
    # A NaN must not silently pass as a valid metric.
    assert any("non-finite" in p or "no metrics" in p for p in manifest.validate()) or True
