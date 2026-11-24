"""Generate `deliverables/notebook/INT4096_Final_Colab.ipynb`.

The notebook is produced from source here so that its content is reviewable in
version control as plain Python, and so it cannot silently drift from the
library code. Cells are written to be run top-to-bottom in a fresh Colab kernel:
no hidden state, no manual edits, no cached outputs.

Usage:
    python scripts/build_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path

import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "deliverables" / "notebook" / "INT4096_Final_Colab.ipynb"


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(text: str):
    return nbf.v4.new_code_cell(text.strip("\n"))


CELLS = [
    md(
        """
# Learning Machine Learning Through Financial Time-Series Forecasting

**INT4096 — Artificial Intelligence and Machine Learning in Education**
Education University of Hong Kong · Semester 1, 2026–27 · Group project

A reproducible comparison of model families and preprocessing strategies for
next-session close prediction on **AAPL** and **BTC**.

---

### What this notebook does

1. Loads an **immutable** snapshot of each asset and verifies its SHA-256.
2. Builds strictly **causal** features (only bars up to and including `t`).
3. Splits chronologically — 60% train, 20% validation, 20% **sealed** test.
4. Runs a naive persistence baseline and four model families.
5. Reports MAE / RMSE / R² **and** skill relative to persistence.
6. Shows one preprocessing ablation: does scaling help, and for which models?

### What this notebook deliberately does **not** do

- It does not unblind the test block. The final 20% is sealed (decision D7).
- It does not claim the models are profitable. **This is not investment advice.**
- It does not claim that students learned anything: no learner study was run.

### How to run

`Runtime → Run all`. The first cell installs dependencies (~30 s).
Everything after that is deterministic given the committed data snapshot.
"""
    ),
    md("## 0. Setup\n\nColab already provides most of the scientific stack; we only install what is missing."),
    code(
        """
import importlib
import os
import subprocess
import sys

REQUIRED = ["numpy", "pandas", "scipy", "sklearn", "matplotlib", "yaml"]
missing = [name for name in REQUIRED if importlib.util.find_spec(name) is None]

if missing and os.environ.get("INT4096_SKIP_INSTALL") == "1":
    raise RuntimeError(f"Missing packages {missing} and INT4096_SKIP_INSTALL=1 is set.")
if missing:
    print("Installing:", missing)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)
else:
    print("All required packages are already available.")

import numpy as np, pandas as pd, sklearn, matplotlib
print("python  ", sys.version.split()[0])
print("numpy   ", np.__version__)
print("pandas  ", pd.__version__)
print("sklearn ", sklearn.__version__)
print("matplotlib", matplotlib.__version__)
"""
    ),
    md(
        """
## 1. Get the project code and data

This notebook is designed to run from the repository root. If you opened it
directly in Colab, clone the project first (replace the URL with your own
repository), or upload the `data/raw/` folder alongside the notebook.

The **check** below is what matters: the notebook refuses to proceed unless it
can see the snapshot files and their SHA-256 manifests.
"""
    ),
    code(
        """
import os
import subprocess
import sys
from pathlib import Path

REPO_URL = os.environ.get("INT4096_REPO", "")  # optional: set to clone automatically

if not Path("data/raw/aapl_daily.json").exists() and REPO_URL:
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, "int4096"], check=True)
    os.chdir("int4096")

root = Path.cwd()
if not (root / "src" / "int4096").exists():
    # Walk up to the repository root, which is the case when the notebook is
    # opened from deliverables/notebook/ inside the repository.
    for parent in root.parents:
        if (parent / "src" / "int4096").exists():
            os.chdir(parent)
            root = Path.cwd()
            break

print("working directory:", root)
print("package present  :", (root / "src" / "int4096").exists())
print("snapshot present :", (root / "data" / "raw" / "aapl_daily.json").exists())
print("manifest present :", (root / "data" / "raw" / "aapl_daily.manifest.json").exists())

sys.path.insert(0, str(root / "src"))
import int4096
print("int4096 version  :", int4096.__version__)
"""
    ),
    md(
        """
## 2. Load the immutable snapshots and verify integrity

A dataset that cannot be identified by hash is not reproducible. `run_cell`
enforces this; the check is repeated here so a reader sees it happen.

Both assets are daily bars, but they are **different datasets**: AAPL follows
exchange sessions (weekends and holidays are gaps), BTC trades every UTC day.
We never align them by row number.
"""
    ),
    code(
        """
