# Slide Storyboard — Three Questions, Five Acts

**Deck:** `slides/latex/main.tex` → `slides/final/INT4096_Presentation.pdf`
**Slides:** 16 narrative + 5 backup + 2 reference pages (23 pages) · **Speech:** 17:15 of a 20:00 slot
**Structure source:** `docs/story/feature_extraction_story.md` (v2) — change the story first, then the script, then the deck.
**Companions:** `timing_plan.md` (clock, voice blocks) · `speaker_script_bilingual.md` (words to say) · `speaker_notes.md` (key messages, Q&A routing)

> **Speakers are not named.** The deck footer shows the act and page only. Who speaks which
> block is decided in `timing_plan.md`; every one of the five members must speak `[A]`.
> Research ownership: `docs/management/responsibilities.md`.

---

## The spine

The deck follows the project pipeline (data → processing → training → evaluation → education), and the
audience is given three questions up front that each act answers.

| Question | Where answered |
|---|---|
| Q1 What information could the model see? | Act I data, Act II processing |
| Q2 How well did a simple rule do on the same examples? | Act III training (fair opponent), Act IV evaluation |
| Q3 How certain is the improvement? | Act IV bootstrap intervals, scaling ablation |
| Teaching it | Act V |

**Deliberate choice:** slide 1 shows the R² hook (SVR 0.9556 vs copy-yesterday 0.9555) and **no results
table**. The audience holds the guess until Act IV.

## Opening — The high-score trap

| # | Title | Message | Visual |
|---|---|---|---|
| 1 | Learning Machine Learning Through Financial Forecasting | A fancy model and a copy-paste rule score the same R² | Two large numbers, disclaimer line |
| 2 | Three Questions to Ask of Any AI Score | The three questions are the talk's spine and the lesson's goal | Numbered questions + where-answered table + audience block |

## Act I — Data

| # | Title | Message | Visual |
|---|---|---|---|
| 3 | Two Markets, One Protocol | Two calendars as a robustness check; checks reject, not repair; BTC is one venue | Comparison table (source, window, n, close range, quality) + four bullets |

## Act II — Processing

| # | Title | Message | Visual |
|---|---|---|---|
| 4 | Ten Inputs Use Only Information Available at the Close | Ten backward-looking features, tested; no price level | Feature-group table |
| 5 | Predicting the Change Gives Models a Clearer Task | Predict ΔP, add it to the known close; the design was forced by a failed first run | Formula + one real validation row (model error 1.25 vs persistence 1.35) |
| 6 | Chronological Splits, Train-Only Fitting, a Sealed Test Block | Purge a row at each boundary; fit scaling on train only; test sealed | Timeline + date table + three bullets |
| 7 | How We Know the Pipeline Cannot Peek | Audit found a leak; six injected defects must all be caught | Two audit blocks + numbered defect list |

## Act III — Training

| # | Title | Message | Visual |
|---|---|---|---|
| 8 | Five Models, Three Mechanisms | Chosen for mechanism contrast; each teaches one question | Model / how it predicts / question table |
| 9 | Same Budget, Same Rules, Two Preprocessing Settings | Fairness enforced in code; tuning never sees validation; P0 vs P2 | Bullets + P0/P2 blocks + "5×2×2 = 20 runs" |

## Act IV — Evaluation

| # | Title | Message | Visual |
|---|---|---|---|
| 10 | The Opponent: Copy Today's Close | Baseline, skill score, why not R² | Skill formula + persistence MAE block + R² alert |
| 11 | Best Skill Is +0.52%; 5 of 20 Runs Lose | The range is tiny; some runs lose; no cherry-picking | Skill bar chart (P2), one caption |
| 12 | All 20 Bootstrap Intervals Include Zero | Tie, not a winner; 244/358 validation days | Forest plot, caption |
| 13 | Scaling Changes Some Models and Leaves Trees Untouched | Preprocessing changes behaviour, not necessarily accuracy | Three notes + ablation chart |
| 14 | Why the Gains Stay Small | Near-zero return correlation; rule already tracks level; one diagnostic, not proof | 100/101/100 illustration + two bullets |

**Wording discipline.** Say *some configurations are slightly better*. Never say a model *won*, never
say standardisation *improved* prediction, never say there is *no signal*. Every **model-performance**
number is validation; only the dataset sizes and the return-correlation diagnostic use the full price
history.

## Act V — Education

| # | Title | Message | Visual |
|---|---|---|---|
| 15 | A 60-Minute Lesson Built on the Result | Lesson package + a live check (answer B); no learner study | Package list + A/B/C question block |
| 16 | The Skill Students Can Take to Any AI Claim | Three questions; limits; disclaimer | Questions + limits column + disclaimer |

## Backup — not presented

| # | Title | Use it when |
|---|---|---|
| 17 | Backup 1: Full 20-Run Transparency Matrix | "Did you cherry-pick P2?" → all 20 cells; best BTC overall is linear baseline P0, +0.26% |
| 18 | Backup 2: Experimental Fairness and Manifest Audit | "Was the budget fair?" → identical features/splits/budget; tuning inside train only; grid-edge caveat |
| 19 | Backup 3: Why One Row Is Dropped at Each Boundary | "How do you know there's no leakage?" → mechanism, 0.408, six defects |
| 20 | Backup 4: What Signals Did the Models Rely On? | "Which features mattered?" → permutation importance, explicitly non-causal |
| 21 | Backup 5: Q&A Quick-Reference Cards | Six prepared one-line answers (incl. "why only P0 and P2?") |
| 22–23 | References | Bibliography generated from `reports/latex/references.bib` |

---

## What changed from the previous deck, and why

| Change | Reason |
|---|---|
| Reordered from reveal-style (puzzle → fair experiment → verdict → why) to the story's pipeline (data → processing → training → evaluation → education) | `docs/story/feature_extraction_story.md` v2 is now the source of truth; the pipeline also mirrors the rubric categories |
| Added the **three questions** as spine, repeated on slides 2 and 16 | One memorable frame that ties every act and the lesson together |
| Previous script, storyboard and `main.tex` had drifted apart (different slide titles and order) | One structure now, in all three |
| Leakage mutation testing moved from backup to main (slide 7) | It is a headline strength (rubric: programming and evaluation) and part of the story |
| New slide 9: tuning protocol (inside-train CV, identical budget) | Corrects the old claim that tuning used the validation set; answers "was it fair?" in the main flow |
| Slide 3 merges data selection, window and quality gate | Frees time for processing and training |
| Speaker names removed from footer and script | Speaking order is still open; voice blocks replace names |
| Title of the results slide now states the range and the 5 of 20 losses | "Saved 1.5 cents per forecast" over-claimed given intervals that include zero |
| "Near-unregularised" label dropped | The linear lane is a ridge with tuned α (selected 10); the old name was misleading |
| Dropped the untested "forests cannot extrapolate" claim | Not measured; slide 14 now states only what the artifacts support |
| Lesson slide no longer says "Why Smart Models Still Lose" | 15 of 20 runs were slightly ahead; the honest finding is a tie, not a loss |
