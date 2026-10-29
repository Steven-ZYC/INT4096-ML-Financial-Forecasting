# Decision Log

Append-only record of scientific and engineering decisions. Each entry has a
date, a proposer, the alternatives considered, the trade-off, the affected
configuration, and whether human approval is required.

**Rules**

- Never delete or rewrite an entry. If a decision changes, add a new entry that
  supersedes it and reference the old ID.
- An entry marked `REQUIRES HUMAN APPROVAL` is a request, not an approval. The
  project must not treat it as settled until the owner signs it.
- Decisions that change the primary research question, label, dataset, primary
  metric or split **must** be approved by the human owner.

---

## D1 — Label uses raw close, not adjusted close

- **Date:** 2026-10-29
- **Proposer:** `int-methodologist`
- **Status:** Accepted (provisional pending owner confirmation)
- **Choice:** `Close_{t+1}` from the **raw** close series.
- **Alternatives:** (a) adjusted close; (b) total-return series.
- **Rationale:** Adjusted prices embed dividend and split factors that the
  provider revises retroactively. A model trained today on adjusted history sees
  values that were not observable at the original decision time — a subtle
  leakage channel. Raw close avoids it. The 2021-10-28..2026-10-28 window was
  checked for splits (max adjustment-ratio jump < 2%, no split discontinuity),
  so raw close is continuous within the window.
- **Trade-off:** Dividends are ignored, so the series understates total return.
  Irrelevant for a next-session *price* prediction task, which is the stated
  question.
- **Affects:** `label_field`, all runs.
- **Requires human approval:** Yes — confirm the raw-close convention, or
  request an adjusted-close sensitivity check.

## D2 — Shallow MLP lane is excluded by default

- **Date:** 2026-10-29
- **Proposer:** `int-methodologist`
- **Status:** **Pending human approval** (blocking for that lane only)
- **Choice:** Do not include a neural lane until the owner records the oral
  instructor guidance.
- **Alternatives:** (a) small MLP over engineered features; (b) LSTM over raw
  sequences; (c) omit neural models entirely.
- **Rationale:** The written handout discourages deep learning; the instructor
  reportedly said it could be considered if necessary. That is `[B]` reported
  guidance, not a published rule change, so it must be documented rather than
  assumed. A five-person project with a ~2,500-word report also has limited
  capacity to justify and evaluate an extra family.
- **Note:** `src/int4096/models/mlp.py` exists and is gated with
  `REQUIRES_OWNER_APPROVAL = True`. Enabling it without approval would be a
  process violation, not a technical one.
- **Affects:** model lineup, `configs/research_protocol.yaml#models.mlp`.
- **Requires human approval:** Yes.

## D3 — Binance BTCUSDT accepted as the BTC series, with stated caveats

- **Date:** 2026-10-29
- **Proposer:** `int-data-steward`
- **Status:** Accepted (provisional)
- **Choice:** Binance `BTCUSDT` daily klines, 2021-10-28 onwards.
- **Alternatives:** CoinGecko aggregate index; a paid consolidated feed.
- **Rationale:** Public, well documented, complete daily coverage (no gaps > 1
  day in the snapshot), reproducible pagination.
- **Caveats that must appear in the report:** USDT is not exactly USD; Binance
  is a single venue, so this is a venue-specific price, not a global index.
- **Affects:** BTC dataset card, results discussion.
- **Requires human approval:** Yes — accept the proxy, or request an aggregate.

## D4 — No AAPL split inside the analysis window

- **Date:** 2026-10-29
- **Proposer:** `int-data-steward`
- **Status:** Accepted (evidence-based)
- **Evidence:** Over 2021-10-28..2026-10-28 the adjusted/raw close ratio shows no
  jump larger than 2%; all 1,198 differences are dividend drift. A split would
  produce a single-day ratio jump near 4x or 7x.
- **Consequence:** Raw close can be used without split discontinuity.
- **Reproduce:** see `docs/research/data_cards/aapl_dataset_card.md` §5 and the
  ratio check in the data card generator.
- **Requires human approval:** No.

## D5 — Appendices must be assumed to count toward the word limit

- **Date:** 2026-10-29
- **Proposer:** `int-report-editor`
- **Status:** **Pending human approval**
- **Choice:** Plan the report so that the core argument fits in ~2,500 words,
  and do not rely on appendices being excluded.
- **Rationale:** The specification states 2,000 words; the instructor reportedly
  permitted ~500 more. No source confirms how appendices are counted. Assuming
  the optimistic interpretation risks a penalty.
- **Requires human approval:** Yes — confirm with the instructor/course page.

## D6 — Plan for the earlier presentation slot

- **Date:** 2026-10-29
- **Proposer:** `int-report-editor`
- **Status:** **Pending human approval**
- **Choice:** Target readiness for 19 November even if the assigned slot is 26
  November.
- **Rationale:** The draft is due 18 November 18:00 either way; preparing for the
  earlier date removes schedule risk.
- **Requires human approval:** Yes — confirm the assigned slot.

## D7 — Single test-set release, target 2026-11-14

- **Date:** 2026-10-29
- **Proposer:** `int-methodologist`
- **Status:** **Pending human approval**
- **Choice:** One `allow_test=True` run per final cell, executed only after the
  analysis is frozen, with the release recorded here.
- **Rationale:** Repeated unblinding turns a held-out estimate into a tuned one.
  One release keeps the test block a genuine holdout.
- **Requires human approval:** Yes — this is a grade-sensitive, irreversible step.

## D8 — Train on the price change (delta), report error on the price level

