# 第三十四轮执行报告（Round 34：Round 33 主线下的 TP 倍数复验）

## 1. Experiment ID 与目标

1. Experiment ID：R34_H6_TP_FINE_XAU_BMAIN
2. 目标：在 Round 33 最优版本（`z_entry=-0.75`, `stop_atr_multiple=1.15`, `max_hold_days=5`）上，仅调整 `take_profit_atr_multiple`，验证止盈倍数是否仍应保持在 4.0 x ATR 附近。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 33）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round33_zentry_m0_75_v1.py`
2. 参数核心：`z_entry=-0.75`, `stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 108, TotalPnL +1007.5500, Sharpe 1.6275, MaxDD 0.01608

### 2.2 Test Variants

1. V1：`xauusd_round34_tp3_0_v1.py`，TP = 3.0 x ATR
2. V2：`xauusd_round34_tp3_5_v1.py`，TP = 3.5 x ATR
3. V3：`xauusd_round34_tp4_5_v1.py`，TP = 4.5 x ATR
4. V4：`xauusd_round34_tp5_0_v1.py`，TP = 5.0 x ATR

## 3. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_142650_837087
   - task_id: 1777127210837087
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_142743_589147
   - task_id: 1777127263589147
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_142834_193925
   - task_id: 1777127314193925
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_142924_808057
   - task_id: 1777127364808057
   - status: DONE

## 4. Metrics 与结果

| Version | TP x ATR | TradeCnt | TotalPnL | Sharpe | MaxDD | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Round 33 baseline | 4.0 | 108 | +1007.5500 | 1.6275 | 0.01608 | 当前主线 |
| V1 | 3.0 | 108 | +938.3400 | 1.5487 | 0.01619 | 未超过主线 |
| V2 | 3.5 | 108 | +938.3400 | 1.5487 | 0.01619 | 未超过主线 |
| V3 | 4.5 | 108 | +1007.5500 | 1.6275 | 0.01608 | 与主线相同 |
| V4 | 5.0 | 108 | +1007.5500 | 1.6275 | 0.01608 | 与主线相同 |

## 5. 判定与解释

1. TP=3.0/3.5 过早截断盈利，PnL 与 Sharpe 均低于 Round 33。
2. TP=4.0/4.5/5.0 结果完全一致，说明当前交易路径中有效止盈触发已经不再区分 4.0 以上的 TP。
3. 出于参数简洁和避免无意义放大的考虑，继续保留 `take_profit_atr_multiple=4.0`。
4. Round 34 未产生新的主线替换版本。

