# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `slides/final/INT4096_Presentation.pdf` — 24 pages (17 narrative + 5 backup + 2 references)
**Structure:** one part per pipeline stage: Data Selection → Processing & Features → Models & Tuning → Evaluation → Teaching Design
**Clock:** `timing_plan.md` · **Key messages:** `speaker_notes.md` · **Story:** `docs/story/feature_extraction_story.md`
**Speech:** 16:15 planned (+0:40 for four handovers and slide changes, +2:00 Q&A = 18:55 inside the 20:00 slot)

> ### How to use this document · 使用方法
> **The presentation is delivered in English. Read only the English blocks.**
> The Chinese is a translation to help you understand what you are saying, so you can speak from meaning instead of from memory. **Do not read the Chinese aloud.**
>
> **本演示用英文进行。上台只念英文部分。** 中文是逐段翻译，帮助你先理解、再自然地讲出来。中文不要念出来。
> 忘词时看 **【中文要点】**——那是这一页唯一必须传达的内容。

> ### Who speaks · 分工
>
> | Slides | Part | Speaker | Time |
> |---|---|---|---:|
> | 1–5 | Opening, Part 1 Data Selection | **Dong Yuankun** | 4:35 |
> | 6–12 | Part 2 Processing & Features, Part 3 Models & Tuning | **Zhang Yancheng** | 7:00 |
> | 13–15 | Part 4 Evaluation | **Zhang Haoyu** | 2:50 |
> | 16 | Part 5 Teaching Design | **Lau Pak Hei** | 1:00 |
> | 17 | Part 5 Summary and close | **Lui Shing Lam** | 0:50 |
>
> The speaker's name is also in each slide's footer. 每页幻灯片的页脚也写着讲者姓名。
>
> **Slides 16 and 17 are written in short, plain sentences on purpose: read them exactly as written, slowly, without adding anything.** If either speaker stops for more than about five seconds, **Zhang Yancheng** steps in and finishes the slide from its 【中文要点】. 第 16、17 页刻意写成短句：照稿慢慢读，不要自由发挥。若讲者停顿超过约 5 秒，由 Zhang Yancheng 接上，按【中文要点】讲完该页。

---

## 0. Before you start · 开始之前

| Item | English | 中文 |
|---|---|---|
| Language | English throughout; slides are English too. | 全程英文，幻灯片也是英文。 |
| Pace | ~105 words per minute. The English below is 1,695 words, i.e. about 16 minutes 15 seconds. | 约每分钟 105 词；英文共 1,695 词，约 16 分 15 秒。 |
| Logic | Every part answers one question on the roadmap (slide 2). Say the part name aloud when you start. | 每一部分回答路线图（第 2 页）上的一个问题；开口先报部分名称。 |
| Slide 1 | The R² hook: read both numbers slowly, then pause one beat before the question. | 第 1 页 R² 钩子：两个数字慢慢读，提问前停一拍。 |
| Who clicks | One person clicks for the whole talk (any member). | 全程由一个人翻页。 |
| Backup slides | 18–22 stay in the file. **Backup 1** for "did you cherry-pick?", **Backup 3** for "why drop a row?". | 备用页 18–22；被问"是否挑选结果"开 Backup 1，问"为什么删一行"开 Backup 3。 |
| Numbers | Never invent one. If unsure: "it is in our run records". | 绝不编数字；不确定就说"记录在仓库里"。 |
| **Wording discipline** | Say "every **model-performance** number is from validation". The data statistics on slides 4–5 use the full five-year history. | 要说"每一个**模型表现**数字都来自验证集"；第 4–5 页的数据统计用的是完整五年历史。 |

### The whole project in 30 seconds · 30 秒讲清整个项目

> **English.** We took five years of daily Apple and Bitcoin prices from two public sources. We turned them into ten backward-looking features, asked five classical models to predict the next day's price change, and tuned every model with the same budget. Then we compared each model with one free rule: tomorrow equals today. No model beat that rule by more than about half a percent, and every confidence interval included zero. We turned that result into a sixty-minute lesson on how to judge an AI score.

> **中文.** 我们从两个公开来源取了苹果和比特币五年的日线价格，构造十个"只看过去"的特征，让五种经典模型预测第二天的价格变化，并用相同预算调参。然后把每个模型和一条免费规则比较：明天等于今天。没有模型比它好过约 0.5%，所有置信区间都包含 0。我们把这个结果做成了一节 60 分钟的课：如何判断一个 AI 分数。

---

# INTRODUCTION · 开场 （Dong Yuankun）

## Slide 1 — Learning Machine Learning Through Financial Forecasting · 0:40
**Page / 页码:** 1/24 · **Speaker / 讲者:** Dong Yuankun

**【中文要点】** 用 R² 钩子开场：SVR 0.9556 对"照抄今天收盘价"0.9555，只差小数点后第四位；引出研究问题。

