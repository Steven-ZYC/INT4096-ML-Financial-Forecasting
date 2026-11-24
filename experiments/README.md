# Experiments

Everything here is produced by code from `data/` and `configs/research_protocol.yaml`.
These files are the only source of reported numbers.

| Folder | What is in it |
|---|---|
| [`models/`](models/README.md) | One folder per model (`linear_baseline`, `ridge`, `svr`, `random_forest`, `hist_gradient_boosting`). Each holds its four runs (AAPL/BTC × P0/P2) and a README with the search grid, the chosen configuration, every tuning trial and the validation results. `registry.jsonl` lists every run. |
| `analysis/` | Cross-run analysis: block-bootstrap skill intervals for all 20 runs and the return-autocorrelation diagnostic. |
| `figures/` | Figures regenerated from the runs by `scripts/reproduce.sh` (not tracked). |
| `supplementary/` | Add-on experiments outside the 20-run comparison, e.g. the MLP/LSTM direction test (`scripts/supplementary_direction_test.py`, decision D14). |

Re-run everything: `bash scripts/reproduce.sh`. Summaries: `python scripts/summarize_models.py`.
Naive persistence (tomorrow equals today) is computed inside every run, so it has no folder of its own.
