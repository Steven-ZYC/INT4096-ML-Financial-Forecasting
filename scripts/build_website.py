"""Build the interactive explainer site from the repository's real files.

    deliverables/website/template.html   hand-written page (layout, charts, copy)
    deliverables/website/index.html      GENERATED: template + the data below, inlined

Everything the page shows is read here from data/ and experiments/; nothing is typed
by hand into the page. Inlining keeps index.html a single file that opens straight
from disk (no server needed) and publishes as one artifact.

Run: PYTHONPATH=src python scripts/build_website.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.data.load import load_snapshot  # noqa: E402
from int4096.experiments.run import prepare_dataset  # noqa: E402

SITE = REPO_ROOT / "deliverables" / "website"
RUNS = REPO_ROOT / "experiments" / "models"
ASSETS = ("AAPL", "BTC")
MODELS = ["linear_baseline", "ridge", "svr", "random_forest", "hist_gradient_boosting"]
EXAMPLE_DATE = "2024-11-21"

# Document shell for the standalone page. The template is written as a page body
# (title, styles, markup, scripts); this adds the doctype, charset, viewport and the
# small reset the artifact viewer would otherwise provide.
STANDALONE_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
"""


def sig(x: float, digits: int = 6) -> float:
    return float(f"{x:.{digits}g}") if np.isfinite(x) else None


def asset_block(asset: str, protocol) -> dict:
    frame = load_snapshot(asset)
    prepared = prepare_dataset(asset, protocol)
    X, split = prepared["X"], prepared["split"]
    dates = [f"{d:%Y-%m-%d}" for d in frame.index]
    xdates = [f"{d:%Y-%m-%d}" for d in X.index]

    returns = frame["close"].pct_change(fill_method=None).dropna()
    gaps = frame.index.to_series().diff().dt.days.dropna()
    train = X.iloc[split.train_start:split.train_end]
    block = {
        "source": protocol.assets[asset]["provider"],
        "link": (
            "https://stockanalysis.com/api/symbol/s/aapl/history?range=10Y&period=Daily"
            if asset == "AAPL" else
            "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d"
        ),
        "currency": protocol.assets[asset]["quote_currency"],
        "calendar": protocol.assets[asset]["calendar"],
        "bars": {
            "date": dates,
            "close": [round(float(v), 2) for v in frame["close"]],
            "high": [round(float(v), 2) for v in frame["high"]],
            "low": [round(float(v), 2) for v in frame["low"]],
            "volume": [int(v) for v in frame["volume"]],
        },
        "stats": {
            "bars": len(frame),
            "first": dates[0], "last": dates[-1],
            "ret_sd_pct": round(float(returns.std() * 100), 2),
            "gaps_over_2d": int((gaps > 2).sum()),
            "close_min": round(float(frame["close"].min()), 2),
            "close_max": round(float(frame["close"].max()), 2),
            "adj_differs_pct": (
                round(float(((frame["adj_close"] - frame["close"]).abs() > 1e-9).mean() * 100), 1)
                if "adj_close" in frame and frame["adj_close"].notna().any() else None
            ),
        },
        "features": {
            "columns": list(X.columns),
            "date": xdates,
            "values": [[sig(float(v), 5) for v in row] for row in X.to_numpy()],
            "train_mean": [sig(float(v)) for v in train.mean().to_numpy()],
            "train_sd": [sig(float(v)) for v in train.std(ddof=0).to_numpy()],
        },
        "split": json.loads((REPO_ROOT / "data" / "splits" / f"{asset.lower()}.json").read_text()),
        "warmup": int(protocol.raw["features"]["lookback"]),
    }
    return block