**English — say this:**
> Good morning. Here is a number. On Apple's validation data, a support vector regression model scores an R-squared of 0.9556. Impressive? Now take a rule that simply copies today's closing price. It scores 0.9555. The difference is in the fourth decimal place. So our question is: can five classical models really beat that simple rule on Apple and Bitcoin, with the same data, the same rules, and no look at the future?

**中文对照：**
> 大家早上好。先看一个数字：在苹果验证集上，支持向量回归模型的 R² 是 0.9556。很厉害吗？再看一条规则：直接照抄今天的收盘价，R² 是 0.9555。差别在小数点后第四位。所以我们的问题是：在相同数据、相同规则、看不到未来的条件下，五种经典模型真的能在苹果和比特币上打败这条简单规则吗？

**→ Transition:** "Here is the pipeline." · **过渡：** "这就是整条流水线。"

---

## Slide 2 — Roadmap: One Pipeline, Five Stages · 0:50
**Page / 页码:** 2/24 · **Speaker / 讲者:** Dong Yuankun

**【中文要点】** 五个阶段各回答一个问题；任务、对照基准、结论先说清；每人讲一个阶段。

**English — say this:**
> We answer it as one pipeline with five stages, and each stage answers one question. Which data, and why? What may the model see? Which models, tuned how fairly? Measured how, and how certain? And how does it become a lesson?
>
> The task is to forecast the next daily close; the yardstick is naive persistence, tomorrow equals today. The result in one line: all twenty model runs land within one percent of that yardstick, and none is reliably better. All five of us will present.

**中文对照：**
> 我们把它当作一条五个阶段的流水线来回答，每个阶段回答一个问题：用什么数据、为什么？模型可以看到什么？用哪些模型、调参是否公平？怎么衡量、有多确定？怎样变成一节课？
>
> 任务是预测下一个交易日的收盘价；对照基准是朴素持续性：明天等于今天。一句话结论：全部 20 次模型运行都落在这条基准的 1% 以内，没有一个可靠地更好。我们五个人都会上台讲。

**→ Transition:** "Part one: the data." · **过渡：** "第一部分：数据。"

---

# PART 1 — DATA SELECTION · 第一部分：数据选择 （Dong Yuankun）

## Slide 3 — What We Used, and Exactly Where It Came From · 0:50
**Page / 页码:** 3/24 · **Speaker / 讲者:** Dong Yuankun

**【中文要点】** 两个数据集、两个公开来源，链接就是代码实际调用的地址；下载一次、原样保存、SHA-256 指纹每次运行都校验。

**English — say this:**
> Part one: data selection. Apple comes from the StockAnalysis public history API; Bitcoin from Binance's public API, as daily BTC-to-USDT candles. The two links are exactly the addresses our code calls.
>
> Each daily bar has open, high, low, close and volume; Apple also has an adjusted close. The window is five years from October 2021: 1,255 trading days for Apple, 1,828 days for Bitcoin.
>
> Each file was downloaded once and saved unchanged, with a SHA-256 fingerprint that every run re-checks. So every number traces back to the same bytes.

**中文对照：**
> 第一部分：数据选择。苹果数据来自 StockAnalysis 的公开历史接口；比特币来自 Binance 的公开接口，是 BTC 对 USDT 的日线。这两个链接就是我们代码实际调用的地址。
>
> 每根日线有开盘、最高、最低、收盘和成交量；苹果还多一个复权收盘价。窗口是从 2021 年 10 月起的五年：苹果 1,255 个交易日，比特币 1,828 天。
>
> 每个文件只下载一次、原样保存，并带有 SHA-256 指纹，每次运行都重新校验。所以每个数字都能追溯到同一份字节。

**→ Transition:** "Why these two?" · **过渡：** "为什么选这两个？"

---

## Slide 4 — Why These Two: Two Markets With Different Characteristics · 1:05
**Page / 页码:** 4/24 · **Speaker / 讲者:** Dong Yuankun

**【中文要点】** 两个市场结构不同：交易日历、波动率、价格量级、公司行为都不一样；同一协议在两种结构上都成立，才是关于方法的结论；量级不同，所以只比较无单位指标。

**English — say this:**
> We chose them because they differ in every way that matters. Apple trades in exchange sessions, so its history has 261 weekend and holiday gaps; Bitcoin trades every day. Bitcoin is more volatile: daily returns vary by 2.66 percent, against 1.76 for Apple, and the chart shows both moving through calm and wild periods. Their price scales differ by over a hundred times. And Apple pays dividends, so its adjusted close differs from the raw close on 95.5 percent of days.
>
> One protocol on two such structures is a robustness check: a result that holds on both is about the method, not one market. And because the scales differ, we compare the assets only with unit-free scores.

