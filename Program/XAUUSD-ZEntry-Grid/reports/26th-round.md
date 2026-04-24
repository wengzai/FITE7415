# 第二十六轮执行报告（Round 26：z_entry 网格验证，H2）

## 1. Experiment ID 与目标

1. Experiment ID：R26_H2_ZENTRY_GRID_XAU_BMAIN
2. 目标：在固定对照基线（round23）下，仅调整 z_entry，验证信号阈值对收益稳定性与交易频率的影响。

## 2. Baseline 与测试变体

### 2.1 固定对照基线（round23）

1. 全样本：TradeCnt 280, TotalPnL +696.9780, Sharpe 0.7956, MaxDD 0.02653
2. 弱窗口：TradeCnt 22, TotalPnL +119.3500, Sharpe 0.9986, MaxDD 0.00856

### 2.2 Test Variants（仅改单一变量 z_entry）

1. V1：z_entry = -1.0
2. V2：z_entry = -1.2
3. V3：z_entry = -1.5
4. V4：z_entry = -2.0

## 3. Time Windows

1. 全样本：2023-01 到 2025-12
2. 弱窗口：2025-07 到 2025-12

## 4. 运行记录（MCP）

1. V1 全样本
   - runtime_id: 20260424_113207_869745
   - task_id: 1777030327869745
   - status: DONE
2. V1 弱窗口
   - runtime_id: 20260424_113244_187870
   - task_id: 1777030364187870
   - status: DONE
3. V2 全样本
   - runtime_id: 20260424_113310_231414
   - task_id: 1777030390231414
   - status: DONE
4. V2 弱窗口
   - runtime_id: 20260424_113343_016658
   - task_id: 1777030423016658
   - status: DONE
5. V3 全样本
   - runtime_id: 20260424_113414_747639
   - task_id: 1777030454747639
   - status: DONE
6. V3 弱窗口
   - runtime_id: 20260424_113458_917754
   - task_id: 1777030498917754
   - status: DONE
7. V4 全样本
   - runtime_id: 20260424_113522_013569
   - task_id: 1777030522013569
   - status: DONE
8. V4 弱窗口
   - runtime_id: 20260424_113602_309715
   - task_id: 1777030562309715
   - status: DONE

## 5. Metrics 与结果表

### 5.1 全样本（2023-01 ~ 2025-12）

1. V1（-1.0）：TradeCnt 100, TotalPnL +601.6870, Sharpe 1.1869, MaxDD 0.01281
2. V2（-1.2）：TradeCnt 76, TotalPnL +489.4010, Sharpe 1.0872, MaxDD 0.01512
3. V3（-1.5）：TradeCnt 54, TotalPnL +388.3710, Sharpe 0.9943, MaxDD 0.01945
4. V4（-2.0）：TradeCnt 26, TotalPnL -60.3420, Sharpe -0.2716, MaxDD 0.01457

### 5.2 弱窗口（2025-07 ~ 2025-12）

1. V1（-1.0）：TradeCnt 4, TotalPnL +103.9750, Sharpe 1.4424, MaxDD 0.00421
2. V2（-1.2）：TradeCnt 2, TotalPnL +76.2550, Sharpe 1.4213, MaxDD 0.00007
3. V3（-1.5）：TradeCnt 2, TotalPnL +76.2550, Sharpe 1.4213, MaxDD 0.00007
4. V4（-2.0）：TradeCnt 0, TotalPnL 0, Sharpe 0, MaxDD 0

## 6. 判定与解释

1. H2（提高入场阈值减少噪声）得到部分支持：阈值从 -1.0 向更严格方向移动时，回撤略降，但收益与 Sharpe 同步下滑。
2. 综合收益-风险-频率三维，V1（z_entry=-1.0）最优：
   - Sharpe 显著高于 round23 基线（1.1869 > 0.7956）
   - MaxDD 显著低于基线（0.01281 < 0.02653）
   - 全样本 TradeCnt=100，满足统计充足性（>=50）
3. V4（-2.0）出现明显信号过筛，已接近失效区。

## 7. 结论与下一步

1. Round 26 选定版本：`z_entry=-1.0`（作为 Round 27 起的工作基线）。
2. 下一轮进入 H3（退出机制）：对比固定 TP 与“弱化固定止盈（更依赖止损与持有期）”版本。
3. 继续保持固定比较基线 round23，不变更对照口径。
