"""Protocol configuration loading.

The frozen research protocol lives in ``configs/research_protocol.yaml``. This
module is the single access point so that no experiment code hard-codes a split
boundary, a feature list, or a tuning budget.

Every run records ``protocol_version`` from here in its manifest. A silent
protocol change is therefore detectable by comparing manifests.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROTOCOL = REPO_ROOT / "configs" / "research_protocol.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise RuntimeError(
            "PyYAML is required to load the research protocol. "
            "Install dependencies with: pip install -r requirements.txt"
        ) from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Protocol file {path} did not parse to a mapping.")
    return data


@dataclass(frozen=True)
class Protocol:
    """Immutable view of the frozen protocol.

    Frozen so that an experiment cannot mutate the protocol mid-run.
    """

    raw: dict[str, Any] = field(repr=False)
    source_path: Path = field(repr=False)

    # -- identity ------------------------------------------------------
    @property
    def version(self) -> str:
        return str(self.raw["protocol_version"])

    @property
    def target(self) -> str:
        return str(self.raw["prediction_target"])

    @property
    def label_field(self) -> str:
        return str(self.raw["label_field"])

    @property
    def label_mode(self) -> str:
        """How models are trained: 'level' or 'delta' (see protocol D8)."""
        return str(self.raw.get("label_mode", "level"))

    # -- assets --------------------------------------------------------
    @property
    def assets(self) -> dict[str, Any]:
        return dict(self.raw["assets"])

    def asset(self, name: str) -> dict[str, Any]:
        try:
            return dict(self.raw["assets"][name])
        except KeyError as exc:
            raise KeyError(
                f"Unknown asset {name!r}; known assets: {sorted(self.raw['assets'])}"
            ) from exc

    # -- features ------------------------------------------------------
    @property
    def lookback(self) -> int:
        return int(self.raw["features"]["lookback"])

    @property
    def min_periods(self) -> int | None:
        """``None`` means "require a full window"; an int means a fixed minimum.

        A full window is the default because a partially-filled ``vol_30`` is not
        a 30-observation volatility, and silently reporting it as one would make
        the feature dictionary inaccurate.
        """
        value = self.raw["features"].get("min_periods", "window")
        if value in ("window", None):
            return None
        return int(value)

    @property
    def purge_gap(self) -> int:
        """Boundary rows purged so no label crosses a split (audit LEAK-001)."""
        return int(self.raw["splits"].get("purge_gap", 1))

    @property
    def feature_list(self) -> list[str]:
        return list(self.raw["features"]["list"])

    @property
    def reduced_feature_list(self) -> list[str]:
        return list(self.raw["features"]["reduced_list"])

    # -- splits --------------------------------------------------------
    @property
    def train_fraction(self) -> float:
        return float(self.raw["splits"]["train_fraction"])

    @property
    def validation_fraction(self) -> float:
        return float(self.raw["splits"]["validation_fraction"])

    @property
    def test_fraction(self) -> float:
        return float(self.raw["splits"]["test_fraction"])

    @property
    def cv(self) -> dict[str, Any]:
        return dict(self.raw["cv"])

    # -- preprocessing -------------------------------------------------
    @property
    def variants(self) -> dict[str, Any]:
        return dict(self.raw["preprocessing_variants"])

    def variant(self, name: str) -> dict[str, Any]:
        try:
            return dict(self.raw["preprocessing_variants"][name])
        except KeyError as exc:
            raise KeyError(
                f"Unknown preprocessing variant {name!r}; "
                f"known variants: {sorted(self.raw['preprocessing_variants'])}"
            ) from exc

    # -- models --------------------------------------------------------
    @property
    def models(self) -> dict[str, Any]:
        return dict(self.raw["models"])

    def model(self, name: str) -> dict[str, Any]:
        try:
            return dict(self.raw["models"][name])
        except KeyError as exc:
            raise KeyError(
                f"Unknown model {name!r}; known models: {sorted(self.raw['models'])}"
            ) from exc

    @property
    def tuning(self) -> dict[str, Any]:
        return dict(self.raw["tuning"])

    # -- provenance ----------------------------------------------------
    def fingerprint(self) -> str:
        """SHA256 of the canonical JSON form of the protocol.

        Recorded in every run manifest so that two runs can be proven to share
        (or not share) the same protocol.
        """
        canonical = json.dumps(self.raw, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_protocol(path: str | Path | None = None) -> Protocol:
    """Load and freeze the research protocol."""
    resolved = Path(path) if path is not None else DEFAULT_PROTOCOL
    if not resolved.is_absolute():
        resolved = (REPO_ROOT / resolved).resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Protocol file not found: {resolved}")
    return Protocol(raw=_load_yaml(resolved), source_path=resolved)
