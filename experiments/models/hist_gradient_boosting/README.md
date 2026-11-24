# Histogram gradient boosting (`hist_gradient_boosting`)

**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.

Trees added one by one to fix the remaining error.

Implementation: `int4096.models.hist_gradient_boosting.build_hist_gradient_boosting` · family: boosting

## Search grid (frozen in the protocol before any result)

| Hyperparameter | Values |
|---|---|
| `learning_rate` | 0.01, 0.05, 0.1 |
| `max_iter` | 100, 300 |
| `max_depth` | None, 3, 5 |
| `min_samples_leaf` | 5, 20, 50 |

Tuning: random search, 10 trials, at most 90.0 s per run, seed 42, scored by mean MAE over 5 expanding-window folds inside the training block (see `data/splits/`). The validation block is never used for tuning.

## Runs

| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | P0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 1.992 | 2.898 | 4.356 | 0.9556 | +0.25% | 54.9% |
| AAPL | P2 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 1.992 | 2.898 | 4.356 | 0.9556 | +0.25% | 54.9% |
| BTC | P0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 757.500 | 1605.016 | 2204.911 | 0.9614 | -0.04% | 48.9% |
| BTC | P2 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 757.500 | 1605.016 | 2204.911 | 0.9614 | -0.04% | 48.9% |

P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "tomorrow equals today". All results are on the validation block; the test block is sealed.

## Every tuning trial

### AAPL P0 — `2026-10-29T145531Z_aapl_hist_gradient_boosting_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 1.992 | 0.3707 | ok |
| 1 | learning_rate=0.05, max_iter=300, max_depth=None, min_samples_leaf=50 | 2.039 | 0.2356 | ok |
| 2 | learning_rate=0.01, max_iter=100, max_depth=3, min_samples_leaf=50 | 2.001 | 0.3401 | ok |
| 3 | learning_rate=0.1, max_iter=300, max_depth=5, min_samples_leaf=50 | 2.053 | 0.1839 | ok |
| 4 | learning_rate=0.05, max_iter=100, max_depth=5, min_samples_leaf=20 | 2.062 | 0.2865 | ok |
| 5 | learning_rate=0.05, max_iter=100, max_depth=None, min_samples_leaf=50 | 2.039 | 0.2437 | ok |
| 6 | learning_rate=0.1, max_iter=300, max_depth=3, min_samples_leaf=50 | 2.050 | 0.1981 | ok |
| 7 | learning_rate=0.05, max_iter=100, max_depth=3, min_samples_leaf=5 | 2.058 | 0.2423 | ok |
| 8 | learning_rate=0.01, max_iter=300, max_depth=5, min_samples_leaf=5 | 1.998 | 0.4038 | ok |
| 9 | learning_rate=0.1, max_iter=300, max_depth=None, min_samples_leaf=20 | 2.141 | 0.3121 | ok |

### AAPL P2 — `2026-10-29T145535Z_aapl_hist_gradient_boosting_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 1.992 | 0.3898 | ok |
| 1 | learning_rate=0.05, max_iter=300, max_depth=None, min_samples_leaf=50 | 2.039 | 0.2256 | ok |
| 2 | learning_rate=0.01, max_iter=100, max_depth=3, min_samples_leaf=50 | 2.001 | 0.335 | ok |
| 3 | learning_rate=0.1, max_iter=300, max_depth=5, min_samples_leaf=50 | 2.053 | 0.2203 | ok |
| 4 | learning_rate=0.05, max_iter=100, max_depth=5, min_samples_leaf=20 | 2.062 | 0.2743 | ok |
| 5 | learning_rate=0.05, max_iter=100, max_depth=None, min_samples_leaf=50 | 2.039 | 0.2697 | ok |
| 6 | learning_rate=0.1, max_iter=300, max_depth=3, min_samples_leaf=50 | 2.050 | 0.1854 | ok |
| 7 | learning_rate=0.05, max_iter=100, max_depth=3, min_samples_leaf=5 | 2.058 | 0.239 | ok |
| 8 | learning_rate=0.01, max_iter=300, max_depth=5, min_samples_leaf=5 | 1.998 | 0.424 | ok |
| 9 | learning_rate=0.1, max_iter=300, max_depth=None, min_samples_leaf=20 | 2.141 | 0.3269 | ok |

### BTC P0 — `2026-10-29T145614Z_btc_hist_gradient_boosting_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 757.500 | 0.3287 | ok |
| 1 | learning_rate=0.05, max_iter=300, max_depth=None, min_samples_leaf=50 | 768.957 | 0.2113 | ok |
| 2 | learning_rate=0.01, max_iter=100, max_depth=3, min_samples_leaf=50 | 760.710 | 0.2401 | ok |
| 3 | learning_rate=0.1, max_iter=300, max_depth=5, min_samples_leaf=50 | 773.949 | 0.2162 | ok |
| 4 | learning_rate=0.05, max_iter=100, max_depth=5, min_samples_leaf=20 | 781.751 | 0.2034 | ok |
| 5 | learning_rate=0.05, max_iter=100, max_depth=None, min_samples_leaf=50 | 768.957 | 0.2126 | ok |
| 6 | learning_rate=0.1, max_iter=300, max_depth=3, min_samples_leaf=50 | 773.649 | 0.1784 | ok |
| 7 | learning_rate=0.05, max_iter=100, max_depth=3, min_samples_leaf=5 | 795.731 | 0.2416 | ok |
| 8 | learning_rate=0.01, max_iter=300, max_depth=5, min_samples_leaf=5 | 772.563 | 0.4488 | ok |
| 9 | learning_rate=0.1, max_iter=300, max_depth=None, min_samples_leaf=20 | 813.354 | 0.2634 | ok |

### BTC P2 — `2026-10-29T145617Z_btc_hist_gradient_boosting_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | learning_rate=0.01, max_iter=300, max_depth=3, min_samples_leaf=20 | 757.500 | 0.3145 | ok |
| 1 | learning_rate=0.05, max_iter=300, max_depth=None, min_samples_leaf=50 | 768.957 | 0.2353 | ok |
| 2 | learning_rate=0.01, max_iter=100, max_depth=3, min_samples_leaf=50 | 760.710 | 0.2267 | ok |
| 3 | learning_rate=0.1, max_iter=300, max_depth=5, min_samples_leaf=50 | 773.949 | 0.2218 | ok |
| 4 | learning_rate=0.05, max_iter=100, max_depth=5, min_samples_leaf=20 | 781.751 | 0.2305 | ok |
| 5 | learning_rate=0.05, max_iter=100, max_depth=None, min_samples_leaf=50 | 768.957 | 0.218 | ok |
| 6 | learning_rate=0.1, max_iter=300, max_depth=3, min_samples_leaf=50 | 773.649 | 0.1779 | ok |
| 7 | learning_rate=0.05, max_iter=100, max_depth=3, min_samples_leaf=5 | 795.731 | 0.2635 | ok |
| 8 | learning_rate=0.01, max_iter=300, max_depth=5, min_samples_leaf=5 | 772.563 | 0.4141 | ok |
| 9 | learning_rate=0.1, max_iter=300, max_depth=None, min_samples_leaf=20 | 813.354 | 0.3076 | ok |

## Files in each run folder

`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · `metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · `environment.json` (package versions).
