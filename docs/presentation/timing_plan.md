# Presentation Timing Plan

**Deck:** `slides/final/INT4096_Presentation.pdf` — **23 pages = 16 narrative + 5 backup + 2 references**
**Build:** `bash slides/build.sh` (0 overfull boxes, 0 missing files)
**Script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照) · **Notes:** `speaker_notes.md`
**Structure:** `storyboard.md`, from `docs/story/feature_extraction_story.md` (v2)

> **Speakers are not assigned to people here.** The talk is cut into five contiguous **voice blocks**.
> Give each member a block; the order of blocks is fixed by the story, but which person takes
> which block is free. All five members must speak `[A]`.

## Budget

| Component | Time |
|---|---|
| Formal speech (16 slides, 1,808 English words at ~105 wpm, one deliberate pause on slide 15) | **17:15** |
| Slide changes and four handovers | 0:45 |
| Q&A | 2:00 |
| **Total against the 20-minute limit** `[A]` | **20:00** |

## Act structure

| Act | Question it serves | Slides | Time |
|---|---|---|---:|
| Opening — the high-score trap | Why does a high score prove little? | 1–2 | 1:50 |
| I — Data | What did we choose, and why? | 3 | 1:10 |
| II — Processing | What can the model see? | 4–7 | 4:10 |
| III — Training | Is the comparison fair? | 8–9 | 2:00 |
| IV — Evaluation | How did a simple rule do; how certain is the gain? | 10–14 | 5:45 |
| V — Education | What do we hand to teachers? | 15–16 | 2:20 |
| **Total** | | 16 | **17:15** |

## Slide-by-slide

| # | Slide | Words | Target | Cumulative |
|---|---|---:|---:|---:|
| 1 | Learning Machine Learning Through Financial Forecasting | 91 | 0:50 | 0:50 |
| 2 | Three Questions to Ask of Any AI Score | 106 | 1:00 | 1:50 |
| 3 | Two Markets, One Protocol | 125 | 1:10 | 3:00 |
| 4 | Ten Inputs Use Only Information Available at the Close | 108 | 1:00 | 4:00 |
| 5 | Predicting the Change Gives Models a Clearer Task | 117 | 1:05 | 5:05 |
| 6 | Chronological Splits, Train-Only Fitting, a Sealed Test Block | 120 | 1:10 | 6:15 |
| 7 | How We Know the Pipeline Cannot Peek | 98 | 0:55 | 7:10 |
| 8 | Five Models, Three Mechanisms | 103 | 1:00 | 8:10 |
| 9 | Same Budget, Same Rules, Two Preprocessing Settings | 108 | 1:00 | 9:10 |
| 10 | The Opponent: Copy Today's Close | 100 | 0:55 | 10:05 |
| 11 | Best Skill Is +0.52%; 5 of 20 Runs Lose | 141 | 1:20 | 11:25 |
| 12 | All 20 Bootstrap Intervals Include Zero | 139 | 1:20 | 12:45 |
| 13 | Scaling Changes Some Models and Leaves Trees Untouched | 110 | 1:05 | 13:50 |
| 14 | Why the Gains Stay Small | 112 | 1:05 | 14:55 |
| 15 | A 60-Minute Lesson Built on the Result (includes a 10 s pause for the question) | 119 | 1:15 | 16:10 |
| 16 | The Skill Students Can Take to Any AI Claim | 111 | 1:05 | 17:15 |
| 17–23 | Backup 1–5 and References (not presented) | — | — | — |

## Voice blocks

| Block | Slides | Content | Time | Share |
|---|---|---|---:|---:|
| A | 1–3 | Hook, three questions, data | **3:00** | 17% |
| B | 4–6 | Features, predict-the-change, splits | **3:15** | 19% |
| C | 7–10 | Leakage testing, models, fair budget, baseline | **3:50** | 22% |
| D | 11–13 | Results, bootstrap, scaling | **3:45** | 22% |
| E | 14–16 | Why gains are small, lesson, close | **3:25** | 20% |
| **Total** | 16 | | **17:15** | 100% |

Blocks are contiguous so each person speaks once, then hands over. Swap block order only if the story order
is preserved. Block C is the only one that crosses an act boundary (II → III → IV); its first sentence on
slide 8 and slide 10 should name the act aloud.

## Handovers (four, ~5 s each)

| After slide | Bridge sentence |
|---|---|
| 3 (A → B) | "Now, what goes into the model?" |
| 6 (B → C) | "But how do we know the pipeline cannot peek?" |
| 10 (C → D) | "So, the results." |
| 13 (D → E) | "So why do the gains stay so small?" |

## If you are running long

Check the clock at the **end of slide 9**: it should read **≈9:10**.

- **9:40 or later:** cut slide 14 to two sentences — *"Returns barely predict themselves, and the rule
  already tracks the price level. A tie is plausible."* Saves ~0:30.
- **10:10 or later:** also name the five models on slide 8 in one breath, without the teaching
  questions. Saves ~0:25.
- **Never cut** slide 10 (the baseline) or slide 11 (the results table figure): the evaluation argument
  carries most of the marks.

## If you are running short

Add detail that is already prepared: the grid-edge caveat from Backup 2 on slide 9, or the Friday/Monday
walkthrough from Backup 3 on slide 6.

## Rehearsal checklist

- [ ] Two full timed run-throughs with a visible clock.
- [ ] All four handovers rehearsed, they are where time leaks.
- [ ] Slide 1 and slide 16 disclaimer stays visible while the sentence is spoken.
- [ ] Backup 1 and Backup 3 are open in a second window, ready for "did you cherry-pick?" and
      "how do you know there's no leakage?".
- [ ] Nobody says "every number is from validation": say "every **model-performance** number".
- [ ] Deck tested on the presentation machine (16:9, figures embedded).