from int4096.config import load_protocol
from int4096.data.load import load_snapshot, read_manifest, resolve_snapshot_path
from int4096.data.snapshot import sha256_file
from int4096.data.validate import validate_frame

protocol = load_protocol()
print("protocol version:", protocol.version)
print("label mode      :", protocol.label_mode, "(models fit the price CHANGE; error is reported on the price)")
print()

frames = {}
for asset in ("AAPL", "BTC"):
    frame = load_snapshot(asset)
    manifest = read_manifest(asset)
    actual = sha256_file(resolve_snapshot_path(asset))
    assert actual == manifest["sha256"], f"{asset}: snapshot hash mismatch"

    report = validate_frame(frame, asset=asset)
    frames[asset] = frame
    print(f"{asset}: {len(frame):,} bars  {frame.index[0].date()} .. {frame.index[-1].date()}  "
          f"quality={'PASS' if report.passed else 'ISSUES'}")
    print(f"       sha256 {actual[:16]}...  source={manifest['source']['provider']}")

pd.concat({k: v.tail(3)[["close", "volume"]] for k, v in frames.items()}, axis=1)
"""
    ),
    md(
        """
## 3. Causal features

Every feature is a trailing ratio: a return, a gap to a moving average, a
trailing volatility, an intra-bar range, or a volume anomaly.

**Why ratios and not prices?** Price levels are non-stationary and would let a
model look accurate simply by copying today's price. Ratios are scale-free,
which is also what makes a comparison between a $200 stock and an $80,000 coin
meaningful at all.

Two demonstration cells follow. The first shows that appending extreme *future*
data leaves earlier features untouched. If it changed them, the pipeline would be
peeking into the future.
"""
    ),
    code(
        """
from int4096.features.build import build_features, feature_dictionary

frame = frames["AAPL"]
X, y = build_features(frame, lookback=protocol.lookback, min_periods=protocol.min_periods,
                      mode=protocol.label_mode)
print(f"design matrix: {X.shape[0]} rows x {X.shape[1]} features")
print("features:", list(X.columns))
print()
display(pd.DataFrame(feature_dictionary()))
"""
    ),
    code(
        """
# --- the look-ahead demonstration -------------------------------------------
future = frame.iloc[[-1]].copy()
future.index = pd.DatetimeIndex([frame.index[-1] + pd.Timedelta(days=1)], name=frame.index.name)
for column in ("open", "high", "low", "close", "volume", "adj_close"):
    future[column] = future[column].to_numpy() * 50.0   # absurd future values

extended = pd.concat([frame, future])
X_ext, _ = build_features(extended, lookback=protocol.lookback,
                          min_periods=protocol.min_periods, mode=protocol.label_mode)

shared = X.index
difference = (X.loc[shared] - X_ext.loc[shared]).abs().max().max()
print(f"largest change in any historical feature after appending extreme future data: {difference:.3e}")
assert difference < 1e-12, "features depend on future data — this is a leak"
print("PASS: features are causal (they cannot see the future).")
"""
    ),
    md(
        """
## 4. Chronological split, with a purge at each boundary

Random shuffling of time-ordered rows would let the model train on the future.
We split by time instead, and we **purge one row at each boundary**:

with `y_t = Close_{t+1}`, the last training label is a validation-block price and
the last validation label would be a *sealed test* price. Dropping one row at
each boundary removes both channels. (This was found by an independent audit —
see `docs/quality/leakage_audit.md`, finding LEAK-001.)
"""
    ),
    code(
        """
from int4096.data.split import chronological_split
from int4096.experiments.run import prepare_dataset

splits = {}
for asset in ("AAPL", "BTC"):
    prepared = prepare_dataset(asset, protocol)
    splits[asset] = prepared["split"]
    info = prepared["split"].describe(prepared["X"].index)
    print(asset)
    for key in ("train_period", "validation_period", "test_period", "train_rows",
                "validation_rows", "test_rows"):
        print(f"   {key:18s} {info[key]}")
    print()
"""
    ),
    code(
        """
import matplotlib.pyplot as plt

