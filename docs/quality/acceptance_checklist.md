# Acceptance Checklist — Gates G0–G7

Each gate is `PASS`, `FAIL` or `PENDING` **with a verifiable evidence path**.
A failed gate blocks any downstream "completed" claim, even though development
can continue.

**Last updated:** 2026-10-29 (Asia/Hong_Kong)
**Protocol:** `v1.1-delta-target`
**Test status at last run:** 83 passed

Legend: `PASS` = evidence exists and was executed · `PENDING` = blocked on a
human decision or an independent retest · `FAIL` = known defect.

---

## G0 — Architecture and requirements

| Item | Status | Evidence |
|---|---|---|
| 10 project agent definitions with valid frontmatter | PASS | `.pi/agents/*.md`; discovery verified by `int-scout` |
| Coordinator contract + source-of-truth hierarchy | PASS | `AGENTS.md` |
| Dispatch contract and acceptance format | PASS | `.pi/prompts/dispatch.md` |
| `pi-subagents` installed, version-pinned, compatible | PASS | `pi install npm:pi-subagents@0.84.0`; Pi 1.4.0 ≥ required 1.2.0 |
| Real read-only delegation | PASS | `int-scout` returned all 10 agent names |
| Real bounded write delegation | PASS | all `src/`, `tests/`, `scripts/` produced by bounded lanes |
| Real independent review delegation | PASS | `int-leakage-auditor` run; returned FAIL with 10 findings — see `docs/quality/leakage_audit.md` |
| Requirements matrix with weights and provenance tags | PASS | `docs/course/course_requirements.md` |
| **Official course specification archived** | **PENDING** | `docs/course/` is empty; needs the real PDF |

## G1 — Data and temporal integrity

| Item | Status | Evidence |
|---|---|---|
| Immutable snapshots with SHA-256 manifests | PASS | `data/raw/{aapl,btc}_daily.json` + `.manifest.json` |
| Hash verified before every run | PASS | `run_cell` raises on mismatch; probe `LEAK-003` |
| Dataset cards generated from data (not typed) | PASS | `data/cards/*.md` via `int4096.data.cards` |
| Data quality checks on both assets | PASS | both `PASS`; 0 non-positive prices, 0 high<low, 0 missing core values |
| Chronological split with frozen boundaries | PASS | `configs/research_protocol.yaml#splits` |
| Boundary purge (no label crosses a split) | PASS | `purge_gap: 1`; `test_split_purge_gap_prevents_label_crossing` |
| Causal features, no future information | PASS | `test_features_match_independent_trailing_formulas` |
| Leakage suite proven able to fail | PASS | `scripts/mutation_check.py` → 5/5 caught |
| Independent leakage audit PASS | **PASS** | audit #1 returned FAIL; all findings fixed; audit #2 (separate context) returned PASS — `docs/quality/leakage_audit.md` §3 |
| Leakage suite proven able to fail | PASS | `scripts/mutation_check.py` → 6/6 caught, restores SHA-256 verified |
| Runner slicing covered by a test | PASS | `test_runner_fits_and_tunes_on_training_rows_only` (fails when `fit` is given validation rows) |

## G2 — Executable baseline

| Item | Status | Evidence |
|---|---|---|
| Naive persistence produces metrics from a real run | PASS | registry rows for `linear_baseline` / all models carry `baseline_mae` |
| Baseline aligned to the same forecast dates | PASS | `predictions.csv` has `y_true`, `y_pred`, `y_naive` per row |
| Run manifest with git commit, data hash, protocol, seed | PASS | `experiments/models/*/manifest.json` |
| Metrics cross-checked against hand-computed values | PASS | `test_mae_rmse_r2_on_hand_computed_values` |
| Failed runs recorded as FAILED, not deleted | PASS | registry is append-only; a `FAILED` linear_baseline row exists from an earlier interface bug (since fixed) |

## G3 — Model fairness

| Item | Status | Evidence |
|---|---|---|
| Identical features, split, target, metric per asset | PASS | `test_lane_receives_identical_columns` (parametrised over all lanes) |
| Identical tuning budget | PASS | `max_trials`/`max_seconds` read from the protocol for every lane |
| Deterministic given a seed | PASS | `test_lane_is_deterministic_for_a_fixed_seed`; probe `REPRO` |
| Every attempted trial logged, including failures | PASS | `manifest.fold_metrics[*]` with `stage: inner_cv_train_block` |
| Test set never used for tuning | PASS | `allow_test=False` by default; no run has `test_*` metrics |
| Optional `mlp` lane gated | PASS | `mlp.REQUIRES_OWNER_APPROVAL = True`; decision D2 |

