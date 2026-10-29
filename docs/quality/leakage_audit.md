# Leakage Audit Record

Independent, adversarial audit of the temporal integrity of the INT4096 pipeline.
The auditor (`int-leakage-auditor`) did not write the code it audited and was
required to produce a reproducible demonstration for each finding.

**Audit #1 verdict: FAIL** (2 HIGH, 4 MEDIUM, 4 LOW; no BLOCKER).
**Retest status: see §3.** Gate G1/G4 sign-off remains withheld until the
retest is executed by an independent context.

---

## 1. Method

The auditor traced the prediction timestamp end to end:

raw provider payload → snapshot → canonical frame → feature construction →
label shift → split boundaries → preprocessing fit → CV folds → tuning objective
→ reported metrics.

It was required to inspect code and **run** probes, not to accept comments or
docstrings as evidence.

---

## 2. Findings

### LEAK-001 — HIGH — outer split boundaries not purged

**Where:** `src/int4096/data/split.py`, `src/int4096/experiments/run.py`,
`configs/research_protocol.yaml`.

**Issue:** with `y_t = Close_{t+1}`, the last training row's label is a
validation-block price and the last validation row's label is a **sealed test
price**. The config key `validation_horizon_gap: 0` existed but was never read by
any code, so no purge was implementable.

**Reproduction (auditor):** perturbing a single sealed test price changed the
headline validation metric by **0.408**, ≈46× the reported model-vs-persistence
margin. The committed `predictions.csv` last validation row had
`y_true = 270.14`, equal to `Close[2025-11-05]` — the first bar of the sealed
test block — while `manifest.test_period` was empty.

**Fix (D9):** `purge_gap: 1` is now read from the protocol and applied at both
boundaries; the affected rows are dropped from both blocks. Regression tests:
`test_split_purge_gap_prevents_label_crossing`,
`test_split_purge_gap_zero_is_explicit_opt_in`.

**Status:** FIXED, pending independent retest.

### LEAK-002 — HIGH — the leakage suite could not detect canonical defects

**Where:** `tests/test_temporal_integrity.py`.

**Issue:** mutation testing showed a one-bar `shift(-1)` and a `bfill` both
survived the entire file. `test_no_backward_fill_in_features` asserted
`isnan(v) or isfinite(v)` — a tautology. The scaler test imported sklearn
directly and never exercised project code.

**Reproduction (auditor):**

```
=== mutation: shift   -> 17 passed
=== mutation: bfill   -> 17 passed
```

**Fix (D10):**

1. `test_features_match_independent_trailing_formulas` recomputes every feature
   from raw data with trailing-only formulas **in the test itself**. A one-bar
   look-ahead now mismatches.
2. The tautology was replaced with a real forward-fill vs backward-fill
   discrimination.
3. The scaler test now calls `build_variant_matrix` (project code).
4. A static guard scans feature functions for forbidden constructs.
5. `scripts/mutation_check.py` injects five defect classes and asserts the suite
   catches each one.

**Verification actually executed:**

```
$ python scripts/mutation_check.py
baseline: PASS (23 passed)
CAUGHT    features read the next bar (shift(-1))
CAUGHT    centred rolling window
CAUGHT    backward fill of missing inputs
CAUGHT    whole-series statistic instead of trailing window
CAUGHT    preprocessing fitted on train+apply rows
PASS: all 5 injected defects were detected.
```

**Status:** FIXED and verified by mutation testing.

### LEAK-003 — MEDIUM — snapshot hash recorded but never verified

**Where:** `src/int4096/experiments/run.py`.

**Issue:** the manifest recorded `source_snapshot_sha256` from the sidecar but no
code compared it with the bytes actually loaded, so a tampered snapshot would run
under a stale, "reproducible-looking" hash.

**Fix (D11):** `run_cell` recomputes the SHA256 and raises on mismatch.
**Status:** FIXED.

### LEAK-004 — MEDIUM — tuning stage mislabelled

**Where:** `src/int4096/experiments/run.py`, `docs/research/protocol.md`.

**Issue:** hyperparameter search ran on expanding-window folds **inside the
train block**, while the protocol text said "inside train+validation". Trial
scores were also stored under a `validation_mae` key, implying they came from the
validation block.

**Fix:** the protocol text now states train-block-only CV (which is the stricter,
implemented behaviour and keeps validation a genuine selection holdout), and trial
records carry `"stage": "inner_cv_train_block"`.
**Status:** FIXED.

