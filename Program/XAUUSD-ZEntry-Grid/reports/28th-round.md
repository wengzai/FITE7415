# 第二十八轮执行报告（Round 28：最大持仓天数网格，H5）

## 1. Experiment ID 与目标

1. Experiment ID：R28_H5_MAX_HOLD_DAYS_XAU_BMAIN
2. 目标：在 Round 26 最优基线（z_entry=-1.0）上，仅调整 `max_hold_days`，验证延长或缩短最大持仓天数是否能改善收益-风险质量。

## 2. Baseline 与测试变体

### 2.1 工作基线（Round 26）

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`
2. 参数核心：`max_hold_days=4`, `z_entry=-1.0`, `stop=1.2xATR`, `take-profit=3.0xATR`
3. 全样本：TradeCnt 100, TotalPnL +601.6870, Sharpe 1.1869, MaxDD 0.01281
4. 弱窗口：TradeCnt 4, TotalPnL +103.9750, Sharpe 1.4424, MaxDD 0.00421

### 2.2 Test Variants

1. V1：`xauusd_round28_hold3_v1.py`，`max_hold_days=3`
2. V2：`xauusd_round28_hold5_v1.py`，`max_hold_days=5`
3. V3：`xauusd_round28_hold6_v1.py`，`max_hold_days=6`

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12（仅对通过全样本筛选的 V2 复验）
3. 成本敏感性：TradeCost=1，全样本

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260425_111422_721822
   - task_id: 1777115662721822
   - status: DONE
2. V2 全样本
   - runtime_id: 20260425_111507_319760
   - task_id: 1777115707319760
   - status: DONE
3. V3 全样本
   - runtime_id: 20260425_111549_418972
   - task_id: 1777115749418972
   - status: DONE
4. V2 弱窗口
   - runtime_id: 20260425_111714_144926
   - task_id: 1777115834144926
   - status: DONE
5. Round 26 TradeCost=1 对照
   - runtime_id: 20260425_111830_599463
   - task_id: 1777115910599463
   - status: DONE
6. V2 TradeCost=1
   - runtime_id: 20260425_111913_353281
   - task_id: 1777115953353281
   - status: DONE

## 5. Metrics 与结果

### 5.1 全样本（2023-01 ~ 2025-12）

| Version | max_hold_days | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: | ---: |
| Round 26 baseline | 4 | 100 | +601.6870 | 1.1869 | 0.01281 |
| V1 | 3 | 112 | +355.1260 | 0.7320 | 0.02106 |
| V2 | 5 | 88 | +630.7600 | 1.1972 | 0.01456 |
| V3 | 6 | 74 | +510.4580 | 0.9516 | 0.01625 |

### 5.2 弱窗口（2025-07 ~ 2025-12）

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 26 baseline | 4 | +103.9750 | 1.4424 | 0.00421 |
| V2 | 4 | +103.2200 | 1.4319 | 0.00421 |

### 5.3 TradeCost=1 全样本

| Version | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | ---: | ---: | ---: | ---: |
| Round 26 baseline | 100 | +551.6870 | 1.0866 | 0.01400 |
| V2 | 88 | +586.7600 | 1.1109 | 0.01556 |

## 6. 判定与解释

1. H5 得到部分支持：将最大持仓天数从 4 天延长到 5 天，在全样本和成本敏感性下均略微提升 TotalPnL 与 Sharpe。
2. V1（3 天）明显过早退出，虽然交易次数增加，但收益和 Sharpe 大幅下降，回撤反而恶化。
3. V3（6 天）信号更稀疏，收益与 Sharpe 均低于基线，说明继续延长持仓会进入边际收益递减。
4. V2 的主要代价是 MaxDD 上升：全样本 MaxDD 从 0.01281 增至 0.01456，TradeCost=1 时增至 0.01556。
5. 弱窗口中 V2 与 Round 26 基本接近但略低，说明 V2 不是稳定碾压版本，而是轻微偏收益的替代候选。

## 7. 结论与下一步

1. Round 28 暂定最优变体：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round28_hold5_v1.py`。
2. 是否替代 Round 26：暂不直接替代。理由是 V2 改进幅度较小（Sharpe 1.1972 vs 1.1869），同时回撤更高、弱窗口略低。
3. 下一步建议：若继续优化，应以 V2 作为“收益偏高候选”进行一轮退出参数验证；若准备交作业，Round 26 仍是更保守的默认提交版本。
