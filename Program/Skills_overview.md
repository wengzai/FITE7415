# FITE7415 Project Skills Overview

## 为什么需要 Skills

这个项目不是单次问答，而是连续几周反复做"想法-实现-回测-复盘-写报告"的迭代研究过程。  
在这种场景下，Skills 可以：

1. **固化流程和模板**，避免每次讨论都从头开始。
2. **标准化输出格式**，保证研究结论和报告内容对齐。
3. **降低非专业背景的风险**，通过结构化检查避免遗漏关键评估项。
4. **提高执行效率**，尤其在接近截止时能显著减少重复和返工。

## 推荐的 6 类 Skills

### 1. Strategy Design Skill ⭐⭐⭐

**用途**  
把一个交易策略想法标准化成结构化输出，强制完成"假设、信号、入场、出场、风控、资金管理、失败情景"六个必填段。

**核心价值**  
- 避免讨论发散，保证每个策略想法都能被清楚表述。
- 强制思考"这个策略失败时会怎样"，这往往是非金融背景的人容易忽视的。
- 输出直接对应报告里的 Executive Summary 和 Implementation Details。

**典型用法**  
```
用户：我想试试一个基于 RSI 的反转策略
Skill 触发：Strategy Design
输出：
- 核心假设：[...]
- 信号逻辑：[...]
- 入场条件：[...]
- 出场条件：[...]
- 风险管理：[...]
- 资金管理：[...]
- 失败场景：[...]
```

**何时使用**  
- 刚想到一个新策略想法。
- 要调整现有策略前，做一遍设计文档更新。
- 团队内部讨论新方向前。

---

### 2. Backtest Experiment Skill ⭐⭐⭐

**用途**  
固定回测实验的完整模板：参数表、时间窗口划分、对照组设置、回测指标列表、结果记录和存储格式。

**核心价值**  
- 防止"随意调参导致过拟合"这类常见错误。
- 确保所有回测都可复现，方便对比和追溯。
- 让你们能清楚回答"为什么这个参数"和"之前试过什么"。

**典型框架**  
```
Experiment ID: [名字]
Baseline: [对照参数]
Test Variants: [要测试的参数变化]
Time Windows: [训练窗口/测试窗口划分]
Key Metrics: [Sharpe, MaxDD, PnL, Win Rate 等]
Expected Outcome: [预期这次实验想验证什么]
Result: [实际结果和结论]
```

**何时使用**  
- 每次计划回测前。
- 需要对比两个参数集合。
- 要做参数敏感性分析。

---

### 3. Risk and Capital Review Skill ⭐⭐⭐

**用途**  
策略改动后自动做风险清单检查。包括：最大回撤承受度、单笔风险比例、仓位上限、交易频率、策略容量假设、杠杆合理性、流动性可得性。

**核心价值**  
- 你们是非金融背景，这个 Skill 可以显著降低"收益看起来好但风控空白"的风险。
- 把模糊的"有风险管理意识"转化为清晰的检查清单。
- 每次改动都过一遍，能提前发现不合理设计。

**检查项示例**  
```
□ 最大可接受回撤百分比？
□ 单笔交易最多承担多少资金比例风险？
□ 建议最小仓位和最大仓位分别是多少？
□ 一天最多开几笔单？
□ 这个策略最适合的资金规模是？
□ 是否需要杠杆？杠杆倍数合理吗？
□ 滑点和成本对收益的影响有多大？
□ 在真实交易中最可能失效的场景是？
```

**何时使用**  
- 完成一个策略版本后。
- 参数大幅调整后。
- 在准备提交报告前做最后检查。

---

### 4. Result Interpretation Skill ⭐⭐

**用途**  
回测跑完后，自动生成分析框架：好区间、差区间、可能原因、是否符合原始假设、下一步改动建议。

**核心价值**  
- 把"有数字结果"升级成"有研究结论"。
- 强制思考结果背后的原因，而不只是看收益率。
- 输出直接支持报告里的 Backtest Performance 和 Expectations for Real Trading。

**分析框架**  
```
回测期间最好的 N 个月：
  - 时间：
  - 特征：
  - 收益：
  - 为什么表现好：

回测期间最差的 N 个月：
  - 时间：
  - 特征：
  - 回撤：
  - 为什么表现差：

与原始假设的对照：
  - 假设：
  - 实际结果：
  - 是否符合：

改进建议：
  - 发现的问题：
  - 可能的改动方向：
```