### LEAK-005 — MEDIUM — P1 ablation was a structural no-op

**Where:** `src/int4096/features/pipeline.py`.

**Issue:** with no missing inputs the P1 imputer changed nothing, so P1 would have
been byte-identical to P0 while appearing as a separate result.

**Fix (D13):** genuine missingness indicators are implemented, and
`variant_is_applicable` reports P1 as `NOT_RUN` with an explicit reason when the
snapshot has no missing values. No synthetic NaNs are injected.
**Status:** FIXED.

### LEAK-006 — MEDIUM — protocol version drift

**Where:** `docs/research/protocol.md` vs `configs/research_protocol.yaml`.

**Issue:** the config said `v1.1-delta-target` while the prose still said
`v1.0-draft`, and the `label_mode: delta` change had no decision-log entry.

**Fix (D8):** protocol prose updated to `v1.1-delta-target` with a change-history
table; decision D8 records the rationale, alternatives and the approval request.
**Status:** FIXED.

### LEAK-007 — LOW — session keys are dates, not wall-clock instants

**Issue:** an AAPL bar closes at 16:00 America/New_York but is indexed at 00:00
UTC, up to ~21h earlier.

**Resolution (D12):** the index is a **session key**, not a claim about wall-clock
time. Features, labels and the shift relationship depend only on ordering,
uniqueness and `t → t+1`, all of which are tested. Wall-clock instants would be
more misleading because they would imply AAPL and BTC share a timeline.
Documented in the protocol and dataset cards. **Accepted, with residual risk
noted for any future intra-day extension.**

### LEAK-008 — LOW — reproduction commands referenced missing files

**Fix:** `pyproject.toml`, `requirements.txt`, `scripts/reproduce.sh`, `README.md`
and the Colab notebook now exist. **Status:** FIXED.

### LEAK-009 — LOW — `run_cell` cannot write outside the repo root

**Resolution:** artifacts are required to live under the repository so that
manifests can store relative paths and remain portable. An external output root
is now supported but recorded as an explicit warning
(`explicit snapshot path supplied: metrics are not comparable...`).
**Status:** ACCEPTED (documented limitation).

### LEAK-010 — LOW — partial windows in rolling statistics

**Issue:** `min_periods=5` on 10- and 30-bar windows meant `vol_30` could be
computed from 5 observations while being documented as a 30-observation window.

**Fix:** rolling statistics now require a **full window** (`min_periods =
window`), and the protocol says so explicitly. Behaviour is unchanged for the
rows that survive the 30-row warm-up, but the definition is now accurate.
**Status:** FIXED.

---

## 3. Retest checklist (must be executed by an independent context)

| Finding | Retest action | Expected evidence |
|---|---|---|
| LEAK-001 | Perturb one sealed test price; rerun a validation cell | Validation metrics unchanged |
| LEAK-001 | Inspect manifest periods | `validation_period` ends before `test_period` starts, with a 1-row hole |
| LEAK-002 | `python scripts/mutation_check.py` | All 5 mutations caught, exit 0 |
| LEAK-003 | Corrupt one byte of a snapshot; run a cell | Run raises `Snapshot integrity failure` |
| LEAK-004 | Inspect `fold_metrics[*].stage` | `inner_cv_train_block` |
| LEAK-005 | Run variant P1 | Status `NOT_RUN` with reason |
| LEAK-006 | Compare config and prose versions | Both `v1.1-delta-target` |

**Current status:** the coordinator executed each of these locally (§4 records the
observed output), but a **coordinator retest is not an independent retest**. The
gate stays PENDING until an auditor context reproduces them.

## 4. Coordinator-side verification already observed

```
$ python -m pytest -q                      -> 75 passed
$ python scripts/mutation_check.py         -> PASS: all 5 injected defects detected
$ variant P1 run                           -> status NOT_RUN (no missing inputs)
$ snapshot hash check                      -> enforced in run_cell
```

These are recorded as *self-checks*, not as audit sign-off.

## 5. Attacks that did not succeed (from audit #1)

Future-append invariance (bit-exact), whole-column contamination, scaler fitted
on validation/test (identical `mean_`/`scale_`), sealed-block poisoning during
tuning (identical CV scores), label-in-X, terminal-row/label alignment,
cross-asset row alignment (disjoint calendars), shuffled splits (none present),
CV fold purge inside training, and committed-artifact seal integrity (all
committed `test_*` metrics null).

A suite that has never been attacked is not evidence. This section is what makes
the eventual PASS meaningful.
