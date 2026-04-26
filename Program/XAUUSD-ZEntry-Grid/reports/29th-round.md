# 第二十九轮执行报告（Round 29：Hold5 下的止盈倍数验证）

## 1. Experiment ID 与目标

1. Experiment ID：R29_H6_TP_MULTIPLE_XAU_BMAIN
2. 目标：在 Round 28 最优变体（`max_hold_days=5`）上，仅调整 `take_profit_atr_multiple`，验证更高止盈倍数是否能释放均值回归收益，同时保持回撤可控。

## 2. Baseline 与测试变体

### 2.1 对照基线

1. Round 26 默认主线：`max_hold_days=4`, `take_profit_atr_multiple=3.0`
   - 全样本：TradeCnt 100, TotalPnL +601.6870, Sharpe 1.1869, MaxDD 0.01281
2. Round 28 Hold5 候选：`max_hold_days=5`, `take_profit_atr_multiple=3.0`
   - 全样本：TradeCnt 88, TotalPnL +630.7600, Sharpe 1.1972, MaxDD 0.01456

### 2.2 Test Variants

1. V1：`xauusd_round29_hold5_tp2_5_v1.py`，TP = 2.5 x ATR
2. V2：`xauusd_round29_hold5_tp3_5_v1.py`，TP = 3.5 x ATR
3. V3：`xauusd_round29_hold5_tp4_0_v1.py`，TP = 4.0 x ATR
4. V4：`xauusd_round29_hold5_tp4_5_v1.py`，TP = 4.5 x ATR
5. V5：`xauusd_round29_hold5_tp5_0_v1.py`，TP = 5.0 x ATR

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12（仅对最优 V3 复验）
3. 成本敏感性：TradeCost=1，全样本（仅对最优 V3 复验）

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_112211_582158
   - task_id: 1777116131582158
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_112258_873829
   - task_id: 1777116178873829
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_112342_612376
   - task_id: 1777116222612376
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_112548_170094
   - task_id: 1777116348170094
   - status: DONE
5. V5 全样本
   - runtime_id: 20260425_112635_004384
   - task_id: 1777116395004384
   - status: DONE
6. V3 弱窗口
   - runtime_id: 20260425_112724_741276
   - task_id: 1777116444741276
   - status: DONE
7. V3 TradeCost=1
   - runtime_id: 20260425_112753_775265
   - task_id: 1777116473775265
   - status: DONE

## 5. Metrics 与结果

### 5.1 全样本（2023-01 ~ 2025-12）

| Version | max_hold_days | TP x ATR | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Round 26 baseline | 4 | 3.0 | 100 | +601.6870 | 1.1869 | 0.01281 |
| Round 28 Hold5 | 5 | 3.0 | 88 | +630.7600 | 1.1972 | 0.01456 |
| V1 | 5 | 2.5 | 88 | +630.7600 | 1.1972 | 0.01456 |
| V2 | 5 | 3.5 | 88 | +630.7600 | 1.1972 | 0.01456 |
| V3 | 5 | 4.0 | 88 | +699.9700 | 1.2913 | 0.01446 |
| V4 | 5 | 4.5 | 88 | +699.9700 | 1.2913 | 0.01446 |
| V5 | 5 | 5.0 | 88 | +699.9700 | 1.2913 | 0.01446 |

### 5.2 弱窗口（2025-07 ~ 2025-12）

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 26 baseline | 4 | +103.9750 | 1.4424 | 0.00421 |
| V3 | 4 | +103.2200 | 1.4319 | 0.00421 |

### 5.3 TradeCost=1 全样本

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 26 baseline | 100 | +551.6870 | 1.0866 | 0.01400 |
| Round 28 Hold5 | 88 | +586.7600 | 1.1109 | 0.01556 |
| V3 | 88 | +655.9700 | 1.2073 | 0.01545 |

## 6. 判定与解释

1. 提高 TP 到 4.0 x ATR 明显改善全样本收益质量：Sharpe 从 Round 26 的 1.1869 提升到 1.2913，TotalPnL 从 +601.6870 提升到 +699.9700。
2. V1 和 V2 与 Round 28 Hold5 完全一致，说明 TP 低于 4.0 时没有改变主要成交路径。
3. V3、V4、V5 完全一致，说明 TP 达到 4.0 后，继续提高止盈倍数不再改变主要退出路径。选择 V3（TP=4.0）更保守、更容易解释。
4. V3 的全样本 MaxDD 为 0.01446，较 Round 26 的 0.01281 上升，但仍明显低于 5% 风险上限，且未超过 Round 28 设定的“MaxDD 不恶化超过 20%”筛选口径。
5. 成本敏感性下，V3 仍优于 Round 26：Sharpe 1.2073 vs 1.0866，TotalPnL +655.9700 vs +551.6870。
6. 弱窗口中，V3 略低于 Round 26，但差异很小，未出现失稳或回撤恶化。

## 7. 结论与下一步

1. Round 29 选定版本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round29_hold5_tp4_0_v1.py`
2. 推荐将 Round 29 V3 作为新的主线候选：
   - 全样本 Sharpe 明显提升。
   - 成本敏感性更强。
   - TradeCnt=88，仍满足统计稳定性要求。
   - MaxDD 虽高于 Round 26，但仍处于低风险区间。
3. 保留 Round 26 作为保守对照版本；若最终报告偏好更低回撤，可继续提交 Round 26，若偏好综合收益-风险质量，则建议提交 Round 29 V3。
