# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `deliverables/presentation/INT4096_Presentation.pdf` — 26 pages (18 narrative + 6 backup + 2 references)
**Structure:** one part per pipeline stage: Data Selection → Processing & Features → Models & Tuning → Evaluation → Teaching Design
**Clock:** `timing_plan.md` · **Key messages:** `speaker_notes.md` · **Story:** `deliverables/presentation/planning/feature_extraction_story.md`
**Speech:** 17:10 planned (+0:40 for four handovers and slide changes, +2:00 Q&A = 19:50 inside the 20:00 slot)

> ### How to use this document · 使用方法
> **The presentation is delivered in English. Read only the English Version.**
> Each part has the full English text first, then the full Chinese translation. The Chinese helps you understand what you are saying, so you can speak from meaning instead of from memory. **Do not read the Chinese aloud.**
>
> **本演示用英文进行。上台只念 English Version。** 每一部分先是完整英文，再是完整中文翻译。中文帮助你先理解、再自然地讲出来，不要念出来。

> ### Who speaks · 分工
>
> | Slides | Part | Speaker | Time |
> |---|---|---|---:|
> | 1–5 | Introduction, Part 1 Data Selection | **Dong Yuankun** | 4:50 |
> | 6–12 | Part 2 Processing & Features, Part 3 Models & Tuning | **Zhang Yancheng** | 7:25 |
> | 13–15 | Part 4 Evaluation | **Zhang Haoyu** | 2:50 |
> | 16–17 | Part 5 Teaching Design and website | **Lau Pak Hei** | 1:20 |
> | 18 | Part 5 Summary and close | **Lui Shing Lam** | 0:45 |
>
> The speaker's name is also in each slide's footer. 每页幻灯片的页脚也写着讲者姓名。

### How the script is written · 写法

All five parts follow the same style, set by the Introduction and Part 1:

- **Short sentences, one idea each.** Say them one at a time, with a small pause between.
- **Signposts.** "First… Second… Finally…" so the audience always knows where they are.
- **Explain, then give an example.** Every technical idea comes with a plain-language meaning and one concrete case (Apple at 200 dollars; Bitcoin above 77,000; one real day in November 2024).
- **Bold = the sentence to stress.** Slow down on it.
- **The last sentence of each part hands over** to the next part or speaker.

全部五个部分都沿用开场和第一部分的风格：短句、每句一个意思；用"第一、第二、最后"做路标；先用白话解释概念，再举一个具体例子；粗体是要加重语气的句子；每部分最后一句负责交接。

---

## 0. Before you start · 开始之前

| Item | English | 中文 |
|---|---|---|
| Language | English throughout; slides are English too. | 全程英文，幻灯片也是英文。 |
| Pace | ~105 words per minute. The English below is 1,795 spoken words (stage directions and optional lines not counted), i.e. about 17 minutes. | 约每分钟 105 词；英文共 1,795 个要念的词（不含动作提示和备用内容），约 17 分钟。 |
| Logic | Every part answers one question on the roadmap (slide 2). Say the part name aloud when you start. | 每一部分回答路线图（第 2 页）上的一个问题；开口先报部分名称。 |
| Slide 1 | The R² hook: read both numbers slowly, then pause one beat. | 第 1 页 R² 钩子：两个数字慢慢读，然后停一拍。 |
| Who clicks | One person clicks for the whole talk (any member). | 全程由一个人翻页。 |
| Backup slides | 19–24 stay in the file. **Backup 1** for "did you cherry-pick?", **Backup 3** for "why drop a row?", **Backup 6** for "why not deep learning?". | 备用页 19–24；被问"是否挑选结果"开 Backup 1，问"为什么删一行"开 Backup 3，问"为什么不用深度学习"开 Backup 6。 |
| Numbers | Never invent one. If unsure: "it is in our run records". | 绝不编数字；不确定就说"记录在仓库里"。 |
| **Wording discipline** | Say "every **model-performance** number is from validation". The data statistics on slides 3–5 use the full five-year history. | 要说"每一个**模型表现**数字都来自验证集"；第 3–5 页的数据统计用的是完整五年历史。 |

### The whole project in 30 seconds · 30 秒讲清整个项目

> **English.** We took five years of daily Apple and Bitcoin prices from two public sources. We turned them into ten backward-looking features, asked five classical models to predict the next day's price change, and tuned every model with the same budget. Then we compared each model with one free rule: tomorrow equals today. No model beat that rule by more than about half a percent, and every confidence interval included zero. We turned that result into a sixty-minute lesson on how to judge an AI score.

> **中文.** 我们从两个公开来源取了苹果和比特币五年的日线价格，构造十个"只看过去"的特征，让五种经典模型预测第二天的价格变化，并用相同预算调参。然后把每个模型和一条免费规则比较：明天等于今天。没有模型比它好过约 0.5%，所有置信区间都包含 0。我们把这个结果做成了一节 60 分钟的课：如何判断一个 AI 分数。

