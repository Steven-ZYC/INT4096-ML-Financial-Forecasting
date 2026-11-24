# Course Requirements — INT4096 Group Project

**Status:** Working transcription. Source of institutional authority: the
official Group Project Specification and rubric.

**Verification status of this document:**

| Item | Status |
|---|---|
| Full official specification text | **NOT PRESENT in the repository** (`docs/course/` is empty) |
| Rubric weights and deliverable list | Transcribed from the owner's master brief (`int4096/INT4096_Pi_Multi_Agent_Master_Brief.md` §2) — `[B]`-grade provenance, to be re-verified against the official PDF |
| Instructor oral clarifications | `[B]` Reported by the student owner only |
| Topic confirmation form | Uploaded file is a **blank template** — **not** evidence of an approved topic |

> **Action required before G7:** place the official specification in
> `docs/course/` (subject to permission/licensing) and re-verify every row of
> the requirement matrix below. Until then, treat this page as a faithful but
> unverified transcription.

---

## 1. Official objective `[B→A]`

Apply machine learning to an appropriately justified real-world problem related
to education, using public data, with clearly identified features, target, task,
preprocessing and metrics.

Required explanatory content:

- Explanation of the algorithms and the model-selection rationale.
- Cleaning, preprocessing, feature engineering, train/validation/test splitting.
- Evaluation procedure and potential biases.
- Meaningful graphs, results, limitations, and team learnings.

## 2. Deliverables `[B→A]`

| # | Deliverable | Format | Status in repo |
|---|---|---|---|
| 1 | Final report | PDF | Not started |
| 2 | Presentation | PPTX or PDF | Not started |
| 3 | Original dataset | Data file(s) | In progress — real snapshots in `data/raw/` |
| 4 | Colab-compatible notebook | `.ipynb` | Skeleton: `deliverables/notebook/INT4096_Final_Colab.ipynb` |
| — | Uploaded via | Moodle | — |

All four are required. A local file is **not** proof of submission.

## 3. Deadlines and constraints `[B→A]`

| Event | Date / time (HKT) | Note |
|---|---|---|
| Optional topic confirmation | 17 Oct 2026 | Template blank; no approved submission recorded |
| Presentation draft due | **18 Nov 2026, 18:00** | — |
| Presentation slots | **19 and/or 26 Nov 2026** | Confirm the group's assigned slot |
| Final submission | **Sat 28 Nov 2026, 23:59** | 10% marks/day late deduction |

| Constraint | Value | Provenance |
|---|---|---|
| Written report length | ≤2,000 words | `[A]` written spec |
| Additional allowance | ~500 words (~2,500 practical) | `[B]` oral, not published |
| Presentation length | ≤20 minutes | `[A]` |
| Speakers | All five members must speak | `[A]` |
| Language | English | `[A]` |
| Deep learning | Handout discourages it; oral guidance says it may be considered if necessary | `[A]` + `[B]` — **must not be described as a rule change** |
| AI-generated material | Must be critically reviewed, adapted, acknowledged | `[A]` |

## 4. Rubric `[B→A]`

| Category | Weight | A-range evidence |
|---|---:|---|
| Introduction & theoretical background | 20% | Accurate, focused education problem; definitions; relevant algorithms; solid forecasting context; sourced claims |
| Data searching & preparation | 10% | Provenance; samples; detailed statistics; documented cleaning; justified **chronological** splits |
| Programming skill | 20% | Working, readable, modular, commented, tested Python; no obvious bugs; reproducible Colab notebook |
| Model evaluation, discussion & conclusion | 20% | Sound metrics; fair comparison and baseline; analysis not just numbers; justified limitations |
| Report clarity & organization | 10% | Logical, precise English; coherent tables/figures; clear narrative |
| Presentation clarity & results | 20% | Confident five-person delivery ≤20 min; relevant evidence; defensible conclusions |

**Presentation is worth 20%** — equal to programming and to evaluation. Treat
the speaking plan as a first-class deliverable, not an afterthought.

## 5. Course-content connections `[A]`

Lectures cover: supervised ML, regression vs classification, decision trees,
KNN, unsupervised learning, preprocessing, generalization, evaluation, leakage
prevention, teacher judgement; later: neural networks, deep learning, AI agents.

The project must explicitly connect to: feature/target separation, fitting and
generalization, train-only preprocessing, metrics, model complexity, leakage
prevention, and teacher judgement.

**Do not** present financial speculation as evidence of educational
learning-outcome achievement.

---

## 6. Requirement → evidence matrix

`Status` values: `MET` (artifact exists and verified) / `PARTIAL` /
`MISSING` / `NOT_APPLICABLE`.

