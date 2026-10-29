"""Naive persistence baseline.

``y_hat_t = Close_t`` for the target ``Close_{t+1}``.

This is not a straw man. For near-random-walk price series it is a strong
forecaster, and the project's central honest question is whether any trained
model beats it. It is also the denominator of every skill score reported.
"""

from __future__ import annotations

import numpy as np


def naive_persistence(close_t: np.ndarray) -> np.ndarray:
    """Predict the next close as the current close.

    ``close_t`` must be the *raw close* column aligned to the same rows as the
    design matrix, i.e. ``Close`` at the decision time — never ``Close_{t+1}``.
    """
    values = np.asarray(close_t, dtype="float64")
    if values.ndim != 1:
        raise ValueError(f"Expected a 1-D array of closes, got shape {values.shape}")
    return values.copy()


def moving_average_forecast(close: np.ndarray, window: int = 5) -> np.ndarray:
    """Trailing moving-average forecast, as a simple statistical comparator.

    Rows before the window is full are ``NaN`` and must be aligned/dropped by the
    caller. Provided for context only; it is not a tuned model.
    """
    import pandas as pd

    series = pd.Series(np.asarray(close, dtype="float64"))
    return series.rolling(window=window, min_periods=window).mean().to_numpy()
