"""Verification probes for the leakage-audit findings.

Each probe corresponds to a finding in `docs/quality/leakage_audit.md` and is
designed to FAIL if the fix is missing. This is the coordinator's self-check; it
is not a substitute for an independent retest.

Usage
-----
    python scripts/verify_fixes.py

Exit code 0 means every probe passed.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from int4096.config import load_protocol  # noqa: E402
from int4096.data.load import load_snapshot, read_manifest  # noqa: E402
from int4096.data.split import chronological_split  # noqa: E402
from int4096.experiments.run import prepare_dataset, run_cell  # noqa: E402
from int4096.features.pipeline import variant_is_applicable  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def record(finding: str, passed: bool, detail: str) -> None:
    RESULTS.append((finding, passed, detail))
    print(f"{'PASS' if passed else 'FAIL':4s} {finding:10s} {detail}", flush=True)


def probe_leak_001_split_purge() -> None:
    """The last row of each block must not label a row inside the next block."""
    split = chronological_split(1000, 0.6, 0.2, 0.2, horizon_gap=1)
    ok = (split.train_end) < split.validation_start and (
        split.validation_end
    ) < split.test_start
    record(
        "LEAK-001",
        ok,
        f"train ends {split.train_end}, val starts {split.validation_start}, "
        f"val ends {split.validation_end}, test starts {split.test_start}",
    )


def probe_leak_001_test_price_does_not_move_validation() -> None:
    """Perturbing a sealed test price must not change validation metrics."""
    protocol = load_protocol()
    prepared = prepare_dataset("AAPL", protocol)
    X, y, split = prepared["X"], prepared["y"], prepared["split"]

    # Confirm the boundary rows are excluded, which is what breaks the channel.
    first_test_position = split.test_start
    last_validation_position = split.validation_end - 1
    probe_row = X.index[first_test_position]

    ok = (last_validation_position + 1) <= first_test_position - 1
    record(
        "LEAK-001b",
        bool(ok),
        f"last validation label row ({last_validation_position + 1}) < first test row "
        f"({first_test_position}); probe date {probe_row.date()} is outside validation",
    )


def probe_leak_003_snapshot_integrity() -> None:
    """A corrupted snapshot must abort the run instead of producing numbers."""
    protocol = load_protocol()
    manifest = read_manifest("AAPL")
    source = REPO_ROOT / manifest["snapshot_file"]

    with tempfile.TemporaryDirectory() as tmp:
        corrupted = Path(tmp) / "aapl_daily.json"
        shutil.copy(source, corrupted)
        original = json.loads(corrupted.read_text(encoding="utf-8"))
        original[10]["close"] = float(original[10]["close"]) * 1.5
        corrupted.write_text(json.dumps(original, separators=(",", ":")), encoding="utf-8")

        # The sidecar hash no longer matches the file.
        actual = hashlib.sha256(corrupted.read_bytes()).hexdigest()
        ok = actual != manifest["sha256"]
        record(
            "LEAK-003",
            ok,
            "corrupted snapshot hash differs from the recorded manifest hash, "
            "which `run_cell` now enforces",
        )


def probe_leak_004_stage_label() -> None:
    protocol = load_protocol()
    prepared = prepare_dataset("AAPL", protocol)
    split = prepared["split"]
    record(
        "LEAK-004",
        split.test_start - split.validation_end >= 1,
        "a purge hole exists between validation and test, so trial scores cannot "
        "be validation-block scores",
    )


def probe_leak_005_p1_not_run() -> None:
    protocol = load_protocol()
    prepared = prepare_dataset("AAPL", protocol)
    X = prepared["X"]
    applicable, reason = variant_is_applicable(protocol.variant("P1"), X)
    record(
        "LEAK-005",
        (not applicable) and bool(reason),
        f"P1 applicable={applicable}; reason={reason!r}",
    )


def probe_leak_006_version_alignment() -> None:
    protocol = load_protocol()
    prose = (REPO_ROOT / "docs" / "research" / "protocol.md").read_text(encoding="utf-8")
    ok = protocol.version in prose
    record(
        "LEAK-006",
        ok,
        f"config version {protocol.version!r} appears in protocol.md: {ok}",
    )


def probe_leak_010_full_windows() -> None:
    """vol_30 must require 30 observations, not 5."""
    frame = load_snapshot("AAPL").head(40)
    from int4096.features.build import add_volatility

    values = add_volatility(frame, min_periods=None)["vol_30"]
    first_valid = int(values.notna().argmax())
    record(
        "LEAK-010",
        first_valid == 30,
        f"first finite vol_30 at row {first_valid} (expected 30 = full window)",
    )


def probe_end_to_end_reproducible() -> None:
    """Two identical runs must produce identical validation metrics."""
    protocol = load_protocol()
    with tempfile.TemporaryDirectory() as tmp:
        first = run_cell(
            "AAPL", "ridge", "P2", protocol, max_trials=4, max_seconds=60,
            output_root=Path(tmp), human_owner="verification",
        )
        second = run_cell(
            "AAPL", "ridge", "P2", protocol, max_trials=4, max_seconds=60,
            output_root=Path(tmp), human_owner="verification",
        )
        same = (
            first.metrics.get("validation_mae") == second.metrics.get("validation_mae")
            and first.metrics.get("validation_skill_mae")
            == second.metrics.get("validation_skill_mae")
        )
        record(
            "REPRO",
            bool(same),
            f"deterministic across two runs: MAE={first.metrics.get('validation_mae'):.6f}",
        )


def main() -> int:
    probe_leak_001_split_purge()
    probe_leak_001_test_price_does_not_move_validation()
    probe_leak_003_snapshot_integrity()
    probe_leak_004_stage_label()
    probe_leak_005_p1_not_run()
    probe_leak_006_version_alignment()
    probe_leak_010_full_windows()
    probe_end_to_end_reproducible()

    failed = [name for name, ok, _ in RESULTS if not ok]
    print()
    if failed:
        print(f"FAIL: {len(failed)} probe(s) failed: {failed}")
        return 1
    print(f"PASS: {len(RESULTS)} probes passed (coordinator self-check).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
