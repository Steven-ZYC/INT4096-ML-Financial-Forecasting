# Speaker Notes — Key Messages, Transitions, Q&A Routing

**Deck:** `slides/final/INT4096_Presentation.pdf` (21 pages: 16 narrative + 5 backup)
**Full spoken script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照)
**Clock:** `timing_plan.md`

This file is the **one-page-per-act briefing**: what each slide must land, how to
hand over, and who answers what. For the words to say, use the bilingual script —
deliberately kept in one place so the two documents cannot drift apart.

> Presentation roles only. Research and software ownership is recorded in
> `docs/management/responsibilities.md`.

---

## How the project works — the 8-step brief

Every presenter should be able to describe this without notes.

1. **Two price histories.** Apple (exchange sessions, USD) and Bitcoin (24/7,
   Binance BTCUSDT — one venue, not a global index).
2. **Ten features per day**, all ratios: returns (1/5/20), gaps to 5- and
   20-session averages, volatility (10/30), intraday range, volume anomaly, weekday.
3. **Predict the change, not the price.** A ratio cannot output a price, so the
   model predicts ΔP and we add it to the known close.
4. **Split by time**: 60% train, 20% validation, 20% sealed test, with one row
   purged at each boundary.
5. **Tune inside training only**: 10 random trials, ≤90 s per cell, identical for
   every lane. (The protocol allows 24/300; we report what we used.)
6. **Compare against persistence** — "tomorrow equals today". Skill = 1 −
   MAE_model / MAE_naive, so 0 means no better.
7. **20 cells**: 5 model families × 2 assets × 2 preprocessing variants. All
   validation; the test block has never been read.
8. **Then ask why**: compare unscaled vs standardised inputs, and check whether
   each model family even depends on feature scale.

**If asked something you don't know:** *"I don't know — but our run records are in
the repository, so we can look it up."* Never improvise a number.

---

## Per-slide key message and handover

| # | Slide | Presenter | The one thing it must land | Handover |
|---|---|---|---|---|
| 1 | Can Five ML Models Beat a One-Line Rule? | Pak Hei | The whole talk is one comparison; don't reveal the answer | "Haoyu will explain why this data is the right place to test it." |
| 2 | Why Use Market Data to Teach ML? | Haoyu | Market data punishes three beginner mistakes fast | "Dong sets up the experiment." |
| 3 | Two Markets, One Rigorous Protocol | Yuankun | Same protocol, two microstructures, integrity-checked data | "What exactly is the model predicting?" |
| 4 | Framing the Prediction Target | Haoyu | Predict the change, add it back — otherwise copying the level looks good | "Before any result, we locked four questions." |
| 5 | Pre-Committed Questions | Haoyu | Rules fixed in advance; a null result counts | "That means nothing if the model can see the future." |
| 6 | Ten Signals from the Past | Yuankun | Ten backward-looking ratios, no price level | "Clean features aren't enough — the split must be clean." |
| 7 | Chronological Splitting and Zero Leakage | Yuankun | Purge the boundary, seal the test block, test the claim | "So the data is clean. Pak Hei on what we put on top." |
| 8 | Five Classical Models, Three Paradigms | Pak Hei | Contrast in mechanism, one shared path, no deep learning | "Whatever the model, it must beat something." |
| 9 | The Opponent Everyone Forgets | Pak Hei | A model's own MAE is meaningless without a baseline | "We have models and benchmark. Yancheng has results." |
| 10 | The Verdict: Almost Zero Gain | Yancheng | Peak +0.52%; 3/10 standardised runs lose to the rule | "Which is exactly what we tested next." |
| 11 | Statistical Reality Check | Yancheng | 20/20 bootstrap intervals cross zero → tie, not a winner | "So was it how we prepared the data?" |
| 12 | Does Preprocessing Save the Models? | Yancheng | Trees identical under scaling; kernels/penalties move; not an upgrade button | "So why didn't the extra capacity pay off?" |
| 13 | Why Complexity Hit a Wall | Yancheng | Thin signal (autocorr ≈ 0) + leaf averaging | "That's what the numbers say. Yuankun on what we learned." |
| 14 | From Finding to a Turnkey Classroom Lab | Yancheng | 60-min lab, 5 tasks, live MCQ with answer B; no learner study | "What did we learn as builders?" |
| 15 | Engineering and Pedagogical Takeaways | Yuankun | Four disciplines of a trustworthy benchmark | "Shing Lam closes with boundaries and the bigger lesson." |
| 16 | Study Boundaries and the Bigger Lesson | Shing Lam | Scope, next steps, one memorable sentence, disclaimer | → Q&A |

---

## Q&A routing

| Question | Owner | One-line answer |
|---|---|---|
| Why classical ML, not deep learning? | Yancheng | Handout discourages it; not needed here; classical families keep the comparison interpretable. |
| Is this just a random walk? | Yancheng | At one day, close to it — that *is* the finding, and why persistence is strong. |
| Why AAPL and BTC? | Haoyu | One session-based equity, one 24/7 market: same protocol, different microstructure. |
| Did you leak future data? | Yuankun | Chronological split, boundary purge, sealed test, mutation-tested leakage suite → Backup 3. |
| Did you cherry-pick P2? | Yancheng | No: Backup 1 shows all 20 cells; best BTC overall is unscaled linear, +0.26%. |
| Was the budget fair? | Yuankun | Identical for all lanes: 10 trials / 90 s; protocol allows 24/300, we report what we used → Backup 2. |
| Is +0.52% meaningful? | Yancheng | No by our own test: all 20 bootstrap intervals include zero. |
| Can this make money? | Pak Hei | No. Error metrics ignore costs and risk; we make no profitability claim. |
| What should students learn? | Shing Lam | Ask three questions of any model: did it generalise, did it cheat, did it beat the baseline. |

---

## Two things to never do

1. **Never read a number you cannot explain.** If a figure is challenged, refer to
   Backup 1 or the repository rather than guessing.
2. **Never imply the test block was used, or that the lesson improved learning.**
   Both claims are false as of this submission, and both are easy for an examiner
   to check.
