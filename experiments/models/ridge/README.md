# Ridge regression (`ridge`)

**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.

Linear model with an L2 penalty searched over a wide range.

Implementation: `int4096.models.ridge.build_ridge` · family: linear

## Search grid (frozen in the protocol before any result)

| Hyperparameter | Values |
|---|---|
| `alpha` | 0.01, 0.1, 1, 10, 100, 1000 |

Tuning: random search, 10 trials, at most 90.0 s per run, seed 42, scored by mean MAE over 5 expanding-window folds inside the training block (see `data/splits/`). The validation block is never used for tuning.

## Runs

| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | P0 | alpha=1000 | 1.977 | 2.898 | 4.359 | 0.9555 | +0.25% | 55.7% |
| AAPL | P2 | alpha=1000 | 1.983 | 2.897 | 4.357 | 0.9556 | +0.29% | 56.6% |
| BTC | P0 | alpha=1000 | 756.373 | 1601.874 | 2205.475 | 0.9614 | +0.15% | 52.2% |
| BTC | P2 | alpha=1000 | 761.150 | 1602.388 | 2205.961 | 0.9614 | +0.12% | 51.1% |

P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "tomorrow equals today". All results are on the validation block; the test block is sealed.

## Every tuning trial

### AAPL P0 — `2026-10-29T145505Z_aapl_ridge_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.01 | 2.012 | 0.0247 | ok |
| 1 | alpha=100 | 1.980 | 0.0165 | ok |
| 2 | alpha=10 | 1.986 | 0.015 | ok |
| 3 | alpha=1 | 1.994 | 0.0185 | ok |
| 4 | alpha=1 | 1.994 | 0.0165 | ok |
| 5 | alpha=1000 | 1.977 | 0.017 | ok |
| 6 | alpha=0.01 | 2.012 | 0.0153 | ok |
| 7 | alpha=100 | 1.980 | 0.015 | ok |
| 8 | alpha=0.1 | 2.002 | 0.0166 | ok |
| 9 | alpha=0.01 | 2.012 | 0.0153 | ok |

### AAPL P2 — `2026-10-29T145506Z_aapl_ridge_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.01 | 2.020 | 0.028 | ok |
| 1 | alpha=100 | 1.997 | 0.0194 | ok |
| 2 | alpha=10 | 2.012 | 0.0176 | ok |
| 3 | alpha=1 | 2.019 | 0.0165 | ok |
| 4 | alpha=1 | 2.019 | 0.0168 | ok |
| 5 | alpha=1000 | 1.983 | 0.0194 | ok |
| 6 | alpha=0.01 | 2.020 | 0.0181 | ok |
| 7 | alpha=100 | 1.997 | 0.0194 | ok |
| 8 | alpha=0.1 | 2.019 | 0.0176 | ok |
| 9 | alpha=0.01 | 2.020 | 0.0195 | ok |

### BTC P0 — `2026-10-29T145542Z_btc_ridge_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.01 | 771.808 | 0.0293 | ok |
| 1 | alpha=100 | 756.785 | 0.0158 | ok |
| 2 | alpha=10 | 759.265 | 0.0156 | ok |
| 3 | alpha=1 | 763.640 | 0.0152 | ok |
| 4 | alpha=1 | 763.640 | 0.0149 | ok |
| 5 | alpha=1000 | 756.373 | 0.0171 | ok |
| 6 | alpha=0.01 | 771.808 | 0.0174 | ok |
| 7 | alpha=100 | 756.785 | 0.0171 | ok |
| 8 | alpha=0.1 | 766.973 | 0.0174 | ok |
| 9 | alpha=0.01 | 771.808 | 0.0181 | ok |

### BTC P2 — `2026-10-29T145543Z_btc_ridge_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | alpha=0.01 | 781.106 | 0.0275 | ok |
| 1 | alpha=100 | 772.045 | 0.0213 | ok |
| 2 | alpha=10 | 779.545 | 0.0177 | ok |
| 3 | alpha=1 | 780.937 | 0.0176 | ok |
| 4 | alpha=1 | 780.937 | 0.018 | ok |
| 5 | alpha=1000 | 761.150 | 0.0199 | ok |
| 6 | alpha=0.01 | 781.106 | 0.0182 | ok |
| 7 | alpha=100 | 772.045 | 0.0177 | ok |
| 8 | alpha=0.1 | 781.090 | 0.017 | ok |
| 9 | alpha=0.01 | 781.106 | 0.0183 | ok |

## Files in each run folder

`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · `metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · `environment.json` (package versions).
