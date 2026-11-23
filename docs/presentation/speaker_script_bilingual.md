# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `slides/final/INT4096_Presentation.pdf` — 23 pages (16 narrative + 5 backup + 2 references)
**Structure source:** `docs/story/feature_extraction_story.md` (v2) · **Clock:** `timing_plan.md` · **Key messages:** `speaker_notes.md`
**Speech:** 17:15 planned (+0:45 handovers and slide changes, +2:00 Q&A = 20:00)

> ### How to use this document · 使用方法
> **The presentation is delivered in English. Read only the English blocks.**
> The Chinese is a translation to help you understand what you are saying, so you can speak from meaning instead of from memory. **Do not read the Chinese aloud.**
>
> **本演示用英文进行。上台只念英文部分。** 中文是逐段翻译，帮助你先理解、再自然地讲出来。中文不要念出来。
> 忘词时看 **【中文要点】**——那是这一页唯一必须传达的内容。

> **Speakers are not named here on purpose.** The deck is split into five contiguous *voice blocks* (see `timing_plan.md`). Assign people to blocks; every one of the five must speak. 本稿故意不写讲者姓名；按"语音分段"分配人员即可，五个人都必须开口。

---

## 0. Before you start · 开始之前

| Item | English | 中文 |
|---|---|---|
| Language | English throughout; slides are English too. | 全程英文，幻灯片也是英文。 |
| Pace | ~105 effective words per minute. The English below totals **1,808 words**, i.e. about 17 minutes of speech plus one deliberate pause on slide 15. | 约每分钟 105 词；英文总量 1,808 词，约 17 分钟，另加第 15 页一次有意的停顿。 |
| Who clicks | One person clicks for the whole talk (any member). | 全程由一个人翻页。 |
| Backup slides | 17–21 stay in the file. Open **Backup 1** for "did you cherry-pick?", **Backup 3** for "why drop a row?". | 备用页 17–21；被问"是否挑选结果"开 Backup 1，问"为什么删一行"开 Backup 3。 |
| Disclaimer | On slide 1 and slide 16. Never remove. | 免责声明在第 1、16 页，不能删。 |
| Numbers | Never invent one. If unsure: "it is in our run records". | 绝不编数字；不确定就说"记录在仓库里"。 |
| **Wording discipline** | Say "every **model-performance** number is from validation". Do **not** say "every number in this talk" — the dataset sizes and the return-correlation diagnostic use the full price history. | 要说"每一个**模型表现**数字都来自验证集"，不要说"每一个数字"——数据规模和收益率自相关用了完整价格序列。 |

### The whole project in 30 seconds · 30 秒讲清整个项目

> **English.** We took two price histories, Apple and Bitcoin. From ten backward-looking ratios, five classical models predicted the next session's price *change*, which we added back to today's price. We compared every model with one free rule: tomorrow equals today. Nothing beat that rule by more than about half a percent, and every confidence interval included zero.

> **中文.** 两组价格数据：苹果和比特币。用十个"只看过去"的比率特征，让五种经典模型预测下一交易日的价格**变化量**，再加回今天的价格。所有模型都和一条免费规则比较：明天等于今天。没有任何模型比它好过约 0.5%，所有置信区间都包含 0。

---

# OPENING — THE HIGH-SCORE TRAP · 开场：高分陷阱

## Slide 1 — Learning Machine Learning Through Financial Forecasting · 0:50
**Page / 页码:** 1/23

**【中文要点】** 用一个钩子开场：SVR 和"复制昨天收盘价"的 R² 只差 0.0001。

**English — say this:**
> Good morning. Here is a number. On Apple's validation data, a support vector regression model scores an R-squared of zero point nine five five six. Impressive? Now take a rule that simply copies yesterday's closing price. It scores zero point nine five five five. The difference is in the fourth decimal place. Our project is about what to ask when someone shows you a score like that. Over the next seventeen minutes we will show you where a score can hide the truth, and how to teach students to see it.

**中文对照：**
> 大家早上好。先看一个数字。在苹果验证集上，一个支持向量回归模型的 R² 是 0.9556。很厉害吗？再看一条规则：直接把昨天的收盘价抄过来，R² 是 0.9555。差别在小数点后第四位。我们的项目讲的就是：别人给你看这样的分数时，你该问什么。接下来十七分钟，我们会展示分数怎样掩盖真相，以及怎样教学生看穿它。

