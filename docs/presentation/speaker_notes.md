# Speaker Notes and Rehearsal Script

**Deck:** `slides/final/INT4096_Presentation.pdf` (20 pages: 15 narrative + 5 backup)
**Total speech:** 16:00 · **Limit:** 20:00 · **Timing table:** `timing_plan.md`

These notes are written to be **spoken**, not read aloud verbatim. The scripts are
sized for a relaxed pace of about 125 words per minute. If you speak faster, slow
down rather than adding content.

> **Presentation roles only.** Nothing here describes who built the software or
> ran the experiments; that is in `docs/management/responsibilities.md`.

---

## 0. How the whole project works — for every presenter

Read this once, even if you did not write the code. It is the entire pipeline in
plain language.

1. **We downloaded two price histories.** Apple (an exchange-traded stock) and
   Bitcoin (trades 24/7; our series is Binance BTCUSDT, one venue, quoted in
   USDT). Each is stored as a file that never changes, with a fingerprint so we
   can prove we used the same data every time.
2. **We built ten features per day.** All ten are ratios: recent returns, distance
   from moving averages, recent volatility, today's range, a volume measure, and
   the weekday. None of them is a price, so a model cannot cheat by copying the
   price level.
3. **We defined the prediction.** At today's close, predict *how much* the price
   will change by tomorrow's close. Then add that change back to today's price to
   get a predicted price. Splitting it this way stops the model from being judged
   on the trend that is already in the price.
4. **We split by time, not randomly.** The first 60% of dates train, the next 20%
   validate, the last 20% is sealed. One row is dropped at each boundary, because
   otherwise the last training answer would be the first validation price.
5. **We tuned each model inside the training block only.** Ten random
   hyperparameter trials per model, capped at 90 seconds. Validation was never
   used for tuning, so it stays a fair selection set.
6. **We compared against naive persistence** — "tomorrow equals today". Skill is
   `1 − MAE_model / MAE_naive`, so 0 means no better than the simple rule.
7. **We ran 20 cells:** 5 model families × 2 assets × 2 preprocessing variants.
   Every number in the deck is validation only; the test block has not been read.
8. **We then asked why.** We compared unscaled and scaled inputs (P0 vs P2) and
   checked whether the models depend on feature scale at all.

If someone asks a question you cannot answer, say: *"I don't know — but our run
records are public in the repository, so we can look it up."* That is a good
answer. Inventing one is not.

---

## Act I — The Challenge · Lau Pak Hei · 1:20

### Slide 1 — "Can Five Machine-Learning Models Beat a One-Line Rule?" · 0:25

**Key message:** We asked a simple question and let the data answer it.

**Script:**
> Good morning. Our project started with a question that sounds almost too simple:
> if we take five different machine-learning models, and compare them against one
> rule that requires no training at all, which one should we trust? I'm Pak Hei,
> and I'll set up that question before we show you the answer.

**Transition:** "Let me make the question concrete."

### Slide 2 — "Which Would You Trust?" · 0:55

**Key message:** Complexity is not the same thing as usefulness, and only a
defensible comparison can tell them apart.

**Script:**
> Imagine you want tomorrow's Apple closing price. Option one: five models, from
> regularised linear regression up to boosted trees — real machinery, real
> training. Option two: one line of arithmetic. Tomorrow's close equals today's
> close. Nothing else.
>
> Most people assume the five models win. That assumption is exactly what this
> project tests. And the reason it matters is bigger than finance: a model can look
> sophisticated and still learn nothing useful. The only way to know is to build a
> comparison we can defend — a fair baseline, honest data, and a result we are
> willing to report even if it is boring. Keep your guess in mind. We'll come back
> to it.

**Transition:** "So let's build that comparison. Haoyu."

**Anticipated confusion:** someone may ask which five models. Hold that for
slide 10; naming them now front-loads detail before the audience knows why it
matters.

---

## Act II — Designing a Fair Experiment · 7:00

### Slide 3 — "Two Markets, One Fair Test" · Zhang Haoyu · 1:05

**Key message:** Two deliberately different markets, one identical pipeline.

