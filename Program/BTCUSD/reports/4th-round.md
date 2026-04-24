# 第四轮执行报告（Round 4, Step 2 到 Step 5）

## 0. 执行目标

根据本轮优化安排，本轮目标是优先解决“交易次数过少”的核心问题，并在结果出来后判断是否继续 round5、round6 等后续轮次。

## 1. Pre-run checks

### 1.1 会话与账户检查

1. 已刷新 session token。
2. 已确认 livetest 账户可见且可用。

### 1.2 标的与环境检查

1. 标的：BTCUSD。
2. 区间：2023-01 到 2025-12。
3. 频率：dataset=1440（日线）。
4. 初始资金：10000 USD。
5. 外部 news/econs/weather feed 关闭。

## 2. Step 2：Round 4 策略定义

### 2.1 round3 的问题复盘

round3 仍只有 1 笔完整交易，说明仅做阈值微调（RSI 阈值、pullback 阈值）没有触及根因。观察到一个重要可疑点：

1. 持仓状态门控过强（或状态更新机制不稳定）导致新信号长期无法进场。

### 2.2 本轮唯一核心改动（结构性）

本轮只改一个核心模块：重构入场触发与持仓门控机制。

具体做法：

1. 入场信号改为 `z-score` 反转（基于 SMA20 与 rolling std20）。
2. 用“固定冷却窗口（5天）”替代历史版本里对实时持仓状态回调的强依赖。

其余模块保持不变：

1. 风控仍为 ATR 止损/止盈（1.5 ATR / 2.5 ATR）。
2. 单笔风险仍为 1%。
3. 最大持仓时间仍为 5 天。

### 2.3 参数（round4-v3）

1. sma_period = 20
2. std_period = 20
3. z_entry = -1.2
4. atr_period = 14
5. stop_atr_multiple = 1.5
6. take_profit_atr_multiple = 2.5
7. max_hold_days = 5
8. risk_per_trade = 1%

脚本文件：Program/BTCUSD/code/btcusd_round4_reversion_v3.py

## 3. Step 3：回测配置与实验记录

### 3.1 回测配置

1. strategyName: BTCUSD round4 mean reversion v3
2. subscribeList: [BTCUSD]
3. StartDate: 2023-01
4. EndDate: 2025-12
5. InitialCapital: 10000
6. BaseCurrency: USD
7. Leverage: 1
8. allowShortSell: false
9. dataset: 1440

### 3.2 运行记录

1. runtime_id: 20260423_143826_923661
2. task_id: 1776955106923661
3. 状态轮询：IN PROGRESS -> DONE

## 4. Step 4：结果收集

### 4.1 核心绩效指标

1. TotalPnL: +168.1449
2. AnnualSharpe: 0.1865
3. AnnualSortino: 0.2690
4. MaxDrawdownPct: 0.04285
5. TradeCnt: 114
6. TradeCntPerMonth: 2.2904
7. WinRate: 0.4455

### 4.2 交易活跃度结果

1. `TradeCnt` 从 round2/3 的 2 提升到 114。
2. 完整往返交易显著增加，覆盖多个年份与月份。
3. 核心问题“交易次数过少”已被实质性解决。

### 4.3 日志与执行稳定性

1. 日志显示回测期间持续有开平仓记录。
2. 未见先前那类“仅首笔交易后长期静默”的表现。

## 5. Step 5：结果解释与是否继续

### 5.1 结论

1. round4 成功解决了本任务的首要问题（样本不足）。
2. 策略现已具备“可分析级”交易样本，后续优化可转向收益质量与风险效率。

### 5.2 风险复核（Pass/Fail）

1. 单笔风险限制：PASS
2. 止损机制：PASS
3. 最大持仓时间：PASS
4. 样本充分性：PASS（相对前几轮）
5. 成本与滑点现实性：NEEDS-DATA（平台 `TradeCost=0`）

### 5.3 是否继续 round5 及以上

决策：本次按指令停止在 round4，不进入 round5。

权衡理由：

1. “交易次数过少”已被充分解决，达成当前主目标。
2. 继续 round5 当然可做，但目标会从“样本修复”转为“绩效优化”，属于新问题域。
3. 在当前指令语境下，继续加轮次的边际收益已明显下降，不如先沉淀本轮结果并明确下一阶段目标。

## 6. 下一阶段建议（非本轮执行）

如进入下一阶段优化（可视为新任务），建议只改一个方向：

1. 在保持 round4 触发机制不变的前提下，优化出场模块（例如分层止盈/移动止损）以提升 Sharpe 与回撤表现。
