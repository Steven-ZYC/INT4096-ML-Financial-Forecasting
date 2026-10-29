"""Provider adapters: fetch raw payloads and normalise to canonical records.

Each adapter returns ``(records, metadata)`` where ``records`` is a list of
plain dicts in ascending timestamp order and ``metadata`` records provenance.

Adapters perform **no** cleaning beyond type coercion and ordering. Anything
that changes values is the job of ``validate`` and the feature layer, so that
the transformation is visible and testable.
"""

from __future__ import annotations

import datetime as dt
import json
import urllib.request
from typing import Any

USER_AGENT = "INT4096-coursework/0.1 (educational; non-commercial)"

# AAPL comes from a public JSON history endpoint. The ``a`` field is the
# split/dividend adjusted close; ``c`` is the raw close.
_AAPL_URL = "https://stockanalysis.com/api/symbol/s/aapl/history?range={range}&period=Daily"
_BTC_URL = "https://api.binance.com/api/v3/klines"
_BTC_START = "2021-10-28T00:00:00+00:00"


def _get_json(url: str, timeout: int = 60) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8")), len(raw)


def fetch_aapl(range_: str = "10Y", timeout: int = 60) -> tuple[list[dict], dict]:
    """Fetch AAPL daily history.

    Returns records in **ascending** date order. The provider returns them
    descending, which we reverse here — reversing a time series is safe and
    explicit, unlike reindexing or filling.
    """
    url = _AAPL_URL.format(range=range_)
    payload, nbytes = _get_json(url, timeout=timeout)
    rows = payload.get("data")
    if not rows:
        raise RuntimeError(
            f"AAPL provider returned no rows (status={payload.get('status')!r}). "
            "The endpoint may have changed or be rate limiting."
        )

    records: list[dict] = []
    for row in rows:
        records.append(
            {
                "date": str(row["t"]),
                "open": float(row["o"]),
                "high": float(row["h"]),
                "low": float(row["l"]),
                "close": float(row["c"]),
                "volume": float(row["v"]),
                "adj_close": float(row["a"]) if row.get("a") is not None else None,
            }
        )
    records.sort(key=lambda r: r["date"])

    metadata = {
        "provider": "stockanalysis.com",
        "url": url,
        "symbol": "AAPL",
        "quote_currency": "USD",
        "calendar": "us_exchange_sessions",
        "row_count": len(records),
        "payload_bytes": nbytes,
    }
    return records, metadata


def fetch_btc(start: str = _BTC_START, timeout: int = 60) -> tuple[list[dict], dict]:
    """Fetch BTCUSDT daily klines from Binance, paginating to the present.

    Binance returns ``[open_time_ms, o, h, l, c, v, close_time_ms, ...]``.
    Times are UTC by definition for this endpoint.
    """
    start_dt = dt.datetime.fromisoformat(start)
    cursor = int(start_dt.timestamp() * 1000)
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)

    records: list[dict] = []
    pages = 0
    while True:
        url = f"{_BTC_URL}?symbol=BTCUSDT&interval=1d&startTime={cursor}&limit=1000"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            page = json.loads(response.read().decode("utf-8"))
        pages += 1
        if not page:
            break
        for k in page:
            open_time = dt.datetime.fromtimestamp(k[0] / 1000, dt.timezone.utc)
            records.append(
                {
                    "date": open_time.strftime("%Y-%m-%d"),
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4]),
                    "volume": float(k[5]),
                    "adj_close": None,  # no corporate actions for a crypto pair
                }
            )
        next_cursor = int(page[-1][0]) + 86_400_000
        if len(page) < 1000 or next_cursor > now_ms:
            break
        cursor = next_cursor

    if not records:
        raise RuntimeError("Binance returned no klines for BTCUSDT.")

    metadata = {
        "provider": "binance",
        "url": f"{_BTC_URL}?symbol=BTCUSDT&interval=1d",
        "symbol": "BTCUSDT",
        "quote_currency": "USDT",
        "calendar": "24_7_utc",
        "row_count": len(records),
        "pages": pages,
        "caveat": (
            "USDT is not exactly USD and Binance is a single venue; this is a "
            "venue-specific price series, not a global index."
        ),
    }
    return records, metadata


FETCHERS = {"AAPL": fetch_aapl, "BTC": fetch_btc}
