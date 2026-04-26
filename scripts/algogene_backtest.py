from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import algogene_mcp_server  # noqa: F401 - registers legacy tool imports
from algogene_mcp_server.tools.backtest_run import backtest_run
from algogene_mcp_server.tools.get_task_status import get_task_status
from algogene_mcp_server.tools.strategy_logs import strategy_logs
from algogene_mcp_server.tools.strategy_pl import strategy_pl
from algogene_mcp_server.tools.strategy_stats import strategy_stats


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STRATEGY = (
    PROJECT_ROOT
    / "Program"
    / "XAUUSD-ZEntry-Grid"
    / "code"
    / "xauusd_round35_stop1_10_v1.py"
)
DEFAULT_OUTDIR = PROJECT_ROOT / "Program" / "XAUUSD-ZEntry-Grid" / "backtests"


DONE_STATES = {"DONE", "COMPLETED", "COMPLETE", "SUCCESS", "SUCCEEDED", "FINISHED"}
FAILED_STATES = {"FAILED", "ERROR", "CANCELLED", "CANCELED", "TIMEOUT"}


def standard_settings(strategy_name: str, style: str) -> dict[str, Any]:
    if style == "readme":
        return {
            "strategyName": strategy_name,
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
            "weatherFeed": False,
        }

    return {
        "strategyName": strategy_name,
        "subscribeList": ["XAUUSD"],
        "StartDate": "2023-01",
        "EndDate": "2025-12",
        "InitialCapital": 10000,
        "BaseCurrency": "USD",
        "risk_free": 0,
        "Leverage": 1,
        "allowShortSell": False,
        "dataset": 1440,
        "isPositionBaseEnv": False,
        "isNewsFeedOn": False,
        "isEconstatFeedon": False,
        "isWeatherFeedOn": False,
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def find_value(data: Any, names: set[str]) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in names:
                return value
        for value in data.values():
            found = find_value(value, names)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_value(item, names)
            if found not in (None, ""):
                return found
    return None


def extract_task_id(data: Any) -> str | None:
    value = find_value(data, {"task_id", "taskId", "taskID"})
    return str(value) if value not in (None, "") else None


def extract_runtime_id(data: Any) -> str | None:
    value = find_value(data, {"runtime_id", "runtimeId", "runtimeID", "accountid", "accountId"})
    return str(value) if value not in (None, "") else None


def extract_state(data: Any) -> str | None:
    if isinstance(data, str):
        return data.upper()
    if isinstance(data, list) and data:
        return extract_state(data[-1])
    if isinstance(data, dict):
        for key in ["task_status", "taskStatus", "state", "result"]:
            value = data.get(key)
            if isinstance(value, str):
                return value.upper()
        value = data.get("status")
        if isinstance(value, str):
            return value.upper()
        if "res" in data:
            return extract_state(data["res"])
    return None


def load_settings(args: argparse.Namespace, strategy_name: str) -> dict[str, Any]:
    settings = standard_settings(strategy_name, args.settings_style)
    if args.settings:
        override = json.loads(Path(args.settings).read_text(encoding="utf-8"))
        settings.update(override)
    if args.start_date:
        for key in ["StartDate", "startDate"]:
            if key in settings:
                settings[key] = args.start_date
    if args.end_date:
        for key in ["EndDate", "endDate"]:
            if key in settings:
                settings[key] = args.end_date
    if args.trade_cost is not None:
        settings["TradeCost"] = args.trade_cost
    return settings


def poll_task(
    task_id: str,
    outdir: Path,
    interval: int,
    timeout_minutes: int,
    initial_runtime_id: str | None = None,
) -> tuple[str | None, str | None, list[Any]]:
    history: list[Any] = []
    deadline = time.time() + timeout_minutes * 60
    runtime_id: str | None = initial_runtime_id
    state: str | None = None

    while True:
        response = get_task_status(task="backtest", task_id=task_id)
        history.append({"time": datetime.now().isoformat(timespec="seconds"), "response": response})
        write_json(outdir / "status_history.json", history)

        state = extract_state(response)
        runtime_id = extract_runtime_id(response) or runtime_id
        print(f"status={state or 'UNKNOWN'} runtime_id={runtime_id or '-'}")

        if state in DONE_STATES or state in FAILED_STATES:
            break
        if time.time() >= deadline:
            print("Polling timed out. Re-run with --task-id to continue checking.", file=sys.stderr)
            break
        time.sleep(interval)

    return state, runtime_id, history


def fetch_results(runtime_id: str, outdir: Path) -> dict[str, Any] | None:
    pl = strategy_pl(runmode="backtest", runtime_id=runtime_id)
    final_acdate = extract_final_acdate(pl)
    stats = strategy_stats(runmode="backtest", runtime_id=runtime_id, acdate=final_acdate or "")
    logs = strategy_logs(runmode="backtest", runtime_id=runtime_id)

    write_json(outdir / "stats.json", stats)
    write_json(outdir / "logs.json", logs)
    write_json(outdir / "pl.json", pl)

    performance = stats.get("performance") if isinstance(stats, dict) else None
    if isinstance(performance, dict):
        print("performance summary:")
        for key in [
            "TradeCnt",
            "TotalPnL",
            "AnnualSharpe",
            "Sharpe",
            "maxDrawdown_pct",
            "MaxDrawdownPct",
            "MaxDD",
            "profit_factor",
        ]:
            if key in performance:
                print(f"  {key}: {performance[key]}")
        return performance
    return None


def validate_performance(performance: dict[str, Any], args: argparse.Namespace, outdir: Path) -> bool:
    checks: list[dict[str, Any]] = []

    def as_float(key: str) -> float | None:
        value = performance.get(key)
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def add_check(name: str, actual: float | None, op: str, expected: float | None) -> None:
        if expected is None:
            return
        passed = actual is not None and (actual >= expected if op == ">=" else actual <= expected)
        checks.append({
            "name": name,
            "actual": actual,
            "operator": op,
            "expected": expected,
            "passed": passed,
        })

    add_check("TradeCnt", as_float("TradeCnt"), ">=", args.min_trades)
    add_check("TotalPnL", as_float("TotalPnL"), ">=", args.min_pnl)
    add_check("AnnualSharpe", as_float("AnnualSharpe"), ">=", args.min_sharpe)
    add_check("maxDrawdown_pct", as_float("maxDrawdown_pct"), "<=", args.max_drawdown)

    if not checks:
        return True

    passed = all(item["passed"] for item in checks)
    write_json(outdir / "validation.json", {"passed": passed, "checks": checks})
    print("validation summary:")
    for item in checks:
        mark = "PASS" if item["passed"] else "FAIL"
        print(
            f"  {mark} {item['name']}: {item['actual']} "
            f"{item['operator']} {item['expected']}"
        )
    return passed


def extract_final_acdate(pl_response: Any) -> str | None:
    if not isinstance(pl_response, dict):
        return None
    rows = pl_response.get("res")
    if not isinstance(rows, list) or not rows:
        return None
    last = rows[-1]
    if not isinstance(last, dict):
        return None
    value = last.get("Acdate") or last.get("acdate")
    return str(value) if value else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit and monitor an ALGOGENE backtest.")
    parser.add_argument("--strategy", default=str(DEFAULT_STRATEGY), help="Path to the ALGOGENE strategy script.")
    parser.add_argument("--name", default="XAUUSD-ZEntry-Grid-R35", help="ALGOGENE strategy name.")
    parser.add_argument("--settings", help="Optional JSON file with settings overrides.")
    parser.add_argument("--settings-style", choices=["api", "readme"], default="api")
    parser.add_argument("--start-date", help="Override backtest start date, YYYY-MM.")
    parser.add_argument("--end-date", help="Override backtest end date, YYYY-MM.")
    parser.add_argument("--trade-cost", type=float, help="Override ALGOGENE TradeCost setting.")
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR), help="Directory for saved run outputs.")
    parser.add_argument("--task-id", help="Skip submit and poll an existing task ID.")
    parser.add_argument("--runtime-id", help="Skip submit/poll and fetch results for an existing runtime ID.")
    parser.add_argument("--no-poll", action="store_true", help="Submit only; do not poll.")
    parser.add_argument("--no-fetch", action="store_true", help="Do not fetch stats/logs/pl after completion.")
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--timeout-minutes", type=int, default=60)
    parser.add_argument("--expect-round26", action="store_true", help="Validate against the round26 reproduction threshold.")
    parser.add_argument("--expect-round29", action="store_true", help="Validate against the round29 reproduction threshold.")
    parser.add_argument("--expect-round30", action="store_true", help="Validate against the round30 reproduction threshold.")
    parser.add_argument("--expect-round33", action="store_true", help="Validate against the round33 reproduction threshold.")
    parser.add_argument("--expect-round35", action="store_true", help="Validate against the round35 reproduction threshold.")
    parser.add_argument("--min-trades", type=float)
    parser.add_argument("--min-pnl", type=float)
    parser.add_argument("--min-sharpe", type=float)
    parser.add_argument("--max-drawdown", type=float)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expect_round35:
        args.min_trades = args.min_trades if args.min_trades is not None else 105
        args.min_pnl = args.min_pnl if args.min_pnl is not None else 1000
        args.min_sharpe = args.min_sharpe if args.min_sharpe is not None else 1.65
        args.max_drawdown = args.max_drawdown if args.max_drawdown is not None else 0.014
    if args.expect_round33:
        args.min_trades = args.min_trades if args.min_trades is not None else 100
        args.min_pnl = args.min_pnl if args.min_pnl is not None else 950
        args.min_sharpe = args.min_sharpe if args.min_sharpe is not None else 1.5
        args.max_drawdown = args.max_drawdown if args.max_drawdown is not None else 0.018
    if args.expect_round30:
        args.min_trades = args.min_trades if args.min_trades is not None else 85
        args.min_pnl = args.min_pnl if args.min_pnl is not None else 750
        args.min_sharpe = args.min_sharpe if args.min_sharpe is not None else 1.3
        args.max_drawdown = args.max_drawdown if args.max_drawdown is not None else 0.018
    if args.expect_round29:
        args.min_trades = args.min_trades if args.min_trades is not None else 80
        args.min_pnl = args.min_pnl if args.min_pnl is not None else 650
        args.min_sharpe = args.min_sharpe if args.min_sharpe is not None else 1.2
        args.max_drawdown = args.max_drawdown if args.max_drawdown is not None else 0.016
    if args.expect_round26:
        args.min_trades = args.min_trades if args.min_trades is not None else 95
        args.min_pnl = args.min_pnl if args.min_pnl is not None else 550
        args.min_sharpe = args.min_sharpe if args.min_sharpe is not None else 1.1
        args.max_drawdown = args.max_drawdown if args.max_drawdown is not None else 0.015

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(args.outdir) / run_stamp
    outdir.mkdir(parents=True, exist_ok=True)

    strategy_path = Path(args.strategy)
    if not strategy_path.is_absolute():
        strategy_path = PROJECT_ROOT / strategy_path

    task_id = args.task_id
    runtime_id = args.runtime_id
    state = None

    if runtime_id:
        write_json(outdir / "summary.json", {"runtime_id": runtime_id, "outdir": str(outdir)})
    elif task_id:
        write_json(outdir / "summary.json", {"task_id": task_id, "outdir": str(outdir)})
    else:
        code = strategy_path.read_text(encoding="utf-8")
        settings = load_settings(args, args.name)
        write_json(outdir / "settings.json", settings)
        submit = backtest_run(code=code, settings=settings)
        write_json(outdir / "submit.json", submit)
        task_id = extract_task_id(submit)
        runtime_id = extract_runtime_id(submit)
        print(f"submitted task_id={task_id or '-'} runtime_id={runtime_id or '-'}")

        if not task_id and not runtime_id:
            if isinstance(submit, dict) and submit.get("msg"):
                print(f"ALGOGENE submit message: {submit['msg']}", file=sys.stderr)
            print("Could not find task_id/runtime_id in submit response.", file=sys.stderr)
            return 2

    if task_id and not args.no_poll:
        state, runtime_id, _history = poll_task(
            task_id=task_id,
            outdir=outdir,
            interval=args.poll_interval,
            timeout_minutes=args.timeout_minutes,
            initial_runtime_id=runtime_id,
        )

    summary = {
        "strategy": str(strategy_path),
        "strategy_name": args.name,
        "task_id": task_id,
        "runtime_id": runtime_id,
        "state": state,
        "outdir": str(outdir),
    }
    write_json(outdir / "summary.json", summary)

    if runtime_id and not args.no_fetch:
        performance = fetch_results(runtime_id, outdir)
        if performance and not validate_performance(performance, args, outdir):
            print(f"saved outputs: {outdir}")
            return 3
    elif not runtime_id:
        print("No runtime_id yet. Fetch results after task completion.", file=sys.stderr)

    print(f"saved outputs: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
