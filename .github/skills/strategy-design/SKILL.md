---
name: strategy-design
description: "Use when designing a new trading strategy, revising strategy logic, or asking for hypothesis/signal/entry/exit/risk/capital/failure-case structure for FITE7415."
---

# Strategy Design Skill

## Purpose
Convert a raw idea into a testable strategy spec with clear assumptions and execution rules.

## Workflow
1. Restate the strategy idea in one sentence.
2. Define market regime and instrument scope.
3. Build signal logic and exact entry/exit rules.
4. Add risk rules and capital allocation limits.
5. List invalidation conditions and failure scenarios.
6. End with a ready-to-backtest checklist.

## Required Output Sections
- Core hypothesis
- Signal logic
- Entry conditions
- Exit conditions
- Risk management
- Capital management
- Failure scenarios
- Backtest readiness checklist

## Guardrails
- Avoid vague language such as "buy when trend is good".
- Every rule must be measurable from available data.
- Include at least one scenario where the strategy should stop trading.

## Template
Use: templates/strategy-design-template.md
