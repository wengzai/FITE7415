# 第二十五轮执行报告（Round 25：趋势过滤器验证，H1）

## 1. Experiment ID 与目标

1. Experiment ID：R25_H1_TREND_FILTER_XAU_BMAIN
2. 目标：验证在 round23 主线（固定基线）上加入趋势过滤器后，是否能提升稳定性并满足 B-mainline 进入标准。

## 2. Baseline 与测试变体

### 2.1 固定 Baseline（round23）

1. 全样本（2023-01 ~ 2025-12）：TradeCnt 280, TotalPnL +696.9780, Sharpe 0.7956, MaxDD 0.02653
2. 弱窗口（2025-07 ~ 2025-12）：TradeCnt 22, TotalPnL +119.3500, Sharpe 0.9986, MaxDD 0.00856

### 2.2 Test Variants（仅改趋势过滤模块）

1. V1（严格过滤）：SMA(80) 5日斜率 > 0 时抑制做多
2. V2（宽松过滤）：SMA(80) 10日平均斜率 > 1.0 美元/日时抑制做多

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260424_112204_681000
   - task_id: 1777029724681000
   - status: DONE
2. V1 弱窗口
   - runtime_id: 20260424_112354_897793
   - task_id: 1777029834897793
   - status: DONE
3. V2 全样本
   - runtime_id: 20260424_112456_481323
   - task_id: 1777029896481323
   - status: DONE
4. V2 弱窗口
   - runtime_id: 20260424_112539_965292
   - task_id: 1777029939965292
   - status: DONE

备注：提交 V2 弱窗口时首次遇到平台并发限制（max concurrent tasks: 1），在 V2 全样本完成后重提成功。

## 5. Metrics 与结果表

### 5.1 V1（严格过滤）

1. 全样本：TradeCnt 26, TotalPnL +20.3900, Sharpe 0.0792, MaxDD 0.01248
2. 弱窗口：TradeCnt 2, TotalPnL +49.7400, Sharpe 0.7894, MaxDD 0.00421

### 5.2 V2（宽松过滤）

1. 全样本：TradeCnt 48, TotalPnL +322.2630, Sharpe 0.8125, MaxDD 0.01274
2. 弱窗口：TradeCnt 4, TotalPnL +103.9750, Sharpe 1.4424, MaxDD 0.00421

### 5.3 按 round25 预设判定标准检查（H1）

1. 判定阈值：Sharpe >= 0.7956，MaxDD <= 0.0318（2.65% x 1.2），TradeCnt >= 50
2. V1：Sharpe 未达标，TradeCnt 明显不足，未通过
3. V2：Sharpe 达标，MaxDD 达标，但 TradeCnt=48 < 50，未通过（触发稀疏信号约束）

## 6. 解释与结论

1. 观察事实
   - 趋势过滤显著降低回撤（两版 MaxDD 均低于 baseline）。
   - 过滤同时大幅压缩交易频率，尤其 V1 出现明显过筛。
   - V2 在收益风险比上优于 V1，但全样本交易次数仍低于统计阈值。
2. 假设检验结论（H1）
   - 按本轮既定规则，H1 不成立/不通过主线纳入条件。
   - 主要失败点是 TradeCnt < 50（强制约束），而非回撤或 Sharpe。

## 7. Next Action（Round 26）

1. 按 B-mainline 计划进入 H2（z_entry 网格）：{-1.0, -1.2, -1.5, -2.0}
2. 保持固定对照基线为 round23（Program/XAUUSD/code/xauusd_mainline_v1.py）
3. 继续双窗口验证（全样本 + 弱窗口），并沿用同一判定口径
