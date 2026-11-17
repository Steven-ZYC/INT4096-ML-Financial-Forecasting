# Five-Person Responsibilities and Presentation Plan

**Group roster (confirmed).** Slot numbers are kept alongside names because the
task graph, gate table and speaker plan below refer to them.

| Slot | Name | Primary ownership | Model lane |
|---|---|---|---|
| 1 | Dong Yuankun | shared data pipeline + preprocessing ablation | `hist_gradient_boosting` |
| 2 | Zhang Haoyu | linear family | `ridge`, `linear_baseline` |
| 3 | Lau Pak Hei | kernel methods | `svr` |
| 4 | Lui Shing Lam | bagged trees | `random_forest` |
| 5 | Zhang Yancheng | integration, packaging, reproducibility | — (no fifth model) |

**Data protection.** Student IDs are deliberately **not** stored in this
repository: they are personal data and the project's Git policy excludes them.
Each member's ID is entered directly into Moodle at submission time.

**Status:** the allocation below was assigned when the roster was confirmed. Each
member should still verify that they can defend their lane (see §1) before the
presentation; swap lanes now rather than after rehearsing.

The course requires that **every member speaks** in a **≤20-minute** English
presentation worth **20%** of the grade. Ownership below is therefore paired with
a speaking section, not just a coding task.

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

| Slot | Member | Primary ownership | Model lane | Research accountability | Secondary |
|---|---|---|---|---|---|
| 1 | **Dong Yuankun** | Shared data pipeline + preprocessing ablation | `hist_gradient_boosting` (hardest lane) | Data provenance, dataset cards, **RQ3** preprocessing study | Leakage-audit support |
| 2 | **Zhang Haoyu** | Linear family | `ridge` + `linear_baseline` | Theory of regularized linear models; **RQ1** framing | Introduction & learning explanations |
| 3 | **Lau Pak Hei** | Kernel methods | `svr` | Scaling sensitivity, kernel intuition; the P2 contrast | Diagnostic figures |
| 4 | **Lui Shing Lam** | Bagged trees | `random_forest` | Overfitting/variance, extrapolation limits; **RQ2** | Limitations & threats to validity |
| 5 | **Zhang Yancheng** | Packaging + comparison | _(integration, not a 5th model)_ | Colab notebook, run registry, reproducibility | Slides integration, Q&A preparation |

**Why Zhang Yancheng has no model lane.** The brief permits a defensible lineup rather
than a forced fifth family. Zhang Yancheng owns the deliverable that carries 20% of the
programming mark (an executable, Colab-compatible notebook) plus reproducibility —
more work than a fifth near-duplicate regressor.

**Optional fifth model (`mlp`).** Available but **gated** behind decision D2
(recorded oral guidance). If the group enables it, Zhang Yancheng owns it and Dong Yuankun's
preprocessing load is reduced accordingly.

### Cross-review (mandatory, and not optional politeness)

| Artefact | Author | Independent reviewer |
|---|---|---|
| Data pipeline, features | Dong Yuankun | Lui Shing Lam |
| `ridge` lane | Zhang Haoyu | Lau Pak Hei |
| `svr` lane | Lau Pak Hei | Zhang Haoyu |
| `random_forest` lane | Lui Shing Lam | Dong Yuankun |
| Notebook + registry | Zhang Yancheng | Zhang Haoyu |
| Ablation analysis | Dong Yuankun | Zhang Yancheng |
| Report | all (section owners) | `int-claim-auditor` + one human |
| Slides | all | Zhang Yancheng |

Review means: run the tests yourself, read the code, and state in the shared log
that you did. A review that only reads the summary is not a review.

---

## 3. Task ownership by gate

| Gate | Lead | Support | Evidence required |
|---|---|---|---|
| G0 Requirements & architecture | Zhang Haoyu | all | `docs/requirements/`, `.pi/agents/` |
| G1 Data & temporal integrity | Dong Yuankun | Lui Shing Lam | dataset cards, split tests |
| G2 Executable baseline | Zhang Yancheng | Zhang Haoyu | naive + linear run manifests |
| G3 Model lanes | Persons 2–4 (+1) | — | one manifest + test per lane |
| G4 Ablation & leakage audit | Dong Yuankun | Zhang Yancheng | `docs/quality/leakage_audit.md`, ablation figure |
| G5 Education | Zhang Haoyu | Lau Pak Hei | `docs/education/` |
| G6 Reproducibility | Zhang Yancheng | — | clean-env transcript, notebook run |
| G7 Deliverables | all | Zhang Yancheng integrates | report, slides, data, notebook |

