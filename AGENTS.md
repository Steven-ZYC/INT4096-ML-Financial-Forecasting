# AGENTS.md

Working agreement for anyone — human or AI — who changes this repository. Read it
before you start; the agents under `.pi/agents/` load it as shared context.

## What this project is

INT4096 (AI and Machine Learning in Education, EdUHK, 2026–27) group coursework by five
students. We compare five model families against a "copy today's close" baseline on two
price histories (AAPL and BTC), with a controlled preprocessing comparison (raw vs
standardised), and turn the result into a 60-minute lesson on how to judge an AI score.

Forecasting is the teaching vehicle. What we are really delivering is a comparison people
can trust: no leakage, the same rules for every model, uncertainty stated, and every claim
traceable to a file.

## How to settle a disagreement

When two sources conflict, the earlier one in this list wins:

1. `docs/requirements/course_requirements.md` — the assignment and rubric
2. `docs/research/decision_log.md` — decisions the team approved, with dates
3. `docs/research/protocol.md` and `configs/research_protocol.yaml` — the frozen protocol
   (changing it means bumping `protocol_version`)
4. This file, then the role files in `.pi/agents/`
5. `artifacts/experiments/` — the only place numbers come from
6. Everything else: summaries, chat, commit messages, slide prose

Only the human owner approves a change to the research question, target, dataset, main
metric or split.

Mark how solid a statement is when it matters: **[A]** written course rule, **[B]** oral
guidance reported by a student (not a published rule), **[C]** team decision in the log,
**[D]** proposal, not yet approved.

## Priorities

Correctness first, then reproducibility, then educational value, then completeness, then
polish. Polish never justifies a shortcut on the first two. Nobody should promise a grade.

## Things that are never okay

- Making up a number, run, dataset, citation, URL, instructor approval, learning gain or
  claim about who contributed what. If it is not in `artifacts/` or a cited source, it is
  not a result.
- Calling a run successful when it failed, was cut short, produced NaN or lacks its files.
- Shuffling time-ordered data, or fitting anything (scaler, imputer, selector, tuning
  choice) on validation or test rows.
- Letting the future into a feature: centred windows, `shift(-1)` in the inputs, backfill,
  statistics over the whole series.
- Opening the sealed test block without a recorded human release.
- Comparing AAPL and BTC errors in raw currency units as if they were the same thing.
- Presenting lesson materials as proof that students learned. We built the lesson; we have
  not measured learning.
- Writing "significant" without naming the test, the resampling unit and its limits.
- Committing secrets or large model binaries; force-pushing, rewriting history or running
  broad deletes without the owner's say-so.
- Signing off your own work. The author and the auditor are different people or agents.

## Method rules that keep the science sound

**Time.** Each row is stamped at the close of its bar. The label is the next close in that
asset's own calendar, and the last row is dropped. Every feature uses data up to and
including the current bar. AAPL (exchange sessions) and BTC (24/7) are separate datasets;
never line them up by row number. Keep raw `Close` and `Adj Close` apart and say which one
the target uses.

**Splits and fitting.** Chronological only, with fixed boundaries and a purged row at each
one. Preprocessing sits inside the model pipeline and is fitted on training rows only.
Tuning happens inside the training block. Validation is for reporting; test stays sealed.

**Baseline.** Naive persistence is in every results table and figure. A model that does
not beat it is a legitimate finding and is reported like any other.

**Metrics.** MAE, RMSE, R² and skill = 1 − MAE_model / MAE_naive. R² alone is misleading on
prices, so it never carries a claim by itself. Across assets, use relative measures.
Uncertainty comes from paired comparisons on the same dates, with the resampling unit and
the dependence caveat written down.

**Diagnostics shown in deliverables** (return autocorrelation, price ranges, dataset
statistics) should use train + validation only, or be labelled "full history" wherever they
appear. `[D]` — proposed, awaiting approval.

## Who does what

The ten roles in `.pi/agents/` are job types, not people; the five students own the work
and use the roles as helpers. Pick the role by the job:

