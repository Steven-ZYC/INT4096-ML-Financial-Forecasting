# Speaker Notes — Key Messages, Transitions, Q&A Routing

**Deck:** `slides/final/INT4096_Presentation.pdf` (24 pages: 17 narrative + 5 backup + 2 references)
**Full spoken script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照)
**Clock and voice blocks:** `timing_plan.md` · **Structure:** `storyboard.md`

This file is the **one-page briefing**: what each slide must land, how to hand over, and who answers
what. For the words to say, use the bilingual script — kept in one place so the two cannot drift apart.

> Speakers are not named: use the voice blocks in `timing_plan.md`. Research and software ownership is in
> `docs/management/responsibilities.md`.

---

## How the project works — the five-stage brief

Every presenter should be able to say this without notes. It is also the order of the talk.

1. **Data selection.** Apple from the StockAnalysis public API (exchange sessions, USD, 1,255 bars) and
   Bitcoin from the Binance public API (BTC/USDT daily, every day, 1,828 bars; one venue, not a global
   index). Five years from 2021-10-28, after Apple's 2020 split. Four conditions: window, raw close,
   a six-check quality gate that rejects rather than repairs, complete history (drop 30 warm-up rows
   and the last row). Result: 1,224 / 1,797 modelling rows.
2. **Processing and features.** Six raw-data problems, six decisions. Ten trailing, scale-free features
   (returns 1/5/20, gaps to 5- and 20-day averages, volatility 10/30, intraday range, relative volume,
   weekday). The model predicts the price change and we add it to the known close. Split 60/20/20 by
   date with one row purged at each boundary; six injected leakage defects are all caught.
3. **Models and tuning.** Linear baseline, ridge, SVR (RBF), random forest, histogram gradient boosting:
   three mechanisms. Every model is tuned the same way: 5 expanding-window folds inside the training
   block, 10 random trials, ≤90 s, seed 42, grids frozen in advance. The tuner mostly picks the most
   cautious settings. We also explored the target representation and P0 vs P2 scaling (trees identical).
4. **Evaluation.** MAE, RMSE, R² and skill = 1 − MAE_model / MAE_persistence. R² is high for any forecast
   near yesterday's price, so it never ranks. All 20 runs lie between −0.78% and +0.52% skill, and all
   20 block-bootstrap intervals include zero: parity with a strong baseline.
5. **Teaching design.** A 60-minute lesson whose five tasks each come from one pipeline stage and practise
   one course concept; baseline before models; Colab workbook, teacher guide with answers, a notebook
   that rebuilds the results.

**If asked something you don't know:** *"I don't know — but our run records are in the repository, so we
can look it up."* Never improvise a number.

---

## Per-slide key message and handover

| # | Slide | The one thing it must land | Handover / next |
|---|---|---|---|
| 1 | Learning ML Through Financial Forecasting | R² 0.9556 vs 0.9555: a score alone proves little; then the question | "Here is the pipeline." |
| 2 | Roadmap: One Pipeline, Five Stages | Five stages, one question each; task, yardstick, one-line result | "Part one: the data." **(handover E→A)** |
| 3 | What We Used, and Where It Came From | Two public sources, exact URLs, fingerprinted files | "Why these two?" |
| 4 | Why These Two | Calendar, volatility, scale, dividends all differ: robustness; only unit-free scores cross assets | "Not every row is usable." |
| 5 | Selection Conditions | Four conditions; reject, never repair; 1,224 / 1,797 rows | "With clean rows, part two…" **(handover A→B)** |
| 6 | Problems in the Raw Data | Six problems, six decisions | "Here are the features that come out." |
| 7 | Ten Features | Trailing, scale-free, tested; identical inputs for every model | "No price level means one more design step." |
| 8 | Engineering the Target | Predict the change, add it back; real row 1.25 vs 1.35; found by iteration | "The last processing step is the split." |
| 9 | Chronological Split and Leakage Checks | Purge per boundary (0.408); 6/6 defects caught | "Clean inputs, so part three…" **(handover B→C)** |
| 10 | Five Models Plus a Baseline | How each predicts, its strength, its role; three mechanisms | "Comparing them is only fair if…" |
| 11 | Fine-Tuning | Same inner CV, trials, time, seed; frozen grids; cautious choices | "We also explored more than hyperparameters." |
| 12 | What We Explored Beyond Hyperparameters | Target, P0 vs P2, trees identical, grid edges | "So how well did they do? Part four." **(handover C→D)** |
| 13 | Four Metrics | Each metric's job; R² trap; skill crosses assets | "Here is skill for every run." |
| 14 | Results | Within 1% of the baseline; best +0.52% / +0.26%; every run shown | "But are those small leads real?" |
| 15 | How Certain? | 20/20 intervals include zero; near-zero return correlation | "That result is exactly what we teach." **(handover D→E)** |
| 16 | Teaching Design | Five tasks ↔ stages ↔ course concepts; baseline first | "To close, what each stage delivered." |
| 17 | Summary | One outcome per stage; next steps; disclaimer | → Q&A |

---

## Q&A routing

Topic owners are voice blocks (see `timing_plan.md`), not names.

| Question | Suggested block | One-line answer |
|---|---|---|
| Where exactly is the data from? | A | The two URLs on slide 3 are the exact calls in our code; files and hashes are in `data/raw/`. |
| Why classical ML, not deep learning? | C | Handout discourages it; classical families keep the comparison interpretable. |
| Is this just a random walk? | D | At one day the return correlation is near zero, which is why a simple rule is such a strong baseline. |
| Why AAPL and BTC? | A | Different calendars, volatility, scale and corporate actions: one protocol on two structures is a robustness check. |
| Did you leak future data? | B | Chronological split, boundary purge, sealed test, 6/6 injected defects caught → Backup 3. |
| Did you cherry-pick P2? | D | No: Backup 1 shows all 20; best BTC overall is the unscaled linear baseline, +0.26%. |
| Was the budget fair? | C | Identical for all lanes: 10 trials / 90 s; tuning inside train only; protocol allows 24/300 → Backup 2. |
| Is +0.52% meaningful? | D | Not by our own test: all 20 bootstrap intervals include zero. |
| Why P0 and P2? | C | They isolate scaling, the course's question. P1 would duplicate P0 (no missing values); P3/P4 are queued next. |
| Why are some chosen values at the grid edge? | C | Small declared grids, same budget for every model; widening them is an easy next step. |
| Can this make money? | E | No. Error metrics ignore costs and risk; we make no profitability claim. |
| Did the lesson improve learning? | E | The lesson is built and reproducible; measuring learning is what the classroom pilot is for. |
| What should students learn? | E | Compare every model with a simple baseline, check what it could see, and ask how certain the gain is. |

---

## Delivery guardrails (internal, not for slides)

The talk leads with strengths. These guardrails keep that framing accurate when examiners ask.

1. **Never read a number you cannot explain.** If a figure is challenged, go to Backup 1 or the repository.
2. **Never say "every number in this talk is from validation".** Say "every **model-performance** number".
   Dataset sizes, price ranges and the return-correlation diagnostic use the full price history.
3. **Never imply the test block was used, or that the lesson improved learning.** Both are false as of
   this submission and both are easy for an examiner to check.
4. **Never say a model "won", or that standardisation "improved" prediction.** Say "slightly ahead" and
   "changed behaviour".
5. **Never call the linear lane "near-unregularised".** It is a ridge with a tuned penalty (selected 10).
