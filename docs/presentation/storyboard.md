# Slide Storyboard — 18:00 content, five speakers, ≤20 minutes

Companion to `docs/management/responsibilities.md` §4. Every number on a slide
must carry a run ID or point to the figure that regenerates it.

**Constraint check:** 3:30 + 4:00 + 4:00 + 3:30 + 3:00 = **18:00** of content,
leaving 2:00 for Q&A inside a 20-minute limit.

---

## Slide 1 — Title (Person 2, 0:00)

- Working title, course, group, date.
- Non-advisory disclaimer already visible on the title slide, not only at the end.

## Slide 2 — The educational problem (Person 2, 0:30–2:00)

- Audience: advanced secondary / non-specialist university learners.
- Why forecasting is a good vehicle: it makes *generalisation*, *leakage* and
  *baselines* concrete and checkable.
- One sentence naming the four research questions. Do not read them all.

## Slide 3 — Research questions and the honest goal (Person 2, 2:00–3:30)

- RQ1 model comparison, RQ2 capacity, RQ3 preprocessing, RQ4 education.
- State plainly: "a negative result is an acceptable outcome; we are not
  optimising for an attractive number."

## Slide 4 — Data: two different datasets (Person 1, 3:30–5:30)

- `fig01` coverage and splits.
- AAPL: exchange sessions, USD, raw close. BTC: 24/7 UTC, USDT, single venue.
- **"We never align them by row number."**

## Slide 5 — Causal features and the split trap (Person 1, 5:30–7:30)

- The ten features, all trailing ratios; the ratio-vs-price-level reason.
- Chronological 60/20/20 + the **one-row purge** at each boundary.
- One-line teaser: "an audit found we had a boundary leak; here is the fix."

## Slide 6 — Measured evidence of no leakage (Person 1, 7:30)

- Appending absurd future prices leaves historical features unchanged.
- Mutation testing: 5 injected leakage defects, 5 caught.
- Say the number: **79 tests**, and the suite is *proven able to fail*.

## Slide 7 — The opponent everyone forgets (Person 3, 7:30–9:30)

- Show the naive baseline MAE **first**, before any model.
- Define `skill_MAE = 1 − MAE_model / MAE_naive`.
- Explain why dollar errors are not comparable across assets.

## Slide 8 — Five model families, one fair protocol (Person 3, 9:30–11:30)

- Table: family, what it learns, needs scaling?, tuning budget.
- Identical features, split, evaluation dates, `max_trials`, `max_seconds`.
- Tuning never sees validation or test.

## Slide 9 — Results: nothing meaningfully beats persistence (Person 4, 11:30–13:30)

- `fig04` (shared axis — explain why the axis is shared).
- Every value within ±1%; `random_forest` on AAPL is **−0.78%** (worse).
- Trained models: 20 runs, all validation only; **test block still sealed**.

## Slide 10 — Why complexity did not help (Person 4, 13:30–15:00)

- Near-zero daily-return autocorrelation.
- Trees cannot extrapolate beyond the training price range.
- "The limiting factor is information, not capacity."

## Slide 11 — Deep dive: preprocessing is part of the model (Person 5, 15:00–16:30)

- `fig06` ablation.
- Trees: **exactly 0.0000%** change. SVR/ridge: measurable change.
- Contrast: thresholds within a feature vs distances across features.
- Honest extra: scaling *increased* error for `linear_baseline` on AAPL.

## Slide 12 — The lesson for learners (Person 5, 16:30–17:30)

- One objective (O3): read a skill score, including a negative one.
- One task shown live: spot the `shift(-1)` leak in six lines of code.
- State: designed resource, **no learner study**, no learning-gain claim.

## Slide 13 — Limitations and conclusion (Person 5, 17:30–18:00)

- Two assets, one window, one horizon, no costs, BTC is one venue.
- The finding: careful comparison beats impressive complexity.
- Disclaimer repeated. Close.

---

## Q&A appendix slides (not presented, shown only if asked)

| Slide | Content |
|---|---|
| A1 | Full 20-cell skill table with run IDs |
| A2 | Split boundaries in dates, per asset, with the purge row marked |
| A3 | Audit findings LEAK-001/002 with the before/after reproduction |
| A4 | Why not deep learning: `[A]` handout + `[B]` oral guidance + gated MLP (D2) |
| A5 | Bootstrap interval method and its temporal-dependence caveat |
| A6 | Word-count policy and appendix uncertainty (D5) |
| A7 | AI-use statement and per-member contributions |

---

## Production rules

1. **One idea per slide.** If a slide needs two sentences of setup, split it.
2. **Every figure gets an axis label and a unit.** No unlabelled axes.
3. **Never show a number without its run ID** in the speaker notes at minimum.
4. **Rehearse with a visible timer twice.** Cut from slides 2–3 and 12 first.
5. **Do not read the slides.** The audience can read; the speaker interprets.
6. **Handover must be a technical bridge**, e.g. "…and that is *why* the split
   boundary matters — Person 1 will show the fix." Not "over to you."
