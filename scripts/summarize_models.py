"""Write a README for each model folder under experiments/models/, and an index.

Each experiments/models/<model_id>/README.md lists the model's search grid, the
configuration the tuning chose in every run, the tuning score, every trial, and
the validation results. All values are read from the committed run files
(metrics.json, config.json); nothing is typed by hand.

Run: PYTHONPATH=src python scripts/summarize_models.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.paths import RUNS_ROOT  # noqa: E402

TITLES = {
    "linear_baseline": ("Linear baseline", "Ridge regression with a small L2 penalty: the simplest learned model."),
    "ridge": ("Ridge regression", "Linear model with an L2 penalty searched over a wide range."),
    "svr": ("Support vector regression (RBF kernel)", "Predicts from similarity to training examples; scale-sensitive."),
    "random_forest": ("Random forest", "Average of many independent trees; scale-invariant control."),
    "hist_gradient_boosting": ("Histogram gradient boosting", "Trees added one by one to fix the remaining error."),
}


def fmt(value) -> str:
    if value is None:
        return "None"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def params(d: dict) -> str:
    return ", ".join(f"{k}={fmt(v)}" for k, v in d.items()) or "—"


def model_readme(model_id: str, protocol) -> tuple[str, list[dict]]:
    title, blurb = TITLES.get(model_id, (model_id, ""))
    cfg = protocol.raw["models"][model_id]
    runs = []
    for run_dir in sorted(p for p in (RUNS_ROOT / model_id).iterdir() if p.is_dir()):
        metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
        budget = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
        runs.append({"dir": run_dir.name, "m": metrics, "budget": budget})

    out = [
        f"# {title} (`{model_id}`)",
        "",
        "**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.",
        "",
        blurb,
        "",
        f"Implementation: `{cfg['class']}` · family: {cfg['family']}",
        "",
        "## Search grid (frozen in the protocol before any result)",
        "",
        "| Hyperparameter | Values |",
        "|---|---|",
    ]
    for k, vals in (cfg.get("search_space") or {}).items():
        out.append(f"| `{k}` | {', '.join(fmt(v) for v in vals)} |")
    b = runs[0]["budget"] if runs else {}
    out += [
        "",
        f"Tuning: random search, {b.get('max_trials')} trials, at most {b.get('max_seconds')} s per run, "
        "seed 42, scored by mean MAE over 5 expanding-window folds inside the training block "
        "(see `data/splits/`). The validation block is never used for tuning.",
        "",
        "## Runs",
        "",
        "| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    rows = []
    for r in runs:
        m, s = r["m"]["metrics"], r["m"]["search"]
        out.append(
            f"| {r['m']['asset']} | {r['m']['preprocess_variant']} | {params(s['best_hyperparameters'])} "
            f"| {s['best_validation_mae']:.3f} | {m['validation_mae']:.3f} | {m['validation_rmse']:.3f} "
            f"| {m['validation_r2']:.4f} | {m['validation_skill_mae'] * 100:+.2f}% "
            f"| {m['validation_direction_accuracy'] * 100:.1f}% |"
        )
        rows.append({"model": model_id, "asset": r["m"]["asset"], "variant": r["m"]["preprocess_variant"],
                     "skill": m["validation_skill_mae"], "dir": r["dir"]})
    out += [
        "",
        "P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "
        "\"tomorrow equals today\". All results are on the validation block; the test block is sealed.",
        "",
        "## Every tuning trial",
        "",
    ]
    for r in runs:
        s = r["m"]["search"]
        out += [
            f"### {r['m']['asset']} {r['m']['preprocess_variant']} — `{r['dir']}`",
            "",
            f"{s['n_trials']} trials, {s['n_failed']} failed, stopped by `{s['stopped_reason']}`.",
            "",
            "| Trial | Configuration | Tuning MAE | Seconds | Status |",
            "|---:|---|---:|---:|---|",
        ]
        for t in s["trials"]:
            score = "—" if t["validation_mae"] is None else f"{t['validation_mae']:.3f}"
            out.append(f"| {t['trial']} | {params(t['hyperparameters'])} | {score} | {t['seconds']} | {t['status']} |")
        out.append("")
    out += [
        "## Files in each run folder",
        "",
        "`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · "
        "`metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · "
        "`environment.json` (package versions).",
        "",
    ]
    return "\n".join(out), rows


def supplementary_readme() -> None:
    """README for experiments/supplementary/direction_test/ from its newest COMPLETE run."""
    root = RUNS_ROOT.parent / "supplementary" / "direction_test"
    runs = [p for p in sorted(root.glob("*/results.json"), reverse=True)
            if json.loads(p.read_text(encoding="utf-8")).get("status") == "COMPLETE"]
    if not runs:
        return
    d = json.loads(runs[0].read_text(encoding="utf-8"))
    pct = lambda x: f"{x * 100:.1f}%"  # noqa: E731
    out = [
        "# Supplementary test: can neural networks call tomorrow's direction?",
        "",
        "**Generated** by `scripts/summarize_models.py` from the newest complete run "
        f"(`{runs[0].parent.name}/`). Experiment: `scripts/supplementary_direction_test.py`; decision D14.",
        "",
        d["question"],
        "",
        f"- Data: {d['data']}.",
        f"- Inputs: MLP = {d['inputs']['mlp']}; LSTM = {d['inputs']['lstm']}.",
        f"- Selection: {d['selection']}.",
        f"- Seeds {d['seeds']} (probabilities averaged); device `{d['device']}`, torch {d['torch']}.",
        f"- Uncertainty: {d['uncertainty']}.",
        "",
        "| Asset | Validation days | Majority rule | MLP | LSTM | Classical models |",
        "|---|---:|---|---|---|---|",
    ]
    for asset, r in d["results"].items():
        cells = []
        for k in ("mlp", "lstm"):
            x = r[k]
            lo, hi = x["diff_vs_majority_ci95"]
            cells.append(f"{pct(x['accuracy_ensemble'])} (seeds {pct(min(x['accuracy_by_seed']))}–"
                         f"{pct(max(x['accuracy_by_seed']))}); vs majority {x['diff_vs_majority'] * 100:+.1f} pp "
                         f"[{lo * 100:+.1f}, {hi * 100:+.1f}]")
        cl = r["classical_direction_accuracy"].values()
        out.append(f"| {asset} | {r['mlp']['n_validation']} | {r['mlp']['majority_rule']}: "
                   f"{pct(r['mlp']['majority_accuracy'])} | {cells[0]} | {cells[1]} | {pct(min(cl))}–{pct(max(cl))} |")
    zero = [r[k]["ci_includes_zero"] for r in d["results"].values() for k in ("mlp", "lstm")]
    verdict = ("Every interval includes zero: neither network calls the direction reliably better than "
               "the majority rule." if all(zero) else
               f"{len(zero) - sum(zero)} of {len(zero)} intervals exclude zero; read them with the "
               "dependence caveat above.")
    out += ["", verdict + " Direction accuracy ignores costs and risk; this is not a trading signal.", ""]
    (root / "README.md").write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    protocol = load_protocol()
    index_rows = []
    for model_id in TITLES:
        if not (RUNS_ROOT / model_id).is_dir():
            continue
        text, rows = model_readme(model_id, protocol)
        (RUNS_ROOT / model_id / "README.md").write_text(text, encoding="utf-8")
        index_rows += rows
    lines = [
        "# Model runs",
        "",
        "**Generated** by `scripts/summarize_models.py`. One folder per model; inside it, one folder per run "
        "(`<timestamp>_<asset>_<model>_<setting>_seed42`). `registry.jsonl` is the append-only list of every run.",
        "",
        "| Model | AAPL P0 | AAPL P2 | BTC P0 | BTC P2 |",
        "|---|---:|---:|---:|---:|",
    ]
    for model_id, (title, _) in TITLES.items():
        cells = []
        for asset in ("AAPL", "BTC"):
            for variant in ("P0", "P2"):
                hit = [r for r in index_rows if r["model"] == model_id and r["asset"] == asset and r["variant"] == variant]
                cells.append(f"{hit[0]['skill'] * 100:+.2f}%" if hit else "—")
        lines.append(f"| [{title}]({model_id}/README.md) | " + " | ".join(cells) + " |")
    lines += ["", "Validation skill versus \"tomorrow equals today\" (0 = no better). Naive persistence is "
              "computed inside every run, so it has no folder of its own.", ""]
    (RUNS_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    supplementary_readme()
    print(f"wrote {len(index_rows)} runs into {RUNS_ROOT.relative_to(REPO_ROOT)}/*/README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
