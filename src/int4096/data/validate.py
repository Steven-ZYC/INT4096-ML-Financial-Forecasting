"""Data quality validation.

Produces a structured report. Never mutates or repairs the input frame: every
issue is surfaced so that a human (or the data steward) decides what to do and
records the decision. Silent repair is how datasets become unexplainable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DataQualityReport:
    """Structured result of validating one asset's canonical frame."""

    asset: str
    rows: int
    first_ts: str
    last_ts: str
    checks: dict[str, Any] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset": self.asset,
            "rows": self.rows,
            "first_ts": self.first_ts,
            "last_ts": self.last_ts,
            "passed": self.passed,
            "checks": self.checks,
            "issues": list(self.issues),
        }

    def summary(self) -> str:
        head = (
            f"{self.asset}: {self.rows} rows, {self.first_ts} .. {self.last_ts}, "
            f"{'PASS' if self.passed else 'ISSUES'}"
        )
        return head + "".join(f"\n  - {i}" for i in self.issues)


def validate_frame(frame, asset: str | None = None, price_tolerance: float = 1e-9) -> DataQualityReport:
    """Run schema and sanity checks on a canonical frame.

    ``price_tolerance`` absorbs floating-point noise in provider values.
    """
    import numpy as np

    asset = asset or frame.attrs.get("asset", "UNKNOWN")
    report = DataQualityReport(
        asset=asset,
        rows=int(len(frame)),
        first_ts=str(frame.index[0].date()) if len(frame) else "n/a",
        last_ts=str(frame.index[-1].date()) if len(frame) else "n/a",
    )

    # -- structural ----------------------------------------------------
    if len(frame) == 0:
        report.issues.append("empty frame")
        return report

    if frame.index.name != "ts":
        report.issues.append(f"index name is {frame.index.name!r}, expected 'ts'")
    if str(frame.index.tz) != "UTC":
        report.issues.append(f"index tz is {frame.index.tz}, expected UTC")
    if not frame.index.is_monotonic_increasing:
        report.issues.append("index is not strictly increasing")
    if frame.index.has_duplicates:
        report.issues.append("index has duplicate timestamps")

    required = {"open", "high", "low", "close", "volume", "adj_close"}
    missing = required - set(frame.columns)
    if missing:
        report.issues.append(f"missing columns: {sorted(missing)}")
        return report
    extra = set(frame.columns) - required
    if extra:
        report.issues.append(f"unexpected extra columns: {sorted(extra)}")

    # -- value sanity --------------------------------------------------
    ohlc = ["open", "high", "low", "close"]
    non_positive = {c: int((frame[c] <= 0).sum()) for c in ohlc}
    report.checks["non_positive_prices"] = non_positive
    for col, count in non_positive.items():
        if count:
            report.issues.append(f"{col}: {count} non-positive values")

    bad_range = int((frame["high"] + price_tolerance < frame["low"]).sum())
    report.checks["high_below_low"] = bad_range
    if bad_range:
        report.issues.append(f"{bad_range} rows with high < low")

    outside = int(
        (
            (frame["close"] > frame["high"] + price_tolerance)
            | (frame["close"] < frame["low"] - price_tolerance)
        ).sum()
    )
    report.checks["close_outside_high_low"] = outside
    if outside:
        report.issues.append(f"{outside} rows with close outside [low, high]")

    neg_volume = int((frame["volume"] < 0).sum())
    zero_volume = int((frame["volume"] == 0).sum())
    report.checks["negative_volume"] = neg_volume
    report.checks["zero_volume"] = zero_volume
    report.checks["zero_volume_pct"] = round(100.0 * zero_volume / len(frame), 4)
    if neg_volume:
        report.issues.append(f"{neg_volume} rows with negative volume")

    # -- missingness ---------------------------------------------------
    missing_counts = {c: int(frame[c].isna().sum()) for c in required}
    report.checks["missing_values"] = missing_counts
    core_missing = {c: n for c, n in missing_counts.items() if c != "adj_close" and n}
    if core_missing:
        report.issues.append(f"missing core values: {core_missing}")

    has_adj = frame["adj_close"].notna().any()
    report.checks["has_adjusted_close"] = bool(has_adj)
    if has_adj:
        differing = int((~np.isclose(frame["close"], frame["adj_close"], rtol=0, atol=1e-9)).sum())
        report.checks["adj_close_differs_from_close"] = differing
        report.checks["adj_close_differs_pct"] = round(100.0 * differing / len(frame), 4)

    # -- calendar gaps (reported, not repaired) ------------------------
    gaps = frame.index.to_series().diff().dropna()
    if len(gaps):
        max_gap_days = float(gaps.dt.total_seconds().max() / 86400.0)
        report.checks["max_gap_days"] = round(max_gap_days, 2)
        # AAPL legitimately jumps over weekends and holidays; BTC should be daily.
        if asset == "BTC" and max_gap_days > 2.0:
            report.issues.append(
                f"BTC has a {max_gap_days:.1f}-day gap; a 24/7 series should not"
            )

    # -- extreme daily moves (reported as context, not an error) -------
    returns = frame["close"].pct_change()
    report.checks["max_abs_daily_return"] = (
        round(float(returns.abs().max()), 6) if returns.notna().any() else None
    )
    report.checks["n_days_over_20pct_move"] = int((returns.abs() > 0.20).sum())

    return report
