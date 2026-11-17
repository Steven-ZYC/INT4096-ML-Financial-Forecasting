# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `slides/final/INT4096_Presentation.pdf` — 21 pages (16 narrative + 5 backup)
**Speech:** 17:30 of a 20:00 slot · **Clock:** `timing_plan.md`
**Key messages:** `speaker_notes.md`

> ### How to use this document · 使用方法
> **The presentation is delivered in English. Read only the English blocks.**
> The Chinese below is a translation to help you understand what you are saying,
> so you can speak from meaning instead of from memory. **Do not read the Chinese aloud.**
>
> **本演示用英文进行。上台只念英文部分。**
> 中文是逐段翻译，目的是让你先理解意思、再自然讲出来，而不是背稿。中文不要念出来。
>
> If you lose your place, look at **【中文要点】** — that is the one thing the slide
> must communicate.
> 如果忘了词，就看【中文要点】——那是这一页唯一必须传达的内容。

---

## 0. Before you start · 开始之前

| Item | English | 中文 |
|---|---|---|
| Language | English throughout; slides are English too. | 全程英文，幻灯片也是英文。 |
| Pace | ~105 effective words per minute. The English totals ~1,840 words: about 17–18 minutes at a natural pace. | 实际约每分钟 105 词；英文总量约 1840 词，正常语速约 17–18 分钟。 |
| Who clicks | Zhang Yancheng (he also presents Act III–IV). | 由 Zhang Yancheng 统一翻页（他也负责第三、四幕）。 |
| Backup slides | 17–21 stay in the file; open Backup 1 and 3 if asked. | 第 17–21 页是备用页；被问到"是否挑选结果""有没有泄漏"时打开 Backup 1 和 3。 |
| Disclaimer | On slide 1 and slide 16. Never remove. | 免责声明在第 1 页和第 16 页，不能删。 |
| Numbers | Never invent one. If unsure: "it's in our run records". | 绝不编数字；不确定就说"记录在仓库里"。 |

### The whole project in 30 seconds · 30 秒讲清整个项目

> **English.** We took two price histories — Apple, and Bitcoin from one exchange.
> From ten backward-looking ratios we asked five classical models to predict the
> next session's price *change*, then added it back to today's price. We compared
> every model against one free rule: tomorrow equals today. Nothing beat that rule
> by more than about half a percent, and every confidence interval included zero.

> **中文.** 我们用了两组价格数据：苹果，和一个交易所的比特币。用十个"只看过去"的比率特征，
> 让五种经典模型预测下一个交易日的价格**变化量**，再加回今天的价格。
> 所有模型都和一条免费规则比较：明天等于今天。没有一个模型比这条规则好过约 0.5%，
> 而且所有置信区间都包含 0。

---

# ACT I — THE CHALLENGE · 第一幕：提出问题

## Slide 1 — Can Five Machine-Learning Models Beat a One-Line Rule? · 0:40
**Presenter / 讲者:** Lau Pak Hei · **Page / 页码:** 1/21

**【中文要点】** 开场只做一件事：把"五个模型 vs 一行规则"这个悬念摆出来，不剧透结果。

**English — say this:**
> Good morning. Here is the question our whole project comes from. On the left, five
> classical machine-learning models — linear, ridge, a kernel method, and two tree
> ensembles. On the right, one line: tomorrow's price equals today's price. No
> training, no parameters.
>
> Which one should you actually trust? Most people assume the five models. Over the
> next seventeen minutes we test that assumption properly, and I think the answer
> will surprise you.

**中文对照：**
> 大家早上好。这就是我们整个项目要回答的问题。左边是五个经典机器学习模型——线性、岭回归、
> 一个核方法、两个树集成；右边只有一行：明天的价格等于今天的价格，不训练、没有参数。
>
> 你该相信哪一个？大多数人会选那五个模型。接下来十七分钟，我们会用严谨的方法检验这个假设，
> 而答案可能会让你意外。

**→ Transition:** "That is the question. Haoyu will explain why this data is the
right place to test it." · **过渡：** "问题摆在这里。为什么用这类数据来检验，由 Haoyu 说明。"

---

## Slide 2 — Why Use Market Data to Teach Machine Learning? · 1:15
**Presenter / 讲者:** Zhang Haoyu · **Page / 页码:** 2/21

**【中文要点】** 选金融数据不是为了炒股，而是因为它是暴露"过拟合、泄漏、迷信复杂模型"最锋利的教学载体。

