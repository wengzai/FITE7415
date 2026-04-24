# 第五轮执行报告（Round 5, Step 2 到 Step 5）

## 0. 执行目标

在 round4 已解决“交易次数过少”后，round5 转向“收益质量优化”。本轮采用并行优化思想（受平台并发限制改为串行提交、同轮比较）：

1. 方向A（Signal Quality）：收紧入场阈值（z_entry -1.2 -> -1.5）。
2. 方向B（Exit Structure）：优化止损止盈比（stop 1.5ATR -> 1.2ATR，TP 2.5ATR -> 3.0ATR）。

## 1. Pre-run checks

1. 已刷新 session。
2. 已确认 BTCUSD 与账户环境正常。
3. 与前轮保持同一回测窗口（2023-01 到 2025-12）与日线频率。

## 2. Step 2：策略与参数

### 2.1 方向A（signal）

脚本：Program/BTCUSD/code/btcusd_round5A_signal_v1.py

核心改动：

1. z_entry = -1.5（更严格入场）

其他保持不变。

### 2.2 方向B（exit）

脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py

核心改动：

1. stop_atr_multiple = 1.2
2. take_profit_atr_multiple = 3.0

其他保持不变。

## 3. Step 3：实验记录

### 3.1 Round5A

1. runtime_id: 20260423_145505_257038
2. task_id: 1776956105257038
3. status: DONE

### 3.2 Round5B

1. runtime_id: 20260423_145545_302177
2. task_id: 1776956145302177
3. status: DONE

## 4. Step 4：结果对比

### 4.1 Round5A（Signal）结果

1. TradeCnt: 80
2. TotalPnL: -207.4242
3. AnnualSharpe: -0.2395
4. MaxDrawdownPct: 0.04729

结论：显著劣化。

### 4.2 Round5B（Exit）结果

1. TradeCnt: 114
2. TotalPnL: +545.7112
3. AnnualSharpe: 0.4182
4. MaxDrawdownPct: 0.04102
5. ProfitFactor: 1.3702

结论：相对 round4 明显优化（Sharpe 与 PnL 提升，回撤略降）。

## 5. Step 5：结论与下一步

1. 本轮胜出方向为 Exit Structure（round5B）。
2. Signal 收紧方向判定为无效尝试（方向A第1次，失败）。
3. 进入 round6，继续在胜出方向上做第2次迭代验证边际增益。

## 6. 风险复核

1. 单笔风险规则：PASS
2. 止损规则：PASS
3. 样本充分性：PASS
4. 成本/滑点现实性：NEEDS-DATA