| Job | Role | May write to |
|---|---|---|
| Map rubric to evidence, gather sources | `int-scout` | nothing |
| Freeze protocol, hypotheses, splits | `int-methodologist` | protocol, configs |
| Data loading, features, preprocessing | `int-data-steward` | `src/int4096/data`, `src/int4096/features`, `data/raw` |
| One model family (needs a `model_id`) | `int-model-builder` | that model's file, config and test |
| Run the frozen experiment grid | `int-executor` | `artifacts/`, `scripts/` |
| Check for leakage | `int-leakage-auditor` | nothing |
| Rebuild from a clean checkout | `int-repro-auditor` | nothing (scratch space only) |
| Check every claim traces to an artifact | `int-claim-auditor` | nothing |
| Lesson, questions, teacher notes | `int-educator` | `docs/education`, `src/int4096/education` |
| Report, story, script, slides | `int-report-editor` | `docs/report`, `docs/presentation`, `docs/story`, `slides/latex/main.tex` |

Practical rules: read-only roles can run side by side; model work starts only once the data
interface and protocol are frozen; two writers never touch the same file; figures and text
come after the artifacts they describe.

## Gates

A failed gate means nothing downstream may be called finished. Status and evidence paths
live in `docs/quality/acceptance_checklist.md`.

| Gate | Passes when |
|---|---|
| G0 | Role files load, requirements matrix exists |
| G1 | Data snapshots hashed, split and leakage tests green |
| G2 | Persistence baseline ran with real metrics and a valid manifest |
| G3 | Every model lane used the same target, features, test policy and tuning budget |
| G4 | Independent leakage audit passed, ablation isolated, uncertainty caveats written |
| G5 | Lesson objectives map to evidence; no invented learning claims |
| G6 | Clean-environment install, tests, notebook run and hashes all match |
| G7 | Report, slides, dataset, notebook, AI-use acknowledgement and speaking plan are in |

## Commands

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q          # unit and leakage tests (83)
bash scripts/reproduce.sh              # data -> experiments -> artifacts
python3 scripts/mutation_check.py      # injected leakage defects must all be caught
bash slides/build.sh                   # numbers + figures from artifacts, compile, copy to slides/final
python3 scripts/build_script_pdf.py    # printable bilingual script (xelatex, xeCJK, a CJK font)
```

Downloading data needs network and is never done inside tests. The slide build needs
`latexmk`, beamer with metropolis, and `biblatex` with `logreq`; beamer will not warn about
content running off the bottom of a page, so look at the rendered pages. The Colab notebook
(`notebooks/INT4096_Final_Colab.ipynb`) must rebuild its outputs, not show saved ones.

## The talk

The order of work is story → script → slides. `docs/story/feature_extraction_story.md` holds
the structure and the claims; `docs/presentation/speaker_script_bilingual.md` holds the
words; `slides/latex/main.tex` is the deck. Change the story first and bring the others
into line.

- Slide numbers come from macros in `slides/latex/generated/numbers.tex`, which
  `scripts/build_slide_assets.py` writes from `artifacts/`. Never type a result by hand.
- Slides and script name no one. The talk is split into voice blocks
  (`docs/presentation/timing_plan.md`) and each of the five members must speak `[A]`.
- Lead with what the team built and found: a fair benchmark, an audited pipeline,
  intervals for all 20 runs, a lesson ready to teach. A null result is a precise finding
  ("parity with a strong baseline"), and open items are next steps. Keep it accurate: no
  "model X won", no "standardising improved prediction", no use of the test block, no
  learning-gain claim. Caveats that are not on a slide stay in the story and Q&A notes and
  are answered plainly if someone asks.
- The speech is planned at about 105 spoken words a minute and must fit well inside the
  20-minute limit `[A]`.

## Before you say "done"

Run the commands and keep the output; confirm the files exist where you say they do; run
the relevant tests and report the result whether it passed or failed; list anything
blocked; name the next gate. Completion is something you show, not something you intend.

## Not financial advice

Everything here is historical and educational. Nothing is a recommendation to buy, sell or
hold anything, and error metrics say nothing about profit. AI-assisted material is reviewed
by the named human owners and acknowledged in the report as the course requires.