**English — say this:**
> Let me be explicit about why we chose this data. Not because we want to predict
> markets, but because market data punishes three beginner mistakes quickly.
>
> First, a model can fit history beautifully and still fail tomorrow. Second, it is
> alarmingly easy to let a model see the future by accident. Third, we all assume a
> complicated model must beat a simple rule.
>
> So the data is a stress test for three questions: can it generalise, did it
> cheat, does it beat the baseline? Our audience is advanced secondary students and
> non-specialist undergraduates. They should leave able to ask those three
> questions of any model.

**中文对照：**
> 我先说明为什么用这类数据。不是因为我们想预测市场，而是因为市场数据会迅速惩罚三个
> 初学者最常犯的错误。
>
> 第一，模型可以把历史拟合得非常漂亮，却在明天失效。第二，一不小心就会让模型"看到未来"。
> 第三，我们很容易以为复杂的模型一定比简单规则更好。
>
> 所以这组数据其实是对三个问题的压力测试：它能否泛化？它有没有作弊？它有没有打败基线？
> 我们的受众是高中高年级、预科，以及非机器学习专业的本科生。到最后，他们应该能对任何模型
> 回答这三个问题，并能解释为什么标准化对不同模型族影响不同，以及为什么预测误差不等于盈利。

**→ Transition:** "So how do we test that? Dong sets up the experiment."
**过渡：** "那怎么做这个检验？由 Dong 介绍实验设置。"

---

# ACT II — DESIGNING A FAIR EXPERIMENT · 第二幕：设计公平实验

## Slide 3 — Two Markets, One Rigorous Protocol · 1:00
**Presenter / 讲者:** Dong Yuankun · **Page / 页码:** 3/21

**【中文要点】** 同一套协议跑两个截然不同的市场结构；数据完整性用自动检查把关。

**English — say this:**
> One protocol, two very different markets. Apple: 1,255 daily bars, exchange
> sessions only, quoted in dollars. Bitcoin: 1,828 bars, trading around the clock,
> and our series is Binance BTCUSDT — one venue in USDT, not a global index.
>
> Before any model runs, the data passes automated integrity checks: duplicate
> timestamps, missing fields, non-positive prices, negative volume. Every file is
> fingerprinted, so the same bytes underlie every number you will see.
>
> Two markets is a robustness test: a conclusion that holds in only one
> microstructure is not a conclusion about machine learning.

**中文对照：**
> 一套协议，两个非常不同的市场。苹果是传统股票：1255 根日线，只在交易时段，美元计价。
> 比特币有 1828 根，全天候交易，我们用的是 Binance BTCUSDT——一个交易所、USDT 计价，
> 不是全球指数。我们明确说明这一点，而不是含糊过去。
>
> 在任何模型运行之前，数据要通过自动完整性检查：重复时间戳、核心字段缺失、非正价格、
> 负成交量。每个文件还有哈希指纹，所以我们可以证明所有数字用的都是同一份数据。
>
> 用两个市场不是为了多样好看，而是一个稳健性检验：如果结论只在一种市场结构下成立，
> 那它就不是关于机器学习的结论。

**→ Transition:** "With clean data, what exactly is the model predicting?"
**过渡：** "数据干净了，那模型到底预测什么？"

---

## Slide 4 — Framing the Prediction Target for Fair Learning · 1:00
**Presenter / 讲者:** Zhang Haoyu · **Page / 页码:** 4/21

**【中文要点】** 特征全是比率，所以让模型预测"变动量"，再加回已知价格——避免靠抄价格水平取巧。

**English — say this:**
> This decision makes the comparison honest. Our ten inputs are all ratios, and a
> ratio cannot produce a price. So the model predicts the change, and we add it
> back: predicted close tomorrow equals today's close plus the predicted change.
>
> One real row from our committed results, 21 November 2024: today's close is
> 228.52, the model predicts a rise of ten cents, so the predicted close is 228.62.
> The actual close was 229.87.
>
> If we predicted the raw price, a model could score well by repeating today's
> level, and we would never learn whether it forecasts. Predicting the change
> forces it to contribute information.

**中文对照：**
> 这个设计决定让比较变得诚实。我们的十个输入全是比率——收益率、缺口、波动率。
> 比率无法直接产出价格。所以模型预测"变化量"，我们再把它加回去：
> 预测的明日收盘价 = 今日收盘价 + 预测变化量。
>
> 这是我们已提交结果中的一个真实样本，2024 年 11 月 21 日。今天收盘 228.52，
> 模型预测上涨 0.10，所以预测收盘 228.62；实际收盘 229.87。
>
> 为什么要这么麻烦？如果直接让模型预测原始价格，它只要重复今天的价格就能拿到不错的分数，
> 我们就永远不知道它到底会不会预测。预测变化量，逼模型贡献信息，而不是复述价格。

