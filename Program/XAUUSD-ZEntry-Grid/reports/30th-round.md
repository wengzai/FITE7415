# 第三十轮执行报告（Round 30：Round 29 主线下的止损倍数验证）

## 1. Experiment ID 与目标

1. Experiment ID：R30_H7_STOP_MULTIPLE_XAU_BMAIN
2. 目标：在 Round 29 最优版本（`max_hold_days=5`, `take_profit_atr_multiple=4.0`）上，仅调整 `stop_atr_multiple`，验证止损距离对收益、回撤和成本敏感性的影响。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 29）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round29_hold5_tp4_0_v1.py`
2. 参数核心：`stop_atr_multiple=1.2`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 88, TotalPnL +699.9700, Sharpe 1.2913, MaxDD 0.01446
4. TradeCost=1：TradeCnt 88, TotalPnL +655.9700, Sharpe 1.2073, MaxDD 0.01545

### 2.2 Test Variants

1. V1：`xauusd_round30_hold5_tp4_stop1_0_v1.py`，Stop = 1.0 x ATR
2. V2：`xauusd_round30_hold5_tp4_stop1_1_v1.py`，Stop = 1.1 x ATR
3. V3：`xauusd_round30_hold5_tp4_stop1_15_v1.py`，Stop = 1.15 x ATR
4. V4：`xauusd_round30_hold5_tp4_stop1_4_v1.py`，Stop = 1.4 x ATR
5. V5：`xauusd_round30_hold5_tp4_stop1_6_v1.py`，Stop = 1.6 x ATR

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12（仅对最优 V3 复验）
3. 成本敏感性：TradeCost=1，全样本（仅对最优 V3 复验）

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_115907_684915
   - task_id: 1777118347684915
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_120529_569527
   - task_id: 1777118729569527
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_120959_251813
   - task_id: 1777118999251813
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_120001_547609
   - task_id: 1777118401547609
   - status: DONE
5. V5 全样本
   - runtime_id: 20260425_120052_747153
   - task_id: 1777118452747153
   - status: DONE
6. V3 弱窗口
   - runtime_id: 20260425_121304_769170
   - task_id: 1777119184769170
   - status: DONE
7. V3 TradeCost=1
   - runtime_id: 20260425_121342_931840
   - task_id: 1777119222931840
   - status: DONE

## 5. Metrics 与结果

### 5.1 全样本（2023-01 ~ 2025-12）

| Version | Stop x ATR | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: | ---: |
| Round 29 baseline | 1.20 | 88 | +699.9700 | 1.2913 | 0.01446 |
| V1 | 1.00 | 98 | +827.4820 | 1.3175 | 0.01931 |
| V2 | 1.10 | 96 | +772.8320 | 1.2955 | 0.01846 |
| V3 | 1.15 | 92 | +791.9070 | 1.3797 | 0.01627 |
| V4 | 1.40 | 68 | +375.8050 | 0.9127 | 0.00972 |
| V5 | 1.60 | 64 | +276.1830 | 0.9491 | 0.00781 |

### 5.2 弱窗口（2025-07 ~ 2025-12）

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 29 baseline | 4 | +103.2200 | 1.4319 | 0.00421 |
| V3 | 4 | +103.2200 | 1.4319 | 0.00421 |

### 5.3 TradeCost=1 全样本

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 29 baseline | 88 | +655.9700 | 1.2073 | 0.01545 |
| V3 | 92 | +745.9070 | 1.2966 | 0.01726 |

## 6. 判定与解释

1. H7 得到支持：在 Round 29 的 TP4.0 / Hold5 框架下，适度收紧止损到 1.15 x ATR 能显著提升全样本收益和 Sharpe。
2. V1（Stop=1.0）收益最高，但 MaxDD 上升到 0.01931，超过相对 Round 29 的 20% 回撤恶化守门线，不直接主线化。
3. V2（Stop=1.1）也有收益提升，但 MaxDD 为 0.01846，风险改善不如 V3 平衡。
4. V3（Stop=1.15）在收益和风险之间最均衡：
   - Sharpe 1.3797，高于 Round 29 的 1.2913。
   - TotalPnL +791.9070，高于 Round 29 的 +699.9700。
   - MaxDD 0.01627，相比 Round 29 增幅约 12.5%，仍在 20% 守门线内。
5. V4/V5 表明止损过宽会显著减少有效交易和收益质量，虽然回撤下降，但 Sharpe 不足。
6. 成本敏感性中 V3 仍保持较强表现：TradeCost=1 下 Sharpe 1.2966，TotalPnL +745.9070。
7. 弱窗口中 V3 与 Round 29 完全一致，说明该改动没有破坏近期弱窗口稳定性。

## 7. 结论与下一步

1. Round 30 选定版本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round30_hold5_tp4_stop1_15_v1.py`
2. 推荐将 Round 30 V3 作为新的默认提交候选。
3. Round 29 保留为低回撤对照版本；Round 26 保留为更保守的历史 winner 对照。
4. 后续如继续优化，建议只做稳健性复验（例如 SMA 窗口小网格或 walk-forward 时间切片），避免继续追求单一样本指标而过拟合。
