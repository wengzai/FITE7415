# 第六轮执行报告（Round 6, Step 2 到 Step 5）

## 0. 执行目标

沿 round5 胜出方向（Exit Structure）做第二次迭代，验证是否仍有显著增益。

## 1. Step 2：策略改动

脚本：Program/BTCUSD/code/btcusd_round6_exit_v2.py

本轮唯一改动：

1. 在 round5B 基础上将 `take_profit_atr_multiple` 从 3.0 提升到 3.5。

其余参数不变。

## 2. Step 3：实验记录

1. runtime_id: 20260423_145645_456405
2. task_id: 1776956205456405
3. status: DONE

## 3. Step 4：结果

核心结果：

1. TradeCnt: 114
2. TotalPnL: +545.7112
3. AnnualSharpe: 0.4182
4. MaxDrawdownPct: 0.04102

对比 round5B：

1. 指标完全一致（可视为无增量改进）。

## 4. Step 5：停止条件判断

### 4.1 是否继续 round7+

决策：停止继续轮次（在本次任务内停止于 round6）。

理由：

1. 主问题“交易次数过少”已在 round4 解决。
2. round5 已拿到显著收益质量提升。
3. round6 对胜出方向再迭代后无任何新增收益，边际收益接近 0。
4. 在当前策略框架内继续细调参数的价值有限，应转入“新结构问题”再开新任务。

### 4.2 方向跟踪状态

1. 方向A（Signal 收紧）：1 次尝试失败，未继续到 3 次上限。
2. 方向B（Exit 优化）：2 次尝试，其中 round5B 有效，round6 无增量。

未触发 hard.md 条件（无方向达到“连续 3 轮仍无法解决”的状态）。

## 5. 下一阶段建议（新任务）

1. 若继续优化，建议改为“状态过滤模块”或“多头寸约束模块”的结构性变更，而非继续微调同类参数。
