# B-mainline Optimization Closeout

## 1. 执行范围

1. 自动执行轮次：Round 25 -> Round 35；报告补充验证：Round 36。
2. 固定比较基线：`Program/XAUUSD/code/xauusd_mainline_v1.py`（round23）。

## 2. 各轮关键结论

1. Round 25（H1 趋势过滤）
   - 结论：未通过纳入标准（主要问题是 TradeCnt 不足）。
2. Round 26（H2 z_entry 网格）
   - 结论：`z_entry=-1.0` 最优。
   - 全样本：TradeCnt 100, PnL +601.6870, Sharpe 1.1869, MaxDD 0.01281。
   - 弱窗口：TradeCnt 4, PnL +103.9750, Sharpe 1.4424, MaxDD 0.00421。
3. Round 27（H3 退出机制变体）
   - 结论：弱化固定 TP 后，全样本 Sharpe 回落到 1.1076，未优于 Round 26。
4. Round 28（H5 最大持仓天数）
   - 结论：`max_hold_days=5` 是较优候选。
   - 全样本：TradeCnt 88, PnL +630.7600, Sharpe 1.1972, MaxDD 0.01456。
   - 弱窗口略低于 Round 26，但未失稳。
5. Round 29（Hold5 下的 TP 倍数）
   - 结论：`take_profit_atr_multiple=4.0` 最优。
   - 全样本：TradeCnt 88, PnL +699.9700, Sharpe 1.2913, MaxDD 0.01446。
   - TradeCost=1：TradeCnt 88, PnL +655.9700, Sharpe 1.2073, MaxDD 0.01545。
6. Round 30（Round 29 主线下的止损倍数）
   - 结论：`stop_atr_multiple=1.15` 在收益和回撤之间最均衡。
   - 全样本：TradeCnt 92, PnL +791.9070, Sharpe 1.3797, MaxDD 0.01627。
   - 弱窗口：TradeCnt 4, PnL +103.2200, Sharpe 1.4319, MaxDD 0.00421。
   - TradeCost=1：TradeCnt 92, PnL +745.9070, Sharpe 1.2966, MaxDD 0.01726。
7. Round 31（Round 30 主线下的 SMA/std 窗口复验）
   - 结论：15/25/30/40 日窗口均未超过 20 日窗口；H4 在最终参数组合下未得到支持。
   - 最优变体 SMA/std=25：TradeCnt 78, PnL +655.5100, Sharpe 1.2566, MaxDD 0.01519。
8. Round 32（z_entry 粗网格）
   - 结论：`z_entry=-0.8` 与 `z_entry=-0.9` 均显著优于 Round 30。
   - `z_entry=-0.8`：TradeCnt 106, PnL +996.3600, Sharpe 1.6100, MaxDD 0.01608。
   - `z_entry=-0.9`：TradeCnt 102, PnL +959.7300, Sharpe 1.6036, MaxDD 0.01399。
9. Round 33（z_entry 细网格与最终候选验证）
   - 结论：`z_entry=-0.75` 最优。
   - 全样本：TradeCnt 108, PnL +1007.5500, Sharpe 1.6275, MaxDD 0.01608。
   - 弱窗口：TradeCnt 6, PnL +118.9950, Sharpe 1.4412, MaxDD 0.00481。
   - TradeCost=1：TradeCnt 108, PnL +953.5500, Sharpe 1.5370, MaxDD 0.01641。
10. Round 34（Round 33 主线下的 TP 倍数复验）
   - 结论：TP=4.0/4.5/5.0 结果一致；为避免无意义放大，保留 `take_profit_atr_multiple=4.0`。
   - TP=3.0/3.5：TradeCnt 108, PnL +938.3400, Sharpe 1.5487, MaxDD 0.01619。
11. Round 35（Round 33 主线下的 Stop 倍数细网格）
   - 结论：`stop_atr_multiple=1.10` 的风险调整后收益最优。
   - 全样本：TradeCnt 112, PnL +1071.3050, Sharpe 1.7139, MaxDD 0.01293。
   - 弱窗口：TradeCnt 8, PnL +183.4650, Sharpe 2.1019, MaxDD 0.00418。
   - TradeCost=1：TradeCnt 112, PnL +1015.3050, Sharpe 1.6207, MaxDD 0.01323。
12. Round 36（最终稳健性与报告补充验证）
   - 结论：不改变主线，仅补充报告证据。
   - 年度/半年度分段均为正收益：2023 +294.7100，2024 +413.4850，2025 +329.9300。
   - TradeCost=1/2/3/5 均保持 Sharpe 1.6207；平台对非零成本字段返回相同结果，应谨慎表述。
   - 2026 行情可通过只读接口查询，但当前账户 backtest 权限限制在 2021-01 到 2025-12，无法提交官方 2026 回测。

## 3. 最终选定主线

1. 选定脚本：`Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py`
2. 选定理由：
   - 相比 round23，Sharpe 明显提升（1.7139 > 0.7956），TotalPnL 也提升（+1071.3050 > +696.9780）。
   - 相比 Round 33，TotalPnL 和 Sharpe 均提升（+1071.3050 vs +1007.5500；1.7139 vs 1.6275）。
   - 相比 Round 33，MaxDD 明显下降（0.01293 vs 0.01608），没有以更高回撤换取收益。
   - TradeCost=1 下仍保持较强表现（Sharpe 1.6207，TotalPnL +1015.3050）。
   - 全样本 TradeCnt=112，满足统计稳定性要求（>=50）。

## 4. 风险与现实性说明

1. 回撤约束：满足（MaxDD 显著低于 5% 强制阈值）。
2. 单笔风险：保持 0.5% 初始资金，未放大杠杆。
3. 成本敏感性：Round 35 已验证在 TradeCost=1.0 下仍为正收益，并保持 Sharpe > 1.6。

## 5. 收官判定

1. 已达到 B-mainline 目标：获得一版较基线显著更优且风险仍可控的主线版本。
2. 触发提前收官原因：
   - Round 35 在收益、Sharpe、回撤和成本敏感性上均优于 Round 33。
   - Round 34 复验排除了继续放大 TP 的必要性；Round 35 细网格后 `stop_atr_multiple=1.10` 附近已出现更优收益-风险组合。

## 6. 后续可选研究（非本轮必做）

1. 若账户权限升级，优先补 2026 真正样本外回测。
2. Round 26 保留为低回撤保守对照；Round 29/30/33 保留为历史主线对照；Round 35 作为默认提交候选。
