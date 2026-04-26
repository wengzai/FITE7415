# 第三十一轮执行报告（Round 31：Round 30 主线下的 SMA/std 窗口复验）

## 1. Experiment ID 与目标

1. Experiment ID：R31_H4_SMA_STD_WINDOW_XAU_BMAIN
2. 目标：在 Round 30 最优版本（`stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`）上，仅调整 `sma_period` 与 `std_period`，验证均值回归观察窗口是否仍以 20 日为最优。

## 2. Baseline 与测试变体

### 2.1 对照基线（Round 30）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round30_hold5_tp4_stop1_15_v1.py`
2. 参数核心：`sma_period=20`, `std_period=20`, `stop_atr_multiple=1.15`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 全样本：TradeCnt 92, TotalPnL +791.9070, Sharpe 1.3797, MaxDD 0.01627

### 2.2 Test Variants

1. V1：`xauusd_round31_sma15_v1.py`，SMA/std = 15
2. V2：`xauusd_round31_sma25_v1.py`，SMA/std = 25
3. V3：`xauusd_round31_sma30_v1.py`，SMA/std = 30
4. V4：`xauusd_round31_sma40_v1.py`，SMA/std = 40

## 3. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_123826_722703
   - task_id: 1777120706722703
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_132106_219798
   - task_id: 1777123266219798
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_132156_495819
   - task_id: 1777123316495819
   - status: DONE
4. V4 全样本
   - runtime_id: 20260425_132242_765866
   - task_id: 1777123362765866
   - status: DONE

## 4. Metrics 与结果

### 4.1 全样本（2023-01 ~ 2025-12）

| Version | SMA/std window | TradeCnt | TotalPnL | Sharpe | MaxDD | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Round 30 baseline | 20 | 92 | +791.9070 | 1.3797 | 0.01627 | 当前主线 |
| V1 | 15 | 96 | +511.8130 | 0.8693 | 0.02385 | 淘汰 |
| V2 | 25 | 78 | +655.5100 | 1.2566 | 0.01519 | 未超过主线 |
| V3 | 30 | 74 | +590.0720 | 1.1604 | 0.01595 | 未超过主线 |
| V4 | 40 | 62 | +466.4170 | 0.9517 | 0.01856 | 淘汰 |

## 5. 初步判定

1. V1（SMA/std=15）明显劣于 Round 30：Sharpe 从 1.3797 降到 0.8693，MaxDD 从 0.01627 升到 0.02385。
2. V2（SMA/std=25）回撤略低于 Round 30，但 PnL 与 Sharpe 都下降，不满足主线替换标准。
3. V3/V4 说明窗口继续拉长会减少交易次数并降低收益质量。
4. H4 在 Round 30 最优参数组合下未得到支持；20 日窗口仍是当前最优均值回归观察窗口。
5. 当前不能替换主线；Round 30 继续作为默认提交候选。
