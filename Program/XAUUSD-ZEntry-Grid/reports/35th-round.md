# 第三十五轮执行报告（Round 35：Round 33 主线下的 Stop 倍数细网格）

## 1. Experiment ID 与目标

1. Experiment ID：R35_H7_STOP_FINE_XAU_BMAIN
2. 目标：在 Round 33 最优版本（`z_entry=-0.75`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`）上，仅调整 `stop_atr_multiple`，验证是否可以进一步提升 Sharpe 并降低回撤。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 33）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round33_zentry_m0_75_v1.py`
2. 参数核心：`z_entry=-0.75`, `stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 108, TotalPnL +1007.5500, Sharpe 1.6275, MaxDD 0.01608
4. 弱窗口：TradeCnt 6, TotalPnL +118.9950, Sharpe 1.4412, MaxDD 0.00481
5. TradeCost=1：TradeCnt 108, TotalPnL +953.5500, Sharpe 1.5370, MaxDD 0.01641

### 2.2 Test Variants

1. V1：`xauusd_round35_stop1_05_v1.py`，Stop = 1.05 x ATR
2. V2：`xauusd_round35_stop1_10_v1.py`，Stop = 1.10 x ATR
3. V3：`xauusd_round35_stop1_20_v1.py`，Stop = 1.20 x ATR
4. V4：`xauusd_round35_stop1_25_v1.py`，Stop = 1.25 x ATR

## 3. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_143318_836831
   - task_id: 1777127598836831
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_143434_477152
   - task_id: 1777127674477152
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_143734_276194
   - task_id: 1777127854276194
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_143849_536383
   - task_id: 1777127929536383
   - status: DONE
5. V2 弱窗口
   - runtime_id: 20260425_144001_381627
   - task_id: 1777128001381627
   - status: DONE
6. V2 TradeCost=1
   - runtime_id: 20260425_144037_465128
   - task_id: 1777128037465128
   - status: DONE

## 4. Metrics 与结果

### 4.1 全样本（2023-01 ~ 2025-12）

| Version | Stop x ATR | TradeCnt | TotalPnL | Sharpe | MaxDD | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Round 33 baseline | 1.15 | 108 | +1007.5500 | 1.6275 | 0.01608 | 对照 |
| V1 | 1.05 | 112 | +1077.0950 | 1.7011 | 0.01292 | 高 PnL 候选 |
| V2 | 1.10 | 112 | +1071.3050 | 1.7139 | 0.01293 | 最优 |
| V3 | 1.20 | 104 | +899.5230 | 1.5418 | 0.01607 | 淘汰 |
| V4 | 1.25 | 100 | +818.6580 | 1.5399 | 0.01302 | 淘汰 |

### 4.2 弱窗口（2025-07 ~ 2025-12）

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 33 baseline | 6 | +118.9950 | 1.4412 | 0.00481 |
| V2 | 8 | +183.4650 | 2.1019 | 0.00418 |

### 4.3 TradeCost=1 全样本

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 33 baseline | 108 | +953.5500 | 1.5370 | 0.01641 |
| V2 | 112 | +1015.3050 | 1.6207 | 0.01323 |

## 5. 判定与解释

1. H7 再次得到支持：在 Round 33 的 `z_entry=-0.75` 框架下，适度收紧止损可以同时提升 Sharpe、PnL，并降低 MaxDD。
2. V1 的 PnL 最高，但 V2 的 Sharpe 更高；两者 MaxDD 几乎相同。按风险调整后收益优先，选择 V2。
3. V3/V4 说明止损放宽到 1.20 以上会降低有效交易和收益质量。
4. V2 弱窗口显著优于 Round 33，且 TradeCost=1 下仍保持 Sharpe > 1.6。

## 6. 结论与下一步

1. Round 35 选定版本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py`
2. 推荐将 Round 35 V2 作为新的默认提交候选。
3. Round 33 保留为上一版主线对照；Round 30/29/26 继续保留为历史对照。
4. 已完成用户要求的两轮扩展至 Round 35。后续若继续到 Round 40，建议转向 walk-forward 时间切片、TradeCost 压力测试和参数稳定性复验，而不是继续单一样本密集调参。

