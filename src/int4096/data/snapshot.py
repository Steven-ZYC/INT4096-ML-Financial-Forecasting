"""Snapshot writing: immutable raw data + checksum manifest.

A snapshot is written **once**. Refreshing the data creates a new file with a
new date-suffixed name; it never overwrites an existing snapshot. This is what
makes a run's ``source_snapshot_sha256`` meaningful months later.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from ..config import REPO_ROOT, load_protocol
from .providers import FETCHERS


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_snapshot(
    asset: str,
    out_dir: str | Path | None = None,
    force: bool = False,
    protocol_path: str | Path | None = None,
) -> dict[str, Any]:
    """Fetch ``asset`` and write an immutable snapshot plus manifest.

    Refuses to overwrite unless ``force=True``. Returns the manifest.
    """
    protocol = load_protocol(protocol_path)
    asset_cfg = protocol.asset(asset)
    fetch = FETCHERS[asset]
    records, meta = fetch()

    out = Path(out_dir) if out_dir is not None else REPO_ROOT / "data" / "raw"
    out.mkdir(parents=True, exist_ok=True)
    target = out / Path(asset_cfg["snapshot_file"]).name

    if target.exists() and not force:
        raise FileExistsError(
            f"Refusing to overwrite immutable snapshot {target}. "
            "Pass force=True only after recording why history must be refreshed "
            "in docs/research/decision_log.md."
        )

    payload = json.dumps(records, separators=(",", ":")).encode("utf-8")
    target.write_bytes(payload)

    manifest = {
        "asset": asset,
        "snapshot_file": str(target.relative_to(REPO_ROOT))
        if target.is_relative_to(REPO_ROOT)
        else str(target),
        "sha256": sha256_bytes(payload),
        "bytes": len(payload),
        "downloaded_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "row_count": len(records),
        "first_date": records[0]["date"],
        "last_date": records[-1]["date"],
        "source": meta,
        "protocol_version": protocol.version,
    }
    manifest_path = target.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def adopt_snapshot(
    asset: str,
    path: str | Path,
    downloaded_utc: str,
    out_dir: str | Path | None = None,
    protocol_path: str | Path | None = None,
) -> dict[str, Any]:
    """Record a manifest for a snapshot that was already fetched.

    Used when the raw bytes were obtained by an earlier download and must not be
    re-fetched (for example, to keep a stable snapshot after the upstream
    provider changed history). The file content is left byte-identical; only the
    provenance sidecar is written.

    ``downloaded_utc`` must be the time the bytes were *actually* obtained, not
    the time this manifest was written.
    """
    protocol = load_protocol(protocol_path)
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Cannot adopt missing snapshot: {source}")

    records = json.loads(source.read_text(encoding="utf-8"))
    if not records:
        raise ValueError(f"Snapshot {source} is empty.")

    payload = source.read_bytes()
    target = source
    if out_dir is not None:
        destination = Path(out_dir) / source.name
        if destination.resolve() != source.resolve():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        target = destination

    def _first_date(record: Any) -> Any:
        if isinstance(record, dict):
            return record.get("date")
        if isinstance(record, list):
            return record[0]
        return None

    configured = protocol.asset(asset)
    manifest = {
        "asset": asset,
        "snapshot_file": (
            str(target.relative_to(REPO_ROOT))
            if target.is_relative_to(REPO_ROOT)
            else str(target)
        ),
        "sha256": sha256_bytes(payload),
        "bytes": len(payload),
        "downloaded_utc": downloaded_utc,
        "manifest_written_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "row_count": len(records),
        "first_date": _first_date(records[0]),
        "last_date": _first_date(records[-1]),
        "adopted": True,
        "source": {
            "provider": configured.get("provider"),
            "endpoint": configured.get("endpoint"),
            "symbol": configured.get("symbol"),
            "quote_currency": configured.get("quote_currency"),
            "calendar": configured.get("calendar"),
        },
        "protocol_version": protocol.version,
    }
    manifest_path = target.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Write an immutable data snapshot.")
    parser.add_argument("--asset", required=True, choices=sorted(FETCHERS))
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--protocol", default=None)
    parser.add_argument(
        "--adopt",
        default=None,
        help="Write a manifest for an existing snapshot file instead of downloading.",
    )
    parser.add_argument(
        "--downloaded-utc",
        default=None,
        help="Actual UTC download time of the adopted snapshot (required with --adopt).",
    )
    args = parser.parse_args(argv)

    if args.adopt:
        if not args.downloaded_utc:
            parser.error("--adopt requires --downloaded-utc to record true provenance")
        manifest = adopt_snapshot(
            args.asset,
            args.adopt,
            args.downloaded_utc,
            out_dir=args.out_dir,
            protocol_path=args.protocol,
        )
        print(json.dumps(manifest, indent=2))
        return 0

    manifest = write_snapshot(
        args.asset, out_dir=args.out_dir, force=args.force, protocol_path=args.protocol
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
