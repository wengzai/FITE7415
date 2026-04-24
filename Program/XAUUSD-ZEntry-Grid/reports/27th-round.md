# 第二十七轮执行报告（Round 27：退出机制对比，H3）

## 1. Experiment ID 与目标

1. Experiment ID：R27_H3_EXIT_MECHANISM_XAU_BMAIN
2. 目标：在 Round 26 最优基线（z_entry=-1.0）上，验证“弱化固定止盈（近似 trailing 思路）”是否能提升全样本收益质量。

## 2. Baseline 与测试变体

### 2.1 工作基线（来自 Round 26 最优）

1. 参数核心：z_entry=-1.0, stop=1.2xATR, take-profit=3.0xATR
2. 全样本：TradeCnt 100, TotalPnL +601.6870, Sharpe 1.1869, MaxDD 0.01281
3. 弱窗口：TradeCnt 4, TotalPnL +103.9750, Sharpe 1.4424, MaxDD 0.00421

### 2.2 Test Variant

1. V1：take_profit_atr_multiple 从 3.0 调整为 100.0（弱化固定止盈），其余参数不变。

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260424_113847_575360
   - task_id: 1777030727575360
   - status: DONE
2. V1 弱窗口
   - runtime_id: 20260424_113922_429146
   - task_id: 1777030762429146
   - status: DONE

## 5. Metrics 与结果

1. V1 全样本：TradeCnt 100, TotalPnL +566.3470, Sharpe 1.1076, MaxDD 0.01285
2. V1 弱窗口：TradeCnt 4, TotalPnL +103.9750, Sharpe 1.4424, MaxDD 0.00421

## 6. 判定与解释

1. 与基线相比，V1 全样本收益与 Sharpe 均下降（Sharpe 1.1869 -> 1.1076），回撤未改善。
2. 弱窗口结果与基线基本一致，说明该窗口中固定 TP 不是主要约束。
3. H3 本轮结论：不支持当前退出机制变体，保留 Round 26 版本作为主线。

## 7. Next Action

1. 当前已获得显著优于 round23 的稳定版本（Sharpe 与 MaxDD 双改善，且 TradeCnt 充足）。
2. 若继续推进可进入 H4（SMA 窗口网格），但需警惕过拟合与边际收益递减。
