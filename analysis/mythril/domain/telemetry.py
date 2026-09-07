"""Domain logic for report telemetry triage, Pareto distribution, and anomaly auditing."""

from typing import Any, Dict

from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_csv_rows


def verify_telemetry(
    harness: VerificationHarness,
    art_dir: str,
    plan_rows: Dict[str, Dict[str, str]],
) -> Dict[str, Any]:
    """Execute section 7 checks: Report usage telemetry analysis."""
    harness.section("7. Report telemetry - parsed from artifacts/report-usage.csv")
    reports = read_csv_rows("report-usage.csv", art_dir)
    for r in reports:
        r["views"] = int(r["views_last_12m"])

    total_views = sum(r["views"] for r in reports)
    zero = [r for r in reports if r["views"] == 0]
    active = [r for r in reports if r["last_viewed"].startswith("2026")]
    dormant = [r for r in reports if r["last_viewed"].strip() and not r["last_viewed"].startswith("2026")]
    active_views = sum(r["views"] for r in active)

    harness.check("catalogue size", len(reports), 120)
    harness.check("total views", total_views, 2309)
    harness.check("zero-view reports (Finding 11)", len(zero), 56)
    harness.check("as a share of the catalogue (%)", round(100.0 * len(zero) / len(reports), 2), 46.67)
    harness.check(
        "every zero-view report also has a null last_viewed",
        sum(1 for r in zero if not r["last_viewed"].strip()),
        len(zero)
    )
    harness.check("reports viewed in 2026", len(active), 38)
    harness.check("views they hold", active_views, 2270)
    harness.check("share of all usage (%)", round(100.0 * active_views / total_views, 2), 98.31)
    harness.check("dormant reports", len(dormant), 26)
    harness.check("their views", sum(r["views"] for r in dormant), 39)
    harness.check("dormant view range", (min(r["views"] for r in dormant), max(r["views"] for r in dormant)), (1, 2))
    harness.check("tiers partition the catalogue", len(zero) + len(active) + len(dormant), len(reports))
    harness.check("reports cut under the recommendation", len(reports) - len(active), 82)

    stale = [r for r in reports if r["last_viewed"].strip() and r["last_viewed"] < "2025-08-31"]
    harness.check("rows whose telemetry contradicts itself", len(stale), 19)
    harness.check("views they claim", sum(r["views"] for r in stale), 28)

    excel_active = sorted(r["report_id"] for r in active if r["source"] == "Excel extract")
    harness.check(
        "Excel-sourced reports in the catalogue",
        sum(1 for r in reports if r["source"] == "Excel extract"),
        30
    )
    harness.check("Excel-sourced reports inside Day-One scope (Finding 13)", len(excel_active), 10)

    scorecards = [r for r in reports if "scorecard" in r["report_name"].lower()]
    harness.check("studio scorecards already in the catalogue (Finding 12)", len(scorecards), 6)
    harness.check("their combined views in 12 months", sum(r["views"] for r in scorecards), 6)
    harness.check("how many were viewed in 2026", sum(1 for r in scorecards if r["last_viewed"].startswith("2026")), 0)
    harness.check(
        "their ids",
        sorted(r["report_id"] for r in scorecards),
        ["RPT-049", "RPT-050", "RPT-051", "RPT-052", "RPT-053", "RPT-054"]
    )

    inherited_effort = int(plan_rows["T06"]["effort_days"])
    rate = inherited_effort / float(len(reports))
    harness.check("inherited unit rate (days per report)", round(rate, 3), 0.333)
    harness.check("effort for the 38, at that rate", int(round(len(active) * rate)), 13)
    harness.check("effort days freed by descoping", inherited_effort - int(round(len(active) * rate)), 27)
    harness.check(
        "zero-view reports among the first 42 rows (the trap in AI_WORKFLOW)",
        sum(1 for r in reports[:42] if r["views"] == 0),
        24
    )
    harness.check(
        "defensible expectation for any unprioritised 42",
        int(round(len(zero) / float(len(reports)) * 42)),
        20
    )

    return {
        "reports": reports,
        "active": active,
        "zero": zero,
        "dormant": dormant,
        "total_views": total_views,
    }
