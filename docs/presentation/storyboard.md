# Slide Storyboard — One Pipeline, Five Stages

**Deck:** `slides/latex/main.tex` → `slides/final/INT4096_Presentation.pdf`
**Slides:** 17 narrative + 5 backup + 2 reference pages (24 pages) · **Speech:** 16:25 of a 20:00 slot
**Structure source:** `docs/story/feature_extraction_story.md`. Change the story first, then the script, then the deck.
**Companions:** `timing_plan.md` (clock, voice blocks) · `speaker_script_bilingual.md` (words to say) · `speaker_notes.md` (key messages, Q&A routing)

> **Speakers are not named.** The deck footer shows the part, the page and a five-stage progress bar.
> Who speaks which block is decided in `timing_plan.md`; every one of the five members must speak `[A]`.

---

## The spine

The instructor wants the technical implementation explained logically and systematically, in as little
time as possible. So the deck *is* the pipeline: one part per stage, each part answering one question,
and each slide inside a part answering one sub-question. The roadmap on slide 2 shows all five
questions up front; the footer progress bar shows where we are.

| Part | Question | Sub-questions, one slide each |
|---|---|---|
| 1 Data Selection | Which data, from where, and why? | (a) what and (b) where from → slide 3 · (c) why these two → slide 4 · (d) which rows qualify → slide 5 |
| 2 Processing & Features | What can the model legally see? | problems → handling, slide 6 · features, slide 7 · target, slide 8 · split and leakage checks, slide 9 |
| 3 Models & Tuning | Which models, tuned how fairly? | which and why, slide 10 · tuning protocol and chosen values, slide 11 · what else we explored, slide 12 |
| 4 Evaluation | Measured how, and how certain? | metrics, slide 13 · results, slide 14 · uncertainty and why, slide 15 |
| 5 Teaching Design | How does it become a lesson? | tasks ↔ stages ↔ course concepts, slide 16 · summary by stage, slide 17 |

Every empirical number on a slide is a macro generated from `artifacts/` and `data/raw/` by
`scripts/build_slide_assets.py`. The tuning table on slide 11 is generated too
(`slides/latex/generated/tuning_table.tex`).

## Introduction

| # | Title | Must land | Visual |
|---|---|---|---|
| 1 | Learning Machine Learning Through Financial Forecasting | R² hook: SVR 0.9556 vs copy-the-close 0.9555, so a score alone proves little; then the research question | Title, the two R² values, names, small starred disclaimer |
| 2 | Roadmap: One Pipeline, Five Stages | Five stages, one question each; task, yardstick and one-line result | Five-box pipeline diagram |

## Part 1 — Data Selection

| # | Title | Must land | Visual |
|---|---|---|---|
| 3 | What We Used, and Exactly Where It Came From | Two public sources; the exact download URLs; fields, window, bar counts; SHA-256 fingerprints | Source table + the two URLs |
| 4 | Why These Two: Two Markets With Different Characteristics | Calendar gaps, volatility, price scale, dividends all differ, so one protocol on both is a robustness check; only unit-free scores cross assets | Comparison table + `fig02_asset_characteristics` |
| 5 | Selection Conditions: From Raw Bars to Modelling Rows | Four conditions (window after split, raw close, six-check quality gate that rejects rather than repairs, complete history); row funnel to train/val/test | Numbered conditions + row-count funnel |

## Part 2 — Processing and Feature Engineering

| # | Title | Must land | Visual |
|---|---|---|---|
| 6 | Problems in the Raw Data, and How We Handled Each | Six problems, each mapped to one decision | Problem / why / what we did table |
| 7 | Ten Features, Built Only From Information Available at the Close | Ten trailing, scale-free features; future-append test; identical inputs for all models | Feature table with formulas |
| 8 | Engineering the Target: Predict the Change, Then Add It Back | Forecast = close + predicted change; persistence = zero change; found by iteration | Equation + one real worked example |
| 9 | Chronological Split, and Proof That the Pipeline Cannot Peek | 60/20/20 by date, one row purged per boundary (audit: 0.408); 6/6 injected defects caught | Split bar + two text columns |

## Part 3 — Models and Fine-Tuning

| # | Title | Must land | Visual |
|---|---|---|---|
| 10 | Five Models Plus a Baseline: Why Each One Is There | How each predicts, its classic strength, its role here; three mechanisms; no deep learning | Model table |
| 11 | Fine-Tuning: The Same Search and Budget for Every Model | Inner expanding-window CV in the training block, 10 trials, ≤90 s, one seed, frozen grids; the tuner picks the most cautious settings | Fold diagram + generated grid/choice table |
| 12 | What We Explored Beyond Hyperparameters | Target representation, P0 vs P2, what scaling changed (trees identical), grid edges | Four short items + `fig06_ablation_delta` |

## Part 4 — Evaluation

| # | Title | Must land | Visual |
|---|---|---|---|
| 13 | Four Metrics, Each With a Job | MAE, RMSE, R², skill: formula and purpose; R² trap; only skill crosses assets | Metric table with best-AAPL vs persistence values |
| 14 | Results: All 20 Runs Land Within 1% of the Baseline | Best AAPL +0.52%, best BTC +0.26%; range −0.78 to +0.52; 5 below zero | `fig04_model_vs_naive` |
| 15 | How Certain? Every Interval Includes Zero | Paired block bootstrap; 20/20 intervals include zero; near-zero return autocorrelation explains why | `fig08_skill_intervals` |

## Part 5 — Teaching Design

| # | Title | Must land | Visual |
|---|---|---|---|
| 16 | Teaching Design: The Pipeline Becomes a 60-Minute Lesson | Five tasks, each from one stage and one course concept; baseline before models; materials | Task ↔ stage ↔ concept table |
| 17 | Summary: What Each Stage Delivered | One outcome per stage; next steps; not investment advice | Stage / outcome table |

## Backup (not presented)

| # | Title | Use when asked |
|---|---|---|
| 18 | Backup 1: Full 20-Run Transparency Matrix | "Did you cherry-pick P2?" |
| 19 | Backup 2: Experimental Fairness and Manifest Audit | "Was the comparison fair?" |
| 20 | Backup 3: Why One Row Is Dropped at Each Boundary | "How do you know there is no leakage?" |
| 21 | Backup 4: What Signals Did the Models Rely On? | "Which features mattered?" |
| 22 | Backup 5: Q&A Quick-Reference Cards | Any of the common questions |
| 23–24 | References | — |