**→ Transition:** "Before we look at any result, we locked four questions."
**过渡：** "在看任何结果之前，我们先锁定了四个问题。"

---

## Slide 5 — Pre-Committed Questions, Zero Cherry-Picking · 1:00
**Presenter / 讲者:** Zhang Haoyu · **Page / 页码:** 5/21

**【中文要点】** 研究问题和评估标准在跑模型之前就写死；负面结果本身是有价值的结论。

**English — say this:**
> Four questions, written down before we ran anything. Do the models beat a naive
> baseline? Does more complexity improve generalisation? How does scaling affect
> different families? And what can a learner take from this?
>
> We also accepted something less comfortable in advance: a null result is a
> perfectly good finding. We were not going to keep re-tuning until something
> looked impressive. That commitment is what makes the next slide believable — if
> we had been free to search for a flattering number, the number would mean
> nothing.

**中文对照：**
> 四个问题，在跑任何实验之前就写下来。模型能否打败朴素基线？更复杂是否带来更好的泛化？
> 标准化对不同模型族有什么影响？学习者能从中带走什么？
>
> 我们还事先接受了一件不太舒服的事：负面结果完全可以是好结论。我们不会反复调参直到
> 某个结果看起来漂亮。正是这个承诺让后面的结果值得相信——如果我们可以自由挑选一个
> 好看的数字，那个数字就毫无意义。

**→ Transition:** "None of that means anything if the model can see the future."
**过渡：** "但如果模型能看到未来，这一切都没有意义。"

---

## Slide 6 — Ten Signals from the Past · 1:05
**Presenter / 讲者:** Dong Yuankun · **Page / 页码:** 6/21

**【中文要点】** 十个特征全部"只看过去"，没有价格水平，所以可解释、无泄漏。

**English — say this:**
> Ten features, all computed when today's market closes. Recent returns over one,
> five and twenty sessions. How far the price sits from its five- and twenty-session
> moving average. Volatility over ten and thirty sessions. Today's high-to-low
> range. Volume against its recent average. And the weekday.
>
> Two properties matter. Every feature uses bars up to and including today — a
> strict no-future rule that we test, not just claim. And none of them is a price
> level, which is exactly why the model has to predict a change, as Haoyu showed.
>
> If you are teaching this to beginners, this is the moment where the Week 3 idea
> of features and target stops being abstract: ten interpretable numbers go in, one
> number comes out.

**中文对照：**
> 十个特征，全部在当天收盘时计算：1、5、20 日收益率；价格距离 5 日和 20 日均线的偏离；
> 10 日和 30 日波动率；当天高低幅度；成交量相对近期均值；以及星期几。
>
> 有两点很重要。第一，所有特征只用今天及以前的交易日——这是"不许看未来"的硬规则，
> 我们用测试去验证，而不是口头保证。第二，它们都不是价格水平，这正是模型必须预测
> 变化量的原因。
>
> 如果是给初学者讲，这就是 Week 3 里"特征与目标"从抽象变具体的时刻：
> 十个可解释的数字进去，一个数字出来。

**→ Transition:** "Clean features are not enough — the split has to be clean too."
**过渡：** "特征干净还不够，切分也必须干净。"

---

## Slide 7 — Chronological Splitting and Zero-Leakage Discipline · 1:15
**Presenter / 讲者:** Dong Yuankun · **Page / 页码:** 7/21

**【中文要点】** 严格按时间切分，并在每个边界剔除一行，否则"明天"会渗进验证集。

**English — say this:**
> Here is the trap that catches almost everyone. A random split on a time series
> lets the model train on 2025 and be tested on 2021 — it has seen the future.
>
> It gets subtler. We predict tomorrow's close, so the last training example's
> answer is the first price in the validation block. Nothing crashes, no warning
> appears, and the score quietly improves.
>
> So: split strictly by date, no shuffling. Drop one row at each boundary, so a
> next-day target cannot bridge two blocks. Seal the final twenty percent — nothing
> in this talk comes from it. And we test the claim: six known leakage mistakes are
> injected one at a time, and every one must be caught.