**→ Transition:** "So what should we ask?" · **过渡：** "那我们该问什么？"

---

## Slide 2 — Three Questions to Ask of Any AI Score · 1:00
**Page / 页码:** 2/23

**【中文要点】** 三个问题是全场主线：看到什么？简单规则多好？有多确定？

**English — say this:**
> We boil it down to three questions. One: what information could the model see when it made the prediction? Two: how well did a simple rule do on exactly the same examples? Three: how certain is the improvement?
>
> Every part of this talk answers one of them. The data and processing sections answer the first. Training and evaluation answer the second and third. At the end we show how we turned them into a lesson for senior secondary and first-year university students who are new to machine learning. Financial data is only the vehicle. It punishes careless evaluation quickly, which is exactly why it teaches well.

**中文对照：**
> 我们把它浓缩成三个问题。一，模型做预测时能看到什么信息？二，一条简单规则在完全相同的样本上做得怎么样？三，这点提升有多确定？
>
> 整场报告的每一部分都在回答其中之一。数据和处理回答第一个；训练和评估回答第二、第三个。最后我们展示如何把它做成一节面向高中高年级和大一机器学习新手的课。金融数据只是载体——它会很快惩罚粗糙的评估，所以特别适合教学。

**→ Transition:** "Start with the data." · **过渡：** "先看数据。"

---

# ACT I — DATA · 第一幕：数据选择

## Slide 3 — Two Markets, One Protocol · 1:10
**Page / 页码:** 3/23

**【中文要点】** 两个结构不同的市场，同一套协议；数据质量闸门"拒绝而不修补"；BTC 是单一交易所。

**English — say this:**
> Act one: the data. We use two markets on purpose. Apple trades in exchange sessions, in dollars: 1,255 daily bars. Bitcoin trades around the clock: 1,828 daily bars from one exchange, Binance, quoted in USDT. So it is one venue's price, not a global index, and we say so. Prices differ by orders of magnitude, so we compare models only with unit-free scores.
>
> The same protocol on two different calendars is a robustness check. A conclusion that holds in only one market is not a conclusion about machine learning.
>
> Before any model runs, both datasets pass automated checks for duplicates, missing values, and invalid prices or volumes. The pipeline rejects bad data instead of repairing it. Every file is fingerprinted, so each number traces back to the same bytes.

**中文对照：**
> 第一幕：数据。我们有意用两个市场。苹果按交易所时段交易，美元计价：1255 根日线。比特币全天候交易：1828 根日线，来自 Binance 一个交易所，USDT 计价。所以这是单一交易所的价格，不是全球指数，我们明确说明。两者价格相差几个数量级，所以只用无单位的分数来比较模型。
>
> 同一协议跑在两种日历上，是一个稳健性检验：只在一个市场成立的结论，不是关于机器学习的结论。
>
> 任何模型运行之前，两份数据都要通过自动检查：重复、缺失、非法价格或成交量。流水线遇到坏数据是**拒绝**而不是**修补**。每个文件都有哈希指纹，所以每个数字都能追溯到同一份字节。

**→ Transition:** "Now, what goes into the model?" · **过渡：** "那么，模型的输入是什么？"

---

# ACT II — PROCESSING · 第二幕：数据处理

## Slide 4 — Ten Inputs Use Only Information Available at the Close · 1:00
**Page / 页码:** 4/23

**【中文要点】** 十个特征全部只用截至当天收盘的信息，并且没有价格水平；"不看未来"是被测试的，不是口头保证。

**English — say this:**
> Act two: processing. We build ten features. Returns over one, five and twenty sessions. Gaps from the five- and twenty-session averages. Volatility over ten and thirty sessions. Today's high-to-low range, volume against its recent average, and the weekday.
>
> Every window ends at today's close. That is a rule we test, not just claim: we append absurd future prices, rebuild the features, and the earlier rows must not change by a single digit.
>
> Notice what is missing. No feature is a price level. And all five models, on both assets, get exactly these ten inputs, so the comparison is about the models, not about who was given better information.

