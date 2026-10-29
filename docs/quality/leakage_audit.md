# Leakage Audit Record

Independent, adversarial audit of the temporal integrity of the INT4096 pipeline.
The auditor (`int-leakage-auditor`) did not write the code it audited and was
required to produce a reproducible demonstration for each finding.

**Audit #1 verdict: FAIL** (2 HIGH, 4 MEDIUM, 4 LOW; no BLOCKER).
**Audit #2 (independent retest) verdict: PASS** on both HIGH findings, with no
new leak introduced. Five further hardening findings (3 MEDIUM, 2 LOW) were
raised and have since been fixed — see §6.

The auditor that produced audit #2 was a separate subagent context with no
knowledge of the coordinator's edits; it re-derived the split boundaries through
the production `prepare_dataset` path and wrote its own mutations.

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

## 3. Audit #2 — independent retest result

**Verdict: PASS.** Reproduced by the auditor, not accepted on the coordinator's word:

- **LEAK-001 FIXED.** `purge_gap: 1` flows `config → Protocol.purge_gap →
  chronological_split(horizon_gap=1)`. Recomputed through `prepare_dataset` on
  both assets:

  | Asset | last train label bar | validation starts | last validation label bar | test starts |
  |---|---|---|---|---|
  | AAPL | 2024-11-11 | 2024-11-12 | 2025-11-04 | 2025-11-05 |
  | BTC | 2024-11-08 | 2024-11-09 | 2025-11-02 | 2025-11-03 |

  In both assets the last label bar of a block is strictly before the next block.

- **LEAK-002 FIXED.** The suite is green and `scripts/mutation_check.py` reports
  6/6 caught. The auditor additionally wrote **two guard-blind mutations** — an
  obfuscated `shift(periods=-1)` containing no literal `shift(-`, and a
  matrix-level shift inside a function the static grep never inspects. **Both were
  caught by the numeric test alone**, proving detection is behavioural rather
  than pattern-matching. This was the specific weakness of the first fix, and it
  is now closed.

- **No new leak** at BLOCKER/HIGH. Target alignment verified (y_true equals
  `Close[t+1]` on 244/244 AAPL and 358/358 BTC rows); the sealed test block is
  untouched. The auditor confirmed its temporary mutations were reverted
  byte-for-byte.

## 4. Findings raised by audit #2

| ID | Severity | Issue | Fix | Status |
|---|---|---|---|---|
| LEAK-011 | MEDIUM | `purge_gap` and `cv.gap` were hard-coded at 1 with no invariant binding them to `label_horizon`; raising the horizon would silently restore LEAK-001 | `Protocol.validate()` enforces `purge_gap >= horizon` and `cv.gap >= horizon` at load time; `label_horizon` added to the config | FIXED |
| LEAK-012 | MEDIUM | The purge test used a literal `1`, so `purge_gap: 0` in the YAML would still pass | `test_protocol_purge_is_at_least_the_label_horizon` reads the YAML; `test_protocol_rejects_an_insufficient_purge`; `test_real_split_honours_the_configured_purge` | FIXED |
| LEAK-013 | MEDIUM | No test covered the runner's slicing, so a leak in `fit`/tuning inputs would survive the suite | `test_runner_fits_and_tunes_on_training_rows_only` instruments `build_estimator` and asserts every fitted row index is before `validation_start` | FIXED |
| LEAK-014 | LOW | `mutation_check.py` did not verify its restore and had no guard-blind mutation | Restore is verified by SHA-256 and fails closed; an obfuscated `shift(periods=-1)` mutation was added (6 mutations total) | FIXED |
| LEAK-015 | LOW | Tracked `__pycache__/*.pyc` files dirtied every audit diff | Removed from the index; `__pycache__/` already ignored | FIXED |

Verification that LEAK-013's test is not vacuous: mutating `run_cell` to fit on
`train + validation` makes it fail; restoring the code makes it pass.

## 5. Retest checklist (originally required; now satisfied for HIGH findings)

| Finding | Retest action | Expected evidence |
|---|---|---|
| LEAK-001 | Perturb one sealed test price; rerun a validation cell | Validation metrics unchanged |
| LEAK-001 | Inspect manifest periods | `validation_period` ends before `test_period` starts, with a 1-row hole |
| LEAK-002 | `python scripts/mutation_check.py` | All 5 mutations caught, exit 0 |
| LEAK-003 | Corrupt one byte of a snapshot; run a cell | Run raises `Snapshot integrity failure` |
| LEAK-004 | Inspect `fold_metrics[*].stage` | `inner_cv_train_block` |
| LEAK-005 | Run variant P1 | Status `NOT_RUN` with reason |
| LEAK-006 | Compare config and prose versions | Both `v1.1-delta-target` |

**Current status:** executed by the coordinator (§7) **and** independently
reproduced by the auditor in audit #2 (§3) for every HIGH finding. G4's audit
condition is therefore satisfied; the remaining G4 item is the analysis freeze
and the single test-set release (D7), which is a human decision.

## 6. Attacks that did not succeed (from audit #1)

Future-append invariance (bit-exact), whole-column contamination, scaler fitted
on validation/test (identical `mean_`/`scale_`), sealed-block poisoning during
tuning (identical CV scores), label-in-X, terminal-row/label alignment,
cross-asset row alignment (disjoint calendars), shuffled splits (none present),
CV fold purge inside training, and committed-artifact seal integrity (all
committed `test_*` metrics null).

A suite that has never been attacked is not evidence. This section is what makes
the eventual PASS meaningful.


## 7. Coordinator-side verification already observed

```
$ python -m pytest -q                      -> 83 passed
$ python scripts/mutation_check.py         -> PASS: all 6 injected defects detected
$ variant P1 run                           -> status NOT_RUN (no missing inputs)
$ snapshot hash check                      -> enforced in run_cell
$ python scripts/verify_fixes.py           -> PASS: 8 probes
```

These are recorded as *self-checks*. Sign-off came separately, from audit #2 (§3).
