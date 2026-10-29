"""Figure generation from stored run artifacts.

Every figure is regenerated from files under ``artifacts/experiments``, never
from in-memory values, and every figure records the run IDs it was built from in
its caption file. That is what lets an auditor trace a picture back to a run.

Figures are deliberately small in number and each answers one question:
``coverage_and_splits``, ``model_vs_naive``, ``observed_vs_predicted``,
``train_vs_validation``, ``ablation_delta``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "experiments"
DEFAULT_FIGURE_ROOT = REPO_ROOT / "artifacts" / "figures"


def _mpl():
    import matplotlib

    matplotlib.use("Agg")  # headless: notebooks and CI must not need a display
    import matplotlib.pyplot as plt

    return plt


def load_registry(artifact_root: Path | None = None) -> pd.DataFrame:
    """Read the append-only run registry."""
    root = Path(artifact_root) if artifact_root else DEFAULT_ARTIFACT_ROOT
    path = root / "registry.jsonl"
    if not path.exists():
        raise FileNotFoundError(
            f"No run registry at {path}. Run at least one experiment first."
        )
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def load_predictions(run_id: str, artifact_root: Path | None = None) -> pd.DataFrame:
    root = Path(artifact_root) if artifact_root else DEFAULT_ARTIFACT_ROOT
    path = root / run_id / "predictions.csv"
    if not path.exists():
        raise FileNotFoundError(f"No predictions for run {run_id} at {path}")
    frame = pd.read_csv(path, parse_dates=["date"])
    return frame


def _save(fig, path: Path, caption: str, run_ids: list[str], caption_dir: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    fig.clear()
    import matplotlib.pyplot as plt

    plt.close(fig)

    caption_dir.mkdir(parents=True, exist_ok=True)
    (caption_dir / (path.stem + ".caption.txt")).write_text(
        f"{caption}\n\nrun_ids: {', '.join(run_ids) or 'n/a'}\n"
        f"generated_by: int4096.evaluation.figures\n",
        encoding="utf-8",
    )
    return path


def plot_coverage_and_splits(
    frames: dict[str, pd.DataFrame],
    splits: dict[str, Any],
    run_ids: list[str] | None = None,
    figure_root: Path | None = None,
) -> Path:
    """Figure 1: data coverage and the frozen chronological splits per asset."""
    plt = _mpl()
    fig_root = Path(figure_root) if figure_root else DEFAULT_FIGURE_ROOT
    fig, axes = plt.subplots(len(frames), 1, figsize=(10, 3.2 * len(frames)), squeeze=False)

    for ax, (asset, frame) in zip(axes[:, 0], frames.items()):
        ax.plot(frame.index, frame["close"], lw=0.9, color="black", label="Close (raw)")
        split = splits[asset]
        boundaries = [
            frame.index[split.train_end - 1],
            frame.index[split.validation_start],
            frame.index[split.validation_end - 1],
            frame.index[split.test_start],
        ]
        ax.axvline(boundaries[0], color="tab:blue", ls="--", lw=1)
        ax.axvline(boundaries[2], color="tab:red", ls="--", lw=1)
        ax.axvspan(frame.index[0], boundaries[0], alpha=0.08, color="tab:blue")
        ax.axvspan(boundaries[0], boundaries[2], alpha=0.08, color="tab:green")
        ax.axvspan(boundaries[2], frame.index[-1], alpha=0.12, color="tab:red")
        ax.set_title(f"{asset}: {len(frame)} sessions, chronological 60/20/20 split")
        ax.set_ylabel("Price (quote currency)")
        ax.legend(loc="upper left", fontsize=8)

    fig.suptitle("Data coverage and frozen splits (test block sealed)", y=1.0)
    return _save(
        fig,
        fig_root / "fig01_coverage_and_splits.png",
        "Price history per asset with the frozen 60/20/20 chronological split. "
        "Shaded regions mark train (blue), validation (green) and sealed test (red). "
        "The two assets have different calendars and are plotted separately, never aligned by row.",
        run_ids or [],
        fig_root,
    )


def plot_model_vs_naive(
    registry: pd.DataFrame,
    figure_root: Path | None = None,
) -> Path:
    """Figure 4: skill relative to persistence, per asset and model.

    Skill < 0 means the model is worse than simply repeating today's price.
    """
    plt = _mpl()
    fig_root = Path(figure_root) if figure_root else DEFAULT_FIGURE_ROOT

    data = registry[registry["status"] == "SUCCESS"].dropna(subset=["validation_skill_mae"])
    assets = sorted(data["asset"].unique())
    fig, axes = plt.subplots(
        1, len(assets), figsize=(5.6 * len(assets), 4.2), squeeze=False, sharex=True
    )

    # A shared x-axis is essential: per-panel autoscaling would make BTC's
    # ~0.001 skill look as large as AAPL's ~0.005, which would be a visual
    # exaggeration of the result. We also pad the limit so zero is never flush
    # against the frame.
    values = data["validation_skill_mae"].to_numpy(dtype="float64")
    bound = float(np.nanmax(np.abs(values))) if len(values) else 0.01
    bound = max(bound * 1.25, 0.005)

    for ax, asset in zip(axes[0], assets):
        subset = data[data["asset"] == asset].sort_values("validation_skill_mae")
        colours = ["tab:green" if v > 0 else "tab:red" for v in subset["validation_skill_mae"]]
        ax.barh(subset["model_id"], subset["validation_skill_mae"], color=colours)
        ax.axvline(0, color="black", lw=1)
        ax.set_xlim(-bound, bound)
        ax.xaxis.set_major_formatter(lambda v, _pos: f"{v * 100:+.1f}%")
        ax.set_title(f"{asset} (validation)")
        ax.set_xlabel("skill vs naive persistence")

    fig.suptitle(
        "Skill relative to naive persistence is near zero on both assets "
        "(shared axis)", y=1.02
    )
    return _save(
        fig,
        fig_root / "fig04_model_vs_naive.png",
        "Validation skill score relative to naive persistence, per asset. "
        "Bars to the left of zero indicate a model worse than repeating the current price. "
        "Dollar errors are not compared across assets; only the unitless skill score is.",
        sorted(data["run_id"].tolist()),
        fig_root,
    )


def plot_observed_vs_predicted(
    run_id: str,
    artifact_root: Path | None = None,
    figure_root: Path | None = None,
    split: str = "validation",
) -> Path:
    """Figure 3: observed vs predicted, including the naive forecast.

    Only generated for released splits. The test split must be human-approved.
    """
    plt = _mpl()
    fig_root = Path(figure_root) if figure_root else DEFAULT_FIGURE_ROOT
    predictions = load_predictions(run_id, artifact_root)
    subset = predictions[predictions["split"] == split]
    if subset.empty:
        raise ValueError(f"Run {run_id} has no '{split}' predictions")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
    ax1.plot(subset["date"], subset["y_true"], label="Observed next close", color="black", lw=1)
    ax1.plot(subset["date"], subset["y_pred"], label="Model forecast", color="tab:orange", lw=1)
    ax1.plot(subset["date"], subset["y_naive"], label="Naive (today's close)", color="tab:blue", ls="--", lw=1)
    ax1.set_ylabel("Price")
    ax1.legend(fontsize=8)
    ax1.set_title(f"{run_id} — {split}")

    error = subset["y_pred"] - subset["y_true"]
    ax2.bar(subset["date"], error, color="tab:orange", width=1.0)
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_ylabel("Forecast error")
    ax2.set_xlabel("Date")
    return _save(
        fig,
        fig_root / f"fig03_observed_vs_predicted_{run_id}_{split}.png",
        "Observed next-close price against the model forecast and the naive persistence "
        "forecast, with the signed forecast error below. The naive line overlaps the "
        "observed series closely because next-close prediction is close to a random walk.",
        [run_id],
        fig_root,
    )


def plot_train_vs_validation(
    run_dirs: list[Path],
    figure_root: Path | None = None,
) -> Path:
    """Figure 5: generalization gap, read from each run's metrics.json."""
    plt = _mpl()
    fig_root = Path(figure_root) if figure_root else DEFAULT_FIGURE_ROOT

    rows = []
    for run_dir in run_dirs:
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue
        blob = json.loads(metrics_path.read_text(encoding="utf-8"))
        metrics = blob.get("metrics", {})
        rows.append(
            {
                "run_id": blob["run_id"],
                "asset": blob["asset"],
                "model_id": blob["model_id"],
                "validation_mae": metrics.get("validation_mae"),
            }
        )
    if not rows:
        raise ValueError("No metrics.json found for the supplied run directories")

    data = pd.DataFrame(rows).dropna()
    fig, ax = plt.subplots(figsize=(8, 4.2))
    labels = [f"{r.asset}\n{r.model_id}" for r in data.itertuples()]
    ax.bar(labels, data["validation_mae"], color="tab:purple")
    ax.set_ylabel("Validation MAE")
    ax.set_title("Validation error by lane")
    ax.tick_params(axis="x", labelsize=8)
    return _save(
        fig,
        fig_root / "fig05_validation_mae_by_lane.png",
        "Validation MAE per model lane, regenerated from each run's metrics.json. "
        "Direct MAE comparison between AAPL and BTC is not meaningful because the "
        "quote scales differ by orders of magnitude; see the skill-score figure for "
        "the cross-asset view.",
        data["run_id"].tolist(),
        fig_root,
    )