**中文对照：**
> 第二幕：数据处理。我们构造十个特征：1、5、20 日收益率；价格与 5 日、20 日均线的偏离；10 日和 30 日波动率；当天高低幅度；成交量相对近期均值；以及星期几。
>
> 每个窗口都截止于今天收盘。这条规则是被**测试**的，不只是口头说：我们在数据末尾追加离谱的未来价格，重新构造特征，之前的行不能有任何一位数字变化。
>
> 注意缺了什么：没有任何一个特征是价格水平。而且五个模型在两个资产上用的恰好是这十个输入，所以比较的是模型，而不是谁拿到了更好的信息。

**→ Transition:** "No price level means the model cannot output a price." · **过渡：** "没有价格水平，模型就无法直接输出价格。"

---

## Slide 5 — Predicting the Change Gives Models a Clearer Task · 1:05
**Page / 页码:** 5/23

**【中文要点】** 让模型预测"变化量"再加回已知价格；这是被一次失败逼出来的设计；用一个真实样本说明。

**English — say this:**
> Because no feature is a price level, a model cannot output a price. So we ask it for the change and add that to the price we already know. Forecast equals today's close plus the predicted change.
>
> This was forced on us. Our first run predicted the price directly and scored far worse than copying yesterday. That turned out to be an artefact of the representation, not a failure of the model.
>
> Here is one real validation day, the twenty-first of November 2024. Close: 228.52. Predicted change: plus ten cents. Forecast: 228.62. The next close was 229.87. The rule that predicts no change is off by 1.35; the model by 1.25. That zero-change rule is our opponent.

**中文对照：**
> 因为没有任何特征是价格水平，模型无法直接输出价格。所以我们让它预测"变化量"，再加到已知价格上：预测收盘 = 今日收盘 + 预测变化量。
>
> 这是被逼出来的。我们第一次直接预测价格，结果比"抄昨天"差得多。后来发现那是**表示方式**造成的假象，不是模型本身失败。
>
> 这是一个真实的验证集样本，2024 年 11 月 21 日：收盘 228.52，预测上涨 0.10，预测价 228.62，次日实际 229.87。"变化为零"的规则误差 1.35，模型误差 1.25。这条零变化规则就是我们的对手。

**→ Transition:** "Next: how we split the data." · **过渡：** "接下来：怎么切分数据。"

---

## Slide 6 — Chronological Splits, Train-Only Fitting, a Sealed Test Block · 1:10
**Page / 页码:** 6/23

**【中文要点】** 按时间切；每个边界删一行（否则标签泄漏）；预处理只在训练行上拟合；最后 20% 封存。

**English — say this:**
> Never shuffle a time series. A random split lets a model train on 2025 and be tested on 2021. We split by date: sixty percent train, twenty validation, twenty test.
>
> There is a subtler trap. We predict tomorrow's close, so the last training row's answer is the first price in the validation block, and the last validation row's answer sits inside the test block. Nothing crashes. The score just improves. So we drop one row at each boundary. In our audit, changing a single test-period price moved the headline metric by 0.408, many times any model's edge.
>
> Scaling is fitted on training rows only. And the final twenty percent is sealed: no model-performance number in this talk comes from it.

**中文对照：**
> 时间序列绝不能打乱。随机切分会让模型用 2025 年训练、用 2021 年测试。我们按日期切：60% 训练、20% 验证、20% 测试。
>
> 还有一个更隐蔽的陷阱。我们预测明天的收盘价，所以最后一个训练样本的答案就是验证集的第一个价格，最后一个验证样本的答案落在测试块里。程序不会崩溃，分数只是悄悄变好。所以我们在每个边界各删一行。审计时，改动**一个**测试期价格就让头条指标移动 0.408，远大于任何模型的优势。
>
> 标准化只在训练行上拟合。最后的 20% 是封存的：本次演示中没有任何模型表现数字来自它。

**→ Transition:** "But how do we know the pipeline cannot peek?" · **过渡：** "但怎么知道流水线不会偷看？"

---

## Slide 7 — How We Know the Pipeline Cannot Peek · 0:55
**Page / 页码:** 7/23

**【中文要点】** 故意注入 6 种泄漏缺陷，测试必须全部失败；早期版本做不到，所以重做。

