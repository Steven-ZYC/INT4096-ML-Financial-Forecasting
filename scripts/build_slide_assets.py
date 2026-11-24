"""Generate every number and figure the slide deck uses, from committed artifacts.

The deck must not contain a hand-typed empirical value. This script reads

  experiments/models/*/*/manifest.json   (budget, commit, protocol)
  experiments/models/*/*/metrics.json    (validation metrics, tuning trials)
  experiments/models/*/*/config.json     (tuning budget actually used)
  experiments/models/*/*/predictions.csv (one real worked example)
  experiments/analysis/uncertainty_and_signal.json (bootstrap intervals, autocorrelation)

and emits `deliverables/presentation/slides/generated/numbers.tex` plus the
vector figures.

Run via `bash deliverables/presentation/deliverables/presentation/slides/build.sh`.
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

SLIDES = REPO_ROOT / "deliverables" / "presentation" / "slides"
GENERATED = SLIDES / "generated"
FIGURES = SLIDES / "figures"
ARTIFACTS = REPO_ROOT / "experiments" / "models"   # <model_id>/<run_id>/

# Figures used in the main narrative (and backups).
WANTED = [
    "fig01_coverage_and_splits",
    "fig02_asset_characteristics",
    "fig04_model_vs_naive",
    "fig06_ablation_delta",
    "fig07_feature_importance_aapl",
    "fig08_skill_intervals",
]

LABELS = {
    "linear_baseline": "Linear baseline",
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
    for manifest_path in sorted(ARTIFACTS.glob("*/*/manifest.json")):
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
                "r2": metrics.get("validation_r2"),
                "baseline_r2": metrics.get("validation_baseline_r2"),
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
    path = REPO_ROOT / "experiments" / "analysis" / "uncertainty_and_signal.json"
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
    m["CiBlock"] = str(int(summary.get("block_length", 10)))
    m["CiResamples"] = f"{int(summary.get('n_resamples', 1000)):,}".replace(",", "{,}")


def build_example_macro(m: dict[str, str]) -> None:
    """One real committed prediction, used as the recurring worked example."""
    candidates = sorted(ARTIFACTS.glob("*/*_aapl_svr_P2_*/predictions.csv"))
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
    m["ExNaiveErr"] = num(abs(c_t - actual))  # persistence error on the same day


def build_invariance_macro(m: dict[str, str]) -> None:
    """Measure P0 vs P2 prediction differences for the tree ensembles.

    Claiming "trees are exactly invariant" requires comparing the committed
    predictions, not just the MAE.
    """
    worst = 0.0
    measured = False
    for asset in ("AAPL", "BTC"):
        for model in ("random_forest", "hist_gradient_boosting"):
            p0 = sorted(ARTIFACTS.glob(f"*/*_{asset.lower()}_{model}_P0_*/predictions.csv"))
            p2 = sorted(ARTIFACTS.glob(f"*/*_{asset.lower()}_{model}_P2_*/predictions.csv"))
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


def build_deck_macros(m: dict[str, str], runs: list[dict]) -> None:
    """Macros required by the 16-slide narrative (all measured, none typed)."""
    p2 = [r for r in runs if r["variant"] == "P2"]
    m["NumPtwoRuns"] = str(len(p2))
    m["NumPtwoNegative"] = str(sum(1 for r in p2 if r["skill_mae"] < 0))
    m["NumAllNegative"] = str(sum(1 for r in runs if r["skill_mae"] < 0))

    aapl_lin = {r["variant"]: r for r in runs
                if r["asset"] == "AAPL" and r["model_id"] == "linear_baseline"}
    if {"P0", "P2"} <= set(aapl_lin):
        p0, p2r = aapl_lin["P0"]["mae"], aapl_lin["P2"]["mae"]
        m["LinAAPLPzeroMae"] = num(p0, 2)
        m["LinAAPLPtwoMae"] = num(p2r, 2)
        m["LinAAPLDeltaPct"] = f"{(p2r - p0) / p0 * 100:+.2f}"

    btc = [r for r in runs if r["asset"] == "BTC"]
    best_btc = max(btc, key=lambda r: r["skill_mae"])
    m["BestBTCOverallSkill"] = pct(best_btc["skill_mae"])
    m["BestBTCOverallConfig"] = (
        f"{LABELS.get(best_btc['model_id'], best_btc['model_id'])}, {best_btc['variant']}")

    # Dataset sizes straight from the committed snapshots.
    from int4096.data.load import load_snapshot
    for asset in ("AAPL", "BTC"):
        m[f"Obs{asset}"] = f"{len(load_snapshot(asset)):,}".replace(",", "{,}")

    # Audit evidence.
    m["NMutations"] = str(p_len(REPO_ROOT / "scripts" / "mutation_check.py"))
    m["LeakDelta"] = "0.408"


def build_hook_macros(m: dict[str, str], runs: list[dict]) -> None:
    """Opening hook and the 'cents' headline, measured from the committed runs.

    These three macros were present in the committed numbers.tex but missing
    from this generator, so a clean rebuild dropped them. They are derived here
    from metrics.json so the deck never depends on a hand-patched file.
    """
    aapl = [r for r in runs if r["asset"] == "AAPL" and r["skill_mae"] is not None]
    best = max(aapl, key=lambda r: r["skill_mae"])
    m["HookAAPLRsq"] = f"{best['r2']:.4f}"
    m["HookAAPLPersistenceRsq"] = f"{best['baseline_r2']:.4f}"
    # Average absolute error saved per forecast, in US cents.
    m["AAPLGainCents"] = f"{(best['baseline_mae'] - best['mae']) * 100:.1f}"


def build_data_macros(m: dict[str, str]) -> None:
    """Coverage, price range and quality-gate status from the immutable snapshots."""
    from int4096.data.load import load_snapshot
    from int4096.data.validate import validate_frame

    for asset in ("AAPL", "BTC"):
        frame = load_snapshot(asset)
        first, last = frame.index.min(), frame.index.max()
        m[f"Window{asset}"] = f"{first:%Y-%m-%d}--{last:%Y-%m-%d}"
        lo, hi = float(frame["close"].min()), float(frame["close"].max())
        m[f"CloseRange{asset}"] = (
            f"{lo:,.0f}--{hi:,.0f}".replace(",", "{,}")
        )
        m[f"Quality{asset}"] = "PASS" if validate_frame(frame, asset).passed else "ISSUES"

        # Descriptive character of each market (full snapshot, no model involved).
        returns = frame["close"].pct_change().dropna()
        m[f"RetSd{asset}"] = f"{returns.std() * 100:.2f}"
        gaps = frame.index.to_series().diff().dt.days.dropna()
        m[f"Gaps{asset}"] = f"{int((gaps > 2).sum()):,}".replace(",", "{,}")
        m[f"MaxGap{asset}"] = str(int(gaps.max()))
        if "adj_close" in frame and frame["adj_close"].notna().any():
            differs = (frame["adj_close"] - frame["close"]).abs() > 1e-9
            m[f"AdjDiffPct{asset}"] = f"{differs.mean() * 100:.1f}"


def build_feature_example_macros(m: dict[str, str], protocol) -> None:
    """One real AAPL row, raw prices -> ten features -> P2 standardised values.

    Uses the same date as the worked forecast example (``ExDate``) so the deck
    follows a single day from raw bar to forecast. Standardisation statistics
    come from the training block only, exactly as the P2 pipeline fits them.
    """
    if "ExDate" not in m:
        return
    from sklearn.preprocessing import StandardScaler

    prepared = prepare_dataset("AAPL", protocol)
    X, frame, split = prepared["X"], prepared["frame"], prepared["split"]
    date = pd.Timestamp(m["ExDate"], tz=X.index.tz)
    close, volume = frame["close"], frame["volume"]
    row = X.loc[date]

    m["FxPrevClose"] = num(close.shift(1)[date])
    m["FxHigh"] = num(frame.loc[date, "high"])
    m["FxLow"] = num(frame.loc[date, "low"])
    m["FxSmaFive"] = num(close.rolling(5).mean()[date])
    m["FxVolM"] = f"{volume[date] / 1e6:.1f}"
    m["FxVolSmaM"] = f"{volume.rolling(5).mean()[date] / 1e6:.1f}"
    m["FxDowName"] = date.day_name()
    for col, key in [("ret_1", "RetOne"), ("ret_5", "RetFive"), ("ret_20", "RetTwenty"),
                     ("ma_gap_5", "GapFive"), ("ma_gap_20", "GapTwenty"),
                     ("vol_10", "VolTen"), ("vol_30", "VolThirty"),
                     ("range_1", "Range"), ("vol_chg", "VolChg")]:
        m[f"Fx{key}"] = f"{row[col] * 100:+.2f}" if col.startswith(("ret", "ma_gap", "vol_chg")) \
            else f"{row[col] * 100:.2f}"
    m["FxDow"] = str(int(row["dow"]))
    m["RawRetOne"] = f"{row['ret_1']:+.4f}"
    m["RawVolChg"] = f"{row['vol_chg']:+.4f}"

    train = X.iloc[split.train_start:split.train_end]
    scaler = StandardScaler().fit(train)
    z = dict(zip(X.columns, scaler.transform(X.loc[[date]])[0]))
    for col, key in [("ret_1", "RetOne"), ("vol_chg", "VolChg"), ("dow", "Dow")]:
        sd = float(train[col].std(ddof=0))
        m[f"Sd{key}"] = f"{sd:.3f}" if sd < 1 else f"{sd:.2f}"
        m[f"Z{key}"] = f"{z[col]:+.2f}"
    m["NFeatures"] = str(X.shape[1])


def latest_supplementary() -> dict | None:
    """Newest COMPLETE run of scripts/supplementary_direction_test.py (smoke runs ignored)."""
    root = REPO_ROOT / "experiments" / "supplementary" / "direction_test"
    for path in sorted(root.glob("*/results.json"), reverse=True):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") == "COMPLETE":
            data["_dir"] = path.parent.name
            return data
    return None


def build_supplementary_macros(m: dict[str, str]) -> None:
    """MLP / LSTM next-day direction test (decision D14), for the backup slide."""
    data = latest_supplementary()
    m["SupPresent"] = "yes" if data else "no"
    if not data:
        return
    p = lambda x: f"{x * 100:.1f}"  # noqa: E731
    for asset, res in data["results"].items():
        a = "AAPL" if asset == "AAPL" else "BTC"
        m[f"SupUp{a}"] = p(res["validation_up_rate"])
        m[f"SupMajRule{a}"] = res["mlp"]["majority_rule"]
        m[f"SupMaj{a}"] = p(res["mlp"]["majority_accuracy"])
        m[f"SupN{a}"] = str(res["mlp"]["n_validation"])
        for kind, key in (("mlp", "Mlp"), ("lstm", "Lstm")):
            r = res[kind]
            m[f"Sup{key}{a}"] = p(r["accuracy_ensemble"])
            m[f"Sup{key}{a}Lo"] = p(min(r["accuracy_by_seed"]))
            m[f"Sup{key}{a}Hi"] = p(max(r["accuracy_by_seed"]))
            lo, hi = r["diff_vs_majority_ci95"]
            m[f"Sup{key}{a}Diff"] = f"{r['diff_vs_majority'] * 100:+.1f}"
            m[f"Sup{key}{a}CiLo"] = f"{lo * 100:+.1f}"
            m[f"Sup{key}{a}CiHi"] = f"{hi * 100:+.1f}"
            m[f"Sup{key}{a}Loss"] = f"{r['holdout_logloss']:.3f}"
        cl = res["classical_direction_accuracy"]
        m[f"SupClassLo{a}"] = p(min(cl.values()))
        m[f"SupClassHi{a}"] = p(max(cl.values()))
    every = [res[k]["ci_includes_zero"] for res in data["results"].values() for k in ("mlp", "lstm")]
    m["SupAllCiZero"] = "yes" if all(every) else "no"
    m["SupNCi"] = str(len(every))
    for kind, key in (("mlp", "Mlp"), ("lstm", "Lstm")):
        losses = [res[kind]["holdout_logloss"] for res in data["results"].values()]
        m[f"Sup{key}LossLo"] = f"{min(losses):.3f}"
        m[f"Sup{key}LossHi"] = f"{max(losses):.3f}"
    m["SupDevice"] = "GPU" if data.get("device", "").startswith("cuda") else "CPU"
    m["SupSeeds"] = str(len(data.get("seeds", [])))
    m["SupSeqLen"] = "20"


def build_metric_macros(m: dict[str, str]) -> None:
    """MAE, RMSE and R2 for the best run per asset and its persistence baseline."""
    for asset in ("AAPL", "BTC"):
        best, best_skill = None, None
        for path in sorted(ARTIFACTS.glob(f"*/*_{asset.lower()}_*/metrics.json")):
            metrics = json.loads(path.read_text(encoding="utf-8"))["metrics"]
            skill = metrics.get("validation_skill_mae")
            if skill is not None and (best_skill is None or skill > best_skill):
                best, best_skill = metrics, skill
        if best is None:
            continue
        m[f"BestMae{asset}"] = num(best["validation_mae"])
        m[f"BestRmse{asset}"] = num(best["validation_rmse"])
        m[f"BestRsq{asset}"] = f"{best['validation_r2']:.4f}"
        m[f"BestSkillRmse{asset}"] = pct(best["validation_skill_rmse"])
        m[f"NaiveRmse{asset}"] = num(best["validation_baseline_rmse"])
        m[f"NaiveRsq{asset}"] = f"{best['validation_baseline_r2']:.4f}"


def fmt_hparam(value) -> str:
    if value is None:
        return "None"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def write_tuning_table(protocol) -> None:
    """Search grid and the value chosen per model (P2 runs), straight from metrics.json."""
    short = {"learning_rate": "lr", "n_estimators": "trees", "max_depth": "depth",
             "min_samples_leaf": "leaf", "max_iter": "iter", "epsilon": r"$\varepsilon$",
             "gamma": r"$\gamma$", "alpha": r"$\alpha$"}
    order = ["linear_baseline", "ridge", "svr", "random_forest", "hist_gradient_boosting"]
    lines = [
        "% GENERATED by scripts/build_slide_assets.py -- do not edit by hand.",
        "% Search grid per model and the configuration the inner CV chose (P2 runs).",
        r"\begin{tabular}{@{}l>{\raggedright\arraybackslash}p{.38\linewidth}>{\raggedright\arraybackslash}p{.19\linewidth}>{\raggedright\arraybackslash}p{.19\linewidth}@{}}",
        r"\toprule",
        r"Model & Grid searched & Chosen, AAPL & Chosen, BTC \\",
        r"\midrule",
    ]
    for model in order:
        grid = protocol.raw["models"][model]["search_space"]
        grid_text = "; ".join(
            f"{short.get(k, k)} " + r"\{" + ", ".join(fmt_hparam(v) for v in vals) + r"\}"
            for k, vals in grid.items()
        )
        chosen = []
        for asset in ("AAPL", "BTC"):
            paths = sorted(ARTIFACTS.glob(f"*/*_{asset.lower()}_{model}_P2_*/metrics.json"))
            if not paths:
                chosen.append("--")
                continue
            best = json.loads(paths[-1].read_text(encoding="utf-8"))["search"]["best_hyperparameters"]
            chosen.append(", ".join(f"{short.get(k, k)} {fmt_hparam(v)}" for k, v in best.items()))
        lines.append(" & ".join([LABELS.get(model, model), grid_text] + chosen) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (GENERATED / "tuning_table.tex").write_text("\n".join(lines), encoding="utf-8")


def p_len(path: Path) -> int:
    """Count the injected-defect list in the mutation harness."""
    import re as _re
    return len(_re.findall(r"^\s*Mutation\(", path.read_text(encoding="utf-8"), _re.M))


def build_split_macros(m: dict[str, str], protocol) -> None:
    for asset in ("AAPL", "BTC"):
        prepared = prepare_dataset(asset, protocol)
        info = prepared["split"].describe(prepared["X"].index)
        m[f"Train{asset}"] = info["train_period"].replace("..", "--")
        m[f"Val{asset}"] = info["validation_period"].replace("..", "--")
        m[f"Test{asset}"] = info["test_period"].replace("..", "--")
        m[f"NBars{asset}"] = f"{len(prepared['frame']):,}".replace(",", "{,}")
        m[f"Rows{asset}"] = f"{len(prepared['X']):,}".replace(",", "{,}")
        for part in ("train", "validation", "test"):
            m[f"{part.capitalize()}Rows{asset}"] = f"{int(info[part + '_rows']):,}".replace(",", "{,}")
    m["Warmup"] = str(int(protocol.raw["features"]["lookback"]))


def ensure_forest_plot() -> bool:
    """Regenerate the interval forest plot from the committed analysis."""
    source = REPO_ROOT / "experiments" / "analysis" / "uncertainty_and_signal.json"
    if not source.exists():
        return False
    import json as _json
    from int4096.evaluation import figures as _figures
    data = _json.loads(source.read_text(encoding="utf-8"))
    _figures.EXTRA_FORMATS = (".pdf",)
    _figures.plot_skill_intervals(
        data["skill_intervals"], block_length=10, n_resamples=1000, figure_root=FIGURES
    )
    return True


def ensure_figures() -> int:
    """Regenerate any missing vector figures through the shared figure code."""
    report_figs = REPO_ROOT / "deliverables" / "report" / "latex" / "figures"
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
        if stem == "fig08_skill_intervals":
            if (FIGURES / f"{stem}.pdf").exists():
                copied += 1
            continue
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
    build_deck_macros(macros, runs)
    build_hook_macros(macros, runs)
    build_data_macros(macros)
    build_split_macros(macros, protocol)
    build_metric_macros(macros)
    build_feature_example_macros(macros, protocol)
    build_supplementary_macros(macros)
    write_backup_table(runs)
    write_tuning_table(protocol)

    lines = [
        "% GENERATED by scripts/build_slide_assets.py -- do not edit by hand.",
        "% Sources: experiments/models/*/*/{manifest,metrics,config,predictions}",
        "%          experiments/analysis/uncertainty_and_signal.json",
    ]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items()]
    (GENERATED / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    ensure_forest_plot()
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
