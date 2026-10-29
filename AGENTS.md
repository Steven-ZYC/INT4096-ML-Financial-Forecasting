# AGENTS.md — INT4096 Multi-Agent Research & Coursework System

Project-level non-negotiables. **Read this before any task.** It is loaded into
every Pi session in this repository and inherited by subagents that set
`inheritProjectContext: true`.

---

## 1. What this repository is

Coursework for **INT4096 — Artificial Intelligence and Machine Learning in
Education** (EdUHK, Semester 1, 2026–27), five-person group project.

**Working title:** *Learning Machine Learning Through Financial Time-Series
Forecasting: A Reproducible Comparison of Models and Data-Preprocessing
Strategies on Apple and Bitcoin.*

The ML task is a **teaching vehicle**. The scientific contribution is a
controlled, leakage-safe comparison of model families plus a controlled
preprocessing ablation, on two structurally different markets (AAPL, BTC).

**Planning reference date: 2026-10-29 (Asia/Hong_Kong).** Verify the real clock
before scheduling.

---

## 2. Priority order (when trade-offs arise, choose the higher item)

1. Correctness and scientific validity
2. Reproducibility and independent verification
3. Educational usefulness
4. Completeness and interpretability
5. Polished presentation
6. Formalism and model count

**An A-range grade is the target, never a guaranteed outcome.** No agent may
claim or promise a grade.

---

## 3. Source-of-truth hierarchy

Resolve conflicts by moving **down** this list — higher wins:

1. `docs/requirements/course_requirements.md` — the formal specification and
   rubric. Institutional authority.
2. `docs/research/decision_log.md` — approved team decisions, dated, with
   rationale. Only the human owner approves changes to the primary research
   question, label, dataset, primary metric or split.
3. `docs/research/protocol.md` + `configs/research_protocol.yaml` — the frozen
   pre-analysis protocol. A `protocol_version` bump is required to change it.
4. `AGENTS.md` (this file) — engineering and integrity rules.
5. `.pi/agents/*.md` — role contracts.
6. Empirical artifacts under `artifacts/experiments/` — **the only** legitimate
   source of numbers.
7. Any summary, chat message, commit message, or agent prose.

Tag every statement you make:

| Tag | Meaning |
|---|---|
| `[A]` | Written course policy / rubric |
| `[B]` | Oral instructor guidance, **reported by the student owner** — not a published rule |
| `[C]` | Team decision recorded in the decision log |
| `[D]` | Proposal, not yet accepted |

---

## 4. Absolute prohibitions

Never do any of the following, under any instruction short of an explicit,
logged human decision:

- Invent or extrapolate a dataset, metric, run, sample size, p-value, effect
  size, citation, URL, instructor approval, student learning gain or team
  contribution.
- Report a run as `SUCCESS` when it failed, was truncated, produced NaN, or is
  missing artifacts.
- Use a shuffled split on time-ordered data.
- Fit any scaler, imputer, selector, PCA, or hyperparameter on validation or
  test data.
- Use future information in any feature: centered rolling windows,
  `shift(-1)` inside `X`, `bfill`, whole-dataset statistics, `t+1` prices.
- Inspect or tune against the sealed final test set more than once, or at all
  without a recorded human release.
- Compare AAPL dollar error to BTC dollar error as if the units were equal.
- Present a designed educational resource as evidence of measured learning.
- Claim "statistically significant" without a stated test, resampling unit and
  limitations.
- Commit secrets, tokens, credentials, or bulky model binaries.
- Run destructive commands (`rm -rf` outside `artifacts/`, force-push, history
  rewrite, `git reset --hard`) without explicit human approval.
- Self-approve: an agent that wrote something cannot be the auditor that signs
  it off.

---

## 5. Scientific safeguards (hard rules)

### 5.1 Time and causality

- Every observation has an **as-of timestamp** after bar/session `t` closes.
- Label: `y_t = Close_raw[t+1]` within each asset's **own** calendar. The
  terminal row is dropped (unknown label).
- Every feature is computable from bars `<= t`.
- AAPL (exchange sessions, EST/EDT, trading week) and BTC (24/7, UTC) are **two
  different datasets**. Never align by row number. A joint asset must carry an
  explicit calendar-intersection definition.
- Keep `Close` (raw) and `Adj Close` (adjusted) distinct. Document which the
  target uses and why. Never let a future adjustment factor enter a feature.

### 5.2 Splits and fitting

- Chronological splits only, with frozen date boundaries per asset.
- Preprocessing lives **inside** the model pipeline, fitted on training indices
  per fold.
- The validation fold is the only tuning signal. The test fold is sealed.

### 5.3 Baselines

