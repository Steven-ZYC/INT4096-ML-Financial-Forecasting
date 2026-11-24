# INT4096 — Learning ML Through Financial Time-Series Forecasting

A reproducible, leakage-safe comparison of model families and preprocessing
strategies for **next-session close prediction** on **Apple (AAPL)** and
**Bitcoin (BTC)**, built as a teaching vehicle for an INT4096 group project
(EdUHK, Semester 1, 2026–27).

> **This is not investment advice.** Everything here is historical, educational
> and non-advisory. Forecast error does not imply profitability, and past
> performance does not predict future returns.

**Deliverables**

| Artifact | Path | Status |
|---|---|---|
| Interactive website | [https://steven-zyc.github.io/INT4096-ML-Financial-Forecasting/](https://steven-zyc.github.io/INT4096-ML-Financial-Forecasting/) | step-by-step explainer, deployed from `deliverables/website/index.html` by `.github/workflows/pages.yml` |
| Final report (PDF) | [`deliverables/report/INT4096_Final_Report.pdf`](deliverables/report/INT4096_Final_Report.pdf) | compiled, 11 pages, 2,478 words, sha256 `b8a0bb719c735b26…` |
| LaTeX source | [`deliverables/report/latex/main.tex`](deliverables/report/latex/main.tex) | builds clean (`bash deliverables/report/latex/build.sh`) |
| Word-count log | [`deliverables/report/word_count.txt`](deliverables/report/word_count.txt) | 2,399 body + 100 headings |
| Presentation (PDF) | [`deliverables/presentation/INT4096_Presentation.pdf`](deliverables/presentation/INT4096_Presentation.pdf) | 26 pages (18 + 6 backup + 2 references), sha256 `160dd968301a8d50…` |
| Slide source | [`deliverables/presentation/slides/main.tex`](deliverables/presentation/slides/main.tex) | beamer; builds clean, 0 overfull boxes |
| Slide planning docs | [`deliverables/presentation/planning/`](deliverables/presentation/planning/) | storyboard, timing plan, speaker notes, bilingual script |
| Colab notebook | [`deliverables/notebook/INT4096_Final_Colab.ipynb`](deliverables/notebook/INT4096_Final_Colab.ipynb) | executes end to end in tests |
| Protocol, runs, audit | [`docs/`](docs/) | frozen protocol, 20 runs, audit trail |
| Teaching material | [`deliverables/lesson/`](deliverables/lesson/) | lesson, 5 tasks, teacher notes |

> **Published:** <https://github.com/Steven-ZYC/INT4096-ML-Financial-Forecasting>
> (private, release [`v0.1.0`](https://github.com/Steven-ZYC/INT4096-ML-Financial-Forecasting/releases/tag/v0.1.0)).
> CI runs the tests and builds the report on every push; a clone of the remote
> rebuilds the PDF byte-identically. GitHub is a reproducibility archive — the
> **Moodle** upload remains the submission of record
> ([checklist](docs/project/moodle_checklist.md)).

---

## Headline result (validation only; test block sealed)

Across **2 assets × 5 model families × 2 preprocessing variants = 20 runs**, no
trained model beat naive persistence by more than ~0.5%, and two were *worse* than
it. That negative result is the finding, not a failure.

| Model | AAPL `skill_MAE` | BTC `skill_MAE` |
|---|---:|---:|
| `svr` | +0.52% | +0.08% |
| `ridge` | +0.29% | +0.12% |
| `hist_gradient_boosting` | +0.25% | −0.04% |
| `linear_baseline` | −0.50% | +0.05% |
| `random_forest` | −0.78% | +0.06% |

`skill_MAE = 1 − MAE_model / MAE_naive`; 0 means "no better than copying today's
price". Source of truth: [`docs/research/run_registry.md`](docs/research/run_registry.md).

The clearest teaching artifact in the project: applying feature scaling changes a
**random forest by exactly 0.0000%** and a **kernel SVR by a measurable amount** —
see [`experiments/figures/fig06_ablation_delta.png`](experiments/figures/) and
[`deliverables/lesson/lesson_plan.md`](deliverables/lesson/lesson_plan.md).

---

## Quick start

```bash
# 1. Environment
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. Tests (temporal integrity, metrics, manifests, model lanes, notebook)
PYTHONPATH=src .venv/bin/python -m pytest -q

# 3. Everything: snapshots -> cards -> experiment matrix -> figures -> registry
bash scripts/reproduce.sh

# 4. Offline (use the committed snapshots, no network)
bash scripts/reproduce.sh --offline

# 5. Build the report: regenerate figures/tables, compile, recount, copy PDF
bash deliverables/report/latex/build.sh

# 6. Build the slide deck (beamer)
bash deliverables/presentation/slides/build.sh
```

The report build needs a TeX distribution with `latexmk`, `bibtex` and `texcount`
(TeX Live, or TinyTeX). `scripts/reproduce.sh` needs only Python.

`scripts/reproduce.sh` never overwrites an immutable snapshot and **never releases
the sealed test block**.

### Run one experiment cell

```bash
PYTHONPATH=src .venv/bin/python -m int4096.experiments.run \
  --asset AAPL --model svr --variant P2 \
  --max-trials 10 --max-seconds 90 --human-owner "Person 3"
```

Writes `experiments/models/<run_id>/{manifest.json,metrics.json,predictions.csv,config.json,environment.json}`
and appends one line to `experiments/models/registry.jsonl`.

### Regenerate documents from artifacts

```bash
PYTHONPATH=src .venv/bin/python -m int4096.data.cards               # dataset cards
PYTHONPATH=src .venv/bin/python -m int4096.experiments.registry_report
PYTHONPATH=src .venv/bin/python scripts/build_notebook.py           # Colab notebook
```

---

## Google Colab

Open [`deliverables/notebook/INT4096_Final_Colab.ipynb`](deliverables/notebook/INT4096_Final_Colab.ipynb)
and choose **Runtime → Run all**.

The notebook:

- installs only what is missing;
- verifies the dataset SHA-256 before using it;
- contains a live demonstration that features cannot see the future;
- runs the baseline and four model families on the validation block;
- shows the preprocessing ablation;
- includes two learner-facing leakage exercises;
- **does not** unblind the test block.

If the data files are absent, set `INT4096_REPO` to your repository URL, or upload
`data/raw/` beside the notebook. The notebook fails loudly rather than inventing
data.

---

## What is in this repository

```text
deliverables/                 EVERYTHING WE PRESENT OR SUBMIT (see deliverables/README.md)
  presentation/               INT4096_Presentation.pdf (final deck)
    slides/                   beamer source, figures, generated numbers/tables, build.sh
    script/                   bilingual speaker script (.md source, .pdf to print)
    planning/                 timing plan + speakers, storyboard, speaker notes, story
  report/                     INT4096_Final_Report.pdf, word count, draft; latex/ source
  notebook/                   Colab notebooks (final, teaching template)
  lesson/                     lesson plan, formative tasks with answers, teacher notes
  website/                    interactive explainer of the pipeline (index.html, built from the repo)
data/                         (see data/README.md)
  raw/                        immutable source snapshots + SHA-256 manifests
  cards/                      dataset cards (provenance, statistics, quality checks)
  splits/                     train/validation/test boundaries and tuning folds, per asset
experiments/                  the only source of reported numbers (see experiments/README.md)
  models/<model>/             one folder per model: its runs + README (grid, tuning trials, results)
  models/registry.jsonl       append-only registry of every run
  analysis/                   bootstrap intervals, autocorrelation diagnostic
  supplementary/              add-on experiments (MLP/LSTM direction test)
configs/research_protocol.yaml frozen protocol (machine-readable)
src/int4096/
  data/                       providers, snapshots, validation, splits, cards
  features/                   causal features, P0–P4 preprocessing variants
  models/                     one file per model family, shared pipeline interface
  evaluation/                 baselines, metrics, bootstrap, figures
  experiments/                runner, manifests, tuning, registry report
  paths.py                    every repository location, in one place
tests/                        83 tests, incl. mutation-verified leakage suite
scripts/                      reproduce.sh, builders, mutation_check.py, verify_fixes.py
docs/
  course/                     course requirements and rubric
  research/                   protocol, decision log, feature dictionary, run registry
  quality/                    acceptance checklist, leakage audit, reproducibility manifest
  project/                    responsibilities, hand-off checklists, history of the build
AGENTS.md                     working notes for anyone changing the repository
.github/workflows/ci.yml      tests, report build and deck build on push
```

---

## Scientific guarantees, and how they are enforced

| Guarantee | Enforcement | Evidence |
|---|---|---|
| No future information in features | Feature functions recomputed independently in tests; static guard; mutation testing | `tests/test_temporal_integrity.py`, `scripts/mutation_check.py` |
| No label crossing a split boundary | One row purged at each boundary | `purge_gap: 1`, `test_split_purge_gap_prevents_label_crossing` |
| Preprocessing fitted on training rows only | Scaler lives inside the pipeline, refit per fold | `test_project_preprocessor_is_train_fitted` |
| Data provenance | SHA-256 manifest verified before every run | `run_cell`, probe `LEAK-003` |
| Every number traceable | Run manifests record commit, data hash, protocol, seed, config | `src/int4096/experiments/manifest.py` |
| Failures are visible | Append-only registry; `FAILED`/`INCOMPLETE`/`NOT_RUN` states | `experiments/models/registry.jsonl` |
| Test block stays sealed | `allow_test=False` by default; notebook test asserts no unblinding | `tests/test_notebook.py` |
| The test suite can actually fail | 5 injected leakage defects, all detected | `scripts/mutation_check.py` |

### Verified leakage audit

An independent auditor subagent reviewed the pipeline and returned **FAIL** with
two HIGH-severity findings:

1. outer split boundaries were not purged (the last validation label was a sealed
   test price — perturbing one test price moved the headline metric by 0.408);
2. the leakage test suite could not detect a one-bar `shift(-1)` or a `bfill`.

Both were fixed; the fixes are recorded in
[`docs/quality/leakage_audit.md`](docs/quality/leakage_audit.md) and verified by
`python scripts/verify_fixes.py` (8/8 probes) and
`python scripts/mutation_check.py` (5/5 defects caught).

---

## Multi-agent development method

The project was built with a single accountable coordinator session plus bounded
specialist subagents (Pi + `pi-subagents` 0.84.0):

`int-scout` · `int-methodologist` · `int-data-steward` · `int-model-builder`
(parameterised per family) · `int-executor` · `int-leakage-auditor` ·
`int-repro-auditor` · `int-claim-auditor` · `int-educator` · `int-report-editor`

Five students are **human owners**, not processes; parallel agents are used for
read-only inspection and non-overlapping file ownership. Full design, gates and
verified delegation transcripts: [`docs/project/multi_agent_design.md`](docs/project/multi_agent_design.md).

---

## Known gaps (stated, not hidden)

- **The official course specification is not in this repository.** The
  requirement matrix is a faithful transcription from the project owner's brief
  and must be re-verified against the official PDF (`docs/course/` is empty).
- **The test block is sealed.** No held-out metrics exist yet; releasing it is a
  human decision (D7).
- **P3/P4 ablation cells are not yet run**; P1 is `NOT_RUN` by design because the
  snapshots contain no missing values (D13).
- **Six decisions need human sign-off** (D1, D2, D5, D6, D7, D8) — see
  [`docs/research/decision_log.md`](docs/research/decision_log.md). D8
  (training on the price *change*) is the most consequential.
- **No learner study was run**, so no learning-gain claim is made anywhere.

---

## Data sources and licences

| Asset | Provider | Notes |
|---|---|---|
| AAPL | `stockanalysis.com` public history endpoint | Raw + split/dividend-adjusted close; USD; US exchange sessions |
| BTC | Binance public REST klines (`BTCUSDT`) | 24/7 UTC daily bars; USDT is not exactly USD; single venue, not a global index |

Snapshots are committed with SHA-256 manifests so every reported number can be
traced to exact bytes. Market data remains subject to the providers' terms; it is
included here for non-commercial coursework.
