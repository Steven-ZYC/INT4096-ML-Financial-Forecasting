"""Snapshot schema, loader strictness and data quality checks."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from int4096.data.load import CANONICAL_COLUMNS, load_snapshot
from int4096.data.validate import validate_frame


def _write_snapshot(tmp_path: Path, records: list[dict]) -> Path:
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def _records(n: int = 40, start: str = "2022-01-03") -> list[dict]:
    dates = pd.date_range(start, periods=n, freq="B").strftime("%Y-%m-%d")
    return [
        {
            "date": d,
            "open": 100.0 + i,
            "high": 101.0 + i,
            "low": 99.0 + i,
            "close": 100.5 + i,
            "volume": 1_000.0 + i,
            "adj_close": 100.0 + i,
        }
        for i, d in enumerate(dates)
    ]


def test_loader_produces_canonical_schema(tmp_path):
    path = _write_snapshot(tmp_path, _records())
    frame = load_snapshot("AAPL", path=path)

    assert list(frame.columns) == CANONICAL_COLUMNS
    assert frame.index.name == "ts"
    assert str(frame.index.tz) == "UTC"
    assert frame.index.is_monotonic_increasing
    assert not frame.index.has_duplicates
    assert frame["close"].dtype == np.float64


def test_loader_rejects_duplicate_timestamps(tmp_path):
    records = _records()
    records.insert(5, dict(records[4]))  # duplicate session
    path = _write_snapshot(tmp_path, records)
    with pytest.raises(ValueError, match="duplicate"):
        load_snapshot("AAPL", path=path)


def test_loader_rejects_unsorted_snapshot(tmp_path):
    records = _records()
    records[3], records[7] = records[7], records[3]
    path = _write_snapshot(tmp_path, records)
    with pytest.raises(ValueError, match="not sorted"):
        load_snapshot("AAPL", path=path)


def test_loader_rejects_missing_columns(tmp_path):
    records = _records()
    for row in records:
        row.pop("volume")
    path = _write_snapshot(tmp_path, records)
    with pytest.raises(ValueError, match="missing columns"):
        load_snapshot("AAPL", path=path)


def test_validation_passes_on_clean_data(tmp_path):
    frame = load_snapshot("AAPL", path=_write_snapshot(tmp_path, _records()))
    report = validate_frame(frame)
    assert report.passed, report.issues
    assert report.checks["has_adjusted_close"] is True


def test_validation_flags_negative_prices(tmp_path):
    records = _records()
    records[10]["close"] = -5.0
    frame = load_snapshot("AAPL", path=_write_snapshot(tmp_path, records))
    report = validate_frame(frame)
    assert not report.passed
    assert any("non-positive" in issue for issue in report.issues)


def test_validation_flags_high_below_low(tmp_path):
    records = _records()
    records[12]["high"] = 1.0
    records[12]["low"] = 500.0
    frame = load_snapshot("AAPL", path=_write_snapshot(tmp_path, records))
    report = validate_frame(frame)
    assert not report.passed
    assert any("high < low" in issue for issue in report.issues)


def test_validation_reports_missing_without_repairing(tmp_path):
    records = _records()
    records[4]["close"] = None
    frame = load_snapshot("AAPL", path=_write_snapshot(tmp_path, records))
    report = validate_frame(frame)
    assert report.checks["missing_values"]["close"] == 1
    assert not report.passed
    # The loader/validator must not have filled the hole.
    assert frame["close"].isna().sum() == 1


def test_validation_explains_zero_volume_rather_than_failing(tmp_path):
    records = _records()
    for row in records[:3]:
        row["volume"] = 0.0
    frame = load_snapshot("AAPL", path=_write_snapshot(tmp_path, records))
    report = validate_frame(frame)
    assert report.checks["zero_volume"] == 3
    # Zero volume is reported as context, not automatically a blocker.
    assert report.checks["zero_volume_pct"] > 0


def test_real_snapshot_counts_if_present():
    """If the real snapshots exist, their manifests must match the files.

    Skipped on a fresh clone without data, so the suite stays runnable offline.
    """
    from int4096.config import REPO_ROOT
    from int4096.data.load import resolve_snapshot_path, read_manifest
    from int4096.data.snapshot import sha256_file

    for asset in ("AAPL", "BTC"):
        path = resolve_snapshot_path(asset)
        if not path.exists():
            pytest.skip(f"no local snapshot for {asset}")
        manifest = read_manifest(asset)
        assert manifest["asset"] == asset
        assert len(manifest["sha256"]) == 64
        assert sha256_file(path) == manifest["sha256"], "snapshot hash drift detected"
        assert manifest["row_count"] > 100
