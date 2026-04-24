# 第十二轮执行报告（Round 12, Step 2 到 Step 5）

## 0. 执行目标

在 round11 的基础上继续使用“单任务联合改动”，尝试提升全样本收益，同时维持弱窗口稳健性。

## 1. Step 2：策略改动（联合独立变量）

脚本：Program/BTCUSD/code/btcusd_round12_joint_v1.py

本轮联合改动（相对 round11）：

1. 入场阈值：`z_entry -1.0 -> -1.1`（适度收紧）。
2. 止盈倍数：`take_profit_atr_multiple 3.0 -> 3.2`（拉长盈利腿）。
3. 持仓时间：`max_hold_days 4 -> 5`（允许持有更久）。

其余参数保持：

1. trend_period = 80
2. stop_atr_multiple = 1.2
3. risk_per_trade = 0.01

## 2. Step 3：实验记录

1. 全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_091134_312645
   - task_id: 1777021894312645
   - status: DONE
2. 弱窗口（2025-07 到 2025-12）
   - runtime_id: 20260424_091218_538757
   - task_id: 1777021938538757
   - status: DONE

## 3. Step 4：结果

### 3.1 全样本对比（vs round11）

round11：

1. TradeCnt: 60
2. TotalPnL: +314.9233
3. AnnualSharpe: 0.3630
4. MaxDrawdownPct: 0.03562

round12：

1. TradeCnt: 52
2. TotalPnL: +113.8544
3. AnnualSharpe: 0.1570
4. MaxDrawdownPct: 0.03026

结论：

1. 回撤继续下降。
2. 但收益与 Sharpe 明显恶化，交易数下降。

### 3.2 弱窗口对比（2025H2）

round11：

1. TradeCnt: 8
2. TotalPnL: +52.3786
3. AnnualSharpe: 0.4833
4. MaxDrawdownPct: 0.00657

round12：

1. TradeCnt: 8
2. TotalPnL: +23.1245
3. AnnualSharpe: 0.1910
4. MaxDrawdownPct: 0.01212

结论：

1. 弱窗口也明显退化（收益与 Sharpe 下滑、回撤上升）。
2. 本轮联合改动判定为失败样本。

## 4. Step 5：停止判断

决策：在本次默认优化流程中暂时停止继续 round13+。

理由：

1. round11 已提供当前“稳健性优先”方向的较优点。
2. round12 在全样本与弱窗口同时退化，说明该联合改动方向边际收益转负。
3. 继续沿同类变量微调的性价比低，应转入新问题定义后再开新轮次。

## 5. 当前建议保留版本

双基线保留：

1. 收益优先基线：round5B（Program/BTCUSD/code/btcusd_round5B_exit_v1.py）。
2. 稳健优先基线：round11（Program/BTCUSD/code/btcusd_round11_joint_v1.py）。

## 6. 风险复核

1. 单笔风险与止损规则：PASS
2. 方向有效性（联合改动方向）：第二次尝试失败，建议暂缓同类微调
3. 样本充分性：BORDERLINE
4. 成本/滑点现实性：NEEDS-DATA