## G4 — Research integrity

| Item | Status | Evidence |
|---|---|---|
| Comparison and ablation are separate experiments | PASS | main matrix (P0/P2) vs ablation contrast in `fig06` |
| Metric implementation verified | PASS | 10 metric tests incl. hand-computed MAE/RMSE/R² |
| Uncertainty caveat stated | PASS | bootstrap implemented; `protocol.md` §7.3 |
| Preprocessing ablation matched, one factor at a time | PASS | `fig06`; trees as negative control |
| P1 not published as a duplicate cell | PASS | status `NOT_RUN` with reason (D13) |
| Independent leakage retest | PASS | audit #2, `docs/quality/leakage_audit.md` §3 |
| Protocol invariants enforced at load time | PASS | `Protocol.validate()`: `purge_gap >= label_horizon`, `cv.gap >= label_horizon` |
| Hardening findings LEAK-011..015 closed | PASS | `docs/quality/leakage_audit.md` §4 |

## G5 — Education

| Item | Status | Evidence |
|---|---|---|
| Learning objectives written and measurable | PASS | `deliverables/lesson/lesson_plan.md` |
| Objectives mapped to real artifacts with run IDs | PASS | `deliverables/lesson/lesson_plan.md` §3 |
| ≥3 formative tasks with worked answers | PASS | `deliverables/lesson/formative_tasks.md` (5 tasks) |
| Teacher notes on misconceptions | PASS | `deliverables/lesson/teacher_notes.md` |
| No fabricated learning-gain claim | PASS | statements are design statements, explicitly labelled |
| Non-financial-advice disclaimer present | PASS | lesson plan, notebook, README, report |

## G6 — External reproducibility

| Item | Status | Evidence |
|---|---|---|
| One-command reproduction script | PASS | `scripts/reproduce.sh` |
| Pinned dependency set | PASS | `requirements.txt`, `pyproject.toml` |
| Notebook executes end to end, no cached outputs | PASS | `tests/test_notebook.py` (runs every cell in an empty folder and checks all 20 results match) |
| Notebook has no absolute paths or secrets | PASS | `test_notebook_has_no_hardcoded_absolute_paths` |
| Snapshot hashes match files | PASS | `test_real_snapshot_counts_if_present` |
| Figures regenerated from stored metrics | PASS | `int4096.evaluation.figures` writes `.caption.txt` with run IDs |
| **Independent clean-environment reproduction** | **PENDING** | `int-repro-auditor` not yet run (provider balance constraint) |

## G7 — Academic deliverables

| Item | Status | Evidence |
|---|---|---|
| Report draft with word-count tracking | PENDING | skeleton at `deliverables/report/report_draft.md` |
| Figure map with run IDs | PENDING | will be generated with the report |
| Slide storyboard, 5 speakers ≤20 min | PENDING | plan in `docs/project/responsibilities.md` §4 |
| Original dataset deliverable | PASS | `data/raw/` (normalized snapshots + manifests) |
| Colab notebook deliverable | PASS | `deliverables/notebook/INT4096_Final_Colab.ipynb` |
| AI-use acknowledgement drafted | PENDING | template in `deliverables/report/report_draft.md` §9 |
| Claim audit (every number → artifact) | PENDING | `int-claim-auditor` run required |
| Official specification archived | PENDING | see G0 |

---

## Blocking issues, in priority order

1. **`docs/course/` is empty.** The requirement matrix is a transcription from
   the project owner's brief, not the official PDF. Everything downstream inherits
   that risk. *Owner action required.*
2. **Analysis freeze and the single test-set release (D7)** are human decisions.
   Until they happen, Results cannot report held-out numbers.
3. **Human decisions D1, D2, D5, D6, D7, D8** are unanswered. D8 (delta target)
   is the most consequential: it changed the modelling representation, though not
   the reported question.
4. **Final-test release (D7)** is deliberately not scheduled. No run may unblind
   the test block before it.
5. **Independent clean-environment reproduction** has not been performed by
   `int-repro-auditor`.

## What this checklist does **not** claim

- It does not claim an A-range grade. It claims specific evidence exists.
- It does not claim the results are interesting. They are mostly *negative*:
  no model meaningfully beats persistence — that is the finding.
- It does not claim any educational effectiveness. No learner study was run.
