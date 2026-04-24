# 第二十二轮执行报告（Round 22）

## 1. 目标

仅通过拉开进场间隔来减少重叠开仓拒单，观察是否能在不破坏绩效的情况下改善执行稳定性。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round22_spacingfix_v1.py

1. 入场间隔由 `days_since_entry < max_hold_days` 调整为 `days_since_entry <= max_hold_days`。

## 3. 结果

1. 全样本：TradeCnt 295, TotalPnL +1366.1740, AnnualSharpe 0.7343, MaxDrawdownPct 0.05657

## 4. 结论

1. 纯粹拉开进场间距虽然改善了部分执行冲突，但明显压低了策略质量。
2. 该方向不是最终主线候选，继续回到资金占用层做更温和修复。