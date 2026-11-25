# Zhang Yancheng — Slides 6–12 (Part 2 & Part 3)

**Part 2:** Processing & Feature Engineering (slides 6–9) · **Part 3:** Models & Tuning (slides 10–12)
**Target speaking time:** about 7:20 (772 spoken words at ~105 wpm) · **On the clock:** start ≈4:50, end of slide 9 ≈9:10, hand over ≈12:10
**Source:** extracted from `speaker_script_bilingual.md`; if the two differ, the full script wins.

> ### How to read this page · 使用方法
> **Indented text** is what you say, in English. **【提示】** under each paragraph is a one-line Chinese cue: glance at it if you lose your place. Do not read it aloud.
> Grey lines in *[brackets]* are stage directions: point first, then speak. **Bold** = slow down and stress.
>
> 缩进的英文是要念的。每段下面的【提示】是一行中文快速提示，忘词时瞄一眼，不要念。方括号是动作：先指，再说。粗体放慢加重。

---

### Slide 6 — Problems in the Raw Data · 1:05

> Thank you. Part two is processing and feature engineering.

【提示】开场：谢谢，进入第二部分——数据处理与特征工程

> Raw prices cannot go straight into a model. This table shows six problems. Read each row from left to right: the problem, why it matters, and what we did.

【提示】原始价格不能直接用；表里六个问题，每行读法：问题→原因→做法

*[Point to the first row. · 指第一行]*

> The first row is the most important: prices drift. For example, in our training years Bitcoin never closed above 77,000 dollars. In the validation year, it reached almost 125,000. A model trained on raw prices cannot handle levels it has never seen.

【提示】第一行最重要：价格漂移；比特币训练期 < 77,000，验证期近 125,000

*[Point to the last cell of the first row. · 指第一行最右边一格]*

> So, as the last column says, we give the model ratios instead of prices.

【提示】所以给模型比率，不给价格

*[Sweep your hand down the other five rows. · 手往下扫过其余五行]*

> The other five rows all follow one rule, and it runs through our whole project: **use only what was known at that moment.**

【提示】其余五行同一规则（重读）：只用当时已知的信息

---

### Slide 7 — From One Day to Ten Features · 1:15

*[Point to the small table on the left. · 指左边小表]*

> On the left is one real day: Apple, the twenty-first of November 2024. On the right are the ten features we compute from it.

【提示】左边：苹果 2024-11-21 真实一天；右边：算出的十个特征

*[Point to the first row of the right table, ret_1. · 指右表第一行 ret_1]*

> Let's work out the first one together. Apple closed at 228.52, after 229.00 the day before. So the one-day return is minus 0.21 percent. The next row does the same against five and twenty days ago.

【提示】一起算 ret_1：228.52 / 229.00 − 1 = −0.21%；下一行是 5 天、20 天

*[Point to ma_gap_5. · 指 ma_gap_5]*

> Next, the close was 0.33 percent above its five-day average. That is the moving-average gap.

【提示】收盘比 5 日均价高 0.33% = 均线偏离

*[Move down the remaining rows. · 往下指过其余几行]*

> Then volatility, range and volume change. Notice that **every one is a ratio, not a price.** And the last row: Thursday is coded as three.

【提示】波动率、幅度、成交量变化；（重读）全是比率不是价格；星期四 = 3

*[Point to the note under the table. · 指表格下方说明]*

> Now the key point: **every feature uses only this day and earlier days.** We test it by adding fake future prices; the earlier rows must not change.

【提示】关键点（重读）：只用当天及之前；加假的未来价格，旧行不变

---

### Slide 8 — Every Model Gets the Same Data · 1:10

> You may be wondering: **did every model get the same data?**

【提示】抛出问题（重读）：每个模型数据一样吗？

*[Trace the arrows across the top, left to right. · 从左到右沿顶部箭头指]*

> Follow the arrows. Daily prices become ten features, go through preprocessing, and enter one of the five models.

【提示】跟着箭头：价格 → 十个特征 → 预处理 → 五个模型之一

*[Point to the list on the right. · 指右边列表]*

> As the list on the right says, all five models get the same rows, features, target and splits. **Only the algorithm changes.**

【提示】右边列表：行、特征、目标、切分全相同；（重读）只有算法不同

*[Point to the third box, "P0 / P2". · 指第三个方框 P0/P2]*

> There is just one switch. P0 leaves the features as they are. P2 standardises them, using the training years only.

【提示】唯一开关：P0 原样，P2 用训练年份标准化

*[Point to the table at the bottom left. · 指左下表格]*

> Why? Compare these rows. A daily return is about 0.02 in size; the weekday is about 1.4, a hundred times larger. Without scaling, the weekday dominates SVR. Trees do not care.

【提示】为什么：收益率 ~0.02，星期几 ~1.4，差一百倍；不缩放就主导 SVR；树不在乎

*[Point to the last box of the diagram. · 指流程图最后一格]*

> Finally, the forecast is today's close plus the predicted change. On our example day: 228.52 plus 10 cents, so 228.62.

【提示】预测 = 今天收盘 + 预测变化：228.52 + 0.10 = 228.62

---

### Slide 9 — Splitting by Time · 0:50

*[Trace the bar at the top from left to right. · 从左到右沿顶部时间条指]*

> Next, the split. Time runs from left to right: sixty percent to train, twenty to validate, twenty to test. The grey test block stays sealed.

【提示】按时间切：60 训练 / 20 验证 / 20 测试；灰色测试块封存

*[Point to the two small red boxes, "Drop 1 row". · 指两个红色小框 Drop 1 row]*

> Notice these two small red boxes. At each boundary we drop one row. Why? Our label is tomorrow's close, so the last training answer would be the first validation price.

