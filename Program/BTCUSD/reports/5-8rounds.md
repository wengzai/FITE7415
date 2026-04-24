# Round 5-8 迭代简报

## 1. 总体结论

round5-8 的结果非常明确：

1. 当前最优版本出现在 round5B。
2. round6 没有带来任何新增收益，说明该方向已出现明显边际递减。
3. round7 与 round8 虽然尝试了结构性改动与策略性改动，但均显著劣化，未能超越 round5B。

当前建议保留版本：

1. 脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py
2. 核心指标：TradeCnt 114，TotalPnL +545.7112，AnnualSharpe 0.4182，MaxDrawdownPct 0.04102

## 2. 各轮摘要

### Round 5

本轮目标：

1. 在 round4 已解决“交易次数过少”后，转向“收益质量优化”。

使用策略：

1. 仍然基于单向均值回归框架。
2. 同轮并行比较两个优化方向（平台限制下改为串行提交、同轮对比）。

优化方向：

1. 方向A，Signal Quality：收紧入场阈值，`z_entry -1.2 -> -1.5`
2. 方向B，Exit Structure：优化止损止盈比，`stop 1.5ATR -> 1.2ATR`，`TP 2.5ATR -> 3.0ATR`

回测效果：

1. Round5A
	- TradeCnt: 80
	- TotalPnL: -207.4242
	- AnnualSharpe: -0.2395
	- MaxDrawdownPct: 0.04729
	- 结果：显著劣化
2. Round5B
	- TradeCnt: 114
	- TotalPnL: +545.7112
	- AnnualSharpe: 0.4182
	- MaxDrawdownPct: 0.04102
	- ProfitFactor: 1.3702
	- 结果：相对 round4 明显优化

结论：

1. round5B 是第一个明显优于 round4 的收益质量改进版本。
2. round5A 说明单纯收紧入场只会减少机会并破坏收益。

### Round 6

本轮目标：

1. 沿 round5B 胜出方向继续迭代，确认是否还有显著增益。

使用策略：

1. 保持 round5B 的单向均值回归和出场结构。

优化方向：

1. 将 `take_profit_atr_multiple` 从 3.0 提升到 3.5。

回测效果：

1. TradeCnt: 114
2. TotalPnL: +545.7112
3. AnnualSharpe: 0.4182
4. MaxDrawdownPct: 0.04102

结论：

1. 与 round5B 完全一致，可视为零增量。
2. 说明在当前框架内继续细调 TP 已没有意义。

### Round 7

本轮目标：

1. 尝试结构性改动，在保持样本可用的前提下改善 Sharpe/回撤。

使用策略：

1. 基于 round5B 最优版本。
2. 引入状态过滤模块与更严格的单仓约束。

优化方向：

1. 新增状态过滤：
	- `trend_ratio = abs(SMA20 - SMA100) / SMA100 <= 0.08`
	- `bandwidth = std20 / SMA20` 限制在 `[0.01, 0.12]`
2. 增强单仓约束：`cooldown_days = 6`

回测效果：

1. TradeCnt: 56
2. TotalPnL: +63.6121
3. AnnualSharpe: 0.0909
4. MaxDrawdownPct: 0.04113

结论：

1. 交易次数下降明显。
2. 收益和 Sharpe 显著恶化。
3. 回撤没有得到实质改善。
4. 该状态过滤模块在当前阈值设计下是一次失败尝试。

### Round 8

本轮目标：

1. 尝试策略性改动，测试“多空双向均值回归”是否优于单向版本。

使用策略：

1. 从单向均值回归升级为双向均值回归。
2. 允许做空。

优化方向：

1. `zscore <= -1.2` 做多
2. `zscore >= +1.2` 做空
3. 多空使用对称 ATR 风控

回测效果：

1. TradeCnt: 232
2. TotalPnL: -697.3774
3. AnnualSharpe: -0.2989
4. MaxDrawdownPct: 0.11835
5. ProfitFactor: 0.8518

结论：

1. 虽然交易次数大幅增加，但收益质量严重恶化。
2. 当前 BTCUSD 日线框架下，双向均值回归并不成立。
3. 这是一次典型的“样本更多但策略更差”的失败扩展。

## 3. 关键比较

按综合表现排序：

1. Round5B：当前最优解
2. Round4：解决交易次数问题的基准解
3. Round6：与 round5B 完全相同，无增量
4. Round7：结构过滤失败
5. Round8：双向策略失败
6. Round5A：信号收紧失败

最关键观察：

1. 交易次数问题已经在 round4 解决，不再是主矛盾。
2. round5B 证明“出场优化”比“入场收紧”更有效。
3. 从 round6 开始，继续在该方向上细调参数的收益几乎归零。
4. 后续两次更大的结构/策略改动都没能超越 round5B。

## 4. 当前最佳版本

建议当前保留版本为：

1. 脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py
2. 核心逻辑：单向均值回归 + 改良版 ATR 出场结构
3. 指标：
	- TradeCnt: 114
	- TotalPnL: +545.7112
	- AnnualSharpe: 0.4182
	- MaxDrawdownPct: 0.04102
	- ProfitFactor: 1.3702

## 5. TODO

### 5.1 立即要做

1. 固定 round5B 为后续所有实验的对照组。
2. 在总报告中加入 round4 与 round5B 的对比表，突出“从样本修复到收益质量优化”的演化过程。
3. 明确在报告里说明 `TradeCost = 0` 的限制，避免把当前结果表述为真实可交易结论。

### 5.2 如果继续下一阶段优化

1. 不要再继续细调同类 TP/SL 参数。
2. 优先测试一个更强但更可解释的 regime filter，而不是继续堆复杂条件。
3. 若再做结构性改动，建议一次只加一个模块，并以 round5B 为基线做 A/B 对照。

### 5.3 更具体的后续实验建议

1. 先做一个单变量状态过滤实验：
	- 例如 ADX 过滤，或长期均线斜率过滤，或波动率分位数过滤。
2. 若尝试做空逻辑，不要直接复用多头参数；应单独设计空头子策略并独立验证其期望收益。
3. 增加成本敏感性分析：即使平台 TradeCost 为 0，也应手动做手续费/滑点压力测试。

## 6. 一句话总结

round5B 是 round5-8 区间内最值得保留的策略版本；其后的优化不是没有尝试，而是已经尝试到足以说明：短期内继续改同类参数或直接扩成双向策略，都很难带来更好的性价比。
