# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `slides/final/INT4096_Presentation.pdf` — 20 pages (15 narrative + 5 backup)
**Total speaking time:** 16:00 (limit 20:00)
**Timing table:** `timing_plan.md` · **Short notes:** `speaker_notes.md`

> ### How to use this document · 使用方法
> **The presentation is delivered in English. Read only the English blocks.**
> The Chinese text is a translation to help you understand what you are saying, so
> you can speak from meaning rather than from memory. Do not read the Chinese aloud.
>
> **本演示用英文进行。上台只念英文部分。**
> 中文是逐段翻译，目的是让你先理解意思、再自然地讲出来，而不是背稿。
> 中文不要念出来。
>
> If you forget a sentence, look at the **【中文要点】** line — it is the one thing
> that slide must communicate.
> 如果忘了词，就看【中文要点】那一行——那是这一页唯一必须传达的内容。

---

## 0. Before you start · 开始之前

| Item | English | 中文 |
|---|---|---|
| Language | Speak English throughout. Slides are English too. | 全程英文，幻灯片也是英文。 |
| Pace | ~105 effective words per minute once you pause, point at figures and breathe. The English below is 1,645 words total: about 13 minutes read flat out, 16 at a natural pace. | 加上停顿、指图和呼吸，实际约每分钟 105 词。全部英文约 1645 词：快速念完约 13 分钟，正常语速约 16 分钟。 |
| If you finish early | You are not "behind" — use the time to point at the figure and let the audience read it. | 提前讲完不是坏事：用多出来的时间指图，让听众自己看。 |
| Who clicks | Zhang Yancheng clicks for everyone (he also presents Act III–IV). | 由 Zhang Yancheng 统一翻页（他也负责第三、四幕）。 |
| Disclaimer | It is on slide 1 and slide 15. Do not delete it. | 免责声明在第 1 页和第 15 页，不要删。 |
| Numbers | Never invent a number. If unsure, say "it's in our run records". | 绝不编数字。不确定就说"记录在仓库里"。 |

### The whole project in 30 seconds (memorise this) · 30 秒讲清整个项目

> **English.** We took two price histories — Apple, and Bitcoin from one exchange.
> We built ten simple features from past prices, then asked five different models
> to predict how much the price would change tomorrow. We compared every model
> against one free rule: tomorrow equals today. Nothing beat that rule by more
> than about half a percent, and some models were worse.

> **中文.** 我们用了两组价格数据：苹果，和一个交易所的比特币。用过去价格算十个简单特征，
> 让五种模型预测"明天价格会变动多少"。所有模型都和一条免费规则比较：明天等于今天。
> 结果没有一个模型能比这条规则好过约 0.5%，有的还更差。

---

# ACT I — THE CHALLENGE · 第一幕：提出问题
### Lau Pak Hei · 1:20

## Slide 1 — Can Five Machine-Learning Models Beat a One-Line Rule? · 0:25

**Presenter / 讲者:** Lau Pak Hei · **Time / 时长:** 0:25 · **Page / 页码:** 1/20

**【中文要点】** 开场只做一件事：把这节课的核心问题摆出来。

**English — say this:**
> Good morning everyone. Our project started from a question that sounds almost too
> simple. If we have five machine-learning models on one side, and one rule that
> needs no training at all on the other — which one should we actually trust?
> I'm Pak Hei, and I'll set up that question before we show you the answer.

**中文对照（只帮助理解）：**
> 大家早上好。我们的项目来自一个听起来几乎太简单的问题：一边是五个机器学习模型，
> 另一边是一条完全不需要训练的规则——我们到底该相信哪一个？
> 我是 Pak Hei，我先把这个问题的背景讲清楚，然后再给答案。

**→ Transition:** "Let me make that question concrete."
**过渡：** "我把这个问题说得更具体一点。"

---

## Slide 2 — Which Would You Trust? · 0:55

**Presenter / 讲者:** Lau Pak Hei · **Time / 时长:** 0:55 · **Page / 页码:** 2/20