**English — say this:**
> We attack it. A script injects six known leakage mistakes, one at a time: reading the next bar, a disguised version of the same thing, a centred rolling window, backward filling, a statistic computed over the whole series, and a scaler fitted on training plus test data. The test suite must fail every time. All six are caught.
>
> Our first version did not. An independent audit found it missed a one-bar look-ahead and a backward fill. We rebuilt it.
>
> Eighty-three automated tests now pass, and this mutation check runs separately. A test suite that cannot fail proves nothing.

**中文对照：**
> 我们主动攻击它。一个脚本逐个注入六种已知的泄漏错误：读取下一根 K 线、同一件事的伪装写法、居中滚动窗口、后向填充、用整段序列的统计量、以及在训练加测试数据上拟合标准化。测试套件每次都必须失败。六种全部被抓到。
>
> 我们的第一版并没有做到：独立审计发现它漏掉了一步前视和后向填充。于是我们重做了。
>
> 现在 83 项自动测试全部通过，而这个变异检查是单独运行的。一个不可能失败的测试套件什么也证明不了。

**→ Transition:** "With clean inputs, let's meet the models." · **过渡：** "输入干净了，来看模型。"

---

# ACT III — TRAINING · 第三幕：训练

## Slide 8 — Five Models, Three Mechanisms · 1:00
**Page / 页码:** 8/23

**【中文要点】** 五个模型选的是"机制差异"，每个都对应一个教学问题；不用深度学习。

**English — say this:**
> Act three: the models. Five, chosen for how they work, not for the headcount. A linear baseline and ridge regression, which adds an L2 penalty. Support vector regression with an RBF kernel, which predicts from similarity to training examples. A random forest, which averages many decorrelated trees, and histogram gradient boosting, which fits trees one after another to the remaining error.
>
> Each earns its place with a teaching question. Does a penalty tame overfitting? Do distances make a model sensitive to scale? Do thresholds make trees immune?
>
> We avoided deep learning. The course handout discourages it, and classical models keep the comparison interpretable.

**中文对照：**
> 第三幕：模型。五个，选的是它们的工作机制，不是凑数量。线性基线，和加了 L2 惩罚的岭回归；RBF 核的支持向量回归，根据与训练样本的相似度预测；随机森林，平均许多去相关的树；直方图梯度提升，让树一棵接一棵地拟合剩余误差。
>
> 每个模型都对应一个教学问题：惩罚能不能抑制过拟合？距离会不会让模型对尺度敏感？阈值会不会让树免疫？
>
> 我们没有用深度学习：课程讲义不鼓励，而经典模型让比较更可解释。

**→ Transition:** "Then, how do we keep it fair?" · **过渡：** "那么怎么保证公平？"

---

## Slide 9 — Same Budget, Same Rules, Two Preprocessing Settings · 1:00
**Page / 页码:** 9/23

**【中文要点】** 公平由代码强制：同特征、同种子、同预算；调参只在训练块内部；P0/P2 两种预处理；20 次运行全部记录。

**English — say this:**
> Fairness is enforced in code. Every model on every asset gets the same ten features, the same seed, and the same search budget: ten random trials, at most ninety seconds per cell. The protocol allows twenty-four and three hundred; we report what we used.
>
> Candidates are scored by five expanding-window folds inside the training block only. The validation block never touches tuning.
>
> We run two preprocessing settings. P0 keeps the original feature values. P2 standardises them using training data. Five models, two assets, two settings: twenty runs. Each is recorded with its commit, data hash and configuration, and a failed run would be kept, not deleted. None failed.

**中文对照：**
> 公平性是用代码强制的。每个资产上的每个模型都用同样的十个特征、同一个随机种子、同一个搜索预算：十次随机试验，每个格子最多 90 秒。协议允许 24 次和 300 秒，我们如实报告实际用的。
>
> 候选配置只用**训练块内部**的五折扩展窗口来打分。验证块从不参与调参。
>
> 我们跑两种预处理：P0 保持原始特征值，P2 用训练数据标准化。五个模型、两个资产、两种设置：共 20 次运行。每次都记录提交号、数据哈希和配置；失败的运行会保留而不是删除。（实际没有失败。）

