# Research Protocol — INT4096 Time-Series ML Comparison

**Protocol version:** `v1.1-delta-target`
**Frozen on:** 2026-10-29 (Asia/Hong_Kong)
**Author:** `int-methodologist` (role contract: `.pi/agents/int-methodologist.md`)
**Machine-readable twin:** `configs/research_protocol.yaml`
**Status:** DRAFT — awaiting human sign-off on §10 open decisions before the
first validation sweep is treated as confirmatory.

**Change history**

| Version | Date | Change | Authority |
|---|---|---|---|
| v1.0-draft | 2026-10-29 | Initial protocol | `int-methodologist` |
| v1.1-delta-target | 2026-10-29 | Train on the price change, report error on the price level (D8); purge one boundary row per split (D9); full-window rolling statistics; P1 reported NOT_RUN when no missingness (D13) | Coordinator, after audit LEAK-001/002/005/006/010 |

> Changing anything in §3–§7 requires a `protocol_version` bump, a decision-log
> entry, and human approval. This is what makes the analysis *pre-registered*
> rather than post-hoc.

---

## 1. Research questions

**RQ1 (model comparison).** Under identical, leakage-safe experimental
conditions, how do distinct model families perform against a naive persistence
baseline on AAPL and BTC?

**RQ2 (capacity and regime).** How do model complexity, hyperparameter tuning
and changing market conditions affect generalization and error patterns?

**RQ3 (preprocessing).** To what extent do preprocessing and feature-engineering
choices change forecast error, and does the effect depend on model family and
market?

**RQ4 (education).** What do carefully selected examples and counterexamples
teach learners about ML behaviour, evaluation, limitations and responsible
interpretation? — **Design question.** Answered by artifact design and mapping,
not by a learner study.

## 2. Hypotheses (written before any result was inspected)

| ID | Hypothesis | Falsified if | Test |
|---|---|---|---|
| H1 | Naive persistence will be competitive with, or better than, trained regressors on next-session close prediction. | A trained model beats persistence by a clear, stable margin across folds, using the skill score. | Relative `skill_MAE` per model per asset |
| H2 | AAPL will be more predictable than BTC under equal treatment. | BTC skill/relative error is at least as good as AAPL's. | Within-asset normalized error ranking |
| H3 | Preprocessing changes error more for scaling-sensitive models (SVR, Ridge, MLP) than for scale-invariant trees. | Scaling effect magnitudes are indistinguishable. | P2−P0 deltas per model family |
| H4 | More complex models will show a larger train/validation gap. | Complexity and the gap are uncorrelated. | Train − validation error vs. model capacity rank |
| H5 | Adding lag/rolling features (P3) will change error more than changing the scaler (P2). | Feature ablation is weaker than scaler ablation for most lanes. | P3−P0 vs P2−P0 |

H1 being true is a **scientifically valuable negative result** and does not
reduce the project's quality. We do not select a model to make H1 false.

---

## 3. Data contract

### 3.1 Assets

| Property | AAPL | BTC |
|---|---|---|
| Description | Apple Inc. common stock | Bitcoin / USD |
| Provider | `stockanalysis.com` public history API | Binance public REST klines (`BTCUSDT`) |
| Quote currency | USD | USDT (treated as USD-proxy; **documented caveat**) |
| Calendar | US exchange trading sessions (Mon–Fri, NYSE holidays) | 24/7/365 |
| Bar close | 16:00 America/New_York | 00:00 UTC daily boundary |
| Rows expected | ~1,250 per 5 years (≈252/yr) | ~365 per year |
| Raw close field | `c` (unadjusted) | kline close (unadjusted) |
| Adjusted close | `a` (split/dividend adjusted) | not applicable |

**These are two different datasets.** They differ in calendar, in hours per
period, in volatility regime and in price scale. Any comparison is of
*within-asset normalized* behaviour, never of dollar errors.

> **Provider caveat to verify (open decision D3):** USDT is not exactly USD, and
> Binance is one venue. The BTC series is a venue-specific price, not a global
> index. This must be stated in the report.

