"""Supplementary test: can a neural network call tomorrow's direction?

This is an ADD-ON experiment, separate from the frozen 20-run comparison
(protocol v1.1). It asks a simpler question than the main study: how often does
a model correctly predict whether the next close is HIGHER than today's close?
It compares two neural networks:

  MLP   reads today's 10 engineered features (the same columns as the main study).
  LSTM  reads the last SEQ_LEN days of those 10 features as a sequence.

What is kept from the main protocol (non-negotiable)
----------------------------------------------------
* Same snapshots, same chronological 60/20/20 split, same purged boundary rows.
* Every input is computable at the close of day t; the label is day t+1.
* Standardisation statistics come from the training block only.
* Model choice and early stopping use a time-ordered hold-out carved from the
  END of the training block (with a one-row gap). The validation block is used
  once, for reporting. The sealed test block is never read.

What is deliberately different
------------------------------
* The target is a binary direction (up / not up), trained with cross-entropy.
* The LSTM sees a sequence, so it is not an identical-input comparison. This is
  stated in the output and on the slide.

Yardsticks reported alongside
-----------------------------
* "Always predict the training majority" (usually "up").
* A coin flip (50%).
* The direction accuracy of the five classical models (from metrics.json).

Uncertainty: a moving-block bootstrap (block 10, 1,000 resamples) of the
accuracy difference versus the majority rule, on the validation dates. Indicative,
not confirmatory; consecutive days are dependent.

Run (from the repository root)
------------------------------
    # 1. PyTorch with CUDA, once (see https://pytorch.org/get-started/locally/):
    #    pip install torch --index-url https://download.pytorch.org/whl/cu124
    # 2. The experiment:
    python scripts/supplementary_direction_test.py
    # Quick check that everything is wired up (a few epochs, one seed):
    python scripts/supplementary_direction_test.py --smoke

Output: artifacts/supplementary/direction_test/<UTC timestamp>/
    results.json        every number the slide and report may quote
    predictions.csv     per-date validation probabilities and labels
    holdout_search.csv  every configuration tried, scored on the training hold-out
Nothing here is investment advice; direction accuracy ignores costs and risk.
"""

from __future__ import annotations

import argparse
import csv
import json
import platform
import random
import sys
import time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.experiments.run import prepare_dataset  # noqa: E402

try:
    import torch
    from torch import nn
except ImportError as exc:  # pragma: no cover - environment message
    raise SystemExit(
        "PyTorch is required: pip install torch (see the module docstring)."
    ) from exc

ASSETS = ("AAPL", "BTC")
SEQ_LEN = 20                 # LSTM look-back in trading days (bars of each asset)
HOLDOUT_FRACTION = 0.20      # end of the training block used for early stopping
GAP = 1                      # rows dropped between inner-fit and hold-out (label overlap)
SEEDS = (0, 1, 2, 3, 4)      # final predictions average these seeds
GRID = {
    "hidden": (16, 32, 64),
    "dropout": (0.0, 0.2),
    "lr": (1e-3, 3e-3),
}
MAX_EPOCHS = 300
PATIENCE = 20
BATCH = 64
WEIGHT_DECAY = 1e-4
BLOCK, RESAMPLES = 10, 1000


# --------------------------------------------------------------------------- data
def load_asset(asset: str, protocol) -> dict:
    """Features, direction labels and index ranges for one asset (no test rows)."""
    prepared = prepare_dataset(asset, protocol)
    X, y, split = prepared["X"], prepared["y"], prepared["split"]
    if protocol.label_mode != "delta":
        raise SystemExit("Expected label_mode 'delta' (y = Close[t+1] - Close[t]).")
    feats = X.to_numpy(dtype="float32")
    up = (y.to_numpy(dtype="float64") > 0).astype("float32")   # strict rise = 1

    train = np.arange(split.train_start, split.train_end)
    val = np.arange(split.validation_start, split.validation_end)
    n_hold = int(round(len(train) * HOLDOUT_FRACTION))
    inner = train[: len(train) - n_hold - GAP]
    hold = train[len(train) - n_hold:]

    # Standardise with statistics from the full training block only.
    mean = feats[train].mean(axis=0)
    std = feats[train].std(axis=0)
    std[std == 0] = 1.0
    z = (feats - mean) / std

    return {
        "asset": asset, "z": z, "up": up, "dates": X.index,
        "inner": inner, "hold": hold, "train": train, "val": val,
        "columns": list(X.columns),
        "train_up_rate": float(up[train].mean()),
        "val_up_rate": float(up[val].mean()),
    }


def make_inputs(d: dict, rows: np.ndarray, kind: str) -> tuple[np.ndarray, np.ndarray]:
    """Rows -> model inputs. LSTM rows need SEQ_LEN past days; earlier rows are skipped."""
    if kind == "mlp":
        return d["z"][rows], rows
    keep = rows[rows >= SEQ_LEN - 1]
    seq = np.stack([d["z"][r - SEQ_LEN + 1: r + 1] for r in keep])   # days t-19 .. t
    return seq, keep