---

# Introduction & Part 1: Data Selection · 开场与第一部分：数据选择

**Speaker / 讲者:** Dong Yuankun · **Slides / 页码:** 1–5 · **Target speaking time / 目标时长:** about 4:50

## English Version

### Slide 1 — Introduction

Good morning everyone. Today, our project is about learning machine learning through financial forecasting.

Our main question is: **Does a more complicated machine learning model necessarily produce better predictions?**

To investigate this, we selected five machine learning models to predict the next daily closing prices of Apple and Bitcoin.

However, before comparing these models, we introduced a very simple baseline called **Copy the Latest Close**, also known as *naive persistence*.

The idea is straightforward: tomorrow's closing price is predicted to be exactly the same as today's closing price.

For example, if Apple's closing price today is 200 dollars, our prediction for tomorrow is simply 200 dollars.

Surprisingly, this simple method performs extremely well.

As you can see on this slide, the R-squared score of our best model, Support Vector Regression, is 0.9556, while the baseline achieves 0.9555.

The difference is almost negligible.

This leads to the central idea of our project: **more complex models do not necessarily mean better predictions.**

### Slide 2 — Roadmap

Our presentation follows five stages.

First, Data Selection, where we explain which datasets we chose and why.

Second, Processing and Feature Engineering, where we prepare the data for machine learning.

Third, Models and Tuning, where we introduce our five models and explain how we optimise them.

Fourth, Evaluation, where we compare their performance against our baseline.

Finally, Teaching Design, where we explore how to turn our findings into a learning experience.

Now, let's begin with the first stage.

### Slide 3 — Data Selection

We selected two financial assets: Apple, representing the traditional stock market, and Bitcoin, representing the cryptocurrency market.

For Apple, we obtained historical daily data from the StockAnalysis public API. For Bitcoin, we used Binance's public REST API.

Both datasets cover approximately five years, starting from October 2021.

We collected 1,255 daily records for Apple and 1,828 for Bitcoin.

### Slide 4 — Why These Two?

The main reason for choosing these two assets is that they have different market characteristics.

First, Apple follows traditional stock market trading hours, while Bitcoin trades continuously, 24 hours a day, seven days a week.

Second, Bitcoin has higher daily return volatility in our dataset: 2.66%, compared with Apple's 1.76%.

Their price scales are also very different.

Finally, Apple has corporate actions such as dividends and stock splits, while Bitcoin does not have equivalent adjustments.

These differences allow us to investigate how the same machine learning models perform across two different financial markets.

### Slide 5 — Selection Conditions

Before modelling, we applied several data selection conditions.

We used a five-year observation window, selected raw closing prices as our prediction target, and checked for missing values, duplicate dates, invalid prices and other data quality issues.

We also removed the first 30 rows because they lacked sufficient historical information for our rolling features, and removed the last row because its next closing price was unavailable.

Finally, we divided the data chronologically into three parts: 60% for training, 20% for validation, and 20% for testing.

We also removed one row at each split boundary to prevent information leakage between datasets.

With our data selected and prepared, we can now move on to Processing and Feature Engineering.

## 中文版本

### 第 1 页 — 引入

大家早上好。今天我们小组要介绍的项目是通过金融预测来学习机器学习。

我们想探讨的核心问题是：**一个更加复杂的机器学习模型，是否一定能够做出更好的预测？**

为了研究这个问题，我们选择了五种机器学习模型，用来预测 Apple 和 Bitcoin 下一天的收盘价。

不过，在比较这些模型之前，我们先引入了一种非常简单的基准方法，叫作 **Copy the Latest Close**，也就是朴素持久性预测。

它的想法非常简单：我们假设明天的收盘价会和今天的收盘价完全一样。

例如，如果 Apple 今天的收盘价是 200 美元，那么我们对明天的预测就是 200 美元。

令人意外的是，这种简单的方法表现得相当好。

正如这一页所展示的，我们表现最好的模型——支持向量回归（SVR）——其 R-squared 分数是 0.9556，而这个简单基准方法的分数是 0.9555。

两者之间的差距几乎可以忽略不计。

这也引出了我们项目的核心观点：**模型更加复杂，并不一定意味着预测效果更好。**

### 第 2 页 — Roadmap

我们的展示分为五个阶段。

第一部分是数据选择，我们会介绍选择了哪些数据集，以及为什么选择它们。

第二部分是数据处理与特征工程，介绍我们如何为机器学习准备数据。

第三部分是模型与调参，我们会介绍五种模型，以及如何优化它们的参数。

第四部分是模型评估，我们会将模型的表现与基准方法进行比较。

最后是教学设计，我们会探讨如何把项目中的发现转化为一个学习体验。

接下来，我们先从第一部分开始。

### 第 3 页 — 数据选择