**Script:**
> We used two datasets, and the contrast is the point. Apple is a traditional
> stock: it only trades during exchange sessions, so weekends and holidays show up
> as gaps, about 251 bars a year, priced in US dollars.
>
> Bitcoin never closes. It trades every day, all year, quoted in USDT on Binance.
> One honest caveat: that is one exchange's price in one stablecoin, not a global
> dollar index. We say that explicitly rather than pretending it is the whole
> market.
>
> Everything else is identical: same ten features, same prediction target, same
> metrics, same tuning budget. So if the two markets behave differently, the
> difference comes from the data, not from our setup.

**Transition:** "But what exactly is the model being asked to predict?"

### Slide 4 — "What We Are Actually Predicting" · 1:20

**Key message:** We predict the *change*, then add it to the price we already know —
so the model has to contribute information, not just repeat the price level.

**Script:**
> This is the part that is easy to get wrong. All ten of our features are ratios.
> A ratio cannot produce a price. So the model does not predict "Apple will be
> 228 dollars". It predicts the change.
>
> Here is one real prediction from our committed results, on the 21st of November
> 2024. We know today's close: 228 dollars 52 cents. The model says the price will
> rise by ten cents. So the predicted next close is 228.62. The actual next close
> turned out to be 229.87, so the error was 1 dollar 25.
>
> I want to be clear about what this slide is and is not: it is one row, shown to
> make the pipeline concrete. It is not evidence of performance.
>
> Why do it this way? Because if you predicted the raw price, a lazy model could
> score well just by copying today's price. Predicting the change forces it to say
> something.

**Transition:** "With that in place, here is what we actually asked."

**Anticipated confusion:** "Why not predict the price directly?" — Because the
price level carries the trend, and copying it looks accurate. Answer that now if
it comes up; it is the single most common question here.

### Slide 5 — "Four Questions, Fixed Before We Looked" · 0:55

**Key message:** The questions and the acceptance of a negative result were fixed
in advance, which is what stops us from rationalising afterwards.

**Script:**
> Four questions, written down before we saw any result. How do the model families
> compare against persistence? Does extra capacity actually buy generalisation? Do
> preprocessing choices change the answer, and does that depend on the model? And
> what should a learner take away?
>
> We also wrote down something less comfortable: a negative result is an
> acceptable outcome. We were not going to keep re-slicing the data until something
> looked impressive. That commitment is what makes the next result worth believing.
>
> None of it means anything, though, if the model can accidentally see the future.
> Yuankun.

**Transition:** hand to Yuankun on the word "future".

### Slide 6 — "Only the Past Is Visible" · Dong Yuankun · 1:20

**Key message:** With time-ordered data, an ordinary random split is cheating, and
the fix needs more than just sorting the dates.

**Script:**
> Here is the trap. Normally we split data randomly into training and test. On a
> time series, that means the model can train on 2025 and be tested on 2021. It has
> effectively seen the future.
>
> It gets subtler. We predict tomorrow's close. So the last training example's
> answer — the thing we teach it — is literally the first price in the validation
> block. Nothing dramatic happens, no error message, and your score quietly
> improves.
>
> So we split strictly by date, in order. And we drop one row at each boundary, so
> no answer can cross from one block into the next. Every feature is computed from
> bars up to and including today. And because "we were careful" is not evidence, we
> also inject six known leakage mistakes into the code one at a time — a one-step
> look-ahead, a backward fill, a centred window and so on — and every single one
> must be caught before we trust the pipeline.

**Transition:** "Visually, this is what that looks like."

### Slide 7 — "Splitting Time Without Cheating" · 0:55

**Key message:** The test block is visibly sealed and is not part of any number in
this talk.

**Script:**
> Blue is what the models learn from. Green is where we compare them. Red is
> sealed: we have not used it, and we are not showing results from it.
>
> Note the two x-axes are different lengths, because the calendars differ — Bitcoin
> has weekends, Apple does not. That is why we never line the two up row by row.
>
> Everything you are about to see is a validation number. The honest ceiling on our
> claim is exactly that: validation, one period, two assets.

**Transition:** "Last piece of setup: the inputs."

### Slide 8 — "Ten Signals from the Past" · 1:25

**Key message:** Ten trailing ratios, no price level — which is why the model
predicts a change.

**Script:**
> Ten features, all computable when today's market closes. Returns over one, five
> and twenty sessions. How far the price sits from its five- and twenty-session
> average. Volatility over ten and thirty sessions. Today's high-to-low range.
> Volume compared with its recent average. And the weekday.
>
> They are all ratios on purpose. If we fed the model the raw price, it could look
> accurate by repeating the level, and we would learn nothing about whether it
> forecasts. The cost is that a ratio cannot output a price — which is exactly why
> we predict the change and add it back, as Haoyu showed.
>
> That is the whole setup: honest data, honest features, honest split.