**中文对照：**
> 选它们，是因为它们在所有重要方面都不同。苹果按交易所时段交易，所以历史里有 261 处周末和节假日间隔；比特币每天都交易。比特币波动更大：日收益率标准差 2.66%，苹果 1.76%；图上可以看到两个市场都经历了平静期和剧烈期。两者价格量级相差一百倍以上。苹果还会派息，所以复权收盘价有 95.5% 的天数与原始收盘价不同。
>
> 同一套协议跑在两种这样的结构上，是一次稳健性检验：两边都成立的结论，才是关于方法、而不是关于某个市场的。又因为量级不同，资产之间只用无单位的分数比较。

**→ Transition:** "Not every row is usable." · **过渡：** "但并不是每一行都能用。"

---

## Slide 5 — Selection Conditions: From Raw Bars to Modelling Rows · 1:10
**Page / 页码:** 5/24 · **Speaker / 讲者:** Dong Yuankun

**【中文要点】** 四个筛选条件：窗口在 2020 年拆股之后；用原始收盘价；六项质量检查，失败就停而不修补（两份数据都 PASS）；去掉前 30 行和最后 1 行。得到 1,224 / 1,797 行，再按时间 60/20/20 切分。

**English — say this:**
> Every row must meet four conditions. One: the window starts after Apple's 2020 stock split, so raw prices have no split jumps. Two: we use the raw close, because adjusted prices are revised later. Three: a quality gate checks for duplicate dates, missing values, non-positive prices, a high below the low, a close outside the day's range, and negative volume. Any failure stops the pipeline: we reject bad data rather than quietly repair it. Both datasets passed with no row flagged. Four: we drop the first thirty rows, where rolling windows are not yet full, and the last row, which has no next close.
>
> That leaves 1,224 rows for Apple and 1,797 for Bitcoin, split by time sixty, twenty, twenty.

**中文对照：**
> 每一行都必须满足四个条件。一：窗口从苹果 2020 年拆股之后开始，原始价格没有拆股跳变。二：用原始收盘价，因为复权价格会事后修订。三：质量闸门检查重复日期、缺失值、非正价格、最高价低于最低价、收盘价超出当日区间、负成交量。任何一项不通过，流水线就停下：坏数据直接拒绝，而不是悄悄修补。两份数据都通过了，没有任何一行被标记。四：去掉前 30 行（滚动窗口还没填满）和最后 1 行（没有下一个收盘价）。
>
> 最后得到苹果 1,224 行、比特币 1,797 行，按时间 60/20/20 切分。

**→ Transition (handover Dong Yuankun → Zhang Yancheng):** "With clean rows, part two turns them into model inputs." · **过渡：** "行数据干净了，第二部分把它们变成模型输入。"

---

# PART 2 — PROCESSING AND FEATURE ENGINEERING · 第二部分：数据处理与特征工程 （Zhang Yancheng）

## Slide 6 — Problems in the Raw Data, and How We Handled Each · 1:05
**Page / 页码:** 6/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 原始数据的六个问题，每个都对应一个处理方法：价格水平漂移→比率特征；复权会修订→原始收盘价；两种日历→各用自己的"下一根"；窗口要历史→删前 30 行；尺度不同→P2 只在训练行上标准化；时间顺序→按时间切分并删边界行。

**English — say this:**
> Part two: processing and feature engineering. Raw prices raise six problems, and each maps to one decision. Price levels drift and differ by asset, so a model fitted on old levels cannot extrapolate: we use returns and ratios. Adjusted prices carry future revisions: the target is the raw close. The calendars differ: each asset uses the next bar on its own calendar, and rows are never aligned across assets. Rolling windows need history, and back-filling would leak: we drop the first thirty rows. Features sit on different scales, which biases distance- and penalty-based models: setting P2 standardises them, fitted on training rows only. And time order rules out shuffling: we split by date.

**中文对照：**
> 第二部分：数据处理与特征工程。原始价格带来六个问题，每个对应一个决定。价格水平会漂移、各资产不同，在旧水平上拟合的模型无法外推：所以用收益率和比率。复权价格带有未来的修订：目标用原始收盘价。日历不同：每个资产用自己日历上的下一根 K 线，绝不跨资产按行对齐。滚动窗口需要历史，向后填充会泄漏：删掉前 30 行。特征尺度不同，会让基于距离和惩罚的模型产生偏向：P2 设置做标准化，只在训练行上拟合。时间顺序不允许打乱：按日期切分。

**→ Transition:** "Here are the features that come out." · **过渡：** "得到的特征是这些。"

---

## Slide 7 — Ten Features, Built Only From Information Available at the Close · 0:50
**Page / 页码:** 7/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 十个特征、六组，全部是只看过去的比率，没有价格水平；"不看未来"用测试保证；五个模型用完全相同的十个输入。