### 3.2 Immutability

- Raw provider responses are written once to `data/raw/` with a sibling
  `<name>.manifest.json` containing `source_url`, `downloaded_utc`, `row_count`,
  `first_ts`, `last_ts` and `sha256` of the raw bytes.
- Snapshots are never edited. A refresh creates a new snapshot file.
- Tests **must not** hit the network. They use the committed snapshot or a
  labelled synthetic fixture.

### 3.3 Label and decision time

```
Decision time:  immediately after the bar for session t has closed.
Features:       f(bars <= t)              -- trailing only
Label:          y_t = Close_raw[t+1]      -- next session's raw close
```

- The final row of each asset has no observable `t+1`; it is **dropped**.
- "Next session" for AAPL means the next exchange session (weekends/holidays
  are gaps, not steps). For BTC it means the next UTC daily bar.
- AAPL uses **raw close** as the label to keep the target aligned with the
  price a learner would see, informed by the adjustment caveat below.
  *Open decision D1:* whether to run a sensitivity check with adjusted close.

> **Target representation (decision D8, v1.1).** The reported estimand is always
> the error on the **next close price**. Models are trained on the price
> **change** `y_t = Close_{t+1} - Close_t` and the forecast is reconstructed as
> `Close_t + predicted_delta`. This is information-equivalent, because `Close_t`
> is known at decision time, and it is necessary because every feature is
> scale-free: a model trained on the raw level cannot recover a price level and
> collapses toward the training mean. The naive baseline is the same in both
> representations (`delta = 0`, i.e. `Close_t`).

> **Corporate-action caveat.** Using `Adj Close` as a target mixes dividend and
> split adjustment factors into the prediction problem, and those factors are
> revised *after* the fact by the provider. A model trained today on adjusted
> history sees numbers that were not available at the original decision time.
> This is a **subtle leakage channel** and must be disclosed. Raw close avoids
> it for the label but spans the 4:1 (2020) and 7:1 (2014) split boundaries in
> longer histories; our 5-year window is chosen to lie after the most recent
> split — **verify this on the actual snapshot** (open decision D4).

### 3.4 Eligible features (all trailing, all `<= t`)

| Feature | Definition | Rationale (educational) |
|---|---|---|
| `ret_1` | `Close_t / Close_{t-1} - 1` | Momentum; the scale-free quantity that matters |
| `ret_5` | `Close_t / Close_{t-5} - 1` | Weekly trend |
| `ret_20` | `Close_t / Close_{t-20} - 1` | Monthly trend |
| `ma_gap_5` | `Close_t / SMA_5,t - 1` | Distance from short moving average |
| `ma_gap_20` | `Close_t / SMA_20,t - 1` | Distance from long moving average |
| `vol_10` | rolling std of `ret_1` over 10 bars | Realized volatility |
| `vol_30` | rolling std of `ret_1` over 30 bars | Slower volatility |
| `range_1` | `(High_t - Low_t) / Close_t` | Intra-day dispersion |
| `vol_chg` | `Volume_t / SMA_5(Volume)_t - 1` | Volume anomaly |
| `dow` | day-of-week index (0–6) | Calendar effect |

Rolling statistics require a **full window** (`min_periods = window`), so
`vol_30` always means 30 observations; the first `lookback = 30` rows are
dropped rather than back-filled. No feature reads `t+1`.

### 3.5 Forbidden constructs (tests enforce these)

Shuffled splits · `center=True` rolling · `shift(-1)` in `X` · `bfill` ·
whole-dataset `mean`/`std` in preprocessing · fitting a scaler on
validation/test · target-derived features · per-model row filters.

---

## 4. Splits

Chronological, per asset, computed on the **asset's own session index** (never
on a shared calendar):

| Split | Fraction | Use |
|---|---|---|
| Train | first 60% of rows | Fitting, and the inner CV folds |
| Validation | next 20% | Hyperparameter selection, preprocessing choice, model selection |
| **Test** | final 20% | **Sealed.** One release, human-approved |