**→ Transition:** "Now to evaluation — and to the opponent." · **过渡：** "进入评估，先看对手。"

---

# ACT IV — EVALUATION · 第四幕：评估

## Slide 10 — The Opponent: Copy Today's Close · 0:55
**Page / 页码:** 10/23

**【中文要点】** 基线 = 明天等于今天；用 skill（相对基线的提升）打分，0 表示一样好；R² 不用来排名。

**English — say this:**
> Act four: evaluation. Before judging any model we need its opponent: naive persistence. Tomorrow equals today. No training, no parameters. Its mean absolute error is about 2.91 dollars on Apple and 1,604 on Bitcoin, and those cannot be compared, because the scales differ.
>
> So we score with skill: one minus the model's error divided by the rule's error. Zero means no better. Negative means worse.
>
> This is also why we do not rank by R-squared. Persistence already scores 0.9555, because prices are tied to yesterday's level. The real question is whether a model beats the rule at predicting the change.

**中文对照：**
> 第四幕：评估。评判任何模型之前，先要有它的对手：朴素持续性——明天等于今天。不训练、没有参数。它的平均绝对误差在苹果上约 2.91 美元，在比特币上约 1604，这两个数不能比，因为尺度不同。
>
> 所以我们用 skill 打分：1 减去模型误差除以规则误差。0 表示没有更好，负数表示更差。
>
> 这也是我们不用 R² 排名的原因：持续性规则的 R² 已经是 0.9555，因为价格紧贴昨天的水平。真正的问题是：在预测"变化"上，模型能否打败这条规则。

**→ Transition:** "So — the results." · **过渡：** "那么，看结果。"

---

## Slide 11 — Best Skill Is +0.52%; 5 of 20 Runs Lose · 1:20
**Page / 页码:** 11/23

**【中文要点】** 最高只有 +0.52%（约 1.5 美分）；20 次里 5 次输给规则；讲范围，不宣布冠军；两种预处理都在 Backup 1。

**English — say this:**
> Here are the results, on validation data only. The best Apple run is support vector regression, standardised, at plus 0.52 percent skill. In money, that is about one and a half cents less average error per forecast. On Bitcoin, the best is the linear baseline, unscaled, at plus 0.26.
>
> Now look at the other end. On Apple, the random forest sits at minus 0.78: worse than copying yesterday. Across all twenty runs, five lose to the one-line rule. Among the ten standardised runs, three do.
>
> I am deliberately not reading every cell. The point is the range: from minus 0.78 to plus 0.52, a spread of 1.3 points. Some configurations really are slightly ahead. Both preprocessing settings are in the full table in Backup 1, so nothing is cherry-picked. The question is whether those small leads survive an honest uncertainty check.

**中文对照：**
> 这是结果，只来自验证集。苹果最好的是标准化后的支持向量回归，skill 为 +0.52%。换成钱，大约是每次预测平均误差少 1.5 美分。比特币最好的是未缩放的线性基线，+0.26%。
>
> 再看另一端：苹果上的随机森林是 −0.78%，比"抄昨天"还差。全部 20 次运行里，5 次输给这条一行规则；10 个标准化运行里有 3 个。
>
> 我故意不逐格念。重点是**范围**：从 −0.78 到 +0.52，跨度 1.3 个百分点。有些配置确实略好一点。两种预处理的完整表格在 Backup 1，所以没有挑选。问题是：这点微小的领先经得起诚实的不确定性检验吗？

**→ Transition:** "That is exactly what we tested next." · **过渡：** "这正是我们下一步检验的。"

---

## Slide 12 — All 20 Bootstrap Intervals Include Zero · 1:20
**Page / 页码:** 12/23

**【中文要点】** 配对 + 移动分块 Bootstrap（块长 10、1000 次、95%）；20/20 区间含 0 → 与基线打平，不是赢家；区间是"指示性"的。

**English — say this:**
> So we put an interval around every score. We pair each model's errors with the rule's errors on the same dates, resample blocks of ten consecutive days a thousand times, and take a ninety-five percent interval. Blocks keep some of the dependence between neighbouring days that a naive resample would destroy.
>
> Every row is one run. The dot is its skill. The bar is the interval. Every single bar crosses zero. All twenty, including the best Apple run.
>
> With 244 validation days for Apple and 358 for Bitcoin, we cannot separate these gains from noise. So we do not name a winner. We report a tie with the baseline. These intervals are indicative, not confirmatory, and we say so. A small positive number with an interval across zero is one of the most common mistakes in reading AI scores.

