# 第三十六轮执行报告（Round 36：最终稳健性与报告补充验证）

## 1. Experiment ID 与目标

1. Experiment ID：R36_FINAL_ROBUSTNESS_XAU_BMAIN
2. 目标：不再调参，仅使用 Round 35 最终主线，补充老师报告模板所需的稳健性证据，包括年度/半年度分段、交易成本压力和 2026 样本外可用性检查。

## 2. 固定策略版本

1. 脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py`
2. 参数核心：`z_entry=-0.75`, `stop_atr_multiple=1.10`, `take_profit_atr_multiple=4.0`, `max_hold_days=5`
3. 注意：Round 36 不用于选择参数，只用于报告验证。

## 3. 分段稳健性检查

| Segment | runtime_id | task_id | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 2023 | 20260426_035022_658883 | 1777175422658883 | 56 | +294.7100 | 1.2433 | 0.0121 |
| 2024 | 20260426_035052_208538 | 1777175452208538 | 41 | +413.4850 | 2.1100 | 0.0133 |
| 2025 | 20260426_035123_341698 | 1777175483341698 | 14 | +329.9300 | 2.1762 | 0.0065 |
| 2025H1 | 20260426_035158_657524 | 1777175518657524 | 7 | +89.2300 | 1.5918 | 0.0065 |
| 2025H2 | 20260425_144001_381627 | 1777128001381627 | 8 | +183.4650 | 2.1019 | 0.0042 |

### 判定

1. 所有年度/半年度分段均为正收益。
2. 2023 Sharpe 相对最低，但仍高于 1.2，说明策略不是只依赖 2024 或 2025 的单一行情。
3. 2025 交易次数较少，因此不能过度解读其 Sharpe；但它能说明最终主线在最近样本内没有失效。
4. 这些分段属于 sample 内稳健性检查，不是严格样本外验证，因为参数选择使用了 2023-2025 主样本。

## 4. 成本压力测试

| Setting | runtime_id | task_id | TradeCnt | TotalPnL | Sharpe | MaxDD |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Base | 20260425_143434_477152 | 1777127674477152 | 112 | +1071.3050 | 1.7139 | 0.0129 |
| TradeCost=1 | 20260425_144037_465128 | 1777128037465128 | 112 | +1015.3050 | 1.6207 | 0.0132 |
| TradeCost=2 | 20260426_035227_560804 | 1777175547560804 | 112 | +1015.3050 | 1.6207 | 0.0132 |
| TradeCost=3 | 20260426_035311_361895 | 1777175591361895 | 112 | +1015.3050 | 1.6207 | 0.0132 |
| TradeCost=5 | 20260426_035403_417028 | 1777175643417028 | 112 | +1015.3050 | 1.6207 | 0.0132 |

### 判定

1. 启用交易成本后，策略仍保持 TotalPnL > +1000 和 Sharpe > 1.6。
2. `TradeCost=1/2/3/5` 返回相同结果。提交参数文件已确认分别包含对应 TradeCost 数值，因此推测 ALGOGENE 当前账户或 API 路径可能将该字段按固定成本档处理，而不是线性按数值放大。
3. 报告中应谨慎表述为“non-zero transaction cost stress”，不要声称已经验证线性成本曲线。

## 5. 2026 样本外验证限制

1. 使用 `get_history_price` 只读接口检查，ALGOGENE 已有 XAUUSD 2026 日线行情，查询到 2026 bars，并且最近日期可到 2026-04-25。
2. 但是用当前账户提交 `2026-01 ~ 2026-04` backtest 时，平台拒绝并返回：

```text
Your account only allow StartDate and EndDate within '2021-01' to '2025-12'.
```

3. 因此，本项目不能在当前 ALGOGENE 账户权限下生成官方 2026 backtest 结果。
4. 最终报告应诚实说明：2026 是未来样本外验证的理想方向，但当前账户权限限制导致无法纳入正式回测结果。

## 6. 图表与报告素材

已生成最终报告素材目录：

```text
Program/XAUUSD-ZEntry-Grid/final_report/
```

包含：

1. `Final_Report.md`
2. `assets/equity_curve.svg`
3. `assets/drawdown_curve.svg`
4. `assets/monthly_pnl.svg`
5. `monthly_pnl.md`
6. `segment_robustness.md`
7. `cost_stress.md`
8. `summary_metrics.md`

## 7. 结论

Round 36 不改变主线。最终提交候选仍为：

```text
Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py
```

补充验证增强了报告模板中的 Backtest Performance、Risk Management、Capital Management 和 Expectations for Real Trading 章节证据。下一步不建议继续调参，应进入最终报告排版与提交材料整理。