**Transition:** "So — what did the models do? Yancheng."

**Anticipated confusion:** "Isn't ten features very few?" — Yes, deliberately. The
question is whether a model can beat a simple rule, not how much data we can throw
at it. More features would make the comparison harder to interpret.

---

## Act III — The Reveal · Zhang Yancheng · 3:35

### Slide 9 — "What Must Our Models Beat?" · 1:05

**Key message:** The opponent is naive persistence, and the score is skill relative
to it.

**Script:**
> Before any model, we need its opponent. Naive persistence says tomorrow's close
> equals today's close. No training, no parameters, no code to speak of.
>
> And it is a genuinely strong opponent at a one-day horizon, because daily returns
> are close to unpredictable. On Apple it achieves a mean absolute error of about
> 2 dollars 91 over 244 validation sessions. On Bitcoin, about 1,604 — and note
> those two numbers are not comparable, because the assets are quoted at completely
> different scales.
>
> So our score is skill: one minus the model's error divided by the simple rule's
> error. Zero means "no better than the rule". Negative means worse. That scale is
> the thing to watch.

**Transition:** "Here is what we got."

### Slide 10 — "More Complexity, Almost No Improvement" · 1:30

**Key message:** The best model improves on the rule by about half a percent on
Apple, and several configurations are worse.

**Script:**
> This table shows the standardised variants — the P2 column set — for both assets.
> Skill in percent, so zero is the simple rule, and negative is worse than it.
>
> Three things I want you to notice. First, the best Apple result is support vector
> regression at plus 0.52 percent. That is half a percent — an improvement, but a
> very small one. Second, on the same asset, the random forest is at minus 0.78: it
> is genuinely worse than doing nothing. Third, look at the spread across all five
> families: everything sits between about minus 0.8 and plus 0.5.
>
> Overall, five of our twenty runs finish below the simple rule. I am not going to
> read every number — the point is the range, not the ranking.
>
> And notice what we are not saying. We are not saying nothing ever helps. Some
> configurations do come out slightly ahead. The question is whether that is real.

**Transition:** "Which is exactly what we tested."

**Anticipated confusion:** "So which model is best?" — Answer with the range, not
a winner: differences are within noise. If pressed on BTC: the best BTC
configuration overall is actually the linear model without scaling at +0.26,
slightly above the best P2 value.

### Slide 11 — "The Improvements Are Inside the Noise" · 1:00

**Key message:** The differences are small and not distinguishable from zero.

**Script:**
> Two things together. The whole spread across every configuration is about one and
> a third percentage points. And when we put an uncertainty interval around each
> skill score — resampling blocks of consecutive dates, because neighbouring days
> are not independent — that interval includes zero for all twenty runs.
>
> So we do not claim a winner. We report a tie against the baseline, with some
> configurations slightly ahead and some behind.
>
> That is the reveal, and it is deliberately unglamorous. The interesting question
> is why.

**Transition:** "So we asked what else could be going on."

---

## Act IV — Investigating Why · Zhang Yancheng · 2:25

### Slide 12 — "Does Changing the Input Change the Answer?" · 1:30

**Key message:** Preprocessing changes some models and not others — exactly as
theory predicts — but changing behaviour is not the same as improving forecasts.

**Script:**
> If more complexity did not help, maybe how we prepare the data matters more than
> which model we pick. So we changed one thing: standardise the inputs, or leave
> them raw. Same model, same features, same split.
>
> The prediction is specific. A decision tree splits on a threshold inside one
> feature: is this value above or below some number? Rescale a feature and the
> order is unchanged, so an equivalent threshold exists. The tree should not
> notice. A kernel method is different: it measures distances that combine several
> features, so rescaling changes which feature dominates. It should notice.
>
> And that is what we measured — not approximately, exactly. For both tree
> ensembles, the predictions with and without scaling differ by exactly zero. Same
> numbers, to the last digit. Linear and kernel models move slightly, in both
> directions.
>
> Here is the distinction I care about most: preprocessing changes how a model
> behaves. It does not automatically improve it. In our runs, scaling made the
> linear baseline slightly worse on Apple.

