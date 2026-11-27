"""Cross-run analysis: bootstrap skill intervals and return autocorrelation.

Writes ``experiments/analysis/uncertainty_and_signal.json`` from the stored
validation predictions and the data snapshots. Nothing is retrained.

Usage (from the repository root):
    python -m int4096.evaluation.analysis
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ..data.load import load_snapshot
from ..paths import ANALYSIS, RUNS_ROOT, run_files
from .metrics import moving_block_bootstrap

OUTPUT_NAME = "uncertainty_and_signal.json"
BLOCK_LENGTH = 10
RESAMPLES = 1000
SEED = 42


def return_autocorrelation() -> dict[str, dict[str, float]]:
    """Lag-1 autocorrelation of daily close-to-close returns, per asset."""
    out = {}
    for asset in ("AAPL", "BTC"):
        returns = load_snapshot(asset)["close"].pct_change(1, fill_method=None).dropna()
        rho = float(returns.autocorr(lag=1))
        out[asset] = {
            "lag1_autocorrelation": round(rho, 5),
            "r2_lag1": round(rho**2, 6),
            "n_obs": int(len(returns)),
        }
    return out


def skill_intervals(runs_root: Path | None = None) -> list[dict]:
    """Moving-block bootstrap interval of MAE skill for every stored run."""
    rows = []
    paths = run_files("predictions.csv", root=runs_root or RUNS_ROOT)
    for path in sorted(paths, key=lambda p: p.parent.name):  # chronological
        frame = pd.read_csv(path)
        frame = frame[frame["split"] == "validation"]
        result = moving_block_bootstrap(
            frame["y_true"], frame["y_pred"], frame["y_naive"],
            block_length=BLOCK_LENGTH, n_resamples=RESAMPLES, seed=SEED,
        )
        error = (frame["y_true"] - frame["y_pred"]).abs().mean()
        rows.append(
            {
                "run_id": path.parent.name,
                "mae": round(float(error), 4),
                "skill_mae": round(result["skill_mae"], 6),
                "ci_low": round(result["ci_low"], 6),
                "ci_high": round(result["ci_high"], 6),
                "ci_excludes_zero": bool(result["ci_low"] > 0 or result["ci_high"] < 0),
            }
        )
    return rows


def build_summary(runs_root: Path | None = None) -> dict:
    intervals = skill_intervals(runs_root)
    excluding = sum(row["ci_excludes_zero"] for row in intervals)
    return {
        "generated_from": "experiments/models/*/predictions.csv",
        "note": "derived analysis; no retraining",
        "return_autocorrelation": return_autocorrelation(),
        "skill_intervals": intervals,
        "summary": {
            "runs": len(intervals),
            "ci_includes_zero": len(intervals) - excluding,
            "ci_excludes_zero": excluding,
            "max_skill": max(row["skill_mae"] for row in intervals),
            "min_skill": min(row["skill_mae"] for row in intervals),
        },
    }


def write_summary(output_dir: Path | None = None, runs_root: Path | None = None) -> Path:
    path = Path(output_dir or ANALYSIS) / OUTPUT_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_summary(runs_root), indent=2) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":  # pragma: no cover
    print(f"wrote {write_summary()}")
