# Speaker Notes — Key Messages, Transitions, Q&A Routing

**Deck:** `deliverables/presentation/INT4096_Presentation.pdf` (26 pages: 18 narrative + 6 backup + 2 references)
**Full spoken script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照)
**Clock and voice blocks:** `timing_plan.md` · **Structure:** `storyboard.md`

This file is the **one-page briefing**: what each slide must land, how to hand over, and who answers
what. For the words to say, use the bilingual script — kept in one place so the two cannot drift apart.

> Speakers: Dong Yuankun slides 1–5 · Zhang Yancheng 6–12 · Zhang Haoyu 13–15 · Lau Pak Hei 16–17 ·
> Lui Shing Lam 18 (see `timing_plan.md`).

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
| 2 | Roadmap: One Pipeline, Five Stages | Five stages, one question each; task, yardstick, one-line result | "Part one: the data." |
| 3 | What We Used, and Where It Came From | Two public sources, exact URLs, fingerprinted files | "Why these two?" |
| 4 | Why These Two | Calendar, volatility, scale, dividends all differ: robustness; only unit-free scores cross assets | "Not every row is usable." |
| 5 | Selection Conditions | Four conditions; reject, never repair; 1,224 / 1,797 rows | "…move on to Processing and Feature Engineering." **(handover Dong Yuankun → Zhang Yancheng)** |
| 6 | Problems in the Raw Data | Six problems, six decisions | "Here is what that looks like for one real day." |
| 7 | From One Day's Prices to Ten Features | Walk one real row: each feature from that day and earlier; tested | "Now, what happens to these numbers inside each model?" |
| 8 | Every Model Gets the Same Data | Same data for all five; P0/P2 the only switch (scale table); predict the change, add it back | "Last: how the rows are split in time." |
| 9 | Chronological Split and Leakage Checks | Purge per boundary; 6/6 defects caught | "Clean inputs, so part three…"  |
| 10 | Five Models Plus a Baseline | How each predicts, its strength, its role; three mechanisms | "Comparing them is only fair if…" |
| 11 | Fine-Tuning | Same inner CV, trials, time, seed; frozen grids; cautious choices | "We also explored more than hyperparameters." |
| 12 | What We Explored Beyond Hyperparameters | Target, P0 vs P2, trees identical, grid edges | "So, how well did all these models do? Zhang Haoyu will show you." **(handover Zhang Yancheng → Zhang Haoyu)** |
| 13 | Four Metrics | Each metric's job; R² trap; skill crosses assets | "Here is skill for every run." |
| 14 | Results | Within 1% of the baseline; best +0.52% / +0.26%; every run shown | "But are those small leads real?" |
| 15 | How Certain? | 20/20 intervals include zero; near-zero return correlation | "And that is exactly what our lesson teaches." **(handover Zhang Haoyu → Lau Pak Hei)** |
| 16 | Teaching Design | Five tasks ↔ stages ↔ course concepts; baseline first | "And you can try all of it yourself." |
| 17 | Try It Yourself | The website: every step with real data; scan the QR code | "Scan the code to try it." **(handover Lau Pak Hei → Lui Shing Lam)** |
| 18 | Summary | One outcome per stage; next steps; disclaimer | → Q&A |

---

## Q&A routing

Questions go to Dong Yuankun, Zhang Yancheng or Zhang Haoyu. Lau Pak Hei and Lui Shing Lam do not take Q&A; Zhang Yancheng answers anything aimed at them.

| Question | Answers | One-line answer |
|---|---|---|
| Where exactly is the data from? | Dong Yuankun | The two URLs on slide 3 are the exact calls in our code; files and hashes are in `data/raw/`. |
| Why classical ML, not deep learning? | Zhang Yancheng | Handout discourages it, so the main comparison is classical. A supplementary MLP and LSTM could not call the next-day direction better than a simple rule; all four intervals include zero → Backup 6. |
| Is this just a random walk? | Zhang Haoyu | At one day the return correlation is near zero, which is why a simple rule is such a strong baseline. |
| Why AAPL and BTC? | Dong Yuankun | Different calendars, volatility, scale and corporate actions: one protocol on two structures is a robustness check. |
| Did you leak future data? | Zhang Yancheng | Chronological split, boundary purge, sealed test, 6/6 injected defects caught → Backup 3. |
| Did you cherry-pick P2? | Zhang Haoyu | No: Backup 1 shows all 20; best BTC overall is the unscaled linear baseline, +0.26%. |
| Was the budget fair? | Zhang Yancheng | Identical for all lanes: 10 trials / 90 s; tuning inside train only; protocol allows 24/300 → Backup 2. |
| Is +0.52% meaningful? | Zhang Haoyu | Not by our own test: all 20 bootstrap intervals include zero. |
| Why P0 and P2? | Zhang Yancheng | They isolate scaling, the course's question. P1 would duplicate P0 (no missing values); P3/P4 are queued next. |
| Why are some chosen values at the grid edge? | Zhang Yancheng | Small declared grids, same budget for every model; widening them is an easy next step. |
| Can this make money? | Zhang Haoyu | No. Error metrics ignore costs and risk; we make no profitability claim. |
| Where can we see the details? | Zhang Yancheng | On our website (QR code on slide 17), built from the same data and results as the slides. |
| Did the lesson improve learning? | Zhang Yancheng | The lesson is built and reproducible; measuring learning is what the classroom pilot is for. |
| What should students learn? | Zhang Yancheng | Compare every model with a simple baseline, check what it could see, and ask how certain the gain is. |

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