**English — say this:**
> The result is ten features in six groups: returns over one, five and twenty days; the gap from the five- and twenty-day averages; volatility over ten and thirty days; today's high-to-low range; volume against its five-day average; and the weekday.
>
> Every window looks backwards and ends at today's close, and no feature is a price level. We test this: we append absurd future prices, rebuild, and earlier rows must not change. All five models get exactly these ten inputs, so the comparison is about the models, not the information.

**中文对照：**
> 结果是六组共十个特征：1、5、20 日收益率；相对 5 日和 20 日均线的偏离；10 日和 30 日波动率；当天高低幅度；成交量相对 5 日均量；以及星期几。
>
> 每个窗口都往回看、截止于今天收盘，没有任何特征是价格水平。这一点经过测试：在末尾追加离谱的未来价格、重新构造，之前的行不能变化。五个模型用的恰好是这十个输入，所以比较的是模型，而不是信息。

**→ Transition:** "No price level means one more design step." · **过渡：** "没有价格水平，就还需要一步设计。"

---

## Slide 8 — Engineering the Target: Predict the Change, Then Add It Back · 0:55
**Page / 页码:** 8/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 比率特征没有价格水平，所以让模型预测变化量，再加回今天的收盘价；误差仍按价格衡量；持续性就是"变化为 0"；这是迭代出来的设计。

**English — say this:**
> Because no feature is a price level, the model learns the change, and today's close supplies the level: forecast equals today's close plus the predicted change. Errors are still measured on the price, and persistence is simply a predicted change of zero.
>
> One real validation day, the twenty-first of November 2024: close 228.52, predicted change plus ten cents, forecast 228.62. The next close was 229.87, so the model missed by 1.25 and persistence by 1.35.
>
> We found this by iteration: predicting the level directly made every model collapse toward the training average.

**中文对照：**
> 因为没有特征是价格水平，所以让模型学习变化量，价格水平由今天的收盘价提供：预测 = 今日收盘 + 预测变化。误差仍然按价格衡量，持续性就是"预测变化为 0"。
>
> 验证集里真实的一天，2024 年 11 月 21 日：收盘 228.52，预测上涨 0.10，预测价 228.62。第二天实际 229.87，模型误差 1.25，持续性误差 1.35。
>
> 这是迭代出来的：直接预测价格水平时，所有模型都塌向了训练期的平均值。

**→ Transition:** "The last processing step is the split." · **过渡：** "处理的最后一步是切分。"

---

## Slide 9 — Chronological Split, and Proof That the Pipeline Cannot Peek · 1:00
**Page / 页码:** 9/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 按时间 60/20/20 切分，每个边界删一行（标签是下一天收盘价，否则训练的答案落进验证块；审计量化为 0.408）；故意注入 6 种泄漏错误，全部被抓到；83 项测试通过。

**English — say this:**
> We split by date, sixty, twenty, twenty, and the final block stays sealed. At each boundary we drop one row: the label is the next close, so otherwise the last training answer would be the first validation price. An independent audit showed that, without this purge, changing one test-period price moved the headline metric by 0.408.
>
> Then we attack the pipeline on purpose: a script injects six known leakage mistakes, one at a time, and the tests must fail every time. All six are caught, and eighty-three automated tests pass. Every model-performance number from here on comes from the validation block.

**中文对照：**
> 按日期 60/20/20 切分，最后一块封存。每个边界删一行：标签是下一天收盘价，不删的话，最后一个训练样本的答案就是验证集的第一个价格。独立审计显示，不删行时，改动一个测试期价格就让头条指标移动 0.408。
>
> 然后我们主动攻击流水线：脚本逐个注入六种已知的泄漏错误，测试每次都必须失败。六种全部被抓到，83 项自动测试全部通过。接下来每一个模型表现数字都来自验证块。

**→ Transition:** "Clean inputs, so part three: the models." · **过渡：** "输入干净了，第三部分：模型。"

---

# PART 3 — MODELS AND FINE-TUNING · 第三部分：模型与调参 （Zhang Yancheng）

## Slide 10 — Five Models Plus a Baseline: Why Each One Is There · 1:10
**Page / 页码:** 10/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 一个基线加五个模型，代表三种机制（线性权重、核相似度、树切分）；每个模型说清"怎么预测、传统优势、在本研究里的角色"；不用深度学习。

**English — say this:**
> Part three: models and fine-tuning. Beside the yardstick we use five models covering three ways of learning. Two linear ones: a linear baseline with a small penalty, the simplest learned model, and ridge, which searches a wide penalty range to test whether regularisation helps. Support vector regression with an RBF kernel predicts from similarity to training examples; it captures non-linear patterns but depends on distances, so it is our scale-sensitive case. Two tree ensembles: a random forest averages many independent trees, is robust and needs little tuning, and is our scale-invariant control. Gradient boosting adds trees one by one to fix the remaining error, and is often strongest on tabular data.
>
> No deep learning: the handout discourages it, and classical models stay interpretable.

