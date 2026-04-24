# 第二十轮执行报告（Round 20）

## 1. 目标

把 XAUUSD 影子策略放宽到接近无门槛状态，确认问题究竟是信号缺失还是执行被拒绝。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round20_notrend_noband_zrelax_v1.py

1. `z_entry` 放宽至 `1.0`。
2. 维持无趋势过滤、无带宽过滤。

## 3. 结果

1. 全样本统计：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0
2. 系统日志：大量 `Invalid order is rejected due to insufficient capital`。

## 4. 结论

1. 方案B并非没有信号，而是下单被资金不足持续拒绝。
2. 根因锁定为 XAUUSD 合约规格与 `volume` 计算不匹配，需要优先修复 sizing。