**【中文要点】** 复杂 ≠ 有用；只有可辩护的比较才能分辨。（此时绝不说结果）

**English — say this:**
> Imagine you want tomorrow's Apple closing price. Option one: five models, from
> regularised linear regression up to boosted trees — real machinery, real
> training. Option two: one line of arithmetic. Tomorrow's close equals today's
> close. Nothing else.
>
> Most people assume the five models win. That assumption is exactly what we
> test. And it matters beyond finance: a model can look sophisticated and still
> learn nothing useful. The only way to know is a comparison we can defend — a fair
> baseline, honest data, and a result we report even if it is boring.
>
> Keep your guess in mind. We'll come back to it.

**中文对照：**
> 假设你要预测明天苹果的收盘价。方案一：五个模型，从正则化线性回归一直到提升树，
> 有真正的训练过程。方案二：一行算术——明天收盘价等于今天收盘价，别的都不做。
>
> 大多数人会认为五个模型赢。这正是我们要检验的假设。这件事的意义不只在金融：
> 一个模型可以看起来很高级，却什么有用的东西都没学到。唯一能分辨的方法，
> 是做一个站得住脚的比较：公平的基线、诚实的数据，以及即使结果不好看也要如实报告。
>
> 请记住你刚才的猜测，最后我们会回到它。

**→ Transition:** "So let's build that comparison. Haoyu."
**过渡：** "那我们就来做这个比较。Haoyu。"

**⚠ 常被问：** "Which five models?" → "We'll show them on slide 10 — I don't want to front-load detail before you know why it matters."
**⚠ 可能被问：** "哪五个模型？" → 答："第 10 页会讲；现在先讲为什么这件事重要。"

---

# ACT II — A FAIR EXPERIMENT · 第二幕：设计公平实验
### Zhang Haoyu 3:20, then Dong Yuankun 3:40

## Slide 3 — Two Markets, One Fair Test · Zhang Haoyu · 1:05

**Presenter / 讲者:** Zhang Haoyu · **Time / 时长:** 1:05 · **Page / 页码:** 3/20

**【中文要点】** 两个刻意不同的市场，跑同一套流程；差异只能来自数据。

**English — say this:**
> We used two datasets, and the contrast is the point. Apple is a traditional
> stock: it only trades in exchange sessions, so weekends and holidays show up as
> gaps — about 251 bars a year, priced in US dollars.
>
> Bitcoin never closes. It trades every day, quoted in USDT on Binance. One honest
> caveat: that is one exchange's price in one stablecoin, not a global dollar
> index. We say that instead of pretending it is the whole market.
>
> Everything else is identical: same ten features, same target, same metrics, same
> tuning budget. So if the two markets behave differently, the difference comes
> from the data, not from our setup.

**中文对照：**
> 我们用了两组数据，对比本身才是重点。苹果是传统股票，只在交易时段交易，
> 所以周末和假期会形成空档，一年大约 251 根日线，以美元计价。
>
> 比特币从不收盘，每天交易，我们在 Binance 用 USDT 计价。这里要老实说一句：
> 那是一个交易所、一个稳定币的价格，不是全球美元指数。我们明确写出来，
> 而不是假装它代表整个市场。
>
> 其他一切都相同：同样十个特征、同样目标、同样指标、同样调参预算。
> 所以如果两个市场表现不同，差异来自数据，而不是来自我们的设置。

**→ Transition:** "But what exactly is the model being asked to predict?"
**过渡：** "但模型到底被要求预测什么？"

---

## Slide 4 — What We Are Actually Predicting · 1:20

**Presenter / 讲者:** Zhang Haoyu · **Time / 时长:** 1:20 · **Page / 页码:** 4/20

**【中文要点】** 模型预测"变动量"，不是"价格"；再把变动加回已知的价格。

