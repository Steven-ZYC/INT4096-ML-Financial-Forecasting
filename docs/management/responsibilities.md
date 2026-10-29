# Five-Person Responsibilities and Presentation Plan

**Status:** proposed allocation awaiting confirmation by the five members.
No member names are invented here: slots are `Person 1..5` and must be mapped to
real students by the group.

The course requires that **every member speaks** in a **≤20-minute** English
presentation worth **20%** of the grade. Ownership below is therefore paired with
a speaking section, not just a coding task.

---

## 1. Accountability rule

A person owns results they can **defend**, not merely code that was generated.
For each model lane, the named owner must be able to answer, without notes:

1. What does this model family learn, in one sentence?
2. Why does it need (or not need) scaling?
3. What was tuned, within what budget, and against which data?
4. What did it do relative to naive persistence, and why might that be?
5. What is one way this model could fail silently?

An owner who cannot answer these should not present that lane.

---

## 2. Allocation

| Slot | Primary ownership | Model lane | Research accountability | Secondary |
|---|---|---|---|---|
| **Person 1** | Shared data pipeline + preprocessing ablation | `hist_gradient_boosting` (hardest lane) | Data provenance, dataset cards, **RQ3** preprocessing study | Leakage-audit support |
| **Person 2** | Linear family | `ridge` + `linear_baseline` | Theory of regularized linear models; **RQ1** framing | Introduction & learning explanations |
| **Person 3** | Kernel methods | `svr` | Scaling sensitivity, kernel intuition; the P2 contrast | Diagnostic figures |
| **Person 4** | Bagged trees | `random_forest` | Overfitting/variance, extrapolation limits; **RQ2** | Limitations & threats to validity |
| **Person 5** | Packaging + comparison | _(integration, not a 5th model)_ | Colab notebook, run registry, reproducibility | Slides integration, Q&A preparation |

**Why Person 5 has no model lane.** The brief permits a defensible lineup rather
than a forced fifth family. Person 5 owns the deliverable that carries 20% of the
programming mark (an executable, Colab-compatible notebook) plus reproducibility —
more work than a fifth near-duplicate regressor.

**Optional fifth model (`mlp`).** Available but **gated** behind decision D2
(recorded oral guidance). If the group enables it, Person 5 owns it and Person 1's
preprocessing load is reduced accordingly.

### Cross-review (mandatory, and not optional politeness)

| Artefact | Author | Independent reviewer |
|---|---|---|
| Data pipeline, features | Person 1 | Person 4 |
| `ridge` lane | Person 2 | Person 3 |
| `svr` lane | Person 3 | Person 2 |
| `random_forest` lane | Person 4 | Person 1 |
| Notebook + registry | Person 5 | Person 2 |
| Ablation analysis | Person 1 | Person 5 |
| Report | all (section owners) | `int-claim-auditor` + one human |
| Slides | all | Person 5 |

Review means: run the tests yourself, read the code, and state in the shared log
that you did. A review that only reads the summary is not a review.

---

## 3. Task ownership by gate

| Gate | Lead | Support | Evidence required |
|---|---|---|---|
| G0 Requirements & architecture | Person 2 | all | `docs/requirements/`, `.pi/agents/` |
| G1 Data & temporal integrity | Person 1 | Person 4 | dataset cards, split tests |
| G2 Executable baseline | Person 5 | Person 2 | naive + linear run manifests |
| G3 Model lanes | Persons 2–4 (+1) | — | one manifest + test per lane |
| G4 Ablation & leakage audit | Person 1 | Person 5 | `docs/quality/leakage_audit.md`, ablation figure |
| G5 Education | Person 2 | Person 3 | `docs/education/` |
| G6 Reproducibility | Person 5 | — | clean-env transcript, notebook run |
| G7 Deliverables | all | Person 5 integrates | report, slides, data, notebook |

---

## 4. Presentation plan (≤20 minutes, five speakers)

