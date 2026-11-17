# Presentation Timing Plan

**Deck:** `slides/final/INT4096_Presentation.pdf` — 20 pages = **15 narrative slides + 5 backup**
**Build:** `bash slides/build.sh`
**Bilingual script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照) (0 overfull boxes, 0 missing files)
**Content time:** **16:00** of speech, leaving ~4:00 inside the 20-minute limit for
transitions, slower delivery and questions.

> **Scope note.** The roles below are **presentation roles only**. They are not
> statements about who wrote which code, ran which experiment or owns which
> research question — that is recorded separately in
> `docs/management/responsibilities.md`.

## Narrative arc

| Act | Question it answers | Presenter | Time |
|---|---|---|---|
| I — The challenge | Which would you trust: five models, or one line? | Lau Pak Hei | 1:20 |
| II — Designing a fair experiment | How do we compare them without cheating? | Zhang Haoyu, Dong Yuankun | 7:00 |
| III — The reveal | What actually happened? | Zhang Yancheng | 3:35 |
| IV — Investigating why | Why didn't complexity help? | Zhang Yancheng | 2:25 |
| V — The bigger lesson | What does this teach us? | Lui Shing Lam | 1:40 |

## Slide-by-slide timing

| # | Slide | Presenter | Target | Cumulative |
|---|---|---|---:|---:|
| 1 | Can Five Machine-Learning Models Beat a One-Line Rule? | Lau Pak Hei | 0:25 | 0:25 |
| 2 | Which Would You Trust? | Lau Pak Hei | 0:55 | 1:20 |
| 3 | Two Markets, One Fair Test | Zhang Haoyu | 1:05 | 2:25 |
| 4 | What We Are Actually Predicting | Zhang Haoyu | 1:20 | 3:45 |
| 5 | Four Questions, Fixed Before We Looked | Zhang Haoyu | 0:55 | 4:40 |
| 6 | Only the Past Is Visible | Dong Yuankun | 1:20 | 6:00 |
| 7 | Splitting Time Without Cheating | Dong Yuankun | 0:55 | 6:55 |
| 8 | Ten Signals from the Past | Dong Yuankun | 1:25 | 8:20 |
| 9 | What Must Our Models Beat? | Zhang Yancheng | 1:05 | 9:25 |
| 10 | More Complexity, Almost No Improvement | Zhang Yancheng | 1:30 | 10:55 |
| 11 | The Improvements Are Inside the Noise | Zhang Yancheng | 1:00 | 11:55 |
| 12 | Does Changing the Input Change the Answer? | Zhang Yancheng | 1:30 | 13:25 |
| 13 | Why More Complexity Did Not Help | Zhang Yancheng | 0:55 | 14:20 |
| 14 | What This Teaches Us About Machine Learning | Lui Shing Lam | 0:50 | 15:10 |
| 15 | The Value Is in the Comparison | Lui Shing Lam | 0:50 | 16:00 |
| 16–20 | Backup: full table, fairness, leak audit, feature importance, Q&A owners | (not presented) | — | 16:00 |

## Per-presenter totals

| Presenter | Slides | Time | Share of content |
|---|---|---:|---:|
| Lau Pak Hei | 1–2 | **1:20** | 8% |
| Zhang Haoyu | 3–5 | **3:20** | 21% |
| Dong Yuankun | 6–8 | **3:40** | 23% |
| Zhang Yancheng | 9–13 | **6:00** | 37% |
| Lui Shing Lam | 14–15 | **1:40** | 10% |
| **Total** | 15 | **16:00** | 100% |

Pak Hei and Shing Lam each speak for under two minutes and handle no technical
explanation, no chart reading and no algorithm internals. Haoyu, Yuankun and
Yancheng carry all substantive research content.

Zhang Yancheng's five slides are **one continuous segment** (Act III runs straight
into Act IV), so there is no mid-argument speaker switch.

## Handover discipline

There are only four handovers, and each is a technical bridge rather than
"over to you":

| Transition | Bridge sentence |
|---|---|
| Pak Hei → Haoyu (after slide 2) | "…so we need a comparison we can defend. Haoyu will show what we actually set up." |
| Haoyu → Yuankun (after slide 5) | "None of those questions means anything if the model can see the future — Yuankun explains how we prevented that." |
| Yuankun → Yancheng (after slide 8) | "So we have honest data and honest features. Yancheng will show what the models did with them." |
| Yancheng → Shing Lam (after slide 13) | "That is the technical story. Shing Lam will say what it means for learning." |

## If you are running long

Check the clock at slide 10 (should be ≈11:00).

- **At 11:30 or later:** cut slide 13 to one sentence ("daily returns barely
  predict themselves, so extra capacity fits noise") — saves ~0:40.
- **At 12:00 or later:** also shorten slide 3 to the two-market contrast only —
  saves ~0:30.
- **Never cut** slide 9 (the baseline) or slide 10 (the results table). The
  evaluation argument carries most of the marks.

## If you are running short

Add the mechanism behind the tree-invariance result on slide 12 (thresholds vs
distances), which is prepared in the speaker notes as an optional expansion.

## Rehearsal checklist

- [ ] Two timed run-throughs with a visible clock.
- [ ] Each presenter has said their own segment aloud at least twice.
- [ ] Handover sentences rehearsed — they are the most common place to lose time.
- [ ] Slide 1 disclaimer stays on screen while the first sentence is spoken.
- [ ] Test the PDF on the presentation machine (fonts, 16:9, no missing figures).