**English — say this:**
> This is the part that is easy to get wrong. All ten of our features are ratios.
> A ratio cannot produce a price. So the model does not say "Apple will be 228
> dollars" — it predicts the change.
>
> Here is one real prediction from our committed results, on 21 November 2024. We
> know today's close: 228 dollars 52. The model says the price will rise by ten
> cents. So the predicted next close is 228.62. The actual next close was 229.87,
> so the error was 1 dollar 25.
>
> To be clear: this is one row, shown to make the pipeline concrete. It is not
> evidence of performance.
>
> Why do it this way? If you predicted the raw price, a lazy model could score well
> just by copying today's price. Predicting the change forces it to say something.

**中文对照：**
> 这一点最容易做错。我们十个特征全是比率，比率不可能直接产出价格。
> 所以模型不会说"苹果会是 228 美元"，它预测的是"变动量"。
>
> 这里是我们已提交结果中的一个真实预测，2024 年 11 月 21 日。
> 今天的收盘价已知：228.52。模型说价格会涨 0.10 美元，所以预测下一收盘价是 228.62。
> 实际下一收盘价是 229.87，误差 1.25 美元。
>
> 说明一下：这只是**一行**数据，用来让流程变具体，不是性能证据。
>
> 为什么这样设计？如果直接预测原始价格，一个偷懒的模型只要复制今天的价格就能拿到好分数。
> 预测变动量，就逼它必须说点什么。

**→ Transition:** "With that in place, here is what we actually asked."
**过渡：** "有了这个基础，我们来看真正要问的问题。"

**⚠ 常被问：** "Why not predict the price directly?" → the level carries the trend; copying it looks accurate.
**⚠ 可能被问：** "为什么不直接预测价格？" → 因为价格水平本身带有趋势，抄一下就看起来很准。

---

## Slide 5 — Four Questions, Fixed Before We Looked · 0:55

**Presenter / 讲者:** Zhang Haoyu · **Time / 时长:** 0:55 · **Page / 页码:** 5/20

**【中文要点】** 四个问题 + "接受负面结果"是事先写下的，所以结果可信。

**English — say this:**
> Four questions, written down before we saw any result. How do the model families
> compare against persistence? Does extra capacity buy generalisation? Do
> preprocessing choices change the answer, and does that depend on the model? And
> what should a learner take away?
>
> We also wrote something less comfortable: a negative result is an acceptable
> outcome. We were not going to keep re-slicing data until something looked
> impressive. That commitment is what makes the next result worth believing.
>
> None of it means anything, though, if the model can see the future. Yuankun.

**中文对照：**
> 四个问题，在看到任何结果之前就写下来了。各模型族和"持续性规则"相比如何？
> 更多容量真的换来泛化能力吗？预处理会不会改变结论，而且会不会因模型而异？
> 最后，学习者应该带走什么？
>
> 我们还写下一句不太舒服的话：负面结果是可以接受的。我们不会反复重新切数据，
> 直到某个结果看起来漂亮。正是这个承诺，让后面的结果值得相信。
>
> 不过，如果模型能看到未来，这一切都没有意义。Yuankun。

**→ Transition:** hand over on the word "future".
**过渡：** 在"未来"这个词上交给下一位。

---

## Slide 6 — Only the Past Is Visible · Dong Yuankun · 1:20

**Presenter / 讲者:** Dong Yuankun · **Time / 时长:** 1:20 · **Page / 页码:** 6/20

**【中文要点】** 时间序列不能随机切分；而且光排序还不够，要丢掉边界那一行。

**English — say this:**
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
> bars up to and including today.
>
> And because "we were careful" is not evidence, we also inject six known leakage
> mistakes into the code, one at a time — a one-step look-ahead, a backward fill, a
> centred window and so on — and every one must be caught before we trust the
> pipeline.

