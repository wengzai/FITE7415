# B-mainline Optimization Closeout

## 1. 执行范围

1. 自动执行轮次：Round 25 -> Round 27（授权窗口 round25-round39 内提前收官）。
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

## 3. 最终选定主线

1. 选定脚本：`Program/B-mainline/code/xauusd_round26_zentry_m1_0_v1.py`
2. 选定理由：
   - 相比 round23，Sharpe 明显提升（1.1869 > 0.7956）。
   - MaxDD 明显下降（0.01281 < 0.02653）。
   - 全样本 TradeCnt=100，满足统计稳定性要求（>=50）。

## 4. 风险与现实性说明

1. 回撤约束：满足（MaxDD 显著低于 5% 强制阈值）。
2. 单笔风险：保持 0.5% 初始资金，未放大杠杆。
3. 成本敏感性：round24 已验证在 TradeCost=1.0 下仍为正收益。

## 5. 收官判定

1. 已达到 B-mainline 目标：获得一版较基线显著更优且风险更低的主线版本。
2. 触发提前收官原因：
   - 已出现可落地主线（Round 26）。
   - 后续一轮（Round 27）未带来增益，进入边际收益递减阶段。

## 6. 后续可选研究（非本轮必做）

1. H4（SMA 窗口网格）作为稳健性复验而非主线必要步骤。
2. H5（持仓天数）仅在 H4 出现稳定改进时再做联合验证。
