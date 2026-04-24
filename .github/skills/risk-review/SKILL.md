---
name: risk-review
description: "Use when reviewing risk and capital rules after strategy changes; produce a structured checklist with pass/fail status and required fixes."
---

# Risk and Capital Review Skill

## Purpose
Detect hidden risk before moving to another strategy iteration.

## Workflow
1. Collect strategy settings and latest backtest metrics.
2. Evaluate position sizing and per-trade risk.
3. Evaluate portfolio-level risk and drawdown controls.
4. Evaluate execution realism (costs, slippage, liquidity).
5. Mark each check as pass/fail/needs-data.
6. Output a mandatory fix list before next run.

## Required Output Sections
- Risk summary
- Checklist results
- Critical failures
- Required fixes
- Go/No-go decision

## Guardrails
- If max drawdown control is undefined, decision is No-go.
- If per-trade loss limit is missing, decision is No-go.
- If assumptions on costs are absent, mark needs-data.

## Checklist
Use: checklist.txt
