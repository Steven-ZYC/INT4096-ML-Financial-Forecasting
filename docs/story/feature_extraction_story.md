# Feature Extraction Story
## INT4096 — Learning Machine Learning Through Financial Forecasting

> [!NOTE]
> 本文档梳理从原始金融数据到最终模型评估的完整流程，以"故事线"方式分阶段讲述，供 PPT Slides 内容确认及教学材料撰写使用。文中所有实验数字均来自项目 `artifacts/` 目录，由 `scripts/build_slide_assets.py` 自动提取，不手动录入。

---

## 目录

1. [Act I · 数据选择：我们挑了什么、为什么挑](#act-i--数据选择)
2. [Act II · 数据处理：清洗、特征工程与切割防漏](#act-ii--数据处理)
3. [Act III · 训练阶段：模型选择与调参](#act-iii--训练阶段)
4. [Act IV · 模型评估：准确度、鲁棒性与对比排序](#act-iv--模型评估)
5. [Act V · 教育提议：从实验到 Colab 课程](#act-v--教育提议)
6. [PPT Slides 内容速查](#ppt-slides-内容速查)
7. [参考文献 Reference List](#参考文献-reference-list)

---

## Act I · 数据选择

### 1.1 为什么选这两个资产？

| | Apple (AAPL) | Bitcoin (BTC/USDT) |
|---|---|---|
| **市场类型** | 传统股票市场，按交易所日历交易 | 加密货币现货市场，24/7 全天候 |
| **数据来源** | StockAnalysis API — `GET /api/symbol/s/aapl/history` | Binance REST API — `GET /api/v3/klines`，Symbol: `BTCUSDT` |
| **Provider 代码** | `src/int4096/data/providers.py`（symbol: `aapl`） | `src/int4096/data/providers.py`（symbol: `BTCUSDT`） |
| **数据卡片** | `docs/research/data_cards/aapl_dataset_card.md` | `docs/research/data_cards/btc_dataset_card.md` |
| **可复现性** | API 公开，响应按日期下载，SHA-256 哈希存档 | Binance 官方 REST API，历史 K 线免注册可访问，SHA-256 哈希存档 |
| **时区** | 美东时间交易时段（NASDAQ 日历） | UTC 日线 |

**选择理由（供老师/答辩时阐述）：**

1. **对比微观结构**：AAPL 有周末休市、节假日休市；BTC 无休。同一套实验协议在两种日历下运行，让学生理解"下一个交易日"不能想当然地定义为"明天"。
2. **学生熟悉度**：AAPL 和 Bitcoin 是高中/大学新生最能在新闻里看到的金融资产，降低领域门槛。
3. **价格量级差异大**：AAPL 单价约 \$200–230，BTC 约 \$30,000–100,000+，能检验模型对绝对价格量级的适应性。
4. **体现 EMH 语境**：Fama (1970) 有效市场假说认为市场价格已充分反映所有信息，因此使用经典 ML 在短期预测上只能期待有限提升——这正是课程要传达的核心观点。

### 1.2 数据的时间范围

| 资产 | 总样本量 | 训练集 (60%) | 验证集 (20%) | 测试集 (20%, 封存) |
|---|---|---|---|---|
| AAPL | **1,255** 个交易日 | 2021-12-10 → 2024-11-08 | 2024-11-12 → 2025-11-03 | 2025-11-05 → 2026-10-27 |
| BTC | **1,828** 个日线 | 2021-11-27 → 2024-11-07 | 2024-11-09 → 2025-11-01 | 2025-11-03 → 2026-10-28 |

> [!IMPORTANT]
> **测试集目前完全封存，所有展示数字均为验证集结果。**
> - `run.py` 中 `allow_test: bool = False`（默认关闭），需显式传 `--allow-test` 才会解封
> - registry.jsonl 中 20 次实验的 `test_mae` 全部为 `null`，每个 manifest 均记录 `"test set sealed: no test metrics produced in this run"`
> - 决策日志 `docs/research/decision_log.md` D7 状态：**Pending human approval**
> - Moodle 检查单 `docs/handoff/moodle_checklist.md:82` 明确标注：**DELIBERATELY NOT DONE**
> - 教学 Notebook 明确注释：*"It does not unblind the test block."*

### 1.3 数据中的噪声问题及处理

原始数据存在以下问题，均由自动检查脚本标记：

| 噪声类型 | 具体表现 | 处理方式 |
|---|---|---|
| **重复时间戳** | 同一日期出现两条记录 | 保留第一条，标记并记录 |
| **缺失字段** | OHLCV 中某列为 NaN | 检查后剔除或前向填充（视情况） |
| **无效价格/成交量** | 价格为负数或成交量为零 | 自动标记，人工确认后剔除 |
| **BTC 日历连续性** | 无休市，但某些聚合器可能有空缺 | 以 Binance 官方源为准，不补插 |

---

## Act II · 数据处理

### 2.1 核心设计原则：只使用"当时可见"的信息

所有特征的计算窗口必须**截止于当前收盘**，不得使用未来数据。检验方法：

> 在原始序列末尾追加几行"离谱的未来价格"，重新计算特征——已存在日期的所有特征值应保持完全不变。

### 2.2 特征工程：10 个输入特征

所有五个模型在 AAPL 和 BTC 上使用**完全相同的 10 个特征**：

```
特征群组           具体构造方式                              数量
─────────────────────────────────────────────────────────
Returns（收益率）  1期、5期、20期的收盘价百分比变化          3
MA Gap（均线距离） 与5期、20期移动均线的百分比偏差           2
Volatility（波动率）10期、30期的1期收益率标准差             2
Price Range（价格区间）当日(high - low) / close            1
Relative Volume（相对成交量）与5期平均成交量的百分比偏差   1
Calendar（日历）   星期几（Monday=0）                       1
─────────────────────────────────────────────────────────
合计                                                       10
```

> [!TIP]
> 特征全部使用**相对量**（百分比变化、比率、标准化距离），使同一套特征能跨 AAPL（\$200 量级）和 BTC（\$60,000+ 量级）复用，无需按资产调整。

### 2.3 目标变量的设计：预测"变化量"而非"价格"

早期方案直接预测 $\hat{P}_{t+1}$（次日收盘价绝对值），但相对特征无法为模型提供可靠的价格水平锚点。  
**改进设计**：

$$
\underbrace{\hat{P}_{t+1}}_{\text{预测收盘价}}
=
\underbrace{P_t}_{\text{已知收盘价（锚点）}}
+
\underbrace{\widehat{\Delta P}_{t+1}}_{\text{模型预测的变化量}}
$$

**真实示例（AAPL 验证集，2024-11-21）：**
- 当日收盘：\$228.52
- 模型预测变化：+\$0.10
- 预测价格：\$228.62
- 实际收盘：\$229.87，误差 \$1.25

**Naive Persistence 基线**（最简单规则）：令 $\widehat{\Delta P} = 0$，即 $\hat{P}_{t+1} = P_t$。

### 2.4 数据切割与防泄露设计

```mermaid
flowchart LR
    A["Train 60%\n(2021 → 2024-11)"]
    B["Drop 1 row\n边界清洗"]
    C["Validate 20%\n(2024-11 → 2025-11)"]
    D["Drop 1 row\n边界清洗"]
    E["Test 20% 🔒\n(封存)"]
    A --> B --> C --> D --> E
```

**为什么要在边界删除一行？**  
设最后一条训练样本是周五，其标签（目标变量）是下一期（周一）的收盘价。若周一已是验证集的第一行，则这条训练标签实际上携带了验证集的信息——即**标签泄露**。在每个边界删除一行可完全杜绝这种情况。

### 2.5 防止预处理泄露：Fit-on-Train-Only

标准化（StandardScaler）的均值和方差**只在训练集上计算**，然后应用到验证/测试集：

- **P0（Preprocessing variant 0）**：保留原始特征值，不做标准化
- **P2（Preprocessing variant 2）**：使用训练集统计量标准化所有特征

### 2.6 泄露检测：Mutation Testing（变异测试）

我们故意注入 **6 种泄露缺陷**，测试套件必须全部检出：

| # | 泄露类型 | 注入方式 |
|---|---|---|
| 1 | 单步前视 | 特征向未来移动一期 |
| 2 | 混淆前视 | 特征与目标混合计算 |
| 3 | 中心化窗口 | 滚动窗口用未来数据对称 |
| 4 | 向后填充 | NaN 用未来值填充 |
| 5 | 全序列统计量 | 用整个序列均值标准化 |
| 6 | 预处理跨集 | StandardScaler 拟合在 train+test 上 |

> [!CAUTION]
> 在早期版本中，测试套件**未能**检出所有 6 种缺陷，导致我们重新设计了整个检测框架。扰动一个测试集价格可使基准指标偏移 **0.408**（LeakDelta），远超任何模型的实际提升幅度。

---

## Act III · 训练阶段

### 3.1 模型选择理由

| 模型 | 类别 | 选择理由（教育视角） |
|---|---|---|
| **Linear Regression**（近无正则化）| 线性模型 | 最简单的基础，权重可直接解释 |
| **Ridge Regression**（L2 正则）| 线性模型 | 展示正则化如何约束过拟合 |
| **SVR (RBF kernel)** | 核方法 | 展示距离度量对特征缩放的敏感性 |
| **Random Forest** | 集成树方法 | 展示树模型对缩放不敏感的性质 |
| **Hist. Gradient Boosting** | 集成梯度提升 | 展示 boosting 与 bagging 的区别 |

> [!NOTE]
> 选择经典 ML 而非深度学习的原因：经典模型族的决策机制更透明，学生可以对比"为什么 SVR 受缩放影响而随机森林不受"，这正是教育目标所在。

### 3.2 训练协议（统一搜索预算）

每个模型-资产-预处理组合（共 20 个）使用**相同的超参数搜索预算**：

| 参数 | 实际用量 | 协议上限 |
|---|---|---|
| 随机搜索轮数 | 10 次 | 24 次 |
| 每轮时间上限 | 90 秒 | 300 秒 |
| 随机种子 | 固定（相同） | — |

**每次运行记录：**
- Run ID、Git commit hash、数据集 SHA-256
- 协议版本、配置哈希
- 超参数及每次搜索的结果
- 指标、artifacts 和错误日志（失败的运行不删除）

### 3.3 Fine-tuning 过程

超参数搜索在**验证集 MAE** 上评估。每个模型家族的搜索空间：

- **Linear/Ridge**：正则化强度 `alpha` 在对数空间搜索
- **SVR**：`C`（惩罚系数）、`epsilon`（不敏感带）、RBF `gamma`
- **Random Forest**：树的数量、最大深度、最小分裂样本数
- **Hist. Gradient Boosting**：学习率、最大迭代次数、叶节点数

---

## Act IV · 模型评估

### 4.1 评估指标体系

| 指标 | 公式 | 作用 |
|---|---|---|
| **MAE**（平均绝对误差）| $\frac{1}{n}\sum|y_i - \hat{y}_i|$ | 以价格单位衡量典型误差大小 |
| **Skill Score** | $1 - \frac{\text{Model MAE}}{\text{Persistence MAE}}$ | 相对于最简单基线的提升百分比 |
| **R²** | $1 - \frac{\text{SS}_{res}}{\text{SS}_{tot}}$ | 课程开场"高分陷阱"的说明工具 |
| **Bootstrap CI** | 移动区块 Bootstrap，区块大小=10，重采样=1,000次 | 量化技能分数的不确定性 |

> [!IMPORTANT]
> **R² 是陷阱指标**：Naive Persistence（$\hat{P}_{t+1} = P_t$）在 AAPL 验证集上的 R² = **0.9555**，而最优 SVR 模型的 R² = **0.9556**，仅差 0.0001。这就是为什么我们用 Skill Score 而非 R² 做最终排名。

### 4.2 完整结果：20 次实验的 Skill Score 矩阵（%）

|  | AAPL P0 | AAPL P2 | BTC P0 | BTC P2 |
|---|:---:|:---:|:---:|:---:|
| **Linear (near-unregularised)** | +0.24 | -0.50 | **+0.26** | +0.05 |
| **Ridge** | +0.25 | +0.29 | +0.15 | +0.12 |
| **SVR (RBF)** | +0.51 | **+0.52** | +0.01 | +0.08 |
| **Random Forest** | -0.78 | -0.78 | +0.06 | +0.06 |
| **Hist. Gradient Boosting** | +0.25 | +0.25 | -0.04 | -0.04 |
| **Naive Persistence** | 0.00 | 0.00 | 0.00 | 0.00 |

**关键发现：**
- 20 次运行中，5 次输给了 Persistence 基线
- AAPL 最优：SVR P2，Skill = **+0.52%**（每次预测节省约 1.5 美分）
- BTC 最优：Linear P0，Skill = **+0.26%**
- 技能分数范围：-0.78% 到 +0.52%，总跨度 1.30%

### 4.3 模型鲁棒性：Bootstrap 置信区间

**方法**：移动区块 Bootstrap（Moving-Block Bootstrap）
- **区块大小**：10 个连续观测（保留相邻误差的相关性）
- **重采样次数**：1,000 次
- **置信水平**：95%

**结论**：**全部 20 个置信区间均包含零**，包括表现最好的 AAPL SVR P2。

> 这说明在现有验证数据上，没有任何模型能可靠地声称超越 Naive Persistence。观测到的正技能分数可能仅来自随机波动。

### 4.4 缩放敏感性分析（Ablation Study）

| 模型族 | 缩放影响 | 原因 |
|---|---|---|
| **Random Forest** | 完全无影响（$\Delta$MAE = 0.00） | 树的分裂基于排序，不依赖绝对数值 |
| **Hist. Gradient Boosting** | 完全无影响（$\Delta$MAE = 0.00） | 同上 |
| **SVR** | 有轻微变化 | RBF 核依赖特征间欧氏距离 |
| **Ridge** | 有轻微变化 | L2 惩罚项依赖系数量级 |
| **Linear** | AAPL 上 MAE 升高 +0.74% | 近无正则化，缩放后数值范围变化影响优化路径 |

### 4.5 信号诊断：收益率自相关检验

相邻期收益率的相关性（Lag-1 autocorrelation）：
- AAPL：**+0.021**（$R^2$ = 0.0005）
- BTC：**-0.026**（$R^2$ = 0.0007）

两者均接近零，说明上一期收益对下一期几乎无预测力。这解释了为什么模型提升空间有限——与 Fama (1970) EMH 一致。

### 4.6 特征重要性（以 AAPL Ridge 为例）

使用**排列重要性（Permutation Importance）**：打乱某一特征，衡量验证误差增量。
- 短期收益率（1期、5期）和短期波动率主导
- 各特征的重要性量级均很小（与技能分数一致）
- **重要：特征重要性 ≠ 因果关系**

---

## Act V · 教育提议

### 5.1 教育目标

> 让高中高年级和大学一年级学生在看到"某模型达到 95.56% 准确率"时，知道要追问三件事：
> 1. 模型预测时能看到哪些信息？
> 2. 最简单的规则在同样数据上能达到多少？
> 3. 这个提升有多确定？

### 5.2 Colab 课程设计（60 分钟）

| 环节 | 内容 | 时长 |
|---|---|---|
| 引入 | 展示"高分陷阱"，对比 SVR R² 和 Persistence R² | 10 min |
| Task 1 | 学生预测 Naive Persistence 在验证集上的表现 | 10 min |
| Task 2 | 学生识别一个含前视的特征，解释为何非法 | 10 min |
| Task 3 | 学生重跑一个模型，记录 Skill Score | 10 min |
| Task 4 | 学生解读 Bootstrap 置信区间 | 10 min |
| Task 5 | 学生将上述框架迁移到另一个领域（如预测出勤率）| 10 min |

### 5.3 可复现性保证（供老师验证）

| 要素 | 实现方式 |
|---|---|
| 数据版本锁定 | 数据集 SHA-256 哈希，存于 manifest |
| 代码版本 | Git commit hash 随每次运行记录 |
| 自动化测试 | 83 项测试全部通过（含 6 种泄露注入测试） |
| 配置哈希 | 每次运行的超参数配置有唯一哈希，防止静默修改 |

### 5.4 学生可在 Colab 中完成的操作

- 从零构建 Naive Persistence 基线
- 重跑任意模型并追溯数字来源
- 故意插入前视特征，观察指标变化
- 解释为什么两个模型对标准化反应不同

---

## PPT Slides 内容速查

> [!NOTE]
> 下表对应 `slides/latex/main.tex` 中的 16 张主要幻灯片，可直接用作 PPT 大纲确认。

| Slide # | 标题 | 主讲人 | 核心内容点 |
|---|---|---|---|
| 1 | Learning ML Through Financial Forecasting | Lau Pak Hei | SVR R²=0.9556 vs Persistence R²=0.9555 ← 开场钩子 |
| 2 | What Should Learners Ask About an AI Score? | Zhang Haoyu | 三个问题框架；目标受众 |
| 3 | Two Datasets Test the Same Protocol | Dong Yuankun | AAPL vs BTC，1,255 vs 1,828 条，来源 |
| 4 | Every Forecast Starts at the Same Time | Zhang Haoyu | 预测时刻定义；信息边界 |
| 5 | One Comparison for Every Model | Zhang Haoyu | 实验设计；20 次运行；统一预算 |
| 6 | Ten Inputs Use Only Available Information | Dong Yuankun | 10 个特征明细表 |
| 7 | Chronological Splits Keep the Future Out | Dong Yuankun | 60/20/20 切割；边界删行；6 种泄露检测 |
| 8 | Predicting the Change Gives Models a Clearer Task | Lau Pak Hei | $\hat{P}_{t+1} = P_t + \widehat{\Delta P}$；真实 AAPL 示例 |
| 9 | P0 and P2 Test the Effect of Scaling | Lau Pak Hei | P0/P2 定义；Skill Score 公式 |
| 10 | AAPL's Best Run Saved 1.5 Cents per Forecast | Zhang Yancheng | 完整结果图；SVR +0.52%；5 次输给基线 |
| 11 | All 20 Bootstrap Intervals Included Zero | Zhang Yancheng | Bootstrap CI 图；区块=10；重采=1,000 |
| 12 | Scaling Changed Some Models and Left Trees Unchanged | Zhang Yancheng | Ablation 图；树模型 Δ=0；线性 +0.74% |
| 13 | Price Levels and Daily Changes Tell Different Stories | Zhang Yancheng | Lag-1 相关近零；R² 陷阱解释 |
| 14 | Why Smart Models Still Lose to a Simple Rule | Zhang Yancheng | 课堂提问互动；60 分钟 Colab 课 |
| 15 | Learners Can Reproduce and Challenge the Result | Dong Yuankun | 83 项测试；可复现代码；学生任务 |
| 16 | The Skill Students Can Take to Any AI Claim | Lui Shing Lam | 三步框架迁移；课堂试教提议 |

---

## 参考文献 Reference List

> 以下文献来自 `reports/latex/references.bib`，分为两组，对应 PPT 最后两张 Reference 页。

### 模型与软件

| 编号 | 引用 | 链接 |
|---|---|---|
| [1] | Pedregosa et al. (2011). **Scikit-learn: Machine Learning in Python**. *JMLR*, 12, 2825–2830. | [https://jmlr.org/papers/v12/pedregosa11a.html](https://jmlr.org/papers/v12/pedregosa11a.html) |
| [2] | Hastie, Tibshirani & Friedman (2009). **The Elements of Statistical Learning** (2nd ed.). Springer. | [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/) |
| [3] | Breiman (2001). **Random Forests**. *Machine Learning*, 45(1), 5–32. | [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324) |
| [4] | Drucker et al. (1997). **Support Vector Regression Machines**. *NIPS*, 9, 155–161. | [https://papers.nips.cc/paper/1996/hash/d38901788c533e8286cb6400b40b386d-Abstract.html](https://papers.nips.cc/paper/1996/hash/d38901788c533e8286cb6400b40b386d-Abstract.html) |
| [5] | Friedman (2001). **Greedy Function Approximation: A Gradient Boosting Machine**. *Annals of Statistics*, 29(5), 1189–1232. | [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451) |
| [6] | Fisher, Rudin & Dominici (2019). **All Models are Wrong, but Many are Useful**. *JMLR*, 20(177), 1–81. | [https://jmlr.org/papers/v20/18-760.html](https://jmlr.org/papers/v20/18-760.html) |

### 预测、评估与课程材料

| 编号 | 引用 | 链接 |
|---|---|---|
| [7] | Bergmeir, Hyndman & Koo (2018). **A Note on the Validity of Cross-Validation for Evaluating Autoregressive Time Series Prediction**. *Computational Statistics & Data Analysis*, 120, 70–83. | [https://doi.org/10.1016/j.csda.2017.11.003](https://doi.org/10.1016/j.csda.2017.11.003) |
| [8] | Roberts et al. (2017). **Cross-validation Strategies for Data with Temporal, Spatial, Hierarchical, or Phylogenetic Structure**. *Ecography*, 40(8), 913–929. | [https://doi.org/10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881) |
| [9] | Kaufman, Rosset, Perlich & Stitelman (2012). **Leakage in Data Mining: Formulation, Detection, and Avoidance**. *ACM TKDD*, 6(4), 1–21. | [https://doi.org/10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579) |
| [10] | Makridakis, Spiliotis & Assimakopoulos (2018). **The M4 Competition: Results, Findings, Conclusion and Way Forward**. *International Journal of Forecasting*, 34(4), 802–808. | [https://doi.org/10.1016/j.ijforecast.2018.06.001](https://doi.org/10.1016/j.ijforecast.2018.06.001) |
| [11] | Fama (1970). **Efficient Capital Markets: A Review of Theory and Empirical Work**. *The Journal of Finance*, 25(2), 383–417. | [https://doi.org/10.2307/2325486](https://doi.org/10.2307/2325486) |
| [12] | Hyndman & Athanasopoulos (2021). **Forecasting: Principles and Practice** (3rd ed.). OTexts. | [https://otexts.com/fpp3/](https://otexts.com/fpp3/) |
| [13] | The Education University of Hong Kong (2026). **INT4096 Artificial Intelligence and Machine Learning in Education: Group Project Specification**. Course handout, Semester 1, 2026–27. | 课程内部材料 |

### 数据来源（供可复现性验证）

| 资产 | 来源 | 链接 |
|---|---|---|
| Apple (AAPL) | StockAnalysis.com API（`/api/symbol/s/aapl/history`），Symbol: `aapl` | [https://stockanalysis.com/api/symbol/s/aapl/history](https://stockanalysis.com/api/symbol/s/aapl/history) |
| Bitcoin (BTC/USDT) | Binance REST API，`/api/v3/klines`，Symbol: `BTCUSDT` | [https://api.binance.com/api/v3/klines](https://api.binance.com/api/v3/klines) |
| 数据提供者代码 | `src/int4096/data/providers.py` | — |
| AAPL 数据卡片 | `docs/research/data_cards/aapl_dataset_card.md` | — |
| BTC 数据卡片 | `docs/research/data_cards/btc_dataset_card.md` | — |
| Scikit-learn | PyPI / 官方文档 | [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/) |

---

*文档生成时间：2026-11-23 | INT4096 Group Project | The Education University of Hong Kong*
