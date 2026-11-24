# Model runs

**Generated** by `scripts/summarize_models.py`. One folder per model; inside it, one folder per run (`<timestamp>_<asset>_<model>_<setting>_seed42`). `registry.jsonl` is the append-only list of every run.

| Model | AAPL P0 | AAPL P2 | BTC P0 | BTC P2 |
|---|---:|---:|---:|---:|
| [Linear baseline](linear_baseline/README.md) | +0.24% | -0.50% | +0.26% | +0.05% |
| [Ridge regression](ridge/README.md) | +0.25% | +0.29% | +0.15% | +0.12% |
| [Support vector regression (RBF kernel)](svr/README.md) | +0.51% | +0.52% | +0.01% | +0.08% |
| [Random forest](random_forest/README.md) | -0.78% | -0.78% | +0.06% | +0.06% |
| [Histogram gradient boosting](hist_gradient_boosting/README.md) | +0.25% | +0.25% | -0.04% | -0.04% |

Validation skill versus "tomorrow equals today" (0 = no better). Naive persistence is computed inside every run, so it has no folder of its own.
