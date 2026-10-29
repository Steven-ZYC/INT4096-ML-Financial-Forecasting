"""Metrics — the single source of truth for reported numbers.

Definitions
-----------
MAE           mean(|y - y_hat|)                       [quote currency]
RMSE          sqrt(mean((y - y_hat)^2))               [quote currency]
R^2           1 - SS_res / SS_tot                     [unitless, inflated by trend]
skill_MAE     1 - MAE_model / MAE_naive               [unitless, 0 = no better]
skill_RMSE    1 - RMSE_model / RMSE_naive             [unitless]
normalized_MAE  MAE / mean(|y|)                       [unitless, cross-asset safe]

Interpretation rules enforced by the report and the auditors:

* MSE-based metrics penalize large misses more; on volatile assets RMSE grows
  much faster than MAE, so a model can look fine on MAE and poor on RMSE.
* R^2 on a trending price level is easy to score highly on, because the label
  variance is dominated by the trend. A naive forecast therefore has high R^2.
  We report it because the rubric expects it, and we say this out loud.
* Dollar errors are **not** comparable across AAPL and BTC. Cross-asset
  statements use ``skill_MAE`` or ``normalized_MAE``.
* Skill scores are the primary comparative metric. Negative skill means "worse
  than looking at today's price", which is a legitimate finding.
"""

from __future__ import annotations

from typing import Any, Iterable

import numpy as np


def _paired(y_true, y_pred) -> tuple[np.ndarray, np.ndarray]:
    true = np.asarray(y_true, dtype="float64").ravel()
    pred = np.asarray(y_pred, dtype="float64").ravel()
    if true.shape != pred.shape:
        raise ValueError(f"Shape mismatch: y_true {true.shape} vs y_pred {pred.shape}")
    mask = np.isfinite(true) & np.isfinite(pred)
    if not mask.any():
        raise ValueError("No finite paired observations to evaluate.")
    return true[mask], pred[mask]


def mae(y_true, y_pred) -> float:
    true, pred = _paired(y_true, y_pred)
    return float(np.mean(np.abs(true - pred)))


def rmse(y_true, y_pred) -> float:
    true, pred = _paired(y_true, y_pred)
    return float(np.sqrt(np.mean((true - pred) ** 2)))


def r2(y_true, y_pred) -> float:
    true, pred = _paired(y_true, y_pred)
    ss_res = float(np.sum((true - pred) ** 2))
    ss_tot = float(np.sum((true - np.mean(true)) ** 2))
    if ss_tot == 0.0:
        return float("nan")
    return 1.0 - ss_res / ss_tot


def mape(y_true, y_pred) -> float:
    """Mean absolute percentage error. Undefined for zero/negative labels."""
    true, pred = _paired(y_true, y_pred)
    if np.any(np.abs(true) < 1e-12):
        return float("nan")
    return float(np.mean(np.abs((true - pred) / true)) * 100.0)


def skill_score(model_error: float, baseline_error: float) -> float:
    """``1 - model/baseline``. Positive is better than the baseline.

    Returns NaN when the baseline error is not positive, rather than silently
    producing an infinite or fabricated score.
    """
    if not np.isfinite(model_error) or not np.isfinite(baseline_error) or baseline_error <= 0:
        return float("nan")
    return float(1.0 - model_error / baseline_error)


def normalized_mae(y_true, y_pred) -> float:
    """MAE divided by the mean absolute label magnitude (cross-asset safe)."""
    true, pred = _paired(y_true, y_pred)
    scale = float(np.mean(np.abs(true)))
    if scale <= 0:
        return float("nan")
    return float(np.mean(np.abs(true - pred)) / scale)


def direction_accuracy(y_true, y_pred, reference=None) -> float:
    """Share of *directional calls* that have the right sign.

    ``reference`` is the decision-time value (``Close_t``). The realized change is
    ``y_true - reference``; the predicted change is ``y_pred - reference``.

    A prediction that exactly equals the reference makes **no directional call**
    (it is a tie). Ties are excluded from the denominator rather than scored as
    wrong, and :func:`direction_tie_rate` reports how many were excluded. Without
    this, the naive persistence baseline would always score exactly 0.0, which is
    a meaningless artefact rather than a result.

    Returns ``NaN`` when there is no directional call at all, so the report shows
    "n/a" instead of a fake zero.

    This is a **secondary diagnostic**, not a trading signal: it ignores
    magnitude, transaction costs and risk.
    """
    true = np.asarray(y_true, dtype="float64").ravel()
    pred = np.asarray(y_pred, dtype="float64").ravel()
    ref = np.asarray(reference, dtype="float64").ravel() if reference is not None else true - 1.0
    mask = np.isfinite(true) & np.isfinite(pred) & np.isfinite(ref)
    if not mask.any():
        return float("nan")
    realized = np.sign(true[mask] - ref[mask])
    predicted = np.sign(pred[mask] - ref[mask])
    decisive = predicted != 0.0
    if not decisive.any():
        return float("nan")
    return float(np.mean(realized[decisive] == predicted[decisive]))