**中文对照：**
> 这里有个陷阱。通常我们随机把数据分成训练集和测试集。但在时间序列上，
> 这意味着模型可能用 2025 年的数据训练、然后去测 2021 年——等于它已经看过未来了。
>
> 更微妙的是：我们预测明天的收盘价，所以**最后一个训练样本的答案**，
> 恰好就是验证段的第一个价格。整个过程不会报错，但你的分数就悄悄变好了。
>
> 所以我们严格按日期顺序切分，并且在每个边界**丢掉一行**，
> 让答案无法从一个段跨到下一段。所有特征都只用今天及以前的交易日计算。
>
> 而"我们很小心"不能当作证据。所以我们把六种已知的泄漏错误逐个注入代码——
> 一步前视、向后填充、居中窗口等等——每一种都必须被测试抓到，我们才相信这套流程。

**→ Transition:** "Visually, this is what that looks like."
**过渡：** "从图上看就是这样。"

**⚠ 常被问：** "Isn't dropping a row wasteful?" → it is one row out of ~1,200; the alternative is a contaminated score.
**⚠ 可能被问：** "丢一行不可惜吗？" → 大约 1200 行里丢一行；不丢的代价是分数被污染。

---

## Slide 7 — Splitting Time Without Cheating · 0:55

**Presenter / 讲者:** Dong Yuankun · **Time / 时长:** 0:55 · **Page / 页码:** 7/20

**【中文要点】** 红色测试段是封存的，本次所有数字都不来自它。

**English — say this:**
> Blue is what the models learn from. Green is where we compare them. Red is
> sealed: we have not used it, and we are not showing results from it.
>
> Notice the two x-axes are different lengths, because the calendars differ —
> Bitcoin has weekends, Apple does not. That is why we never line the two up row by
> row.
>
> Everything you are about to see is a validation number. The honest ceiling on our
> claim is exactly that: validation, one period, two assets.

**中文对照：**
> 蓝色是模型学习的数据，绿色是我们比较模型的区间，红色是封存的：
> 我们没有用过它，也不会展示来自它的结果。
>
> 注意两条横轴长度不同，因为交易日历不同——比特币有周末，苹果没有。
> 这就是为什么我们从不让两个资产按行对齐。
>
> 你接下来看到的全部是**验证集**上的数字。我们结论的上限也就到这里：
> 验证集、一个时间段、两个资产。

**→ Transition:** "Last piece of setup: the inputs."
**过渡：** "最后一块准备工作：输入特征。"

---

## Slide 8 — Ten Signals from the Past · 1:25

**Presenter / 讲者:** Dong Yuankun · **Time / 时长:** 1:25 · **Page / 页码:** 8/20

**【中文要点】** 十个"比率"特征，没有价格水平；所以只能预测变动。

**English — say this:**
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

**中文对照：**
> 十个特征，全部在当天收盘时就能算出来：1、5、20 日的收益率；价格距离 5 日和 20 日
> 均线的偏离；10 日和 30 日的波动率；当天最高最低的幅度；成交量相对近期平均的变化；
> 以及星期几。
>
> 它们全是比率，这是刻意设计的。如果把原始价格直接喂给模型，它只要重复价格水平
> 就能看起来很准，那我们就无法判断它到底会不会预测。代价是：比率无法直接输出价格——
> 这正是刚才 Haoyu 讲的，我们预测变动再把它加回去。
>
> 这就是完整的准备：诚实的数据、诚实的特征、诚实的切分。

**→ Transition:** "So — what did the models do? Yancheng."
**过渡：** "那么模型表现如何？Yancheng。"

---

# ACT III — THE REVEAL · 第三幕：揭晓结果
### Zhang Yancheng · 3:35

## Slide 9 — What Must Our Models Beat? · 1:05

**Presenter / 讲者:** Zhang Yancheng · **Time / 时长:** 1:05 · **Page / 页码:** 9/20

**【中文要点】** 对手是"持续性规则"；分数是相对它的 skill，0 表示没有更好。

**English — say this:**
> Before any model, we need its opponent. Naive persistence says tomorrow's close
> equals today's close. No training, no parameters, no code to speak of.
>
> And it is a strong opponent at a one-day horizon, because daily returns are close
> to unpredictable. On Apple it gets a mean absolute error of about 2 dollars 91
> over 244 validation sessions. On Bitcoin, about 1,604 — and note those two numbers
> are not comparable, because the assets are quoted at completely different scales.
>
> So our score is skill: one minus the model's error over the rule's error. Zero
> means "no better than the rule". Negative means worse. That scale is the thing to
> watch.

