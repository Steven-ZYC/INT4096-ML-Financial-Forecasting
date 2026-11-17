# Slide Storyboard — Five-Act Research Story

**Deck:** `slides/latex/main.tex` → `slides/final/INT4096_Presentation.pdf`
**Slides:** 16 narrative + 5 backup (21 pages) · **Speech:** 17:30 of a 20:00 slot
**Companions:** `timing_plan.md` (clock) · `speaker_script_bilingual.md` (full
script, English spoken · 中文对照) · `speaker_notes.md` (key messages, transitions)

> **Presentation roles only.** Speaker assignments describe who talks, not who
> built what. Research ownership: `docs/management/responsibilities.md`.

---

## The spine

One question, five acts, each act creating the need for the next:

| Act | Question raised | Answered by |
|---|---|---|
| **I** | Five models or one line — which would you trust? | Framing the teaching purpose and the three traps |
| **II** | How do we compare them without cheating? | Two markets, the delta target, pre-registered questions, ten features, chronological splits, five paradigms, the baseline |
| **III** | What actually happened? | Validation skill table + bootstrap interval forest plot |
| **IV** | Why didn't complexity or scaling break through? | P0/P2 ablation + near-zero signal / leaf-averaging limits |
| **V** | What is transferable, and what do we hand to teachers? | Classroom lab, engineering takeaways, boundaries, final line |

---

## Act I — The Challenge

| # | Title | Presenter | Message | Visual |
|---|---|---|---|---|
| 1 | Can Five Machine-Learning Models Beat a One-Line Rule? | Lau Pak Hei | The whole talk in one comparison | Dark hero: five model chips **vs** `P̂(t+1) = P(t)` |
| 2 | Why Use Market Data to Teach Machine Learning? | Zhang Haoyu | Market data is a deliberate teaching vehicle for three traps | Three questions + five learning objectives |

**Deliberate choice:** no results, no numbers yet. The audience is asked to hold a
guess until Act III.

## Act II — Designing a Fair Experiment

| # | Title | Presenter | Message | Visual |
|---|---|---|---|---|
| 3 | Two Markets, One Rigorous Protocol | Dong Yuankun | One protocol stress-tested on two microstructures | Table: source, observations, regime, currency + integrity checks |
| 4 | Framing the Prediction Target for Fair Learning | Zhang Haoyu | Predict the change, add it back to a known price | Formula + three-step flow + one real committed row |
| 5 | Pre-Committed Questions, Zero Cherry-Picking | Zhang Haoyu | Rules locked before results; a null result counts | Four RQs + integrity banner |
| 6 | Ten Signals from the Past | Dong Yuankun | Ten backward-looking ratios, no price level | Feature-category table |
| 7 | Chronological Splitting and Zero-Leakage Discipline | Dong Yuankun | Purge the boundary, seal the test block | Timeline with two purge gaps + three safeguards |
| 8 | Five Classical Models Across Three Paradigms | Lau Pak Hei | Mechanism diversity, not model count | Paradigm/model/mechanism table |
| 9 | The Opponent Everyone Forgets | Lau Pak Hei | A model's own MAE is meaningless without a baseline | Baseline formula, MAE, skill scale |

**Recurring artefact:** slide 4's committed row (AAPL, 2024-11-21: 228.52 →
+0.10 → 228.62 vs 229.87) keeps the abstract pipeline concrete.

## Act III — The Reveal

| # | Title | Presenter | Message | Visual |
|---|---|---|---|---|
| 10 | The Verdict: Complexity Yields Almost Zero Gain | Zhang Yancheng | Peak gain +0.52%; 3 of 10 standardised runs lose to the rule | P2 table + diverging skill bar chart centred on zero |
| 11 | Statistical Reality Check: Every Gain Sits Inside the Noise | Zhang Yancheng | 20 of 20 bootstrap intervals span zero | Forest plot, full width, dashed zero line |

**Wording discipline:** the deck says some configurations are *slightly better*;
it never claims a reliable winner, and never claims nothing ever helps.

## Act IV — Investigating Why

| # | Title | Presenter | Message | Visual |
|---|---|---|---|---|
| 12 | Does Preprocessing Save the Models? | Zhang Yancheng | Trees are invariant to scaling; kernels and penalties are not | P0 vs P2 table + ablation chart; AAPL linear got *worse* by 0.74% |
| 13 | Why Complexity Hit a Wall: Signal and Structure | Zhang Yancheng | Near-zero autocorrelation + leaf averaging | Two mechanism blocks + one-line conclusion |

**Key distinction made explicit:** preprocessing *changes behaviour* is not the
same as preprocessing *improves prediction*.

## Act V — The Bigger Lesson

| # | Title | Presenter | Message | Visual |
|---|---|---|---|---|
| 14 | From Research Finding to a Turnkey Classroom Lab | Zhang Yancheng | The finding ships as a 60-minute lab and five tasks | Package list + live multiple-choice check (answer B) |
| 15 | Engineering and Pedagogical Takeaways | Dong Yuankun | Four disciplines of building a trustworthy benchmark | Numbered insights + pull quote |
| 16 | Study Boundaries and the Bigger Lesson | Lui Shing Lam | Scope, next steps, one memorable sentence | Scope/next-steps + final takeaway + disclaimer |

## Backup — not presented

| # | Title | Use it when |
|---|---|---|
| 17 | Backup 1: Full 20-Run Transparency Matrix | "Did you cherry-pick P2?" → full grid; best BTC overall is linear at P0, +0.26% |
| 18 | Backup 2: Experimental Fairness and Manifest Audit | "Was the comparison fair?" → identical features/splits/metrics; 10 trials, 90 s per cell |
| 19 | Backup 3: Catching Data Leakage in Action | "How do you know there's no leakage?" → 0.408 reproduction, 6/6 mutation catches |
| 20 | Backup 4: What Signals Did the Models Rely On? | "Which features mattered?" → permutation importance, explicitly non-causal |
| 21 | Backup 5: Q&A Quick-Reference Cards | Five prepared one-line answers, with a named owner for each |

---

## What changed from the previous version

| Change | Reason |
|---|---|
| 15 → 16 narrative slides | Act II split into protocol / target / questions / features / leakage / models / baseline so each slide carries one idea |
| Every title states a conclusion | "The Verdict: Complexity Yields Almost Zero Gain" instead of "Results" |
| Baseline promoted to its own slide (9) before results | The audience must know the opponent before seeing the score |
| Bootstrap interval forest plot added (11) | Separates "small positive number" from "reliable advantage" visually |
| Ablation reframed as an *answer* (12) | Follows the reveal instead of interrupting the setup |
| Classroom lab and takeaways split (14, 15) | The teaching product and the engineering lessons are different claims |
| Speaker load redistributed | Pak Hei 2:45, Haoyu 3:15, Yuankun 4:30, Yancheng 5:45, Shing Lam 1:15 |
| Backup expanded to five specific rebuttal aids | Each answers one predictable examiner question |