我们选择了两种金融资产：Apple 代表传统股票市场，而 Bitcoin 代表加密货币市场。

对于 Apple，我们从 StockAnalysis 的公开 API 获取历史日度数据；对于 Bitcoin，我们使用 Binance 的公开 REST API。

两个数据集都覆盖了大约五年的时间，从 2021 年 10 月开始。

我们收集了 1,255 条 Apple 日度记录，以及 1,828 条 Bitcoin 日度记录。

### 第 4 页 — 为什么选择这两个资产？

选择这两种资产的主要原因，是它们具有不同的市场特征。

首先，Apple 遵循传统股票市场的交易时间，而 Bitcoin 则是每周七天、每天 24 小时持续交易。

其次，在我们的数据中，Bitcoin 的日收益率波动率更高，为 2.66%，而 Apple 是 1.76%。

另外，两者的价格尺度也有很大差异。

最后，Apple 存在股息和股票拆分等公司行动，而 Bitcoin 没有同类的调整。

这些差异让我们能够研究：当同样的机器学习模型应用于两个不同的金融市场时，它们的表现会有什么不同。

### 第 5 页 — 数据筛选条件

在建立模型之前，我们对数据应用了几项筛选条件。

我们采用五年的观察窗口，选择原始收盘价作为预测目标，并检查数据中是否存在缺失值、重复日期、无效价格以及其他数据质量问题。

我们还删除了最前面的 30 行，因为这些数据缺少计算滚动特征所需的历史信息；同时删除最后一行，因为它没有对应的下一期收盘价。

最后，我们按照时间顺序将数据分为三个部分：60% 用于训练，20% 用于验证，20% 用于测试。

此外，我们在每个数据集划分的边界处额外删除一行，以避免不同数据集之间发生信息泄漏。

至此，我们完成了数据的选择和准备。接下来进入第二部分：数据处理与特征工程。

---

# Part 2: Processing & Features, Part 3: Models & Tuning · 第二部分：数据处理与特征工程，第三部分：模型与调参

**Speaker / 讲者:** Zhang Yancheng · **Slides / 页码:** 6–12 · **Target speaking time / 目标时长:** about 7:25

Lines in *[square brackets]* are stage directions: what to point at or do. Do not read them aloud. Point with your hand or the laser at the part of the slide named, then speak. Sentences in **bold** are the ones to slow down on.

方括号 *[ ]* 里是动作提示：指向哪里、做什么，不要念出来。先指到屏幕上对应的位置，再开口。**粗体**句子放慢、加重。

## English Version

### Slide 6 — Problems in the Raw Data

Thank you, Dong Yuankun. Now, Part Two: Processing and Feature Engineering.

Dong showed you our data. Looking at it closely, we found six problems that stop raw prices from going straight into a model. The table lists all six, with what we did.

**Because of time, I'll focus on the top three.**

*[Point to row 1.]*

First, prices drift to levels a model has never seen. So we use returns and ratios over **rolling windows**: each day compared with the five to thirty days before it.

*[Point to row 2.]*

Second, adjusted prices are revised later, so they leak the future. So our target is the raw close.

*[Point to row 3.]*

Third, Apple trades on weekdays, but Bitcoin trades every day. So we predict the next close on each asset's own calendar.

*[Sweep your hand over rows 4 to 6.]*

The rest are in the table. Now, the features.

**Rows 4–6, only if there is time or someone asks (not in the timed plan):**

> Fourth, rolling windows need history. The first thirty days do not have enough past data, so we drop them instead of filling them in.
>
> Fifth, the features have very different scales. So in one setting, P2, we standardise them, fitted on the training rows only.
>
> Sixth, time order matters. A shuffled split would train on the future, so we split by time and drop one row at each boundary.

### Slide 7 — From One Day to Ten Features

*[Point to the small table on the left.]*

On the left is one real day for Apple. On the right are its ten features.

*[Point to "Close today" and "Close yesterday" on the left, then to ret_1.]*

First, today's close against yesterday's close. That change, in percent, is the one-day return.

*[Point to ret_5 and ret_20.]*

Then the same against five days ago and twenty days ago: the short move and the longer move.

*[Point to ma_gap_5 and ma_gap_20.]*

Next, today's close against its five-day and twenty-day average: is the price above or below its recent trend?

*[Move down the remaining rows.]*

Then volatility, how jumpy the price was; range, how wide the day was; volume change; and the weekday. Notice that **every one is a comparison, not a price.**

*[Point to the note under the table.]*

Now the key point: **every feature uses only today and earlier days, never tomorrow.** We test it: we add fake future prices, and the earlier rows must not change.

### Slide 8 — Every Model Gets the Same Data

You may be wondering: **did every model get the same data?**

*[Trace the arrows across the top, left to right.]*

Follow the arrows. Daily prices become ten features, go through preprocessing, and enter one of the five models.

