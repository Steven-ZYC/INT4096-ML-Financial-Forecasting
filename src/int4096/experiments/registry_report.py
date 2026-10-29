"""Generate `docs/research/run_registry.md` from the machine-readable registry.

Markdown is generated, never hand-edited, so the coverage counts in the report
cannot drift from the artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from ..config import REPO_ROOT

ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "experiments"
DOCS_PATH = REPO_ROOT / "docs" / "research" / "run_registry.md"


def build_report(artifact_root: Path | None = None) -> str:
    root = Path(artifact_root) if artifact_root else ARTIFACT_ROOT
    registry = root / "registry.jsonl"
    if not registry.exists():
        raise FileNotFoundError(f"No registry at {registry}; run an experiment first.")

    rows = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines() if line.strip()]
    frame = pd.DataFrame(rows)
    counts = frame["status"].value_counts().to_dict()
    total = len(frame)

    lines = [
        "# Run Registry",
        "",
        "**Generated** by `python -m int4096.experiments.registry_report` from",
        "`artifacts/experiments/registry.jsonl`. Do not edit by hand.",
        "",
        "The registry is **append-only**. A failed run is never deleted: failures are",
        "evidence, and the coverage table below depends on them being visible.",
        "",
        "## Coverage",
        "",
        "| Status | Count |",
        "|---|---|",
    ]
    for status in ("SUCCESS", "FAILED", "INCOMPLETE", "NOT_RUN"):
        lines.append(f"| {status} | {counts.get(status, 0)} |")
    lines += [
        f"| **Total attempted** | **{total}** |",
        "",
        "## Cells",
        "",
        "| run_id | status | asset | model | variant | val MAE | skill_MAE | test | review |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    ordered = frame.sort_values(["asset", "model_id", "preprocess_variant", "run_id"])
    for row in ordered.itertuples():
        def fmt(value):
            if value is None or (isinstance(value, float) and value != value):
                return "n/a"
            return f"{value:.4f}" if isinstance(value, float) else str(value)

        lines.append(
            f"| `{row.run_id}` | {row.status} | {row.asset} | {row.model_id} | "
            f"{row.preprocess_variant} | {fmt(row.validation_mae)} | "
            f"{fmt(row.validation_skill_mae)} | {fmt(row.test_mae)} | {row.review_state} |"
        )

    lines += [
        "",
        "## Explicit gaps",
        "",
        "Cells that were planned but not executed are listed here rather than omitted,",
        "so the report cannot imply coverage that does not exist.",
        "",
    ]

    if "asset" in frame and "model_id" in frame:
        assets = sorted(frame["asset"].unique())
        models = sorted(frame["model_id"].unique())
        variants = sorted(frame["preprocess_variant"].unique())
        missing = []
        for asset in assets:
            for model in models:
                for variant in variants:
                    present = frame[
                        (frame["asset"] == asset)
                        & (frame["model_id"] == model)
                        & (frame["preprocess_variant"] == variant)
                        & (frame["status"] == "SUCCESS")
                    ]
                    if present.empty:
                        missing.append((asset, model, variant))
        if missing:
            lines += ["| Asset | Model | Variant | Reason |", "|---|---|---|---|"]
            for asset, model, variant in missing:
                reason = "not executed"
                if variant == "P1":
                    reason = "NOT_RUN: no missing inputs in snapshot (decision D13)"
                lines.append(f"| {asset} | {model} | {variant} | {reason} |")
        else:
            lines.append("None: every asset x model x variant cell in the registry succeeded.")

    lines += [
        "",
        "## What this registry does not prove",
        "",
        "- It does not prove the runs are correct; that is the leakage auditor's job.",
        "- `test` is `n/a` for every row until a single human-approved release occurs",
        "  (decision D7). Absence of test metrics is deliberate, not missing work.",
        "- `review_state` is `UNREVIEWED` until an independent auditor signs off.",
        "",
    ]
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate the run registry report.")
    parser.add_argument("--artifact-root", default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    text = build_report(args.artifact_root)
    out = Path(args.out) if args.out else DOCS_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