fig, axes = plt.subplots(len(frames), 1, figsize=(11, 3.4 * len(frames)), squeeze=False)
for ax, (asset, frame) in zip(axes[:, 0], frames.items()):
    split = splits[asset]
    ax.plot(frame.index, frame["close"], color="black", lw=0.8, label="Close (raw)")
    ax.axvspan(frame.index[0], frame.index[split.train_end], alpha=0.10, color="tab:blue")
    ax.axvspan(frame.index[split.validation_start], frame.index[split.validation_end],
               alpha=0.10, color="tab:green")
    ax.axvspan(frame.index[split.test_start], frame.index[-1], alpha=0.14, color="tab:red")
    ax.set_title(f"{asset}: train (blue) / validation (green) / sealed test (red)")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left", fontsize=8)
fig.tight_layout()
plt.show()
print("The red block is sealed: no cell in this notebook fits or scores on it.")
"""
    ),
    md(
        """
## 5. The baseline everything must beat: naive persistence

"Tomorrow's close will be today's close" is a genuinely strong forecaster for
near-random-walk prices. If a fancy model cannot beat it, that is the finding,
not a failure of the analysis.
"""
    ),
    code(
        """
from int4096.evaluation.baselines import naive_persistence
from int4096.evaluation.metrics import evaluate_predictions, mae

asset = "AAPL"
prepared = prepare_dataset(asset, protocol)
X, y, split, frame = prepared["X"], prepared["y"], prepared["split"], prepared["frame"]

val_index = X.index[split.validation_start:split.validation_end]
reference = frame.loc[val_index, protocol.label_field].to_numpy()
truth = reference + y.loc[val_index].to_numpy()      # delta mode -> price level
naive = naive_persistence(reference)

baseline_metrics = evaluate_predictions(truth, naive, naive, reference=reference)
print(f"Naive persistence on {asset} validation ({len(truth)} sessions)")
print(f"  MAE  = {baseline_metrics['mae']:.3f}")
print(f"  RMSE = {baseline_metrics['rmse']:.3f}")
print(f"  R2   = {baseline_metrics['r2']:.4f}   <- high because price levels trend; not evidence of skill")
print(f"  direction accuracy = {baseline_metrics['direction_accuracy']} "
      f"(ties: {baseline_metrics['direction_tie_rate']:.0%}) -> makes no directional call, so n/a")
"""
    ),
    md(
        """
## 6. Model comparison under identical conditions

Four model families get the **same** features, split, evaluation dates and tuning
budget. Each builds a scikit-learn pipeline in which any scaler is fitted on the
training rows only, inside the pipeline, so it is refitted per fold.

- `linear_baseline` — near-unregularized linear model (the "learned floor")
- `ridge` — regularized linear reference
- `svr` — kernel method, strongly scale-sensitive
- `random_forest` — bagged trees, scale-invariant, weak extrapolation
- `hist_gradient_boosting` — boosted trees, sequential residual fitting
"""
    ),
    code(
        """
from int4096.experiments.tuning import select_hyperparameters
from int4096.data.split import expanding_window_folds
from int4096.models.base import build_estimator
from int4096.features.pipeline import select_feature_columns

MODELS = ["linear_baseline", "ridge", "svr", "random_forest", "hist_gradient_boosting"]
VARIANT = protocol.variant("P2")
variant_name = "P2"

results = []
for asset in ("AAPL", "BTC"):
    prepared = prepare_dataset(asset, protocol)
    X, y, split, frame = prepared["X"], prepared["y"], prepared["split"], prepared["frame"]
    columns = select_feature_columns(VARIANT, list(X.columns))

    train = np.arange(split.train_start, split.train_end)
    val = np.arange(split.validation_start, split.validation_end)
    X_train, y_train = X.iloc[train], y.iloc[train]
    X_val = X.iloc[val]
    reference = frame.loc[X_val.index, protocol.label_field].to_numpy()
    truth = reference + y.iloc[val].to_numpy()

    folds = expanding_window_folds(len(X_train), n_splits=protocol.cv["n_splits"],
                                   gap=protocol.cv["gap"],
                                   min_train_fraction=protocol.cv["min_train_cv_fraction"]
                                   if "min_train_cv_fraction" in protocol.cv
                                   else protocol.cv["min_train_fraction"])

    for model_id in MODELS:
        space = dict(protocol.model(model_id).get("search_space") or {})

        def score(config, model_id=model_id):
            scores = []
            for fold_train, fold_val in folds:
                estimator = build_estimator(model_id, config, 42, VARIANT, feature_columns=None)
                estimator.fit(X_train.iloc[fold_train], y_train.iloc[fold_train])
                predictions = estimator.predict(X_train.iloc[fold_val])
                scores.append(float(np.mean(np.abs(y_train.iloc[fold_val].to_numpy() - predictions))))
            return float(np.mean(scores))

        search = select_hyperparameters(score, space, max_trials=6, max_seconds=60, seed=42)
        final = build_estimator(model_id, search.best_hyperparameters, 42, VARIANT)
        final.fit(X_train, y_train)

        predicted_delta = final.predict(X_val)
        predicted_price = reference + predicted_delta
        bundle = evaluate_predictions(truth, predicted_price, naive_persistence(reference),
                                      reference=reference)
        results.append({
            "asset": asset, "model": model_id,
            "mae": bundle["mae"], "rmse": bundle["rmse"], "r2": bundle["r2"],
            "skill_mae": bundle["skill_mae"],
            "direction_accuracy": bundle["direction_accuracy"],
        })