| ID | Requirement | Tag | Weight | Evidence path | Status | Owner |
|---|---|---|---|---|---|---|
| R1 | Official specification archived in repo | B→A | — | `docs/course/` | **MISSING** | Owner |
| R2 | Education problem statement & audience | A | 20% | `docs/report/`, `deliverables/lesson/` | MISSING | Person 2 |
| R3 | Algorithm explanations for each model family | A | 20% | `docs/report/`, model lane notes | MISSING | Persons 2–5 |
| R4 | Forecasting/theoretical context, sourced | A | 20% | `docs/research/` source register | MISSING | int-scout |
| R5 | Research questions RQ1–RQ4 frozen | C | — | `docs/research/protocol.md` | PARTIAL | int-methodologist |
| R6 | Data provenance & immutable snapshots | A | 10% | `data/raw/*`, dataset cards | PARTIAL (real AAPL/BTC snapshots) | int-data-steward |
| R7 | Descriptive statistics / EDA | A | 10% | `experiments/` EDA figures | MISSING | int-data-steward |
| R8 | Documented cleaning & missingness handling | A | 10% | dataset cards, `src/int4096/data/` | PARTIAL | int-data-steward |
| R9 | Chronological splits with frozen boundaries | A | 10% | `configs/research_protocol.yaml`, tests | PARTIAL | int-methodologist |
| R10 | Causal (leakage-safe) features | A | 20% | `src/int4096/features/`, leakage tests | PARTIAL | int-data-steward |
| R11 | Naive persistence baseline | A | 20% | `src/int4096/evaluation/baselines.py` | PARTIAL | int-executor |
| R12 | 4–5 distinct model families implemented | A | 20% | `src/int4096/models/` | PARTIAL | Persons 1–5 |
| R13 | Comparable tuning budget across models | A | 20% | `configs/experiments/*.yaml` | PARTIAL | int-methodologist |
| R14 | Metrics incl. skill vs baseline | A | 20% | `src/int4096/evaluation/metrics.py` | PARTIAL | int-methodologist |
| R15 | Preprocessing ablation P0–P4 | A | 20% | `configs/`, results | PARTIAL | Person 1 |
| R16 | Meaningful figures with captions | A | 10% | `experiments/figures/` | MISSING | int-executor |
| R17 | Limitations & threats to validity | A | 20% | `docs/report/` | MISSING | Person 4 |
| R18 | Unit tests incl. leakage assertions | A | 20% | `tests/` | PARTIAL | int-repro-auditor |
| R19 | Google Colab notebook, executable | A | 20% | `deliverables/notebook/INT4096_Final_Colab.ipynb` | PARTIAL (skeleton) | Person 5 |
| R20 | Educational module (objectives, tasks, answers) | A | 20% | `deliverables/lesson/` | MISSING | int-educator |
| R21 | Final report PDF ≤2,500 words tracked | A | 10% | `docs/report/` | MISSING | int-report-editor |
| R22 | Slides, 5 speakers, ≤20 min | A | 20% | `deliverables/presentation/planning/` | MISSING | int-report-editor |
| R23 | Dataset uploaded as original dataset | A | 10% | `data/raw/` | PARTIAL | Person 1 |
| R24 | AI-use acknowledgement | A | — | `docs/report/acknowledgements.md` | MISSING | Owner |
| R25 | Contribution statement per member | A | — | `docs/project/responsibilities.md` | PARTIAL | Owner |
| R26 | Non-financial-advice disclaimer | A | — | `README.md`, report, slides | **MET** | int-report-editor |

---

## 7. Written vs oral discrepancies

| Topic | Written `[A]` | Oral `[B]` | How the project handles it |
|---|---|---|---|
| Word count | ≤2,000 | ~+500 permitted | Plan ~2,500; **state both** in the report; never claim the 2,000 limit was removed |
| Deep learning | Avoid DL | DL could be considered if necessary | Keep DL optional; require a documented research justification and a recorded oral guidance note; never quietly add it |
| Topic breadth | ML related to education | Broad ML topic acceptable with a meaningful educational connection | Do not rely on the educational connection as decoration — the module must be substantive |
| Appendices | Not stated to be excluded | Not confirmed | **Do not assume** appendices are excluded from the word limit until verified |

## 8. Grading risk register

| Risk | Weight at stake | Mitigation | Status |
|---|---|---|---|
| Presentation under-rehearsed | 20% | Speaking plan with per-member timing; two rehearsals | Not started |
| Report exceeds word count | 10% | Running count table in `docs/report/` | Not started |
| Evaluation seen as unrigorous | 20% | Baseline prominence, skill score, uncertainty caveats | Partial |
| Education connection seen as decorative | 20% | Real module with objective↔evidence map | Not started |
| Notebook does not run in Colab | 20% | Clean-kernel execution test in G6 | Not started |
| Fabricated/unsourced claim slips in | 10% | `int-claim-auditor` gate before submission | Not started |
| Missing a required deliverable | — | Upload checklist in `docs/quality/` | Not started |
