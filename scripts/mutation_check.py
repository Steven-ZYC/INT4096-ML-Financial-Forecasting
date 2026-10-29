"""Mutation testing for the temporal-integrity suite.

A passing test suite proves nothing unless the tests can fail. This script
injects the canonical leakage defects one at a time, runs the leakage tests, and
asserts that the suite **detects** each one. It restores every file afterwards,
including on error or interruption.

Usage
-----
    python scripts/mutation_check.py

Exit code 0 means every injected defect was caught.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_FILE = REPO_ROOT / "src" / "int4096" / "features" / "build.py"
PIPELINE_FILE = REPO_ROOT / "src" / "int4096" / "features" / "pipeline.py"


@dataclass
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    expected_test: str


MUTATIONS = [
    Mutation(
        name="features read the next bar (shift(-1))",
        path=BUILD_FILE,
        old='        out[f"ret_{h}"] = _safe_div(close, close.shift(h)) - 1.0',
        new='        out[f"ret_{h}"] = _safe_div(close.shift(-h), close) - 1.0',
        expected_test="test_features_match_independent_trailing_formulas",
    ),
    Mutation(
        name="centred rolling window",
        path=BUILD_FILE,
        old="sma = close.rolling(window=w, min_periods=min_periods or w).mean()",
        new=(
            "sma = close.rolling(window=w, min_periods=min_periods or w, "
            "center=True).mean()"
        ),
        expected_test="test_features_match_independent_trailing_formulas",
    ),
    Mutation(
        name="backward fill of missing inputs",
        path=BUILD_FILE,
        old='    out = pd.DataFrame(index=frame.index)\n    sma = frame["volume"].rolling(',
        new=(
            '    out = pd.DataFrame(index=frame.index)\n    frame = frame.bfill()\n'
            '    sma = frame["volume"].rolling('
        ),
        expected_test="test_no_nan_is_silently_filled_from_the_future",
    ),
    Mutation(
        name="whole-series statistic instead of trailing window",
        path=BUILD_FILE,
        old='    for w in windows:\n        out[f"vol_{w}"] = rets.rolling(\n            window=w, min_periods=min_periods or w\n        ).std(ddof=0)',
        new='    for w in windows:\n        out[f"vol_{w}"] = float(rets.std(ddof=0))',
        expected_test="test_features_match_independent_trailing_formulas",
    ),
    Mutation(
        name="preprocessing fitted on train+apply rows",
        path=PIPELINE_FILE,
        old=(
            "    preprocessor = build_preprocessor(variant)\n"
            "    if preprocessor is not None:\n"
            "        train_matrix = preprocessor.fit_transform(train_matrix)\n"
            "        apply_matrix = preprocessor.transform(apply_matrix)"
        ),
        new=(
            "    preprocessor = build_preprocessor(variant)\n"
            "    if preprocessor is not None:\n"
            "        import numpy as _np\n"
            "        preprocessor.fit(_np.vstack([train_matrix, apply_matrix]))\n"
            "        train_matrix = preprocessor.transform(train_matrix)\n"
            "        apply_matrix = preprocessor.transform(apply_matrix)"
        ),
        expected_test="test_project_preprocessor_is_train_fitted",
    ),
]


def run_leakage_tests() -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_temporal_integrity.py",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(REPO_ROOT / "src"), "PATH": "/usr/bin:/bin"},
    )


def main() -> int:
    baseline = run_leakage_tests()
    if baseline.returncode != 0:
        print("Baseline suite is already failing; fix that before mutation testing.")
        print(baseline.stdout[-3000:])
        return 2
    print(f"baseline: PASS ({(baseline.stdout.strip().splitlines() or ['?'])[-1]})\n")

    survivors: list[str] = []
    for mutation in MUTATIONS:
        original = mutation.path.read_text(encoding="utf-8")
        try:
            if mutation.old not in original:
                print(f"SKIP  {mutation.name}: anchor text not found")
                survivors.append(mutation.name)
                continue
            mutation.path.write_text(
                original.replace(mutation.old, mutation.new, 1), encoding="utf-8"
            )
            result = run_leakage_tests()
            caught = result.returncode != 0
            marker = "CAUGHT" if caught else "SURVIVED"
            print(f"{marker:9s} {mutation.name}")
            if not caught:
                survivors.append(mutation.name)
            else:
                failing = [
                    line.split("::")[-1].split(" ")[0]
                    for line in result.stdout.splitlines()
                    if line.startswith("FAILED")
                ]
                print(f"          failing tests: {', '.join(failing[:3])}")
        finally:
            mutation.path.write_text(original, encoding="utf-8")

    print()
    if survivors:
        print(f"FAIL: {len(survivors)} mutation(s) survived: {survivors}")
        return 1
    print(f"PASS: all {len(MUTATIONS)} injected defects were detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
