"""Generate every number and figure the slide deck uses, from committed artifacts.

The deck must not contain a hand-typed empirical value. This script reads

  artifacts/experiments/*/manifest.json   (budget, commit, protocol)
  artifacts/experiments/*/metrics.json    (validation metrics)
  artifacts/experiments/*/config.json     (tuning budget actually used)
  artifacts/experiments/*/predictions.csv (one real worked example)
  artifacts/analysis/uncertainty_and_signal.json (bootstrap intervals, autocorrelation)

and emits `slides/latex/generated/numbers.tex` plus the vector figures.

Run via `bash slides/build.sh`.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.evaluation import figures  # noqa: E402
from int4096.experiments.run import prepare_dataset  # noqa: E402

SLIDES = REPO_ROOT / "slides" / "latex"
GENERATED = SLIDES / "generated"
FIGURES = SLIDES / "figures"
ARTIFACTS = REPO_ROOT / "artifacts" / "experiments"

# Figures used in the main narrative (and backups).
WANTED = [
    "fig01_coverage_and_splits",
    "fig04_model_vs_naive",
    "fig06_ablation_delta",
    "fig07_feature_importance_aapl",
]

LABELS = {
    "linear_baseline": "Linear (near-unregularised)",
    "ridge": "Ridge",
    "svr": "SVR (RBF)",
    "random_forest": "Random forest",
    "hist_gradient_boosting": "Hist.\\ gradient boosting",
}


def pct(value: float, digits: int = 2) -> str:
    return f"{value * 100:+.{digits}f}"


def num(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def load_runs() -> list[dict]:
    """One record per executed cell, with metrics and the budget it used."""
    runs = []
    for manifest_path in sorted(ARTIFACTS.glob("*/manifest.json")):
        directory = manifest_path.parent
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        metrics_path = directory / "metrics.json"
        if not metrics_path.exists():
            continue
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))["metrics"]

        budget = (500, 500.0)
        config_path = directory / "config.json"
        if config_path.exists():
            config = json.loads(config_path.read_text(encoding="utf-8"))
            budget = (config.get("max_trials"), config.get("max_seconds"))

        runs.append(
            {
                "run_id": manifest["run_id"],
                "asset": manifest["asset"],
                "model_id": manifest["model_id"],
                "variant": manifest["preprocess_variant"],
                "skill_mae": metrics.get("validation_skill_mae"),
                "mae": metrics.get("validation_mae"),
                "baseline_mae": metrics.get("validation_baseline_mae"),
                "n_obs": metrics.get("validation_n_obs"),
                "trials": budget[0],
                "seconds": budget[1],
                "attempted": len(manifest.get("fold_metrics", [])),
            }
        )
    return runs


def build_macros(runs: list[dict], protocol) -> dict[str, str]:
    m: dict[str, str] = {}
    runs = [r for r in runs if r["skill_mae"] is not None]

    pairs = {(r["asset"], r["model_id"]) for r in runs}
    m["NRunTotal"] = str(len(runs))
    m["NPairTotal"] = str(len(pairs))

    below = [r for r in runs if r["skill_mae"] < 0]
    below_pairs = {(r["asset"], r["model_id"]) for r in below}
    m["NBelowBaseline"] = str(len(below))
    m["NPairsBelowBaseline"] = str(len(below_pairs))

    # Best configuration per asset, across ALL preprocessing variants.
    for asset in ("AAPL", "BTC"):
        subset = [r for r in runs if r["asset"] == asset]
        best = max(subset, key=lambda r: r["skill_mae"])
        m[f"Best{asset}ModelAll"] = LABELS.get(best["model_id"], best["model_id"])
        m[f"Best{asset}VariantAll"] = best["variant"]
        m[f"Best{asset}SkillAll"] = pct(best["skill_mae"])

        # Best within the standardised (P2) slice used in the results table.
        p2 = [r for r in subset if r["variant"] == "P2"]
        best_p2 = max(p2, key=lambda r: r["skill_mae"])
        m[f"Best{asset}ModelPtwo"] = LABELS.get(best_p2["model_id"], best_p2["model_id"])
        m[f"Best{asset}SkillPtwo"] = pct(best_p2["skill_mae"])

        m[f"NaiveMae{asset}"] = num(subset[0]["baseline_mae"])
        m[f"NValObs{asset}"] = str(int(subset[0]["n_obs"]))

        for r in subset:
            key = "".join(p.capitalize() for p in r["model_id"].split("_"))
            if r["variant"] == "P2":
                m[f"Skill{asset}{key}"] = pct(r["skill_mae"])
                m[f"Mae{asset}{key}"] = num(r["mae"])

    skills = [r["skill_mae"] for r in runs]
    m["SkillMin"] = pct(min(skills))
    m["SkillMax"] = pct(max(skills))
    m["SkillSpan"] = f"{(max(skills) - min(skills)) * 100:.2f}"

    # Budget actually used (this is what the deck must state).
    m["TrialsUsed"] = str(runs[0]["trials"])
    m["SecondsUsed"] = str(int(runs[0]["seconds"]))
    m["TrialsMax"] = str(protocol.tuning["max_trials"])
    m["SecondsMax"] = str(int(protocol.tuning["max_seconds"]))
    budgets = {(r["trials"], r["seconds"]) for r in runs}
    m["BudgetUniform"] = "yes" if len(budgets) == 1 else "no"
    return m


def build_analysis_macros(m: dict[str, str]) -> None:
    """Autocorrelation and bootstrap-interval evidence, if committed."""
    path = REPO_ROOT / "artifacts" / "analysis" / "uncertainty_and_signal.json"
    if not path.exists():
        m["AnalysisPresent"] = "no"
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    m["AnalysisPresent"] = "yes"
    for asset in ("AAPL", "BTC"):
        info = data["return_autocorrelation"][asset]
        m[f"Auto{asset}"] = f"{info['lag1_autocorrelation']:+.3f}"
        m[f"AutoRsq{asset}"] = f"{info['r2_lag1']:.4f}"
    summary = data["summary"]
    m["NCiTotal"] = str(summary["runs"])
    m["NCiIncludeZero"] = str(summary["ci_includes_zero"])


def build_example_macro(m: dict[str, str]) -> None:
    """One real committed prediction, used as the recurring worked example."""
    candidates = sorted(ARTIFACTS.glob("*_aapl_svr_P2_*/predictions.csv"))
    if not candidates:
        return
    frame = pd.read_csv(candidates[-1])
    if "split" in frame:
        frame = frame[frame["split"] == "validation"]
    row = frame.iloc[7]
    c_t = float(row["y_naive"])
    predicted = float(row["y_pred"])
    actual = float(row["y_true"])
    m["ExDate"] = str(row["date"])
    m["ExCt"] = num(c_t)
    m["ExDelta"] = f"{predicted - c_t:+.2f}"
    m["ExPred"] = num(predicted)
    m["ExActual"] = num(actual)
    m["ExErr"] = num(abs(predicted - actual))


def build_invariance_macro(m: dict[str, str]) -> None:
    """Measure P0 vs P2 prediction differences for the tree ensembles.

    Claiming "trees are exactly invariant" requires comparing the committed
    predictions, not just the MAE.
    """
    worst = 0.0
    measured = False
    for asset in ("AAPL", "BTC"):
        for model in ("random_forest", "hist_gradient_boosting"):
            p0 = sorted(ARTIFACTS.glob(f"*_{asset.lower()}_{model}_P0_*/predictions.csv"))
            p2 = sorted(ARTIFACTS.glob(f"*_{asset.lower()}_{model}_P2_*/predictions.csv"))
            if not p0 or not p2:
                continue
            a = pd.read_csv(p0[-1])
            b = pd.read_csv(p2[-1])
            if len(a) != len(b):
                continue
            worst = max(worst, float((a["y_pred"] - b["y_pred"]).abs().max()))
            measured = True
    m["TreeMeasured"] = "yes" if measured else "no"
    m["TreeMaxDiff"] = "0" if worst == 0.0 else f"{worst:.1e}"
    m["TreeExact"] = "zero" if worst == 0.0 else f"{worst:.2e}"
    # Ready-made verdict so the slide cannot read "differ by zero (0)".
    m["TreeVerdict"] = "exactly zero" if worst == 0.0 else f"at most {worst:.1e}"


def write_backup_table(runs: list[dict]) -> None:
    """LaTeX table of every cell's skill, for the 'was P2 cherry-picked?' backup."""
    skill: dict[tuple[str, str, str], float] = {}
    for r in runs:
        if r["skill_mae"] is not None:
            skill[(r["asset"], r["model_id"], r["variant"])] = r["skill_mae"]

    order = ["linear_baseline", "ridge", "svr", "random_forest", "hist_gradient_boosting"]
    lines = [
        "% GENERATED by scripts/build_slide_assets.py -- do not edit by hand.",
        r"% Backup slide: skill (\%) for every model, asset and preprocessing variant.",
        r"\begin{tabular}{@{}lrrrr@{}}",
        r"\toprule",
        r" & \multicolumn{2}{c}{AAPL} & \multicolumn{2}{c}{BTC} \\",
        r"\cmidrule(lr){2-3}\cmidrule(l){4-5}",
        r"Model & P0 & P2 & P0 & P2 \\",
        r"\midrule",
    ]
    for model in order:
        cells = [LABELS.get(model, model)]
        for asset in ("AAPL", "BTC"):
            for variant in ("P0", "P2"):
                value = skill.get((asset, model, variant))
                cells.append("--" if value is None else pct(value))
        lines.append(" & ".join(cells) + r" \\")
    lines += [
        r"\midrule",
        r"Naive persistence & 0.00 & 0.00 & 0.00 & 0.00 \\",
        r"\bottomrule",
        r"\end{tabular}",
        "",
    ]
    (GENERATED / "backup_table.tex").write_text("\n".join(lines), encoding="utf-8")