**中文对照：**
> 第三部分：模型与调参。除了基准，我们用五个模型覆盖三种学习方式。两个线性模型：带小惩罚的线性基线，是最简单的可学习模型；岭回归在很宽的惩罚范围里搜索，检验正则化是否有用。RBF 核支持向量回归根据与训练样本的相似度预测，能捕捉非线性，但依赖距离，所以是"对尺度敏感"的案例。两种树集成：随机森林平均许多独立的树，稳健、几乎不用调参，是"对尺度不变"的对照；梯度提升一棵接一棵地加树来修正剩余误差，在表格数据上通常最强。
>
> 不用深度学习：讲义不鼓励，而经典模型更容易解释。

**→ Transition:** "Comparing them is only fair if they are tuned the same way." · **过渡：** "只有用同样方式调参，比较才公平。"

---

## Slide 11 — Fine-Tuning: The Same Search and Budget for Every Model · 1:05
**Page / 页码:** 11/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 训练块内部五折扩展窗口交叉验证；随机搜索 10 次、每格 ≤90 秒、同一随机种子；目标是 MAE；验证块不参与调参；网格事先冻结。调参器几乎总是选最保守的设置。

**English — say this:**
> Every model is tuned the same way. Inside the training block only, five expanding-window folds: fit on the earlier part, score on the next slice. A random search tries ten settings per model, within ninety seconds and with the same seed, and keeps the one with the lowest average error. The validation block is never used, and the grids were fixed in our protocol before any result.
>
> The table shows each grid and the choice. Notice the pattern: the choices are mostly the most cautious ones. Ridge takes the strongest penalty, boosting the smallest learning rate, SVR on Apple the smallest C. The tuner is telling us the safest forecast stays close to "no change".

**中文对照：**
> 每个模型的调参方式完全相同。只在训练块内部做五折扩展窗口：用前面一段拟合、在下一小段打分。随机搜索每个模型试 10 组参数，限时 90 秒、同一个随机种子，保留平均误差最低的那组。验证块从不使用，网格在看到任何结果前就写进了协议。
>
> 表里是每个网格和选中的值。注意规律：选中的大多是最保守的设置。岭回归选最强的惩罚，梯度提升选最小的学习率，苹果上的 SVR 选最小的 C。调参器在告诉我们：最安全的预测就是贴近"不变"。

**→ Transition:** "We also explored more than hyperparameters." · **过渡：** "我们探索的不止超参数。"

---

## Slide 12 — What We Explored Beyond Hyperparameters · 0:55
**Page / 页码:** 12/24 · **Speaker / 讲者:** Zhang Yancheng

**【中文要点】** 另外三个探索方向：目标表示（价格水平→变化量）、预处理 P0 vs P2（20 次运行）、缩放的影响（树完全不变，SVR 和岭回归会变）；以及网格边缘的观察。

**English — say this:**
> Beyond hyperparameters, we explored three design choices. First, the target: from price level to change, as you saw. Second, preprocessing: every model ran on raw features, P0, and standardised features, P2, giving twenty runs. A missing-value setting was skipped, because there are no missing values.
>
> Third, what scaling changed, in the chart. Both tree ensembles gave identical predictions, exactly as split thresholds predict. SVR and ridge moved, because distances and penalties depend on scale; the Apple linear baseline's error rose by 0.74 percent. And ridge chose the edge of its grid, so wider grids are a clear next step.

**中文对照：**
> 除了超参数，我们还探索了三个设计选择。第一，目标：从价格水平改成变化量，前面讲过。第二，预处理：每个模型都在原始特征 P0 和标准化特征 P2 上各跑一次，共 20 次运行。缺失值填补的设置没有跑，因为数据没有缺失值。
>
> 第三，缩放改变了什么，见右图。两种树集成的预测完全相同，正如阈值切分所预期。SVR 和岭回归有变化，因为距离和惩罚依赖尺度；苹果线性基线的误差上升了 0.74%。另外，岭回归选中了网格边缘，所以放宽网格是明确的下一步。

**→ Transition (handover Zhang Yancheng → Zhang Haoyu):** "So how well did they do? Part four." · **过渡：** "那它们表现如何？第四部分。"

---

# PART 4 — EVALUATION · 第四部分：评估 （Zhang Haoyu）

## Slide 13 — Four Metrics, Each With a Job · 1:00
**Page / 页码:** 13/24 · **Speaker / 讲者:** Zhang Haoyu

**【中文要点】** 四个指标各有分工：MAE 典型误差、RMSE 惩罚大错、R² 解释的方差占比、skill 相对基准的提升；R² 对任何贴着昨天价格的预测都很高，所以不用它排名；跨资产只用 skill。

