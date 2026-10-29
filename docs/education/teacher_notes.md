# Teacher Notes

Companion to `docs/education/lesson_plan.md` and
`docs/education/formative_tasks.md`.

---

## 1. What this lesson is really teaching

Not "how to predict stock prices". The real lesson is:

> **A model can be mathematically sophisticated and still be useless, and careful
> evaluation is what tells you which one you have.**

That is a transferable idea. It applies to predicting student grades, rainfall,
or hospital demand just as much as to prices. Say this explicitly — learners
often assume the finance setting is the point.

---

## 2. The three things learners most often get wrong

### 2.1 "The model with the lowest error is the best model"

They will look at MAE and rank. Redirect them to *skill relative to a baseline*.
A model is only interesting if it beats the free rule. The strongest moment in
this lesson is showing that `random_forest` on AAPL is **worse than copying
today's price**.

### 2.2 "More data or a bigger model will fix it"

The limiting factor here is *information*, not capacity. Demonstrate with the
near-zero return autocorrelation in notebook §8 Example C: if yesterday's return
barely predicts today's, extra parameters fit noise.

Ask: "If I gave you a bigger brain but the same blurry photograph, would you see
more?" That analogy usually lands.

### 2.3 "Scaling is a technical detail"

Two model families in this project are **exactly** invariant to it (identical to
every printed digit) and two are not. That is not a detail; it is a property of
what the model *does*. Use Task 4.

---

## 3. Timing guidance

| If you have... | Drop this | Never drop this |
|---|---|---|
| 45 minutes | Worked Task 4 in class (set as homework) | The baseline reveal (§5) and the skill table |
| 30 minutes | The leakage snippet (Task 2) | Baseline + skill table + the non-advisory discussion |
| 20 minutes | The ablation deep dive | Baseline reveal, then "why complexity failed", then the disclaimer |

The single non-negotiable is that learners see the baseline **before** the models.
If they see model results first, they will anchor on them.

---

## 4. How to answer "so can I use this to get rich?"

Do not dodge the question, and do not moralise. Use it:

> "Two reasons not yet. First, the best model beat a trivial rule by about half a
> percent on one period, which is inside the noise — I would not bet on it
> repeating. Second, even a genuinely better forecast is not automatically profit:
> there are fees, spreads, and the risk of large moves the error metric never
> shows. What you *can* take away is the method: always compare against the dumb
> baseline, and always test on data the model has never seen."

This reframes the question as an evaluation lesson, which is the point of the
module.

---

## 5. Discussion prompts that work

- "Before I show you the results: will a trained model beat 'tomorrow = today'?
  Write your prediction down." *(Commitment makes the reveal land.)*
- "This model is worse than doing nothing. Is it a failed experiment?" *(The
  answer is no: a well-run comparison that produces a negative result is a
  success. Distinguish process quality from outcome attractiveness.)*
- "Which of these two claims is stronger: 'R² = 0.96' or 'skill = 0.5%'?" *(The
  second, because R² on a trending series is inflated.)*
- "What would you need to see before you believed the 0.5% was real?" *(More
  periods, more assets, uncertainty intervals, cost modelling.)*

---

## 6. Technical notes for the teacher

**Running the notebook.** `Runtime → Run all`. The first cell installs missing
packages; everything after is deterministic. Total runtime is a few minutes.

**If Colab has no data.** The notebook looks for `data/raw/*.json`. Either clone
the repository (set `INT4096_REPO`), or upload the `data/raw/` folder next to the
notebook. The notebook fails loudly rather than inventing data — that is
deliberate and worth pointing out to learners.

**Regenerating every number.** `bash scripts/reproduce.sh` rebuilds the runs,
figures and registry. `docs/research/run_registry.md` lists every run with its
status.

**If a learner asks about the test set.** Explain that the final 20% of dates is
*sealed*: nobody has looked at it yet, so that it remains a genuine holdout. This
is the same reason exam papers are not distributed with the course notes.

**If a learner asks "did AI write this?"** Answer honestly: yes, with named human
review, a protocol frozen before experiments, tests that can fail, and an
independent leakage audit that found real defects which were then fixed. That is
a better answer than pretending otherwise, and it models good practice.

---

## 7. Assessment rubric for the five tasks

| Task | Objective | Weight | Full marks require |
|---|---|---:|---|
| 1 | O1 | 15% | Baseline comparison used to justify the verdict |
| 2 | O2 | 25% | Both leaks identified **and** a correct rewrite |
| 3 | O3 | 20% | Caveat on "best" + plain-language reading of negative skill |
| 4 | O4 | 25% | Order/threshold argument for trees + distance argument for kernels + objection to "improves" |
| 5 | O5 | 15% | Two money-level reasons + two scope limits + an honest slide sentence |

Suggested mastery threshold: 70% overall, with **Task 2 and Task 4 both at full
marks**, because leakage recognition and scale reasoning are the two ideas most
likely to transfer.

---

## 8. What this lesson does **not** establish

No learners were observed, tested or surveyed. Nothing here is evidence that the
lesson improves understanding. It is a **designed resource** with objectives,
activities and assessments that a teacher could evaluate. If the group later runs
a consented pilot, results may be reported only with that method and evidence
stated explicitly.

**Disclaimer to display with any learner-facing material:**

> Historical market data, education only. Not investment advice. Forecast error
> does not imply profit, and past performance does not predict future results.