*[Point to the list on the right.]*

As the list on the right says, all five models get the same rows, features, target and splits. **Only the algorithm changes.**

*[Point to the third box, "P0 / P2".]*

There is just one switch. P0 leaves the features as they are. P2 standardises them, using the training years only.

*[Point to the table at the bottom left.]*

Why? Compare these rows. A daily return is a tiny number, but the weekday is about a hundred times larger. Without scaling, the weekday dominates SVR. Trees do not care.

*[Point to the last box of the diagram.]*

Finally, the forecast is today's close plus the predicted change. So the model only has to learn the change, not the whole price.

### Slide 9 — Splitting by Time

*[Trace the bar at the top from left to right.]*

Next, the split. Time runs from left to right: sixty percent to train, twenty to validate, twenty to test. The grey test block stays sealed.

*[Point to the two small red boxes, "Drop 1 row".]*

Notice these two small red boxes. At each boundary we drop one row. Why? Our label is tomorrow's close, so the last training answer would be the first validation price.

*[Point to the right column.]*

We also attacked our own pipeline with six common leakage mistakes, one at a time. **All six were caught.**

*[Point to the line at the bottom.]*

So please remember: **every model-performance number from here on comes from the validation block.**

### Slide 10 — Five Models and a Baseline

Part three: models and tuning.

*[Point to the first row.]*

The table has one row per model. The first row is our baseline. Below it are five models that learn in three different ways.

*[Point to the linear baseline and ridge rows.]*

First, two linear models. They give each feature a weight and add them up; ridge also keeps the weights small.

*[Point to the SVR row.]*

Second, SVR. It predicts from how similar a day is to past days. It measures distance, so **it is sensitive to scale. Keep that in mind.**

*[Point to the last two rows.]*

Third, two tree ensembles. A random forest averages many independent trees. Gradient boosting adds trees one by one, each fixing the errors left so far.

*[Point to the note at the bottom.]*

We also tried two neural networks, an MLP and an LSTM. Neither did better; that is backup six.

### Slide 11 — Fair Tuning

A comparison is only fair if every model is tuned the same way.

*[Point to the fold diagram on the left.]*

Look at the diagram. Each bar is one fold, inside the training years only. We fit on the blue part and score on the green slice. Then the window grows, five times.

*[Point to the bullet points.]*

Every model gets the same deal: ten random settings, the same time limit, the same seed. **The validation block is never touched.**

*[Point to the "Chosen" columns of the table.]*

Now look at what was chosen. Ridge took alpha 1000, the strongest penalty. Boosting took the smallest learning rate. These are the most cautious settings. **The tuner is telling us that the safest forecast stays close to "no change".**

### Slide 12 — What Else We Explored

*[Point to points 1 and 2 on the left.]*

We also changed the target from price to price change, and we ran every model on raw and on standardised features: twenty runs.

*[Point to the chart.]*

The chart shows what scaling changed. Each bar is one model on one asset. Red means the error went up; green means it went down.

*[Point to the empty rows in the middle.]*

Look at the middle: **the tree models have no bar at all.** Their predictions were exactly the same, just as we expected. The linear models and SVR moved, because they depend on scale.

So, how well did all these models do? Zhang Haoyu will show you.

## 中文版本

### 第 6 页 — 原始数据的问题

谢谢 Dong Yuankun。接下来是第二部分：数据处理与特征工程。

Dong 刚才介绍了我们的数据。仔细看时，我们发现了六个问题，让原始价格不能直接放进模型。表里列出了全部六个，以及我们的做法。

**由于时间关系，我重点讲前三个。**

*[指第 1 行。]*

第一，价格会漂移到模型从没见过的水平。所以我们在**滚动窗口**上计算收益率和比率：把每一天和它之前 5 到 30 天作比较。

*[指第 2 行。]*

第二，复权价会事后修订，等于泄露了未来。所以预测目标用原始收盘价。

*[指第 3 行。]*

第三，苹果只在工作日交易，比特币每天都交易。所以我们按各自资产的日历预测下一次收盘。

*[手扫过第 4–6 行。]*

其余的都在表里。接下来看特征。

**第 4–6 行：仅在有时间或被问到时讲（不计入计时）：**

> 第四，滚动窗口需要历史数据。前 30 天的历史不够，所以直接删掉，而不是填补。
>
> 第五，各个特征的尺度差别很大。所以在 P2 设置下我们把它们标准化，只用训练行来拟合。
>
> 第六，时间顺序很重要。打乱切分会用未来训练，所以我们按时间切分，并在每个边界删一行。

### 第 7 页 — 从一天的数据到十个特征

*[指向左边的小表。]*

左边是苹果真实的一天，右边是它的十个特征。

*[指向左边的"今天收盘"和"昨天收盘"，再指 ret_1。]*