【提示】红框：每个边界删一行；标签是明天收盘，否则训练答案 = 验证第一个价格

*[Point to the right column. · 指右栏]*

> We also attacked our own pipeline with six common leakage mistakes, one at a time. **All six were caught.**

【提示】主动攻击：注入六种泄漏错误；（重读）六种全抓到

*[Point to the line at the bottom. · 指底部那行字]*

> So please remember: **every model-performance number from here on comes from the validation block.**

【提示】请记住（重读）：之后所有模型表现数字都来自验证块

---

### Slide 10 — Five Models and a Baseline · 1:05

> Part three: models and tuning.

【提示】第三部分：模型与调参

*[Point to the first row. · 指第一行]*

> The table has one row per model. The first row is our baseline. Below it are five models that learn in three different ways.

【提示】每行一个模型；第一行是基准，下面五个模型、三种学法

*[Point to the linear baseline and ridge rows. · 指线性基线和岭回归两行]*

> First, two linear models. They give each feature a weight and add them up; ridge also keeps the weights small.

【提示】一、两个线性模型：特征加权求和；岭回归让权重变小

*[Point to the SVR row. · 指 SVR 那行]*

> Second, SVR. It predicts from how similar a day is to past days. It measures distance, so **it is sensitive to scale. Keep that in mind.**

【提示】二、SVR：看和过去哪些天相似；（重读）对尺度敏感，记住这点

*[Point to the last two rows. · 指最后两行]*

> Third, two tree ensembles. A random forest averages many independent trees. Gradient boosting adds trees one by one, each fixing the errors left so far.

【提示】三、两种树集成：随机森林取平均；梯度提升逐棵修正误差

*[Point to the note at the bottom. · 指底部说明]*

> We also tried two neural networks, an MLP and an LSTM. Neither did better; that is backup six.

【提示】另试 MLP 和 LSTM，没有更好，见备份第 6 页

---

### Slide 11 — Fair Tuning · 1:00

> A comparison is only fair if every model is tuned the same way.

【提示】调参方式一样，比较才公平

*[Point to the fold diagram on the left. · 指左边折叠示意图]*

> Look at the diagram. Each bar is one fold, inside the training years only. We fit on the blue part and score on the green slice. Then the window grows, five times.

【提示】示意图：每条一个折，只在训练年份；蓝色拟合、绿色打分，窗口扩大五次

*[Point to the bullet points. · 指右边要点]*

> Every model gets the same deal: ten random settings, the same time limit, the same seed. **The validation block is never touched.**

【提示】条件相同：10 组设置、同时限、同种子；（重读）验证块从不碰

*[Point to the "Chosen" columns of the table. · 指表格 Chosen 两列]*

> Now look at what was chosen. Ridge took alpha 1000, the strongest penalty. Boosting took the smallest learning rate. These are the most cautious settings. **The tuner is telling us that the safest forecast stays close to "no change".**

【提示】选中值：岭回归 alpha 1000、提升最小学习率，都最保守；（重读）最安全就是贴近"不变"

---

### Slide 12 — What Else We Explored · 0:55

*[Point to points 1 and 2 on the left. · 指左边第 1、2 点]*

> We also changed the target from price to price change, and we ran every model on raw and on standardised features: twenty runs.

【提示】目标改为价格变化；原始 vs 标准化各跑一次，共 20 次

*[Point to the chart. · 指右边的图]*

> The chart shows what scaling changed. Each bar is one model on one asset. Red means the error went up; green means it went down.

【提示】图：每条一个模型×资产；红 = 误差变大，绿 = 变小

*[Point to the empty rows in the middle. · 指中间空着的几行]*

> Look at the middle: **the tree models have no bar at all.** Their predictions were exactly the same, just as we expected. The linear models and SVR moved, because they depend on scale.

【提示】看中间（重读）：树模型没有条，完全不变；线性模型和 SVR 变了，因为依赖尺度

> So, how well did all these models do? Zhang Haoyu will show you.

【提示】交接：表现如何？请 Zhang Haoyu

---

### If running long · 超时怎么砍

| Clock after slide 9 | Cut | 中文 |
|---|---|---|
| 9:40 or later | Slide 10: drop the neural-network sentence. Slide 12: drop the first paragraph. (~20 s) | 删第 10 页神经网络那句、第 12 页第一段 |
| 10:10 or later | Slide 11: shorten the diagram paragraph to "Five folds, training years only." (~10 s) | 第 11 页示意图那段压成一句 |

### Likely questions for you · 可能问你的问题

| Question | Short answer | 中文 |
|---|---|---|
| Did every model get the same data? | Yes: same rows, ten features, target, splits and folds; only the algorithm and the P0/P2 switch change. | 是，只有算法和 P0/P2 不同 |
| Why not deep learning? | The handout discourages it; a separate MLP/LSTM direction test did no better, all four intervals include zero → Backup 6. | 讲义不鼓励；补充测试没更好 → Backup 6 |
| Did you leak future data? | Chronological split, a purged row per boundary, sealed test block, 6 of 6 injected defects caught → Backup 3. | 时间切分、删行、封存、6/6 → Backup 3 |
| Was tuning fair? | Same folds, 10 trials, 90 s, seed 42, grids frozen beforehand → Backup 2. | 同折、10 次、90 秒、同种子 → Backup 2 |
| Why do choices sit at grid edges? | Little signal, so the tuner picks the most cautious setting; wider grids are a next step. | 信号少，选最保守；下一步放宽网格 |
| Why only P0 and P2? | They isolate scaling; P1 equals P0 because there are no missing values. | 隔离缩放影响；P1 无缺失值等于 P0 |
