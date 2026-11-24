# Presentation Timing Plan

**Deck:** `slides/final/INT4096_Presentation.pdf` — **24 pages = 17 narrative + 5 backup + 2 references**
**Build:** `bash slides/build.sh` (0 overfull vertical boxes, 0 missing files)
**Script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照) · **Notes:** `speaker_notes.md`
**Structure:** `storyboard.md`, from `docs/story/feature_extraction_story.md`

> **Speakers.** Dong Yuankun: slides 1–5 · Zhang Yancheng: 6–12 · Zhang Haoyu: 13–15 ·
> Lau Pak Hei: 16 · Lui Shing Lam: 17. All five members speak `[A]`. Names also appear in each slide's footer.

## Budget

| Component | Time |
|---|---|
| Formal speech (17 slides, 1,759 English words at ~105 wpm) | **16:50** |
| Slide changes and four handovers | 0:40 |
| Q&A | 2:00 |
| **Planned total** (0:30 of slack inside the 20-minute limit `[A]`) | **19:30** |

## Part structure

| Part | Question it answers | Slides | Time |
|---|---|---|---:|
| Introduction | What is the question, and what is the route? | 1–2 | 1:30 |
| 1 — Data Selection | Which data, from where, why, and which rows qualify? | 3–5 | 3:05 |
| 2 — Processing & Features | What problems did raw data have, and what can the model see? | 6–9 | 4:25 |
| 3 — Models & Tuning | Which models, why, and tuned how fairly? | 10–12 | 3:10 |
| 4 — Evaluation | Which metrics, what results, how certain? | 13–15 | 2:50 |
| 5 — Teaching Design | How does the project become a lesson, and what did each stage deliver? | 16–17 | 1:50 |
| **Total** | | 17 | **16:50** |

## Slide-by-slide

| # | Slide | Words | Target | Cumulative |
|---|---|---:|---:|---:|
| 1 | Learning Machine Learning Through Financial Forecasting | 72 | 0:40 | 0:40 |
| 2 | Roadmap: One Pipeline, Five Stages | 85 | 0:50 | 1:30 |
| 3 | What We Used, and Exactly Where It Came From | 89 | 0:50 | 2:20 |
| 4 | Why These Two: Two Markets With Different Characteristics | 117 | 1:05 | 3:25 |
| 5 | Selection Conditions: From Raw Bars to Modelling Rows | 120 | 1:10 | 4:35 |
| 6 | Problems in the Raw Data, and How We Handled Each | 97 | 0:55 | 5:30 |
| 7 | From One Day's Prices to Ten Features | 123 | 1:10 | 6:40 |
| 8 | Every Model Gets the Same Data: One Shared Pipeline | 138 | 1:20 | 8:00 |
| 9 | Chronological Split, and Proof That the Pipeline Cannot Peek | 101 | 1:00 | 9:00 |
| 10 | Five Models Plus a Baseline: Why Each One Is There | 123 | 1:10 | 10:10 |
| 11 | Fine-Tuning: The Same Search and Budget for Every Model | 115 | 1:05 | 11:15 |
| 12 | What We Explored Beyond Hyperparameters | 99 | 0:55 | 12:10 |
| 13 | Four Metrics, Each With a Job | 108 | 1:00 | 13:10 |
| 14 | Results: All 20 Runs Land Within 1% of the Baseline | 95 | 0:55 | 14:05 |
| 15 | How Certain? Every Interval Includes Zero | 100 | 0:55 | 15:00 |
| 16 | Teaching Design: The Pipeline Becomes a 60-Minute Lesson | 100 | 1:00 | 16:00 |
| 17 | Summary: What Each Stage Delivered | 77 | 0:50 | 16:50 |
| 18–24 | Backup 1–5 and References (not presented) | — | — | — |

## Speakers

| Speaker | Slides | Content | Time | Share |
|---|---|---|---:|---:|
| Dong Yuankun | 1–5 | Opening (R² hook, roadmap); Part 1 data selection | **4:35** | 27% |
| Zhang Yancheng | 6–12 | Part 2 processing and features; Part 3 models, tuning, what else we explored | **7:35** | 45% |
| Zhang Haoyu | 13–15 | Part 4: metrics, results, uncertainty | **2:50** | 17% |
| Lau Pak Hei | 16 | Part 5: teaching design | **1:00** | 6% |
| Lui Shing Lam | 17 | Part 5: summary and close | **0:50** | 5% |
| **Total** | 17 | | **16:50** | 100% |

Every speaker names each part as it starts ("Part two: processing and feature engineering").

**Why Part 2 sits with Part 3.** Processing, features and the chronological split lead straight into the
models and the inner cross-validation, so one speaker carries the whole technical line from raw data to
tuned models.

**Evaluation stays with one speaker.** Slides 13–15 carry the evaluation argument and most of the
numbers, so they are not split.

**Slides 16 and 17** are written in short, plain sentences. Read them exactly as written. If either
speaker stops for more than about five seconds, **Zhang Yancheng** steps in and finishes the slide from
its 【中文要点】. Lau Pak Hei and Lui Shing Lam do not take Q&A questions.

## Handovers (four, ~5 s each)

| After slide | From → to | Bridge sentence |
|---|---|---|
| 5 | Dong Yuankun → Zhang Yancheng | "With clean rows, part two turns them into model inputs." |
| 12 | Zhang Yancheng → Zhang Haoyu | "So how well did they do? Part four." |
| 15 | Zhang Haoyu → Lau Pak Hei | "That result is exactly what we teach. Part five." |
| 16 | Lau Pak Hei → Lui Shing Lam | "Now the summary." |

## If you are running long

Check the clock at the **end of slide 5** (Dong Yuankun hands over): it should read **≈4:35**. Check again at the
**end of slide 9**: it should read **≈9:00**. Zhang Yancheng is speaking at that point and makes the cuts below himself.

- **9:30 or later:** on slide 12, drop the grid-edge sentence and say only "trees unchanged, SVR and
  ridge move". Saves ~0:20.
- **10:00 or later:** also name the five models on slide 10 with their roles only, without the classic
  strengths. Saves ~0:25.
- **Never cut** slides 13–15 (metrics, results, intervals): the evaluation argument carries most of the
  marks.

## If you are running short

Add detail that is already prepared: the Friday/Monday purge walkthrough from Backup 3 on slide 9, or
the permutation-importance reading from Backup 4 after slide 7.

## Rehearsal checklist

- [ ] Two full timed run-throughs with a visible clock.
- [ ] All four handovers rehearsed; they are where time leaks.
- [ ] Lau Pak Hei and Lui Shing Lam each read their slide aloud to Zhang Yancheng at least three times, timed.
- [ ] Zhang Yancheng can deliver slides 16 and 17 from the 【中文要点】 as the fallback.
- [ ] Backup 1 and Backup 3 are open in a second window, ready for "did you cherry-pick?" and
      "how do you know there's no leakage?".
- [ ] Say "every **model-performance** number is from validation", not "every number".
- [ ] Deck tested on the presentation machine (16:9, figures embedded, links on slide 3 readable).