**何时使用**  
- 每次回测完成后。
- 要总结一个阶段的研究进展。
- 准备更新报告时。

---

### 5. Report Writer Skill ⭐⭐⭐

**用途**  
按作业模板的六大章节（Executive Summary、Implementation Details、Risk Management、Capital Management、Backtest Performance、Expectations for Real Trading）生成初稿段落，并自动把回测指标映射到对应章节。

**核心价值**  
- 避免"最后一周赶报告"的噩梦。
- 研究过程和报告同步推进，不用重复解释。
- 确保报告内容和回测脚本保持一致。

**工作流**  
```
策略设计完成 → Report Section 1+2 初稿
回测+分析完成 → Report Section 5 初稿
风控检查完成 → Report Section 3 初稿
资金计划完成 → Report Section 4 初稿
现实交易讨论 → Report Section 6 初稿
所有初稿 → 组织整理成最终版本
```

**何时使用**  
- 策略设计完成后，立刻生成 Executive Summary 初稿。
- 每次重要回测结果出来，更新 Backtest Performance 部分。
- 做风险评估时，同步更新报告的 Risk Management。

---

### 6. MCP Ops Skill ⭐⭐

**用途**  
把常用的 ALGOGENE MCP 操作固化成固定步骤和检查清单。包括：获取会话令牌、查账户信息、提交回测脚本、查询回测状态、读取回测统计、下载结果。

**核心价值**  
- 减少操作失误（例如令牌过期、参数错误）。
- 提高执行效率，尤其在临近截止时。
- 建立操作审计追溯，能回答"上一次回测用的什么参数"。

**操作流程示例**  
```
Step 1: 获取新会话令牌
Step 2: 确认账户信息
Step 3: 上传策略脚本
Step 4: 检查脚本是否成功上传
Step 5: 提交回测任务
Step 6: 记录 Task ID
Step 7: 轮询任务状态
Step 8: 任务完成后拉取统计和日志
Step 9: 保存结果到本地
```

**何时使用**  
- 需要提交或查询回测时。
- 多人协作，要确保操作步骤一致。
- 最后阶段做最终脚本提交时。

---

## 实施优先级建议

### Tier 1（本周立刻做）
1. **Strategy Design Skill** — 为下周的策略实验打基础。
2. **Backtest Experiment Skill** — 保证回测流程规范。
3. **Report Writer Skill** — 同步推进报告，避免最后赶。

### Tier 2（回测开始后补充）
4. **Risk and Capital Review Skill** — 每个版本完成后做检查。
5. **Result Interpretation Skill** — 结果出来后做分析。

### Tier 3（可选增强）
6. **MCP Ops Skill** — 如果多人协作或操作频繁，值得投入。

---

## 下一步建议

如果要立刻开始使用 Skills，建议按以下顺序：

1. **第一天**：起草 Strategy Design Skill 的最小可用版本（5 min）+ Backtest Experiment 模板（10 min）。
2. **第二天**：用这两个 Skill 把第一个 baseline 策略想法标准化。
3. **第三天**：跑第一个回测，用 Report Writer Skill 生成初稿。
4. **第四天**：补充 Risk and Capital Review Skill，对第一个版本做检查。

这样做的好处是，到本周末，你们就已经积累了"1 个完整的策略-回测-分析-报告"的闭环，后续只需要迭代这个过程。

---

## 技能文件位置建议

这些 Skills 应该放在 `.github/skills/` 下（如果项目在 Git），或者 `.claude/skills/` 下（VS Code 本地用）：

```
.github/
└── skills/
    ├── strategy-design/
    │   ├── SKILL.md
    │   └── templates/
    ├── backtest-experiment/
    │   ├── SKILL.md
    │   └── templates/
    ├── risk-review/
    │   ├── SKILL.md
    │   └── checklist.txt
    ├── result-interpretation/
    │   ├── SKILL.md
    │   └── analysis-template.md
    ├── report-writer/
    │   ├── SKILL.md
    │   └── sections/
    └── mcp-ops/
        ├── SKILL.md
        └── operation-steps.md
```

也可以全部放在项目根目录的 `.claude/` 下，这样不需要 Git。

