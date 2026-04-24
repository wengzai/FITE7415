---
name: mcp-ops
description: "Use when operating ALGOGENE MCP workflows such as session refresh, account checks, backtest submission, status polling, and result collection."
---

# MCP Ops Skill

## Purpose
Execute ALGOGENE MCP operations with a stable, auditable sequence.

## Workflow
1. Refresh session token.
2. Validate account and balance.
3. Validate strategy settings and instrument names.
4. Submit backtest job and capture task ID.
5. Poll task status until completion/failure.
6. Collect stats/logs and save run record.

## Required Output Sections
- Pre-run checks
- Submission details
- Polling status
- Final result snapshot
- Errors and remediation

## Guardrails
- Never submit without a fresh token check.
- Always record task ID and timestamp.
- On failure, capture logs before retry.

## Runbook
Use: operation-steps.md