**中文对照：**
> 在谈任何模型之前，先要有一个对手。"朴素持续性"规则说：明天收盘价等于今天收盘价。
> 没有训练、没有参数、几乎没有代码。
>
> 在"预测一天"这种尺度上，它是一个很强的对手，因为日收益率接近不可预测。
> 在苹果上，它 244 个验证日的平均绝对误差约 2.91 美元；比特币约 1604 美元。
> 注意这两个数不能直接比较，因为两个资产的报价尺度完全不同。
>
> 所以我们用 skill 打分：1 减去"模型误差除以规则误差"。
> 等于 0 表示和规则一样；负数表示更差。看数字时请盯住这个刻度。

**→ Transition:** "Here is what we got."
**过渡：** "这就是我们得到的结果。"

---

## Slide 10 — More Complexity, Almost No Improvement · 1:30

**Presenter / 讲者:** Zhang Yancheng · **Time / 时长:** 1:30 · **Page / 页码:** 10/20

**【中文要点】** 苹果最好 +0.52%，森林 −0.78%；20 次里 5 次低于规则；讲"范围"不讲"排名"。

**English — say this:**
> This table shows the standardised variants — the P2 columns — for both assets.
> Skill in percent, so zero is the simple rule, and negative is worse than it.
>
> Three things to notice. First, the best Apple result is support vector regression
> at plus 0.52 percent. That is half a percent — an improvement, but a very small
> one. Second, on the same asset, the random forest is at minus 0.78: it is
> genuinely worse than doing nothing. Third, look at the spread across all five
> families: everything sits between about minus 0.8 and plus 0.5.
>
> Overall, five of our twenty runs finish below the simple rule. I am not going to
> read every number — the point is the range, not the ranking.
>
> And notice what we are not saying. We are not saying nothing ever helps. Some
> configurations do come out slightly ahead. The question is whether that is real.

**中文对照：**
> 这张表是"标准化版本"（P2）在两个资产上的结果。skill 用百分比表示：
> 0 就是那条简单规则，负数是比它更差。
>
> 请注意三点。第一，苹果上最好的是支持向量回归，+0.52%——是提升，但非常小。
> 第二，同一个资产上，随机森林是 −0.78%，确实比"什么都不做"更差。
> 第三，看五个模型族的整体分布：全部落在约 −0.8% 到 +0.5% 之间。
>
> 总共 20 次运行里，有 5 次低于简单规则。我不逐行念数字——重点是**范围**，不是排名。
>
> 也要注意我们**没有**说什么：我们没有说"任何方法都没用"。有些配置确实略微更好，
> 问题是：那是真的吗？

**→ Transition:** "Which is exactly what we tested."
**过渡：** "这正是我们接下来检验的。"

**⚠ 常被问：** "So which model is best?" → give the range, not a winner.
**⚠ 可能被问：** "那哪个模型最好？" → 给范围，不给冠军。

---

## Slide 11 — The Improvements Are Inside the Noise · 1:00

**Presenter / 讲者:** Zhang Yancheng · **Time / 时长:** 1:00 · **Page / 页码:** 11/20

**【中文要点】** 差距约 1.3 个百分点；20 个配置的不确定性区间全部包含 0，所以只能说"平手"。

**English — say this:**
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

**中文对照：**
> 两件事放在一起看。所有配置的整体跨度只有约 1.3 个百分点。另外，我们给每个 skill
> 分数加了不确定区间——用的是重采样"连续日期的区块"，因为相邻交易日并不独立——
> 结果 20 次运行中，每一个区间都包含 0。
>
> 所以我们不宣布谁赢。我们报告的是：与基线打平，有些配置略好、有些略差。
>
> 这就是揭晓，而且它故意不够漂亮。有意思的问题是：为什么。

