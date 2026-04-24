# 第八轮执行报告（Round 8, Step 2 到 Step 5）

## 0. 执行目标

执行策略性改动（非仅参数微调）：将单向均值回归升级为双向均值回归（多空都做），验证是否能在更高交易活跃度下带来更好的风险收益。

## 1. Step 2：策略改动

脚本：Program/BTCUSD/code/btcusd_round8_biside_v1.py

本轮核心改动：

1. 启用双向入场：
   - `zscore <= -1.2` 做多
   - `zscore >= +1.2` 做空
2. 回测设置 `allowShortSell = true`
3. 多空分别使用对称 ATR 风控（stop 1.2ATR, TP 3.0ATR）

## 2. Step 3：实验记录

1. runtime_id: 20260423_150456_081181
2. task_id: 1776956696081181
3. status: DONE

## 3. Step 4：结果

1. TradeCnt: 232
2. TotalPnL: -697.3774
3. AnnualSharpe: -0.2989
4. MaxDrawdownPct: 0.11835
5. ProfitFactor: 0.8518

对比 round5B：

1. 交易次数大幅增加，但收益和 Sharpe 显著转负。
2. 最大回撤明显恶化。
3. 收益质量劣化幅度远超样本量提升收益。

## 4. Step 5：停止判断

决策：在本次任务内停止继续 round9+。

理由：

1. round5B 已形成当前最优解（PnL/Sharpe/回撤综合最优）。
2. 后续两次结构性/策略性改动（round7, round8）均显著劣化。
3. 当前可尝试变更已从参数微调扩展到结构改造与策略改造，仍未超越 round5B，边际收益显著递减。
4. 满足“已经没有有效新改动可短期验证”的停止条件。

## 5. 方向跟踪与 hard 条件

1. 方向S（状态过滤模块）：1次尝试失败。
2. 方向T（双向策略改造）：1次尝试失败。
3. 尚无方向达到“连续3轮失败”，因此未触发 hard.md 写入条件。

## 6. 推荐保留版本

建议将当前策略候选基线固定为 round5B：

1. 脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py
2. 指标：TradeCnt 114, TotalPnL +545.7112, AnnualSharpe 0.4182, MaxDrawdownPct 0.04102
