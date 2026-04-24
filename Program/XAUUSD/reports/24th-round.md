# 第二十四轮执行报告（Round 24：成本/滑点敏感性验证）

## 1. Experiment ID 与目标

1. Experiment ID：R24_COST_SENSITIVITY_XAU_B23
2. 目标：验证 round23 主线候选在引入交易成本后的稳定性，并据此完成主线切换决策闭环。

## 2. Baseline 与测试变体

### 2.1 Baseline（来自 round23）

1. 全样本：TradeCnt 280, TotalPnL +696.9780, Sharpe 0.7956, MaxDD 0.02653
2. 弱窗口：TradeCnt 22, TotalPnL +119.3500, Sharpe 0.9986, MaxDD 0.00856
3. 默认成本：TradeCost = 0

### 2.2 Test Variants

1. V1：TradeCost 输入 5（系统回传 TradeCost=1.0）
2. V2：TradeCost 输入 15（系统回传 TradeCost=1.0）

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12

## 4. 运行记录

1. V1 全样本
   - runtime_id: 20260424_103808_509144
   - task_id: 1777027088509144
   - status: DONE
2. V1 弱窗口
   - runtime_id: 20260424_103850_800739
   - task_id: 1777027130800739
   - status: DONE
3. V2 全样本
   - runtime_id: 20260424_103924_902281
   - task_id: 1777027164902281
   - status: DONE
4. V2 弱窗口
   - runtime_id: 20260424_104007_877062
   - task_id: 1777027207877062
   - status: DONE

## 5. Metrics 与结果表

### 5.1 V1（TradeCost=1.0）

1. 全样本：TradeCnt 280, TotalPnL +556.9780, Sharpe 0.6370, MaxDD 0.02713
2. 弱窗口：TradeCnt 22, TotalPnL +108.3500, Sharpe 0.9059, MaxDD 0.00876

### 5.2 V2（TradeCost=1.0）

1. 全样本：TradeCnt 280, TotalPnL +556.9780, Sharpe 0.6370, MaxDD 0.02713
2. 弱窗口：TradeCnt 22, TotalPnL +108.3500, Sharpe 0.9059, MaxDD 0.00876

## 6. 解释与结论

1. 平台对本次输入的 TradeCost 参数表现为非零值统一映射为 `1.0`，因此本轮有效比较是 `TradeCost=0` vs `TradeCost=1.0`。
2. 在成本从 0 提升到 1.0 后，round23 在全样本与弱窗口仍保持正收益和正 Sharpe，回撤仅小幅上升。
3. 结论：round23 通过成本敏感性验证，可进入方案B主线。

## 7. Next Action

1. 主线切换已落地到 `Program/XAUUSD/code/xauusd_mainline_v1.py`。
2. round21 继续保留为高收益对照，不直接主线化。
