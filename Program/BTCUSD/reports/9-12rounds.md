# Round 9-12 执行结果汇总（本次）

## 1. 执行范围与目标

本次覆盖 round9 到 round12，目标分两步：

1. 先验证 round5B 在不同时间窗口的泛化稳定性（round9）。
2. 再按“单任务内联合改动独立变量”的方式进行联合优化（round11、round12），尝试在弱窗口改善与全样本收益之间取得更好平衡。

## 2. Round 9：多时间窗泛化验证（基线 round5B）

时间窗结果：

1. 2024H1：TradeCnt 21，TotalPnL +46.9844，Sharpe 0.2314，MaxDD 0.02566
2. 2024H2：TradeCnt 17，TotalPnL +150.4734，Sharpe 0.6092，MaxDD 0.01542
3. 2025H1：TradeCnt 18，TotalPnL +395.2735，Sharpe 1.3280，MaxDD 0.01836
4. 2025H2：TradeCnt 26，TotalPnL -34.9122，Sharpe -0.1760，MaxDD 0.02875

结论：

1. 4 窗口中 3 个窗口为正，说明基线并非只在单一窗口有效。
2. 2025H2 明显转弱，说明泛化能力仍不稳定。

## 3. Round 10（已有前置结果）：轻量趋势过滤

对比 round5B，round10 的核心表现为：

1. 全样本收益下降，但回撤更低。
2. 2025H2 由负转正，弱窗口稳健性改善。

该轮将策略从“单一收益优先”推进到“收益/稳健权衡”框架。

## 4. Round 11：联合改动（单任务并发定义）

脚本：Program/BTCUSD/code/btcusd_round11_joint_v1.py

联合改动（同一回测任务内）：

1. trend_period：100 -> 80
2. z_entry：-1.2 -> -1.0
3. max_hold_days：5 -> 4

结果：

1. 全样本：TradeCnt 60，TotalPnL +314.9233，Sharpe 0.3630，MaxDD 0.03562
2. 2025H2：TradeCnt 8，TotalPnL +52.3786，Sharpe 0.4833，MaxDD 0.00657

结论：

1. 弱窗口改善明显（收益、Sharpe、回撤都优于 round10）。
2. 全样本收益略低于 round10，需要继续验证联合改动边界。

## 5. Round 12：联合改动二次验证

脚本：Program/BTCUSD/code/btcusd_round12_joint_v1.py

联合改动（相对 round11）：

1. z_entry：-1.0 -> -1.1
2. take_profit_atr_multiple：3.0 -> 3.2
3. max_hold_days：4 -> 5

结果：

1. 全样本：TradeCnt 52，TotalPnL +113.8544，Sharpe 0.1570，MaxDD 0.03026
2. 2025H2：TradeCnt 8，TotalPnL +23.1245，Sharpe 0.1910，MaxDD 0.01212

结论：

1. 全样本与弱窗口同时退化。
2. 该联合改动方向本轮判定为失败样本，边际收益转负。

## 6. 本次决策：暂时固定双基线

自本次起，先固定双基线用于后续所有对照实验：

1. 收益优先基线（Baseline-P）：round5B
	- 脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py
	- 参考表现：TradeCnt 114，TotalPnL +545.7112，Sharpe 0.4182，MaxDD 0.04102
2. 稳健优先基线（Baseline-R）：round11
	- 脚本：Program/BTCUSD/code/btcusd_round11_joint_v1.py
	- 参考表现：全样本 TotalPnL +314.9233，Sharpe 0.3630，MaxDD 0.03562；2025H2 Sharpe 0.4833，MaxDD 0.00657

执行规则：

1. 后续新方案必须同时对比 Baseline-P 与 Baseline-R。
2. 若新方案仅在单一目标上改善（例如只降回撤但收益显著下滑），不直接替换双基线。
3. 只有在“全样本 + 弱窗口”双维度都达到可接受改进时，才进入新的候选基线评审。

## 7. 下一步建议（保持简化）

1. 暂停同类微调（避免继续在已退化方向消耗轮次）。
2. 新轮次优先采用“一次只变一个模块”的对照设计。
3. 保留并复用 round9 的多窗口验证框架，避免回到单一窗口结论。

## 8. 建议落地为下一条执行指令

为把建议变成可执行流程，下一轮按以下规则执行：

1. 继续方案 A（BTCUSD）主线，并且一轮只改一个模块。
2. 同时开启方案 B 影子验证：将冻结参数迁移到 XAUUSD，不调参。
3. 新方案必须同时对比 Baseline-P 与 Baseline-R。
4. 若新方案无法在“全样本 + 弱窗口”双维度达到可接受改进，则不进入新候选基线。