**→ Transition:** "So we asked what else could be going on."
**过渡：** "于是我们去看还有什么因素在起作用。"

---

# ACT IV — INVESTIGATING WHY · 第四幕：探究原因
### Zhang Yancheng · 2:25

## Slide 12 — Does Changing the Input Change the Answer? · 1:30

**Presenter / 讲者:** Zhang Yancheng · **Time / 时长:** 1:30 · **Page / 页码:** 12/20

**【中文要点】** 树对缩放"完全不变"（差异精确为 0）；核方法/线性会变。但"改变行为"≠"提升性能"。

**English — say this:**
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
> ensembles, predictions with and without scaling differ by exactly zero. Same
> numbers, to the last digit. Linear and kernel models move slightly, in both
> directions.
>
> Here is the distinction I care about most: preprocessing changes how a model
> behaves. It does not automatically improve it. In our runs, scaling made the
> linear baseline slightly worse on Apple.

**中文对照：**
> 如果更多复杂度没有帮助，也许"怎么准备数据"比"选哪个模型"更重要。
> 所以我们只改一件事：把输入标准化，或者保持原始尺度。模型、特征、切分都不变。
>
> 理论预测是很具体的。决策树在单个特征上用阈值切分：这个值大于还是小于某个数？
> 把一个特征整体缩放，顺序不变，等效的阈值仍然存在，所以树"应该察觉不到"。
> 核方法不同：它计算的是跨多个特征的距离，缩放会改变哪个特征占主导，所以它"应该察觉到"。
>
> 我们测到的结果不是"近似"，而是"精确"：两个树模型的预测，在缩放前后**差异精确为零**，
> 每一位数字都一样。线性模型和核方法则略有移动，方向还不一致。
>
> 我最想强调的区别是：预处理**改变模型的行为**，但并不自动**提升它的性能**。
> 在我们的运行里，标准化反而让苹果上的线性基线稍微变差。

**→ Transition:** "So why didn't the extra capacity pay off?"
**过渡：** "那为什么更多的容量没有带来收益？"

**⚠ 常被问：** "So scaling is useless?" → no: necessary for some families, irrelevant for others, never a source of information.
**⚠ 可能被问：** "那标准化没用？" → 不是：有些模型必须用，有些完全不受影响，但它本身不提供信息。

---

## Slide 13 — Why More Complexity Did Not Help · 0:55

**Presenter / 讲者:** Zhang Yancheng · **Time / 时长:** 0:55 · **Page / 页码:** 13/20

**【中文要点】** 信号本来就少（自相关≈0）；树只能输出"叶子平均"，做不出大幅变动。

**English — say this:**
> Two reasons. First, the signal is thin. The correlation between one day's return
> and the next is about plus 0.02 for Apple and minus 0.03 for Bitcoin — an R² of
> roughly 0.0005. With that little signal, more parameters mostly fit noise.
>
> Second, the tree models have a structural limit: a forest predicts an average of
> values it has seen at the leaves. On a change target that average is small and
> piecewise constant, so it struggles to produce large moves.
>
> What we did not find: no family is reliably superior, and preprocessing changes
> behaviour without creating an edge. That is the honest version — and more useful
> than an unstable win.

**中文对照：**
> 两个原因。第一，信号本来就很弱：今天的收益率和明天的收益率相关性，
> 苹果约 +0.02，比特币约 −0.03，对应的 R² 大约 0.0005。
> 信号这么弱，更多参数主要是在拟合噪声。
>
> 第二，树模型有结构性限制：森林的预测是它见过的那些叶子值的平均。
> 在"预测变动量"的目标下，这个平均值很小、而且是分段常数，所以它很难给出大幅变动。
>
> 我们**没有**发现的：没有任何模型族可靠地更好；预处理改变了行为，但没有创造优势。
> 这才是诚实的版本——比一个不稳定的"胜利"更有用。

**→ Transition:** "That is the technical story. Shing Lam will say what it means."
**过渡：** "技术部分到这里。下面由 Shing Lam 讲它的意义。"

---

