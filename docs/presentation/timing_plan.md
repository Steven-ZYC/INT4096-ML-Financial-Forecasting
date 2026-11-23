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
| Formal speech (16 slides, 1,766 English words at ~105 wpm, one deliberate pause on slide 15) | **16:50** |
| Slide changes and four handovers | 0:45 |
| Q&A | 2:00 |
| **Planned total** (25 s of slack inside the 20-minute limit `[A]`) | **19:35** |

## Act structure

| Act | Question it serves | Slides | Time |
|---|---|---|---:|
| Opening — the high-score trap | Why does a high score prove little? | 1–2 | 1:50 |
| I — Data | What did we choose, and why? | 3 | 1:05 |
| II — Processing | What can the model see? | 4–7 | 4:15 |
| III — Training | Is the comparison fair? | 8–9 | 2:00 |
| IV — Evaluation | How did a simple rule do; how certain is the gain? | 10–14 | 5:20 |
| V — Education | What do we hand to teachers? | 15–16 | 2:20 |
| **Total** | | 16 | **16:50** |

## Slide-by-slide

| # | Slide | Words | Target | Cumulative |
|---|---|---:|---:|---:|
| 1 | Learning Machine Learning Through Financial Forecasting | 91 | 0:50 | 0:50 |
| 2 | Three Questions to Ask of Any AI Score | 106 | 1:00 | 1:50 |
| 3 | Two Markets, One Protocol | 113 | 1:05 | 2:55 |
| 4 | Ten Inputs Use Only Information Available at the Close | 108 | 1:00 | 3:55 |
| 5 | Predicting the Change Gives Models a Clearer Task | 114 | 1:05 | 5:00 |
| 6 | Chronological Splits, Train-Only Fitting, a Sealed Test Block | 133 | 1:15 | 6:15 |
| 7 | How We Know the Pipeline Cannot Peek | 99 | 0:55 | 7:10 |
| 8 | Five Models, Three Mechanisms | 103 | 1:00 | 8:10 |
| 9 | Same Budget, Same Rules, Two Preprocessing Settings | 108 | 1:00 | 9:10 |
| 10 | The Opponent: Copy Today's Close | 100 | 0:55 | 10:05 |
| 11 | 20 Runs, One Yardstick: Skill Stays Within 1% of the Baseline | 123 | 1:10 | 11:15 |
| 12 | Uncertainty Measured for All 20 Runs: Parity With the Baseline | 124 | 1:10 | 12:25 |
| 13 | Scaling Effects Match What Theory Predicts | 112 | 1:05 | 13:30 |
| 14 | Why a Simple Rule Is So Hard to Beat | 104 | 1:00 | 14:30 |
| 15 | A 60-Minute Lesson Built on the Result (includes a 10 s pause for the question) | 118 | 1:15 | 15:45 |
| 16 | The Skill Students Can Take to Any AI Claim | 110 | 1:05 | 16:50 |
| 17–23 | Backup 1–5 and References (not presented) | — | — | — |

## Voice blocks

| Block | Slides | Content | Time | Share |
|---|---|---|---:|---:|
| A | 1–3 | Hook, three questions, data | **2:55** | 17% |
| B | 4–6 | Features, predict-the-change, splits | **3:20** | 20% |
| C | 7–10 | Leakage testing, models, fair budget, baseline | **3:50** | 23% |
| D | 11–13 | Results, uncertainty, scaling | **3:25** | 20% |
| E | 14–16 | Why a simple rule is hard to beat, lesson, close | **3:20** | 20% |
| **Total** | 16 | | **16:50** | 100% |

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
  already tracks the price level. That is why a strong baseline is the right yardstick."* Saves ~0:30.
- **10:10 or later:** also name the five models on slide 8 in one breath, without the teaching
  questions. Saves ~0:25.
- **Never cut** slide 10 (the baseline) or slide 11 (the results figure): the evaluation argument
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
- [ ] Say "every **model-performance** number is from validation", not "every number".
- [ ] Deck tested on the presentation machine (16:9, figures embedded).