第一，今天收盘对比昨天收盘，变化的百分比就是一日收益率。

*[指向 ret_5 和 ret_20。]*

然后同样对比 5 天前和 20 天前：短期变化和较长期变化。

*[指向 ma_gap_5 和 ma_gap_20。]*

接着，今天收盘对比 5 日和 20 日均价：价格在近期趋势的上方还是下方？

*[往下指过其余几行。]*

然后是波动率（价格跳得多厉害）、幅度（当天波动多宽）、成交量变化，以及星期几。请注意，**每一个都是比较，而不是价格。**

*[指向表格下方的说明。]*

关键点来了：**每个特征只用今天和以前的数据，绝不用明天。** 我们用测试来保证：加入假的未来价格，之前的行必须完全不变。

### 第 8 页 — 每个模型用的数据都一样

大家可能会问：**每个模型用的数据都一样吗？**

*[从左到右沿着上方的箭头指过去。]*

跟着箭头看：每日价格变成十个特征，经过预处理，进入五个模型中的一个。

*[指向右边的列表。]*

正如右边列表写的，五个模型用相同的行、特征、目标和切分。**唯一变化的是算法。**

*[指向第三个方框 "P0 / P2"。]*

只有一个开关。P0 保持特征原样；P2 把特征标准化，只用训练年份的数据。

*[指向左下方的表格。]*

为什么？比较这几行。日收益率是一个很小的数，而星期几大了大约一百倍。不做缩放的话，星期几会主导 SVR。树不受影响。

*[指向流程图最后一个方框。]*

最后，预测值等于今天的收盘价加上预测的变化量。所以模型只需要学变化，而不是整个价格。

### 第 9 页 — 按时间切分

*[从左到右沿着上方的条形指过去。]*

接下来是切分。时间从左往右：60% 训练、20% 验证、20% 测试。灰色的测试块一直封存。

*[指向两个红色小方框 "Drop 1 row"。]*

注意这两个红色小方框。每个边界我们删掉一行。为什么？因为标签是明天的收盘价，最后一个训练样本的答案，恰好就是验证集的第一个价格。

*[指向右边一栏。]*

我们还用六种常见的泄漏错误主动攻击自己的流水线，一次注入一种。**六种全部被抓到。**

*[指向底部那一行字。]*

所以请记住：**从这里开始，每一个模型表现数字都来自验证块。**

### 第 10 页 — 五个模型和一个基准

第三部分：模型与调参。

*[指向第一行。]*

这张表每一行是一个模型。第一行是基准，下面是五个模型，用三种不同的方式学习。

*[指向线性基线和岭回归两行。]*

第一，两个线性模型。它们给每个特征一个权重再加起来；岭回归还会让权重保持很小。

*[指向 SVR 那一行。]*

第二，SVR。它根据某一天和过去的日子有多相似来预测。它衡量距离，所以**对尺度敏感。请记住这一点。**

*[指向最后两行。]*

第三，两种树集成。随机森林把许多独立的树取平均；梯度提升一棵接一棵地加树，每棵都修正前面留下的误差。

*[指向底部的说明。]*

我们还试了两个神经网络，MLP 和 LSTM，都没有更好，见备份第六页。

### 第 11 页 — 公平调参

只有每个模型都用同样的方式调参，比较才公平。

*[指向左边的折叠示意图。]*

看这张图。每一条是一个折，全部在训练年份里面。我们在蓝色部分拟合，在绿色小段上打分，然后窗口扩大，一共五次。

*[指向右边的要点。]*

每个模型条件完全一样：10 组随机设置、相同的时间限制、相同的随机种子。**验证块从来不碰。**

*[指向表格里 "Chosen" 两列。]*

再看选中的值。岭回归选了 alpha 1000，最强的惩罚；梯度提升选了最小的学习率。这些都是最保守的设置。**调参器在告诉我们：最安全的预测就是贴近"不变"。**

### 第 12 页 — 其他探索

*[指向左边第 1、2 点。]*

我们还把目标从价格改成价格变化量，并让每个模型分别在原始特征和标准化特征上运行：一共 20 次。

*[指向右边的图。]*

这张图显示缩放改变了什么。每一条是一个模型在一个资产上的结果。红色表示误差变大，绿色表示误差变小。

*[指向中间空着的几行。]*

看中间：**树模型完全没有条形。** 它们的预测完全相同，和我们预期的一样。线性模型和 SVR 有变化，因为它们依赖尺度。

那么，这些模型到底表现如何？请 Zhang Haoyu 为大家介绍。

---

# Part 4: Evaluation · 第四部分：评估

**Speaker / 讲者:** Zhang Haoyu · **Slides / 页码:** 13–15 · **Target speaking time / 目标时长:** about 2:50

## English Version

### Slide 13 — Four Metrics

Thank you. Part four is evaluation. We use four metrics, and each one has a job.

