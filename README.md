# FITE7415 Project

Quantitative trading strategy research project for HKU FITE7415. This repository contains the full path from early BTCUSD exploration to the final XAUUSD production candidate.

## Final Strategy

The final selected strategy is `XAUUSD-ZEntry-Grid`, a daily mean-reversion strategy on XAUUSD.

- Main script: `Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`
- Selected round: Round 26
- Core idea: enter when price is sufficiently below a 20-day mean, then manage risk with ATR-based stop loss, take profit, and a max holding period

### Final Result vs Baseline

| Metric | Final Strategy | Baseline (Round 23) |
|--------|----------------|---------------------|
| Sharpe | 1.1869 | 0.7956 |
| MaxDD | 0.01281 | 0.02653 |
| TotalPnL | +601.6870 | +696.9780 |
| TradeCnt | 100 | 280 |

## How To Reproduce

The recommended path is the ALGOGENE Web UI. This is the simplest way for teammates to reproduce the reported result.

### Script To Run

Use:

`Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`

### Backtest Settings

Use these values exactly:

| Field | Value |
|-------|-------|
| Strategy Name | XAUUSD-ZEntry-Grid-R26 |
| Subscribe List | XAUUSD |
| Start Date | 2023-01 |
| End Date | 2025-12 |
| Initial Capital | 10000 |
| Base Currency | USD |
| Risk Free Rate | 0 |
| Leverage | 1 |
| Allow Short Sell | False |
| Dataset | 1440 (1-day) |
| Position Base Env | False |
| News Feed | False |
| Economics Feed | False |
| Weather Feed | False |

### Web UI Steps

1. Log in to `algogene.com`.
2. Open **Algo Research Lab**.
3. Upload `Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`.
4. Enter the exact settings from the table above.
5. Submit the backtest.
6. Compare the output with the target metrics below.

### Reproduction Success Criteria

Treat the run as successfully reproduced if the full-sample result is close to:

| Metric | Target |
|--------|--------|
| TradeCnt | 100 |
| TotalPnL | +601.6870 |
| Sharpe | 1.1869 |
| MaxDD | 0.01281 |

Small differences can occur because of platform-side execution details, but the trade count, Sharpe level, and drawdown profile should remain close.

## Quick Setup for Teammates (One-Click Local Testing)

For team members who want to test the strategy locally with MCP environment:

### Prerequisites
- Python 3.10 or higher (download from python.org if not installed)
- Git (for cloning the repository)
- VS Code + GitHub Copilot (for vibe coding / AI-assisted workflow)

### Setup Steps (Windows/Mac/Linux)

**Step 1: Clone Repository**
```bash
git clone https://github.com/CharlieInTheFranxx/FITE7415-Project.git
cd FITE7415-Project
```

**Step 2: Create Virtual Environment**

*On Windows (PowerShell):*
```powershell
python -m venv FITE7415
.\FITE7415\Scripts\Activate.ps1
```

*On Mac/Linux:*
```bash
python3 -m venv FITE7415
source FITE7415/bin/activate
```

**Step 3: Install Dependencies**

This repo includes a **locally patched version** of `algogene_mcp_server` (with bug fixes not in the PyPI release). Install it directly from the repo:

```bash
pip install --upgrade pip
pip install -e ./algogene_mcp_server   # local patched MCP package
pip install -r requirements.txt        # remaining dependencies
```

> **Why `-e ./algogene_mcp_server`?** The `algogene_mcp_server` folder in this repo is our modified version of the upstream package. Installing it in editable mode (`-e`) means your Python environment uses our patched code, not the version from PyPI.

**Step 4: Set ALGOGENE Credentials**

Create a `.env` file in the project root (this file is gitignored — never commit it):
```
ALGOGENE_USER=your_algogene_user_id
ALGOGENE_API_KEY=your_algogene_api_key
```

You can find your User ID and API Key in your ALGOGENE account settings at `algogene.com`.

**Step 5: Verify Installation**
```bash
python -c "import algogene_mcp_server; print('MCP dependencies installed successfully')"
```

