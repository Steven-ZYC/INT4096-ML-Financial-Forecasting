# Feature Extraction Story（v3：按流水线五部分组织；事实部分沿用 v2 的逐条核实）
## INT4096 — Learning Machine Learning Through Financial Forecasting

> [!NOTE]
> 本文档是**演示材料的单一叙事来源**：`deliverables/presentation/slides/main.tex`、`deliverables/presentation/planning/*` 的结构、顺序和措辞都以此为准。
> **v3（2026-11-24）结构调整：** 按老师偏好"有逻辑、有体系、用最少时间讲透技术实现"，演示改为**一个部分对应流水线的一个阶段**：Part 1 数据选择 → Part 2 数据处理与特征工程 → Part 3 模型与调参 → Part 4 评估 → Part 5 教学设计（17 页正文，见附录 C）。下文各节的事实与证据不变；"Act I–V"即 Part 1–5。
> v2 相对 v1 做了三件事：① 按「三个问题」重新组织主线；② 逐条对照 `experiments/`、`configs/`、`src/`、`tests/` 核实，修正了 v1 中的事实错误（见附录 A）；③ 每一节都标明证据路径和"演示时该怎么说 / 不能怎么说"。
> 所有实验数字来自 `experiments/models/`（由 `scripts/build_slide_assets.py` 生成宏），不手填。
> 证据标签沿用 AGENTS.md：`[A]` 课程书面要求 · `[B]` 口头指引（学生转述）· `[C]` 团队决策（decision_log）· `[D]` 提案/未批准。

---

## 0. 一页总览

### 0.1 主线：一条流水线，五个部分，每部分回答一个问题

| Part | 要回答的问题 | 子问题（各一页） |
|---|---|---|
| 1 数据选择 | 用了什么数据、从哪来、为什么、哪些行合格？ | (a) 用了什么 + (b) 来源链接 → 第 3 页；(c) 为什么选这两个 → 第 4 页；(d) 筛选条件 → 第 5 页 |
| 2 数据处理与特征工程 | 原始数据有什么问题？模型能合法地看到什么？ | 第 6 页承接数据部分：发现六个问题，因时间只讲前三项（价格漂移、复权价事后修订、交易日历不同），其余三项写在稿里备用；十个特征（第 7 页）；目标变量（第 8 页）；切分与泄漏检验（第 9 页） |
| 3 模型与调参 | 用哪些模型、为什么、怎样公平地调参？ | 模型与理由（第 10 页）；调参流程与选中值（第 11 页）；超参数之外的探索（第 12 页） |
| 4 评估 | 用什么指标、结果如何、有多确定？ | 四个指标（第 13 页）；20 次结果（第 14 页）；Bootstrap 与原因（第 15 页） |
| 5 教学设计 | 项目怎样变成一节课？ | 任务↔阶段↔课程概念（第 16 页）；分阶段总结（第 17 页） |

原先的"三个问题"（能看到什么 / 简单规则多好 / 有多确定）仍然是教学目标，体现在 Part 2、Part 4 和第 16 页的任务里，不再作为演示的骨架。

### 0.2 五部分结论速查

| 部分 | 一句话结论 | 核心证据 |
|---|---|---|
| Opening | 验证集 R²：SVR **0.9556** vs 复制昨日收盘 **0.9555**——高分不说明学到东西 | `experiments/models/*_aapl_svr_P2_*/metrics.json` |
| I 数据 | 两个结构不同的市场（AAPL 交易时段 / BTC 24×7），同一套协议 | `data/raw/*.manifest.json`、`data/cards/` |
| II 处理 | 10 个只看过去的相对特征；预测"变化量"；按时间切分并在边界各删 1 行；6 种泄漏缺陷全被抓到 | `docs/research/feature_dictionary.md`、`tests/test_temporal_integrity.py`、`scripts/mutation_check.py` |
| III 训练 | 5 个模型族，**同一预算**（10 次随机搜索 / 每格 ≤90 秒），调参只在训练块内部做 | `configs/research_protocol.yaml`、`src/int4096/experiments/{run,tuning}.py` |
| IV 评估 | 20 次运行技能分数在 −0.78% 到 +0.52%；5/20 输给基线；**20/20 区间含 0** | `docs/research/run_registry.md`、`experiments/analysis/uncertainty_and_signal.json` |
| V 教育 | 60 分钟 Colab 课 + 教师指南；**没有做学习者实验，不声称学习增益** | `deliverables/notebook/`、`deliverables/lesson/` |

**英文一句话（用于开场/结尾）：** *Five classical models, one free rule, two markets: no model reliably beat "tomorrow equals today".*

