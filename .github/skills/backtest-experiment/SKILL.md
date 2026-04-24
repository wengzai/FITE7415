---
name: backtest-experiment
description: "Use when planning, running, or documenting a backtest experiment; enforce baseline vs variants, date windows, metrics, and reproducible records."
---

# Backtest Experiment Skill

## Purpose
Standardize every backtest so results are reproducible and comparable.

## Workflow
1. Assign experiment ID and objective.
2. Define baseline and test variants before execution.
3. Split periods (in-sample / out-of-sample) where applicable.
4. Pre-commit key metrics and acceptance criteria.
5. Record run metadata, results, and interpretation.
6. Recommend next experiment based on evidence.

## Required Output Sections
- Experiment ID and objective
- Baseline setup
- Test variants
- Time windows
- Metrics and criteria
- Result table
- Conclusion and next action

## Guardrails
- No post-hoc metric switching.
- Distinguish exploratory run vs comparison run.
- Flag potential overfitting whenever many variants are tested.

## Template
Use: templates/experiment-template.md
