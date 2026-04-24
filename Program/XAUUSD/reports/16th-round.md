# 第十六轮执行报告（Round 16）

## 1. 目标

仅放宽 XAUUSD 影子策略的长期趋势门槛，检验轻微趋势过滤是否阻断交易。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round16_trend_v1.py

1. 趋势条件由 `latest_close > trend_sma` 放宽为 `latest_close > 0.995 * trend_sma`。
2. 其他参数冻结不变。

## 3. 结果

1. 全样本：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0

## 4. 结论

1. 轻微放宽趋势过滤无效。
2. 问题不在趋势阈值边缘，而更可能在更深层的执行或 sizing 逻辑。