> [!IMPORTANT]
> **测试集仍然封存。** 所有**模型表现**数字都来自验证集。
> - `run.py` 中 `allow_test: bool = False`；`registry.jsonl` 里 20 条记录 `test_mae` 全为 `null`（已核实 0/20 非空）
> - 决策 D7 状态 **Pending human approval**；`docs/project/moodle_checklist.md:82` 标注 **DELIBERATELY NOT DONE**
> - **精确措辞（重要）：** 只有两个**描述性**统计量用到了含封存期的完整价格序列——数据集规模/价格范围，以及收益率自相关（见 4.5 和附录 B-1）。所以演示中不能说"本次演示的每一个数字都来自验证集"，应说"**每一个模型表现数字**都来自验证集"。

---

## Act I · 数据选择：我们挑了什么、为什么

### 1.1 两个资产，同一套协议

| | Apple (AAPL) | Bitcoin (BTC/USDT) |
|---|---|---|
| 市场类型 | 股票，按交易所日历（周末/节假日休市） | 加密现货，24×7 |
| 来源 | StockAnalysis 公开历史接口 `/api/symbol/s/aapl/history` | Binance REST `/api/v3/klines`，`BTCUSDT`，日线 |
| 币种 / 时区 | USD；美东收盘 | USDT；UTC 日线 |
| 窗口 | 2021-10-28 → 2026-10-28 | 2021-10-28 → 2026-10-29 |
| 观测数 | **1,255** | **1,828** |
| 收盘价范围（全窗口） | 约 125 – 348 USD | 约 15,781 – 124,659 USDT |
| 数据卡片 | `data/cards/aapl_dataset_card.md` | `data/cards/btc_dataset_card.md` |

**为什么是这两个（演示用）：**
1. **对比日历结构**：同一套协议在"有休市"和"无休市"两种日历下运行，让学生看到"下一个交易日"≠"明天"。
2. **稳健性检验**：只在一种市场结构里成立的结论，不是关于机器学习的结论。
3. **价格量级差异大**（约 $10² vs $10⁴–10⁵）：所以跨资产只能比**无单位**指标（技能分数），不能比美元误差。
4. **学生熟悉**，降低领域门槛；并给 EMH（Fama 1970）语境：短期预测空间本来就有限。

**必须如实说明的限定（decision D3 要求出现在材料中）：**
- BTC 是 **Binance 单一交易所**的 USDT 计价序列，不是全球指数，USDT ≠ USD。
- AAPL 的标签用**原始收盘价**而非复权价（D1）：复权因子会被事后修订，用它会给"当时"的特征带入未来信息。窗口内已检查无拆股断点。BTC 无复权。

> [!WARNING]
> v1 写的"AAPL 约 $200–230、BTC 约 $30,000–100,000+"**不正确**（实际范围见上表；验证期内 AAPL 172–271，BTC 约 76k–125k）。

### 1.2 样本量、窗口与封存

原始观测 → 建模行：AAPL 1,255 → **1,224**，BTC 1,828 → **1,797**（各丢 30 行用于 30 期回看窗口预热，再丢 1 行终端行——它没有可观测的 t+1 标签；数据卡片 §6）。

| 资产 | 训练 60% | 验证 20% | 测试 20%（封存） | 验证样本数 |
|---|---|---|---|---|
| AAPL | 2021-12-10 → 2024-11-08 | 2024-11-12 → 2025-11-03 | 2025-11-05 → 2026-10-27 | **244** |
| BTC | 2021-11-27 → 2024-11-07 | 2024-11-09 → 2025-11-01 | 2025-11-03 → 2026-10-28 | **358** |

> **为什么要强调验证样本数：** 所有结论只基于 244 / 358 个样本，这直接决定 Bootstrap 区间有多宽（见 4.3）。测试期日期由切分规则算出，测试期**数据**未被读取用于任何模型指标。

### 1.3 数据质量闸门：**拒绝，而不是修补**

> v1 写成"重复→保留第一条、缺失→前向填充、异常→人工确认后剔除"。**代码不是这样做的。**

- `src/int4096/data/load.py`：遇到**重复时间戳或乱序直接抛错**（"a duplicate session would corrupt the label shift"）。
- `src/int4096/data/validate.py`：检查重复、缺失核心列/值、非正价格、`high<low`、收盘价超出 [low, high]、负成交量。
- **结果：两个快照全部 PASS，0 行被标记**；不存在需要"清洗"的行。每个快照有 SHA-256，运行前重新校验，不一致则报错（LEAK-003）。
- 这条设计原则值得讲：**数据有问题时，让流水线失败，而不是悄悄修补**——悄悄修补本身就是一种泄漏/偏差来源。

---

## Act II · 数据处理：只使用"当时可见"的信息

### 2.1 核心原则与检验方法

每个特征的窗口**截止于当日收盘**。检验：在原始序列末尾追加离谱的未来价格，重算特征——已有日期的特征必须逐位不变（`tests/test_temporal_integrity.py`）。

### 2.2 十个特征（全部在 `bars ≤ t` 上计算）

