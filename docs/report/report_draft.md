# Report Draft — INT4096

**Working title:** Learning Machine Learning Through Financial Time-Series
Forecasting: A Reproducible Comparison of Models and Data-Preprocessing
Strategies on Apple and Bitcoin

**Status:** SKELETON. Sections marked `PENDING ARTIFACT` must not be filled with
plausible-sounding numbers; they must wait for the artifact or be deleted.

**Word-count policy**

| Source | Limit | Tag |
|---|---|---|
| Written specification | ≤ 2,000 words | `[A]` |
| Instructor oral guidance | ~+500 permitted | `[B]` reported by the owner, **not published** |
| Practical planning allowance | ~2,500 words | working target |

Track actual counts in §10. Do not silently exceed the allowance, and do not
claim the 2,000-word rule was removed.

> Every figure, number and conclusion carries `[run: …]` provenance. A sentence
> with no artifact behind it does not belong in Results or Discussion.

---

## Abstract (~150 words) — PENDING

Must state: the educational problem, the two assets, the controlled comparison,
the headline finding (models do not meaningfully beat persistence), and the
explicit non-advisory caveat. No claim of learning gains.

## 1. Introduction and educational problem (~350 words) — DRAFTABLE NOW

Content available from `docs/education/lesson_plan.md` §1 and the requirements
matrix. Must state *why* forecasting is a good teaching vehicle: it makes
generalisation, leakage and baseline comparison concrete.

## 2. Theoretical background (~300 words) — DRAFTABLE NOW

- The five model families and what each learns
  (`docs/research/protocol.md` §5; `.pi/agents/int-model-builder.md` notes).
- Why scaling matters for kernels and not trees
  (`artifacts/figures/fig06_ablation_delta.png`).
- Why naive persistence is a strong baseline (notebook §8 Example C).

## 3. Research questions and design (~300 words) — DRAFTABLE NOW

RQ1–RQ4 from `docs/research/protocol.md` §1; hypotheses H1–H5 from §2; target
representation decision D8; the purge (D9).

## 4. Data and preprocessing (~350 words) — DRAFTABLE NOW

From the two dataset cards: provenance, row counts, date ranges, calendars, the
raw-vs-adjusted decision (D1/D4), the ten causal features, the chronological split
and the boundary purge. Figures: `fig01`.

## 5. Models, tuning and baselines (~250 words) — DRAFTABLE NOW

Table of families, budgets (`max_trials`, `max_seconds`), CV scheme, and the
statement that tuning never touched validation or test.

## 6. Evaluation method (~200 words) — DRAFTABLE NOW

MAE, RMSE, R² and skill relative to persistence; why raw dollar errors are not
comparable across assets; the moving-block bootstrap caveat.

## 7. Results (~450 words) — BLOCKED ON ANALYSIS FREEZE

Available now (validation only, 20 runs):

| Model | AAPL skill_MAE (P2) | BTC skill_MAE (P2) |
|---|---:|---:|
| `svr` | +0.52% | +0.08% |
| `ridge` | +0.29% | +0.12% |
| `hist_gradient_boosting` | +0.25% | −0.04% |
| `random_forest` | −0.78% | +0.06% |
| `linear_baseline` | −0.50% | +0.05% |

Source: `docs/research/run_registry.md` `[run: 20 SUCCESS runs]`.
Figures: `fig04`, `fig03`, `fig05`.

**Test set: sealed.** No test metrics exist. This section must say so rather than
imply a held-out result.

## 8. Preprocessing deep dive (RQ3) (~400 words) — DRAFTABLE NOW

P0→P2 deltas per model per asset (`fig06`). Key finding: trees exactly invariant
(0.0000%), linear/kernel models move slightly and sometimes get worse. P1 is
`NOT_RUN` because the snapshots contain no missing values (D13) — say this
explicitly instead of hiding the gap.

**Pending:** P3 (reduced feature set) and P4 (robust scaling) cells are scheduled
but not yet run. Mark as `PENDING`, do not describe results.

## 9. Educational design (~350 words) — DRAFTABLE NOW

From `docs/education/` — objectives O1–O5, three worked examples with run IDs, and
five formative tasks. Must be phrased as a **designed resource**; no learner study
was conducted.

## 10. Limitations, ethics and conclusion (~350 words) — DRAFTABLE NOW

Limitations: two assets, one window, one horizon, no transaction costs, BTC is a
single-venue USDT price, test block sealed as of writing, no learner study.
Ethics: historical, educational, non-advisory. AI-use acknowledgement in §12.

---

## 11. Figures and tables — map

| Item | Caption source | Run IDs | Script |
|---|---|---|---|
| fig01 coverage and splits | `.caption.txt` beside the PNG | dataset-level | `int4096.evaluation.figures` |
| fig03 observed vs predicted | same | one run | same |
| fig04 model vs naive | same | all SUCCESS runs | same |
| fig05 validation MAE by lane | same | all SUCCESS runs | same |
| fig06 ablation delta | same | matched P0/P2 pairs | same |
| Table 1 dataset summary | `docs/research/data_cards/*.md` | dataset-level | `int4096.data.cards` |
| Table 2 hyperparameters | `artifacts/experiments/*/config.json` | per run | `int4096.experiments.run` |
| Table 3 results | `docs/research/run_registry.md` | all runs | `int4096.experiments.registry_report` |

## 12. AI-use and contribution acknowledgement — DRAFT

This project used an AI coding agent (Pi with the `pi-subagents` extension) as a
development tool: drafting code, tests and documentation under a frozen protocol.
All model lanes were reviewed and are presented by their named human owners, who
are accountable for their content. An independent automated leakage audit was run
against the pipeline; it found two HIGH-severity defects (unpurged split
boundaries, and a leakage test suite unable to detect a one-bar look-ahead), both
of which were fixed and are recorded in `docs/quality/leakage_audit.md`.
Contribution statement per member: see
`docs/management/responsibilities.md` (to be finalised by the group).

## 13. References — PENDING

Must include: the course specification, scikit-learn documentation for each
estimator, the data providers' documentation, and the methodological sources
actually relied on for time-series CV and leakage. **No citation may be added
without opening it and recording the access date** (`int-scout` source register).

---

## 14. Word count tracking

| Section | Target | Current | Notes |
|---|---:|---:|---|
| Abstract | 150 | 0 | PENDING |
| 1 Introduction | 350 | 0 | draftable |
| 2 Background | 300 | 0 | draftable |
| 3 RQs and design | 300 | 0 | draftable |
| 4 Data | 350 | 0 | draftable |
| 5 Models | 250 | 0 | draftable |
| 6 Evaluation | 200 | 0 | draftable |
| 7 Results | 450 | 0 | blocked on analysis freeze |
| 8 Ablation | 400 | 0 | draftable (P3/P4 pending) |
| 9 Education | 350 | 0 | draftable |
| 10 Limitations | 350 | 0 | draftable |
| **Total** | **3,450** | **0** | **exceeds the ~2,500 allowance — must be cut** |

**Note the honest problem:** the target allocation above sums to ~3,450 words,
which exceeds the ~2,500 practical allowance. Either the section targets shrink or
detail moves into figures/tables. This must be resolved *before* drafting, not by
silently overshooting. `int-report-editor` should produce a revised allocation
that fits the allowance and record the cut decisions here.
