# Speaker Notes — Key Messages, Transitions, Q&A Routing

**Deck:** `slides/final/INT4096_Presentation.pdf` (23 pages: 16 narrative + 5 backup + 2 references)
**Full spoken script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照)
**Clock and voice blocks:** `timing_plan.md` · **Structure:** `storyboard.md`

This file is the **one-page briefing**: what each slide must land, how to hand over, and who answers
what. For the words to say, use the bilingual script — kept in one place so the two cannot drift apart.

> Speakers are not named: use the voice blocks in `timing_plan.md`. Research and software ownership is in
> `docs/management/responsibilities.md`.

---

## How the project works — the 8-step brief

Every presenter should be able to say this without notes.

1. **Two price histories.** Apple (exchange sessions, USD, 1,255 bars) and Bitcoin (24/7, Binance
   BTCUSDT, 1,828 bars — one venue, not a global index).
2. **Ten features per day**, all computed up to the close: returns (1/5/20), gaps to 5- and 20-session
   averages, volatility (10/30), intraday range, volume anomaly, weekday. No price level.
3. **Predict the change, not the price.** The model predicts ΔP; we add it to the known close. We did
   this because the first run, which predicted the price level directly, scored far below persistence.
4. **Split by time**: 60% train, 20% validation, 20% sealed test, one row purged at each boundary.
   Scaling is fitted on training rows only.
5. **Tune inside the training block only**: 5 expanding-window folds, 10 random trials, ≤90 s per cell,
   identical for every lane. The validation block never touches tuning. (The protocol allows 24/300; we
   report what we used.)
6. **Compare against persistence** — "tomorrow equals today". Skill = 1 − MAE_model / MAE_naive, so 0
   means no better.
7. **20 runs**: 5 model families × 2 assets × 2 preprocessing settings (P0 raw, P2 standardised). All
   validation. The test block has never been read.
8. **Then ask why**: 20/20 bootstrap intervals include zero; trees ignore scaling; return correlation
   is near zero.

**If asked something you don't know:** *"I don't know — but our run records are in the repository, so we
can look it up."* Never improvise a number.

---

## Per-slide key message and handover

| # | Slide | The one thing it must land | Handover / next |
|---|---|---|---|
| 1 | Learning ML Through Financial Forecasting | R² 0.9556 vs 0.9555: a score alone proves little | "So what should we ask?" |
| 2 | Three Questions to Ask of Any AI Score | The three questions are the spine and the lesson's goal | "Start with the data." |
| 3 | Two Markets, One Protocol | Two calendars as robustness; data checks reject, not repair; BTC is one venue | "Now, what goes into the model?" **(handover A→B)** |
| 4 | Ten Inputs … at the Close | Ten backward-looking features, tested; no price level | "No price level means the model cannot output a price." |
| 5 | Predicting the Change … | Predict ΔP and add it back; forced by a failed first run; real row 1.25 vs 1.35 | "Next: how we split the data." |
| 6 | Chronological Splits … | Purge a row per boundary, fit on train only, test sealed | "How do we know the pipeline cannot peek?" **(handover B→C)** |
| 7 | How We Know the Pipeline Cannot Peek | Six injected defects, all caught; the first suite missed two | "With clean inputs, let's meet the models." |
| 8 | Five Models, Three Mechanisms | Mechanism contrast, one teaching question each; no deep learning | "Then, how do we keep it fair?" |
| 9 | Same Budget, Same Rules … | Same features, seed, budget; tuning inside train only; 20 runs | "Now to evaluation, and to the opponent." |
| 10 | The Opponent: Copy Today's Close | Baseline + skill score; why not R² | "So, the results." **(handover C→D)** |
| 11 | Best Skill Is +0.52%; 5 of 20 Lose | The range, not a ranking; nothing cherry-picked (Backup 1) | "That is exactly what we tested next." |
| 12 | All 20 Bootstrap Intervals Include Zero | A tie, not a winner; 244/358 validation days; indicative only | "Maybe the data just needs better preparation?" |
| 13 | Scaling Changes Some … | Trees identical; kernels/penalties move; behaviour ≠ improvement | "So why do the gains stay so small?" **(handover D→E)** |
| 14 | Why the Gains Stay Small | Near-zero return correlation; the rule tracks level; one diagnostic, not proof | "Now: what do we hand to teachers?" |
| 15 | A 60-Minute Lesson … | Package + live question (B); no learner study | "Let me close with the skill, and its limits." |
| 16 | The Skill Students Can Take … | Three questions; limits; disclaimer | → Q&A |

---

## Q&A routing

Topic owners are voice blocks (see `timing_plan.md`), not names.

| Question | Suggested block | One-line answer |
|---|---|---|
| Why classical ML, not deep learning? | C | Handout discourages it; classical families keep the comparison interpretable. |
| Is this just a random walk? | D | At one day the return correlation is near zero, which fits; it probes one signal, so it is not proof. |
| Why AAPL and BTC? | A | One session-based equity, one 24/7 market: same protocol, different microstructure. |
| Did you leak future data? | C | Chronological split, boundary purge, sealed test, 6/6 injected defects caught → Backup 3. |
| Did you cherry-pick P2? | D | No: Backup 1 shows all 20; best BTC overall is the unscaled linear baseline, +0.26%. |
| Was the budget fair? | C | Identical for all lanes: 10 trials / 90 s; tuning inside train only; protocol allows 24/300 → Backup 2. |
| Is +0.52% meaningful? | D | Not by our own test: all 20 bootstrap intervals include zero. |
| Why only P0 and P2? | C | P1 would equal P0 (no missing values), logged as not run; P3/P4 not yet run. |
| Why are some chosen values at the grid edge? | C | The grid may be narrow; it does not change the direction of the result. |
| Can this make money? | E | No. Error metrics ignore costs and risk; we make no profitability claim. |
| Did the lesson improve learning? | E | Not tested. It is a designed resource ready for a classroom pilot. |
| What should students learn? | E | Ask three questions of any model: what it could see, how a simple rule did, how certain the gain is. |

---

## Things to never do

1. **Never read a number you cannot explain.** If a figure is challenged, go to Backup 1 or the repository.
2. **Never say "every number in this talk is from validation".** Say "every **model-performance** number".
   Dataset sizes, price ranges and the return-correlation diagnostic use the full price history.
3. **Never imply the test block was used, or that the lesson improved learning.** Both are false as of
   this submission and both are easy for an examiner to check.
4. **Never say a model "won", or that standardisation "improved" prediction.** Say "slightly ahead" and
   "changed behaviour".
5. **Never call the linear lane "near-unregularised".** It is a ridge with a tuned penalty (selected 10).