| 特征组 | 构造 | 个数 |
|---|---|---|
| Returns | 收盘价 1、5、20 期百分比变化（`ret_1/5/20`） | 3 |
| MA gap | 与 5、20 期**尾部**均线的百分比偏差（`ma_gap_5/20`） | 2 |
| Volatility | 1 期收益率的 10、30 期**尾部**标准差（`vol_10/30`） | 2 |
| Price range | (high − low)/close（`range_1`） | 1 |
| Relative volume | 成交量相对 5 期均量的偏差（`vol_chg`） | 1 |
| Calendar | 星期几，周一 = 0（`dow`） | 1 |

五个模型、两个资产、P0/P2 **用同一套 10 个特征**。除 `dow` 外全部是相对量，**没有价格水平特征**——这是 2.3 必须预测"变化量"的原因。

### 2.3 目标变量：预测变化量，再加回已知价格

$$\widehat{P}_{t+1} \;=\; P_t \;+\; \widehat{\Delta P}_{t+1}$$

- **为什么：** 特征全是比率，模型无法从中恢复价格水平。
- **这是被一次失败逼出来的设计（decision D8）：** 第一次真实 AAPL 运行直接拟合价格水平，Ridge 的技能分数约 −18.3、R² 约 −7.4。调查发现这是**表示方式的假象**（预测值塌向训练均值），不是模型失败。改成预测变化量后，被评估的问题不变——仍然是"下一收盘价"的误差，因为 $P_t$ 在决策时已知。
- **真实样本（AAPL 验证集，决策日 2024-11-21）：** 收盘 228.52 → 预测变化 +0.10 → 预测 228.62 → 次日实际 229.87，误差 1.25（同一天持续性规则误差 1.35）。
- **持续性基线** = 令 $\widehat{\Delta P}=0$。
- ⚠ **D8 的状态是"provisionally accepted，requires human approval"**——这是你们最需要尽快签字的决策（README 也这么写）。

### 2.4 切分与边界清洗

```mermaid
flowchart LR
    A["Train 60%"] --> B["purge 1 row"] --> C["Validate 20%"] --> D["purge 1 row"] --> E["Test 20% 🔒 sealed"]
```

- 标签是 $\text{Close}_{t+1}$：训练块最后一行的标签 = 验证块第一个价格；验证块最后一行的标签 = **封存测试期的价格**。不删边界行，就是**标签泄漏**——不会报错，分数悄悄变好。
- 审计复现（LEAK-001）：扰动**一个**封存测试价格，验证集头条指标移动 **0.408**（约为模型相对持续性优势的 46 倍）。修复：`purge_gap: 1`，两个边界都应用。
- 防过拟合到验证集：超参数搜索**不看验证块**（见 3.3）。

### 2.5 预处理：只在训练行上拟合

- **P0**：特征保持原值（流水线里有训练集拟合的中位数填补，但快照没有缺失值，所以是空操作）。
- **P2**：`StandardScaler` 仅在训练索引上拟合，再应用到验证期。
- 协议还定义了 P1、P3、P4，但**当前只运行 P0 与 P2**：P1 因"无缺失值"被登记为 `NOT_RUN`（D13，避免发布一个与 P0 逐字节相同的重复结果）；P3/P4 尚未运行（README "Known gaps"）。被问到"为什么只有 P0/P2"时如实回答。

### 2.6 泄漏防线：审计 → 变异测试

**真实经过（比 v1 讲得更有说服力）：**
1. 独立审计员第一次判 **FAIL**（2 HIGH）：边界没删行；并且测试套件**检测不出**一步前视 `shift(-1)` 和 `bfill`——两个变异在 17 个测试里全部"通过"。
2. 修复后重写测试（在测试里用尾部公式独立重算每个特征），并写了 `scripts/mutation_check.py`：**故意注入缺陷，测试必须失败**。
3. 现在的变异集是 **6 种**（脚本中已核实）：

| # | 注入的缺陷 |
|---|---|
| 1 | 特征读取下一根 K 线 `shift(-1)` |
| 2 | **伪装**的一步前视 `periods=-1`（换写法，仍要被抓到） |
| 3 | 居中滚动窗口 `center=True` |
| 4 | 缺失值**后向**填充 `bfill` |
| 5 | 用整段序列的统计量代替尾部窗口 |
| 6 | 预处理在 train+apply 行上拟合 |

> v1 把第 2 项写成"特征与目标混合计算"，**不准确**；`docs/quality/leakage_audit.md` 里的"5 种"是较早版本，脚本现为 6 种。变异测试是**独立脚本**，不属于 pytest 的 83 项。

---

## Act III · 训练：同样的机会，同样的规则

### 3.1 五个模型：选"机制差异"，不是凑数量