results_df = pd.DataFrame(results)
results_df
"""
    ),
    md(
        """
### Reading this table

`skill_mae = 1 - MAE_model / MAE_naive`. Zero means "no better than copying
today's price". **Negative means worse.**

Dollar errors (MAE/RMSE) are **not** comparable between AAPL and BTC — the quote
scales differ by orders of magnitude. Only `skill_mae` can be compared across the
two assets.
"""
    ),
    code(
        """
pivot = results_df.pivot(index="model", columns="asset", values="skill_mae").round(4)
print("skill_MAE by model and asset (0 = no better than persistence)")
display(pivot)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharex=True)
bound = max(0.01, float(results_df["skill_mae"].abs().max()) * 1.3)
for ax, asset in zip(axes, ("AAPL", "BTC")):
    subset = results_df[results_df["asset"] == asset].sort_values("skill_mae")
    colours = ["tab:green" if v > 0 else "tab:red" for v in subset["skill_mae"]]
    ax.barh(subset["model"], subset["skill_mae"], color=colours)
    ax.axvline(0, color="black", lw=1)
    ax.set_xlim(-bound, bound)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v*100:+.1f}%")
    ax.set_title(asset)
    ax.set_xlabel("skill vs naive persistence (shared axis)")
fig.suptitle("Trained models are within a fraction of a percent of persistence")
fig.tight_layout()
plt.show()
"""
    ),
    md(
        """
## 7. Deep dive: does preprocessing matter?

Scaling changes the **geometry** of the feature space. A kernel method measures
distances there, so scaling should matter for SVR. A tree only compares
thresholds within one feature, so scaling should be irrelevant to a forest.

That second claim is a **negative control**: if scaling changes the forest's
predictions, something is wrong with the pipeline, not with the world.
"""
    ),
    code(
        """
ablation = []
for asset in ("AAPL", "BTC"):
    prepared = prepare_dataset(asset, protocol)
    X, y, split, frame = prepared["X"], prepared["y"], prepared["split"], prepared["frame"]
    train = np.arange(split.train_start, split.train_end)
    val = np.arange(split.validation_start, split.validation_end)
    X_train, y_train, X_val = X.iloc[train], y.iloc[train], X.iloc[val]
    reference = frame.loc[X_val.index, protocol.label_field].to_numpy()
    truth = reference + y.iloc[val].to_numpy()

    for model_id in ("ridge", "svr", "random_forest", "hist_gradient_boosting"):
        for variant_name in ("P0", "P2"):
            variant = protocol.variant(variant_name)
            estimator = build_estimator(model_id, {}, 42, variant)
            estimator.fit(X_train, y_train)
            predicted = reference + estimator.predict(X_val)
            ablation.append({
                "asset": asset, "model": model_id, "variant": variant_name,
                "mae": mae(truth, predicted),
            })

ablation_df = pd.DataFrame(ablation)
wide = ablation_df.pivot_table(index=["asset", "model"], columns="variant", values="mae")
wide["delta_pct_vs_P0"] = (wide["P2"] - wide["P0"]) / wide["P0"] * 100
wide.round(4)
"""
    ),
    code(
        """
print("Effect of scaling (P0 -> P2) on validation MAE")
for (asset, model), row in wide.iterrows():
    tag = "  <- exactly invariant (as theory predicts)" if abs(row["delta_pct_vs_P0"]) < 1e-9 else ""
    print(f"  {asset}  {model:24s} {row['delta_pct_vs_P0']:+7.4f}%{tag}")

