"""Write the chronological split and the tuning folds of each asset to data/splits/.

The split is computed in code (int4096.data.split) from the frozen protocol; this
script only records the result so it can be read without running anything:

    data/splits/aapl.json, data/splits/btc.json   machine-readable boundaries
    data/splits/README.md                          the same, as tables

Run: PYTHONPATH=src python scripts/export_splits.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.data.split import expanding_window_folds  # noqa: E402
from int4096.experiments.run import prepare_dataset  # noqa: E402
from int4096.paths import DATA_SPLITS  # noqa: E402


def day(ts) -> str:
    return f"{ts:%Y-%m-%d}"


def describe(asset: str, protocol) -> dict:
    prepared = prepare_dataset(asset, protocol)
    X, split = prepared["X"], prepared["split"]
    idx = X.index
    block = lambda a, b: {"first": day(idx[a]), "last": day(idx[b - 1]), "rows": int(b - a)}  # noqa: E731
    purged = [day(idx[i]) for i in range(split.train_end, split.validation_start)]
    purged += [day(idx[i]) for i in range(split.validation_end, split.test_start)]

    n_train = split.train_end - split.train_start
    folds = expanding_window_folds(
        n_train,
        n_splits=int(protocol.cv["n_splits"]),
        gap=int(protocol.cv["gap"]),
        min_train_fraction=float(protocol.cv["min_train_fraction"]),
    )
    fold_rows = []
    for k, (fit, score) in enumerate(folds, start=1):
        fit, score = fit + split.train_start, score + split.train_start
        fold_rows.append({
            "fold": k,
            "fit": {"first": day(idx[fit[0]]), "last": day(idx[fit[-1]]), "rows": int(len(fit))},
            "score": {"first": day(idx[score[0]]), "last": day(idx[score[-1]]), "rows": int(len(score))},
        })

    return {
        "asset": asset,
        "protocol_version": protocol.version,
        "rule": "chronological 60/20/20 on the asset's own calendar; one row purged at each boundary",
        "modelling_rows": int(len(idx)),
        "train": block(split.train_start, split.train_end),
        "validation": block(split.validation_start, split.validation_end),
        "test_sealed": block(split.test_start, split.test_end),
        "purged_rows": purged,
        "tuning_folds": {
            "scheme": "expanding window inside the training block only",
            "gap_rows": int(protocol.cv["gap"]),
            "folds": fold_rows,
        },
    }


def main() -> int:
    protocol = load_protocol()
    DATA_SPLITS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Data splits",
        "",
        "**Generated** by `scripts/export_splits.py` from the frozen protocol "
        "(`configs/research_protocol.yaml`) and `src/int4096/data/split.py`. Do not edit by hand.",
        "",
        "Every model on an asset uses exactly these rows. Tuning only ever sees the training block, "
        "through the expanding-window folds below. The validation block is used once, for reporting. "
        "The test block is sealed.",
        "",
    ]
    for asset in ("AAPL", "BTC"):
        info = describe(asset, protocol)
        (DATA_SPLITS / f"{asset.lower()}.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        lines += [
            f"## {asset} ({info['modelling_rows']:,} modelling rows)",
            "",
            "| Block | First day | Last day | Rows |",
            "|---|---|---|---:|",
        ]
        for key, name in (("train", "Train (60%)"), ("validation", "Validation (20%)"),
                          ("test_sealed", "Test (20%, sealed)")):
            b = info[key]
            lines.append(f"| {name} | {b['first']} | {b['last']} | {b['rows']:,} |")
        lines += ["", f"Purged boundary rows: {', '.join(info['purged_rows'])}.", "",
                  "| Tuning fold | Fit on | Score on |", "|---:|---|---|"]
        for f in info["tuning_folds"]["folds"]:
            lines.append(f"| {f['fold']} | {f['fit']['first']} – {f['fit']['last']} ({f['fit']['rows']}) "
                         f"| {f['score']['first']} – {f['score']['last']} ({f['score']['rows']}) |")
        lines.append("")
    (DATA_SPLITS / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {DATA_SPLITS.relative_to(REPO_ROOT)}/{{aapl,btc}}.json and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