| 模型 | 机制 | 教学理由 |
|---|---|---|
| Linear baseline | 线性 + L2（见下方说明） | 权重可解释，最简单的学习型对照 |
| Ridge | 线性 + 更强的 L2 搜索范围 | 正则化如何约束拟合 |
| SVR (RBF) | 核方法：基于样本相似度 | 距离度量 → 对特征缩放敏感 |
| Random Forest | bagging 的树集成 | 树按阈值切分 → 对单调缩放不变 |
| Hist. Gradient Boosting | 顺序拟合残差的树集成 | boosting 与 bagging 的区别 |

不用深度学习：课程讲义不鼓励；MLP 车道存在但被 `REQUIRES_OWNER_APPROVAL` 关闭（D2，口头指引属 `[B]`，不能说成"规则变了"）。

> [!WARNING]
> **"Linear (near-unregularised)" 这个名字有误导性。** 代码里它是 `Ridge(alpha=…)`，搜索网格 `alpha ∈ {0.1, 1, 10}`，实际选中 **10**；而 Ridge 的网格是 `{0.01 … 1000}`，选中 **1000**（网格上限）。所以它不是"近似普通最小二乘"。v2 起统一叫 **Linear baseline**，`build_slide_assets.py` 的标签已改。

### 3.2 统一预算（v1 把"每轮"写错了）

| 项 | 实际 | 协议上限 |
|---|---|---|
| 随机搜索试验数 | **10** | 24 |
| 时间上限 | **90 秒 / 每个模型-资产-预处理格子（整个搜索）** | 300 |
| 随机种子 | 42，全部相同 | — |

> v1 写"每轮时间上限 90 秒"。`tuning.py` 里 `max_seconds` 是**整个搜索**的上限，不是单次试验的。

每次运行记录：run ID、git commit、数据集 SHA-256、协议版本、配置哈希、超参数、每次尝试；**失败运行不删除**（追加式 registry，20/20 SUCCESS）。

### 3.3 调参流程（v1 写成"在验证集 MAE 上评估"——**错误**）

- 实际是**训练块内部**的 5 折**扩展窗口**交叉验证（`gap=1`，首折至少占训练块 30%），目标是 MAE。
- **验证块完全不参与调参**，只用来报告结果。这比"在 train+validation 上调参"更保守（审计 LEAK-004 已把协议文字改成与代码一致）。
- 搜索空间是**离散网格**上的随机抽样（不是对数空间连续搜索）：

| 模型 | 网格 |
|---|---|
| Linear baseline | `alpha ∈ {0.1, 1, 10}` |
| Ridge | `alpha ∈ {0.01, 0.1, 1, 10, 100, 1000}` |
| SVR | `C ∈ {0.1…1000}`、`epsilon ∈ {0.001, 0.01, 0.1}`、`gamma ∈ {scale, 0.001, 0.01, 0.1}` |
| Random Forest | `n_estimators ∈ {100, 200}`、`max_depth ∈ {None, 4, 8, 16}`、`min_samples_leaf ∈ {1, 5, 20}` |
| Hist. GB | `learning_rate ∈ {0.01, 0.05, 0.1}`、`max_iter ∈ {100, 300}`、`max_depth ∈ {None, 3, 5}`、`min_samples_leaf ∈ {5, 20, 50}` |

> **老实话（可放进 Q&A）：** 好几个选中值落在网格边缘——Ridge `alpha=1000`（上限）、AAPL 的 SVR `C=0.1`（下限）、`epsilon=0.1`（上限）。这提示网格可能偏窄；但这不改变"没有明显优势"的结论方向，只是意味着我们没有把每个模型都调到极致。

---

## Act IV · 评估：准确度、不确定性、与"为什么"

### 4.1 指标与 R² 陷阱

| 指标 | 作用 |
|---|---|
| MAE | 以价格单位衡量典型误差（**AAPL 与 BTC 的 MAE 不可直接比较**） |
| **Skill** = 1 − MAE_model / MAE_naive | 相对"复制昨日收盘"的提升；0 = 一样好，负 = 更差；无单位，可跨资产 |
| R² | 展示"高分陷阱"的工具，**不用于排名** |
| Moving-block bootstrap | 块长 10、重采样 1,000、95%；按日期配对 |

**陷阱：** AAPL 验证集 R²——持续性 **0.9555**，SVR **0.9556**，差 0.0001。价格水平本身高度自相关，所以任何"贴着价格走"的预测 R² 都很高。

### 4.2 20 次运行的技能分数矩阵（%，验证集）

|  | AAPL P0 | AAPL P2 | BTC P0 | BTC P2 |
|---|:---:|:---:|:---:|:---:|
| Linear baseline | +0.24 | −0.50 | **+0.26** | +0.05 |
| Ridge | +0.25 | +0.29 | +0.15 | +0.12 |
| SVR (RBF) | +0.51 | **+0.52** | +0.01 | +0.08 |
| Random Forest | −0.78 | −0.78 | +0.06 | +0.06 |
| Hist. GB | +0.25 | +0.25 | −0.04 | −0.04 |
| Naive persistence | 0 | 0 | 0 | 0 |