def direction_tie_rate(y_pred, reference) -> float:
    """Share of rows where the prediction makes no directional call."""
    pred = np.asarray(y_pred, dtype="float64").ravel()
    ref = np.asarray(reference, dtype="float64").ravel()
    mask = np.isfinite(pred) & np.isfinite(ref)
    if not mask.any():
        return float("nan")
    return float(np.mean(np.sign(pred[mask] - ref[mask]) == 0.0))


def evaluate_predictions(
    y_true,
    y_pred,
    y_naive,
    reference=None,
) -> dict[str, float]:
    """Full metric bundle for one model on one evaluation block."""
    result: dict[str, float] = {}
    model_mae = mae(y_true, y_pred)
    model_rmse = rmse(y_true, y_pred)
    naive_mae = mae(y_true, y_naive)
    naive_rmse = rmse(y_true, y_naive)

    result["mae"] = model_mae
    result["rmse"] = model_rmse
    result["r2"] = r2(y_true, y_pred)
    result["mape_pct"] = mape(y_true, y_pred)
    result["normalized_mae"] = normalized_mae(y_true, y_pred)

    result["baseline_mae"] = naive_mae
    result["baseline_rmse"] = naive_rmse
    result["baseline_r2"] = r2(y_true, y_naive)

    result["skill_mae"] = skill_score(model_mae, naive_mae)
    result["skill_rmse"] = skill_score(model_rmse, naive_rmse)

    if reference is not None:
        result["direction_accuracy"] = direction_accuracy(y_true, y_pred, reference)
        result["direction_tie_rate"] = direction_tie_rate(y_pred, reference)
        result["baseline_direction_accuracy"] = direction_accuracy(y_true, y_naive, reference)
        result["baseline_direction_tie_rate"] = direction_tie_rate(y_naive, reference)

    result["n_obs"] = float(len(_paired(y_true, y_pred)[0]))
    return {k: float(v) for k, v in result.items()}


def moving_block_bootstrap(
    y_true,
    y_pred,
    y_naive,
    block_length: int = 10,
    n_resamples: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict[str, float]:
    """Bootstrap interval for the MAE skill score.

    Consecutive errors are dependent in a time series, so we resample **blocks
    of consecutive observations** rather than individual rows. This still
    understates dependence (blocks overlap in the autocorrelation structure),
    so the interval is **indicative**, not a confirmatory test.

    Returns the point estimate and percentile bounds of ``skill_mae``.
    """
    true, pred = _paired(y_true, y_pred)
    _, naive = _paired(y_true, y_naive)
    n = len(true)
    if n < block_length * 2:
        return {
            "skill_mae": skill_score(mae(true, pred), mae(true, naive)),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n_obs": float(n),
            "note": "too few observations for block bootstrap",
        }

    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block_length))
    max_start = n - block_length
    point = skill_score(mae(true, pred), mae(true, naive))

    samples = np.empty(n_resamples, dtype="float64")
    for b in range(n_resamples):
        starts = rng.integers(0, max_start + 1, size=n_blocks)
        idx = np.concatenate([np.arange(s, s + block_length) for s in starts])[:n]
        samples[b] = skill_score(
            mae(true[idx], pred[idx]), mae(true[idx], naive[idx])
        )

    alpha = (1.0 - confidence) / 2.0
    finite = samples[np.isfinite(samples)]
    if finite.size == 0:
        low = high = float("nan")
    else:
        low, high = np.quantile(finite, [alpha, 1.0 - alpha])
    return {
        "skill_mae": float(point),
        "ci_low": float(low),
        "ci_high": float(high),
        "n_obs": float(n),
        "block_length": float(block_length),
        "n_resamples": float(n_resamples),
        "note": "moving-block bootstrap over consecutive dates; indicative only",
    }


def summarize_table(rows: Iterable[dict[str, Any]]) -> str:
    """Markdown table for the handoff/report. Never invents missing values."""
    headers = ["model", "variant", "asset", "mae", "rmse", "r2", "skill_mae", "n"]
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        cells = []
        for key in headers:
            value = row.get(key)
            if isinstance(value, float):
                cells.append("n/a" if not np.isfinite(value) else f"{value:.4g}")
            else:
                cells.append("n/a" if value is None else str(value))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)
