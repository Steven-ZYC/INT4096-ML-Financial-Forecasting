"""Shared test fixtures.

All fixtures are synthetic and deterministic. Tests must never touch the
network: a test that downloads data is a test that fails on a plane, in Colab
with a different provider policy, and during marking.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def make_series(n: int = 300, start: float = 100.0, drift: float = 0.0005,
                noise: float = 0.01, seed: int = 7) -> pd.DataFrame:
    """A deterministic synthetic OHLCV frame with a canonical index."""
    rng = np.random.default_rng(seed)
    returns = rng.normal(drift, noise, size=n)
    close = start * np.exp(np.cumsum(returns))
    high = close * (1 + np.abs(rng.normal(0, 0.004, size=n)))
    low = close * (1 - np.abs(rng.normal(0, 0.004, size=n)))
    open_ = low + (high - low) * rng.random(n)
    volume = rng.integers(1_000_000, 5_000_000, size=n).astype("float64")
    index = pd.date_range("2021-01-04", periods=n, freq="B", tz="UTC", name="ts")
    frame = pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "adj_close": close * 0.99,
        },
        index=index,
    )
    frame.attrs["asset"] = "SYNTHETIC"
    return frame


@pytest.fixture
def synthetic_frame() -> pd.DataFrame:
    return make_series()


@pytest.fixture
def tiny_frame() -> pd.DataFrame:
    return make_series(n=12, noise=0.005, seed=3)


@pytest.fixture
def long_frame() -> pd.DataFrame:
    return make_series(n=400, noise=0.012, seed=11)
