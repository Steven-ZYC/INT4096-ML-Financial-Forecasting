# Random forest (`random_forest`)

**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.

Average of many independent trees; scale-invariant control.

Implementation: `int4096.models.random_forest.build_random_forest` · family: bagging

## Search grid (frozen in the protocol before any result)

| Hyperparameter | Values |
|---|---|
| `n_estimators` | 100, 200 |
| `max_depth` | None, 4, 8, 16 |
| `min_samples_leaf` | 1, 5, 20 |

Tuning: random search, 10 trials, at most 90.0 s per run, seed 42, scored by mean MAE over 5 expanding-window folds inside the training block (see `data/splits/`). The validation block is never used for tuning.

## Runs

| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | P0 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 2.023 | 2.928 | 4.371 | 0.9553 | -0.78% | 52.0% |
| AAPL | P2 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 2.024 | 2.928 | 4.371 | 0.9553 | -0.78% | 52.0% |
| BTC | P0 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 770.762 | 1603.373 | 2208.038 | 0.9613 | +0.06% | 51.4% |
| BTC | P2 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 770.762 | 1603.373 | 2208.038 | 0.9613 | +0.06% | 51.4% |

P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "tomorrow equals today". All results are on the validation block; the test block is sealed.

## Every tuning trial

### AAPL P0 — `2026-10-29T145511Z_aapl_random_forest_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | n_estimators=100, max_depth=16, min_samples_leaf=5 | 2.068 | 0.6963 | ok |
| 1 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 2.024 | 0.4656 | ok |
| 2 | n_estimators=100, max_depth=8, min_samples_leaf=1 | 2.190 | 0.6705 | ok |
| 3 | n_estimators=100, max_depth=8, min_samples_leaf=20 | 2.024 | 0.5065 | ok |
| 4 | n_estimators=200, max_depth=16, min_samples_leaf=20 | 2.024 | 1.0473 | ok |
| 5 | n_estimators=200, max_depth=8, min_samples_leaf=1 | 2.182 | 1.3473 | ok |
| 6 | n_estimators=200, max_depth=4, min_samples_leaf=5 | 2.049 | 0.9449 | ok |
| 7 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 2.023 | 0.5198 | ok |
| 8 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 2.076 | 1.2233 | ok |
| 9 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 2.076 | 1.217 | ok |

### AAPL P2 — `2026-10-29T145521Z_aapl_random_forest_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | n_estimators=100, max_depth=16, min_samples_leaf=5 | 2.068 | 0.7093 | ok |
| 1 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 2.024 | 0.458 | ok |
| 2 | n_estimators=100, max_depth=8, min_samples_leaf=1 | 2.190 | 0.7343 | ok |
| 3 | n_estimators=100, max_depth=8, min_samples_leaf=20 | 2.024 | 0.5434 | ok |
| 4 | n_estimators=200, max_depth=16, min_samples_leaf=20 | 2.024 | 1.0761 | ok |
| 5 | n_estimators=200, max_depth=8, min_samples_leaf=1 | 2.181 | 1.3842 | ok |
| 6 | n_estimators=200, max_depth=4, min_samples_leaf=5 | 2.049 | 0.9576 | ok |
| 7 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 2.024 | 0.5178 | ok |
| 8 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 2.076 | 1.2172 | ok |
| 9 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 2.076 | 1.2179 | ok |

### BTC P0 — `2026-10-29T145548Z_btc_random_forest_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | n_estimators=100, max_depth=16, min_samples_leaf=5 | 809.144 | 0.9781 | ok |
| 1 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 770.762 | 0.5814 | ok |
| 2 | n_estimators=100, max_depth=8, min_samples_leaf=1 | 818.046 | 0.9014 | ok |
| 3 | n_estimators=100, max_depth=8, min_samples_leaf=20 | 773.298 | 0.6941 | ok |
| 4 | n_estimators=200, max_depth=16, min_samples_leaf=20 | 771.708 | 1.4103 | ok |
| 5 | n_estimators=200, max_depth=8, min_samples_leaf=1 | 815.362 | 1.9187 | ok |
| 6 | n_estimators=200, max_depth=4, min_samples_leaf=5 | 798.181 | 1.27 | ok |
| 7 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 773.172 | 0.6967 | ok |
| 8 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 812.430 | 1.6486 | ok |
| 9 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 812.430 | 1.676 | ok |

### BTC P2 — `2026-10-29T145601Z_btc_random_forest_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | n_estimators=100, max_depth=16, min_samples_leaf=5 | 809.092 | 0.964 | ok |
| 1 | n_estimators=100, max_depth=4, min_samples_leaf=20 | 770.762 | 0.583 | ok |
| 2 | n_estimators=100, max_depth=8, min_samples_leaf=1 | 817.925 | 0.8951 | ok |
| 3 | n_estimators=100, max_depth=8, min_samples_leaf=20 | 773.274 | 0.6809 | ok |
| 4 | n_estimators=200, max_depth=16, min_samples_leaf=20 | 771.691 | 1.3798 | ok |
| 5 | n_estimators=200, max_depth=8, min_samples_leaf=1 | 815.469 | 1.7776 | ok |
| 6 | n_estimators=200, max_depth=4, min_samples_leaf=5 | 798.157 | 1.2088 | ok |
| 7 | n_estimators=100, max_depth=None, min_samples_leaf=20 | 773.148 | 0.7011 | ok |
| 8 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 812.379 | 1.6534 | ok |
| 9 | n_estimators=200, max_depth=8, min_samples_leaf=5 | 812.379 | 1.6707 | ok |

## Files in each run folder

`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · `metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · `environment.json` (package versions).
