# 第三十二轮执行报告（Round 32：Round 30 主线下的 z_entry 粗网格）

## 1. Experiment ID 与目标

1. Experiment ID：R32_H2_ZENTRY_COARSE_XAU_BMAIN
2. 目标：在 Round 30 最优版本（`stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`）上，重新测试入场 z-score 阈值附近的粗网格，判断 `z_entry=-1.0` 是否仍是最优。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 30）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round30_hold5_tp4_stop1_15_v1.py`
2. 参数核心：`z_entry=-1.0`, `stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 92, TotalPnL +791.9070, Sharpe 1.3797, MaxDD 0.01627

### 2.2 Test Variants

1. V1：`xauusd_round32_zentry_m0_8_v1.py`，`z_entry=-0.8`
2. V2：`xauusd_round32_zentry_m0_9_v1.py`，`z_entry=-0.9`
3. V3：`xauusd_round32_zentry_m1_1_v1.py`，`z_entry=-1.1`

## 3. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_132651_347935
   - task_id: 1777123611347935
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_132740_917526
   - task_id: 1777123660917526
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_132836_676060
   - task_id: 1777123716676060
   - status: DONE

## 4. Metrics 与结果

| Version | z_entry | TradeCnt | TotalPnL | Sharpe | MaxDD | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Round 30 baseline | -1.00 | 92 | +791.9070 | 1.3797 | 0.01627 | 对照 |
| V1 | -0.80 | 106 | +996.3600 | 1.6100 | 0.01608 | 粗网格最优 |
| V2 | -0.90 | 102 | +959.7300 | 1.6036 | 0.01399 | 低回撤候选 |
| V3 | -1.10 | 86 | +688.7580 | 1.2160 | 0.01791 | 淘汰 |

## 5. 判定与解释

1. `z_entry=-0.8` 与 `z_entry=-0.9` 均显著优于 Round 30，说明在新的止损/止盈/持仓组合下，入场阈值可以适度放宽。
2. `z_entry=-1.1` 交易更少但收益质量下降，说明继续收紧入场条件会错过有效均值回归机会。
3. `z_entry=-0.8` 的 PnL 和 Sharpe 更高；`z_entry=-0.9` 的 MaxDD 更低。两者都值得进入 Round 33 细网格。

## 6. 下一步

围绕 `-0.8` 附近继续细化测试：`z_entry ∈ {-0.70, -0.75, -0.85, -0.95}`。

