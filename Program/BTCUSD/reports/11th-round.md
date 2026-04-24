# 第十一轮执行报告（Round 11, Step 2 到 Step 5）

## 0. 执行目标

按最新 cmd 约定执行“单任务内联合改动独立变量”的并发优化：

1. 保留 round10 的趋势过滤框架。
2. 在同一任务中联合调整独立变量，目标是提升弱窗口表现并尽量恢复交易频次。

## 1. Step 2：策略改动（联合独立变量）

脚本：Program/BTCUSD/code/btcusd_round11_joint_v1.py

本轮联合改动（单任务内）：

1. 趋势过滤窗口：`trend_period 100 -> 80`（放宽 regime 过滤）。
2. 入场阈值：`z_entry -1.2 -> -1.0`（提升触发频率）。
3. 持仓/冷却：`max_hold_days 5 -> 4`（提升周转）。

其余参数保持不变：

1. stop_atr_multiple = 1.2
2. take_profit_atr_multiple = 3.0
3. risk_per_trade = 0.01

## 2. Step 3：实验记录

1. 全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_090951_614728
   - task_id: 1777021791614728
   - status: DONE
2. 弱窗口（2025-07 到 2025-12）
   - runtime_id: 20260424_091041_770385
   - task_id: 1777021841770385
   - status: DONE

## 3. Step 4：结果

### 3.1 全样本对比（vs round10）

round10：

1. TradeCnt: 56
2. TotalPnL: +330.9822
3. AnnualSharpe: 0.4071
4. MaxDrawdownPct: 0.03641

round11：

1. TradeCnt: 60
2. TotalPnL: +314.9233
3. AnnualSharpe: 0.3630
4. MaxDrawdownPct: 0.03562

结论：

1. 交易次数小幅回升。
2. 全样本收益与 Sharpe 下滑。
3. 回撤小幅改善。

### 3.2 弱窗口对比（2025H2）

round10：

1. TradeCnt: 8
2. TotalPnL: +38.8510
3. AnnualSharpe: 0.3223
4. MaxDrawdownPct: 0.01057

round11：

1. TradeCnt: 8
2. TotalPnL: +52.3786
3. AnnualSharpe: 0.4833
4. MaxDrawdownPct: 0.00657

结论：

1. 在弱窗口表现显著改善（收益、Sharpe、回撤均优于 round10）。
2. 样本数仍偏低，需继续关注样本充分性。

## 4. Step 5：判断与下一步

1. round11 证明“联合改动”方式在弱窗口上有效。
2. 为尝试修复全样本收益下滑，进入 round12 做第二次联合改动测试。

## 5. 风险复核

1. 单笔风险与止损约束：PASS
2. 弱状态防御能力：IMPROVED
3. 样本充分性：BORDERLINE
4. 成本/滑点现实性：NEEDS-DATA
