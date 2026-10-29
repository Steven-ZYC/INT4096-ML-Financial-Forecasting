"""Write a reproducibility manifest for the submission artifacts.

Records SHA-256 digests of the immutable data, the compiled report and the run
registry, plus the current commit, so a reader can prove that the PDF they are
holding was built from these exact inputs.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TRACKED = [
    "data/raw/aapl_daily.json",
    "data/raw/btc_daily.json",
    "data/raw/aapl_daily.manifest.json",
    "data/raw/btc_daily.manifest.json",
    "artifacts/experiments/registry.jsonl",
    "configs/research_protocol.yaml",
    "docs/research/protocol.md",
    "notebooks/INT4096_Final_Colab.ipynb",
    "reports/final/INT4096_Final_Report.pdf",
    "reports/word_count.txt",
    "slides/final/INT4096_Presentation.pdf",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    ).stdout.strip()


def main() -> int:
    entries = {}
    missing = []
    for relative in TRACKED:
        path = REPO_ROOT / relative
        if not path.exists():
            missing.append(relative)
            continue
        entries[relative] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    manifest = {
        "project": "INT4096 machine-learning coursework",
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git("rev-parse", "HEAD"),
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "protocol_version": "v1.1-delta-target",
        "run_count": len(list((REPO_ROOT / "artifacts" / "experiments").glob("*/manifest.json"))),
        "artifacts": entries,
        "missing": missing,
        "note": (
            "Hashes cover the exact bytes used. Re-run `bash scripts/reproduce.sh` "
            "and `bash reports/latex/build.sh` to regenerate; run manifests record "
            "the commit, data digest and protocol version behind every number."
        ),
    }

    out = REPO_ROOT / "docs" / "quality" / "reproducibility_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(out.relative_to(REPO_ROOT))
    if missing:
        print("missing (not hashed):", missing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