**中文对照：**
> 这里有个几乎人人都会踩的陷阱。通常我们随机切分数据，但在时间序列上，
> 这意味着模型可能用 2025 年训练、用 2021 年测试——等于看过未来。
>
> 更隐蔽的是：我们预测明天的收盘价，所以**最后一个训练样本的答案**，
> 恰好就是验证集的第一个价格。程序不会崩溃、不会报警，但你的分数悄悄变好了。
>
> 所以我们做三件事：严格按日期切分、不打乱；在每个边界剔除一行，
> 让"次日目标"无法跨段；最后的 20% 完全封存——我们没读过它，本次演示没有任何数字来自它。
> 你看到的全部是验证集结果。
>
> 我们还会检验这件事：把六种已知的泄漏错误逐个注入代码，每一种都必须被抓到，
> 我们才相信结果。

**→ Transition:** "So the data is clean. Pak Hei will show what we put on top of it."
**过渡：** "数据干净了。接下来由 Pak Hei 讲我们在上面放了什么。"

---

## Slide 8 — Five Classical Models Across Three Paradigms · 1:05
**Presenter / 讲者:** Lau Pak Hei · **Page / 页码:** 8/21

**【中文要点】** 五个模型横跨线性、核、树集成三种机制，为的是"机制差异"，不是数量。

**English — say this:**
> Five models, chosen for contrast in mechanism rather than for a headcount. Two
> are linear: a near-ordinary-least-squares baseline, and ridge with an L2 penalty.
> One is a kernel method — support vector regression with an RBF kernel, which
> builds non-linear predictions from similarity to training points. Two are tree
> ensembles: a random forest that bags decorrelated trees, and histogram gradient
> boosting that fits trees sequentially to residuals.
>
> All five are trained through one shared code path, on identical features, with an
> identical search budget. That matters more than the list itself: a comparison is
> only meaningful if every model got the same opportunity.
>
> We deliberately avoided deep learning. The course handout discourages it, and for
> this question it would add opacity without adding information.

**中文对照：**
> 五个模型，选的是"机制上的差异"，不是凑数量。两个线性模型：接近普通最小二乘的基线，
> 和带 L2 惩罚的岭回归。一个是核方法——RBF 核的支持向量回归，用"与训练样本的相似度"
> 构造非线性预测。两个树集成：随机森林做去相关树的并行 bagging，
> 直方图梯度提升则顺序拟合残差。
>
> 五个模型都通过同一条代码路径训练，用同样的特征、同样的搜索预算。
> 这比模型清单本身更重要：只有每个模型获得同等机会，比较才有意义。
>
> 我们刻意没有用深度学习。课程讲义不建议，而对这个问题，它只会增加不透明性，
> 不会增加信息。

**→ Transition:** "Whatever the model, it has to beat something. That something is
usually forgotten." · **过渡：** "不管什么模型，都得先打败一个东西——而它常被忽略。"

---

## Slide 9 — The Opponent Everyone Forgets · 1:00
**Presenter / 讲者:** Lau Pak Hei · **Page / 页码:** 9/21

**【中文要点】** 基线是"明天=今天"；skill 分数以它为 0 点，负数就是不如规则。

**English — say this:**
> Before any model, we need its opponent: naive persistence. Tomorrow's close equals
> today's close. No training, no parameters.
>
> At a one-day horizon it is genuinely strong, because daily returns are nearly
> unpredictable. Its mean absolute error is about 2.91 on Apple and 1,604 on
> Bitcoin — and those numbers are not comparable, since the scales differ.
>
> So we score with skill: one minus the model's error over the rule's error. Zero
> means no better; negative means worse. That is the number to watch — not a
> model's own MAE, which alone tells you nothing.

**中文对照：**
> 在谈任何模型之前，先要有对手：朴素持续性规则。明天收盘价等于今天收盘价。
> 不训练、没有参数、几乎没有代码。
>
> 在"预测一天"这个尺度上它其实很强，因为日收益率接近不可预测。
> 它在美国苹果上的平均绝对误差约 2.91 美元，比特币约 1604 美元——
> 这两个数不能直接比较，因为两个资产的报价尺度完全不同。
>
> 所以我们用 skill 打分：1 减去模型误差除以规则误差。0 表示和规则一样，负数表示更差。
> 接下来请盯住这个数字，而不是模型自己的 MAE——单看 MAE 什么也说明不了。

**→ Transition:** "We have the models and the benchmark. Yancheng has the results."
**过渡：** "模型和标尺都有了。结果由 Yancheng 揭晓。"