**中文对照：**
> 所以我们给每个分数加上区间。把每个模型的误差和规则的误差按相同日期配对，每次重采样十个连续交易日的块，重复一千次，取 95% 区间。分块保留了相邻日之间的部分相关性，而朴素重采样会破坏它。
>
> 每一行是一次运行，圆点是它的 skill，横线是区间。每一条横线都跨过 0——二十条全部如此，包括苹果最好的那次。
>
> 苹果只有 244 个验证日，比特币 358 个，我们无法把这些增益和噪声区分开。所以我们不宣布赢家，只报告"与基线打平"。这些区间是指示性的、不是确证性的，我们也这样说。"一个小的正数、区间却跨过 0"，是解读 AI 分数时最常见的错误之一。

**→ Transition:** "Maybe the data just needs better preparation?" · **过渡：** "也许是数据准备得不够好？"

---

## Slide 13 — Scaling Changes Some Models and Leaves Trees Untouched · 1:05
**Page / 页码:** 13/23

**【中文要点】** 树对缩放完全不变（预测逐位相同）；核与惩罚模型会变；预处理改变行为，不等于改善预测。

**English — say this:**
> Does preprocessing save the models? Beginners often treat standardising as an upgrade button. Our ablation says no, and the pattern matches the algorithms.
>
> A tree splits on a threshold inside one feature. Rescale that feature and an equivalent threshold exists. For both tree ensembles, predictions with and without scaling are identical, to the last digit. A kernel measures distances across features, and a ridge penalty depends on coefficient size, so both react to scale. On Apple, scaling made the linear baseline worse, by 0.74 percent.
>
> Preprocessing changes behaviour. It does not automatically improve prediction. And whether a model is sensitive to it is something we can predict from the mechanism.

**中文对照：**
> 预处理能拯救模型吗？初学者常把标准化当成"升级按钮"。我们的消融实验说不是，而且规律与算法原理吻合。
>
> 树在单个特征上按阈值切分。把这个特征整体缩放，等效的阈值仍然存在。两种树集成在缩放前后的预测**逐位相同**。核方法计算跨特征的距离，岭回归的惩罚与系数大小有关，所以两者都对尺度有反应。在苹果上，标准化让线性基线变差了 0.74%。
>
> 预处理改变行为，但不会自动提升预测。而模型是否对它敏感，我们可以从机制上预先判断。

**→ Transition:** "So why do the gains stay so small?" · **过渡：** "那为什么增益始终这么小？"

---

## Slide 14 — Why the Gains Stay Small · 1:05
**Page / 页码:** 14/23

**【中文要点】** 相邻日收益率相关性≈0；规则已经贴着价格水平；这只是一个描述性诊断，不是"没有信号"的证明。

**English — say this:**
> Why do the gains stay small? One reason is how little the past says about tomorrow's move. The correlation between one day's return and the next is plus 0.02 for Apple and minus 0.03 for Bitcoin. Essentially zero.
>
> Another is that the rule already tracks the price level. In this toy example the forecast stays close to the price and misses both moves, yet it would score well on any level-based measure. What is left to learn is the daily change, and it is small.
>
> This is one descriptive diagnostic, computed on the whole price history. It is not proof that no signal exists. It is a reason a tie is plausible.

**中文对照：**
> 为什么增益这么小？一个原因是：过去对明天的变动几乎没有说明力。今天收益率与明天收益率的相关性，苹果约 +0.02，比特币约 −0.03，基本为零。
>
> 另一个原因是：这条规则已经贴着价格水平。在这个示意例子里，预测始终接近价格，却两次都没抓到变动，但按"水平"类指标看分数很高。剩下要学的只有每日变化，而它很小。
>
> 这只是一个描述性诊断，用的是完整价格序列。它不能证明"没有信号"，只说明"打平"是合理的。

**→ Transition:** "Now: what do we hand to teachers?" · **过渡：** "现在：我们把什么交给老师？"