Mean absolute error, or MAE, is the typical miss in dollars. Root mean squared error, or RMSE, punishes big misses more.

R-squared is the share of price movement the model explains. Skill compares the model with the simple rule: zero means no better than the rule.

For our best Apple model, MAE is 2.89 dollars, against 2.91 for the rule. R-squared is 0.9556, against 0.9555.

**That is the trap: any forecast that follows yesterday's price gets a high R-squared.** So we rank models by skill. It has no units, so it also works across assets.

### Slide 14 — Results

Here is the skill of every run.

The best Apple run is SVR with standardised features, at plus 0.52 percent. That is about one and a half cents less error per forecast. The best Bitcoin run is the linear baseline on raw features, at plus 0.26 percent.

Across all twenty runs, skill stays between minus 0.78 and plus 0.52 percent, and five runs are worse than the rule.

**On daily prices, a simple rule is a very strong opponent.** Backup slide one shows every run.

### Slide 15 — How Certain Are We?

But are these small leads real, or just luck?

We compare each model with the rule on the same days, resample the days in blocks of ten, a thousand times, and get a 95 percent interval.

**All twenty intervals include zero**, even the best Apple run. So no model is reliably better; they are tied with the rule.

Why is the rule so hard to beat? Today's return tells us almost nothing about tomorrow's. The correlation is about plus 0.02 for Apple and minus 0.03 for Bitcoin: almost zero.

And that is exactly what our lesson teaches.

## 中文版本

### 第 13 页 — 四个指标

谢谢。第四部分是评估。我们用四个指标，每个都有自己的作用。

平均绝对误差 MAE，是以美元计的典型误差。均方根误差 RMSE，对大的误差惩罚更重。

R² 是模型解释了多少价格变动。Skill 把模型和简单规则作比较：0 表示没有比规则更好。

我们最好的苹果模型，MAE 是 2.89 美元，规则是 2.91；R² 是 0.9556，规则是 0.9555。

**这就是陷阱：任何跟着昨天价格走的预测，R² 都会很高。** 所以我们用 skill 来给模型排名。它没有单位，所以也能跨资产比较。

### 第 14 页 — 结果

这是每一次运行的 skill。

苹果最好的是标准化特征下的 SVR，+0.52%，相当于每次预测少了大约 1.5 美分的误差。比特币最好的是原始特征下的线性基线，+0.26%。

全部 20 次运行的 skill 都在 −0.78% 到 +0.52% 之间，其中 5 次比规则更差。

**在日度价格上，简单规则是非常强的对手。** 备份页第一页展示了每一次运行。

### 第 15 页 — 我们有多确定？

但这些小小的领先是真的，还是运气？

我们在相同的日子上把每个模型和规则比较，以连续十天为一块重采样一千次，得到 95% 区间。

**20 个区间全部包含 0**，包括苹果最好的那一次。所以没有模型可靠地更好；它们和规则打平。

为什么规则这么难打败？因为今天的收益率几乎说明不了明天。相关系数苹果约 +0.02，比特币约 −0.03，几乎为零。

而这正是我们的课要教的。

---

# Part 5: Teaching Design · 第五部分：教学设计

**Speakers / 讲者:** Lau Pak Hei (slides 16–17) · Lui Shing Lam (slide 18) · **Target speaking time / 目标时长:** about 2:05

These slides are written in short, plain sentences. **Read them exactly as written, slowly, without adding anything.** If you stop for more than about five seconds, Zhang Yancheng steps in and finishes the slide from the key point in the table at the end of this part.

这几页刻意写成短句。**照稿慢慢读，不要自由发挥。** 若停顿超过约 5 秒，由 Zhang Yancheng 接上，按本部分末尾表格里的要点讲完。

## English Version

### Slide 16 — Teaching Design (Lau Pak Hei)

Part five is teaching design. We turned our project into a sixty-minute lesson for students who are new to machine learning.

It has five tasks, and each one comes from a part of our project. Learners compare training error with error on new data, find a leak in a short piece of code, read our skill table, say which models care about scaling, and explain why low error is not profit.

Students see the simple rule first, and the models after.

And you can try all of it yourself.

### Slide 17 — Try It Yourself (Lau Pak Hei)

Everything you saw today is also on a website. It walks through the same steps, with our real data.

You can pick any day and see its ten features. You can pick any model and recompute its scores. It opens in any browser.

Scan the code to try it.

### Slide 18 — Summary (Lui Shing Lam)

To sum up. Data: two different markets, from public sources we can trace. Processing: ten features that only look backwards. Models: five models, tuned in the same way. Evaluation: all twenty runs are within one percent of the simple rule. Teaching: a sixty-minute lesson with five tasks.

Next, we will test on the sealed data once, and try the lesson with a real class. This is not investment advice. Thank you. We are happy to take questions.

## 中文版本

### 第 16 页 — 教学设计（Lau Pak Hei）

