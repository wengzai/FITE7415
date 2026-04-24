# 第二十三轮执行报告（Round 23）

## 1. 目标

在保留 round21 信号结构的前提下，仅把单笔风险降到 0.5%，检验是否能显著减少拒单，同时维持足够的全样本与弱窗口表现。

## 2. 改动

脚本：Program/XAUUSD/code/xauusd_round23_riskhalf_v1.py

1. `risk_per_trade` 从 `0.01` 下调到 `0.005`。
2. 其他 sizing 逻辑沿用 round21。

## 3. 结果

1. 全样本：TradeCnt 280, TotalPnL +696.9780, AnnualSharpe 0.7956, MaxDrawdownPct 0.02653
2. 弱窗口：TradeCnt 22, TotalPnL +119.3500, AnnualSharpe 0.9986, MaxDrawdownPct 0.00856
3. 系统日志：拒单显著减少，仅见极少数 `insufficient capital` 事件，执行稳定性明显优于 round21。

## 4. 对比当前方案A主线（round14）

1. 相比方案A全样本 `PnL +341.4714 / Sharpe 0.3949 / MaxDD 0.03738`，round23 的收益、Sharpe、回撤均更优。
2. 相比方案A弱窗口 `PnL +97.1492 / Sharpe 0.9423 / MaxDD 0.00652`，round23 的收益与 Sharpe 仍更优，回撤略高但仍处低位。

## 5. 结论

1. round23 已满足“非零交易、可重复评估、风险未失控、且相对当前A主线达到可接受改进”的进入主线条件。
2. 相比 round21，round23 牺牲了一部分收益，但换来了更干净的执行质量，更适合晋升为方案B主线候选版本。