---

# ACT V — EDUCATION · 第五幕：教育

## Slide 15 — A 60-Minute Lesson Built on the Result · 1:15
**Page / 页码:** 15/23

**【中文要点】** 结论被做成 60 分钟 Colab 课 + 五个任务 + 教师指南；现场做一道选择题（答案 B）；没有学习者研究，不声称学习增益。

**English — say this:**
> Act five: teaching. We turned the result into a sixty-minute Colab lesson with five tasks and a teacher guide with worked answers. Learners rebuild the baseline, spot a leaking feature, build ten legal features, read bootstrap intervals, and transfer the three questions to a new setting, such as school attendance. A separate notebook rebuilds our results from the hashed data.
>
> Here is one check. A model reports plus 0.52 percent skill, but its interval includes zero. Is it reliably better? A: yes, it is positive. C: yes, complex models generalise better. B: no, the evidence cannot separate it from noise.
>
> If you chose B, you applied the lesson. We ran no learner study, so we claim no learning gain.

**中文对照：**
> 第五幕：教学。我们把结果做成一节 60 分钟的 Colab 课，含五个任务和一份带参考答案的教师指南。学习者重建基线、识别泄漏特征、构造十个合法特征、解读 Bootstrap 区间，并把三个问题迁移到新场景，比如学校出勤率。另有一个独立的 notebook，用带哈希的数据重建我们的全部结果。
>
> 来做一道题。某模型报告 +0.52% 的 skill，但区间包含 0。它可靠地更好吗？A：是，分数是正的。C：是，复杂模型泛化更好。B：不，证据无法把它与噪声分开。
>
> [停顿] 如果你选了 B，你就用上了这节课。我们没有做学习者研究，所以不声称任何学习增益。

**→ Transition:** "Let me close with the skill, and its limits." · **过渡：** "最后讲这项技能，以及它的边界。"

---

## Slide 16 — The Skill Students Can Take to Any AI Claim · 1:05
**Page / 页码:** 16/23

**【中文要点】** 三个问题就是带得走的技能；诚实交代边界与下一步；重申非投资建议。

**English — say this:**
> Let me close with the skill, and its limits. Whenever someone shows you an AI score, ask: what could the model see? How did a simple rule do on the same examples? How certain is the improvement? On our evidence the honest answers were: the information was legitimate, the simple rule was nearly unbeatable, and the improvement was uncertain.
>
> The limits: two assets, one of them from a single exchange; one historical window; a one-day horizon; and a sealed test block we have not opened. Two further preprocessing variants are defined but not yet run.
>
> This is historical, educational analysis, not investment advice. Thank you. We are happy to take questions.

**中文对照：**
> 最后讲这项技能和它的边界。每当有人给你看一个 AI 分数，就问：模型能看到什么？简单规则在相同样本上表现如何？提升有多确定？就我们的证据而言，诚实的回答是：信息是合法的，简单规则几乎打不败，提升不确定。
>
> 边界：两个资产，其中一个来自单一交易所；一个历史窗口；一天的预测跨度；以及一个我们尚未打开的封存测试块。另有两种预处理变体已定义但还没运行。
>
> 这是历史数据的教育性分析，不构成投资建议。谢谢大家，我们很乐意回答问题。

---

# Q&A — bilingual cheat sheet · 问答中英对照