（已与 `experiments/models/registry.jsonl` 逐格核对一致。）

- **5/20** 输给基线（AAPL：Linear-P2、RF-P0、RF-P2；BTC：HGB-P0、HGB-P2）；P2 的 10 个里有 **3** 个。
- AAPL 最好：SVR-P2 **+0.52%**，相当于平均绝对误差少约 **1.5 美分**（2.9056 → 2.8904）；BTC 最好：Linear-P0 **+0.26%**。
- 范围 −0.78% … +0.52%，跨度 1.30 个百分点。
- 措辞纪律：说"**有些配置略好**"，不说"赢了"，也不说"从来没用"。

### 4.3 Bootstrap：全部 20 个区间包含 0

- 配对 + 移动区块（块长 10 保留相邻误差相关性）+ 1,000 次 + 95%。
- **20/20 区间跨过 0**，包括最好的 AAPL SVR-P2。结论：**与基线打平，不是"有赢家"**。
- 图注自带的限定要保留：区间是 *indicative, not confirmatory*；只有 244/358 个验证样本。

### 4.4 缩放消融：P0 vs P2

| 模型 | 现象 | 正确的解释 |
|---|---|---|
| Random Forest、HGB | 预测**逐位相同**（最大差 0） | 树按单个特征的阈值切分，单调缩放后存在等价阈值 |
| SVR | 小幅变化 | RBF 核用跨特征的距离，缩放改变哪个特征占主导 |
| Ridge / Linear | 小幅变化；AAPL Linear 的 MAE **+0.74%（变差）** | **L2 惩罚的有效强度取决于特征尺度** |

> [!WARNING]
> v1 把 Linear 变差解释为"近无正则化，缩放后数值范围变化影响优化路径"——**不对**。该模型是带 α 的 Ridge，闭式求解，没有"优化路径"。我复现了该运行：同样 α=10，P0 的预测几乎是个常数（预测标准差 0.07），P2 的预测波动大得多（0.26）且更差。这是**脆弱性**的例子，**不是**"标准化能提升"的证据。核心信息：*预处理会改变行为，不等于改善预测。*

### 4.5 信号诊断：收益率自相关

| | lag-1 自相关 | R² |
|---|---|---|
| AAPL | **+0.021** | 0.0005 |
| BTC | **−0.026** | 0.0007 |

- 来源 `experiments/analysis/uncertainty_and_signal.json`（n = 1,254 / 1,827）。
- **这是一个只探测"一种信号"的诊断**，不能推出"没有信号"。它对应的合理说法："昨天的收益几乎解释不了今天的收益，所以日度尺度上能学的东西很少"。
- ⚠ **范围问题（见附录 B-1）**：n=1,254/1,827 说明它是用**完整序列（含封存测试期）**算的，虽然只是描述性统计，也与 AGENTS.md "不得查看封存测试集" 的精神有出入。我用训练期、验证期分别重算：AAPL 训练 +0.016、验证 +0.035；BTC 训练 −0.019、验证 −0.063（验证期 n=358，标准误约 0.05，仍在噪声内）。结论方向不变，但建议用"训练+验证"重算后替换。

### 4.6 特征重要性（AAPL Ridge，置换重要性，验证期 n=244）

- 排序：`ret_1` ≈ `ret_5` > `vol_30` > `ma_gap_20` ≫ 其余；`vol_chg` 为负（无帮助）。
- v1 写"短期收益率和**短期波动率**主导"——`vol_30` 是**较长**的波动窗口，已更正。
- 重要性只描述**拟合出的模型**如何依赖特征，**≠ 因果**，且量级很小（与技能分数一致）。

### 4.7 演示口径：讲优势，守住事实

演示稿（幻灯片+口播）只讲"我们做了什么、做得好在哪、能教什么"：严谨的对比基准、经过独立审计的流水线、对每个结果量化的不确定性、可直接试教的课程；下一步写成"Next steps"。不写不真实的说法（例如"模型赢了""标准化提升了预测""学习效果提升"）。第 3 页的 BTC 单一交易所说明、第 4.5 节自相关用了完整序列、网格边缘选择等细节保留在本文件、数据卡片和 Q&A 里，被问到时如实回答。

#### 能说与不能说

| 可以说 | 不能说 |
|---|---|
| 没有任何配置能被区分于"打平基线" | "模型赢了 / 标准化提升了预测" |
| 5/20 输给基线，最高 +0.52% | "技能分数排名第一的模型最好" |
| 日度尺度的自相关接近 0 | "市场是纯随机游走" |
| 误差指标不含成本与风险 | 任何盈利、投资建议含义 |

---

### 4.8 补充测试：神经网络能预测涨跌方向吗？（D14）