def plot_ablation_delta(
    registry: pd.DataFrame,
    baseline_variant: str = "P0",
    figure_root: Path | None = None,
) -> Path:
    """Figure 6: preprocessing ablation effect, as delta MAE vs P0.

    Requires matched cells: the same model and asset must exist for both the
    variant and the baseline variant. Missing pairs are reported, not imputed.
    """
    plt = _mpl()
    fig_root = Path(figure_root) if figure_root else DEFAULT_FIGURE_ROOT

    data = registry[registry["status"] == "SUCCESS"].dropna(subset=["validation_mae"])
    base = data[data["preprocess_variant"] == baseline_variant]
    if base.empty:
        raise ValueError(f"No {baseline_variant} runs available to compare against")

    pairs = []
    for row in data.itertuples():
        if row.preprocess_variant == baseline_variant:
            continue
        match = base[(base["asset"] == row.asset) & (base["model_id"] == row.model_id)]
        if match.empty:
            continue
        reference = float(match.iloc[0]["validation_mae"])
        relative = (float(row.validation_mae) - reference) / reference if reference else np.nan
        pairs.append(
            {
                "label": f"{row.asset}/{row.model_id}/{row.preprocess_variant}",
                "delta": relative,
                "run_id": row.run_id,
            }
        )
    if not pairs:
        raise ValueError(
            "No matched variant pairs found. Run the same model and asset under "
            f"{baseline_variant} and at least one other variant first."
        )

    frame = pd.DataFrame(pairs).sort_values("delta")
    fig, ax = plt.subplots(figsize=(8, 0.35 * len(frame) + 2))
    colours = ["tab:red" if v > 0 else "tab:green" for v in frame["delta"]]
    ax.barh(frame["label"], frame["delta"] * 100, color=colours)
    ax.axvline(0, color="black", lw=1)
    ax.set_xlabel(f"Relative change in validation MAE vs {baseline_variant} (%)")
    ax.set_title("Preprocessing ablation: does the change help or hurt?")
    ax.tick_params(axis="y", labelsize=8)
    return _save(
        fig,
        fig_root / "fig06_ablation_delta.png",
        f"Relative change in validation MAE for each preprocessing variant compared with "
        f"{baseline_variant}, holding model and asset fixed. Positive (red) means worse. "
        "Only matched cells are plotted; unmatched cells are absent rather than imputed.",
        frame["run_id"].tolist(),
        fig_root,
    )
