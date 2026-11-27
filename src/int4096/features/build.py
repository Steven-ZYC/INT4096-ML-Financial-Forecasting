"""Causal feature construction.

All features are ratios, spreads or trailing-window statistics of quantities
that were observable at the close of bar ``t``. Nothing here uses a centered
window, a negative shift, or a backward fill.

Why ratios rather than price levels
-----------------------------------
Price levels are non-stationary and dominate raw regressors, which makes a
model look accurate while it is only learning "prices near today's price".
Ratios of past prices are scale-free, which is what lets us discuss AAPL and
BTC in the same breath without pretending their dollars are comparable.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

_EPS = 1e-12


def _safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / denominator.replace(0.0, np.nan).where(denominator.abs() > _EPS)


def add_returns(frame: pd.DataFrame, horizons: tuple[int, ...] = (1, 5, 20)) -> pd.DataFrame:
    """Trailing simple returns ``Close_t / Close_{t-h} - 1``."""
    out = pd.DataFrame(index=frame.index)
    close = frame["close"]
    for h in horizons:
        out[f"ret_{h}"] = _safe_div(close, close.shift(h)) - 1.0
    return out


def add_moving_average_gaps(
    frame: pd.DataFrame, windows: tuple[int, ...] = (5, 20), min_periods: int | None = None
) -> pd.DataFrame:
    """``Close_t / SMA_w,t - 1`` using trailing means only."""
    out = pd.DataFrame(index=frame.index)
    close = frame["close"]
    for w in windows:
        # ``min_periods=None`` means "require the full window".
        sma = close.rolling(window=w, min_periods=min_periods or w).mean()
        out[f"ma_gap_{w}"] = _safe_div(close, sma) - 1.0
    return out


def add_volatility(
    frame: pd.DataFrame,
    windows: tuple[int, ...] = (10, 30),
    min_periods: int | None = None,
    return_horizon: int = 1,
) -> pd.DataFrame:
    """Trailing realized volatility of 1-bar returns."""
    out = pd.DataFrame(index=frame.index)
    rets = frame["close"].pct_change(return_horizon, fill_method=None)
    for w in windows:
        out[f"vol_{w}"] = rets.rolling(
            window=w, min_periods=min_periods or w
        ).std(ddof=0)
    return out


def add_range(frame: pd.DataFrame) -> pd.DataFrame:
    """Intra-bar dispersion ``(High_t - Low_t) / Close_t``."""
    out = pd.DataFrame(index=frame.index)
    out["range_1"] = _safe_div(frame["high"] - frame["low"], frame["close"])
    return out


def add_volume_change(
    frame: pd.DataFrame, window: int = 5, min_periods: int | None = None
) -> pd.DataFrame:
    """``Volume_t / SMA_w(Volume)_t - 1`` — a trailing volume anomaly."""
    out = pd.DataFrame(index=frame.index)
    sma = frame["volume"].rolling(
        window=window, min_periods=min_periods or window
    ).mean()
    out["vol_chg"] = _safe_div(frame["volume"], sma) - 1.0
    return out


def add_day_of_week(frame: pd.DataFrame) -> pd.DataFrame:
    """Calendar index 0..6. A real effect for equities; mostly noise for BTC."""
    out = pd.DataFrame(index=frame.index)
    # ``day_of_week`` (pandas >= 2.2) replaces the deprecated ``dayofweek``.
    index = frame.index
    accessor = index.day_of_week if hasattr(index, "day_of_week") else index.dayofweek
    out["dow"] = accessor.astype("float64")
    return out


FEATURE_FUNCTIONS = {
    "returns": add_returns,
    "ma_gaps": add_moving_average_gaps,
    "volatility": add_volatility,
    "range": add_range,
    "volume_change": add_volume_change,
    "day_of_week": add_day_of_week,
}

DEFAULT_FEATURES = [
    "ret_1",
    "ret_5",
    "ret_20",
    "ma_gap_5",
    "ma_gap_20",
    "vol_10",
    "vol_30",
    "range_1",
    "vol_chg",
    "dow",
]

REDUCED_FEATURES = ["ret_1", "ret_5", "range_1", "vol_chg", "dow"]


def feature_dictionary() -> list[dict[str, str]]:
    """Documentation table for the feature set (used in the report)."""
    return [
        {"feature": "ret_1", "definition": "Close_t / Close_{t-1} - 1", "window": "1"},
        {"feature": "ret_5", "definition": "Close_t / Close_{t-5} - 1", "window": "5"},
        {"feature": "ret_20", "definition": "Close_t / Close_{t-20} - 1", "window": "20"},
        {
            "feature": "ma_gap_5",
            "definition": "Close_t / SMA_5,t - 1 (trailing mean)",
            "window": "5",
        },
        {
            "feature": "ma_gap_20",
            "definition": "Close_t / SMA_20,t - 1 (trailing mean)",
            "window": "20",
        },
        {
            "feature": "vol_10",
            "definition": "trailing std of 1-bar returns",
            "window": "10",
        },
        {
            "feature": "vol_30",
            "definition": "trailing std of 1-bar returns",
            "window": "30",
        },
        {"feature": "range_1", "definition": "(High_t - Low_t) / Close_t", "window": "1"},
        {
            "feature": "vol_chg",
            "definition": "Volume_t / SMA_5(Volume)_t - 1",
            "window": "5",
        },
        {"feature": "dow", "definition": "day of week, 0=Monday", "window": "0"},
    ]


def make_label(
    frame: pd.DataFrame,
    label_field: str = "close",
    horizon: int = 1,
    mode: str = "level",
) -> pd.Series:
    """Build the training target for horizon ``t+horizon``.

    ``mode='level'`` -> ``y_t = Close_{t+h}``
    ``mode='delta'`` -> ``y_t = Close_{t+h} - Close_t``

    The final ``horizon`` rows have no observable future price and become NaN,
    so ``build_features`` drops them. The label is *never* a column of ``X``.

    Why two modes: the project reports error on the next close **price**, but a
    model whose features are all scale-free ratios cannot recover a price level
    and collapses toward the training mean. Training on the *change* and adding
    it back to the known ``Close_t`` keeps the reported estimand identical while
    removing that representation artefact. Both modes are information-equivalent
    because ``Close_t`` is known at decision time.
    """
    future = frame[label_field].shift(-horizon)
    if mode == "level":
        label = future
        label.name = f"y_next_{label_field}"
    elif mode == "delta":
        label = future - frame[label_field]
        label.name = f"y_delta_{label_field}"
    else:
        raise ValueError(f"Unknown label mode {mode!r}; expected 'level' or 'delta'")
    return label


def build_features(
    frame: pd.DataFrame,
    feature_columns: list[str] | None = None,
    label_field: str = "close",
    horizon: int = 1,
    lookback: int = 30,
    min_periods: int | None = None,
    dropna: bool = True,
    mode: str = "level",
) -> tuple[pd.DataFrame, pd.Series]:
    """Build the design matrix ``X`` and label ``y`` for one asset.

    Returns ``(X, y)`` where both share the identical index and every ``X``
    row uses only information available at the close of its own timestamp.
    """
    feature_columns = list(feature_columns) if feature_columns is not None else list(DEFAULT_FEATURES)

    parts = [
        add_returns(frame),
        add_moving_average_gaps(frame, min_periods=min_periods),
        add_volatility(frame, min_periods=min_periods),
        add_range(frame),
        add_volume_change(frame, min_periods=min_periods),
        add_day_of_week(frame),
    ]
    features = pd.concat(parts, axis=1)
    features.index.name = frame.index.name

    unknown = [c for c in feature_columns if c not in features.columns]
    if unknown:
        raise KeyError(
            f"Requested features not produced: {unknown}. "
            f"Available: {sorted(features.columns)}"
        )
    features = features[feature_columns]

    label = make_label(frame, label_field=label_field, horizon=horizon, mode=mode)

    # Rolling warm-up: drop the first `lookback` rows rather than back-filling.
    # Back-filling would move information backwards in time.
    if lookback > 0:
        features = features.iloc[lookback:]
        label = label.iloc[lookback:]

    if dropna:
        # Only drop rows where an *input* or the *label* is genuinely missing.
        # The terminal rows lose their label because t+1 does not exist yet.
        keep = features.notna().all(axis=1) & label.notna()
        features = features.loc[keep]
        label = label.loc[keep]

    return features, label
