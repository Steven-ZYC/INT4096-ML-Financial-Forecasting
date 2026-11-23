# Presentation Timing Plan

**Deck:** `slides/final/INT4096_Presentation.pdf` — **24 pages = 17 narrative + 5 backup + 2 references**
**Build:** `bash slides/build.sh` (0 overfull vertical boxes, 0 missing files)
**Script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照) · **Notes:** `speaker_notes.md`
**Structure:** `storyboard.md`, from `docs/story/feature_extraction_story.md`

> **Speakers are not assigned to people here.** The talk is cut into five **voice blocks**, one per
> pipeline stage. Block E opens and closes the talk. Give each member a block; all five members must
> speak `[A]`.

## Budget

| Component | Time |
|---|---|
| Formal speech (17 slides, 1,728 English words at ~105 wpm) | **16:25** |
| Slide changes and five handovers | 0:50 |
| Q&A | 2:00 |
| **Planned total** (0:45 of slack inside the 20-minute limit `[A]`) | **19:15** |

## Part structure

| Part | Question it answers | Slides | Time |
|---|---|---|---:|
| Introduction | What is the question, and what is the route? | 1–2 | 1:30 |
| 1 — Data Selection | Which data, from where, why, and which rows qualify? | 3–5 | 3:05 |
| 2 — Processing & Features | What problems did raw data have, and what can the model see? | 6–9 | 3:50 |
| 3 — Models & Tuning | Which models, why, and tuned how fairly? | 10–12 | 3:10 |
| 4 — Evaluation | Which metrics, what results, how certain? | 13–15 | 2:50 |
| 5 — Teaching Design | How does the project become a lesson, and what did each stage deliver? | 16–17 | 2:00 |
| **Total** | | 17 | **16:25** |

## Slide-by-slide

| # | Slide | Words | Target | Cumulative |
|---|---|---:|---:|---:|
| 1 | Learning Machine Learning Through Financial Forecasting | 72 | 0:40 | 0:40 |
| 2 | Roadmap: One Pipeline, Five Stages | 85 | 0:50 | 1:30 |
| 3 | What We Used, and Exactly Where It Came From | 89 | 0:50 | 2:20 |
| 4 | Why These Two: Two Markets With Different Characteristics | 117 | 1:05 | 3:25 |
| 5 | Selection Conditions: From Raw Bars to Modelling Rows | 120 | 1:10 | 4:35 |
| 6 | Problems in the Raw Data, and How We Handled Each | 113 | 1:05 | 5:40 |
| 7 | Ten Features, Built Only From Information Available at the Close | 89 | 0:50 | 6:30 |
| 8 | Engineering the Target: Predict the Change, Then Add It Back | 92 | 0:55 | 7:25 |
| 9 | Chronological Split, and Proof That the Pipeline Cannot Peek | 101 | 1:00 | 8:25 |
| 10 | Five Models Plus a Baseline: Why Each One Is There | 123 | 1:10 | 9:35 |
| 11 | Fine-Tuning: The Same Search and Budget for Every Model | 115 | 1:05 | 10:40 |
| 12 | What We Explored Beyond Hyperparameters | 99 | 0:55 | 11:35 |
| 13 | Four Metrics, Each With a Job | 108 | 1:00 | 12:35 |
| 14 | Results: All 20 Runs Land Within 1% of the Baseline | 95 | 0:55 | 13:30 |
| 15 | How Certain? Every Interval Includes Zero | 100 | 0:55 | 14:25 |
| 16 | Teaching Design: The Pipeline Becomes a 60-Minute Lesson | 122 | 1:10 | 15:35 |
| 17 | Summary: What Each Stage Delivered | 88 | 0:50 | 16:25 |
| 18–24 | Backup 1–5 and References (not presented) | — | — | — |

## Voice blocks

| Block | Slides | Content | Time | Share |
|---|---|---|---:|---:|
| E | 1–2, 16–17 | R² hook and roadmap; teaching design and summary | **3:30** | 21% |
| A | 3–5 | Part 1: data, sources, why two markets, selection conditions | **3:05** | 19% |
| B | 6–9 | Part 2: raw-data problems, features, change target, split and leakage checks | **3:50** | 23% |
| C | 10–12 | Part 3: models, tuning protocol, what else we explored | **3:10** | 19% |
| D | 13–15 | Part 4: metrics, results, uncertainty | **2:50** | 17% |
| **Total** | 17 | | **16:25** | 100% |

Each block is one part of the pipeline, so every speaker opens by naming their part ("Part two:
processing and feature engineering").

## Handovers (five, ~5 s each)

| After slide | From → to | Bridge sentence |
|---|---|---|
| 2 | E → A | "Part one: the data." |
| 5 | A → B | "With clean rows, part two turns them into model inputs." |
| 9 | B → C | "Clean inputs, so part three: the models." |
| 12 | C → D | "So how well did they do? Part four." |
| 15 | D → E | "That result is exactly what we teach. Part five." |

## If you are running long

Check the clock at the **end of slide 9**: it should read **≈8:25**.

- **8:55 or later:** on slide 12, drop the grid-edge sentence and say only "trees unchanged, SVR and
  ridge move". Saves ~0:20.
- **9:25 or later:** also name the five models on slide 10 with their roles only, without the classic
  strengths. Saves ~0:25.
- **Never cut** slides 13–15 (metrics, results, intervals): the evaluation argument carries most of the
  marks.

## If you are running short

Add detail that is already prepared: the Friday/Monday purge walkthrough from Backup 3 on slide 9, or
the permutation-importance reading from Backup 4 after slide 7.

## Rehearsal checklist

- [ ] Two full timed run-throughs with a visible clock.
- [ ] All five handovers rehearsed; they are where time leaks.
- [ ] Each speaker names their part when they start.
- [ ] Backup 1 and Backup 3 are open in a second window, ready for "did you cherry-pick?" and
      "how do you know there's no leakage?".
- [ ] Say "every **model-performance** number is from validation", not "every number".
- [ ] Deck tested on the presentation machine (16:9, figures embedded, links on slide 3 readable).