---

# ACT III — THE REVEAL · 第三幕：揭晓结果

## Slide 10 — The Verdict: Complexity Yields Almost Zero Gain · 1:25
**Presenter / 讲者:** Zhang Yancheng · **Page / 页码:** 10/21

**【中文要点】** 最高只有 +0.52%；10 个标准化配置里 3 个不如规则；讲"范围"，不宣布冠军。

**English — say this:**
> Here is the answer. This table is the standardised variant for both assets, and
> the chart beside it plots exactly the same numbers — everything hugs the zero
> line.
>
> Three things to look at. The best Apple result is support vector regression at
> plus 0.52 percent. Half a percent. On Bitcoin the best here is ridge at plus
> 0.12. Second, look at the negative entries: the random forest on Apple is at minus
> 0.78 — it is genuinely worse than doing nothing, and the linear baseline is at
> minus 0.50. Overall, three of the ten standardised runs, and five of all twenty
> runs, lose to the one-line rule.
>
> I am deliberately not reading every cell. The point is the range, not the ranking.
> And to be fair to the models: some configurations really are slightly ahead. The
> question is whether that survives scrutiny.

**中文对照：**
> 这就是答案。这张表是"标准化版本"在两个资产上的结果，旁边的图画的正是同一组数字——
> 所有条目都紧贴零线。
>
> 请看三点。苹果最好的结果是支持向量回归 +0.52%——半个百分点；比特币这里最好是岭回归 +0.12%。
> 第二，看那些负数：苹果上的随机森林是 −0.78%，确实比"什么都不做"更差，线性基线是 −0.50%。
> 总体上，10 个标准化配置里有 3 个、全部 20 次运行里有 5 次，输给了那条一行规则。
>
> 我故意不逐格念数字：重点是**范围**，不是排名。也要为模型说句公道话：
> 有些配置确实略好一点。问题是，那点优势经得起检验吗？

**→ Transition:** "Which is exactly what we tested next."
**过渡：** "这正是我们下一步检验的。"

---

## Slide 11 — Statistical Reality Check: Every Gain Sits Inside the Noise · 1:10
**Presenter / 讲者:** Zhang Yancheng · **Page / 页码:** 11/21

**【中文要点】** 用保留时间相关性的分块 Bootstrap，20 个配置的 95% 区间全部包含 0，因此不能说"谁更好"。

**English — say this:**
> If you only look at a single number, plus 0.52 percent feels like a win. So we put
> an interval around each one. Every row here is one configuration; the dot is its
> skill, the bar is a 95% interval from a moving-block bootstrap — one thousand
> resamples of ten consecutive sessions, which keeps some of the day-to-day
> dependence that a naive resample would destroy.
>
> Every single bar crosses zero. All twenty of them. What that means is that we
> cannot distinguish these small positive numbers from sampling noise. So we do not
> claim a winner. We report a tie against the baseline.
>
> That is the honest reading of our own experiment, and honestly it is the more
> interesting result: the effect is small enough that the measurement method
> matters more than the leaderboard.

**中文对照：**
> 只看单个数字时，+0.52% 感觉像胜利。所以我们给每个数字加上区间。
> 每一行是一个配置，圆点是它的 skill，横线是移动分块 Bootstrap 得到的 95% 区间——
> 1000 次重采样、每块 10 个连续交易日，这样能保留一部分"相邻日彼此相关"的结构，
> 而朴素重采样会破坏它。
>
> 每一条横线都跨过 0，二十条全部如此。这意味着我们无法把这些微小的正数
> 与抽样噪声区分开。所以我们不宣布赢家，我们报告的是：与基线打平。
>
> 这是对我们自己实验最诚实的解读；而且说实话，这反而更有意思——
> 效应小到"测量方法"比"排行榜"更重要。

**→ Transition:** "So we asked the obvious next question: was it how we prepared the
data?" · **过渡：** "于是我们问下一个问题：会不会是数据准备方式的问题？"

---

# ACT IV — INVESTIGATING WHY · 第四幕：探究原因

## Slide 12 — Does Preprocessing Save the Models? · 1:20
**Presenter / 讲者:** Zhang Yancheng · **Page / 页码:** 12/21

**【中文要点】** 树对缩放完全免疫（预测完全相同）；核与正则化模型会变。但"改变行为"≠"提升性能"。