| Question | English answer | 中文 |
|---|---|---|
| Why classical ML, not deep learning? | The handout discourages it, and classical families keep the comparison interpretable. | 讲义不鼓励；经典模型让比较更可解释。 |
| Is this just a random walk? | At a one-day horizon the return correlation is near zero, which fits that picture. It probes one kind of signal, so it is not proof. | 一天尺度上收益率相关性接近 0，与随机游走相符；但它只探测一种信号，不是证明。 |
| Why AAPL and BTC? | One session-based equity, one 24/7 market: same protocol, different microstructure. | 一个交易时段股票，一个全天市场：同协议、不同微观结构。 |
| Did you leak future data? | Chronological split, a purged boundary row, a sealed test block, and a mutation check where 6 of 6 injected defects must be caught → Backup 3. | 按时间切分、边界删行、封存测试集、6/6 变异必须被抓到 → Backup 3。 |
| Did you cherry-pick P2? | No. Backup 1 shows all 20 runs. The best Bitcoin result overall is the unscaled linear baseline at +0.26%. | 没有。Backup 1 有全部 20 次；比特币整体最好的是未缩放线性基线 +0.26%。 |
| Was the budget fair? | Identical for every lane: 10 trials, 90 s per cell. The protocol allows 24 and 300; we report what we used → Backup 2. | 所有模型相同：10 次试验、每格 90 秒；协议允许 24/300，我们报告实际使用的。 |
| Is +0.52% meaningful? | Not by our own test: all 20 bootstrap intervals include zero. | 按我们自己的检验不是：20 个区间全包含 0。 |
| Why only P0 and P2? | The protocol defines five variants. P1 would be identical to P0 because the data has no missing values, so it is logged as not run. P3 and P4 are not yet run. | 协议定义了五种；P1 因无缺失值会与 P0 相同，登记为未运行；P3、P4 尚未运行。 |
| Why do some chosen hyperparameters sit at the grid edge? | Possibly the grid was narrow. It does not change the direction of the result, but we did not tune each model to its limit. | 可能网格偏窄；不改变结论方向，但我们没有把每个模型调到极限。 |
| Can this make money? | No. Error metrics ignore costs and risk; we make no profitability claim. | 不能。误差指标不含成本和风险；我们不声称盈利。 |
| Did the lesson improve learning? | We have not tested that. It is a designed resource ready for a classroom pilot. | 没有测试过；它是等待课堂试点的设计好的资源。 |

# Backup slides · 备用页

| # | Slide | English one-liner | 中文 |
|---|---|---|---|
| 17 | Full 20-run matrix | "All twenty cells. The best Bitcoin result is the unscaled linear baseline at +0.26%, still inside the noise band." | 全部 20 格；比特币最好 +0.26%，仍在噪声范围内。 |
| 18 | Fairness and manifest audit | "Identical features, splits, dates and budget. Every run records commit, data hash and configuration." | 特征、切分、日期、预算都相同；每次运行记录提交、数据哈希、配置。 |
| 19 | Why one row is dropped | "Friday's label is Monday's price. Without the purge, the last training answer lives inside the validation block." | 周五的标签是周一的价格；不删行，最后一个训练答案就在验证块里。 |
| 20 | Permutation importance | "One- and five-day returns, 30-day volatility and the 20-day average gap matter most. Magnitudes are tiny. Importance is not causation." | 1、5 日收益率、30 日波动率、20 日均线偏离最重要；量级很小；重要性不等于因果。 |
| 21 | Q&A cards | "Short, prepared answers to the five most likely questions." | 五个最可能问题的简短答案。 |

# If you are running over · 超时怎么办

Check the clock at the **end of slide 9**: it should read **≈9:10** (see `timing_plan.md`).

| Situation | Cut | 中文 |
|---|---|---|
| 9:40 or later after slide 9 | Slide 14 → two sentences: "Returns barely predict themselves, and the rule already tracks the price level. A tie is plausible." (~30 s) | 第 14 页压成两句，省约 30 秒。 |
| 10:10 or later | Also name the five models on slide 8 in one breath, no teaching questions. (~25 s) | 再把第 8 页五个模型一口气带过，省约 25 秒。 |
| **Never cut** | Slide 10 (baseline) and slide 11 (results). | **绝不能砍**第 10 页（基线）和第 11 页（结果）。 |

# Rehearsal checklist · 排练清单

- [ ] Every speaker has read their **English** blocks aloud twice. 每位讲者把英文大声读两遍。
- [ ] Every speaker can say their **【中文要点】** from memory. 不看稿能说出中文要点。
- [ ] The four handovers between voice blocks (after slides 3, 6, 10, 13) are rehearsed. 语音分段之间的交接要练。
- [ ] Two full timed run-throughs with a visible clock. 全流程计时彩排两次。
- [ ] Backup 1 and Backup 3 are ready in a second window. 准备好 Backup 1 和 3。
- [ ] Nobody says "every number is from validation". 没人说"每个数字都来自验证集"。

> **Reminder · 提醒** The presentation is in English; Chinese here is a comprehension aid only. 演示用英文；中文仅供理解。
