# Linear baseline (`linear_baseline`)

**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.

Ridge regression with a small L2 penalty: the simplest learned model.

Implementation: `int4096.models.ridge.LinearBaseline` · family: linear

## Search grid (frozen in the protocol before any result)

| Hyperparameter | Values |
|---|---|
| `alpha` | 0.1, 1, 10 |

Tuning: random search, 10 trials, at most 90.0 s per run, seed 42, scored by mean MAE over 5 expanding-window folds inside the training block (see `data/splits/`). The validation block is never used for tuning.

## Runs

| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | P0 | alpha=10 | 1.986 | 2.899 | 4.356 | 0.9556 | +0.24% | 58.6% |
| AAPL | P2 | alpha=10 | 2.012 | 2.920 | 4.366 | 0.9554 | -0.50% | 50.4% |
| BTC | P0 | alpha=10 | 759.265 | 1600.205 | 2205.349 | 0.9614 | +0.26% | 51.1% |
| BTC | P2 | alpha=10 | 779.545 | 1603.587 | 2211.239 | 0.9612 | +0.05% | 53.1% |

P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "tomorrow equals today". All results are on the validation block; the test block is sealed.

## Every tuning trial

### AAPL P0 — `2026-10-29T145503Z_aapl_linear_baseline_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.1 | 2.002 | 0.0257 | ok |
| 1 | alpha=10 | 1.986 | 0.0143 | ok |
| 2 | alpha=1 | 1.994 | 0.0143 | ok |
| 3 | alpha=1 | 1.994 | 0.0149 | ok |
| 4 | alpha=1 | 1.994 | 0.014 | ok |
| 5 | alpha=10 | 1.986 | 0.016 | ok |
| 6 | alpha=0.1 | 2.002 | 0.0154 | ok |
| 7 | alpha=10 | 1.986 | 0.0151 | ok |
| 8 | alpha=0.1 | 2.002 | 0.0141 | ok |
| 9 | alpha=0.1 | 2.002 | 0.0143 | ok |

### AAPL P2 — `2026-10-29T145504Z_aapl_linear_baseline_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.1 | 2.019 | 0.0257 | ok |
| 1 | alpha=10 | 2.012 | 0.0164 | ok |
| 2 | alpha=1 | 2.019 | 0.0198 | ok |
| 3 | alpha=1 | 2.019 | 0.0187 | ok |
| 4 | alpha=1 | 2.019 | 0.0168 | ok |
| 5 | alpha=10 | 2.012 | 0.0168 | ok |
| 6 | alpha=0.1 | 2.019 | 0.0165 | ok |
| 7 | alpha=10 | 2.012 | 0.0198 | ok |
| 8 | alpha=0.1 | 2.019 | 0.0182 | ok |
| 9 | alpha=0.1 | 2.019 | 0.0185 | ok |

### BTC P0 — `2026-10-29T145539Z_btc_linear_baseline_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.1 | 766.973 | 0.0288 | ok |
| 1 | alpha=10 | 759.265 | 0.0176 | ok |
| 2 | alpha=1 | 763.640 | 0.0167 | ok |
| 3 | alpha=1 | 763.640 | 0.0174 | ok |
| 4 | alpha=1 | 763.640 | 0.0179 | ok |
| 5 | alpha=10 | 759.265 | 0.0161 | ok |
| 6 | alpha=0.1 | 766.973 | 0.0162 | ok |
| 7 | alpha=10 | 759.265 | 0.0162 | ok |
| 8 | alpha=0.1 | 766.973 | 0.0171 | ok |
| 9 | alpha=0.1 | 766.973 | 0.0193 | ok |

### BTC P2 — `2026-10-29T145540Z_btc_linear_baseline_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.1 | 781.090 | 0.0278 | ok |
| 1 | alpha=10 | 779.545 | 0.0211 | ok |
| 2 | alpha=1 | 780.937 | 0.0172 | ok |
| 3 | alpha=1 | 780.937 | 0.017 | ok |
| 4 | alpha=1 | 780.937 | 0.019 | ok |
| 5 | alpha=10 | 779.545 | 0.0224 | ok |
| 6 | alpha=0.1 | 781.090 | 0.0203 | ok |
| 7 | alpha=10 | 779.545 | 0.0182 | ok |
| 8 | alpha=0.1 | 781.090 | 0.0175 | ok |
| 9 | alpha=0.1 | 781.090 | 0.0175 | ok |

## Files in each run folder

`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · `metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · `environment.json` (package versions).