**English — say this:**
> Many beginners treat standardisation as a universal upgrade button. Our ablation
> says otherwise, and the pattern is exactly what the algorithm predicts.
>
> A tree splits on a threshold inside one feature. Rescale that feature and the
> order is unchanged, so an equivalent threshold exists — the tree should not care,
> and it does not. For both tree ensembles, predictions with and without scaling are
> *identical*, to the last digit. That is a strong internal control.
>
> A kernel method measures distances across several features, so rescaling changes
> which feature dominates. Ridge is different again: its penalty depends on
> coefficient sizes, which depend on scale. Both do move — in both directions. On
> Apple, scaling made the linear baseline slightly worse: 2.90 to 2.92, about 0.74
> percent.
>
> Preprocessing changes behaviour. It does not automatically improve prediction.

**中文对照：**
> 很多初学者把标准化当成万能升级按钮。我们的消融实验说明它不是——而且规律恰好符合算法原理。
>
> 决策树在单个特征上用阈值切分：这个值大于还是小于某个数？把特征整体缩放，顺序不变，
> 等效阈值仍然存在，所以树"不该在意"——它确实不在意。两个树模型在缩放前后的预测
> **完全相同**，一位数字都不差。这是一个很强的内部对照：说明标准化真的只是单调变换，
> 也没有别的东西依赖特征量级。
>
> 核方法不同：它计算跨多个特征的距离，缩放会改变哪个特征占主导。岭回归又不同：
> 它的惩罚与系数大小有关，而系数大小与尺度有关。这两类模型确实会变，而且方向不一致。
> 在苹果上，标准化甚至让线性基线稍微**变差**：从 2.90 变成 2.92，大约差 0.74%。
>
> 所以：预处理会改变行为，但不自动提升预测。

**→ Transition:** "So why didn't the extra capacity pay off?"
**过渡：** "那为什么多出来的容量没有带来收益？"

---

## Slide 13 — Why Complexity Hit a Wall: Signal and Structure · 1:00
**Presenter / 讲者:** Zhang Yancheng · **Page / 页码:** 13/21

**【中文要点】** 两个原因：信号本来就极弱（自相关≈0）；树集成只能做叶内平均，缺乏外推。

**English — say this:**
> Two reasons, and neither is a bug.
>
> First, the signal is thin. The correlation between one day's return and the next
> is about plus 0.02 for Apple and minus 0.03 for Bitcoin — an R² near 0.0005. When
> yesterday explains almost nothing about tomorrow, extra parameters fit noise.
>
> Second, the tree ensembles have a structural limit: a forest predicts an average
> of the target values in its leaves. On a change target that average is small and
> piecewise constant, so large moves are hard, and it cannot extrapolate beyond the
> range it has seen.
>
> Within a one-day horizon and standard indicators, extra capacity cannot
> manufacture signal that is not there.

**中文对照：**
> 两个原因，都不是程序错误。
>
> 第一，信号本来就弱：今天收益率与明天收益率的相关性，苹果约 +0.02，比特币约 −0.03，
> 对应 R² 大约 0.0005。当"昨天"几乎解释不了"明天"时，多出来的参数主要在拟合噪声。
> 这不是模型的失败，而是数据的性质。
>
> 第二，树集成有结构性限制。森林的预测是叶子里目标值的平均；在"预测变化量"这个目标下，
> 这个平均值很小、而且是分段常数，所以很难给出大幅变动。而且从构造上，它无法外推到
> 训练时见过的范围之外。
>
> 合起来说：在"预测一天"和常规指标下，额外的容量无法凭空造出数据里没有的信号。
> 这就是我们的结论，它比一个虚假的胜利更有价值。

**→ Transition:** "That is what the numbers say. Yuankun on what we learned building this."
**过渡：** "数字讲完了。构建过程中的收获由 Yuankun 讲。"

---

# ACT V — THE BIGGER LESSON · 第五幕：更大的启示

## Slide 14 — From Research Finding to a Turnkey Classroom Lab · 0:50
**Presenter / 讲者:** Zhang Yancheng · **Page / 页码:** 14/21

**【中文要点】** 结论已被打包成可直接进课堂的 60 分钟实验课 + 五道诊断题（含现场互动）。

**English — say this:**
> A finding is only useful to a teacher if it can be taught. So we packaged this into
> a sixty-minute guided Colab notebook, five formative tasks, and a teacher guide
> with worked solutions.
>
> Here is one task. A model reports plus 0.52 percent validation skill, but its 95%
> interval includes zero. Is it reliably better? A says yes, the score is positive.
> C says yes, complex models always generalise better. B says no — the evidence
> cannot separate the gain from noise.
>
> [Pause.] If you chose B, you did what most leaderboards never ask. We ran no
> learner study, so we claim no learning gain: this is a designed resource, ready
> for a classroom pilot.