---

## 4. Presentation plan (≤20 minutes, five speakers)

> **These are presentation roles, not research roles.** Who speaks for how long is
> chosen for narrative quality and delivery confidence. It is *not* a statement
> about who wrote which code, ran which experiment or owns which research
> question — that is §1–§3 above and does not change because of the speaking plan.

The deck is organised as a five-act story (**16 narrative slides + 5 backup**);
each act raises the question the next one answers. Full detail in
`docs/presentation/` (storyboard, timing plan, bilingual script, speaker notes).

| Act | Slides | Presenter | Content | Time |
|---|---|---|---|---|
| I — The challenge | 1–2 | Lau Pak Hei (1), Zhang Haoyu (2) | The core question; why market data teaches ML | 1:55 |
| II — A fair experiment | 3–9 | Dong Yuankun (3, 6, 7), Zhang Haoyu (4, 5), Lau Pak Hei (8, 9) | Two markets, delta target, pre-registered questions, features, leakage control, five paradigms, the baseline | 7:25 |
| III — The reveal | 10–11 | Zhang Yancheng | Validation skill table; bootstrap interval forest plot | 2:35 |
| IV — Investigating why | 12–13 | Zhang Yancheng | Preprocessing ablation; signal and structure limits | 2:20 |
| V — The bigger lesson | 14–16 | Zhang Yancheng (14), Dong Yuankun (15), Lui Shing Lam (16) | Classroom lab, engineering takeaways, boundaries, final line | 3:15 |

**Formal speech: 17:30**, plus ~0:30 of handovers and 2:00 of Q&A — inside the
20-minute limit.

| Presenter | Slides | Speaking time | Technical content |
|---|---|---:|---|
| Lau Pak Hei | 1, 8, 9 | **2:45** | opens the question; explains model mechanisms and the baseline |
| Zhang Haoyu | 2, 4, 5 | **3:15** | teaching rationale, target definition, pre-registration |
| Dong Yuankun | 3, 6, 7, 15 | **4:30** | data protocol, features, leakage control, engineering lessons |
| Zhang Yancheng | 10–14 | **5:45** | results, uncertainty, ablation, classroom lab (one continuous block) |
| Lui Shing Lam | 16 | **1:15** | scope, next steps, final takeaway |

Every member has a substantive role. Six handovers are scripted as technical
bridges in `docs/presentation/speaker_notes.md`; the full spoken text, with a
Chinese translation for comprehension, is in
`docs/presentation/speaker_script_bilingual.md`.

## 5. Q&A preparation (each member owns two answers)

| Question | Owner | Prepared answer must include |
|---|---|---|
| "Isn't this just a random walk? Why bother?" | Lui Shing Lam | Near-zero return autocorrelation; persistence is a *strong* baseline; the educational value is in *why* complexity fails |
| "Did you leak future data?" | Dong Yuankun | Causal features, chronological split, boundary purge, mutation-tested suite |
| "Why not use an LSTM / deep learning?" | Lau Pak Hei | Written handout discourages DL; oral guidance is `[B]`, not a rule change; a shallow MLP is available but gated (D2); the question asked does not require sequence modelling |
| "Is 0.5% skill meaningful?" | Zhang Yancheng | No — state the uncertainty caveat; a difference this small is not evidence of superiority |
| "Did you use AI?" | Zhang Haoyu | Yes, with named human review per lane; acknowledged in the report |
| "Can we use this to trade?" | Zhang Yancheng | No. Error metrics ≠ profit; no costs, no risk model; explicitly non-advisory |
| "Why raw close, not adjusted?" | Dong Yuankun | Retroactive adjustment factors would leak; window has no split; dividends ignored (stated) |
| "Why do AAPL and BTC have different row counts?" | Lui Shing Lam | Different calendars (exchange sessions vs 24/7); never aligned by row |

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
| Dong Yuankun | High | High | 4 min |
| Zhang Haoyu | Medium | High (theory) | 3.5 min |
| Lau Pak Hei | Medium | Medium | 4 min |
| Lui Shing Lam | Medium | High (limitations) | 3.5 min |
| Zhang Yancheng | High (packaging) | Medium | 3 min |

If the optional `mlp` lane is enabled, add ~4 hours to Zhang Yancheng and remove one
variant sweep from Dong Yuankun. This must be agreed before G3 starts.
