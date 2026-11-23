# AGENTS.md

Notes for anyone, human or AI, working in this repository.

## The project

Group coursework for INT4096 (AI and Machine Learning in Education, EdUHK, 2026–27),
five students. We forecast the next daily close of Apple (AAPL) and Bitcoin (BTC), compare
five model families against a "copy today's close" baseline, test raw vs standardised
inputs, and turn the result into a 60-minute lesson on how to judge an AI score.

Forecasting is the teaching vehicle. The real deliverable is a comparison that people can
trust and a lesson built on it.

## Where things are

| What | Where |
|---|---|
| Assignment and rubric | `docs/requirements/course_requirements.md` |
| Team decisions, dated | `docs/research/decision_log.md` |
| Frozen protocol | `docs/research/protocol.md`, `configs/research_protocol.yaml` |
| Code | `src/int4096/` (data, features, models, experiments, evaluation) |
| Tests | `tests/` |
| Experiment outputs | `artifacts/experiments/`, summaries in `artifacts/analysis/` |
| Lesson materials | `docs/education/` |
| Report | `docs/report/` |
| Story, script, slides | `docs/story/`, `docs/presentation/`, `slides/latex/` |
| Notebooks | `notebooks/` |
| Progress checklist | `docs/quality/acceptance_checklist.md` |

If two documents disagree, the course requirements win, then the decision log, then the
protocol. Results come from `artifacts/`, not from prose that quotes them.

## How the method works

- **Target:** next day's raw `Close` in each asset's own calendar. The last row has no
  label and is dropped. Features use only data up to the current bar.
- **Two separate datasets:** AAPL trades in exchange sessions and BTC trades 24/7. They
  are never aligned row by row.
- **Splits:** chronological 60 / 20 / 20 (train / validation / test) per asset, with one
  purged row at each boundary. Preprocessing is fitted on training rows inside the
  pipeline. The test block is held back until the team decides to release it.
- **Baseline:** naive persistence (`y_hat = Close_t`) appears in every results table and
  figure. A plain linear model gives a simple learned comparison.
- **Metrics:** MAE, RMSE, R², and skill = 1 − MAE_model / MAE_naive. Compare across
  assets with relative measures, since AAPL dollars and BTC dollars are not comparable.
  Uncertainty comes from paired comparisons on the same dates.

Changing the target, data, split or main metric is a team decision: record it in the
decision log and bump `protocol_version`.

## Provenance tags

Some documents mark where a statement comes from:

- **[A]** written course rule (handout, rubric, official page)
- **[B]** something the instructor said in class, reported by a student. Useful, but not
  published, so confirm it before relying on it.
- **[C]** team decision recorded in the decision log
- **[D]** proposal, not yet agreed

## Commands

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q          # unit and leakage tests
bash scripts/reproduce.sh              # data -> experiments -> artifacts
python3 scripts/mutation_check.py      # injected leakage bugs should all be caught
bash slides/build.sh                   # numbers + figures from artifacts, compile deck
python3 scripts/build_script_pdf.py    # printable bilingual script (xelatex + CJK font)
```

Downloading data needs network access. The slide build needs `latexmk`, beamer with the
metropolis theme, and `biblatex`. Beamer does not warn when content runs off the bottom of a
page, so check the rendered PDF. The Colab notebook (`notebooks/INT4096_Final_Colab.ipynb`)
should rebuild its outputs when run.

## The presentation

Work in this order: story, then script, then slides.

1. `docs/story/feature_extraction_story.md` holds the structure and the claims.
2. `docs/presentation/speaker_script_bilingual.md` holds the words.
3. `slides/latex/main.tex` is the deck.

Change the story first and bring the other two into line.

- Numbers on slides come from macros in `slides/latex/generated/numbers.tex`, which
  `scripts/build_slide_assets.py` generates from `artifacts/`.
- The talk is split into voice blocks (`docs/presentation/timing_plan.md`). Each of the
  five members speaks `[A]`.
- The plan assumes about 105 spoken words a minute and has to fit inside 20 minutes `[A]`.
