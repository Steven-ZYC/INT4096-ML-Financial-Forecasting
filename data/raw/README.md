# Immutable Data Snapshots

Each `<asset>_daily.json` is a **normalized** record list (ascending by date) with
columns `date, open, high, low, close, volume, adj_close`.

Each `<asset>_daily.manifest.json` records the SHA-256 of the exact bytes, the
provider, the row count, the first/last observation and the true download time.

## Rules

1. **Never edit a snapshot in place.** A refresh creates a new file and a new
   manifest; the run registry preserves which hash produced which number.
2. Every experiment verifies the hash before running and aborts on mismatch.
3. `*_raw_provider.json` (gitignored) holds the untouched provider payload used to
   build the normalized snapshot, kept locally for provenance review.

## Regenerate

```bash
PYTHONPATH=src python -m int4096.data.snapshot --asset AAPL   # refuses to overwrite
PYTHONPATH=src python -m int4096.data.cards                   # rebuild dataset cards
```