- `scripts/supplementary_direction_test.py`：MLP（今天的 10 个特征）和 LSTM（过去 20 天的特征序列）预测"明天收盘是否高于今天"。同一切分与删行；参数和提前停止只用训练块末尾 20%；验证集只用于报告；测试集不读。在 GPU 上用 5 个种子训练，概率取平均。
- 结果见 `experiments/supplementary/direction_test/README.md` 与 Backup 6：苹果上两者都不如"永远猜涨"；比特币 LSTM 相对"永远猜跌"+5.3pp，但区间 [−0.3, +10.1] 包含 0，且验证期 52% 的日子上涨，换成"永远猜涨"优势很小；5 种子平均高于任何单个种子，说明是平均掉的噪声。所有模型在训练预留段上的 log-loss ≈ 0.69 ≈ ln 2（抛硬币）。
- **能说**："在同样的数据上，神经网络（包括序列模型）也没能比简单规则更好地预测方向"。**不能说**："LSTM 在比特币上有效"。
- LSTM 输入不同于主研究，所以它是补充测试，不进入 20 次运行的主矩阵。

## Act V · 教育：从实验到课堂

### 5.1 教育目标
让高中高年级 / 大一新生在看到"某模型 95.56 分"时，追问 **Q1 能看到什么、Q2 简单规则做到多少、Q3 有多确定**。

对应课程要求的七个连接点：特征/目标分离、拟合与泛化、仅训练集预处理、指标、模型复杂度、泄漏预防、教师判断（为什么要教**负面结果**）。

### 5.2 课程材料——目前仓库里有**两套**设计

| | `deliverables/lesson/*`（早期） | `deliverables/notebook/INT4096_Colab_Teaching_Template.ipynb`（11-24 新增） |
|---|---|---|
| 结构 | Hook → 陷阱 → 对手 → 对比 → 深挖 → 讨论；Task 1–5 = 拟合 vs 泛化 / 找泄漏 / 读技能分数 / 缩放敏感性 / 误差≠盈利 | Task 1 基线与 R² 陷阱 / Task 2 识别非法特征 / Task 3 造 10 个合法特征并训练 / Task 4 全模型对比 + Bootstrap / Task 5 迁移到"出勤率预测" |
| 数据 | 真实快照（`INT4096_Final_Colab.ipynb`） | **模拟的几何随机游走**（`np.random`），所以屏幕上的 R²=0.9281 不是项目数字 |

**v2 演示采用较新的 Template 的五个任务**（也是 v1 Act V 的写法）。需要你们统一：要么改 `deliverables/lesson/*` 的任务名，要么在 Template 里注明"练习数据为模拟；真实结果见 Final Colab"。演示里说"五个任务"时不要点名，以免和教师指南对不上。

### 5.3 可复现性
| 要素 | 实现 | 状态 |
|---|---|---|
| 数据版本锁定 | SHA-256，运行前重新校验 | 已核实 |
| 代码版本 | 每次运行记录 git commit | 已核实 |
| 自动化测试 | **83 项 pytest 全部通过**（我在干净环境重跑；README 里写的"79"是旧数字） | 已核实 |
| 泄漏变异测试 | 独立脚本，6 种缺陷必须全部被检出 | 脚本已核实 |
| 配置哈希 | 防止静默修改 | 已核实 |

### 5.4 研究边界（结尾页要说清）
两个资产（其中 BTC 为单一交易所）；一个历史窗口；一天的预测跨度；测试集封存；P3/P4 未运行；**没有学习者研究，不声称学习增益**；非投资建议。下一步：冻结分析后**一次性**解封测试集（需 D7 批准）；用真实班级试教。

---

## 附录 A · 相对 v1 的修正记录

| # | v1 的说法 | 核实结果 | v2 处理 |
|---|---|---|---|
| 1 | 超参数在**验证集** MAE 上评估 | 训练块内 5 折扩展窗口 CV；验证块不参与 | 改写 3.3 |
| 2 | 搜索空间"对数空间" | 离散网格的随机抽样；网格值已列出 | 改写 3.3 |
| 3 | 每轮时间上限 90 秒 | 整个搜索（每格）上限 90 秒 | 改写 3.2 |
| 4 | 重复→保留第一条、缺失→前向填充 | 加载器遇重复直接抛错；两个快照 0 行异常 | 改写 1.3 |
| 5 | AAPL 约 $200–230，BTC $30k–100k+ | AAPL 125–348，BTC 15.8k–124.7k | 改写 1.1 |
| 6 | 变异 #2"特征与目标混合" | 实为伪装的 `periods=-1` 前视 | 改写 2.6 |
| 7 | "早期测试套件没检出 6 种缺陷" | 当时是 `shift(-1)` 和 `bfill` 两种存活 | 改写 2.6 |
| 8 | 83 项测试"含 6 种泄漏注入" | 83 项 pytest + 独立变异脚本 | 改写 5.3 |
| 9 | Linear 变差因"优化路径" | L2 有效强度随尺度变化；已复现 | 改写 4.4 |
| 10 | "Linear (near-unregularised)" | 实为 Ridge，α=10 | 改名 Linear baseline |
| 11 | 短期波动率主导 | 主导的是 `vol_30` 等 | 改写 4.6 |
| 12 | "用 Skill 做最终排名" | 20/20 区间含 0，不排名 | 改写 4.1、4.7 |
| 13 | 自相关解释了"为什么提升空间有限" | 只是诊断之一，且用了完整序列 | 改写 4.5 |
| 14 | 目标变量"早期方案"一笔带过 | 实为 D8 的真实失败（skill ≈ −18.3） | 补写 2.3 |
| 15 | 幻灯片速查表对应旧 16 页 | 旧稿与 `main.tex`、脚本三者互不一致 | 见附录 C |