---

## Vibe Coding with AI: MCP Function Calls

The `algogene_mcp_server` package exposes all ALGOGENE platform capabilities as MCP tools. When used with an AI coding assistant (GitHub Copilot, Cursor, Claude), the AI can directly call these functions on your behalf — this is "vibe coding".

### Start the MCP Server

Before running any AI-assisted workflow, start the MCP server locally:

```bash
# Activate virtual environment first
.\FITE7415\Scripts\Activate.ps1   # Windows
source FITE7415/bin/activate       # Mac/Linux

# Start server (STDIO mode, for VS Code / Copilot)
python -m algogene_mcp_server.main

# Or start in HTTP mode (for browser-based tools)
python -m algogene_mcp_server.main --transport http --host 0.0.0.0 --port 8000
```

### VS Code MCP Configuration

Add the following to your VS Code `.vscode/mcp.json` (create this file if it doesn't exist):

```json
{
  "servers": {
    "algogene": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "algogene_mcp_server.main"],
      "env": {
        "ALGOGENE_USER": "${env:ALGOGENE_USER}",
        "ALGOGENE_API_KEY": "${env:ALGOGENE_API_KEY}"
      }
    }
  }
}
```

Once connected, GitHub Copilot can call MCP tools directly from the chat panel.

---

## How to Run a Backtest via MCP

The primary tool for running backtests programmatically is `backtest_run`. Here is the complete flow:

### Step 1 — Read the strategy script

```python
with open("Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py", "r") as f:
    code = f.read()
```

### Step 2 — Define backtest settings

```python
settings = {
    "strategyName": "XAUUSD-ZEntry-Grid-R26",
    "subscribeList": ["XAUUSD"],
    "startDate": "2023-01",
    "endDate": "2025-12",
    "initialCapital": 10000,
    "baseCurrency": "USD",
    "riskFreeRate": 0,
    "leverage": 1,
    "allowShortSell": False,
    "dataset": 1440,
    "positionBaseEnv": False,
    "newsFeed": False,
    "economicsFeed": False,
    "weatherFeed": False
}
```

### Step 3 — Submit via MCP

Ask GitHub Copilot in chat (with MCP connected):

> "Use the `backtest_run` tool to submit the strategy with the settings above, then poll `get_task_status` until complete."

Or call via Python directly:

```python
from algogene_mcp_server.tools.backtest_run import backtest_run
result = backtest_run(code=code, settings=settings)
task_id = result.get("taskId")
```

### Step 4 — Poll for results

```python
import time
from algogene_mcp_server.tools.get_task_status import get_task_status

while True:
    status = get_task_status(taskId=task_id)
    if status.get("status") in ("completed", "failed"):
        break
    time.sleep(10)

print(status)
```

---

## Available MCP Function Reference

All functions require `ALGOGENE_USER` and `ALGOGENE_API_KEY` in environment variables.

### Market Data
| Function | Description |
|----------|-------------|
| `get_realtime_prices` | Current price for one or more symbols |
| `get_realtime_price_24hrchange` | 24-hour price change |
| `get_realtime_exchange_rate` | Exchange rate between two currencies |
| `get_history_price` | Historical OHLCV price data |
| `get_instruments` | All available tradable instruments |
| `get_instrument_meta` | Contract spec for a specific instrument |
| `search_instrument` | Search instruments by keyword |

### Backtest & Strategy
| Function | Description |
|----------|-------------|
| `backtest_run` | Submit strategy code + settings to ALGOGENE cloud |
| `backtest_cancel` | Cancel a running backtest task |
| `get_task_status` | Poll task status (pending / running / completed / failed) |
| `strategy_stats` | Performance statistics for a completed strategy run |
| `strategy_trade` | Full trade-by-trade history |
| `strategy_pl` | Daily cumulative P&L history |
| `strategy_bal` | Daily account balance history |
| `strategy_pos` | Daily position history |
| `strategy_logs` | System logs for a backtest run |
| `strategy_market_perf` | Market index benchmark performance |

### Account & Session
| Function | Description |
|----------|-------------|
| `get_session` | Get/refresh session token |
| `list_accounts` | List all trading accounts |
| `get_balance` | Current account balance |
| `get_positions` | Outstanding positions |
| `get_opened_trades` | Open trades |
| `get_pending_trades` | Pending (limit) orders |

### Order Management
| Function | Description |
|----------|-------------|
| `open_order` | Place a new order |
| `query_order` | Query order status |
| `cancel_orders` | Cancel one or more unfilled orders |
| `close_orders` | Close outstanding positions |
| `update_pending_order` | Modify a pending order |
| `update_opened_order` | Modify an open trade |

### Analytics Apps
| Function | Description |
|----------|-------------|
| `app_predict_sentiment` | Sentiment score for text (news, reports) |
| `app_algo_generator` | Generate a backtest script from a description |
| `app_performance_calculator` | Performance stats from NAV time series |
| `app_portfolio_optimizer_custom` | Optimal portfolio from custom time series |

---

## Vibe Coding Workflow for Strategy Tuning

The recommended workflow for AI-assisted strategy modification:

1. **Open VS Code** and ensure the MCP server is connected (check Copilot chat panel)
2. **Ask Copilot** to fetch recent price data: `"Call get_history_price for XAUUSD, daily bars, 2023-01 to 2025-12"`
3. **Ask Copilot** to modify a parameter and submit a backtest: `"Change Z-score threshold from 1.5 to 2.0 in xauusd_round26_zentry_m1_0_v1.py and run a backtest with the standard settings"`
4. **Wait** — Copilot will call `backtest_run`, then poll `get_task_status` automatically
5. **Compare** — Ask Copilot to call `strategy_stats` and compare Sharpe / MaxDD against the target table above
6. **Iterate** — Adjust and repeat

### Troubleshooting

**Issue**: Virtual environment creation fails
- **Solution**: Check `python --version` is 3.10+, and you have write permissions in the project directory

**Issue**: `pip install` fails with package resolution errors
- **Solution**: Run `pip install --upgrade pip` first, then retry

**Issue**: "algogene_mcp_server not found"
- **Solution**: Ensure the virtual environment is activated — you should see `(FITE7415)` in your shell prompt. Then run `pip install -e ./algogene_mcp_server`

**Issue**: MCP server returns authentication error
- **Solution**: Check that `ALGOGENE_USER` and `ALGOGENE_API_KEY` are correctly set in your `.env` file or system environment variables

## Repository Layout

- `Program/BTCUSD/`: early BTCUSD research and reports
- `Program/XAUUSD/`: XAUUSD shadow optimization and baseline selection
- `Program/XAUUSD-ZEntry-Grid/`: final mainline optimization rounds and selected production candidate
- `Program/Overview.md`: project status summary
- `Program/current-mainline.md`: active mainline pointer
- `Program/hard.md`: strategy design notes

## Key Research Files

- Main winner report: `Program/XAUUSD-ZEntry-Grid/reports/26th-round.md`
- Final closeout: `Program/XAUUSD-ZEntry-Grid/reports/B-mainline-optimization-closeout.md`
- Baseline reference: `Program/XAUUSD/code/xauusd_mainline_v1.py`

## Strategy Notes

- Platform: ALGOGENE
- Frequency: daily bars
- Instrument: XAUUSD
- Short selling: disabled
- Leverage: 1x

Use your own ALGOGENE account and configure credentials locally outside version control.

## Course Context

Course: FITE7415  
Institution: The University of Hong Kong

This repository is intended for coursework collaboration, research review, and result reproduction.

### Quantitative Trading Theory
- Concepts: Mean reversion, Z-scores, ATR, Sharpe ratio
- References: Course materials and standard quant finance textbooks

### Contact

For questions about this project:
1. **Group Lead**: Zhang Haotian (u3665820@connect.hku.hk)
2. **Team Members**: [To be added by collaborators]

---

**Last Updated**: 2026-04-24  
**Status**: ✅ Production Ready  
**Next Steps**: Final course report submission
