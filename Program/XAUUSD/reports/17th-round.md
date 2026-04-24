# 第十七轮执行报告（Round 17）

## 1. 目标

移除趋势过滤，检验趋势模块是否为 XAUUSD 影子零交易的决定性阻塞项。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round17_notrend_v1.py

1. 完全移除长期趋势过滤。
2. 其余参数保持不变。

## 3. 结果

1. 全样本：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0

## 4. 结论

1. 趋势模块不是单独的根因。
2. 问题继续压缩到 `bandwidth / zscore / 资金约束` 路径。