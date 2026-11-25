# Bilingual Presentation Script (English spoken · 中文对照)

**Deck:** `deliverables/presentation/INT4096_Presentation.pdf` — 26 pages (18 narrative + 6 backup + 2 references)
**Structure:** one part per pipeline stage: Data Selection → Processing & Features → Models & Tuning → Evaluation → Teaching Design
**Clock:** `timing_plan.md` · **Key messages:** `speaker_notes.md` · **Story:** `deliverables/presentation/planning/feature_extraction_story.md`
**Speech:** 16:55 planned (+0:40 for four handovers and slide changes, +2:00 Q&A = 19:35 inside the 20:00 slot)

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
> | 6–12 | Part 2 Processing & Features, Part 3 Models & Tuning | **Zhang Yancheng** | 7:10 |
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
| Pace | ~105 words per minute. The English below is 1,761 words, i.e. about 16 minutes 50 seconds. | 约每分钟 105 词；英文共 1,761 词，约 16 分 50 秒。 |
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

**Speaker / 讲者:** Zhang Yancheng · **Slides / 页码:** 6–12 · **Target speaking time / 目标时长:** about 7:10

## English Version

### Slide 6 — Problems in the Raw Data

Thank you. Part two is processing and feature engineering.

Raw prices cannot go straight into a model. This table lists six problems, and what we did about each one.

The biggest problem is that prices drift. For example, in our training years Bitcoin never closed above 77,000 dollars. In the validation year it reached almost 125,000. A model trained on raw prices cannot handle levels it has never seen.

So instead of prices, we give the model ratios: how much the price moved, and how far it sits from its recent average.

The other problems follow one simple rule: **use only what was known at that moment.**

### Slide 7 — From One Day to Ten Features

Here is how one real day becomes ten numbers: Apple, on the twenty-first of November 2024.

It closed at 228.52 dollars, after 229.00 the day before. So the one-day return is minus 0.21 percent. Five and twenty days back give two more returns.

The close was 0.33 percent above its five-day average. That is the moving-average gap, and we also use a twenty-day one.

Volatility measures how much the price jumped around over ten and thirty days. Range is the day's high minus its low, divided by the close. Volume change compares today's volume with its recent average. And Thursday is coded as three.

**Every feature uses only this day and earlier days.** Our tests add fake future prices to the data, and the earlier features must not change.

### Slide 8 — Every Model Gets the Same Data

So, **did every model get the same data?** Yes.

Every model gets the same rows, the same ten features, the same target, and the same splits. Only the algorithm changes.

There is one switch: preprocessing. P0 leaves the features as they are. P2 standardises them, using the average and spread of the training years only.

Why does this matter? A daily return is about 0.02 in size, but the weekday is about 1.4. Without scaling, the weekday dominates models that measure distance, like SVR. Trees split one feature at a time, so they do not care.

Finally, the model predicts tomorrow's **change**, and we add it to today's close. On our example day, SVR predicted plus 10 cents, so the forecast was 228.62.

### Slide 9 — Splitting by Time

Next, we split the data by time: the first 60 percent for training, the next 20 for validation, and the last 20 for testing. The test block stays sealed.

At each boundary we drop one row. Why? Our label is tomorrow's close. So the answer of the last training row would be the first validation price. Dropping one row keeps them apart.

We also attacked our own pipeline. A script injected six common leakage mistakes, one at a time. Our tests caught all six.

From here on, **every model-performance number comes from the validation block.**

### Slide 10 — Five Models and a Baseline

Part three: models and tuning.

Besides the baseline, we chose five models that learn in three different ways.

First, two linear models. They give each feature a weight and add them up. Ridge also adds a penalty that keeps the weights small.

Second, support vector regression. It predicts from how similar a day is to past days. Because it measures distance, it is sensitive to scale.

Third, two tree ensembles. A random forest averages many independent trees. Gradient boosting adds trees one by one, each fixing the errors left so far.

We also tried two neural networks, an MLP and an LSTM, in a separate test. Neither did better; see our backup slides.

### Slide 11 — Fair Tuning

A comparison is only fair if every model is tuned the same way.

We tune inside the training years only. For example, we fit on the first part, test on the next slice, then grow the window and repeat, five times.

Each model tries ten random settings, with the same time limit and seed. We keep the setting with the lowest average error. The validation block is never touched.

Look at what the tuner chose: mostly the most cautious settings. Ridge took the strongest penalty, and boosting took the smallest learning rate. **The tuner is telling us that the safest forecast stays close to "no change".**

### Slide 12 — What Else We Explored

We explored more than settings.

First, the target: we changed it from the price to the price change, as you saw.

Second, every model ran twice, on raw and on standardised features. That gives twenty runs.

Third, this chart shows what scaling changed. The two tree models gave exactly the same predictions, as expected. SVR and ridge changed, because they depend on scale.

So, how well did all these models do? Zhang Haoyu will show you.

