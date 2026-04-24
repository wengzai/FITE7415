# 方案B影子自动化优化收官总结

## 1. 授权与执行范围

本轮授权：从 round15 开始，围绕 XAUUSD 的方案B影子执行至多 15 轮自动化优化，直到达到进入方案B主线的条件。

本次实际执行：round15 到 round23，共 9 轮。

## 2. 关键研究路径

### 2.1 round15 到 round19：排除假设

1. 依次排除了单独 `bandwidth`、轻微 `trend`、移除 `trend`、移除 `bandwidth` 等路径作为零交易主因。
2. 这些轮次的共同结果是统计指标仍显示 0 交易。

### 2.2 round20：定位根因

1. 在接近无门槛的信号条件下，统计上仍为 0 交易。
2. 系统日志明确显示：`Invalid order is rejected due to insufficient capital`。
3. 结合合约规格确认：`BTCUSD contractSize = 1`，`XAUUSD contractSize = 100`，根因是 sizing 未按 XAU 合约换算。

### 2.3 round21 到 round23：修复与收敛

1. round21 修复 sizing 后，方案B从“假性零交易”跃迁为“可评估高绩效版本”。
2. round22 通过强行拉开进场间距减少重叠，但绩效退化明显。
3. round23 以降低单笔风险的方式保留 round21 信号结构，同时显著减少拒单，是更平衡的版本。

## 3. 候选版本对比

### 3.1 round21

1. 全样本：TradeCnt 283, TotalPnL +2055.1960, Sharpe 1.2565, MaxDD 0.02637
2. 弱窗口：TradeCnt 35, TotalPnL +413.9250, Sharpe 2.0094, MaxDD 0.01509
3. 优点：绩效最强。
4. 缺点：仍存在少量重叠开仓导致的资金不足拒单。

### 3.2 round23

1. 全样本：TradeCnt 280, TotalPnL +696.9780, Sharpe 0.7956, MaxDD 0.02653
2. 弱窗口：TradeCnt 22, TotalPnL +119.3500, Sharpe 0.9986, MaxDD 0.00856
3. 优点：执行质量更干净，仍在全样本与弱窗口上优于当前方案A主线。
4. 缺点：收益不及 round21。

## 4. 风险审查结论

### 4.1 Risk Summary

1. 单笔风险限制已定义：round23 使用 `risk_per_trade = 0.5%`。
2. 最大回撤受控：全样本 2.65%，弱窗口 0.86%。
3. 执行现实性较 round21 改善，拒单仅剩极少数孤立事件。

### 4.2 Checklist Results

1. 每笔风险上限：Pass
2. 回撤控制可观测：Pass
3. 资金占用与合约规格匹配：Pass
4. 执行层拒单是否已大幅缓解：Pass
5. 成本/滑点假设：Needs-data

### 4.3 Go/No-go

1. 对“进入项目主线研究版本”的决策：Go
2. 对“直接视作最终定稿、无需再测成本敏感性”的决策：No-go

## 5. 最终决定

1. 方案B影子优化已完成。
2. 推荐将 round23 作为方案B新的主线候选版本。
3. round21 保留为高收益对照版本，不直接主线化。
4. 当前方案A主线可降级为对照基线，不再作为唯一主线。

## 6. 两项收尾工作执行结果

### 6.1 收尾工作一：主线切换落地

1. 已将默认主线切换为 `Program/XAUUSD/code/xauusd_mainline_v1.py`（源自 round23）。
2. 已将 `Program/XAUUSD/code/xauusd_round21_sizingfix_v1.py` 标记为高收益对照版本。
3. 已将 `Program/BTCUSD/code/btcusd_round14_regime_v2.py` 降级为 legacy A-main 对照。

### 6.2 收尾工作二：成本/滑点敏感性验证

1. 已完成 round24 验证，详见 `Program/XAUUSD/reports/24th-round.md`。
2. 关键结论：在平台可用成本档（TradeCost=1.0）下，round23 仍保持：
   - 全样本：PnL +556.9780, Sharpe 0.6370, MaxDD 0.02713
   - 弱窗口：PnL +108.3500, Sharpe 0.9059, MaxDD 0.00876
3. 因此 round23 具备主线化条件，收尾任务完成。