# ACT V — THE BIGGER LESSON · 第五幕：更大的启示
### Lui Shing Lam · 1:40

## Slide 14 — What This Teaches Us About Machine Learning · 0:50

**Presenter / 讲者:** Lui Shing Lam · **Time / 时长:** 0:50 · **Page / 页码:** 14/20

**【中文要点】** 五条可迁移的经验；教学材料是"设计出来的资源"，没做过学习者实验。

**English — say this:**
> Five things a learner can take away. A sophisticated model is not automatically a
> better one: five families, including two ensembles, could not clearly beat one
> line. A fair baseline is not optional — without persistence, everything here
> would have looked like a success. Leakage is easy and invisible: our own first
> suite missed a one-step leak. Validation is not the future. And preprocessing
> depends on the algorithm, not on good intentions.
>
> We also ship a lesson with five worked exercises and a notebook that re-runs the
> comparison. It is a designed resource: we ran no learner study, so we claim no
> measured learning gain.

**中文对照：**
> 五点可以带走的东西。第一，复杂的模型不等于更好的模型——五个模型族，包括两个集成模型，
> 都没能明显赢过一行代码。第二，公平的基线不是可选项：没有持续性规则，
> 这里每个结果看起来都会像"成功"。第三，泄漏很容易发生而且看不见——
> 我们自己的第一版测试漏掉了一个"一步前视"，直到我们刻意去攻击它才发现。
> 第四，验证集表现不等于未来表现。第五，预处理取决于算法本身的数学性质，
> 而不是取决于我们的好意。
>
> 项目还配了一套教学材料：五个带答案的练习，加一个能重跑整个比较的 notebook。
> 这是**设计出来的资源**——我们没有做学习者实验，所以不能说它提升了谁的理解。

**→ Transition:** "So what should you remember?"
**过渡：** "那么该记住什么？"

---

## Slide 15 — The Value Is in the Comparison · 0:50

**Presenter / 讲者:** Lui Shing Lam · **Time / 时长:** 0:50 · **Page / 页码:** 15/20

**【中文要点】** 简短承认局限；给一句记得住的话；重申非投资建议。

**English — say this:**
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

**中文对照：**
> 局限，简短说：两个资产、一个时间段、一天的预测跨度；比特币是一个交易所的 USDT 价格；
> "预测一天"恰恰是简单规则最难被打败的地方；而且我们的测试段仍然封存，
> 所以这些都是验证集结果。
>
> 如果只记住一句话，就记这句：机器学习的价值，不在于模型有多复杂，
> 而在于它是否学到了超越一个有意义的基线的、真正有用的东西。
>
> 最后是必要的免责声明：这是历史数据的教育性分析，不构成投资建议；
> 预测误差低并不意味着能盈利。谢谢大家，我们很乐意回答问题。

---

# Q&A — bilingual cheat sheet · 问答中英对照

| Question | English answer | 中文意思 |
|---|---|---|
| Isn't this just a random walk? | Largely yes at one day — that *is* the finding, and it's why the rule is strong. | 一天尺度上基本是；这正是发现本身，也是规则强的原因。 |
| Did you leak future data? | No: chronological split, boundary purge, ratio features, and a leakage suite proven able to fail. | 没有：按时间切分、边界剔除、比率特征，而且泄漏测试被证明"能失败"。 |
| Why no deep learning? | The handout discourages it; the instructor's reported guidance is recorded as reported, not as a rule change; it isn't needed for this question. | 讲义不鼓励；老师口头的说法我们按"转述"记录；这个问题也不需要它。 |
| Is 0.5% meaningful? | Not by our standard: the interval includes zero for all 20 runs. | 按我们的标准不算：20 次运行的区间全部包含 0。 |
| Can we trade on this? | No. Error metrics ignore costs and risk; we make no profit claim. | 不能。误差指标不考虑成本和风险，我们不声称能盈利。 |
| Why these two assets? | One conventional equity with session gaps, one continuously traded market with different volatility. | 一个是传统股票（有交易时段空档），一个是全天交易、波动结构不同的市场。 |
| Which model is best? | We report a tie, not a winner — differences are inside the noise. | 我们报告平手，不宣布冠军——差异落在噪声范围内。 |