## 中文版本

### 第 6 页 — 原始数据的问题

谢谢。第二部分是数据处理与特征工程。

原始价格不能直接放进模型。这张表列出了六个问题，以及我们对每个问题的处理方法。

最大的问题是价格会漂移。例如，在训练年份里，比特币的收盘价从没超过 77,000 美元；到了验证年份，它涨到了接近 125,000 美元。用原始价格训练的模型无法处理它从没见过的水平。

所以我们不给模型价格，而是给它比率：价格变动了多少，以及它离近期均值有多远。

其余问题都遵循一条简单的规则：**只用当时已经知道的信息。**

### 第 7 页 — 从一天的数据到十个特征

这是真实的一天怎样变成十个数字：苹果，2024 年 11 月 21 日。

当天收盘 228.52 美元，前一天是 229.00。所以一日收益率是 −0.21%。和 5 天前、20 天前比较，又得到两个收益率。

收盘价比 5 日均价高 0.33%，这就是均线偏离；我们还用了 20 日的版本。

波动率衡量过去 10 天和 30 天里价格跳动有多大。幅度是当天最高价减最低价，再除以收盘价。成交量变化是今天的成交量和近期平均成交量的比较。星期四编码为 3。

**每个特征只用这一天及之前的数据。** 我们的测试会在数据末尾加入假的未来价格，之前的特征必须完全不变。

### 第 8 页 — 每个模型用的数据都一样

那么，**每个模型用的数据都一样吗？** 是的。

每个模型用相同的行、相同的十个特征、相同的目标和相同的切分。唯一变化的是算法。

只有一个开关：预处理。P0 保持特征原样；P2 把特征标准化，只用训练年份的均值和波动幅度。

为什么重要？日收益率的量级大约是 0.02，而星期几大约是 1.4。不做缩放的话，星期几会主导依赖距离的模型，比如 SVR。树每次只按一个特征切分，所以不受影响。

最后，模型预测的是明天的**变化量**，我们再把它加到今天的收盘价上。在刚才的例子里，SVR 预测 +10 美分，所以预测值是 228.62。

### 第 9 页 — 按时间切分

接下来，我们按时间切分数据：前 60% 用于训练，接下来 20% 用于验证，最后 20% 用于测试。测试块一直封存。

每个边界我们删掉一行。为什么？因为标签是明天的收盘价，所以最后一个训练行的答案，恰好就是验证集的第一个价格。删掉一行就能把它们隔开。

我们还主动攻击了自己的流水线：一个脚本逐个注入六种常见的泄漏错误，我们的测试全部抓到了。

从这里开始，**每一个模型表现数字都来自验证块。**

### 第 10 页 — 五个模型和一个基准

第三部分：模型与调参。

除了基准，我们选了五个模型，它们用三种不同的方式学习。

第一，两个线性模型。它们给每个特征一个权重，再加起来。岭回归还加了一个惩罚项，让权重保持很小。

第二，支持向量回归。它根据某一天和过去的日子有多相似来预测。因为它衡量距离，所以对尺度敏感。

第三，两种树集成。随机森林把许多独立的树取平均；梯度提升一棵接一棵地加树，每棵都修正前面留下的误差。

我们还在另一个独立测试里试了两个神经网络，MLP 和 LSTM。两者都没有更好，见备份页。

### 第 11 页 — 公平调参

只有每个模型都用同样的方式调参，比较才公平。

我们只在训练年份里面调参。例如，先用前面一段拟合，在下一小段上测试，然后把窗口扩大再重复，一共五次。

每个模型试 10 组随机设置，时间限制相同、随机种子相同，保留平均误差最低的那组。验证块从来不碰。

看看调参器选了什么：大多是最保守的设置。岭回归选了最强的惩罚，梯度提升选了最小的学习率。**调参器在告诉我们：最安全的预测就是贴近"不变"。**

### 第 12 页 — 其他探索

我们探索的不只是参数设置。

第一，目标：我们把它从价格改成了价格变化量，前面已经看到。

第二，每个模型都跑两次，一次用原始特征，一次用标准化特征，总共 20 次运行。

第三，这张图显示缩放改变了什么。两种树模型的预测完全相同，和预期一样。SVR 和岭回归有变化，因为它们依赖尺度。

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

Check the clock at the **end of slide 5** (≈4:50) and the **end of slide 9**: it should read **≈9:10** (see `timing_plan.md`).

| Situation | Cut | 中文 |
|---|---|---|
| 9:40 or later after slide 9 | Slide 10: drop the neural-network sentence. Slide 12: skip the "target" sentence. (~20 s) | 第 10 页去掉神经网络那句；第 12 页跳过"目标"那句，省约 20 秒。 |
| 10:10 or later | Slide 11: skip the "For example…" walkthrough of the folds. (~10 s) | 再跳过第 11 页"例如……"那段，省约 10 秒。 |
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