第五部分是教学设计。我们把项目做成了一节 60 分钟的课，对象是刚接触机器学习的学生。

这节课有五个任务，每个任务来自项目的一个部分。学生比较训练误差和新数据上的误差；在一小段代码里找出泄漏；读我们的 skill 表；说出哪些模型在意缩放；并解释为什么误差低不等于赚钱。

学生先看简单规则，再看模型。

而且这一切你都可以亲自试一试。

### 第 17 页 — 亲自试一试（Lau Pak Hei）

今天看到的所有内容也都放在一个网站上。它按同样的步骤展示，用的是我们的真实数据。

你可以挑任意一天，看它的十个特征；也可以挑任意一个模型，重新计算它的分数。任何浏览器都能打开。

扫这个二维码就可以试。

### 第 18 页 — 总结（Lui Shing Lam）

总结一下。数据：两个不同的市场，来源公开、可追溯。处理：十个只往回看的特征。模型：五个模型，用同样的方式调参。评估：20 次运行都在简单规则的 1% 以内。教学：一节 60 分钟、五个任务的课。

下一步：在封存的数据上测试一次，并在真实班级里试这节课。这不构成投资建议。谢谢大家，欢迎提问。

## Fallback key points · 后备要点（Zhang Yancheng）

| Slide | Key point | 要点 |
|---|---|---|
| 16 | The project becomes a 60-minute lesson; five tasks, one from each part; simple rule first, models after. | 项目变成 60 分钟的课；五个任务各来自一个部分；先看简单规则再看模型。 |
| 17 | The whole pipeline is on a website with our real data; pick a day, pick a model; scan the code. | 整个流程做成了网站，用真实数据；挑一天、挑一个模型；扫码打开。 |
| 18 | One sentence per stage; next steps; not investment advice; thank you, questions. | 每个阶段一句成果；下一步；不是投资建议；谢谢、请提问。 |

---

# Q&A — bilingual cheat sheet · 问答中英对照

Questions are answered by Dong Yuankun, Zhang Yancheng or Zhang Haoyu. Lau Pak Hei and Lui Shing Lam do not take Q&A; if a question is aimed at them, Zhang Yancheng answers. 问答由 Dong Yuankun、Zhang Yancheng、Zhang Haoyu 回答；Lau Pak Hei 和 Lui Shing Lam 不接问答，若有人点名问他们，由 Zhang Yancheng 回答。

| Question | Answers | English answer | 中文 |
|---|---|---|---|
| Where exactly is the data from? | Dong Yuankun | The two URLs on slide 3 are the exact calls in `src/int4096/data/providers.py`; the saved files and their SHA-256 hashes are in `data/raw/`. | 第 3 页两个链接就是代码实际调用的地址；保存的文件和哈希在 `data/raw/`。 |
| Why AAPL and BTC? | Dong Yuankun | Different calendars, volatility, scale and corporate actions: one protocol on two structures is a robustness check. | 日历、波动率、量级、公司行为都不同：同一协议跑两种结构，是稳健性检验。 |
| Is Binance BTC a global price? | Dong Yuankun | No. It is one exchange, quoted in USDT, which is not exactly USD. We say "BTC/USDT on Binance". | 不是。它是单一交易所、以 USDT 计价，USDT 不完全等于美元。 |
| Why not adjusted close? | Dong Yuankun | Adjustments are revised after the fact, so they carry future information into the past. Our window has no split, so raw close is continuous. | 复权会事后修订，会把未来信息带进过去；窗口内没有拆股，原始收盘价是连续的。 |
| Why classical ML, not deep learning? | Zhang Yancheng | The handout discourages it, so the main comparison is classical. We also ran an MLP and an LSTM to predict next-day direction: on Apple both did worse than "always up", and all four intervals include zero → Backup 6. | 讲义不鼓励，所以主比较用经典模型。我们另外让 MLP 和 LSTM 预测涨跌：苹果上两者都不如"永远猜涨"，四个区间都包含 0 → Backup 6。 |
| Did you leak future data? | Zhang Yancheng | Chronological split, a purged boundary row, a sealed test block, and 6 of 6 injected defects caught → Backup 3. | 按时间切分、边界删行、封存测试集、6/6 注入缺陷被抓到 → Backup 3。 |
| Did you cherry-pick P2? | Zhang Haoyu | No. Backup 1 shows all 20 runs. The best Bitcoin result overall is the unscaled linear baseline at +0.26%. | 没有。Backup 1 有全部 20 次；比特币整体最好的是未缩放线性基线 +0.26%。 |
| Was tuning fair? | Zhang Yancheng | Same folds, same 10 trials, same 90 s, same seed, grids frozen beforehand → Backup 2. | 同样的折、10 次试验、90 秒、同一种子、网格事先冻结 → Backup 2。 |
| Why do chosen values sit at grid edges? | Zhang Yancheng | The tuner prefers the most cautious settings because there is little signal to fit. Widening the grids is a next step. | 信号太少，调参器偏好最保守的设置；放宽网格是下一步。 |
| Is +0.52% meaningful? | Zhang Haoyu | Not by our own test: all 20 bootstrap intervals include zero. | 按我们自己的检验不是：20 个区间全包含 0。 |
| Why only P0 and P2? | Zhang Yancheng | They isolate the effect of scaling. P1 would duplicate P0 because there are no missing values; P3 and P4 are next. | 它们隔离出缩放的影响；P1 因无缺失值会与 P0 重复；P3、P4 是下一步。 |
| Can this make money? | Zhang Haoyu | No. Error metrics ignore costs and risk; we make no profitability claim. | 不能。误差指标不含成本和风险；我们不声称盈利。 |
| Where can we see the details? | Zhang Yancheng | Everything is on our website (QR code on slide 17), built from the same data and results as these slides. | 所有细节都在我们的网站上（第 17 页二维码），与幻灯片用的是同一份数据和结果。 |
| Did the lesson improve learning? | Zhang Yancheng | The lesson is built and ready; measuring learning is what the classroom pilot is for. | 课程已完成；衡量学习效果正是课堂试点要做的。 |