---


# Backup slides — only if asked · 备用页（被问到才用）

| # | Slide | What to say (English) | 中文 |
|---|---|---|---|
| 16 | Every Configuration | "This is every cell, both variants. The P2 table wasn't cherry-picked; the best BTC configuration overall is actually the linear model without scaling, at +0.26%." | "这是全部单元格、两种预处理。P2 那张表不是挑选出来的；比特币整体最好的是未标准化的线性模型，+0.26%。" |
| 17 | Was the Comparison Fair? | "Identical features, split, dates and budget: 10 random trials, at most 90 seconds per cell, the same for every model. The protocol allows up to 24 trials and 300 seconds; we report the budget we actually used." | "特征、切分、日期、预算都相同：每格最多 10 次随机试验、90 秒，所有模型一样。协议允许 24 次/300 秒；我们报告的是实际使用的预算。" |
| 18 | How We Caught Our Own Leak | "An audit found the last training label was a validation price. Perturbing one test price moved our metric by 0.408 — far more than any model's advantage. We purged one row at each boundary, and now inject six known leaks; all six must be caught." | "审计发现最后一个训练标签其实是验证集价格。扰动一个测试价格，指标就移动了 0.408——远大于任何模型的优势。我们于是在每个边界剔除一行，并注入六种已知泄漏，全部必须被抓到。" |
| 19 | What the Model Relies On | "Permutation importance for ridge: short-horizon returns and volatility matter most, and the magnitudes are tiny — consistent with the skill table. It describes the fitted model, not the market." | "岭回归的置换重要性：短期收益率和波动率最重要，量级很小——与 skill 表一致。它描述的是拟合出来的模型，不是市场本身。" |
| 20 | Questions and Who Answers | "We'll route questions to whoever owns that part." | "我们把问题交给最熟悉那部分的人。" |

# If you are running over · 超时怎么办

Check the clock at slide 10: it should read about **11:00**.

| Situation | What to cut | 中文 |
|---|---|---|
| 11:30 or later | Compress slide 13 to one sentence: "daily returns barely predict themselves, so extra capacity fits noise." Saves ~0:40. | 第 13 页压成一句："日收益率几乎无法预测自己，多出的参数主要在拟合噪声。"省约 40 秒。 |
| 12:00 or later | Also cut slide 3 to the two-market contrast only. Saves ~0:30. | 再把第 3 页缩成"两个市场的对比"。省约 30 秒。 |
| **Never cut** | Slide 9 (baseline) or slide 10 (results). | **绝不能砍**第 9 页（基线）和第 10 页（结果）。 |

# If you are running short · 时间不够怎么办

Add the mechanism behind the tree-invariance result on slide 12 (thresholds vs distances), or give the BTC-overall caveat: the best BTC configuration overall is the linear model without scaling at +0.26%.

中文：可以在第 12 页补充"阈值 vs 距离"的机制；或补充"比特币整体最好的配置是未标准化的线性模型，+0.26%"。

---

# Rehearsal checklist · 排练清单

- [ ] Each presenter has read their **English** block aloud twice. 每位讲者把英文段落大声读两遍。
- [ ] Each presenter can say their **【中文要点】** without looking. 不看稿也能说出中文要点。
- [ ] The four handover sentences are rehearsed — that is where time leaks. 四句过渡要练，最容易在这里丢时间。
- [ ] Two full timed run-throughs. 全流程计时彩排两次。
- [ ] Slide 1 and 15 disclaimers are visible and not skipped. 第 1 页和第 15 页的免责声明不能跳过。
- [ ] Nobody reads a number from the slides that they cannot explain. 讲不出含义的数字，就不要念。

> **Reminder · 提醒**
> The presentation is in English; Chinese here is a comprehension aid only.
> 演示用英文；中文仅供理解，不用于上台朗读。
