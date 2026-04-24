# 第十九轮执行报告（Round 19）

## 1. 目标

仅保留 `zscore` 作为主要信号门槛，判断 XAUUSD 是否其实已有交易信号，只是此前被多重过滤阻断。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round19_notrend_noband_v1.py

1. 移除 `bandwidth` 过滤。
2. 保持无趋势过滤。

## 3. 结果

1. 全样本：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0

## 4. 结论

1. 仅看统计指标仍表现为零交易。
2. 需要继续做“几乎无门槛”的执行诊断，以区分信号问题和下单问题。