**中文对照：**
> 一个发现，只有能被教给学生才有用。所以我们把它打包成：一节 60 分钟的引导式 Colab 课、
> 五道针对泄漏／基线／区间的形成性任务，以及一份带参考答案的教师指南。
>
> 举一道题说明它在做什么：某模型报告 +0.52% 的验证 skill，但 95% 区间包含 0，
> 它是否可靠更好？A 说"是，分数是正的"；C 说"是，复杂模型总是泛化更好"；
> B 说"不是——证据无法把这点增益与噪声分开"。
>
> [停顿] 如果你选 B，你刚刚做的正是大多数排行榜从不要求你做的事。
> 我们没有做学习者实验，所以不声称提升了学习效果——这是一份设计好的资源，
> 等着进真实课堂试点。

**→ Transition:** "What did we learn as builders?"
**过渡：** "作为构建者，我们学到了什么？"

---

## Slide 15 — Engineering and Pedagogical Takeaways · 1:10
**Presenter / 讲者:** Dong Yuankun · **Page / 页码:** 15/21

**【中文要点】** 四条工程纪律：尊重市场结构、防静默泄漏、预处理要匹配算法、负面结果有价值。

**English — say this:**
> Four things we would tell anyone building a comparison like this.
>
> Respect market structure: two trading calendars mean two pipelines, never one
> table aligned by row number. Guard against silent leakage: boundary purges and a
> sealed test set are not optional extras, because leakage does not announce itself.
> Match preprocessing to the algorithm: know *why* scaling moves kernels and not
> trees, otherwise you are tuning a knob you do not understand. And value negative
> results: a rigorous null finding teaches more than an overfitted leaderboard,
> because it is reproducible.
>
> If you remember one line from us as builders, it is this: a trustworthy experiment
> is worth infinitely more than an impressive-looking number.

**中文对照：**
> 四句话，给任何要做这类比较的人。
>
> 尊重市场结构：两套交易日历就是两条流水线，绝不能按行号硬对齐。防范静默泄漏：
> 边界剔除和封存测试集不是可选项，因为泄漏从不主动提示自己。预处理要匹配算法：
> 明白**为什么**标准化影响核方法却不影响树模型，否则你调的是一个自己不懂的旋钮。
> 珍视负面结果：一个严谨的"无显著优势"结论比一个过拟合的排行榜更有教学价值，
> 因为它是可复现的。
>
> 如果只记住我们作为构建者的一句话：一个可信的实验，价值远高于一个好看的数字。

**→ Transition:** "Shing Lam will close with our boundaries and the bigger lesson."
**过渡：** "最后由 Shing Lam 讲研究边界与更大的启示。"

---

## Slide 16 — Study Boundaries and the Bigger Lesson · 1:15
**Presenter / 讲者:** Lui Shing Lam · **Page / 页码:** 16/21

**【中文要点】** 老实交代边界与下一步；用一句记得住的话收尾；重申非投资建议。

**English — say this:**
> Let me be precise about what this covers. Two assets: Apple, and a
> single-exchange Bitcoin series. One historical window, a one-session horizon. The
> final twenty percent is still sealed — every number you saw is validation.
>
> Next steps are concrete: unseal that test block once, for a single confirmation,
> and pilot the classroom lab with a real cohort, so we can report something about
> teaching rather than only about models.
>
> One sentence to take away: the value of machine learning is not how complex a
> model looks, but whether it learns genuine signal beyond a meaningful baseline.
>
> And a necessary note: this is historical, educational analysis, not investment
> advice. Thank you — we are happy to take questions.

**中文对照：**
> 我最后把边界说清楚。两个资产：苹果，和一个单交易所的比特币序列。一个历史窗口，
> 一天的预测跨度。最后 20% 的数据仍然封存——你刚才看到的全部是验证集结果。
>
> 下一步很具体：在分析冻结后一次性解封测试集，做唯一一次确认；以及用真实学生班级
> 试跑这套实验课，那样我们才可能报告教学层面的结果，而不只是模型层面。
>
> 如果只带走一句话：机器学习的真正价值，不在于模型看起来多复杂，
> 而在于它是否在一个有意义的基线之上学到了真实信号。
>
> 最后是必要的说明：这是历史数据的教育性分析，不构成投资建议；
> 预测误差小也不意味着能盈利。谢谢大家，我们很乐意回答问题。

