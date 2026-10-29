# Formative Tasks and Worked Answers

Five tasks aligned to the learning objectives in
`docs/education/lesson_plan.md`. Each has a worked answer and a marking guide.

Tasks are designed so that a learner must **interpret real artifacts**, not recall
definitions. Where a number is quoted, it comes from
`docs/research/run_registry.md`; learners should be able to find it themselves.

---

## Task 1 — Fitting versus generalising (objective O1)

**Prompt.** A model reports MAE 0.9 on the data it was trained on and MAE 2.9 on
unseen data. The naive baseline scores 2.9 on the same unseen data.

(a) What is the model doing?
(b) Would you deploy it? Give a one-sentence reason.
(c) What single change to the *evaluation setup* would make the first number
useless for judging the model?

**Worked answer.**
(a) It has memorised the training data. The gap between 0.9 and 2.9 is the
generalisation gap; on unseen data it is no better than doing nothing.
(b) No. A model that matches the baseline has learned nothing that transfers;
"0.9" describes memory, not forecasting skill.
(c) Report only validation/test error and never quote training error as evidence
of quality. (Accept also: shuffle the split — but then note it would *create* a
leak on time-ordered data, which is a different error.)

**Marking guide.** Full marks require (b) to be justified with the baseline
comparison, not with the phrase "overfitting" alone.

---

## Task 2 — Spot the leakage (objective O2)

**Prompt.** This feature builder is used to predict tomorrow's close:

```python
def make_features(df):
    out = pd.DataFrame(index=df.index)
    out["ret_1"] = df["close"].pct_change(1)
    out["tomorrow_ret"] = df["close"].pct_change(1).shift(-1)
    out["ma_5"] = df["close"].rolling(5, center=True).mean()
    return out
```

(a) Identify **two** separate leaks.
(b) Explain, for each, why the model would look excellent in validation and fail
in real use.
(c) Rewrite both lines correctly.

**Worked answer.**
(a) `shift(-1)` moves tomorrow's return into today's features; `center=True` makes
the 5-bar mean include two future bars.
(b) Both give the model the answer at prediction time. Validation looks excellent
because the information really is present *in the data* — it just could not exist
at the moment of prediction. In production, those columns would be unavailable (or
stale), so performance collapses.
(c)

```python
out["ret_1"] = df["close"].pct_change(1)                  # trailing, fine
out["ret_5"] = df["close"].pct_change(5)                  # replace tomorrow_ret
out["ma_5"] = df["close"].rolling(5, min_periods=5).mean()  # no centring
```

**Marking guide.** Both leaks must be named. Partial credit for identifying one.
Deduct if the learner claims `center=True` is "just smoothing" without stating
that it reads future bars.

Note for the teacher: this exact defect class is what the project's own test suite
now catches — see `tests/test_temporal_integrity.py` and
`scripts/mutation_check.py`.

---

## Task 3 — Reading a skill score (objective O3)

**Prompt.** From the project's registry (variant P2, validation):

| Model | AAPL `skill_MAE` |
|---|---:|
| `svr` | +0.52% |
| `ridge` | +0.29% |
| `hist_gradient_boosting` | +0.25% |
| `linear_baseline` | −0.50% |
| `random_forest` | −0.78% |

(a) Which model would you report as "best", and with what caveat?
(b) Explain what −0.78% means in plain language.
(c) The random forest has far more capacity than ridge. Why is it worse?

**Worked answer.**
(a) SVR at +0.52%, but the caveat is that half a percent is small relative to
uncertainty and is not evidence of a practically useful edge.
(b) The forest's average error is 0.78% *larger* than simply predicting that
tomorrow's close equals today's. It is worse than the free rule.
(c) Capacity is not the constraint — information is. Trees also cannot extrapolate
outside the price range seen in training, and with near-zero return
autocorrelation there is little learnable signal; extra capacity mostly fits
noise.

**Marking guide.** Full marks require (a) to include a caveat and (b) to use
"worse than persistence" rather than "negative accuracy".

---

## Task 4 — Which model cares about scaling? (objective O4)

**Prompt.** Applying `StandardScaler` changed validation MAE by **exactly 0.0000%**
for `random_forest` and `hist_gradient_boosting`, but by a small non-zero amount
for `ridge` and `svr`.

(a) Explain mechanistically why trees are unaffected.
(b) Explain why a kernel method is affected.
(c) A classmate says "scaling improves accuracy". What is wrong with that
sentence?

**Worked answer.**
(a) A decision tree splits on `feature < threshold`. Rescaling a feature
multiplies every value by a constant, so the *order* is preserved and an
equivalent threshold exists. The chosen splits — and therefore the predictions —
are identical.
(b) An RBF kernel computes distances between points: it squares differences across
features and sums them. If one feature ranges over 0–6 (day of week) and another
over 0.001–0.02 (returns), the large-range feature dominates the distance. Scaling
changes which feature dominates, so it changes the learned function.
(c) It is causal language applied to an observational comparison, and it is not
universally true: here scaling *increased* error for `linear_baseline` on AAPL
(+0.74%). The accurate statement is "scaling changed the result for these models
on this data; for trees it changed nothing."

**Marking guide.** (a) must mention order/threshold preservation. (c) must object
to the word "improves" and ideally cite the counter-example.

---

## Task 5 — Error is not profit, and limits of the evidence (objective O5)

**Prompt.** The best model has validation MAE of about 2.9 USD on a ~230 USD
stock, and its skill over the naive rule is +0.5%.

(a) A friend says: "0.5% better than a naive rule — we can trade this." Give two
concrete reasons this is unjustified.
(b) Name two things about this study that limit how far its conclusions generalise.
(c) Write one sentence you could put on a slide that is both accurate and honest.

**Worked answer.**
(a) Any two of: transaction costs and spreads can exceed the measured edge; the
edge is within the noise of a single time window; MAE does not model position
sizing or drawdown; one-session-ahead forecasts of a near-random-walk series
rarely survive costs.
(b) Any two of: only two assets; a single 2021–2026 window covering specific
regimes; BTC is one venue's USDT price; only one prediction horizon; no
transaction-cost model; the test block has not been unsealed.
(c) Example: "Across two markets and five model families, none beat a naive
persistence rule by more than about 1% on held-out data — which tells us more
about the difficulty of the task than about the models."

**Marking guide.** (a) must engage with *money*, not with statistics alone.
(c) must not claim profitability and must not invent a stronger result than the
evidence supports.

---

## Answer-key policy

Answers above are the expected reasoning, not the only acceptable wording. Mark
for the **reason**, not the phrase. A learner who reaches a correct conclusion by
a different valid route should receive full marks.

Any learner answer that asserts measured learning gains, profitability, or a
statistically significant superiority should be corrected against
`docs/research/protocol.md` §7.3 and the disclaimers in
`docs/education/lesson_plan.md` §6.
