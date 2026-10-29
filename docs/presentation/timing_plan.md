# Presentation Timing Plan — 21 slides, 18:00 of content

Deck source: `slides/latex/main.tex` · PDF: `slides/final/INT4096_Presentation.pdf`
Limit: **20 minutes**, all **five** members speak. Target 18:00 so a slow
transition or a late start cannot push the talk over.

Every number on a slide is a macro from `slides/latex/generated/numbers.tex`,
generated from `artifacts/experiments/` — the same artifacts the report uses.

## Timing

| # | Slide | Speaker | Target | Cumulative |
|---|---|---|---:|---:|
| 1 | Title | — | 0:10 | 0:10 |
| 2 | The question a model must answer | Zhang Haoyu | 1:10 | 1:20 |
| 3 | Two markets, one protocol | Zhang Haoyu | 1:00 | 2:20 |
| 4 | Research questions and the honest goal | Zhang Haoyu | 1:00 | 3:20 |
| 5 | Immutable data, verified by hash | Dong Yuankun | 0:50 | 4:10 |
| 6 | Causal features, and the split trap | Dong Yuankun | 1:40 | 5:50 |
| 7 | Proof, not promise | Dong Yuankun | 1:10 | 7:00 |
| 8 | Chronological splits (figure) | Dong Yuankun | 0:50 | 7:50 |
| 9 | Five families, one construction path | Lau Pak Hei | 1:20 | 9:10 |
| 10 | The opponent everyone forgets | Lau Pak Hei | 1:30 | 10:40 |
| 11 | Nothing beats persistence (table) | Lui Shing Lam | 1:30 | 12:10 |
| 12 | Read this chart carefully | Lui Shing Lam | 1:00 | 13:10 |
| 13 | Why they fail | Lui Shing Lam | 1:00 | 14:10 |
| 14 | Scaling is part of the model | Zhang Yancheng | 1:20 | 15:30 |
| 15 | What the model actually uses | Zhang Yancheng | 0:50 | 16:20 |
| 16 | What a learner should take away | Zhang Yancheng | 1:00 | 17:20 |
| 17 | Limitations we will not hide | Lui Shing Lam | 0:40 | 18:00 |
| 18 | Conclusion | Zhang Yancheng | 0:50 | 18:50 |

**Wait — this table runs to 18:50.** Content slides 1–18 total **18:50**, which is
still inside the 20-minute limit but leaves only 1:10 for Q&A. Two options, to be
decided at the first rehearsal:

- **Preferred:** trim slide 3 (two markets) to 0:40 and slide 13 (why they fail)
  to 0:40 → content 18:00, leaving 2:00 for questions.
- Or move slides 7 (proof) and 15 (interpretability) to backup and present them
  only if asked.

Slides 19–21 are **backup only** (Q&A table, the audit story, repository
inventory) and are not presented.

## Per-speaker totals

| Speaker | Slides | Time |
|---|---|---:|
| Zhang Haoyu | 2–4 | 3:20 |
| Dong Yuankun | 5–8 | 4:30 |
| Lau Pak Hei | 9–10 | 2:50 |
| Lui Shing Lam | 11–13, 17 | 4:10 |
| Zhang Yancheng | 14–16, 18 | 4:00 |

Every member speaks for at least 2:50 and carries technical content — no
"hand-off" slides.

## Rehearsal rules

1. Two timed run-throughs, clock visible to the speaker.
2. Cut from slides 3 and 13 first; **never** cut slide 10 (the baseline) or 11
   (the results table) — evaluation rigour carries 20% of the unit mark.
3. If running late at slide 12, skip slide 13 and go straight to 14.
4. Handovers must be technical bridges ("…and that is why the boundary purge
   matters — Dong will show the fix"), not "over to you".

## Speaker notes (what to say, not read)

**2 — The question.** Lead with the two questions a model must answer: what did
it learn, and against what baseline. Do not start with finance.

**3 — Two markets.** AAPL trades on exchange sessions, BTC 24/7; different
volatility and quote unit. Same pipeline, so a difference is a property of the
model–data pair.

**4 — RQs.** Read only RQ1 and RQ3 aloud. State the pre-registered expectation
that a negative result is acceptable **before** showing any number.

**5 — Data.** Emphasise the hash check: the run refuses to start on a mismatch.

**6 — Features and the trap.** The key sentence: with `y_t = C_{t+1}`, the last
training label is a validation price and the last validation label would be a
sealed test price. Mention the audit found this, with the 0.408 reproduction.

**7 — Proof.** Six injected defects, six caught. Say plainly: our first suite
passed with a one-bar shift present.

**8 — Splits.** Point at the red block: never read.

**9 — Families.** Contrast what each *can represent*, not hyperparameters.

**10 — Baseline.** Show the baseline before any model number. Define skill and
say zero means "no better than copying today's price".

**11 — Results.** Read the two bold values, then the two positive ones. "20 runs,
validation only, test sealed."

**12 — Chart.** Explain the shared axis: otherwise BTC's 0.1% looks like AAPL's
0.5%.

**13 — Why they fail.** Autocorrelation ≈ 0; and a forest cannot extrapolate.

**14 — Scaling.** Predict first: trees split on order, kernels on distance. Then
reveal that tree results are bit-identical.

**15 — Interpretability.** Short-horizon returns dominate; magnitudes are tiny;
not causal.

**16 — Teaching.** The transferable question: what is the baseline, and did we
beat it? State that no learner study was run.

**17 — Limitations.** Say "we report a tie, not a ranking". This slide builds
credibility; do not rush it.

**18 — Conclusion.** Restate the result, the reproducibility, and the
non-advisory disclaimer.