另有一处代码问题：提交的 `numbers.tex` 含 `HookAAPLRsq` 等 3 个宏，但 `build_slide_assets.py` 不生成它们，**干净重建会丢失并导致编译失败**。已在生成器里补上（值与原来逐位一致）。

## 附录 B · 需要你们决定的事项

| # | 事项 | 建议 |
|---|---|---|
| B-1 | 自相关用了含封存期的完整序列 | 用"训练+验证"重算并更新 JSON 与幻灯片；在此之前措辞为"描述性统计" |
| B-2 | D8（预测变化量）、D7（测试集解封）、D1、D3 等仍待人工批准 | 优先签 D8 |
| B-3 | 两套课程设计 + Template 使用模拟数据 | 见 5.2 |
| B-4 | 我跑了一个**无特征**对照：持续性 + 训练期平均变化量，AAPL 技能约 +0.22%，BTC 约 +0.04%（临时复现，**不在 artifacts 里**） | 这说明 AAPL 上约 +0.25% 的一簇结果与"加一个常数漂移"几乎一样；建议作为第 6 个基线正式跑一次再决定是否讲 |
| B-5 | `README.md` 写 79 项测试、21 页 | 已改为 83 / 23（见 README） |
| B-6 | 参考文献链接 | `references.bib` 没有 DOI/URL 字段；下表的链接是 v1 加的，我的沙箱无法联网验证，提交前请点一遍 |
| B-7 | 网格边缘选择 | 见 3.3，可作为 Q&A |
| B-8 | 报告 `deliverables/report/latex/sections/07_models.tex` 第 5 行也写"near-unregularised linear model" | 与幻灯片保持一致，改为"a linear baseline with a tuned L2 penalty"，并重新编译报告（我没有改报告，因为它是单独的评分交付物） |

## 附录 C · v3 幻灯片对照（18 + 6 备份 + 2 参考文献）

| # | 部分 | 标题 | 对应本文 | 目标时长 |
|---|---|---|---|---|
| 1 | 开场 | Learning Machine Learning Through Financial Forecasting（R² 钩子 + 研究问题） | 0.2 | 1:30 |
| 2 | 开场 | Roadmap: One Pipeline, Five Stages | 0.1–0.2 | 0:45 |
| 3 | 1 | What We Used, and Exactly Where It Came From（含两个下载链接） | 1.1、参考文献·数据来源 | 0:35 |
| 4 | 1 | Why These Two: Two Markets With Different Characteristics | 1.1 | 0:55 |
| 5 | 1 | Selection Conditions: From Raw Bars to Modelling Rows | 1.2–1.3 | 1:05 |
| 6 | 2 | Problems in the Raw Data, and How We Handled Each | 1.1、2.1、2.4–2.5 | 1:10 |
| 7 | 2 | From One Day's Prices to Ten Features（2024-11-21 苹果真实一天，按概念讲，不念小数） | 2.1–2.2 | 1:25 |
| 8 | 2 | Every Model Gets the Same Data: One Shared Pipeline（同一数据、P0/P2 唯一开关、预测变化量） | 2.2、2.3、2.5 | 1:10 |
| 9 | 2 | Chronological Split, and Proof That the Pipeline Cannot Peek | 2.4、2.6 | 0:50 |
| 10 | 3 | Five Models Plus a Baseline: Why Each One Is There | 3.1 | 1:05 |
| 11 | 3 | Fine-Tuning: The Same Search and Budget for Every Model（网格与选中值由脚本生成） | 3.2–3.3 | 1:00 |
| 12 | 3 | What We Explored Beyond Hyperparameters | 2.3、2.5、3.3、4.4 | 0:55 |
| 13 | 4 | Four Metrics, Each With a Job | 4.1 | 1:05 |
| 14 | 4 | Results: All 20 Runs Land Within 1% of the Baseline | 4.2 | 0:50 |
| 15 | 4 | How Certain? Every Interval Includes Zero | 4.3、4.5 | 0:55 |
| 16 | 5 | Teaching Design: The Pipeline Becomes a 60-Minute Lesson | 5.1–5.2 | 0:50 |
| 17 | 5 | Try It Yourself: The Whole Pipeline, Interactive（网站预览 + 二维码） | 5.2 | 0:30 |
| 18 | 5 | Summary: What Each Stage Delivered | 5.4 | 0:45 |

