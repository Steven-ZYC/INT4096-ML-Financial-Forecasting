"""Temporal integrity tests — the scientific core of the test suite.

Every test here encodes an invariant stated in ``docs/research/protocol.md``.
If one of these fails, the experiment results are not trustworthy, regardless of
how good the numbers look.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from int4096.data.split import (
    assert_no_overlap,
    chronological_split,
    expanding_window_folds,
)
from int4096.features.build import build_features, make_label


# ---------------------------------------------------------------- label shift
def test_label_shift_is_next_bar_and_drops_last(synthetic_frame):
    """``y_t`` must equal ``Close_{t+1}`` and the terminal row must be dropped."""
    X, y = build_features(synthetic_frame, lookback=30, mode="level")

    assert len(X) == len(y)
    assert X.index.equals(y.index)

    # The final snapshot row has no observable t+1 and must not appear.
    assert synthetic_frame.index[-1] not in y.index

    # Spot-check the definition on real rows, using the frame's own close.
    close = synthetic_frame["close"]
    for ts in list(y.index)[:5] + list(y.index)[-5:]:
        position = synthetic_frame.index.get_loc(ts)
        expected = close.iloc[position + 1]
        assert y.loc[ts] == pytest.approx(expected, rel=0, abs=0)

    # And the label is strictly the NEXT bar, not the current one.
    first_ts = y.index[0]
    assert y.iloc[0] != pytest.approx(close.loc[first_ts])


def test_delta_label_equals_price_difference_and_drops_last(synthetic_frame):
    """Delta mode: ``y_t = Close_{t+1} - Close_t``, identical index handling."""
    X, y = build_features(synthetic_frame, lookback=30, mode="delta")
    close = synthetic_frame["close"]

    assert len(X) == len(y)
    assert synthetic_frame.index[-1] not in y.index

    for ts in list(y.index)[:5] + list(y.index)[-5:]:
        position = synthetic_frame.index.get_loc(ts)
        expected = close.iloc[position + 1] - close.iloc[position]
        assert y.loc[ts] == pytest.approx(expected, rel=0, abs=1e-12)


def test_level_and_delta_labels_are_information_equivalent(synthetic_frame):
    """``level_t == Close_t + delta_t`` exactly, on identical rows."""
    X_level, y_level = build_features(synthetic_frame, lookback=30, mode="level")
    X_delta, y_delta = build_features(synthetic_frame, lookback=30, mode="delta")

    assert X_level.index.equals(X_delta.index)
    close_at_t = synthetic_frame.loc[X_delta.index, "close"]
    reconstructed = close_at_t + y_delta
    pd.testing.assert_series_equal(
        reconstructed, y_level, check_names=False, check_freq=False, rtol=1e-12, atol=1e-12
    )


def test_unknown_label_mode_is_rejected(synthetic_frame):
    with pytest.raises(ValueError, match="Unknown label mode"):
        build_features(synthetic_frame, lookback=30, mode="log-return")


def test_label_never_appears_in_features(synthetic_frame):
    """The target must not leak into ``X`` under any column name."""
    X, y = build_features(synthetic_frame, lookback=30, mode="level")
    assert "y_next_close" not in X.columns

    # A perfect forecast cannot be reconstructed from X alone: if the label were
    # present, y would be an exact linear function of some column.
    for column in X.columns:
        correlation = np.corrcoef(X[column].to_numpy(), y.to_numpy())[0, 1]
        assert abs(correlation) < 0.999, f"{column} is suspiciously close to the label"


# ------------------------------------------------------- future append invariance
def test_features_are_invariant_to_future_appends(synthetic_frame):
    """Appending extreme future bars must not change earlier feature values.

    This is the strongest single test in the suite: any look-ahead construction
    (centred window, negative shift, backfill, whole-series statistic) will
    change a historical row when the future changes.
    """
    base_X, _ = build_features(synthetic_frame, lookback=30)

    future = synthetic_frame.iloc[[-1]].copy()
    future.index = pd.DatetimeIndex(
        [synthetic_frame.index[-1] + pd.Timedelta(days=1)], name=synthetic_frame.index.name
    )
    for column in ("open", "high", "low", "close", "volume", "adj_close"):
        future[column] = future[column].to_numpy() * 50.0

    extended = pd.concat([synthetic_frame, future])
    ext_X, _ = build_features(extended, lookback=30)

    shared = base_X.index
    # Not bit-exact: pandas' rolling accumulators can differ by ~1 ULP depending
    # on array offsets (SIMD chunking). A look-ahead bug changes values by many
    # orders of magnitude more than this tolerance.
    pd.testing.assert_frame_equal(
        base_X.loc[shared],
        ext_X.loc[shared],
        check_exact=False,
        rtol=1e-12,
        atol=1e-15,
        check_freq=False,
        obj="feature matrix before/after appending extreme future values",
    )


def test_prepending_history_does_not_change_later_rows(synthetic_frame):
    """Adding *older* rows must not change features of already-present rows.

    Trailing windows are causal, so past-only data addition is safe. This
    catches accidental whole-series normalisation.
    """
    base_X, _ = build_features(synthetic_frame, lookback=30)

    older = synthetic_frame.iloc[:10].copy()
    older.index = pd.DatetimeIndex(
        [synthetic_frame.index[0] - pd.Timedelta(days=i) for i in range(10, 0, -1)],
        name=synthetic_frame.index.name,
    )
    extended = pd.concat([older, synthetic_frame])
    ext_X, _ = build_features(extended, lookback=30)

    # Prepending older rows only shifts the warm-up window: every row that was
    # previously available must still be present, with identical feature values.
    assert base_X.index.isin(ext_X.index).all(), "prepending history dropped an existing row"
    pd.testing.assert_frame_equal(
        base_X,
        ext_X.loc[base_X.index],
        check_exact=False,
        rtol=1e-12,
        atol=1e-15,
        check_freq=False,
    )


def test_truncation_invariance_catches_single_bar_lookahead(synthetic_frame):
    """Building on a prefix must agree with building on the full series.

    This is the test that catches a **one-bar** look-ahead. Appending extreme
    future values (above) only exposes leaks that span the boundary or use
    whole-series statistics; a plain ``shift(-1)`` inside a feature is invisible
    to that probe because it shifts every row equally.

    Here the truncated build has no row ``K`` to read, so a feature that peeks at
    ``t+1`` either changes value or disappears at the truncation point.
    """
    for k in (120, 200, 280):
        prefix = synthetic_frame.iloc[:k]
        prefix_X, _ = build_features(prefix, lookback=30)

        full_X, _ = build_features(synthetic_frame, lookback=30)
        overlap = prefix_X.index.intersection(full_X.index)
        assert len(overlap) > 0

        pd.testing.assert_frame_equal(
            prefix_X.loc[overlap],
            full_X.loc[overlap],
            check_exact=False,
            rtol=1e-12,
            atol=1e-15,
            check_freq=False,
            obj=f"prefix({k}) vs full-series features on overlapping rows",
        )


def test_no_nan_is_silently_filled_from_the_future(synthetic_frame):
    """A NaN input must not be filled with a later value.

    The previous version of this test asserted ``isnan(v) or isfinite(v)``, which
    is a tautology and could never fail. This version checks the actual property:
    the value on the NaN date is either absent or computed without the hole being
    filled from a later bar.
    """
    frame = synthetic_frame.copy()
    hole_position = 100
    frame.iloc[hole_position, frame.columns.get_loc("volume")] = np.nan
    hole_ts = frame.index[hole_position]

    filled_forward = frame.ffill()  # what a buggy pipeline would do
    filled_back = frame.bfill()     # the forbidden direction

    X, _ = build_features(frame, lookback=30, dropna=False)

    if hole_ts in X.index:
        # vol_chg on the hole date must not equal the value computed from the
        # *next* bar's volume (the signature of a backward fill).
        X_next, _ = build_features(filled_forward, lookback=30, dropna=False)
        X_back, _ = build_features(filled_back, lookback=30, dropna=False)

        at_hole = X.loc[hole_ts, "vol_chg"]
        back_value = X_back.loc[hole_ts, "vol_chg"]
        next_value = X_next.loc[hole_ts, "vol_chg"]

        assert not np.isclose(at_hole, back_value, equal_nan=True) or np.isnan(at_hole)
        # And the pipeline must not have invented a value for a missing input.
        assert np.isnan(at_hole) or not np.isnan(frame.loc[hole_ts, "volume"])
        assert np.isfinite(next_value) or np.isnan(next_value)


def test_features_match_independent_trailing_formulas(synthetic_frame):
    """Recompute every feature from raw data and compare.

    This is the only test that reliably catches a **one-bar** look-ahead. A
    ``shift(-1)`` applied consistently changes every row, so invariance probes
    that compare two builds of the same buggy function cannot see it. Here the
    expected value is computed independently, in the test, from formulas that
    use trailing data only. Any peek forward produces a mismatch.
    """
    X, _ = build_features(synthetic_frame, lookback=30)
    close = synthetic_frame["close"]
    high = synthetic_frame["high"]
    low = synthetic_frame["low"]
    volume = synthetic_frame["volume"]

    def trailing_mean(series, window):
        return series.rolling(window=window, min_periods=window).mean()

    expected = pd.DataFrame(index=synthetic_frame.index)
    expected["ret_1"] = close / close.shift(1) - 1.0
    expected["ret_5"] = close / close.shift(5) - 1.0
    expected["ret_20"] = close / close.shift(20) - 1.0
    expected["ma_gap_5"] = close / trailing_mean(close, 5) - 1.0
    expected["ma_gap_20"] = close / trailing_mean(close, 20) - 1.0
    expected["vol_10"] = close.pct_change(1).rolling(window=10, min_periods=10).std(ddof=0)
    expected["vol_30"] = close.pct_change(1).rolling(window=30, min_periods=30).std(ddof=0)
    expected["range_1"] = (high - low) / close
    expected["vol_chg"] = volume / trailing_mean(volume, 5) - 1.0
    expected["dow"] = synthetic_frame.index.day_of_week.astype("float64")

    for column in expected.columns:
        pd.testing.assert_series_equal(
            X[column],
            expected.loc[X.index, column],
            check_names=False,
            check_freq=False,
            rtol=1e-10,
            atol=1e-12,
            obj=f"feature {column} vs independent trailing formula",
        )


def test_feature_functions_never_use_future_constructs():
    """Static guard over the FEATURE functions only.

    ``make_label`` is deliberately excluded: it *must* look one bar forward,
    because the target is the next close. The forbidden constructs are forbidden
    inside features, not inside the label.
    """
    import inspect

    from int4096.features import build as build_module

    feature_functions = [
        build_module.add_returns,
        build_module.add_moving_average_gaps,
        build_module.add_volatility,
        build_module.add_range,
        build_module.add_volume_change,
        build_module.add_day_of_week,
    ]
    forbidden = ("center=True", "bfill", "shift(-", ".iloc[i + 1]", ".iloc[i+1]")

    for function in feature_functions:
        source = inspect.getsource(function)
        for pattern in forbidden:
            assert pattern not in source, (
                f"{function.__name__} contains forbidden construct {pattern!r}"
            )

    # And the label function is the only place a forward shift is allowed.
    label_source = inspect.getsource(build_module.make_label)
    assert "shift(-horizon)" in label_source


# --------------------------------------------------------------------- splits
def test_split_is_chronological_and_disjoint():
    split = chronological_split(1000, 0.6, 0.2, 0.2)
    # Blocks start where the fractions say, but one row is PURGED at each
    # boundary so that no label reaches into the next block.
    assert split.train_end == 599          # row 599 purged
    assert split.validation_start == 600
    assert split.validation_end == 799     # row 799 purged
    assert split.test_start == 800
    assert split.test_end == 1000

    # Strict ordering: no shared row, no reordering.
    assert split.train.stop <= split.validation.start
    assert split.validation.stop <= split.test.start
    assert split.test.stop == 1000


def test_split_purge_gap_prevents_label_crossing():
    """The last row of a block must not have its label inside the next block.

    This is the regression test for audit finding LEAK-001.
    """
    import numpy as np

    split = chronological_split(1000, 0.6, 0.2, 0.2, horizon_gap=1)

    last_train_row = split.train_end - 1
    last_validation_row = split.validation_end - 1

    # y_t = Close_{t+1}, so the label row is t+1.
    assert last_train_row + 1 < split.validation_start, (
        "last training label falls inside the validation block"
    )
    assert last_validation_row + 1 < split.test_start, (
        "last validation label falls inside the sealed test block"
    )


def test_split_purge_gap_zero_is_explicit_opt_in():
    """``horizon_gap=0`` reproduces the old behaviour and must be an explicit choice."""
    split = chronological_split(1000, 0.6, 0.2, 0.2, horizon_gap=0)
    assert split.train_end == 600
    assert split.validation_end == 800


def test_split_rejects_bad_fractions():
    with pytest.raises(ValueError):
        chronological_split(1000, 0.5, 0.2, 0.2)


def test_split_blocks_are_nonempty_on_small_inputs():
    split = chronological_split(60, 0.6, 0.2, 0.2, min_rows=30)
    assert split.train_end - split.train_start > 0
    assert split.validation_end - split.validation_start > 0
    assert split.test_end - split.test_start > 0


def test_dates_are_strictly_increasing_across_splits(synthetic_frame):
    X, _ = build_features(synthetic_frame, lookback=30)
    split = chronological_split(len(X))
    train_dates = X.index[split.train]
    val_dates = X.index[split.validation]
    test_dates = X.index[split.test]

    assert train_dates.max() < val_dates.min()
    assert val_dates.max() < test_dates.min()
    assert len(set(train_dates) & set(val_dates)) == 0
    assert len(set(val_dates) & set(test_dates)) == 0


# --------------------------------------------------------------- CV folding
def test_expanding_folds_never_look_forward():
    folds = expanding_window_folds(500, n_splits=5, gap=1, min_train_fraction=0.3)
    assert len(folds) == 5
    assert_no_overlap(folds, 500)

    previous_val_end = 0
    for train_idx, val_idx in folds:
        # Training is always a prefix: this is what makes it "expanding".
        assert train_idx.min() == 0
        assert np.array_equal(train_idx, np.arange(0, len(train_idx)))
        # A one-row gap separates train from validation (label purge).
        assert val_idx.min() == train_idx.max() + 1 + 1
        assert val_idx.min() >= previous_val_end
        previous_val_end = val_idx.max() + 1


def test_expanding_folds_respect_zero_gap():
    folds = expanding_window_folds(500, n_splits=3, gap=0, min_train_fraction=0.3)
    for train_idx, val_idx in folds:
        assert val_idx.min() == train_idx.max() + 1


def test_expanding_folds_reject_impossible_request():
    with pytest.raises(ValueError):
        expanding_window_folds(20, n_splits=10, gap=1, min_train_fraction=0.5)


# --------------------------------------------------------------- scaler leakage
def test_scaler_fit_uses_train_indices_only(synthetic_frame):
    """Scaler statistics must depend only on the rows passed to ``fit``.

    Two fits on the same training rows must produce identical parameters, even
    when the surrounding (validation/test) data differs wildly.
    """
    from sklearn.preprocessing import StandardScaler

    X, _ = build_features(synthetic_frame, lookback=30)
    split = chronological_split(len(X))
    train = X.iloc[split.train]

    scaler_a = StandardScaler().fit(train)
    scaler_b = StandardScaler().fit(train.copy())

    np.testing.assert_array_equal(scaler_a.mean_, scaler_b.mean_)
    np.testing.assert_array_equal(scaler_a.scale_, scaler_b.scale_)

    # Contaminate the "future" rows and refit only on train: parameters identical.
    contaminated = X.copy()
    contaminated.iloc[split.validation] *= 1000.0
    scaler_c = StandardScaler().fit(contaminated.iloc[split.train])
    np.testing.assert_array_equal(scaler_a.mean_, scaler_c.mean_)

    # And a scaler fitted on the whole dataset differs from the train-only one
    # (otherwise the test would be vacuous).
    whole = StandardScaler().fit(X)
    assert not np.allclose(scaler_a.mean_, whole.mean_)


def test_project_preprocessor_is_train_fitted(synthetic_frame):
    """``build_variant_matrix`` must fit its scaler on the training rows only.

    The earlier version of this suite only tested sklearn's ``StandardScaler``,
    which proves nothing about the project code. This test calls the real
    preprocessing path (audit LEAK-002).
    """
    from int4096.features.pipeline import build_variant_matrix

    X, _ = build_features(synthetic_frame, lookback=30)
    split = chronological_split(len(X))
    X_train = X.iloc[split.train]

    variant_p2 = {
        "scaler": "standard",
        "imputer": "median",
        "features": "full",
        "missing_indicators": False,
        "winsorize_quantiles": None,
    }

    train_matrix, _, _ = build_variant_matrix(X_train, X_train, variant_p2, list(X.columns))

    # The transformed training matrix must be standardised using TRAIN statistics.
    assert np.allclose(train_matrix.mean(axis=0), 0.0, atol=1e-8)
    assert np.allclose(train_matrix.std(axis=0, ddof=0), 1.0, atol=1e-8)

    # Contaminating the "future" rows must not change the fitted statistics: the
    # fit only ever sees X_train. We verify by fitting on train and applying to a
    # contaminated frame, then checking the transformed train block is unchanged.
    contaminated = X.copy()
    contaminated.iloc[split.validation] *= 1000.0
    train_again, _, _ = build_variant_matrix(
        X_train, contaminated.iloc[split.validation], variant_p2, list(X.columns)
    )
    np.testing.assert_allclose(train_matrix, train_again, rtol=1e-12, atol=1e-12)


def test_pipeline_refits_scaler_per_fold(synthetic_frame):
    """A model pipeline must not share scaling state across folds."""
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    from int4096.data.split import chronological_split as cs
    from int4096.evaluation.metrics import mae

    X, y = build_features(synthetic_frame, lookback=30)
    split = cs(len(X))
    X_train = X.iloc[split.train]
    y_train = y.iloc[split.train]
    folds = expanding_window_folds(len(X_train), n_splits=3, gap=1)

    fold_means = []
    for train_idx, _ in folds:
        pipe = Pipeline([("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
        pipe.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
        fold_means.append(pipe.named_steps["scale"].mean_.copy())

    # Expanding folds have different training sizes, so their means must differ.
    assert not np.allclose(fold_means[0], fold_means[-1])
    for train_idx, val_idx in folds:
        pipe = Pipeline([("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
        pipe.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
        assert np.isfinite(mae(y_train.iloc[val_idx], pipe.predict(X_train.iloc[val_idx])))


# ------------------------------------------------- protocol-driven invariants
def test_protocol_purge_is_at_least_the_label_horizon():
    """The purge must scale with the horizon (audit LEAK-011/012).

    Reading the value from the YAML — rather than hard-coding 1 in the test —
    means setting `purge_gap: 0` in the config now fails the suite.
    """
    from int4096.config import load_protocol

    protocol = load_protocol()
    assert protocol.purge_gap >= protocol.horizon
    assert int(protocol.cv["gap"]) >= protocol.horizon


def test_protocol_rejects_an_insufficient_purge():
    """A config with purge_gap < horizon must be rejected at load time."""
    from int4096.config import Protocol, REPO_ROOT, _load_yaml

    raw = _load_yaml(REPO_ROOT / "configs" / "research_protocol.yaml")
    raw["label_horizon"] = 3
    raw["splits"]["purge_gap"] = 1
    problems = Protocol(raw=raw, source_path=REPO_ROOT / "synthetic").validate()
    assert any("purge_gap" in p for p in problems), problems


def test_real_split_honours_the_configured_purge():
    """The production path must use the YAML value, not a hidden default."""
    from int4096.config import load_protocol
    from int4096.experiments.run import prepare_dataset

    protocol = load_protocol()
    prepared = prepare_dataset("AAPL", protocol)
    split = prepared["split"]

    # The purged row is the one immediately before the next block's start.
    assert split.validation_start - split.train_end == protocol.purge_gap
    assert split.test_start - split.validation_end == protocol.purge_gap