**Transition:** "So why didn't the extra capacity pay off?"

**Anticipated confusion:** "So scaling is useless?" — No: it is necessary for some
families to behave sensibly at all, and irrelevant for others. It is not a source of
predictive information.

### Slide 13 — "Why More Complexity Did Not Help" · 0:55

**Key message:** There is very little short-horizon signal, and extra capacity fits
noise; the tree models also have a structural limit.

**Script:**
> Two reasons. First, the signal is thin. The correlation between one day's return
> and the next is about plus 0.02 for Apple and minus 0.03 for Bitcoin — an R² of
> roughly 0.0005. With that little signal, more parameters mostly fit noise.
>
> Second, the tree models have a structural limit: a forest predicts an average of
> values it has already seen at the leaves. On a change target that average is
> small and piecewise constant, so it struggles to produce large moves.
>
> What we did not find: no family is reliably superior, and preprocessing changes
> behaviour without creating an edge. That is the honest version — and more useful
> than an unstable win.

**Transition:** "That is the technical story. Shing Lam will say what it means."

---

## Act V — The Bigger Lesson · Lui Shing Lam · 1:40

### Slide 14 — "What This Teaches Us About Machine Learning" · 0:50

**Key message:** Five transferable lessons, all visible in this one experiment.

**Script:**
> Five things a learner can take away. A sophisticated model is not automatically a
> better one — five families, including two ensembles, could not clearly beat a
> single line. A fair baseline is not optional: without persistence, every result
> here would have looked like a success. Leakage is easy and invisible — our own
> first test suite missed a one-step leak until we tried to break it deliberately.
> Validation is not the future. And preprocessing depends on the algorithm, not on
> good intentions.
>
> The project also ships a lesson with five worked exercises and a notebook that
> re-runs the comparison. That is a designed resource — we ran no learner study, so
> we are not claiming it improved anyone's understanding.

**Transition:** "So what should you remember?"

### Slide 15 — "The Value Is in the Comparison" · 0:50

**Key message:** Limitations stated plainly, then one memorable idea.

**Script:**
> Limitations, briefly: two assets, one period, a one-day horizon; Bitcoin is one
> exchange's price in USDT; one-day forecasting is exactly where the simple rule is
> hardest to beat; and our test block is still sealed, so these are validation
> results.
>
> If you remember one sentence, make it this: the value of machine learning is not
> measured by how complicated a model is, but by whether it learns something useful
> beyond a meaningful baseline.
>
> And a necessary disclaimer: this is historical, educational analysis. It is not
> investment advice, and a low forecast error does not imply profit. Thank you —
> we're happy to take questions.

---

## Backup slides — use only if asked

| # | Slide | Presenter | Use it when |
|---|---|---|---|
| 16 | Every configuration (skill for all 20 cells) | Zhang Yancheng | "Did you cherry-pick P2?" — No: show the full grid; best BTC overall is linear at P0, +0.26. |
| 17 | Was the comparison fair? | Zhang Yancheng | "Did every model get the same budget?" — Yes: 10 trials / 90 s, identical for all; the protocol allows 24 / 300 s and we report what we used. |
| 18 | How we caught our own leak | Dong Yuankun | "How do we know there is no leakage?" — The audit story, including the 0.408 reproduction and 6/6 mutation catches. |
| 19 | What the fitted model relies on | Zhang Yancheng | "Which features mattered?" — Permutation importance; short-horizon returns and volatility dominate; magnitudes tiny. |
| 20 | Questions and who answers them | Lau Pak Hei | Route questions to the right person without guessing. |

## Q&A answers in one line each

- **"Isn't this just a random walk?"** Largely yes at a one-day horizon — that is
  the finding, and it is why the baseline is strong.
- **"Did you leak future data?"** No: chronological split, boundary purge, causal
  features, and a mutation-tested leakage suite. See backup 18.
- **"Why no LSTM or deep learning?"** The handout discourages it, the instructor's
  reported guidance is recorded as reported rather than as a rule change, and it is
  not needed to answer our question. It remains available but gated.
- **"Is 0.5% meaningful?"** Not by our own standard: the bootstrap interval
  includes zero for every configuration.
- **"Can we trade on this?"** No. Error metrics ignore costs and risk, and we make
  no profitability claim.
- **"Why these two assets?"** One conventional equity with session gaps, one
  continuously traded market with a different volatility regime.
