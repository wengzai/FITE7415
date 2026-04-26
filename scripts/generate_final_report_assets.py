from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKTESTS = ROOT / "Program" / "XAUUSD-ZEntry-Grid" / "backtests"
OUT = ROOT / "Program" / "XAUUSD-ZEntry-Grid" / "final_report"
ASSETS = OUT / "assets"


RUNS = {
    "full": "20260425_223434",
    "weak_2025h2": "20260425_224001",
    "cost1": "20260425_224037",
    "year_2023": "20260426_115022",
    "year_2024": "20260426_115052",
    "year_2025": "20260426_115123",
    "h1_2025": "20260426_115158",
    "cost2": "20260426_115227",
    "cost3": "20260426_115311",
    "cost5": "20260426_115403",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def performance(run_key: str) -> dict[str, Any]:
    stats = read_json(BACKTESTS / RUNS[run_key] / "stats.json")
    return stats["performance"]


def pl_rows(run_key: str) -> list[dict[str, Any]]:
    data = read_json(BACKTESTS / RUNS[run_key] / "pl.json")
    return data.get("res", [])


def fmt_float(value: Any, digits: int = 4) -> str:
    return f"{float(value):.{digits}f}"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines) + "\n"


def write_summary_tables() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    full = performance("full")
    summary_rows = [[
        "Round 35 final",
        str(int(full["TradeCnt"])),
        f"+{fmt_float(full['TotalPnL'])}",
        fmt_float(full["AnnualSharpe"]),
        fmt_float(full["AnnualSortino"]),
        fmt_float(full["maxDrawdown_pct"]),
        fmt_float(full["profit_factor"]),
    ]]
    (OUT / "summary_metrics.md").write_text(
        markdown_table(
            ["Version", "TradeCnt", "TotalPnL", "Sharpe", "Sortino", "MaxDD", "Profit factor"],
            summary_rows,
        ),
        encoding="utf-8",
    )

    segment_keys = [
        ("2023", "year_2023"),
        ("2024", "year_2024"),
        ("2025", "year_2025"),
        ("2025H1", "h1_2025"),
        ("2025H2", "weak_2025h2"),
    ]
    segment_rows: list[list[str]] = []
    for label, key in segment_keys:
        p = performance(key)
        segment_rows.append([
            label,
            str(int(p["TradeCnt"])),
            f"+{fmt_float(p['TotalPnL'])}",
            fmt_float(p["AnnualSharpe"]),
            fmt_float(p["maxDrawdown_pct"]),
        ])
    (OUT / "segment_robustness.md").write_text(
        markdown_table(["Segment", "TradeCnt", "TotalPnL", "Sharpe", "MaxDD"], segment_rows),
        encoding="utf-8",
    )

    cost_keys = [
        ("Base", "full"),
        ("TradeCost=1", "cost1"),
        ("TradeCost=2", "cost2"),
        ("TradeCost=3", "cost3"),
        ("TradeCost=5", "cost5"),
    ]
    cost_rows: list[list[str]] = []
    for label, key in cost_keys:
        p = performance(key)
        cost_rows.append([
            label,
            str(int(p["TradeCnt"])),
            f"+{fmt_float(p['TotalPnL'])}",
            fmt_float(p["AnnualSharpe"]),
            fmt_float(p["maxDrawdown_pct"]),
        ])
    (OUT / "cost_stress.md").write_text(
        markdown_table(["Setting", "TradeCnt", "TotalPnL", "Sharpe", "MaxDD"], cost_rows),
        encoding="utf-8",
    )


def monthly_pnl() -> list[tuple[str, float]]:
    rows = pl_rows("full")
    by_month: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        date = datetime.strptime(row["Acdate"], "%Y-%m-%d")
        by_month[date.strftime("%Y-%m")].append(float(row["TotalPL"]))

    months = sorted(by_month)
    result: list[tuple[str, float]] = []
    previous = 0.0
    for month in months:
        ending = by_month[month][-1]
        result.append((month, ending - previous))
        previous = ending
    return result


def write_monthly_outputs() -> None:
    months = monthly_pnl()
    with (OUT / "monthly_pnl.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Month", "PnL"])
        writer.writerows(months)

    rows = [[month, f"{pnl:+.2f}"] for month, pnl in months]
    (OUT / "monthly_pnl.md").write_text(
        markdown_table(["Month", "PnL"], rows),
        encoding="utf-8",
    )


def points_from_pl() -> list[tuple[str, float]]:
    return [(row["Acdate"], float(row["TotalPL"])) for row in pl_rows("full")]


def draw_svg_line(path: Path, points: list[tuple[str, float]], title: str, y_label: str, color: str) -> None:
    width, height = 960, 420
    left, right, top, bottom = 70, 20, 48, 58
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = [p[1] for p in points]
    min_y = min(values)
    max_y = max(values)
    if min_y == max_y:
        min_y -= 1
        max_y += 1
    pad = (max_y - min_y) * 0.08
    min_y -= pad
    max_y += pad

    coords: list[str] = []
    n = max(len(points) - 1, 1)
    for i, (_date, value) in enumerate(points):
        x = left + plot_w * i / n
        y = top + plot_h * (max_y - value) / (max_y - min_y)
        coords.append(f"{x:.1f},{y:.1f}")

    axis_labels = []
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        value = max_y - (max_y - min_y) * frac
        y = top + plot_h * frac
        axis_labels.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e5e7eb" />'
            f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#475569">{value:.0f}</text>'
        )

    date_labels = [
        (points[0][0], left),
        (points[len(points) // 2][0], left + plot_w / 2),
        (points[-1][0], left + plot_w),
    ]
    x_labels = "\n".join(
        f'<text x="{x:.1f}" y="{height-22}" text-anchor="middle" font-size="11" fill="#475569">{label}</text>'
        for label, x in date_labels
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{width/2}" y="25" text-anchor="middle" font-size="18" font-family="Arial" fill="#111827">{title}</text>
  <text x="18" y="{height/2}" text-anchor="middle" font-size="12" font-family="Arial" fill="#475569" transform="rotate(-90 18 {height/2})">{y_label}</text>
  {''.join(axis_labels)}
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#94a3b8"/>
  <line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#94a3b8"/>
  <polyline points="{' '.join(coords)}" fill="none" stroke="{color}" stroke-width="2.5"/>
  {x_labels}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_charts() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    equity = points_from_pl()
    draw_svg_line(ASSETS / "equity_curve.svg", equity, "Round 35 Equity Curve", "Cumulative PnL (USD)", "#2563eb")

    drawdown_points: list[tuple[str, float]] = []
    peak = 0.0
    for date, value in equity:
        peak = max(peak, value)
        drawdown_points.append((date, value - peak))
    draw_svg_line(ASSETS / "drawdown_curve.svg", drawdown_points, "Round 35 Drawdown Curve", "Drawdown (USD)", "#dc2626")

    months = monthly_pnl()
    draw_svg_line(ASSETS / "monthly_pnl.svg", months, "Round 35 Monthly PnL", "Monthly PnL (USD)", "#16a34a")


def main() -> None:
    write_summary_tables()
    write_monthly_outputs()
    write_charts()
    print(f"saved report assets to {OUT}")


if __name__ == "__main__":
    main()
