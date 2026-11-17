# Presentation Timing Plan

**Deck:** `slides/final/INT4096_Presentation.pdf` — **21 pages = 16 narrative + 5 backup**
**Build:** `bash slides/build.sh` (0 overfull boxes, 0 missing files)
**Bilingual script:** `speaker_script_bilingual.md` / `.pdf` (English spoken, 中文对照)
**Key messages and transitions:** `speaker_notes.md`

> **Scope note.** These are **presentation roles only**. They describe who speaks,
> not who wrote the code or owns the research. Actual ownership is in
> `docs/management/responsibilities.md`.

## Budget

| Component | Time |
|---|---|
| Formal speech (16 slides) | **17:30** |
| Slide changes and handovers | 0:30 |
| Q&A | 2:00 |
| **Total against the 20-minute limit** | **20:00** |

## Act structure

| Act | Question it answers | Slides | Presenters | Time |
|---|---|---|---|---|
| I — The Challenge | Why use market data to teach ML? | 1–2 | Pak Hei, Haoyu | 1:55 |
| II — Designing a Fair Experiment | How do we build a zero-leakage, fair benchmark? | 3–9 | Yuankun, Haoyu, Pak Hei | 7:25 |
| III — The Reveal | What did five classical models actually achieve? | 10–11 | Yancheng | 2:35 |
| IV — Investigating Why | Why didn't complexity or preprocessing break through? | 12–13 | Yancheng | 2:20 |
| V — The Bigger Lesson | What is the transferable lesson and teaching product? | 14–16 | Yancheng, Yuankun, Shing Lam | 3:15 |

## Slide-by-slide

| # | Slide | Presenter | Target | Cumulative |
|---|---|---|---:|---:|
| 1 | Can Five Machine-Learning Models Beat a One-Line Rule? | Lau Pak Hei | 0:40 | 0:40 |
| 2 | Why Use Market Data to Teach Machine Learning? | Zhang Haoyu | 1:15 | 1:55 |
| 3 | Two Markets, One Rigorous Protocol | Dong Yuankun | 1:00 | 2:55 |
| 4 | Framing the Prediction Target for Fair Learning | Zhang Haoyu | 1:00 | 3:55 |
| 5 | Pre-Committed Questions, Zero Cherry-Picking | Zhang Haoyu | 1:00 | 4:55 |
| 6 | Ten Signals from the Past | Dong Yuankun | 1:05 | 6:00 |
| 7 | Chronological Splitting and Zero-Leakage Discipline | Dong Yuankun | 1:15 | 7:15 |
| 8 | Five Classical Models Across Three Paradigms | Lau Pak Hei | 1:05 | 8:20 |
| 9 | The Opponent Everyone Forgets | Lau Pak Hei | 1:00 | 9:20 |
| 10 | The Verdict: Complexity Yields Almost Zero Gain | Zhang Yancheng | 1:25 | 10:45 |
| 11 | Statistical Reality Check: Every Gain Sits Inside the Noise | Zhang Yancheng | 1:10 | 11:55 |
| 12 | Does Preprocessing Save the Models? | Zhang Yancheng | 1:20 | 13:15 |
| 13 | Why Complexity Hit a Wall: Signal and Structure | Zhang Yancheng | 1:00 | 14:15 |
| 14 | From Research Finding to a Turnkey Classroom Lab | Zhang Yancheng | 0:50 | 15:05 |
| 15 | Engineering and Pedagogical Takeaways | Dong Yuankun | 1:10 | 16:15 |
| 16 | Study Boundaries and the Bigger Lesson | Lui Shing Lam | 1:15 | 17:30 |
| 17–21 | Backup 1–5 (not presented) | — | — | — |

## Per-presenter totals

| Presenter | Slides | Time | Share |
|---|---|---:|---:|
| Lau Pak Hei | 1, 8, 9 | **2:45** | 16% |
| Zhang Haoyu | 2, 4, 5 | **3:15** | 19% |
| Dong Yuankun | 3, 6, 7, 15 | **4:30** | 26% |
| Zhang Yancheng | 10–14 | **5:45** | 33% |
| Lui Shing Lam | 16 | **1:15** | 7% |
| **Total** | 16 | **17:30** | 100% |

**Note on continuity:** Yancheng's five slides are one uninterrupted segment
(Act III into Act IV). The other presenters appear in two blocks each, which the
handover plan below accounts for — each block ends on a sentence that hands over
cleanly.

## Handovers (six, ~5 s each)

| After | From → To | Bridge sentence |
|---|---|---|
| 1 | Pak Hei → Haoyu | "That is the question. Haoyu will explain why this dataset is the right place to test it." |
| 5 | Haoyu → Yuankun | "None of that means anything if the model can see the future — Yuankun." |
| 7 | Yuankun → Pak Hei | "So the data is clean. Pak Hei will show what we actually put on top of it." |
| 9 | Pak Hei → Yancheng | "We have the models and the benchmark. Yancheng has the results." |
| 14 | Yancheng → Yuankun | "That is what the numbers say. Yuankun on what we learned building this." |
| 15 | Yuankun → Shing Lam | "Shing Lam will close with our boundaries and the bigger lesson." |

## If you are running long

Check the clock at slide 10: it should read **≈10:45**.

- **At 11:15 or later:** cut slide 13 to one sentence — *"returns barely predict
  themselves, so extra capacity fits noise; a forest also averages leaf values,
  so it cannot produce large moves."* Saves ~0:40.
- **At 11:45 or later:** also compress slide 8 by naming the three paradigms in
  one breath instead of walking the table. Saves ~0:30.
- **Never cut** slide 9 (the baseline definition) or slide 10 (the results
  table): the evaluation argument carries most of the marks.

## If you are running short

Add detail that is already prepared: the boundary-purge mechanism on slide 7, or
the threshold-versus-distance mechanism on slide 12.

## Rehearsal checklist

- [ ] Two full timed run-throughs with a visible clock.
- [ ] All six handovers rehearsed — they are where time leaks.
- [ ] Slide 1 disclaimer stays visible while the first sentence is spoken.
- [ ] Backup 1 and Backup 3 are open in a second window, ready for "did you
      cherry-pick?" and "how do you know there's no leakage?".
- [ ] Deck tested on the presentation machine (16:9, figures embedded).
