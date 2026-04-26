# ALGOGENE Backtest Setup

This project can run ALGOGENE backtests either through the ALGOGENE Web UI or through the local MCP helper package.

## 1. Create Local Credentials

Copy `.env.example` to `.env` in the project root, then fill in your ALGOGENE account values:

```text
ALGOGENE_USER=your_algogene_user_id
ALGOGENE_API_KEY=your_algogene_api_key
ALGOGENE_BASE_URL=https://algogene.com/rest
```

Do not commit `.env`. It is ignored by Git.

## 2. Install Python Dependencies

From the project root:

```powershell
python -m venv FITE7415
.\FITE7415\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .\algogene_mcp_server
pip install -r requirements.txt
```

If PowerShell blocks activation scripts, either run this for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\FITE7415\Scripts\Activate.ps1
```

or use the Python executable directly:

```powershell
.\FITE7415\Scripts\python.exe -m pip install -e .\algogene_mcp_server
```

## 3. Verify Configuration

```powershell
python -c "from algogene_mcp_server.config import ALGOGENE_USER, ALGOGENE_API_KEY; print(bool(ALGOGENE_USER), bool(ALGOGENE_API_KEY))"
```

Expected output:

```text
True True
```

## 4. Start MCP Server

Run the server from the project root:

```powershell
cd "C:\Users\12098\OneDrive\Desktop\hku_s2\mastering the market\project\FITE7415-Project"
.\FITE7415\Scripts\Activate.ps1
python -m algogene_mcp_server.main
```

If you are already inside `FITE7415\Scripts`, use `.\python.exe` explicitly:

```powershell
.\python.exe -m algogene_mcp_server.main
```

In PowerShell, plain `python` may resolve to the system Python instead of the executable in the current directory.

For HTTP testing:

```powershell
python -m algogene_mcp_server.main --transport streamable-http --host localhost --port 8000
```

## 5. VS Code MCP Configuration

If you want VS Code or Copilot Chat to call ALGOGENE tools directly, create `.vscode/mcp.json` locally:

```json
{
  "servers": {
    "algogene": {
      "type": "stdio",
      "command": "${workspaceFolder}\\FITE7415\\Scripts\\python.exe",
      "args": ["-m", "algogene_mcp_server.main"]
    }
  }
}
```

The Python config loader reads `.env` from the project root, so the MCP JSON does not need to contain your account credentials.

## 6. Standard Final Backtest Settings

Use these settings for the current final candidate:

| Field | Value |
| --- | --- |
| Strategy script | `Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py` |
| Strategy name | `XAUUSD-ZEntry-Grid-R35` |
| Subscribe list | `XAUUSD` |
| Start date | `2023-01` |
| End date | `2025-12` |
| Initial capital | `10000` |
| Base currency | `USD` |
| Risk free rate | `0` |
| Leverage | `1` |
| Allow short sell | `False` |
| Dataset | `1440` |
| Position base env | `False` |
| News feed | `False` |
| Economics feed | `False` |
| Weather feed | `False` |

## 7. Current Benchmark Result

Round 35 target result:

| Metric | Target |
| --- | --- |
| TradeCnt | `112` |
| TotalPnL | `+1071.3050` |
| Sharpe | `1.7139` |
| MaxDD | `0.01293` |

## 8. Automated Backtest Command

Use the local automation script from the project root:

```powershell
.\FITE7415\Scripts\python.exe scripts\algogene_backtest.py --expect-round35
```

By default this submits the current final candidate:

```text
Program/XAUUSD-ZEntry-Grid/code/xauusd_round35_stop1_10_v1.py
```

The script will:

1. Read the strategy script.
2. Submit an ALGOGENE backtest.
3. Poll task status until done or timeout.
4. Fetch `strategy_stats`, `strategy_logs`, and `strategy_pl`.
5. Save raw JSON outputs under `Program/XAUUSD-ZEntry-Grid/backtests/<timestamp>/`.
6. With `--expect-round35`, validate the result against the round35 reproduction threshold.

To submit a new candidate:

```powershell
.\FITE7415\Scripts\python.exe scripts\algogene_backtest.py `
  --strategy Program\XAUUSD-ZEntry-Grid\code\xauusd_round28_sma30_v1.py `
  --name XAUUSD-ZEntry-Grid-R28-SMA30
```

To continue polling an existing task:

```powershell
.\FITE7415\Scripts\python.exe scripts\algogene_backtest.py --task-id 1777030327869745
```

To fetch results for a known runtime ID:

```powershell
.\FITE7415\Scripts\python.exe scripts\algogene_backtest.py --runtime-id 20260424_113207_869745
```