**English — say this:**
> Part four: evaluation. Four metrics, each with a job. Mean absolute error is the typical miss in dollars. Root mean squared error punishes large misses. R-squared is the share of price variance explained. Skill is one minus the model's error over persistence's error: zero means no better than the rule, and it has no units.
>
> For the best Apple model against persistence: MAE 2.89 against 2.91, RMSE 4.36 for both, R-squared 0.9556 against 0.9555. That last pair is the trap: any forecast that follows yesterday's price scores a high R-squared, so it never ranks models. Skill is our main measure, and the only one we use across assets.

**中文对照：**
> 第四部分：评估。四个指标，各有分工。平均绝对误差是以美元计的典型误差；均方根误差惩罚大错；R² 是被解释的价格方差占比；skill 是 1 减去"模型误差除以持续性误差"：0 表示和规则一样，而且没有单位。
>
> 苹果最好的模型对比持续性：MAE 2.89 对 2.91，RMSE 都是 4.36，R² 0.9556 对 0.9555。最后这一对就是陷阱：任何跟着昨天价格走的预测 R² 都很高，所以它从不用来排名。skill 是主要指标，也是跨资产唯一使用的指标。

**→ Transition:** "Here is skill for every run." · **过渡：** "这是每次运行的 skill。"

---

## Slide 14 — Results: All 20 Runs Land Within 1% of the Baseline · 0:55
**Page / 页码:** 14/24 · **Speaker / 讲者:** Zhang Haoyu

**【中文要点】** 最好：苹果 SVR(P2) +0.52%（约少 1.5 美分误差），比特币线性基线(P0) +0.26%；20 次全部在 −0.78% 到 +0.52% 之间，5 次低于 0；完整 20 格见 Backup 1。

**English — say this:**
> Here is skill for every model on validation data. The best Apple run is SVR with standardised features, at plus 0.52 percent: about one and a half cents less error per forecast. The best Bitcoin run is the linear baseline on raw features, at plus 0.26.
>
> Across all twenty runs, skill sits between minus 0.78 and plus 0.52 percent, and five runs are worse than the rule. That narrow band is the finding: on daily prices, a simple rule is a very strong opponent. Every run is shown; the full grid is in Backup 1.

**中文对照：**
> 这是每个模型在验证集上的 skill。苹果最好的是标准化特征下的 SVR，+0.52%：每次预测大约少 1.5 美分误差。比特币最好的是原始特征下的线性基线，+0.26%。
>
> 全部 20 次运行的 skill 在 −0.78% 到 +0.52% 之间，有 5 次比规则更差。这个很窄的范围就是发现：在日度价格上，简单规则是非常强的对手。每一次运行都展示了，完整表格在 Backup 1。

**→ Transition:** "But are those small leads real?" · **过渡：** "但这些小小的领先是真的吗？"

---

## Slide 15 — How Certain? Every Interval Includes Zero · 0:55
**Page / 页码:** 15/24 · **Speaker / 讲者:** Zhang Haoyu

**【中文要点】** 配对移动区块 Bootstrap（块长 10 天、1,000 次、95%）；20 个区间全部包含 0：与强基线持平；原因：相邻日收益率几乎不相关（苹果 +0.021，比特币 −0.026）。

**English — say this:**
> Are those small leads real? We pair each model's errors with the rule's on the same dates, resample blocks of ten consecutive days a thousand times, and take a ninety-five percent interval; blocks keep the dependence between neighbouring days.
>
> Each row is one run. All twenty intervals contain zero, including the best Apple run. So the precise reading is parity with a strong baseline, not a winner.
>
> Why so hard to beat? The correlation between one day's return and the next is plus 0.021 for Apple and minus 0.026 for Bitcoin, essentially zero. Yesterday's move says almost nothing about today's.

**中文对照：**
> 这些小小的领先是真的吗？我们把每个模型的误差和规则的误差按相同日期配对，每次重采样连续十天的块，重复一千次，取 95% 区间；分块保留了相邻日期之间的相关性。
>
> 每一行是一次运行。20 个区间全部包含 0，包括苹果最好的那次。所以准确的结论是：与强基线持平，而不是有赢家。
>
> 为什么这么难打败？今天和明天收益率的相关性，苹果 +0.021，比特币 −0.026，基本为零。昨天的涨跌几乎说明不了今天。

**→ Transition (handover Zhang Haoyu → Lau Pak Hei):** "That result is exactly what we teach. Part five." · **过渡：** "这个结果正是我们要教的。第五部分。"

---

# PART 5 — TEACHING DESIGN · 第五部分：教学设计 （Lau Pak Hei: slide 16 · Lui Shing Lam: slide 17）