Target **18:00 of content** plus transitions, leaving tolerance inside the
20-minute limit. Every speaker gets substantive technical content — no "and now
my teammate will present the data" hand-offs.

| # | Speaker | Section | Minutes | Must land these points |
|---|---|---|---|---|
| 1 | Person 2 | Problem, education angle, research questions | 3:30 | Why teach ML through forecasting; why two contrasting markets; RQ1–RQ4 |
| 2 | Person 1 | Data, causal features, chronological splits | 4:00 | Provenance + hash; the 10 features; **why a shuffle would be cheating**; the boundary purge |
| 3 | Person 3 | Methods, baseline, honest evaluation | 4:00 | The five families; naive persistence as the real opponent; skill score; why raw dollar errors are not comparable across assets |
| 4 | Person 4 | Results and failure analysis | 3:30 | All models within ~1% of persistence; forest has negative skill on AAPL; what that means |
| 5 | Person 5 | Preprocessing deep dive + education + conclusion | 3:00 | Trees exactly invariant to scaling vs kernel sensitivity; the learner lesson; limitations |
| — | all | Q&A | 2:00 | See §5 |

**Total content: 18:00.** Rehearse twice with a timer; cut from §1 and §5 first,
never from §3 (evaluation rigour carries 20%).

### Evidence each speaker must show

- Person 2: one sentence of the education problem, no data yet.
- Person 1: the split figure (`fig01`) and the purge explanation.
- Person 3: the baseline number before any model number.
- Person 4: `fig04` model-vs-naive, with the shared axis explained.
- Person 5: `fig06` ablation, plus one learner task worked live if time allows.

---

## 5. Q&A preparation (each member owns two answers)

| Question | Owner | Prepared answer must include |
|---|---|---|
| "Isn't this just a random walk? Why bother?" | Person 4 | Near-zero return autocorrelation; persistence is a *strong* baseline; the educational value is in *why* complexity fails |
| "Did you leak future data?" | Person 1 | Causal features, chronological split, boundary purge, mutation-tested suite |
| "Why not use an LSTM / deep learning?" | Person 3 | Written handout discourages DL; oral guidance is `[B]`, not a rule change; a shallow MLP is available but gated (D2); the question asked does not require sequence modelling |
| "Is 0.5% skill meaningful?" | Person 5 | No — state the uncertainty caveat; a difference this small is not evidence of superiority |
| "Did you use AI?" | Person 2 | Yes, with named human review per lane; acknowledged in the report |
| "Can we use this to trade?" | Person 5 | No. Error metrics ≠ profit; no costs, no risk model; explicitly non-advisory |
| "Why raw close, not adjusted?" | Person 1 | Retroactive adjustment factors would leak; window has no split; dividends ignored (stated) |
| "Why do AAPL and BTC have different row counts?" | Person 4 | Different calendars (exchange sessions vs 24/7); never aligned by row |

---

## 6. Working agreements

1. **One writer per file.** Parallel edits go through separate worktrees.
2. **No result enters the report without a run ID.** If it has no artifact, it
   does not exist.
3. **Failures are reported, not deleted.** The registry is append-only.
4. **The test block stays sealed** until a single approved release (D7).
5. **Weekly 15-minute gate review** against
   `docs/quality/acceptance_checklist.md`.
6. **AI-generated code is reviewed by its owner before merge**, and the owner is
   the person who presents it.

---

## 7. Workload estimate (to be confirmed by the group)

| Slot | Implementation | Analysis/writing | Presentation |
|---|---|---|---|
| Person 1 | High | High | 4 min |
| Person 2 | Medium | High (theory) | 3.5 min |
| Person 3 | Medium | Medium | 4 min |
| Person 4 | Medium | High (limitations) | 3.5 min |
| Person 5 | High (packaging) | Medium | 3 min |

If the optional `mlp` lane is enabled, add ~4 hours to Person 5 and remove one
variant sweep from Person 1. This must be agreed before G3 starts.