# Backup slides · 备用页

| # | Slide | English one-liner | 中文 |
|---|---|---|---|
| 19 | Full 20-run matrix | "All twenty cells, nothing selected. The best Bitcoin result is the unscaled linear baseline at +0.26%." | 全部 20 格，没有挑选；比特币最好的是未缩放线性基线 +0.26%。 |
| 20 | Fairness and manifest audit | "Identical features, splits, dates and budget. Every run records commit, data hash and configuration." | 特征、切分、日期、预算都相同；每次运行记录提交、数据哈希、配置。 |
| 21 | Why one row is dropped | "Friday's label is Monday's price. The purge keeps every training answer out of the validation block." | 周五的标签是周一的价格；删行保证训练的答案不会落进验证块。 |
| 22 | Permutation importance | "One- and five-day returns, 30-day volatility and the 20-day average gap matter most. Magnitudes are tiny. Importance is not causation." | 1、5 日收益率、30 日波动率、20 日均线偏离最重要；量级很小；重要性不等于因果。 |
| 23 | Q&A cards | "Short, prepared answers to the most likely questions." | 最可能问题的简短答案。 |
| 24 | Supplementary MLP/LSTM test | "Asked to call tomorrow's direction, neither network beat a simple rule; all four intervals include zero." | 预测涨跌时两个神经网络都没有打败简单规则；四个区间都包含 0。 |

# If you are running over · 超时怎么办

Check the clock at the **end of slide 5** (≈4:50) and the **end of slide 9**: it should read **≈9:15** (see `timing_plan.md`).

| Situation | Cut | 中文 |
|---|---|---|
| 9:40 or later after slide 9 | Slide 10: drop the neural-network sentence. Slide 12: skip the "target" sentence. (~20 s) | 第 10 页去掉神经网络那句；第 12 页跳过"目标"那句，省约 20 秒。 |
| 10:10 or later | Slide 11: shorten the fold-diagram paragraph to one sentence. (~10 s) | 再把第 11 页示意图那段压成一句，省约 10 秒。 |
| **Never cut** | Slide 13 (metrics), slide 14 (results), slide 15 (intervals). | **绝不能砍**第 13、14、15 页。 |

# Rehearsal checklist · 排练清单

- [ ] Every speaker has read their **English Version** aloud twice. 每位讲者把英文大声读两遍。
- [ ] Every speaker can explain each of their slides in one sentence without the script. 不看稿能用一句话讲出每一页的意思。
- [ ] Each part starts by naming the part ("Part three: models and tuning"). 每部分开口先报部分名称。
- [ ] The four handovers (after slides 5, 12, 15, 17) are rehearsed. 四次交接要练。
- [ ] **Lau Pak Hei and Lui Shing Lam** each read their slides aloud to Zhang Yancheng at least three times before the talk, timed, with no ad-libbing. Lau Pak Hei 和 Lui Shing Lam 正式前至少各对 Zhang Yancheng 计时朗读三遍，不加词。
- [ ] Zhang Yancheng can deliver slides 16–18 from the fallback key points as the backup. Zhang Yancheng 能按后备要点讲完第 16–18 页。
- [ ] Two full timed run-throughs with a visible clock. 全流程计时彩排两次。
- [ ] Backup 1 and Backup 3 are ready in a second window. 准备好 Backup 1 和 3。
- [ ] Say "every **model-performance** number is from validation", not "every number". 说"每个模型表现数字"，不说"每个数字"。

> **Reminder · 提醒** The presentation is in English; Chinese here is a comprehension aid only. 演示用英文；中文仅供理解。
