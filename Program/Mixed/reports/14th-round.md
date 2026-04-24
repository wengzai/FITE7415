# 第十四轮执行报告（Round 14, Step 2 到 Step 5）

## 0. 执行目标

在多轮自动化授权下继续方案A主线优化，并保留方案B影子验证。

本轮目标：

1. 方案A（BTCUSD）只改一个模块，评估是否可在“全样本 + 弱窗口”双维度优于稳健基线。
2. 方案B（XAUUSD）执行最小可交易性修复（只改一个阈值），观察迁移可行性。

## 1. Step 2：策略改动

### 1.1 方案A主线（BTCUSD）

脚本：Program/BTCUSD/code/btcusd_round14_regime_v2.py

单模块改动：

1. 将带宽过滤下限从 0.008 提高到 0.012（上限 0.09 保持不变）。
2. 其他参数保持与 round13/round11 一致。

### 1.2 方案B影子（XAUUSD）

脚本：Program/XAUUSD/code/xauusd_round14_shadow_fix_v1.py

最小修复改动：

1. 仅将 z_entry 从 -1.0 放宽到 -0.6。
2. 其余冻结参数不变。

## 2. Step 3：实验记录

1. BTCUSD 全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_094431_596140
   - task_id: 1777023871596140
   - status: DONE
2. BTCUSD 弱窗口（2025-07 到 2025-12）
   - runtime_id: 20260424_094525_114647
   - task_id: 1777023925114647
   - status: DONE
3. XAUUSD 影子全样本（2023-01 到 2025-12）
   - runtime_id: 20260424_094551_467297
   - task_id: 1777023951467297
   - status: DONE

## 3. Step 4：结果

### 3.1 方案A主线结果（BTCUSD）

1. 全样本：TradeCnt 58, TotalPnL +341.4714, AnnualSharpe 0.3949, MaxDrawdownPct 0.03738
2. 弱窗口：TradeCnt 8, TotalPnL +97.1492, AnnualSharpe 0.9423, MaxDrawdownPct 0.00652

对比 Baseline-R（round11）：

1. 全样本 PnL、Sharpe 提升，TradeCnt 略降，回撤略增。
2. 弱窗口 PnL、Sharpe 明显提升，回撤保持低位。

对比 Baseline-P（round5B）：

1. 仍未达到 Baseline-P 的全样本收益规模与交易频次。
2. 但稳健性维度（弱窗口）显著更优。

### 3.2 方案B影子结果（XAUUSD）

1. 全样本：TradeCnt 0, TotalPnL 0, AnnualSharpe 0, MaxDrawdownPct 0

结论：

1. 单阈值修复未解决 XAUUSD 可交易性问题。
2. 方案B仍不具备主线切换条件。

## 4. Step 5：结论

1. round14 是方案A在自动化阶段的有效改进样本。
2. 其在“全样本 + 弱窗口”双维度上相对 Baseline-R 达到可接受改进。
3. 方案B影子验证持续失败（零交易），暂不切换主线。

## 5. 下一步建议

1. 维持双基线框架，并将 round14 作为新的“稳健候选版本”参与后续评审。
2. 方案B若继续，建议下一轮先放宽 bandwidth 上限或下限之一（仍保持单变量改动）。