## Slide 16 — Teaching Design: The Pipeline Becomes a 60-Minute Lesson · 1:00
**Page / 页码:** 16/24 · **Speaker / 讲者:** Lau Pak Hei

**【中文要点】** 项目变成 60 分钟的课；五个任务各来自项目的一个部分；先看简单规则再看模型；有练习本和带答案的教师指南。

**English — say this:**
> Part five: teaching design. We turned our project into a sixty-minute lesson. It is for students who are new to machine learning.
>
> The lesson has five tasks. Each task comes from one part of our project. Task one: compare training error with error on new data. Task two: find the leak in a short piece of code. Task three: read our skill table. Task four: say which models care about scaling. Task five: explain why low error is not profit.
>
> Students see the simple rule first, and the models after. Teachers get a Colab workbook and a guide with answers.

**中文对照：**
> 第五部分：教学设计。我们把项目做成了一节 60 分钟的课，对象是刚接触机器学习的学生。
>
> 这节课有五个任务，每个任务来自项目的一个部分。任务一：比较训练误差和新数据上的误差。任务二：在一小段代码里找出泄漏。任务三：读我们的 skill 表。任务四：说出哪些模型在意缩放。任务五：解释为什么误差低不等于赚钱。
>
> 学生先看简单规则，再看模型。老师拿到一个 Colab 练习本和一份带答案的指南。

**→ Transition (handover Lau Pak Hei → Lui Shing Lam):** "Now the summary." · **过渡：** "下面是总结。"

---

## Slide 17 — Summary: What Each Stage Delivered · 0:50
**Page / 页码:** 17/24 · **Speaker / 讲者:** Lui Shing Lam

**【中文要点】** 按五个部分各说一句成果；下一步；不是投资建议；谢谢、请提问。

**English — say this:**
> To sum up. Data: two different markets, from public sources we can trace. Processing: ten features that only look backwards. Models: five models, tuned in the same way. Evaluation: all twenty runs are within one percent of the simple rule. Teaching: a sixty-minute lesson with five tasks.
>
> Next, we will test on the sealed data once, and try the lesson with a real class. This is not investment advice. Thank you. We are happy to take questions.

**中文对照：**
> 总结一下。数据：两个不同的市场，来源公开、可追溯。处理：十个只往回看的特征。模型：五个模型，用同样的方式调参。评估：20 次运行都在简单规则的 1% 以内。教学：一节 60 分钟、五个任务的课。
>
> 下一步：在封存的数据上测试一次，并在真实班级里试这节课。这不构成投资建议。谢谢大家，欢迎提问。
---

# Q&A — bilingual cheat sheet · 问答中英对照

Questions are answered by Dong Yuankun, Zhang Yancheng or Zhang Haoyu. Lau Pak Hei and Lui Shing Lam do not take Q&A; if a question is aimed at them, Zhang Yancheng answers. 问答由 Dong Yuankun、Zhang Yancheng、Zhang Haoyu 回答；Lau Pak Hei 和 Lui Shing Lam 不接问答，若有人点名问他们，由 Zhang Yancheng 回答。

| Question | Answers | English answer | 中文 |
|---|---|---|---|
| Where exactly is the data from? | Dong Yuankun | The two URLs on slide 3 are the exact calls in `src/int4096/data/providers.py`; the saved files and their SHA-256 hashes are in `data/raw/`. | 第 3 页两个链接就是代码实际调用的地址；保存的文件和哈希在 `data/raw/`。 |
| Why AAPL and BTC? | Dong Yuankun | Different calendars, volatility, scale and corporate actions: one protocol on two structures is a robustness check. | 日历、波动率、量级、公司行为都不同：同一协议跑两种结构，是稳健性检验。 |
| Is Binance BTC a global price? | Dong Yuankun | No. It is one exchange, quoted in USDT, which is not exactly USD. We say "BTC/USDT on Binance". | 不是。它是单一交易所、以 USDT 计价，USDT 不完全等于美元。 |
| Why not adjusted close? | Dong Yuankun | Adjustments are revised after the fact, so they carry future information into the past. Our window has no split, so raw close is continuous. | 复权会事后修订，会把未来信息带进过去；窗口内没有拆股，原始收盘价是连续的。 |
| Why classical ML, not deep learning? | Zhang Yancheng | The handout discourages it, and classical families keep the comparison interpretable. | 讲义不鼓励；经典模型让比较更可解释。 |
| Did you leak future data? | Zhang Yancheng | Chronological split, a purged boundary row, a sealed test block, and 6 of 6 injected defects caught → Backup 3. | 按时间切分、边界删行、封存测试集、6/6 注入缺陷被抓到 → Backup 3。 |
| Did you cherry-pick P2? | Zhang Haoyu | No. Backup 1 shows all 20 runs. The best Bitcoin result overall is the unscaled linear baseline at +0.26%. | 没有。Backup 1 有全部 20 次；比特币整体最好的是未缩放线性基线 +0.26%。 |
| Was tuning fair? | Zhang Yancheng | Same folds, same 10 trials, same 90 s, same seed, grids frozen beforehand → Backup 2. | 同样的折、10 次试验、90 秒、同一种子、网格事先冻结 → Backup 2。 |
| Why do chosen values sit at grid edges? | Zhang Yancheng | The tuner prefers the most cautious settings because there is little signal to fit. Widening the grids is a next step. | 信号太少，调参器偏好最保守的设置；放宽网格是下一步。 |
| Is +0.52% meaningful? | Zhang Haoyu | Not by our own test: all 20 bootstrap intervals include zero. | 按我们自己的检验不是：20 个区间全包含 0。 |
| Why only P0 and P2? | Zhang Yancheng | They isolate the effect of scaling. P1 would duplicate P0 because there are no missing values; P3 and P4 are next. | 它们隔离出缩放的影响；P1 因无缺失值会与 P0 重复；P3、P4 是下一步。 |
| Can this make money? | Zhang Haoyu | No. Error metrics ignore costs and risk; we make no profitability claim. | 不能。误差指标不含成本和风险；我们不声称盈利。 |
| Did the lesson improve learning? | Zhang Yancheng | The lesson is built and ready; measuring learning is what the classroom pilot is for. | 课程已完成；衡量学习效果正是课堂试点要做的。 |