def build_split_macros(m: dict[str, str], protocol) -> None:
    for asset in ("AAPL", "BTC"):
        prepared = prepare_dataset(asset, protocol)
        info = prepared["split"].describe(prepared["X"].index)
        m[f"Train{asset}"] = info["train_period"].replace("..", "--")
        m[f"Val{asset}"] = info["validation_period"].replace("..", "--")
        m[f"Test{asset}"] = info["test_period"].replace("..", "--")
        m[f"NBars{asset}"] = f"{len(prepared['frame']):,}".replace(",", "{,}")


def ensure_figures() -> int:
    """Regenerate any missing vector figures through the shared figure code."""
    report_figs = REPO_ROOT / "reports" / "latex" / "figures"
    if not (report_figs / "fig04_model_vs_naive.pdf").exists():
        figures.EXTRA_FORMATS = (".pdf",)
        protocol = load_protocol()
        frames, splits = {}, {}
        for asset in ("AAPL", "BTC"):
            prepared = prepare_dataset(asset, protocol)
            frames[asset] = prepared["frame"]
            splits[asset] = prepared["split"]
        figures.plot_coverage_and_splits(frames, splits, figure_root=report_figs)
        registry = figures.load_registry()
        figures.plot_model_vs_naive(registry, figure_root=report_figs)
        figures.plot_ablation_delta(registry, figure_root=report_figs)
        target = registry[
            (registry.status == "SUCCESS")
            & (registry.asset == "AAPL")
            & (registry.model_id == "ridge")
            & (registry.preprocess_variant == "P2")
        ]
        if not target.empty:
            figures.plot_observed_vs_predicted(target.iloc[0]["run_id"], figure_root=report_figs)

    copied = 0
    for stem in WANTED:
        source = report_figs / f"{stem}.pdf"
        if source.exists():
            shutil.copy2(source, FIGURES / source.name)
            copied += 1
        else:
            print(f"  missing figure: {stem}.pdf")
    return copied


def main() -> int:
    GENERATED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    protocol = load_protocol()
    runs = load_runs()
    if not runs:
        raise SystemExit("No runs found; run scripts/reproduce.sh first.")

    macros = build_macros(runs, protocol)
    build_analysis_macros(macros)
    build_example_macro(macros)
    build_invariance_macro(macros)
    build_split_macros(macros, protocol)
    write_backup_table(runs)

    lines = [
        "% GENERATED by scripts/build_slide_assets.py -- do not edit by hand.",
        "% Sources: artifacts/experiments/*/{manifest,metrics,config,predictions}",
        "%          artifacts/analysis/uncertainty_and_signal.json",
    ]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items()]
    (GENERATED / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    copied = ensure_figures()
    print(f"macros: {len(macros)} | figures: {copied}/{len(WANTED)} | runs: {len(runs)}")
    print(f"budget used: {macros['TrialsUsed']} trials / {macros['SecondsUsed']}s "
          f"(protocol max {macros['TrialsMax']}/{macros['SecondsMax']})")
    print(f"worst/best skill: {macros['SkillMin']}% .. {macros['SkillMax']}% "
          f"| below baseline: {macros['NBelowBaseline']} runs, "
          f"{macros['NPairsBelowBaseline']} pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
