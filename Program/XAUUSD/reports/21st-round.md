# 第二十一轮执行报告（Round 21）

## 1. 目标

仅修复 XAUUSD 的 `volume` 计算，使其按金合约规格进行 sizing，并验证方案B是否从“假性零交易”转入“真实可评估”。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round21_sizingfix_v1.py

1. 引入 `contract_size = 100`。
2. 以 `risk_per_lot = stop_distance * contract_size` 计算每手风险。
3. 用 `max_affordable_volume = capital / (entry_price * contract_size)` 约束最大可承受仓位。
4. 保持 round20 的信号逻辑不变。

## 3. 结果

1. 全样本：TradeCnt 283, TotalPnL +2055.1960, AnnualSharpe 1.2565, MaxDrawdownPct 0.02637
2. 弱窗口：TradeCnt 35, TotalPnL +413.9250, AnnualSharpe 2.0094, MaxDrawdownPct 0.01509
3. 系统日志：已出现大量真实成交，但仍有少量重叠进场时的 `insufficient capital` 拒单。

## 4. 结论

1. 方案B的核心阻塞已经解除，XAUUSD 影子策略正式进入可评估状态。
2. 当前版本是高绩效候选，但执行层仍存在少量重叠开仓导致的拒单，需要进一步优化。