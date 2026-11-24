# Data

| Folder | What is in it | How it is made |
|---|---|---|
| [`raw/`](raw/README.md) | The two source snapshots (AAPL from StockAnalysis, BTC/USDT from Binance) and their SHA-256 manifests | Downloaded once by `python -m int4096.data.snapshot`; never edited |
| [`cards/`](cards/) | One dataset card per asset: provenance, coverage, statistics, quality checks | `python -m int4096.data.cards` |
| [`splits/`](splits/README.md) | The chronological train / validation / test boundaries, the purged rows and the five tuning folds, per asset | `python scripts/export_splits.py` |

Download links (as called by `src/int4096/data/providers.py`):

- AAPL: <https://stockanalysis.com/api/symbol/s/aapl/history?range=10Y&period=Daily>
- BTC: <https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d> (paginated from 2021-10-28)

The ten features are not stored: they are rebuilt from `raw/` every run by
`src/int4096/features/build.py` (definitions in `docs/research/feature_dictionary.md`).
