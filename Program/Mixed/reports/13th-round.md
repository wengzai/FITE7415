# 第十三轮执行报告（Round 13, Step 2 到 Step 5）

## 0. 执行目标

按新指令执行：

1. 固定双基线（Baseline-P: round5B, Baseline-R: round11）。
2. 继续方案A主线（BTCUSD），本轮仅改一个模块。
3. 开启方案B影子验证（XAUUSD），冻结参数迁移，不调参。
4. 输出是否进入方案B的结论。

## 1. Step 2：策略改动与验证设计

### 1.1 方案A主线（BTCUSD）

脚本：Program/BTCUSD/code/btcusd_round13_regime_v1.py

本轮单模块改动：

1. 新增标准化波动带宽过滤（bandwidth = std20 / sma20）。
2. 仅在 bandwidth ∈ [0.008, 0.09] 时允许交易。

其余参数与 round11 保持一致：

1. trend_period = 80
2. z_entry = -1.0
3. stop_atr_multiple = 1.2
4. take_profit_atr_multiple = 3.0
5. max_hold_days = 4

### 1.2 方案B影子验证（XAUUSD）

脚本：Program/XAUUSD/code/xauusd_round13_shadow_v1.py

执行方式：

1. 将 round13 冻结参数直接迁移到 XAUUSD。
2. 不做任何为 XAUUSD 定制调参。

## 2. Step 3：实验记录

1. BTCUSD 全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_093058_559524
   - task_id: 1777023058559524
   - status: DONE
2. BTCUSD 弱窗口（2025-07 到 2025-12）
   - runtime_id: 20260424_093149_734336
   - task_id: 1777023109734336
   - status: DONE
3. XAUUSD 影子全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_093226_290501
   - task_id: 1777023146290501
   - status: DONE

## 3. Step 4：结果

### 3.1 方案A主线结果（BTCUSD）

1. 全样本：TradeCnt 60, TotalPnL +314.9233, AnnualSharpe 0.3630, MaxDrawdownPct 0.03562
2. 弱窗口：TradeCnt 8, TotalPnL +52.3786, AnnualSharpe 0.4833, MaxDrawdownPct 0.00657

对比 Baseline-R（round11）：

1. 指标等同（可视为无增量改进）。
2. 说明本轮新增带宽过滤在当前区间中未产生实质影响。

### 3.2 方案B影子结果（XAUUSD）

1. 全样本：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0

解释：

1. 冻结参数直接迁移后，触发条件未命中，策略在 XAUUSD 上几乎不可交易。
2. 这属于“迁移可行性不足”，不是“XAUUSD一定无效”的结论。

## 4. Step 5：结论与决策

1. 方案A主线：round13 单模块改动未超过双基线，判定为无增量样本。
2. 方案B影子：冻结参数迁移到 XAUUSD 后交易不可触发，当前不具备直接切换主线条件。
3. 决策：暂不进入方案B，继续维持“方案A主线 + 方案B影子验证”框架。

## 5. 下一步建议

1. 若继续做方案B影子验证，先只放宽一个触发阈值（例如 z_entry 或 bandwidth 下限）做最小可交易性修复。
2. 继续要求新方案同时对比 Baseline-P 与 Baseline-R，且满足“全样本 + 弱窗口”双维度改进后再评审新基线。