Hyperparameter search uses an **expanding-window** time-series CV **inside the
training block only**:

- 5 folds, `gap=1`, minimum first training fraction 0.30.
- The `gap=1` purges the boundary row whose label would reach into the next
  fold.
- Tuning therefore never sees the validation block, which keeps the validation
  block a genuine model-selection holdout rather than a second tuning set. This
  is more conservative than tuning on train+validation and is the implemented
  behaviour; the earlier wording in this section said "inside
  train+validation" and has been corrected (audit LEAK-004).

**Boundary rule:** the validation block starts at the first session at or after
the 60% row index. All models see the identical boundaries per asset.

**Purge (decision D9).** With `y_t = Close_{t+1}`, the last training row's label
is a validation-block price and the last validation row's label is a **sealed
test price**. `purge_gap: 1` drops one row at each boundary so that no label
crosses a split. Without it, perturbing a single test price changed the headline
validation metric by 0.408 — roughly 46x the reported model-vs-baseline margin.
A test asserts the purge explicitly.

---

## 5. Models and fairness

| `model_id` | Family | Scaling needed | Notes |
|---|---|---|---|
| `naive_persistence` | Baseline | none | `y_hat_t = Close_t` |
| `linear_baseline` | Linear (small Ridge) | yes | Simple learned floor |
| `ridge` | Regularized linear | yes | Transparent reference |
| `svr` | Kernel method (RBF) | **strongly** | Demonstrates scaling sensitivity |
| `random_forest` | Bagging | no (negative control) | Weak extrapolation |
| `hist_gradient_boosting` | Boosting | no | Early stopping on a random 10% of the training rows passed to `fit()`; the validation block is not used (D16) |
| `mlp` *(optional)* | Neural | yes | **Requires owner approval (D2)** |

Fairness rules:

- Identical features, target, splits, metrics and evaluation dates.
- **Identical tuning budget:** `max_trials = 24`, `max_seconds = 300` per
  (model × asset × variant) cell. Random search with a fixed seed.
- Identical CV folds.
- Every attempted configuration is logged, including failures.
- No model receives extra features, filtering or a shifted label.

---

## 6. Preprocessing ablation (RQ3)

One controlled factor at a time; all else fixed.

| Variant | Policy | Expected to matter for |
|---|---|---|
| `P0` | Minimal causal feature set, no scaling, median-impute (fitted on train) | reference |
| `P1` | Add missingness indicators + train-fitted imputation | models with missing inputs — **NOT_RUN when the snapshot has no missing values** |
| `P2` | `StandardScaler` fitted on train indices only | Ridge, SVR, MLP (contrast: trees invariant) |
| `P3` | Feature-set ablation: drop rolling/MA features, keep only `ret_1`, `ret_5`, `range_1`, `vol_chg`, `dow` | all |
| `P4` | Robust scaling / winsorization at train-fitted quantiles | outlier-sensitive models |

Contrast definition: `delta = metric(variant) - metric(P0)` computed on
**identical evaluation dates**, reported with the fold-level spread.

- `P0` has no missing data on our snapshots, so `P1` is only meaningful if
  missingness exists. If there is none, `P1` is reported as
  `NOT_RUN: no missing inputs in snapshot: imputation is a no-op` — **we do not
  fabricate NaNs** to make the ablation look substantive, and we do not publish
  a cell that would be byte-identical to P0.
- Trees under `P2` are a **negative control**: a large tree delta would indicate
  a bug, not a discovery.

---

## 7. Metrics, uncertainty, reporting

### 7.1 Primary metrics (next-close regression)

| Metric | Definition | Caveat to state |
|---|---|---|
| MAE | mean absolute error | In quote currency; **not comparable across assets** |
| RMSE | root mean squared error | Punishes large misses; same unit caveat |
| R² | `1 - SS_res/SS_tot` on test | **Inflated by trending price levels**; a naive forecast can score high |
| `skill_MAE` | `1 - MAE_model / MAE_naive` | Primary comparative metric; 0 = no better than looking at today's price |
| `skill_RMSE` | `1 - RMSE_model / RMSE_naive` | Secondary |

