# Presentation Timing Plan

**Deck:** `deliverables/presentation/INT4096_Presentation.pdf` — **26 pages = 18 narrative + 6 backup + 2 references**
**Build:** `bash deliverables/presentation/slides/build.sh` (0 overfull vertical boxes, 0 missing files)
**Script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照) · **Notes:** `speaker_notes.md`
**Structure:** `storyboard.md`, from `deliverables/presentation/planning/feature_extraction_story.md`

> **Speakers.** Dong Yuankun: slides 1–5 · Zhang Yancheng: 6–12 · Zhang Haoyu: 13–15 ·
> Lau Pak Hei: 16–17 · Lui Shing Lam: 18. All five members speak `[A]`. Names also appear in each slide's footer.

## Budget

| Component | Time |
|---|---|
| Formal speech (18 slides, 1,761 English words at ~105 wpm) | **16:55** |
| Slide changes and four handovers | 0:40 |
| Q&A | 2:00 |
| **Planned total** (0:25 of slack inside the 20-minute limit `[A]`) | **19:35** |

## Part structure

| Part | Question it answers | Slides | Time |
|---|---|---|---:|
| Introduction | What is the question, and what is the route? | 1–2 | 2:15 |
| 1 — Data Selection | Which data, from where, why, and which rows qualify? | 3–5 | 2:35 |
| 2 — Processing & Features | What problems did raw data have, and what can the model see? | 6–9 | 4:20 |
| 3 — Models & Tuning | Which models, why, and tuned how fairly? | 10–12 | 2:50 |
| 4 — Evaluation | Which metrics, what results, how certain? | 13–15 | 2:50 |
| 5 — Teaching Design | How does the project become a lesson, where can people try it, and what did each stage deliver? | 16–18 | 2:05 |
| **Total** | | 18 | **16:55** |

## Slide-by-slide

| # | Slide | Words | Target | Cumulative |
|---|---|---:|---:|---:|
| 1 | Learning Machine Learning Through Financial Forecasting | 160 | 1:30 | 1:30 |
| 2 | Roadmap: One Pipeline, Five Stages | 78 | 0:45 | 2:15 |
| 3 | What We Used, and Exactly Where It Came From | 58 | 0:35 | 2:50 |
| 4 | Why These Two: Two Markets With Different Characteristics | 93 | 0:55 | 3:45 |
| 5 | Selection Conditions: From Raw Bars to Modelling Rows | 115 | 1:05 | 4:50 |
| 6 | Problems in the Raw Data, and How We Handled Each | 107 | 1:00 | 5:50 |
| 7 | From One Day's Prices to Ten Features | 129 | 1:15 | 7:05 |
| 8 | Every Model Gets the Same Data: One Shared Pipeline | 123 | 1:10 | 8:15 |
| 9 | Chronological Split, and Proof That the Pipeline Cannot Peek | 95 | 0:55 | 9:10 |
| 10 | Five Models Plus a Baseline: Why Each One Is There | 113 | 1:05 | 10:15 |
| 11 | Fine-Tuning: The Same Search and Budget for Every Model | 106 | 1:00 | 11:15 |
| 12 | What We Explored Beyond Hyperparameters | 76 | 0:45 | 12:00 |
| 13 | Four Metrics, Each With a Job | 111 | 1:05 | 13:05 |
| 14 | Results: All 20 Runs Land Within 1% of the Baseline | 85 | 0:50 | 13:55 |
| 15 | How Certain? Every Interval Includes Zero | 97 | 0:55 | 14:50 |
| 16 | Teaching Design: The Pipeline Becomes a 60-Minute Lesson | 89 | 0:50 | 15:40 |
| 17 | Try It Yourself: The Whole Pipeline, Interactive | 49 | 0:30 | 16:10 |
| 18 | Summary: What Each Stage Delivered | 77 | 0:45 | 16:55 |
| 19–26 | Backup 1–6 and References (not presented) | — | — | — |

## Speakers

| Speaker | Slides | Content | Time | Share |
|---|---|---|---:|---:|
| Dong Yuankun | 1–5 | Opening (R² hook, roadmap); Part 1 data selection | **4:50** | 29% |
| Zhang Yancheng | 6–12 | Part 2 processing and features; Part 3 models, tuning, what else we explored | **7:10** | 42% |
| Zhang Haoyu | 13–15 | Part 4: metrics, results, uncertainty | **2:50** | 17% |
| Lau Pak Hei | 16–17 | Part 5: teaching design; the interactive website | **1:20** | 8% |
| Lui Shing Lam | 18 | Part 5: summary and close | **0:45** | 4% |
| **Total** | 18 | | **16:55** | 100% |

Every speaker names each part as it starts ("Part two: processing and feature engineering").

**Why Part 2 sits with Part 3.** Processing, features and the chronological split lead straight into the
models and the inner cross-validation, so one speaker carries the whole technical line from raw data to
tuned models.

**Evaluation stays with one speaker.** Slides 13–15 carry the evaluation argument and most of the
numbers, so they are not split.

**Slides 16–18** are written in short, plain sentences. Read them exactly as written. If either
speaker stops for more than about five seconds, **Zhang Yancheng** steps in and finishes the slide from
the fallback key points at the end of Part 5 in the script. Lau Pak Hei and Lui Shing Lam do not take Q&A questions.

## Handovers (four, ~5 s each)

| After slide | From → to | Bridge sentence |
|---|---|---|
| 5 | Dong Yuankun → Zhang Yancheng | "With our data selected and prepared, we can now move on to Processing and Feature Engineering." |
| 12 | Zhang Yancheng → Zhang Haoyu | "So, how well did all these models do? Zhang Haoyu will show you." |
| 15 | Zhang Haoyu → Lau Pak Hei | "And that is exactly what our lesson teaches." |
| 17 | Lau Pak Hei → Lui Shing Lam | "Scan the code to try it." (Lui Shing Lam opens with "To sum up.") |

## If you are running long

Check the clock at the **end of slide 5** (Dong Yuankun hands over): it should read **≈4:50**. Check again at the
**end of slide 9**: it should read **≈9:10**. Zhang Yancheng is speaking at that point and makes the cuts below himself.

- **9:40 or later:** drop the neural-network sentence on slide 10 and the "target" sentence on slide 12.
  Saves ~0:20.
- **10:10 or later:** also skip the "For example…" fold walkthrough on slide 11. Saves ~0:10.
- **Never cut** slides 13–15 (metrics, results, intervals): the evaluation argument carries most of the
  marks.

## If you are running short

Add detail that is already prepared: the Friday/Monday purge walkthrough from Backup 3 on slide 9, or
the permutation-importance reading from Backup 4 after slide 7.

## Rehearsal checklist

- [ ] Two full timed run-throughs with a visible clock.
- [ ] All four handovers rehearsed; they are where time leaks.
- [ ] Lau Pak Hei and Lui Shing Lam each read their slides aloud to Zhang Yancheng at least three times, timed.
- [ ] Zhang Yancheng can deliver slides 16–18 from the fallback key points (end of Part 5 in the script).
- [ ] Backup 1 and Backup 3 are open in a second window, ready for "did you cherry-pick?" and
      "how do you know there's no leakage?".
- [ ] Say "every **model-performance** number is from validation", not "every number".
- [ ] Deck tested on the presentation machine (16:9, figures embedded, links on slide 3 readable).
