# INT4096: Learning ML Through Financial Time-Series Forecasting

Group coursework for INT4096 (AI and Machine Learning in Education, EdUHK, 2026–27).
We forecast the next daily close of **Apple (AAPL)** and **Bitcoin (BTC)**, compare five
models with a "copy today's close" baseline, and turn the result into a lesson on how to
judge an AI score.

> Educational and historical only. **This is not investment advice.**

## Deliverables

| Item | Link |
|---|---|
| Report | [PDF](deliverables/report/INT4096_Final_Report.pdf) · [LaTeX source](deliverables/report/latex/) |
| Presentation | [PDF](deliverables/presentation/INT4096_Presentation.pdf) · [slides and script](deliverables/presentation/) |
| Notebook | [source](deliverables/notebook/INT4096_Final_Colab.ipynb) · [with outputs](deliverables/notebook/INT4096_Final_Colab_executed.ipynb) · [how to run](deliverables/notebook/README.md) |
| Lesson | [plan, tasks and teacher notes](deliverables/lesson/) |
| Website | [interactive walkthrough](https://steven-zyc.github.io/INT4096-ML-Financial-Forecasting/) |
| Original data | [data/raw](data/raw/) · [dataset cards](data/cards/) |

## Result

Skill is `1 − MAE_model / MAE_naive`: zero means no better than copying today's close.
Validation set, standardised inputs:

| Model | AAPL | BTC |
|---|---:|---:|
| SVR (RBF) | +0.52% | +0.08% |
| Ridge | +0.29% | +0.12% |
| Gradient boosting | +0.25% | −0.04% |
| Linear baseline | −0.50% | +0.05% |
| Random forest | −0.78% | +0.06% |

No model meaningfully beat the baseline. Across all 20 runs (5 models × 2 assets ×
raw and standardised inputs), 5 were worse than it, and every 95% bootstrap interval
includes zero. The test set is still sealed. Full list: [run registry](docs/research/run_registry.md).

## Run it

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q                    # unit, leakage and notebook tests
bash scripts/reproduce.sh --offline              # rerun on saved data (adds new runs)
bash deliverables/report/latex/build.sh          # report (needs TeX)
bash deliverables/presentation/slides/build.sh   # slides (needs TeX)
.venv/bin/python scripts/build_notebook.py       # regenerate the notebook
```

The neural-network experiment also needs PyTorch; see the
[notebook guide](deliverables/notebook/README.md).

## Layout

| Folder | Contents |
|---|---|
| [`src/int4096/`](src/int4096/) | data, features, models, evaluation, experiment runner |
| [`experiments/`](experiments/) | every run, analysis and the neural test; source of all reported numbers |
| [`tests/`](tests/), [`scripts/`](scripts/) | tests, builders, [leakage mutation check](scripts/mutation_check.py) |
| [`configs/`](configs/) | [experiment protocol](configs/research_protocol.yaml) |
| [`docs/`](docs/) | [decisions](docs/research/decision_log.md), [protocol](docs/research/protocol.md), [leakage audit](docs/quality/leakage_audit.md), course notes |

## Data

| Asset | Source | Note |
|---|---|---|
| AAPL | stockanalysis.com | raw close, US exchange sessions, USD |
| BTC | Binance `BTCUSDT` | daily, 24/7; one exchange, quoted in USDT |

Snapshots carry SHA-256 manifests. Market data remains subject to the providers' terms
and is included for non-commercial coursework.
