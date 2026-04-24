# 第九轮执行报告（Round 9, Step 2 到 Step 5）

## 0. 执行目标

在 round8 后，先不继续盲目调参数，改为执行“跨时间窗口泛化验证”：

1. 以 round5B 作为固定基线策略。
2. 在多个半年度窗口上做 out-of-window 稳健性检查。
3. 用聚合结果判断是否继续结构优化。

## 1. Step 2：策略与实验设置

基线脚本：Program/BTCUSD/code/btcusd_round5B_exit_v1.py

本轮不改策略参数，只改验证框架：

1. 标的：BTCUSD
2. 频率：日线（dataset=1440）
3. 账户设置与风险参数保持与 round5B 一致
4. 时间窗切分：
   - Fold A：2024-01 到 2024-06
   - Fold B：2024-07 到 2024-12
   - Fold C：2025-01 到 2025-06
   - Fold D：2025-07 到 2025-12

## 2. Step 3：实验记录

1. Fold A（2024H1）
   - runtime_id: 20260424_085814_388258
   - task_id: 1777021094388258
   - status: DONE
2. Fold B（2024H2）
   - runtime_id: 20260424_085842_466285
   - task_id: 1777021122466285
   - status: DONE
3. Fold C（2025H1）
   - runtime_id: 20260424_085705_465040
   - task_id: 1777021025465040
   - status: DONE
4. Fold D（2025H2）
   - runtime_id: 20260424_085904_035688
   - task_id: 1777021144035688
   - status: DONE

## 3. Step 4：结果

### 3.1 分窗口结果

1. Fold A（2024H1）
   - TradeCnt: 21
   - TotalPnL: +46.9844
   - AnnualSharpe: 0.2314
   - MaxDrawdownPct: 0.02566
2. Fold B（2024H2）
   - TradeCnt: 17
   - TotalPnL: +150.4734
   - AnnualSharpe: 0.6092
   - MaxDrawdownPct: 0.01542
3. Fold C（2025H1）
   - TradeCnt: 18
   - TotalPnL: +395.2735
   - AnnualSharpe: 1.3280
   - MaxDrawdownPct: 0.01836
4. Fold D（2025H2）
   - TradeCnt: 26
   - TotalPnL: -34.9122
   - AnnualSharpe: -0.1760
   - MaxDrawdownPct: 0.02875

### 3.2 聚合观察

1. Sharpe 中位数约为 0.4203（正值）。
2. TotalPnL 中位数约为 +98.7289（正值）。
3. 正收益 fold 占比为 3/4（75%）。
4. 2025H2 出现收益与 Sharpe 同时转负，说明策略对部分市场状态仍较敏感。

## 4. Step 5：结论与下一步

1. round5B 并非仅在单一窗口有效，具备一定跨时段可用性（4 个窗口中 3 个为正）。
2. 但泛化能力不稳定，尤其在 2025H2 出现显著退化。
3. 决策：继续 round10，尝试“轻量趋势过滤”以修复弱状态下的回撤与负收益问题。

## 5. 风险复核

1. 单笔风险与止损规则：PASS
2. 过拟合风险：BORDERLINE（多窗验证已做，但样本总长度仍有限）
3. 成本/滑点现实性：NEEDS-DATA（TradeCost 仍为 0）
