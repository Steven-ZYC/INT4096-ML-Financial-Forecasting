# Support vector regression (RBF kernel) (`svr`)

**Generated** by `scripts/summarize_models.py` from the run files in this folder. Do not edit by hand.

Predicts from similarity to training examples; scale-sensitive.

Implementation: `int4096.models.svr.build_svr` · family: kernel

## Search grid (frozen in the protocol before any result)

| Hyperparameter | Values |
|---|---|
| `C` | 0.1, 1, 10, 100, 1000 |
| `epsilon` | 0.001, 0.01, 0.1 |
| `gamma` | scale, 0.001, 0.01, 0.1 |

Tuning: random search, 10 trials, at most 90.0 s per run, seed 42, scored by mean MAE over 5 expanding-window folds inside the training block (see `data/splits/`). The validation block is never used for tuning.

## Runs

| Asset | Setting | Chosen configuration | Tuning MAE (folds) | Val. MAE | Val. RMSE | Val. R² | Skill vs persistence | Direction acc. |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | P0 | C=0.1, epsilon=0.1, gamma=0.01 | 1.976 | 2.891 | 4.357 | 0.9556 | +0.51% | 55.7% |
| AAPL | P2 | C=0.1, epsilon=0.1, gamma=0.01 | 1.980 | 2.890 | 4.356 | 0.9556 | +0.52% | 55.3% |
| BTC | P0 | C=100, epsilon=0.01, gamma=0.001 | 752.607 | 1604.186 | 2206.369 | 0.9614 | +0.01% | 50.8% |
| BTC | P2 | C=10, epsilon=0.01, gamma=0.1 | 752.204 | 1603.131 | 2203.848 | 0.9614 | +0.08% | 50.8% |

P0 = raw features; P2 = standardised with training-block statistics. Skill = 1 − MAE / MAE of "tomorrow equals today". All results are on the validation block; the test block is sealed.

## Every tuning trial

### AAPL P0 — `2026-10-29T145508Z_aapl_svr_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | C=0.1, epsilon=0.1, gamma=0.01 | 1.976 | 0.0502 | ok |
| 1 | C=10, epsilon=0.01, gamma=0.1 | 2.014 | 0.0458 | ok |
| 2 | C=0.1, epsilon=0.1, gamma=scale | 1.986 | 0.0408 | ok |
| 3 | C=0.1, epsilon=0.01, gamma=0.1 | 1.985 | 0.0393 | ok |
| 4 | C=100, epsilon=0.1, gamma=0.01 | 2.005 | 0.0448 | ok |
| 5 | C=100, epsilon=0.01, gamma=scale | 2.084 | 0.0544 | ok |
| 6 | C=1000, epsilon=0.01, gamma=0.01 | 2.019 | 0.0517 | ok |
| 7 | C=1, epsilon=0.001, gamma=0.1 | 1.998 | 0.0419 | ok |
| 8 | C=100, epsilon=0.01, gamma=0.001 | 1.992 | 0.0385 | ok |
| 9 | C=1000, epsilon=0.01, gamma=0.001 | 1.992 | 0.0486 | ok |

### AAPL P2 — `2026-10-29T145509Z_aapl_svr_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | C=0.1, epsilon=0.1, gamma=0.01 | 1.980 | 0.051 | ok |
| 1 | C=10, epsilon=0.01, gamma=0.1 | 2.230 | 0.0612 | ok |
| 2 | C=0.1, epsilon=0.1, gamma=scale | 1.990 | 0.0404 | ok |
| 3 | C=0.1, epsilon=0.01, gamma=0.1 | 1.992 | 0.0417 | ok |
| 4 | C=100, epsilon=0.1, gamma=0.01 | 2.151 | 0.0622 | ok |
| 5 | C=100, epsilon=0.01, gamma=scale | 2.783 | 0.1971 | ok |
| 6 | C=1000, epsilon=0.01, gamma=0.01 | 2.398 | 0.2264 | ok |
| 7 | C=1, epsilon=0.001, gamma=0.1 | 2.041 | 0.0433 | ok |
| 8 | C=100, epsilon=0.01, gamma=0.001 | 2.015 | 0.0537 | ok |
| 9 | C=1000, epsilon=0.01, gamma=0.001 | 2.057 | 0.0625 | ok |

### BTC P0 — `2026-10-29T145544Z_btc_svr_P0_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | C=0.1, epsilon=0.1, gamma=0.01 | 752.888 | 0.0801 | ok |
| 1 | C=10, epsilon=0.01, gamma=0.1 | 752.752 | 0.0715 | ok |
| 2 | C=0.1, epsilon=0.1, gamma=scale | 752.870 | 0.0707 | ok |
| 3 | C=0.1, epsilon=0.01, gamma=0.1 | 752.865 | 0.0689 | ok |
| 4 | C=100, epsilon=0.1, gamma=0.01 | 753.196 | 0.0696 | ok |
| 5 | C=100, epsilon=0.01, gamma=scale | 754.075 | 0.0699 | ok |
| 6 | C=1000, epsilon=0.01, gamma=0.01 | 754.457 | 0.0748 | ok |
| 7 | C=1, epsilon=0.001, gamma=0.1 | 752.698 | 0.0759 | ok |
| 8 | C=100, epsilon=0.01, gamma=0.001 | 752.607 | 0.0748 | ok |
| 9 | C=1000, epsilon=0.01, gamma=0.001 | 753.232 | 0.0708 | ok |

### BTC P2 — `2026-10-29T145546Z_btc_svr_P2_seed42`

10 trials, 0 failed, stopped by `max_trials`.

| Trial | Configuration | Tuning MAE | Seconds | Status |
|---:|---|---:|---:|---|
| 0 | C=0.1, epsilon=0.1, gamma=0.01 | 752.880 | 0.0881 | ok |
| 1 | C=10, epsilon=0.01, gamma=0.1 | 752.204 | 0.0766 | ok |
| 2 | C=0.1, epsilon=0.1, gamma=scale | 752.863 | 0.074 | ok |
| 3 | C=0.1, epsilon=0.01, gamma=0.1 | 752.864 | 0.0734 | ok |
| 4 | C=100, epsilon=0.1, gamma=0.01 | 755.310 | 0.076 | ok |
| 5 | C=100, epsilon=0.01, gamma=scale | 752.579 | 0.0779 | ok |
| 6 | C=1000, epsilon=0.01, gamma=0.01 | 757.273 | 0.0831 | ok |
| 7 | C=1, epsilon=0.001, gamma=0.1 | 752.631 | 0.0716 | ok |
| 8 | C=100, epsilon=0.01, gamma=0.001 | 752.774 | 0.0762 | ok |
| 9 | C=1000, epsilon=0.01, gamma=0.001 | 755.894 | 0.088 | ok |

## Files in each run folder

`manifest.json` (provenance: commit, data hash, protocol, periods) · `config.json` (budget) · `metrics.json` (validation metrics and every trial) · `predictions.csv` (per-date forecasts) · `environment.json` (package versions).