# Backup slides · 备用页

| # | Slide | English one-liner | 中文 |
|---|---|---|---|
| 18 | Full 20-run matrix | "All twenty cells, nothing selected. The best Bitcoin result is the unscaled linear baseline at +0.26%." | 全部 20 格，没有挑选；比特币最好的是未缩放线性基线 +0.26%。 |
| 19 | Fairness and manifest audit | "Identical features, splits, dates and budget. Every run records commit, data hash and configuration." | 特征、切分、日期、预算都相同；每次运行记录提交、数据哈希、配置。 |
| 20 | Why one row is dropped | "Friday's label is Monday's price. The purge keeps every training answer out of the validation block." | 周五的标签是周一的价格；删行保证训练的答案不会落进验证块。 |
| 21 | Permutation importance | "One- and five-day returns, 30-day volatility and the 20-day average gap matter most. Magnitudes are tiny. Importance is not causation." | 1、5 日收益率、30 日波动率、20 日均线偏离最重要；量级很小；重要性不等于因果。 |
| 22 | Q&A cards | "Short, prepared answers to the most likely questions." | 最可能问题的简短答案。 |

# If you are running over · 超时怎么办

Check the clock at the **end of slide 5** (≈4:35) and the **end of slide 9**: it should read **≈8:25** (see `timing_plan.md`).

| Situation | Cut | 中文 |
|---|---|---|
| 8:55 or later after slide 9 | Slide 12: skip the grid-edge sentence and say only "trees unchanged, SVR and ridge move". (~20 s) | 第 12 页去掉网格边缘那句，只说"树不变，SVR 和岭回归会变"，省约 20 秒。 |
| 9:25 or later | Slide 10: name the five models and their roles in one breath, without the strengths. (~25 s) | 再把第 10 页压成"模型名 + 角色"，省约 25 秒。 |
| **Never cut** | Slide 13 (metrics), slide 14 (results), slide 15 (intervals). | **绝不能砍**第 13、14、15 页。 |

# Rehearsal checklist · 排练清单

- [ ] Every speaker has read their **English** blocks aloud twice. 每位讲者把英文大声读两遍。
- [ ] Every speaker can say their **【中文要点】** from memory. 不看稿能说出中文要点。
- [ ] Each part starts by naming the part ("Part three: models…"). 每部分开口先报部分名称。
- [ ] The four handovers (after slides 5, 12, 15, 16) are rehearsed. 四次交接要练。
- [ ] **Lau Pak Hei and Lui Shing Lam** each read their slide aloud to Zhang Yancheng at least three times before the talk, timed, with no ad-libbing. Lau Pak Hei 和 Lui Shing Lam 正式前至少各对 Zhang Yancheng 计时朗读三遍，不加词。
- [ ] Zhang Yancheng can deliver slides 16 and 17 from the 【中文要点】 as the fallback. Zhang Yancheng 能按【中文要点】讲完第 16、17 页作为后备。
- [ ] Two full timed run-throughs with a visible clock. 全流程计时彩排两次。
- [ ] Backup 1 and Backup 3 are ready in a second window. 准备好 Backup 1 和 3。
- [ ] Say "every **model-performance** number is from validation", not "every number". 说"每个模型表现数字"，不说"每个数字"。

> **Reminder · 提醒** The presentation is in English; Chinese here is a comprehension aid only. 演示用英文；中文仅供理解。