---

# Q&A — bilingual cheat sheet · 问答中英对照

| Question | English answer | 中文 |
|---|---|---|
| Why classical ML over deep learning? | The handout discourages it, it isn't needed for this question, and classical families keep the comparison interpretable. | 讲义不鼓励；这个问题也不需要；经典模型族让比较更可解释。 |
| Does this mean markets are a pure random walk? | At a one-day horizon they are close to it — that is the finding, and it is why persistence is strong. | 一天尺度上接近随机游走——这正是结论，也是基线强的原因。 |
| Why compare AAPL and BTC? | One session-based equity, one 24/7 market: same protocol, different microstructure. | 一个是交易时段股票，一个是全天市场：同协议、不同微观结构。 |
| Can this predict profitable trades? | No. Error metrics ignore costs and risk; we make no profitability claim. | 不能。误差指标不考虑成本和风险；我们不声称能盈利。 |
| Why isn't +0.52% skill enough? | Because all 20 bootstrap intervals include zero, so it is not separable from noise. | 因为 20 个 Bootstrap 区间全部包含 0，无法与噪声区分。 |
| Did you cherry-pick P2? | No — Backup 1 shows all 20 runs; best BTC overall is linear at P0, +0.26%. | 没有——Backup 1 有全部 20 组；比特币整体最好是未标准化的线性，+0.26%。 |
| Was the budget fair? | Identical for every lane: 10 trials, 90 s per cell. The protocol allows 24/300; we report what we used. | 所有模型相同：每格 10 次试验、90 秒。协议允许 24/300；我们报告实际使用的。 |
| How do you know there's no leakage? | Boundary purge, sealed test set, and a mutation harness where 6/6 injected defects must be caught. | 边界剔除、封存测试集，以及注入 6 种缺陷必须全部被抓到的变异测试。 |

# Backup slides · 备用页

| # | Slide | English one-liner | 中文 |
|---|---|---|---|
| 17 | Full 20-run matrix | "All twenty cells; the best BTC estimate overall is the unscaled linear model at +0.26%, still inside the noise band." | 全部 20 格；比特币整体最好的是未标准化线性 +0.26%，仍在噪声范围内。 |
| 18 | Fairness and manifest audit | "Identical features, splits, dates and budget; every run records commit, data hash and configuration." | 特征、切分、日期、预算都相同；每次运行都记录提交、数据哈希和配置。 |
| 19 | Catching leakage | "An audit found the boundary leak; perturbing one test price moved our metric by 0.408. Six injected defects must now be caught." | 审计发现边界泄漏；扰动一个测试价格让指标移动 0.408。现在六种注入缺陷必须全部被抓到。 |
| 20 | Permutation importance | "Short-horizon returns and volatility dominate, magnitudes are tiny, and importance is not causation." | 短期收益率和波动率占主导，量级很小，而且重要性不等于因果。 |
| 21 | Q&A cards | "We'll route each question to whoever owns that part." | 我们把问题交给最熟悉那部分的人。 |

# If you are running over · 超时怎么办

Check the clock at **slide 10**: it should read **≈10:45**.

| Situation | Cut | 中文 |
|---|---|---|
| 11:15 or later | Slide 13 → one sentence: "returns barely predict themselves, so extra capacity fits noise." (~40 s saved) | 第 13 页压成一句，省约 40 秒。 |
| 11:45 or later | Also name the three paradigms on slide 8 in one breath. (~30 s saved) | 再把第 8 页的三个范式一口气带过，省约 30 秒。 |
| **Never cut** | Slide 9 (baseline) and slide 10 (verdict). | **绝不能砍**第 9 页（基线）和第 10 页（结论）。 |

# Rehearsal checklist · 排练清单

- [ ] Every presenter has read their **English** blocks aloud twice. 每位讲者把英文大声读两遍。
- [ ] Every presenter can say their **【中文要点】** from memory. 不看稿能说出中文要点。
- [ ] The six handovers are rehearsed. 六句过渡要练。
- [ ] Two full timed run-throughs. 全流程计时彩排两次。
- [ ] Backup 1 and 3 are ready for the two most likely challenges. 准备好 Backup 1 和 3。

> **Reminder · 提醒** The presentation is in English; Chinese here is a comprehension
> aid only. 演示用英文；中文仅供理解。