Cross-asset discussion uses `skill_MAE` and normalized error
(`MAE / mean(Close)`) only.

### 7.2 Secondary diagnostic (not a change of research question)

A direction/shape diagnostic on **returns** — e.g. sign agreement between
predicted price change and realized price change — is reported as an explicitly
labelled *secondary robustness diagnostic*. It does not replace RQ1.

### 7.3 Uncertainty

- Paired comparison on identical forecast dates only.
- Uncertainty via **moving-block bootstrap** over consecutive date blocks
  (block length ≈ 10 sessions), reporting a 95% interval for the skill score.
- Limitations stated: overlapping windows induce dependence; blocks are not
  independent; intervals are indicative, not confirmatory.
- **No p-values** unless a specific, justified test is added by a protocol bump.
  "Significant" is not used for observational performance differences.

### 7.4 Required figures

1. Data coverage, splits and label timeline (per asset).
2. Price history + volatility context.
3. Observed vs predicted on **approved** test dates, including naive.
4. Model vs naive on `skill_MAE`, per asset.
5. Train vs validation error (overfitting).
6. Preprocessing ablation deltas (heatmap / small multiples).
7. Worst episodes and honest error explanation.
8. Interpretability (coefficients / permutation importance) with no causal
   claim.
9. Education-oriented "which approach helps when" diagram.

---

## 8. Testability checklist

| Invariance | Test that must exist | Status |
|---|---|---|
| Label is `Close[t+1]` with the last row dropped | `test_label_shift_is_next_bar_and_drops_last` | IMPLEMENTED |
| Features never read future bars | `test_features_are_invariant_to_future_appends` | IMPLEMENTED |
| Split is chronological and disjoint | `test_split_is_chronological_and_disjoint` + `test_split_purge_gap_prevents_label_crossing` | IMPLEMENTED |
| Scaler parameters independent of validation/test | `test_scaler_fit_uses_train_indices_only` | planned |
| Naive baseline equals `Close_t` exactly | `test_naive_persistence_equals_previous_close` | IMPLEMENTED |
| All models see identical columns and dates | `test_lane_receives_identical_columns` (parametrised over all lanes) | IMPLEMENTED |
| Manifest rejects a missing data hash | `test_manifest_requires_data_sha256` | IMPLEMENTED |
| Metrics correct on known values | `test_mae_rmse_r2_on_hand_computed_values` | IMPLEMENTED |
| Notebook executes end-to-end | `test_notebook_executes` (G6) | PENDING |

## 9. Compute and scope budget

- Local CPU only. No paid compute.
- Smoke test on a 120-row slice before any real run.
- Full matrix: 2 assets × ~6 models × 5 variants ≈ 60 cells. At ≤300 s each,
  ≤5 h worst case — run in stages, with resume.
- Anything exceeding the budget requires a decision-log entry.

## 10. Open decisions requiring human approval

| ID | Decision | Default if unanswered | Who |
|---|---|---|---|
| D1 | Use raw close as primary label (with adjusted-close sensitivity check?) | Stay with **raw close**; run the sensitivity check as a robustness note | Owner |
| D2 | Include the optional `mlp` lane (needs recorded oral guidance) | **Exclude** until approved | Owner + Person 5 |
| D3 | Accept Binance USDT as the BTC price proxy, with caveat | Accept with caveat; do not claim a global index | Owner |
| D4 | Confirm the 5-year window contains no AAPL split | Verify on snapshot; extend/adjust window if a split is present | Owner + Person 1 |
| D5 | Confirm whether appendices count toward the word limit | Assume they **do** count until confirmed | Owner |
| D6 | Confirm the assigned presentation slot (19 vs 26 Nov) | Plan for the earlier date | Owner |
| D7 | Single test-set release date | Propose **2026-11-14**, one release | Owner |
