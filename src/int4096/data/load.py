"""Canonical snapshot loading.

Converts either provider's snapshot into one schema:

    index : DatetimeIndex (UTC, tz-aware, unique, strictly increasing), name='ts'
    columns : open, high, low, close, volume, adj_close

``adj_close`` is NaN when the provider has no corporate actions (BTC).

The loader is deliberately strict: it raises on duplicate or unsorted
timestamps rather than sorting them away, because a silently reordered time
series is exactly the class of bug this project must catch.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config import REPO_ROOT, load_protocol

CANONICAL_COLUMNS = ["open", "high", "low", "close", "volume", "adj_close"]


def resolve_snapshot_path(asset: str, protocol_path: str | Path | None = None) -> Path:
    protocol = load_protocol(protocol_path)
    configured = Path(protocol.asset(asset)["snapshot_file"])
    return configured if configured.is_absolute() else REPO_ROOT / configured


def read_manifest(asset: str, protocol_path: str | Path | None = None) -> dict[str, Any]:
    """Read the SHA256/provenance sidecar written next to the snapshot."""
    path = resolve_snapshot_path(asset, protocol_path).with_suffix(".manifest.json")
    if not path.exists():
        raise FileNotFoundError(
            f"Missing snapshot manifest: {path}. "
            f"Create it with: python -m int4096.data.snapshot --asset {asset}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_snapshot(
    asset: str,
    protocol_path: str | Path | None = None,
    path: str | Path | None = None,
):
    """Load a snapshot as the canonical frame.

    Parameters
    ----------
    asset : 'AAPL' or 'BTC'
    path : optional explicit snapshot path (used by tests with fixtures)
    """
    import pandas as pd

    protocol = load_protocol(protocol_path)
    cfg = protocol.asset(asset)
    snapshot = Path(path) if path is not None else resolve_snapshot_path(asset, protocol_path)
    if not snapshot.exists():
        raise FileNotFoundError(
            f"Snapshot not found: {snapshot}. "
            f"Run: python -m int4096.data.snapshot --asset {asset}"
        )

    records = json.loads(snapshot.read_text(encoding="utf-8"))
    if not records:
        raise ValueError(f"Snapshot {snapshot} is empty.")

    frame = pd.DataFrame.from_records(records)
    missing = {"date", *CANONICAL_COLUMNS} - set(frame.columns)
    if missing:
        raise ValueError(f"Snapshot {snapshot} is missing columns: {sorted(missing)}")

    # All providers express a daily bar as a calendar date. Daily bars are
    # normalised to midnight UTC so that AAPL (exchange local close) and BTC
    # (UTC close) share one index *type* while remaining separate datasets.
    # We never merge the two indexes.
    index = pd.to_datetime(frame["date"], utc=True)
    frame = frame.drop(columns=["date"])
    frame.index = pd.DatetimeIndex(index, name="ts")

    if frame.index.has_duplicates:
        dupes = frame.index[frame.index.duplicated()].unique()[:5].tolist()
        raise ValueError(
            f"{asset} snapshot has duplicate timestamps, e.g. {dupes}. "
            "Refusing to load: a duplicate session would corrupt the label shift."
        )
    if not frame.index.is_monotonic_increasing:
        raise ValueError(
            f"{asset} snapshot is not sorted ascending by timestamp. "
            "Refusing to auto-sort: order is part of the data contract."
        )

    frame = frame[CANONICAL_COLUMNS].astype("float64")
    frame.attrs["asset"] = asset
    frame.attrs["source"] = cfg.get("provider")
    frame.attrs["quote_currency"] = cfg.get("quote_currency")
    frame.attrs["calendar"] = cfg.get("calendar")
    frame.attrs["snapshot_path"] = str(snapshot)
    return frame