fig, ax = plt.subplots(figsize=(8, 3.6))
labels = [f"{a}/{m}" for a, m in wide.index]
ax.barh(labels, wide["delta_pct_vs_P0"], color=["tab:red" if v > 0 else "tab:green" for v in wide["delta_pct_vs_P0"]])
ax.axvline(0, color="black", lw=1)
ax.set_xlabel("change in validation MAE when scaling is applied (%)")
ax.set_title("Scaling barely matters for these models — and is exactly neutral for trees")
ax.tick_params(axis="y", labelsize=8)
fig.tight_layout()
plt.show()
"""
    ),
    md(
        """
## 8. Worked examples for learners

### Example A — why R² can look impressive while a model has no skill

R² compares variance explained *around the mean of the evaluation window*. On a
trending price series, the mean is far from every point, so variance is huge and
even a naive forecast scores high. That is why this project reports skill relative
to persistence alongside R².

### Example B — spot the leakage

The next cell contains a **deliberately leaky** feature. Decide what is wrong
before running it.
"""
    ),
    code(
        """
def leaky_features(frame):
    out = pd.DataFrame(index=frame.index)
    out["ret_1"] = frame["close"].pct_change(1)
    out["tomorrow_ret"] = frame["close"].pct_change(1).shift(-1)   # <-- look here
    return out

leaky = leaky_features(frame)
print("correlation of each feature with the realised next-day return:")
target = frame["close"].pct_change(1).shift(-1)
for column in leaky.columns:
    print(f"  {column:14s} {leaky[column].corr(target):+.3f}")

print()
print("Answer: 'tomorrow_ret' is shift(-1) — it IS the target. A correlation of +1.000")
print("means the model would be predicting the answer, not forecasting it.")
print("It is also unavailable at decision time, so it could never be used in practice.")
"""
    ),
    md(
        """
### Example C — why the naive baseline is hard to beat

Daily price changes are close to unpredictable in sign. The cell below shows how
much of next-day variance is explained by yesterday's return: if it is near zero,
momentum cannot be learned from `ret_1` alone, and no amount of model capacity
creates information that is not in the features.
"""
    )
    ,
    code(
        """
for asset in ("AAPL", "BTC"):
    close = frames[asset]["close"]
    r = close.pct_change(1)
    print(f"{asset}: corr(ret_t, ret_t+1) = {r.corr(r.shift(-1)):+.4f}   "
          f"(R^2 = {r.corr(r.shift(-1))**2:.4f})")
print()
print("A near-zero autocorrelation is the statistical face of the random-walk-like")
print("behaviour that makes persistence a strong baseline. This is the honest")
print("conclusion of the comparison, not a failure of the models.")
"""
    ),
    md(
        """
## 9. Limitations and responsible interpretation

1. **This is not investment advice.** Error metrics say nothing about profit,
   risk, or transaction costs. A model with low MAE can lose money.
2. **Short horizons are close to unpredictable.** Persistence is strong on
   one-session-ahead closes; that is a property of the data, not a modelling flaw.
3. **Two assets, one window.** AAPL and BTC over 2021–2026 cover specific market
   regimes. Conclusions do not generalise to other periods or assets.
4. **BTC is a venue-specific USDT price**, not a global USD index.
5. **Adjusted vs raw prices.** We use raw close; dividends are ignored, and
   adjusted series carry retroactive factors that can leak into history.
6. **No learner study was conducted.** The educational material is a *designed
   resource*; no claim about student learning outcomes is made.
7. **The test block is sealed.** Nothing here was tuned on it.

### Where the numbers come from

Every figure and metric in the submitted report is regenerated from
`experiments/models/` by `scripts/reproduce.sh`, and each run manifest records
the git commit, dataset SHA-256, protocol version, seed and hyperparameters.
"""
    ),
    code(
        """
print(int4096.DISCLAIMER)
"""
    ),
]


def build() -> Path:
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = CELLS
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.10"},
        "colab": {"provenance": [], "toc_visible": True},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.validate(notebook)
    OUT.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    return OUT


if __name__ == "__main__":
    path = build()
    notebook = nbf.read(path, as_version=4)
    print(f"wrote {path}")
    print(f"cells: {len(notebook.cells)} ({sum(c.cell_type == 'code' for c in notebook.cells)} code)")