- **Date:** 2026-10-29
- **Proposer:** `int-methodologist` (after a failed baseline run)
- **Status:** Accepted provisionally; **requires human approval**
- **Trigger:** The first real AAPL run gave `skill_MAE = -18.3` and R² ≈ -7.4 for
  Ridge. Investigation showed this was a *representation* artefact, not a model
  failure: every feature is scale-free (returns, gaps, ratios), so no model can
  recover a price *level* and every regressor collapses toward the training-set
  mean (predicted range 100–205 while the target range was 172–271).
- **Choice:** Fit `y_t = Close_{t+1} - Close_t` (`label_mode: delta`) and
  reconstruct the forecast as `Close_t + predicted_delta`. Metrics remain error
  on the **next close price**, so the reported question is unchanged.
- **Alternatives considered:**
  (a) keep level-targeting and report the large negative skill — honest but it
  measures the representation, not the model, and would mislead the reader about
  model behaviour;
  (b) add `Close_t` as a feature — legitimate at decision time but it hands the
  model the answer to the level, making the comparison trivial;
  (c) delta-targeting — chosen.
- **Why this is not a change of research question:** `Close_t` is known at the
  decision time, so "predict the level" and "predict the change from a known
  level" are information-equivalent. Every model is treated identically, and the
  naive baseline becomes `delta = 0`, i.e. the same persistence baseline as
  before.
- **Supersedes:** nothing (the estimand is unchanged); it supersedes the
  *implementation* of the label.
- **Affects:** `configs/research_protocol.yaml#label_mode`, `features.build`,
  `experiments.run`, all runs. Protocol bumped `v1.0-draft` -> `v1.1-delta-target`.
- **Requires human approval:** Yes — confirm that delta-targeting with level
  reporting is the intended comparison. If not, reverting is a one-line config
  change and the level-mode results remain reproducible.

## D9 — Purge one boundary row per split

- **Date:** 2026-10-29
- **Proposer:** `int-leakage-auditor` (audit finding LEAK-001), implemented by the
  coordinator
- **Status:** Accepted and implemented
- **Problem:** With `y_t = Close_{t+1}`, the last training row's label is a
  validation-block price, and the last validation row's label is a **sealed test
  price**. The auditor demonstrated that perturbing one test price changed the
  headline validation metric by 0.408 — about 46x the reported model-vs-baseline
  margin.
- **Choice:** `purge_gap: 1` at both boundaries. The affected rows are dropped
  from both blocks rather than reassigned.
- **Cost:** Two rows out of ~1,224. Negligible.
- **Affects:** `splits.purge_gap`, `data/split.py`, all runs.
- **Requires human approval:** No — this is a correctness fix, not a design change.

## D10 — Strengthen the leakage suite with independent formula checks

- **Date:** 2026-10-29
- **Proposer:** `int-leakage-auditor` (finding LEAK-002), implemented by the
  coordinator
- **Status:** Accepted and implemented
- **Problem:** Mutation testing showed that a one-bar `shift(-1)` and a `bfill`
  both survived the original suite. One test was a tautology
  (`isnan(v) or isfinite(v)`); the scaler test exercised sklearn rather than the
  project pipeline.
- **Choice:** Add `test_features_match_independent_trailing_formulas`, which
  recomputes every feature from raw data with trailing-only formulas in the test
  itself; replace the tautology with a real forward-fill/backward-fill
  discrimination; rewrite the scaler test to call `build_variant_matrix`; add a
  static guard scoped to feature functions; add `scripts/mutation_check.py` so
  the suite's ability to fail is itself verifiable evidence.
- **Result:** 5/5 injected defects detected. Recorded in
  `docs/quality/leakage_audit.md`.
- **Requires human approval:** No.

## D11 — Verify the snapshot hash before every run

- **Date:** 2026-10-29
- **Proposer:** `int-leakage-auditor` (finding LEAK-003)
- **Status:** Accepted and implemented
- **Problem:** The manifest recorded a SHA256 that was never checked, so a
  tampered snapshot would have loaded with a stale hash and looked reproducible.
- **Choice:** `run_cell` recomputes the hash from disk and raises on mismatch.
- **Requires human approval:** No.

## D12 — Session labels are dates, not instants; as-of time is the venue close

- **Date:** 2026-10-29
- **Proposer:** `int-leakage-auditor` (finding LEAK-007), resolved by the
  coordinator
- **Status:** Accepted, documented rather than restructured
- **Problem:** The index stores each daily bar at 00:00 UTC, while an AAPL bar
  actually closes at 16:00 America/New_York (20:00/21:00 UTC). The stored
  timestamp therefore precedes the true as-of instant by up to ~21 hours.
- **Why it is not a leak:** every feature and label for row `t` uses only the bar
  labelled `t`; the index is a *session key*, not a claim about wall-clock time.
  Ordering, uniqueness and the shift relationship are what the model relies on,
  and all three are tested.
- **Choice:** Keep date-based session keys (they make the AAPL/BTC calendars
  explicit and prevent accidental row-wise alignment), and document the as-of
  convention in the protocol and dataset cards. A wall-clock instant would be
  *more* misleading, because it would suggest the two assets share a timeline.
- **Residual risk:** Any future intra-day extension must switch to true instants.
- **Requires human approval:** No.

## D13 — P1 ablation is reported as NOT_RUN when there is no missingness

- **Date:** 2026-10-29
- **Proposer:** `int-leakage-auditor` (finding LEAK-005)
- **Status:** Accepted and implemented
- **Problem:** With zero missing inputs, the P1 imputer is a structural no-op, so
  P1 would have been byte-identical to P0 while appearing to be a separate
  result.
- **Choice:** Implement genuine missingness indicators; when the snapshot has no
  missing inputs, record P1 as `NOT_RUN` with the reason
  `no missing inputs in snapshot` instead of publishing a duplicate cell. We do
  **not** inject synthetic NaNs into the main matrix.
- **Requires human approval:** No.
