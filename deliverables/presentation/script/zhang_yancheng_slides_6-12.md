### Slide 6 - Problems in the Raw Data / 原始数据的问题 · 0:55

**English**

> Thank you, Dong Yuankun. Now let's move on to Part Two, Processing and Feature Engineering.
>
> This table shows six issues. I'll highlight the three most important ones.

*[Point to the first three rows. · 指表格前三行]*

> First, price levels change over time, so we use returns and ratios as features.
>
> Second, adjusted prices can be revised later, so we use the raw closing price as our target.
>
> Third, Apple and Bitcoin follow different trading calendars, so we predict the next close on each asset's own calendar.
>
> Given the time, I'll leave the details in the table and move on to our features.

**中文提词**

- 谢谢 Dong Yuankun → 第二部分：数据处理与特征工程
- 六个问题，点出三个重点
- 价格漂移 → 用收益率和比率
- 复权价事后改 → 预测原始收盘价
- 交易日历不同 → 各自预测下一次收盘
- 时间有限，细节看表 → 下一页讲特征

<!-- pagebreak -->

### Slide 7 - From One Day to Ten Features / 从一天的数据到十个特征 · 1:10

**English**

*[Point to the small table on the left. · 指左边小表]*

> On the left is one real day for Apple. On the right are its ten features.

*[Point to "Close today" and "Close yesterday" on the left, then to ret_1. · 指左边今天、昨天收盘，再指 ret_1]*

> First, today's close against yesterday's close. That change, in percent, is the one-day return.

*[Point to ret_5 and ret_20. · 指 ret_5 和 ret_20]*

> Then the same against five days ago and twenty days ago: the short move and the longer move.

*[Point to ma_gap_5 and ma_gap_20. · 指 ma_gap_5 和 ma_gap_20]*

> Next, today's close against its five-day and twenty-day average: is the price above or below its recent trend?

*[Move down the remaining rows. · 往下指过其余几行]*

> Then volatility, how jumpy the price was; range, how wide the day was; volume change; and the weekday. Notice that **every one is a comparison, not a price.**

*[Point to the note under the table. · 指表格下方说明]*

> Now the key point: **every feature uses only today and earlier days, never tomorrow.** We test it: we add fake future prices, and the earlier rows must not change.

**中文提词**

- 左边：苹果真实的一天 → 右边：十个特征
- 今天收盘 vs 昨天收盘 → 一日收益率
- 再比 5 天前、20 天前 → 短期和较长期变化
- 今天收盘 vs 5 日、20 日均价 → 在趋势上方还是下方
- 波动率、日内幅度、成交量变化、星期几 → 都是比较，不是价格
- 关键：只用今天和过去；加假未来数据，旧行不变

<!-- pagebreak -->

### Slide 8 - Every Model Gets the Same Data / 每个模型用相同的数据 · 1:10

**English**

> You may be wondering: **did every model get the same data?**

*[Trace the arrows across the top, left to right. · 从左到右沿顶部箭头指]*

> Follow the arrows. Daily prices become ten features, go through preprocessing, and enter one of the five models.

*[Point to the list on the right. · 指右边列表]*

> As the list on the right says, all five models get the same rows, features, target and splits. **Only the algorithm changes.**

*[Point to the third box, "P0 / P2". · 指第三个方框 P0/P2]*

> There is just one switch. P0 leaves the features as they are. P2 standardises them, using the training years only.

*[Point to the table at the bottom left. · 指左下表格]*

> Why? Compare these rows. A daily return is a tiny number, but the weekday is about a hundred times larger. Without scaling, the weekday dominates SVR. Trees do not care.

*[Point to the last box of the diagram. · 指流程图最后一格]*

> Finally, the forecast is today's close plus the predicted change. So the model only has to learn the change, not the whole price.

**中文提词**

- 提问：每个模型拿到一样的数据吗？
- 价格 → 十个特征 → 预处理 → 模型
- 同样的行、特征、目标和切分
- P0 原样。P2 只用训练期拟合标准化
- 收益率很小，星期几大约大一百倍 → 尺度影响 SVR，树不受影响
- 预测收盘 = 今天收盘 + 预测变化 → 模型只学变化

<!-- pagebreak -->

### Slide 9 - Splitting by Time / 按时间切分 · 0:50

**English**

*[Trace the bar at the top from left to right. · 从左到右沿顶部时间条指]*

> Next, the split. Time runs from left to right: sixty percent to train, twenty to validate, twenty to test. The grey test block stays sealed.

*[Point to the two small red boxes, "Drop 1 row". · 指两个红色小框 Drop 1 row]*

> Notice these two small red boxes. At each boundary we drop one row. Why? Our label is tomorrow's close, so the last training answer would be the first validation price.

*[Point to the right column. · 指右栏]*

> We also attacked our own pipeline with six common leakage mistakes, one at a time. **All six were caught.**

*[Point to the line at the bottom. · 指底部那行字]*

> So please remember: **every model-performance number from here on comes from the validation block.**

**中文提词**

- 60% 训练、20% 验证、20% 测试 → 测试封存
- 每个边界删一行 → 避免标签跨界
- 故意加入六种泄漏错误 → 全抓到
- 后面的模型表现数字 → 都来自验证集