# ------------------------------------------------------------------------- models
class MLP(nn.Module):
    def __init__(self, n_in: int, hidden: int, dropout: float):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_in, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


class LSTMNet(nn.Module):
    def __init__(self, n_in: int, hidden: int, dropout: float):
        super().__init__()
        self.lstm = nn.LSTM(n_in, hidden, batch_first=True)
        self.drop = nn.Dropout(dropout)
        self.head = nn.Linear(hidden, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(self.drop(out[:, -1, :])).squeeze(-1)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_one(kind, x_fit, y_fit, x_hold, y_hold, cfg, seed, device, max_epochs):
    """Fit with early stopping on the training hold-out; return model and best hold-out loss."""
    set_seed(seed)
    n_in = x_fit.shape[-1]
    model = (MLP if kind == "mlp" else LSTMNet)(n_in, cfg["hidden"], cfg["dropout"]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=cfg["lr"], weight_decay=WEIGHT_DECAY)
    loss_fn = nn.BCEWithLogitsLoss()
    xf = torch.tensor(x_fit, device=device)
    yf = torch.tensor(y_fit, device=device)
    xh = torch.tensor(x_hold, device=device)
    yh = torch.tensor(y_hold, device=device)
    gen = torch.Generator(device="cpu").manual_seed(seed)

    best, best_state, bad = float("inf"), None, 0
    for _ in range(max_epochs):
        model.train()
        # Mini-batches are shuffled INSIDE the training rows only; no row from a
        # later block is ever involved, so this is not a shuffled split.
        order = torch.randperm(len(xf), generator=gen).to(device)
        for i in range(0, len(order), BATCH):
            idx = order[i: i + BATCH]
            opt.zero_grad()
            loss_fn(model(xf[idx]), yf[idx]).backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            hold_loss = float(loss_fn(model(xh), yh))
        if hold_loss < best - 1e-5:
            best, bad = hold_loss, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= PATIENCE:
                break
    model.load_state_dict(best_state)
    return model, best


def predict(model, x, device) -> np.ndarray:
    model.eval()
    with torch.no_grad():
        return torch.sigmoid(model(torch.tensor(x, device=device))).cpu().numpy()


# ---------------------------------------------------------------------- evaluation
def accuracy(prob: np.ndarray, up: np.ndarray) -> float:
    return float(np.mean((prob > 0.5).astype("float32") == up))


def block_bootstrap_diff(hit_a: np.ndarray, hit_b: np.ndarray, seed: int = 42) -> tuple[float, float]:
    """95% moving-block interval for mean(hit_a) - mean(hit_b) on the same dates."""
    rng = np.random.default_rng(seed)
    n = len(hit_a)
    n_blocks = int(np.ceil(n / BLOCK))
    diffs = np.empty(RESAMPLES)
    for b in range(RESAMPLES):
        starts = rng.integers(0, n - BLOCK + 1, size=n_blocks)
        idx = np.concatenate([np.arange(s, s + BLOCK) for s in starts])[:n]
        diffs[b] = hit_a[idx].mean() - hit_b[idx].mean()
    return float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def classical_direction(asset: str) -> dict:
    """Direction accuracy of the main study's 20 runs (validation), for reference."""
    out = {}
    for path in sorted((REPO_ROOT / "artifacts" / "experiments").glob(f"*_{asset.lower()}_*/metrics.json")):
        m = json.loads(path.read_text(encoding="utf-8"))
        acc = m["metrics"].get("validation_direction_accuracy")
        if acc is not None and acc == acc:
            out[f"{m['model_id']}_{m['preprocess_variant']}"] = float(acc)
    return out


def run_asset(d: dict, kind: str, device, seeds, max_epochs, search_rows: list) -> dict:
    x_in, r_in = make_inputs(d, d["inner"], kind)
    x_ho, r_ho = make_inputs(d, d["hold"], kind)
    x_va, r_va = make_inputs(d, d["val"], kind)
    y_in, y_ho, y_va = d["up"][r_in], d["up"][r_ho], d["up"][r_va]

    # 1) Choose the configuration on the training hold-out (seed 0 only).
    best_cfg, best_loss = None, float("inf")
    for hidden, dropout, lr in product(GRID["hidden"], GRID["dropout"], GRID["lr"]):
        cfg = {"hidden": hidden, "dropout": dropout, "lr": lr}
        model, loss = train_one(kind, x_in, y_in, x_ho, y_ho, cfg, seeds[0], device, max_epochs)
        hold_acc = accuracy(predict(model, x_ho, device), y_ho)
        search_rows.append({"asset": d["asset"], "model": kind, **cfg,
                            "holdout_logloss": round(loss, 5), "holdout_accuracy": round(hold_acc, 4)})
        if loss < best_loss:
            best_cfg, best_loss = cfg, loss

    # 2) Train the chosen configuration with every seed; average probabilities.
    probs, seed_acc = [], []
    for seed in seeds:
        model, _ = train_one(kind, x_in, y_in, x_ho, y_ho, best_cfg, seed, device, max_epochs)
        p = predict(model, x_va, device)
        probs.append(p)
        seed_acc.append(accuracy(p, y_va))
    prob = np.mean(probs, axis=0)

    majority = 1.0 if d["train_up_rate"] >= 0.5 else 0.0
    hit_model = ((prob > 0.5).astype("float32") == y_va).astype("float64")
    hit_major = (np.full_like(y_va, majority) == y_va).astype("float64")
    lo, hi = block_bootstrap_diff(hit_model, hit_major)
    return {
        "chosen_config": best_cfg,
        "holdout_logloss": round(best_loss, 5),
        "n_validation": int(len(y_va)),
        "accuracy_ensemble": round(float(hit_model.mean()), 4),
        "accuracy_by_seed": [round(a, 4) for a in seed_acc],
        "share_predicted_up": round(float((prob > 0.5).mean()), 4),
        "majority_rule": "always up" if majority == 1.0 else "always down",
        "majority_accuracy": round(float(hit_major.mean()), 4),
        "diff_vs_majority": round(float(hit_model.mean() - hit_major.mean()), 4),
        "diff_vs_majority_ci95": [round(lo, 4), round(hi, 4)],
        "ci_includes_zero": bool(lo <= 0.0 <= hi),
        "validation_rows": r_va.tolist(),
        "probabilities": prob.tolist(),
    }


# ----------------------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--smoke", action="store_true", help="tiny run to check wiring")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "artifacts" / "supplementary" / "direction_test")
    parser.add_argument("--cpu", action="store_true", help="force CPU even if CUDA is available")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    seeds = SEEDS[:1] if args.smoke else SEEDS
    max_epochs = 5 if args.smoke else MAX_EPOCHS
    if args.smoke:
        GRID.update({"hidden": (16,), "dropout": (0.0,), "lr": (1e-3,)})
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = args.out / (stamp + ("_smoke" if args.smoke else ""))
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"device: {device} ({torch.cuda.get_device_name(0) if device.type == 'cuda' else platform.processor() or 'cpu'})")

    protocol = load_protocol()
    started = time.perf_counter()
    results, search_rows, pred_rows = {}, [], []
    for asset in ASSETS:
        d = load_asset(asset, protocol)
        res = {"train_up_rate": round(d["train_up_rate"], 4), "validation_up_rate": round(d["val_up_rate"], 4),
               "classical_direction_accuracy": classical_direction(asset)}
        for kind in ("mlp", "lstm"):
            t0 = time.perf_counter()
            r = run_asset(d, kind, device, seeds, max_epochs, search_rows)
            for row, p in zip(r.pop("validation_rows"), r.pop("probabilities")):
                pred_rows.append({"asset": asset, "model": kind, "date": str(d["dates"][row].date()),
                                  "prob_up": round(p, 5), "actual_up": int(d["up"][row])})
            r["seconds"] = round(time.perf_counter() - t0, 1)
            res[kind] = r
            print(f"{asset} {kind:4s} acc={r['accuracy_ensemble']:.3f} "
                  f"(seeds {min(r['accuracy_by_seed']):.3f}-{max(r['accuracy_by_seed']):.3f}) "
                  f"majority={r['majority_accuracy']:.3f} diff CI={r['diff_vs_majority_ci95']} "
                  f"cfg={r['chosen_config']} {r['seconds']}s")
        results[asset] = res

    summary = {
        "experiment": "supplementary_direction_test",
        "status": "SMOKE" if args.smoke else "COMPLETE",
        "question": "How often does the model correctly predict whether the next close is higher than today's?",
        "not_part_of": "protocol v1.1 main comparison (20 runs); reported separately",
        "data": "same snapshots, chronological split and purge as the main study; validation block only; test block not read",
        "inputs": {"mlp": "today's 10 engineered features",
                   "lstm": f"last {SEQ_LEN} days of the same 10 features (a sequence; not identical inputs)"},
        "selection": f"grid {GRID} chosen by log-loss on the last {int(HOLDOUT_FRACTION*100)}% of the training block "
                     f"(gap {GAP}); early stopping on the same hold-out; validation used once for reporting",
        "seeds": list(seeds), "max_epochs": max_epochs, "patience": PATIENCE,
        "uncertainty": f"moving-block bootstrap, block {BLOCK}, {RESAMPLES} resamples, 95%, accuracy minus majority rule",
        "device": str(device), "torch": torch.__version__, "python": platform.python_version(),
        "elapsed_seconds": round(time.perf_counter() - started, 1),
        "results": results,
    }
    (out_dir / "results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for name, rows in (("predictions.csv", pred_rows), ("holdout_search.csv", search_rows)):
        with open(out_dir / name, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    print(f"wrote {out_dir.relative_to(REPO_ROOT) if out_dir.is_relative_to(REPO_ROOT) else out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
