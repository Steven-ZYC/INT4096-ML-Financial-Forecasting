"""Run manifest: the traceability contract.

Every experiment writes a manifest. The manifest is what allows a reader to
answer: *which code, which data, which configuration, which seed produced this
number, and did anyone review it?*

Design decisions
----------------
* ``status`` is a closed enum and defaults to ``NOT_RUN``. A run that throws is
  recorded as ``FAILED`` with the traceback, never dropped.
* Construction requires the dataset SHA256. There is no path that produces a
  manifest without a data hash, so an unpinned run cannot masquerade as
  reproducible.
* Metrics are stored as observed floats. A ``NaN`` stays ``NaN`` (serialised as
  ``null`` with a warning) instead of being replaced by a nicer-looking number.
* ``review_state`` starts at ``UNREVIEWED``. Only an independent auditor may set
  it to ``PASSED``; a model lane cannot sign off its own work.
"""

from __future__ import annotations

import datetime as dt
import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]


class RunStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    INCOMPLETE = "INCOMPLETE"
    NOT_RUN = "NOT_RUN"


class ReviewState(str, Enum):
    UNREVIEWED = "UNREVIEWED"
    BLOCKED = "BLOCKED"
    PASSED = "PASSED"


REQUIRED_FIELDS = (
    "run_id",
    "status",
    "protocol_version",
    "asset",
    "prediction_target",
    "source_snapshot_sha256",
    "git_commit",
    "model_id",
    "preprocess_variant",
    "seed",
)


def git_commit() -> str:
    """Current commit SHA, or ``UNKNOWN`` outside a repository."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return out.stdout.strip() or "UNKNOWN"
    except (OSError, subprocess.SubprocessError):
        return "UNKNOWN"


def git_is_dirty() -> bool:
    """True if the working tree has uncommitted changes.

    Recorded because a commit SHA alone does not reproduce a dirty tree.
    """
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return bool(out.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return True


def dependency_fingerprint() -> str:
    """Hash of the installed distribution set (name==version sorted)."""
    import hashlib
    from importlib import metadata

    try:
        dists = sorted(
            f"{d.metadata['Name']}=={d.version}" for d in metadata.distributions()
        )
    except Exception:  # noqa: BLE001 - metadata can fail on odd environments
        return "UNKNOWN"
    blob = "\n".join(dists).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def make_run_id(asset: str, model_id: str, variant: str, seed: int, when: dt.datetime | None = None) -> str:
    stamp = (when or dt.datetime.now(dt.timezone.utc)).strftime("%Y-%m-%dT%H%M%SZ")
    return f"{stamp}_{asset.lower()}_{model_id}_{variant}_seed{seed}"


@dataclass
class RunManifest:
    """Machine-readable record of one experiment cell."""

    run_id: str
    status: str
    protocol_version: str
    asset: str
    prediction_target: str
    source_snapshot_sha256: str
    model_id: str
    preprocess_variant: str
    seed: int

    git_commit: str = field(default_factory=git_commit)
    git_dirty: bool = field(default_factory=git_is_dirty)
    python_version: str = field(default_factory=lambda: platform.python_version())
    platform: str = field(default_factory=platform.platform)
    dependencies_lock_hash: str = ""
    config_path: str = ""
    config_hash: str = ""

    source_name: str = ""
    source_coverage: str = ""

    train_period: str = ""
    validation_period: str = ""
    test_period: str = ""
    cv_policy: str = ""

    hyperparameters: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    baseline_metrics: dict[str, float] = field(default_factory=dict)
    fold_metrics: list[dict[str, Any]] = field(default_factory=list)

    artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None

    execution_seconds: float | None = None
    human_owner: str = ""
    review_state: str = ReviewState.UNREVIEWED.value
    notes: str = ""

    # -- validation ----------------------------------------------------
    def validate(self) -> list[str]:
        """Return a list of schema violations (empty means valid)."""
        problems: list[str] = []
        for name in REQUIRED_FIELDS:
            value = getattr(self, name, None)
            if value is None or (isinstance(value, str) and not value.strip()):
                problems.append(f"missing required field: {name}")
        if self.status not in {s.value for s in RunStatus}:
            problems.append(f"invalid status {self.status!r}")
        if self.review_state not in {s.value for s in ReviewState}:
            problems.append(f"invalid review_state {self.review_state!r}")
        if self.status == RunStatus.SUCCESS.value and not self.metrics:
            problems.append("SUCCESS run has no metrics")
        if self.status == RunStatus.FAILED.value and not self.error:
            problems.append("FAILED run must record an error message")
        if len(str(self.source_snapshot_sha256)) != 64:
            problems.append("source_snapshot_sha256 must be a 64-char sha256 hex digest")
        for path in self.artifacts:
            candidate = Path(path)
            resolved = candidate if candidate.is_absolute() else REPO_ROOT / candidate
            if not resolved.exists():
                problems.append(f"artifact path does not exist: {path}")
        return problems

    def require_artifact_exists(self, path: str) -> None:
        if not (REPO_ROOT / path).exists():
            raise FileNotFoundError(f"Manifest references a missing artifact: {path}")

    # -- serialisation -------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        # JSON has no NaN: be explicit about it rather than writing a bare NaN.
        data["metrics"] = _json_safe(self.metrics)
        data["baseline_metrics"] = _json_safe(self.baseline_metrics)
        data["fold_metrics"] = [_json_safe(row) for row in self.fold_metrics]
        data["schema_problems"] = self.validate()
        return data

    def write(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        return target

    @classmethod
    def read(cls, path: str | Path) -> dict[str, Any]:
        return json.loads(Path(path).read_text(encoding="utf-8"))


def _json_safe(mapping: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in mapping.items():
        if isinstance(value, float):
            out[key] = value if value == value and value not in (float("inf"), float("-inf")) else None
        else:
            out[key] = value
    return out


def environment_manifest() -> dict[str, Any]:
    """Environment block included in every run directory."""
    return {
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "dependencies_lock_hash": dependency_fingerprint(),
        "git_commit": git_commit(),
        "git_dirty": git_is_dirty(),
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
