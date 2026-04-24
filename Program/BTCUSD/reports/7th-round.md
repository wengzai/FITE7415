# 第七轮执行报告（Round 7, Step 2 到 Step 5）

## 0. 执行目标

在 round5B 当前最优版本基础上，实施“状态过滤模块 + 更严格单仓约束”结构性改动，验证是否能在保持样本可用的同时改善 Sharpe/回撤。

## 1. Step 2：策略改动

脚本：Program/BTCUSD/code/btcusd_round7_statefilter_v1.py

本轮核心改动：

1. 新增状态过滤模块：
   - `trend_ratio = abs(SMA20 - SMA100) / SMA100 <= 0.08`
   - `bandwidth = std20 / SMA20` 需在 `[0.01, 0.12]`
2. 单仓约束加强：
   - `cooldown_days = 6`（高于 `max_hold_days = 5`）

其余参数保持 round5B 最优版本。

## 2. Step 3：实验记录

1. runtime_id: 20260423_150352_218062
2. task_id: 1776956632218062
3. status: DONE

## 3. Step 4：结果

1. TradeCnt: 56
2. TotalPnL: +63.6121
3. AnnualSharpe: 0.0909
4. MaxDrawdownPct: 0.04113

对比 round5B（TradeCnt 114, PnL +545.7112, Sharpe 0.4182）：

1. 交易次数明显下降。
2. 收益和 Sharpe 显著恶化。
3. 回撤未得到实质改善。

## 4. Step 5：结论

1. 状态过滤方向（第1次尝试）在当前阈值设计下无效。
2. 判定为该方向一次失败样本，暂不继续同方向细调，转入更强策略改动测试。

## 5. 风险复核

1. 单笔风险与止损约束：PASS
2. 样本充分性：BORDERLINE（低于 round5B）
3. 成本/滑点现实性：NEEDS-DATA
