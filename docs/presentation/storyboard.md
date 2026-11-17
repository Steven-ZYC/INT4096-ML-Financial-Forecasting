# Slide Storyboard — Five-Act Research Story

**Bilingual rehearsal script (English spoken, 中文对照):**
`speaker_script_bilingual.md` (printable: `speaker_script_bilingual.pdf`)

**Deck:** `slides/latex/main.tex` → `slides/final/INT4096_Presentation.pdf`
**Slides:** 15 narrative + 5 backup (20 pages) · **Speech:** 16:00 of a 20:00 limit
**Companion documents:** `timing_plan.md` (per-slide clock) · `speaker_notes.md`
(words to say, transitions, likely confusion)

> **Presentation roles only.** The speaker assignments below describe who talks,
> not who built what. Research and software ownership is recorded in
> `docs/management/responsibilities.md`.

---

## The spine

The talk answers one question and lets each act raise the next:

1. **Which would you trust — five models or one line?** (Act I)
2. **How can we compare them without accidentally using the future?** (Act II)
3. **What actually happened?** (Act III)
4. **Why didn't the complexity help?** (Act IV)
5. **What does that teach us about machine learning?** (Act V)

Each act ends with a sentence that makes the next act necessary. If a slide does
not move that chain forward, it belongs in backup.

---

## Act I — The Challenge · Lau Pak Hei · 1:20

| # | Title | Message | Evidence |
|---|---|---|---|
| 1 | Can Five Machine-Learning Models Beat a One-Line Rule? | This is the whole talk in one question | Non-advisory note on the title |
| 2 | Which Would You Trust? | Complexity is not usefulness; only a fair comparison decides | States both options; **results withheld** |

**Deliberate choices:** no results, no numbers, no method. The audience is asked to
commit to a guess, which makes Act III land.

## Act II — Designing a Fair Experiment · 7:00

| # | Title | Presenter | Message | Evidence |
|---|---|---|---|---|
| 3 | Two Markets, One Fair Test | Zhang Haoyu | Two deliberately different markets, one identical pipeline | Bar counts; Binance BTCUSDT caveat |
| 4 | What We Are Actually Predicting | Zhang Haoyu | Predict the change, add it to the known price | **One real committed prediction**: 228.52 → +0.10 → 228.62 vs 229.87 (error 1.25) |
| 5 | Four Questions, Fixed Before We Looked | Zhang Haoyu | Questions and the acceptance of a negative result were declared in advance | RQ1–RQ4 |
| 6 | Only the Past Is Visible | Dong Yuankun | A random split on time-ordered data is cheating; the fix is a purge, not just sorting | Six injected leakage defects, all must be caught |
| 7 | Splitting Time Without Cheating | Dong Yuankun | The test block is visibly sealed and used nowhere in this talk | `fig01` chronological split |
| 8 | Ten Signals from the Past | Dong Yuankun | Ten trailing ratios, no price level — hence the change target | Feature list |

**Recurring example:** the single prediction on slide 4 is reused implicitly
through the results (same units, same target) so the audience can carry one concrete
case through the whole argument.

## Act III — The Reveal · Zhang Yancheng · 3:35

| # | Title | Message | Evidence |
|---|---|---|---|
| 9 | What Must Our Models Beat? | Persistence is a strong opponent; skill has a meaningful zero | Naive MAE 2.91 / 1604.35 over 244 / 358 sessions |
| 10 | More Complexity, Almost No Improvement | Best is +0.52% on AAPL; 5 of 20 runs are below the rule | P2 table, generated from `metrics.json` |
| 11 | The Improvements Are Inside the Noise | Spread ≈1.3 pp; bootstrap interval includes zero for 20/20 runs | `fig04` + block-bootstrap analysis |

**Careful wording:** the deck says some configurations are *better*; it never says
nothing improves, and never claims significance.

## Act IV — Investigating Why · Zhang Yancheng · 2:25

| # | Title | Message | Evidence |
|---|---|---|---|
| 12 | Does Changing the Input Change the Answer? | Trees are exactly invariant to scaling; kernels and linear models are not | `fig06`; P0 vs P2 predictions differ by **exactly 0** for both tree ensembles |
| 13 | Why More Complexity Did Not Help | Thin short-horizon signal; leaf averaging limits tree outputs | lag-1 autocorrelation +0.021 (AAPL), −0.026 (BTC) |

**Key distinction made explicit:** preprocessing *changes behaviour* ≠ preprocessing
*improves prediction*. The deck also notes scaling made the linear baseline slightly
worse on AAPL, so it is not presented as a universal good.

## Act V — The Bigger Lesson · Lui Shing Lam · 1:40

| # | Title | Message | Evidence |
|---|---|---|---|
| 14 | What This Teaches Us About Machine Learning | Five transferable lessons | Ties each lesson to something shown earlier |
| 15 | The Value Is in the Comparison | Limitations, then one memorable sentence | Test block still sealed; non-advisory |

**Education framing:** presented as a *designed* lesson with exercises and a
notebook. No learner study was run, so no learning gain is claimed.

## Backup · not presented

| # | Title | Why it exists |
|---|---|---|
| 16 | Every Configuration, Not Just the Ones We Showed | Answers "did you cherry-pick P2?" — full 20-cell skill grid |
| 17 | Was the Comparison Fair? | Budget actually used (10 trials / 90 s), identical for all lanes |
| 18 | How We Caught Our Own Leak | Audit story: 0.408 reproduction, 6/6 mutation catches |
| 19 | What the Fitted Model Relies On | Permutation importance, labelled non-causal |
| 20 | Questions and Who Answers Them | Routes Q&A without guessing |

---

## What changed from the previous version

| Change | Reason |
|---|---|
| Deck reframed around one question, in five acts | Previously five disconnected technical sections |
| Title slide no longer a topic label | Opens with the challenge instead of the subject |
| Results moved after a deliberately withheld guess | Creates a reveal instead of a data dump |
| Preprocessing placed *after* the result | It now answers "why", not "also, we did this" |
| Leakage framework, hashes and software audits moved to backup | They interrupted the narrative |
| Full configuration grid moved to backup | Kept the main table readable |
| Learner-facing interpretability moved to backup | Not needed for the argument |
| Speaker load shifted: 1:20 / 3:20 / 3:40 / 6:00 / 1:40 | Two presenters get short, non-technical segments; three carry the research |
| Titles state conclusions | "More Complexity, Almost No Improvement" instead of "Results" |
