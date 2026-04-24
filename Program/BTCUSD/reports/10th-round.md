# 第十轮执行报告（Round 10, Step 2 到 Step 5）

## 0. 执行目标

针对 round9 暴露的 2025H2 弱周期问题，尝试在不引入复杂结构的前提下提升稳健性：

1. 保留 round5B 的核心均值回归与 ATR 出场逻辑。
2. 新增轻量趋势过滤，避免在长期弱势状态下逆势做多。

## 1. Step 2：策略改动

脚本：Program/BTCUSD/code/btcusd_round10_trendfilter_v1.py

本轮核心改动：

1. 新增 `trend_period = 100`。
2. 增加入场前置条件：`latest_close > SMA100` 才允许执行原有 long-entry 逻辑。
3. 其余参数保持与 round5B 一致：
   - z_entry = -1.2
   - stop_atr_multiple = 1.2
   - take_profit_atr_multiple = 3.0
   - max_hold_days = 5

## 2. Step 3：实验记录

1. 全样本验证（2023-01 到 2025-12）
   - runtime_id: 20260424_090001_554112
   - task_id: 1777021201554112
   - status: DONE
2. 重点弱窗验证（2025-07 到 2025-12）
   - runtime_id: 20260424_090050_078294
   - task_id: 1777021250078294
   - status: DONE

## 3. Step 4：结果

### 3.1 全样本对比（vs round5B）

round5B（历史最优基线）：

1. TradeCnt: 114
2. TotalPnL: +545.7112
3. AnnualSharpe: 0.4182
4. MaxDrawdownPct: 0.04102

round10（trend filter）：

1. TradeCnt: 56
2. TotalPnL: +330.9822
3. AnnualSharpe: 0.4071
4. MaxDrawdownPct: 0.03641
5. ProfitFactor: 1.6059

结论：

1. 收益和交易数明显下降，但回撤进一步降低。
2. Sharpe 与 round5B 接近，风险收益比没有明显恶化。

### 3.2 弱窗口对比（2025H2）

round9 基线（round5B）在 2025H2：

1. TradeCnt: 26
2. TotalPnL: -34.9122
3. AnnualSharpe: -0.1760
4. MaxDrawdownPct: 0.02875
5. ProfitFactor: 0.8900

round10（trend filter）在 2025H2：

1. TradeCnt: 8
2. TotalPnL: +38.8510
3. AnnualSharpe: 0.3223
4. MaxDrawdownPct: 0.01057
5. ProfitFactor: 1.5439

结论：

1. 在最弱窗口中由负转正。
2. 回撤明显收敛。
3. 代价是样本数下降明显，需要继续观察样本充分性。

## 4. Step 5：决策

1. round10 不是全样本收益最优，但显著改善了弱周期鲁棒性。
2. 将其记录为“稳健性候选版本”，与 round5B 形成收益优先 vs 稳健优先双基线。
3. 下一轮（round11）建议：
   - 在 round10 基础上微调趋势过滤阈值/周期（例如 80/100/120）
   - 目标是在保持 2025H2 稳健性的同时恢复部分交易频次。

## 5. 风险复核

1. 单笔风险与止损约束：PASS
2. 弱状态防御能力：IMPROVED
3. 样本充分性：BORDERLINE（交易数下降明显）
4. 成本/滑点现实性：NEEDS-DATA
