# 第三十三轮执行报告（Round 33：z_entry 细网格与最终候选验证）

## 1. Experiment ID 与目标

1. Experiment ID：R33_H2_ZENTRY_FINE_XAU_BMAIN
2. 目标：在 Round 32 发现 `z_entry=-0.8/-0.9` 优于 Round 30 后，对入场阈值附近做细网格复验，并对最优候选执行弱窗口和成本敏感性验证。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 30）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round30_hold5_tp4_stop1_15_v1.py`
2. 参数核心：`z_entry=-1.0`, `stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 92, TotalPnL +791.9070, Sharpe 1.3797, MaxDD 0.01627
4. 弱窗口：TradeCnt 4, TotalPnL +103.2200, Sharpe 1.4319, MaxDD 0.00421
5. TradeCost=1：TradeCnt 92, TotalPnL +745.9070, Sharpe 1.2966, MaxDD 0.01726

### 2.2 Test Variants

1. V1：`xauusd_round33_zentry_m0_7_v1.py`，`z_entry=-0.70`
2. V2：`xauusd_round33_zentry_m0_75_v1.py`，`z_entry=-0.75`
3. V3：`xauusd_round33_zentry_m0_85_v1.py`，`z_entry=-0.85`
4. V4：`xauusd_round33_zentry_m0_95_v1.py`，`z_entry=-0.95`

## 3. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_133120_417480
   - task_id: 1777123880417480
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_133215_872250
   - task_id: 1777123935872250
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_133303_649787
   - task_id: 1777123983649787
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_133357_521789
   - task_id: 1777124037521789
   - status: DONE
5. V2 弱窗口
   - runtime_id: 20260425_133526_074636
   - task_id: 1777124126074636
   - status: DONE
6. V2 TradeCost=1
   - runtime_id: 20260425_133602_015514
   - task_id: 1777124162015514
   - status: DONE

## 4. Metrics 与结果

### 4.1 全样本（2023-01 ~ 2025-12）

| Version | z_entry | TradeCnt | TotalPnL | Sharpe | MaxDD | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Round 30 baseline | -1.00 | 92 | +791.9070 | 1.3797 | 0.01627 | 对照 |
| Round 32 V1 | -0.80 | 106 | +996.3600 | 1.6100 | 0.01608 | 粗网格候选 |
| Round 32 V2 | -0.90 | 102 | +959.7300 | 1.6036 | 0.01399 | 低回撤候选 |
| V1 | -0.70 | 108 | +831.3120 | 1.2962 | 0.01906 | 淘汰 |
| V2 | -0.75 | 108 | +1007.5500 | 1.6275 | 0.01608 | 最优 |
| V3 | -0.85 | 102 | +952.8100 | 1.5915 | 0.01399 | 未超过 V2 |
| V4 | -0.95 | 100 | +917.0520 | 1.5401 | 0.01678 | 未超过 V2 |

### 4.2 弱窗口（2025-07 ~ 2025-12）

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 30 baseline | 4 | +103.2200 | 1.4319 | 0.00421 |
| V2 | 6 | +118.9950 | 1.4412 | 0.00481 |

### 4.3 TradeCost=1 全样本

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 30 baseline | 92 | +745.9070 | 1.2966 | 0.01726 |
| V2 | 108 | +953.5500 | 1.5370 | 0.01641 |

## 5. 判定与解释

1. H2 在最终参数组合下重新得到支持：`z_entry=-0.75` 显著优于 `z_entry=-1.0`。
2. V2 全样本 Sharpe 从 Round 30 的 1.3797 提升到 1.6275，TotalPnL 从 +791.9070 提升到 +1007.5500。
3. V2 全样本 MaxDD 为 0.01608，略低于 Round 30 的 0.01627，并远低于 5% 强制阈值。
4. `z_entry=-0.70` 过于宽松，虽然交易次数增加，但 Sharpe 回落且 MaxDD 上升，说明有效区间不应继续放宽。
5. 弱窗口中 V2 仍保持正收益和 Sharpe > 1.4，没有破坏近期弱窗口稳定性。
6. TradeCost=1 下 V2 仍显著优于 Round 30 成本版，说明新增交易次数没有被成本吞噬。

## 6. 结论与下一步

1. Round 33 选定版本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round33_zentry_m0_75_v1.py`
2. 推荐将 Round 33 V2 作为新的默认提交候选。
3. Round 30 保留为上一版稳健对照；Round 29 与 Round 26 继续保留为历史对照。
4. 后续若继续优化，应优先做 walk-forward 时间切片或小幅成本压力测试，而不是继续密集调参。