def runs_block(protocol) -> dict:
    runs, truth = [], {}
    for model in MODELS:
        for run_dir in sorted((RUNS / model).iterdir()):
            if not run_dir.is_dir():
                continue
            m = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
            met, search = m["metrics"], m["search"]
            with open(run_dir / "predictions.csv", encoding="utf-8") as fh:
                rows = [r for r in csv.DictReader(fh) if r.get("split", "validation") == "validation"]
            asset = m["asset"]
            if asset not in truth:
                truth[asset] = {
                    "date": [r["date"] for r in rows],
                    "actual": [round(float(r["y_true"]), 2) for r in rows],
                    "naive": [round(float(r["y_naive"]), 2) for r in rows],
                }
            runs.append({
                "id": m["run_id"], "asset": asset, "model": model, "variant": m["preprocess_variant"],
                "pred": [round(float(r["y_pred"]), 3) for r in rows],
                "mae": met["validation_mae"], "rmse": met["validation_rmse"], "r2": met["validation_r2"],
                "skill": met["validation_skill_mae"], "dir_acc": met["validation_direction_accuracy"],
                "best": search["best_hyperparameters"], "cv_mae": search["best_validation_mae"],
                "trials": [{"params": t["hyperparameters"], "cv_mae": t["validation_mae"],
                            "seconds": t["seconds"]} for t in search["trials"]],
            })
    grids = {k: protocol.raw["models"][k]["search_space"] for k in MODELS}
    budget = json.loads(next(RUNS.glob("*/*/config.json")).read_text(encoding="utf-8"))
    analysis = json.loads((REPO_ROOT / "experiments" / "analysis" / "uncertainty_and_signal.json").read_text())
    intervals = {i["run_id"]: [i["ci_low"], i["ci_high"]] for i in analysis["skill_intervals"]}
    for r in runs:
        r["ci"] = intervals.get(r["id"])
    return {
        "runs": runs, "truth": truth, "grids": grids,
        "budget": {"trials": budget.get("max_trials"), "seconds": budget.get("max_seconds"),
                   "cap_trials": protocol.tuning["max_trials"], "cap_seconds": protocol.tuning["max_seconds"]},
        "autocorr": {a: analysis["return_autocorrelation"][a]["lag1_autocorrelation"] for a in ASSETS},
        "bootstrap": {"block": analysis["summary"].get("block_length", 10),
                      "resamples": analysis["summary"].get("n_resamples", 1000)},
    }


def dl_block() -> dict | None:
    root = REPO_ROOT / "experiments" / "supplementary" / "direction_test"
    for path in sorted(root.glob("*/results.json"), reverse=True):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") != "COMPLETE":
            continue
        probs: dict = {}
        with open(path.parent / "predictions.csv", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                probs.setdefault(r["asset"], {}).setdefault(r["model"], []).append(
                    [round(float(r["prob_up"]), 4), int(r["actual_up"])])
        return {"run": path.parent.name, "device": data["device"], "seeds": data["seeds"],
                "inputs": data["inputs"], "results": data["results"], "probs": probs}
    return None


def main() -> int:
    protocol = load_protocol()
    data = {
        "assets": {a: asset_block(a, protocol) for a in ASSETS},
        **runs_block(protocol),
        "dl": dl_block(),
        "example_date": EXAMPLE_DATE,
        "protocol_version": protocol.version,
    }
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    template = (SITE / "template.html").read_text(encoding="utf-8")
    if "__SITE_DATA__" not in template:
        raise SystemExit("template.html has no __SITE_DATA__ placeholder")
    body = template.replace("__SITE_DATA__", blob)

    # 1) Full HTML document: GitHub Pages and opening the file straight from disk.
    out = SITE / "index.html"
    cut = body.index("</style>") + len("</style>")   # title, meta, fonts, styles -> <head>
    out.write_text(STANDALONE_HEAD + body[:cut] + "\n</head>\n<body>" + body[cut:] + "\n</body>\n</html>\n",
                   encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)} ({out.stat().st_size / 1024:.0f} KB, data {len(blob) / 1024:.0f} KB)")

    # 2) Fragment for the claude.ai artifact, which supplies its own document shell.
    frag = REPO_ROOT / "build" / "website" / "artifact.html"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text(body, encoding="utf-8")
    print(f"wrote {frag.relative_to(REPO_ROOT)} (artifact fragment, not tracked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