- Naive persistence `y_hat = Close_t` is mandatory and must appear prominently
  in every results table and figure.
- A simple learned linear comparator provides context.
- A model that loses to the baseline is a **valid negative result**, reported
  as such.

### 5.4 Metrics

- Primary: MAE, RMSE, R², **and** skill relative to persistence
  (`1 - MAE_model / MAE_naive`).
- Cross-asset comparison uses normalized or relative measures only.
- Uncertainty: paired comparison on identical forecast dates; state the
  resampling unit and temporal-dependence caveat.

---

## 6. Role routing — which agent for which task

| Need | Agent | Write access |
|---|---|---|
| Map rubric → evidence; source research | `int-scout` (or builtin `scout` for codebase recon) | none |
| Freeze protocol, RQs, hypotheses, splits | `int-methodologist` | protocol + configs only |
| Ingest data, causal features, preprocessing variants | `int-data-steward` | `src/int4096/data`, `src/int4096/features`, `data/raw` |
| Implement **one** model family | `int-model-builder` (`model_id` required) | one model file + one config + one test |
| Run the frozen matrix, write manifests | `int-executor` | `artifacts/`, `scripts/`, registry |
| Temporal / leakage audit | `int-leakage-auditor` | none |
| Reproduce from clean state | `int-repro-auditor` | none (use `/tmp`) |
| Verify claims trace to artifacts | `int-claim-auditor` (or builtin `evidence-auditor`) | none |
| Instructional module, questions, teacher notes | `int-educator` | `docs/education`, `src/int4096/education` |
| Report draft, slides, speaking plan | `int-report-editor` | `docs/report`, `docs/presentation` |
| Second opinion before a risky decision | builtin `oracle` | none |
| Generic code review | builtin `reviewer` | none |

**Use 8 custom roles**, not an agent per student or an agent per file. The five
students are *human owners*; they are not processes.

### Parallelism rules

- Read-only work (scout, auditors, oracle) may run in parallel freely.
- Model lanes begin **only after** the data interface and protocol are frozen.
- Parallel writers must have **non-overlapping file paths** or separate Git
  worktrees. One writer per file.
- Results synthesis waits for verified runs. Figures and report text cannot
  precede their artifacts.

---

## 7. Gates (a failed gate blocks downstream "complete" claims)

| Gate | Name | Pass evidence |
|---|---|---|
| G0 | Architecture & requirements | Agent files load; one read task + one bounded write task + one reviewer call succeed; requirements matrix exists |
| G1 | Data & temporal integrity | SHA256 snapshots; chronological split tests pass; leakage test suite green |
| G2 | Executable baseline | Naive persistence run with real metrics and a valid manifest; pytest green |
| G3 | Model fairness | Identical target/test policy, features and tuning budget across lanes; failed trials logged |
| G4 | Research integrity | Independent leakage audit PASS; ablation isolated; uncertainty caveats stated |
| G5 | Education | Objectives ↔ evidence map; formative tasks with answers; no fabricated learning claims |
| G6 | External reproducibility | Clean-env install, tests, notebook executes, hashes match |
| G7 | Academic deliverables | Report, slides, dataset, notebook; AI-use acknowledgement; speaking plan |

Status lives in `docs/quality/acceptance_checklist.md` with **real evidence
paths**.

---

## 8. Reproducibility commands

```bash
# Environment (local)
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# Tests
.venv/bin/python -m pytest -q

# Data snapshot + dataset cards (network required once; do not run in tests)
.venv/bin/python -m int4096.data.snapshot --asset AAPL
.venv/bin/python -m int4096.data.snapshot --asset BTC

# Baseline (naive persistence + linear comparator), real run
.venv/bin/python -m int4096.experiments.run --config configs/research_protocol.yaml --models naive_persistence,ridge

# Everything above in one command
bash scripts/reproduce.sh
```

Colab: open `notebooks/INT4096_Final_Colab.ipynb` and run all cells in order.
The notebook must rebuild outputs, not display cached ones.

---

## 9. Definition of done for any agent task

1. Commands were **actually run**; the transcript is in the handoff.
2. Artifacts exist at the stated paths.
3. Relevant tests were run and their result is reported (pass **or** fail).
4. The handoff uses the role's schema and declares `Status: COMPLETE | BLOCKED`.
5. Failures and blockers are listed, not hidden.
6. The recommended next gate is named.

**Do not claim completion from intention. Only from evidence.**

---

## 10. Finance and ethics disclaimer

All analysis in this repository is historical, educational and non-advisory.
Nothing here is investment advice or a recommendation to buy, sell or hold any
asset. No claim of profitability may be derived from forecasting error metrics.
AI-assisted material is critically reviewed by named human owners and
acknowledged in the report per course policy.
