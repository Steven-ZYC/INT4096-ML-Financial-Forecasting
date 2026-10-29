"""Data layer: ingestion, immutable snapshots, validation and loading.

Design rules enforced here
--------------------------
1. Raw provider bytes are never edited. A snapshot is written once, with a
   SHA256 manifest sidecar.
2. The loader produces a *canonical* frame with an explicit UTC index and a
   fixed column set, for both assets. Downstream code never sees a provider
   schema.
3. Validation reports problems; it does not silently repair them.
4. Tests never touch the network.
"""

from .load import CANONICAL_COLUMNS, load_snapshot
from .providers import fetch_aapl, fetch_btc
from .snapshot import write_snapshot
from .validate import DataQualityReport, validate_frame

__all__ = [
    "CANONICAL_COLUMNS",
    "DataQualityReport",
    "fetch_aapl",
    "fetch_btc",
    "load_snapshot",
    "validate_frame",
    "write_snapshot",
]