<!-- pagebreak -->

### Slide 10 - Five Models and a Baseline / 五个模型和一个基准 · 1:05

**English**

> Part three: models and tuning.

*[Point to the first row. · 指第一行]*

> The table has one row per model. The first row is our baseline. Below it are five models that learn in three different ways.

*[Point to the linear baseline and ridge rows. · 指线性基线和岭回归两行]*

> First, two linear models. They give each feature a weight and add them up; ridge also keeps the weights small.

*[Point to the SVR row. · 指 SVR 那行]*

> Second, SVR. It predicts from how similar a day is to past days. It measures distance, so **it is sensitive to scale. Keep that in mind.**

*[Point to the last two rows. · 指最后两行]*

> Third, two tree ensembles. A random forest averages many independent trees. Gradient boosting adds trees one by one, each fixing the errors left so far.

*[Point to the note at the bottom. · 指底部说明]*

> We also tried two neural networks, an MLP and an LSTM. Neither did better; that is backup six.

**中文提词**

- 第三部分：模型与调参
- 首行是基准。五个模型分三类
- 线性模型：特征加权。岭回归压低权重
- SVR：用距离找相似日 → 对尺度敏感
- 随机森林：多棵树取平均。梯度提升：逐棵纠错
- MLP、LSTM 没更好 → 备份第 6 页

<!-- pagebreak -->

### Slide 11 - Fair Tuning / 公平调参 · 1:00

**English**

> A comparison is only fair if every model is tuned the same way.

*[Point to the fold diagram on the left. · 指左边折叠示意图]*

> Look at the diagram. Each bar is one fold, inside the training years only. We fit on the blue part and score on the green slice. Then the window grows, five times.

*[Point to the bullet points. · 指右边要点]*

> Every model gets the same deal: ten random settings, the same time limit, the same seed. **The validation block is never touched.**

*[Point to the "Chosen" columns of the table. · 指表格 Chosen 两列]*

> Now look at what was chosen. Ridge took alpha 1000, the strongest penalty. Boosting took the smallest learning rate. These are the most cautious settings. **The tuner is telling us that the safest forecast stays close to "no change".**

**中文提词**

- 同样的调参方式，比较才公平
- 只用训练期。蓝色拟合、绿色打分，窗口逐次扩大
- 10 组设置、同时限、同种子。验证集不参与
- 岭回归 alpha 1000，提升用最小学习率 → 接近“不变”

<!-- pagebreak -->

### Slide 12 - What Else We Explored / 我们还试了什么 · 0:55

**English**

*[Point to points 1 and 2 on the left. · 指左边第 1、2 点]*

> We also changed the target from price to price change, and we ran every model on raw and on standardised features: twenty runs.

*[Point to the chart. · 指右边的图]*

> The chart shows what scaling changed. Each bar is one model on one asset. Red means the error went up; green means it went down.

*[Point to the empty rows in the middle. · 指中间空着的几行]*

> Look at the middle: **the tree models have no bar at all.** Their predictions were exactly the same, just as we expected. The linear models and SVR moved, because they depend on scale.

> So, how well did all these models do? Zhang Haoyu will show you.

**中文提词**

- 改预测目标，用原始或标准化特征 → 20 次
- 一条 = 一个模型 × 一个资产。红变差，绿变好
- 树模型没变化。线性模型和 SVR 受尺度影响
- 表现怎么样？→ 交给 Zhang Haoyu

<!-- pagebreak -->

### If running long · 超时怎么砍

| Clock after slide 9 | Cut | 中文 |
|---|---|---|
| 9:25 or later | Slide 10: drop the neural-network sentence. Slide 12: drop the first paragraph. (~20 s) | 删第 10 页神经网络那句、第 12 页第一段 |
| 9:55 or later | Slide 11: shorten the diagram paragraph to "Five folds, training years only." (~10 s) | 第 11 页示意图那段压成一句 |

### Likely questions for you · 可能问你的问题

| Question | Short answer | 中文 |
|---|---|---|
| Did every model get the same data? | Yes: same rows, ten features, target, splits and folds; only the algorithm and the P0/P2 switch change. | 是，只有算法和 P0/P2 不同 |
| Why not deep learning? | The handout discourages it; a separate MLP/LSTM direction test did no better, all four intervals include zero → Backup 6. | 讲义不鼓励；补充测试没更好 → Backup 6 |
| Did you leak future data? | Chronological split, a purged row per boundary, sealed test block, 6 of 6 injected defects caught → Backup 3. | 时间切分、删行、封存、6/6 → Backup 3 |
| Was tuning fair? | Same folds, 10 trials, 90 s, seed 42, grids frozen beforehand → Backup 2. | 同折、10 次、90 秒、同种子 → Backup 2 |
| Why do choices sit at grid edges? | Little signal, so the tuner picks the most cautious setting; wider grids are a next step. | 信号少，选最保守；下一步放宽网格 |
| Why only P0 and P2? | They isolate scaling; P1 equals P0 because there are no missing values. | 隔离缩放影响；P1 无缺失值等于 P0 |
