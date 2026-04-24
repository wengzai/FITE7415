# 第三轮执行报告（Round 3, Step 2 到 Step 5）

## 0. 执行目标

根据上一轮结论，round3 仅做一个核心改动：

1. 放宽入场触发密度（提高 RSI 入场阈值，降低价格回撤阈值）。
2. 其余风险、出场与资金参数保持不变。
3. 验证交易样本是否显著高于 round2。

## 1. Pre-run checks

### 1.1 会话与账户

1. 已刷新 session token。
2. 已确认 livetest 账户可用且状态正常。

### 1.2 标的与环境

1. 标的：BTCUSD。
2. 回测区间：2023-01 到 2025-12。
3. 频率：dataset=1440（日线）。
4. 初始资金：10000 USD。

## 2. Step 2：Round 3 策略定义

### 2.1 本轮唯一改动

在 round2 策略基础上，仅放宽入场触发参数：

1. rsi_entry_threshold: 10 -> 20
2. pullback_pct: 0.02 -> 0.01

其余参数保持不变：

1. RSI period: 2
2. SMA period: 20
3. ATR period: 14
4. Stop ATR multiple: 1.5
5. TP ATR multiple: 2.5
6. Max hold: 7 天
7. Risk per trade: 1%

脚本文件：Program/BTCUSD/code/btcusd_round3_reversion_v2.py

### 2.2 假设

若 round2 样本不足主要由触发阈值过严导致，则放宽触发后应观察到：

1. 完整交易数上升。
2. 交易月份覆盖更广。

## 3. Step 3：回测配置与实验记录

### 3.1 固定配置

1. strategyName: BTCUSD round3 mean reversion v2
2. subscribeList: [BTCUSD]
3. StartDate: 2023-01
4. EndDate: 2025-12
5. InitialCapital: 10000
6. BaseCurrency: USD
7. Leverage: 1
8. allowShortSell: false
9. dataset: 1440
10. 外部 feed：全部关闭

### 3.2 运行记录

1. runtime_id: 20260423_142543_843875
2. task_id: 1776954343843875
3. 轮询状态：IN PROGRESS -> DONE

## 4. Step 4：结果收集

### 4.1 日志摘要

1. 2023-01-01 开仓：buy 0.22 lot @ 16539.84
2. 2023-01-08 平仓：sell 0.22 lot @ 16945.33
3. 2025-12-31 回测结束

### 4.2 交易摘要

1. TradeCnt=2（开平各一条）
2. 完整往返交易数=1

### 4.3 绩效摘要

1. TotalPnL: +89.2078
2. AnnualSharpe: 0.7538
3. AnnualSortino: 3.3848
4. MaxDrawdownPct: 0.001262
5. AvgHoldingDay: 7
6. TradeCnt: 2

## 5. Step 5：结果解释与决策

### 5.1 观察事实

1. round3 关键绩效与 round2 基本一致。
2. 交易样本仍为 1 笔完整交易，未达到样本增长目标。
3. 本轮改动未解决核心问题（样本不足）。

### 5.2 结论

1. round3 的单参数放宽方向无效（至少在当前实现下未带来样本提升）。
2. 不应继续沿同一思路做微调（继续改阈值的边际价值低）。

### 5.3 是否继续 round4

结论：建议继续 round4，但必须切换为结构性改动，而非阈值微调。

round4 建议的唯一主改动方向：

1. 重构入场触发机制（例如从绝对阈值改为分位数触发，或引入状态切换逻辑），并保留现有风险控制模块不变。

## 6. 风险复核

1. 单笔风险定义：PASS
2. 止损机制定义：PASS
3. 最大持仓时间：PASS
4. 成本与滑点现实性：NEEDS-DATA
5. 样本充分性：FAIL

Go/No-go：

1. 对继续研发（round4）为 GO。
2. 对形成稳健投资结论为 NO-GO。
