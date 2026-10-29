# Lesson Plan — "Why Smart Models Still Lose to a Simple Rule"

**Audience:** advanced secondary-school students (ages 16–18), pre-university
learners interested in AI, and university students without an AI/ML major.
**Prerequisites:** can read a line chart; knows that a model is "trained" on
examples. No finance knowledge and no calculus assumed.
**Duration:** 60 minutes (45 minutes of activity + 15 minutes of discussion).
**Format:** guided notebook walkthrough (`notebooks/INT4096_Final_Colab.ipynb`).

> **Provenance note.** Every number in this lesson comes from a real run in
> `artifacts/experiments/` and is cited with its run ID and the figure that
> regenerates it. Numbers were not typed by hand; they were read from the run
> registry. If an artifact changes, this lesson must be regenerated.

> **Scope note.** This is a *designed educational resource*. No learners were
> observed, tested or surveyed, so **no claim about learning gains is made**.

---

## 1. Learning objectives

By the end of the lesson a learner can:

| ID | Objective (observable) | Assessment |
|---|---|---|
| O1 | **Explain** why a model that scores well on historical data may still be useless tomorrow, using the train/test split. | Task 1 |
| O2 | **Identify** data leakage from a short code snippet and state the practical consequence. | Task 2 |
| O3 | **Interpret** a skill score relative to a naive baseline, and say what a *negative* value means. | Task 3 |
| O4 | **Predict** which model families are sensitive to feature scaling, and justify the prediction mechanistically (distance vs threshold comparisons). | Task 4 |
| O5 | **Distinguish** forecast error from profitability, and state why a low-error model is not a trading strategy. | Task 5 |

Objectives O1–O4 are assessed by tasks with worked answers; O5 is assessed by a
short written response checked against a marking guide in
`docs/education/formative_tasks.md`.

---

## 2. Lesson sequence

| Time | Segment | What the teacher does | What learners do |
|---|---|---|---|
| 0–5 | **Hook** | Shows one price chart and asks: "If I gave you tomorrow's price rule, would you trust it?" | Vote; write one sentence on what would convince them |
| 5–15 | **The trap: fitting vs generalising** | Runs notebook §3–§4. Deliberately appends absurd *future* prices and shows earlier features are unchanged. | Predict what would happen if the pipeline peeked; check |
| 15–25 | **The opponent everyone forgets** | Runs §5. Shows the naive baseline *before* any model. | Estimate: will a trained model beat "tomorrow = today"? |
| 25–40 | **The comparison** | Runs §6. Reveals the skill table. | Task 3: read the table and explain the negative value |
| 40–50 | **The deep dive** | Runs §7. Shows trees are *exactly* unchanged by scaling, SVR is not. | Task 4: explain why, mechanistically |
| 50–60 | **What this does and does not mean** | Discussion of O5 and limitations. | Task 5 written response |

---

## 3. Objective → evidence map

| Objective | Evidence artifact | Run ID(s) | What the learner sees |
|---|---|---|---|
| O1 | `artifacts/figures/fig01_coverage_and_splits.png` | n/a (dataset-level) | 60/20/20 chronological blocks; the red block is sealed |
| O1 | `tests/test_temporal_integrity.py` future-append test | n/a | Features cannot see the future |
| O2 | notebook §8 Example B | n/a | A `shift(-1)` feature correlating +1.000 with the target |
| O3 | `artifacts/figures/fig04_model_vs_naive.png` | 20 SUCCESS runs, e.g. `..._aapl_random_forest_P2_seed42` | Every bar within ±1% of zero |
| O3 | `docs/research/run_registry.md` | all | The exact `validation_skill_mae` per cell |
| O4 | `artifacts/figures/fig06_ablation_delta.png` | P0/P2 pairs per asset | Trees at exactly 0%; linear/kernel models move |
| O5 | `README.md`, notebook §9 | n/a | Explicit non-advisory statement |

### The three worked examples, in measured numbers

**Example 1 — the baseline is strong.**
Naive persistence on AAPL validation: MAE ≈ 2.90 (price ≈ 230). Every trained
model lands within a fraction of a percent of it:

| Model | AAPL skill_MAE (P2) | BTC skill_MAE (P2) |
|---|---:|---:|
| `ridge` | +0.29% | +0.12% |
| `svr` | +0.52% | +0.08% |
| `random_forest` | **−0.78%** | +0.06% |
| `hist_gradient_boosting` | +0.25% | −0.04% |
| `linear_baseline` | −0.50% | +0.05% |

`skill_MAE = 1 − MAE_model / MAE_naive`. Zero means "no better than copying
today's price". The random forest on AAPL is **worse than doing nothing
clever**. Source: `docs/research/run_registry.md`; regenerate with
`scripts/reproduce.sh`.

**Example 2 — scaling is not a detail, it is the model.**
Applying `StandardScaler` (variant P2) versus not (P0):

| Model | AAPL Δ MAE | BTC Δ MAE |
|---|---:|---:|
| `random_forest` | **0.0000%** (exactly identical) | **0.0000%** (exactly identical) |
| `hist_gradient_boosting` | **0.0000%** (exactly identical) | **0.0000%** (exactly identical) |
| `ridge` | −0.04% | +0.03% |
| `svr` | −0.01% | −0.07% |
| `linear_baseline` | +0.74% | +0.21% |

Trees compare *thresholds inside a single feature*, so a monotone rescaling
changes nothing — the identity is exact, to the last digit. A kernel method
compares *distances across features*, so rescaling changes the geometry. Source:
`artifacts/figures/fig06_ablation_delta.png`.

**Example 3 — why complexity does not rescue you.**
Daily-return autocorrelation is close to zero (notebook §8 Example C). If
yesterday's return barely predicts today's, no amount of model capacity creates
information that is not in the inputs. That is the honest explanation for
Example 1, and it is more valuable than a manufactured win.

---

## 4. Concept links to INT4096 lectures

| Course concept | Where it appears in this lesson |
|---|---|
| Feature/target separation | §3 of the notebook: `X` never contains the label |
| Fitting vs generalisation | §4: train/validation/sealed-test blocks |
| Train-only preprocessing | §6: scaler lives inside the pipeline, refit per fold |
| Evaluation metrics | §5–§6: MAE, RMSE, R² **and** skill vs baseline |
| Model complexity | §6: five families, same budget |
| Leakage prevention | §3 demonstration + Example B |
| Teacher judgement | This document: why we teach the negative result |

---

## 5. Misconceptions to pre-empt

| Misconception | Correction |
|---|---|
| "Higher R² means a better model." | On a trending price level R² is large even for the naive forecast. Compare **skill**, not R². |
| "Deep learning would fix this." | The missing ingredient is information, not capacity. |
| "0.5% better means it works." | State the uncertainty; a difference this small is not evidence of superiority. |
| "Low error means profit." | Error metrics ignore costs, position sizing, and risk. |
| "Scaling always helps." | It is neutral for trees and can *hurt* (see `linear_baseline`, +0.74% on AAPL). |
| "Bitcoin and Apple can be compared directly." | Different calendars and price scales. Only unitless measures like skill are comparable. |

---

## 6. Required disclaimer (display it, do not bury it)

> This lesson uses historical market data for **education only**. Nothing here is
> investment advice or a recommendation to buy or sell any asset. Forecast error
> says nothing about future returns, and past performance does not predict future
> results.