备份：B1 完整 20 格矩阵 · B2 公平性与 manifest 审计 · B3 为什么删一行（周五例子）· B4 特征重要性 · B5 Q&A 卡片 · B6 MLP/LSTM 涨跌方向补充测试。

**v3 的两个取舍：** ① 第 16 页的五个任务采用 `deliverables/lesson/formative_tasks.md`（教师指南有逐题参考答案），解决了 5.2 中"两套任务名对不上"的问题；Colab Template 仍可作为练习本。② 第 11 页新增的"调参器几乎总选最保守设置"（岭回归 α 最大、HGB 学习率最小、AAPL 上 SVR 的 C 最小、RF 叶子最大）来自 `metrics.json` 的 `best_hyperparameters`，与"信号很少"的结论一致。

---

## 参考文献 Reference List

> 书目信息与 `deliverables/report/latex/references.bib` 一致；**DOI/URL 为 v1 补充，未能在沙箱联网验证，提交前请逐个打开确认**。幻灯片的两页 References 由 `references.bib` 直接生成，不依赖下表。

### 模型与软件
| 编号 | 引用 | 链接 |
|---|---|---|
| [1] | Pedregosa et al. (2011). **Scikit-learn: Machine Learning in Python**. *JMLR*, 12, 2825–2830. | https://jmlr.org/papers/v12/pedregosa11a.html |
| [2] | Hastie, Tibshirani & Friedman (2009). **The Elements of Statistical Learning** (2nd ed.). Springer. | https://hastie.su.domains/ElemStatLearn/ |
| [3] | Breiman (2001). **Random Forests**. *Machine Learning*, 45(1), 5–32. | https://doi.org/10.1023/A:1010933404324 |
| [4] | Drucker et al. (1997). **Support Vector Regression Machines**. *NIPS*, 9, 155–161. | https://papers.nips.cc/paper/1996/hash/d38901788c533e8286cb6400b40b386d-Abstract.html |
| [5] | Friedman (2001). **Greedy Function Approximation: A Gradient Boosting Machine**. *Annals of Statistics*, 29(5), 1189–1232. | https://doi.org/10.1214/aos/1013203451 |
| [6] | Fisher, Rudin & Dominici (2019). **All Models are Wrong, but Many are Useful**. *JMLR*, 20(177), 1–81. | https://jmlr.org/papers/v20/18-760.html |

### 预测、评估与课程材料
| 编号 | 引用 | 链接 |
|---|---|---|
| [7] | Bergmeir, Hyndman & Koo (2018). **A Note on the Validity of Cross-Validation for Evaluating Autoregressive Time Series Prediction**. *CSDA*, 120, 70–83. | https://doi.org/10.1016/j.csda.2017.11.003 |
| [8] | Roberts et al. (2017). **Cross-validation Strategies for Data with Temporal, Spatial, Hierarchical, or Phylogenetic Structure**. *Ecography*, 40(8), 913–929. | https://doi.org/10.1111/ecog.02881 |
| [9] | Kaufman, Rosset, Perlich & Stitelman (2012). **Leakage in Data Mining: Formulation, Detection, and Avoidance**. *ACM TKDD*, 6(4), 1–21. | https://doi.org/10.1145/2382577.2382579 |
| [10] | Makridakis, Spiliotis & Assimakopoulos (2018). **The M4 Competition: Results, Findings, Conclusion and Way Forward**. *IJF*, 34(4), 802–808. | https://doi.org/10.1016/j.ijforecast.2018.06.001 |
| [11] | Fama (1970). **Efficient Capital Markets: A Review of Theory and Empirical Work**. *Journal of Finance*, 25(2), 383–417. | https://doi.org/10.2307/2325486 |
| [12] | Hyndman & Athanasopoulos (2021). **Forecasting: Principles and Practice** (3rd ed.). OTexts. | https://otexts.com/fpp3/ |
| [13] | The Education University of Hong Kong (2026). **INT4096 … Group Project Specification**. Course handout. | 课程内部材料，不外传 |

### 数据来源
| 资产 | 来源 | 代码 / 卡片 |
|---|---|---|
| AAPL | StockAnalysis `/api/symbol/s/aapl/history`，symbol `aapl` | `src/int4096/data/providers.py`；`data/cards/aapl_dataset_card.md` |
| BTC/USDT | Binance `/api/v3/klines`，`BTCUSDT` | 同上；`btc_dataset_card.md` |

---

*v2 · 2026-11-24 · INT4096 Group Project · The Education University of Hong Kong*
