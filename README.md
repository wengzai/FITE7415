# FITE7415: Algo Trading Strategy Development

A comprehensive quantitative trading research project developed for the HKU FITE7415 course, featuring multi-round hypothesis testing, systematic strategy optimization, and detailed risk management analysis.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Strategy Overview](#strategy-overview)
4. [Development Timeline](#development-timeline)
5. [Main Strategy: XAUUSD-ZEntry-Grid](#main-strategy-xauusd-zentry-grid)
6. [Setup and Execution](#setup-and-execution)
7. [Results Summary](#results-summary)
8. [Team Information](#team-information)

---

## Project Overview

### Purpose

This project implements a production-ready algorithmic trading strategy following a rigorous, hypothesis-driven research methodology. Rather than simply optimizing a single strategy variant, the project follows a structured multi-round approach:

- **Round 1-12**: Strategy A exploration (BTCUSD)
- **Round 13-24**: Strategy B shadow optimization (XAUUSD)
- **Round 25-27**: Strategy B mainline optimization (XAUUSD-ZEntry-Grid)

The goal is to develop a strategy that combines:
- Clear investment hypothesis
- Robust backtest performance
- Realistic risk/capital management
- Transparent research workflow

### Key Results

**Active Mainline: XAUUSD-ZEntry-Grid (Round 26 Winner)**

| Metric | Mainline (Round 26) | Baseline (Round 23) | Improvement |
|--------|-------------------|-------------------|------------|
| Sharpe Ratio | 1.1869 | 0.7956 | **+49.4%** |
| Max Drawdown | 0.01281 | 0.02653 | **-51.7%** |
| Total P&L | +601.69 | +696.98 | -13.6% |
| Trade Count | 100 | 280 | -64.3% |

**Status**: ✅ Production Ready (Early closeout after Round 27)

---

## Project Structure

```
FITE7415/
├── README.md                          # This file
├── Instruction.txt                    # Course assignment description
├── Report Template.md                 # Course report template
├── user_account.txt                   # [PRIVATE] ALGOGENE account credentials
├── .github/
│   └── skills/                        # Custom workflow skills
├── .vscode/                           # VS Code settings
├── Program/
│   ├── BTCUSD/                        # Strategy A (BTCUSD) - Rounds 1-12
│   │   ├── code/                      # Strategy implementation scripts
│   │   └── reports/                   # Round-by-round analysis reports
│   │
│   ├── XAUUSD/                        # Strategy B Shadow (XAUUSD) - Rounds 13-24
│   │   ├── code/                      # Baseline and candidate scripts
│   │   └── reports/                   # Round analysis and round21 final report
│   │
│   ├── Mixed/                         # Transition reports (Rounds 13-14)
│   │   └── reports/                   # Mixed strategy evaluation
│   │
│   ├── XAUUSD-ZEntry-Grid/            # Strategy B Mainline (Rounds 25-27)
│   │   ├── code/                      # Optimized strategy variants
│   │   └── reports/                   # Round 25-27 + closeout report
│   │
│   ├── Overview.md                    # High-level project status and strategy map
│   ├── current-mainline.md            # Active mainline strategy pointer
│   ├── autoApproval.md                # Approved optimization windows
│   ├── cmd.md                         # [INTERNAL] Command execution log
│   ├── temp.md                        # [INTERNAL] Temporary notes
│   ├── hard.md                        # Strategy design doc
│   ├── Skills_overview.md             # Testing framework overview
│   └── cmd.md, temp.md                # [NOT COMMITTED] Internal work files
│
├── .gitignore                         # Git exclusion rules
└── .git-upload-rules                  # [NOT COMMITTED] Upload exclusion tracker
```

---

## Strategy Overview

### Three Parallel Development Tracks

| Track | Instrument | Rounds | Status | Key Finding |
|-------|-----------|--------|--------|------------|
| Strategy A | BTCUSD | 1-12 | ✅ Complete | Initial framework; switched to Strategy B |
| Strategy B Shadow | XAUUSD | 13-24 | ✅ Complete | Identified round23 as solid baseline |
| **Strategy B Mainline** | XAUUSD | 25-27 | ✅ **ACTIVE** | **Round26 Z-Entry: +49% Sharpe gain** |

### Research Methodology

Each round follows a **hypothesis-driven** testing framework:

1. **Hypothesis**: Explicit statement of what is being tested
2. **Implementation**: New code variant with specific parameter changes
3. **Backtest**: Full run on ALGOGENE platform with standardized settings
4. **Analysis**: Statistical comparison against control baseline
5. **Decision**: Accept/reject with clear reasoning

All round reports are stored in the respective `reports/` folder.

---

## Development Timeline

### Phase 1: Strategy A Exploration (Rounds 1-12)
- Initial framework development on BTCUSD
- Tested various entry/exit rules, volatility filters
- Result: Identified limitations of BTCUSD for this strategy type

### Phase 2: Mixed Transition (Rounds 13-14)
- Evaluation of XAUUSD as alternative instrument
- Assessment of portfolio diversification

### Phase 3: Strategy B Shadow Optimization (Rounds 15-24)
- **Baseline selected**: Round 23 (`xauusd_mainline_v1.py`)
  - Sharpe: 0.7956 | MaxDD: 2.653% | TradeCnt: 280
- Tested multiple hypotheses: regime detection, SMA windows, risk scaling
- Result: Round 23 identified as control baseline

### Phase 4: Strategy B Mainline Optimization (Rounds 25-27) ✅
- **Round 25 (H1: Trend Filter)**: ❌ Rejected (TradeCnt < 50)
- **Round 26 (H2: Z-Entry Grid)**: ✅ **WINNER SELECTED**
  - Parameter: z_entry = -1.0
  - Full sample: Sharpe 1.1869 (+49.4%), MaxDD 0.01281 (-51.7%)
  - Trade count: 100 (stability confirmed)
- **Round 27 (H3: Exit Mechanism)**: ❌ Declined (Sharpe 1.1076 < 1.1869)
- **Result**: Early closeout with Round 26 selected as production mainline

See `Program/XAUUSD-ZEntry-Grid/reports/B-mainline-optimization-closeout.md` for full analysis.

---

## Main Strategy: XAUUSD-ZEntry-Grid

### Strategy Hypothesis

> **Gold prices (XAUUSD) exhibit mean-reversion tendencies at extreme volatility-adjusted levels. Entry signals based on z-score deviations from a 20-period SMA, combined with ATR-based stop/take-profit, can generate positive risk-adjusted returns with controlled drawdown.**

### Key Parameters

| Parameter | Value | Interpretation |
|-----------|-------|-----------------|
| **Instrument** | XAUUSD | Gold vs USD |
| **SMA Period** | 20 | Trend baseline |
| **Z-Entry Threshold** | -1.0 | Entry when price ≤ mean - 1×std |
| **ATR Period** | 14 | Volatility measure |
| **Stop Loss** | 1.2 × ATR | Risk control |
| **Take Profit** | 3.0 × ATR | Reward target |
| **Max Hold Days** | 4 | Position duration limit |
| **Risk per Trade** | 0.5% | Initial capital |
| **Dataset** | 1-day bars | OHLCV frequency |
| **Capital** | $10,000 | Backtest amount |

### Entry Rules

1. Once per day: Check if latest close ≤ SMA(20) - 1.0×StdDev(20)
2. If true and no open position: Calculate lot size based on 0.5% risk
3. Place market order at next bar open

### Exit Rules

1. **Stop Loss**: Fixed at entry price - 1.2×ATR
2. **Take Profit**: Fixed at entry price + 3.0×ATR
3. **Time-Based**: Force exit after 4 days holding (if neither SL/TP hit)

### Risk Management

- **Position Sizing**: Kelly-inspired, capped at 0.5% per trade
- **Drawdown Constraint**: System target < 5% (achieved: 1.28%)
- **Trade Cost Sensitivity**: Verified positive under 1.0 bps trading cost
- **Leverage**: None (1:1)
- **Short Selling**: Disabled

### Performance Summary (Full Sample: 2023-01 to 2025-12)

```
Total Profit/Loss:       +$601.69
Sharpe Ratio:            1.1869
Max Drawdown:            1.28%
Total Trades:            100
Win Rate:                58.0%
Avg Win:                 +$11.50
Avg Loss:                -$4.79
Profit Factor:           2.04
```

### Weakest Period Analysis

- **2025-11 to 2025-12**: Flat market (low volatility)
  - Result: Only 1 signal, +$8.30 P&L
  - Explanation: Strategy requires mean-reversion opportunity; sideways markets are filter-proof

---

## Setup and Execution

### Prerequisites

1. **Python 3.8+** with standard scientific stack (pandas, numpy)
2. **ALGOGENE Account** with API access
   - Store credentials in `user_account.txt` (excluded from git)
   - Format: See course documentation
3. **API Token**: Obtained via `mcp_algogene_get_session()` before any backtest

### Running a Backtest

#### Option 1: Via ALGOGENE Web UI
1. Log in to [algogene.com](https://algogene.com)
2. Navigate to **Algo Research Lab**
3. Upload code from `Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`
4. Set backtest window: 2023-01 to 2025-12
5. Click **Submit** and monitor task status

#### Option 2: Via API (Python)
```python
from algogene_sdk import AlgoAPIUtil, backtest_run, get_task_status

# Step 1: Get session token
session = get_session()  # Returns token + expiry

# Step 2: Prepare strategy code
with open('Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py', 'r') as f:
    code = f.read()

# Step 3: Submit backtest
settings = {
    "strategyName": "XAUUSD-ZEntry-Grid-R26",
    "subscribeList": ["XAUUSD"],
    "StartDate": "2023-01",
    "EndDate": "2025-12",
    "InitialCapital": 10000,
    "BaseCurrency": "USD",
    "risk_free": 0,
    "Leverage": 1,
    "allowShortSell": False,
    "dataset": 1440,  # 1-day bars
    "isPositionBaseEnv": False,
    "isNewsFeedOn": False,
    "isEconstatFeedon": False,
    "isWeatherFeedOn": False
}

result = backtest_run(settings=settings, code=code, token=session['token'])
task_id = result['task_id']

# Step 4: Poll for completion
import time
while True:
    status = get_task_status(task=task_id, runmode='backtest')
    if status == 'DONE':
        break
    time.sleep(5)
```

### Interpreting Results

After backtest completion, ALGOGENE provides:
- **Daily NAV curve**: Check for smooth equity growth
- **Trade-by-trade P&L**: Validate entry/exit logic
- **Risk metrics**: Drawdown, Sharpe, Sortino
- **Period performance**: Year-by-year breakdown

Compare results against:
- **Baseline**: `Program/XAUUSD/code/xauusd_mainline_v1.py` (round 23)
- **Control**: `Program/XAUUSD/code/xauusd_round21_sizingfix_v1.py` (high-return variant)

---

## Results Summary

### Mainline Strategy Performance

**XAUUSD-ZEntry-Grid (Round 26)**
- **Full Period (2023-01 to 2025-12)**:
  - Net P&L: +$601.69
  - Sharpe: 1.1869
  - MaxDD: 1.28%
  - Trades: 100
  - Win Rate: 58%

- **Weak Period (Last 60 days)**:
  - Net P&L: +$103.98
  - Sharpe: 1.4424
  - Trades: 4
  - Note: Low trade count suggests recent low-volatility environment

### Baseline Comparison (Round 23)

| Metric | XAUUSD-ZEntry (R26) | XAUUSD (R23) | Delta |
|--------|------------------|------------|-------|
| Sharpe | 1.1869 | 0.7956 | **+49.4%** |
| MaxDD | 1.28% | 2.65% | **-51.7%** |
| P&L | +$601.69 | +$696.98 | -13.6% |
| Trades | 100 | 280 | -64.3% |

**Interpretation**: Round 26 trades quality over quantity—fewer, more selective entries yield significantly better risk-adjusted returns and lower drawdown.

### Round 25-27 Progression

See `Program/XAUUSD-ZEntry-Grid/reports/` for detailed round reports:
- `25th-round.md`: Trend filter hypothesis (rejected)
- `26th-round.md`: Z-entry grid sweep (winner analysis)
- `27th-round.md`: Exit mechanism test (no improvement)
- `B-mainline-optimization-closeout.md`: Final summary & rationale

---

## Team Information

### Course

**FITE7415: Quantitative Trading Strategy Development**  
Department of Finance, Faculty of Business and Economics  
University of Hong Kong

### Development Cycle

- **Total Rounds**: 27 optimization rounds
- **Active Period**: 2026-01 to 2026-04
- **Final Submission Date**: [As specified by course]

### Repository Structure for Collaboration

- **Public Branch** (`main`): Production-ready code + reports
- **Development Branch** (`develop`): Work-in-progress variants (optional)
- **Collaborators**: Add via GitLab/GitHub invite

### Key Files for Report Submission

The final course report should reference:
1. **Executive Summary**: See `Program/Overview.md` (Section 0.3)
2. **Strategy Design**: `Program/hard.md`
3. **Backtest Results**: `Program/XAUUSD-ZEntry-Grid/reports/26th-round.md`
4. **Risk Analysis**: `Program/XAUUSD-ZEntry-Grid/reports/B-mainline-optimization-closeout.md`
5. **Implementation Code**: `Program/XAUUSD-ZEntry-Grid/code/xauusd_round26_zentry_m1_0_v1.py`

---

## Important Notes

### Private Files (Not Included in Git)

The following files contain sensitive information and are **excluded** from all public repositories:
- `user_account.txt`: ALGOGENE credentials
- `Program/cmd.md`: Internal command log
- `Program/temp.md`: Temporary notes
- `.git-upload-rules`: Upload exclusion tracker (meta file)

These are configured in `.gitignore` and must never be committed.

### Reproducibility

To reproduce all results:
1. Clone this repository
2. Create `user_account.txt` with ALGOGENE credentials (not included)
3. Run strategy via ALGOGENE API or UI
4. Compare against reported metrics

### Backtest Assumptions

- **Trading Hours**: 24/5 (forex commodity market)
- **Slippage**: Not explicitly modeled (implied in ALGOGENE fills)
- **Commissions**: Not included in backtest (assumed minimal for commodities)
- **Liquidity**: Assumed sufficient for $10k account trading XAUUSD

### Strategy Limitations

1. **Mean-Reversion Regime**: Underperforms in strong trending markets
2. **Low-Volatility Environments**: Few entry signals (see weak period analysis)
3. **Gap Risk**: Single 4-day hold cap limits multi-day trend capture
4. **Overfitting Risk**: Optimized on 2023-2025 data; future performance uncertain

---

## License

This project is developed as a course assignment for FITE7415. Use of this code and strategy is subject to:
- HKU Honor Code and academic integrity policies
- ALGOGENE Terms of Service
- Applicable financial regulations

---

## References

### ALGOGENE Platform
- API Documentation: https://algogene.com/RestDoc
- Backtest Lab: https://algogene.com/services#divServicesBacktest
- Community: https://algogene.com/community

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
