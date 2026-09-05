"""Domain logic for August status report verification and burn-rate calculations."""

import re
from datetime import date
from typing import Any, Dict

from mythril.core.calendar import MONTHS
from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_csv_rows, read_text
from mythril.parsers.markdown import md_rows


def verify_status_report(harness: VerificationHarness, art_dir: str) -> Dict[str, Any]:
    """Execute section 4 checks: August status report forensic analysis."""
    harness.section("4. August status report - parsed from artifacts/status-report-2026-08.md")
    status = read_text("status-report-2026-08.md", art_dir)

    harness.check("overall status reported as GREEN", "## Overall status: \U0001F7E2 GREEN" in status, True)
    harness.check("no asks raised to the committee", "None this month" in status, True)

    milestones: Dict[str, str] = {}
    for cells in md_rows(status):
        if len(cells) == 2 and "Date" not in cells[1]:
            milestones[re.sub(r"[*]", "", cells[0]).strip()] = cells[1].strip()

    def milestone_date(label: str, year: int = 2026) -> date:
        m = re.search(r"(\d{1,2}) ([A-Z][a-z]+)", milestones[label])
        return date(year, MONTHS[m.group(2)], int(m.group(1)))

    ms_cutover = milestone_date("Production cutover")
    ms_parallel = milestone_date("Parallel run complete")
    harness.check("cutover date parsed from the milestone table", ms_cutover, date(2026, 10, 12))
    harness.check("parallel-run completion parsed from the milestone table", ms_parallel, date(2026, 10, 14))
    harness.check(
        "status report published cutover BEFORE parallel run completes (Finding 4)",
        ms_cutover < ms_parallel,
        True
    )
    harness.check("days by which go-live preceded its own testing", (ms_parallel - ms_cutover).days, 2)

    r03 = [c for c in md_rows(status) if c and c[0] == "R-03"][0]
    harness.check("vendor risk severity as published", r03[2], "Low")
    harness.check("its mitigation as published", r03[4], "Vendor notified, awaiting confirmation")

    budget = re.search(r"(\d+)% consumed against (\d+)% elapsed", status)
    consumed, claimed_elapsed = int(budget.group(1)), int(budget.group(2))

    plan_rows_list = read_csv_rows("project-plan.csv", art_dir)
    plan_rows = {r["task_id"]: r for r in plan_rows_list}
    project_start = min(r["planned_start"] for r in plan_rows.values())
    cutover = plan_rows["T08"]["planned_start"]
    as_of = "2026-08-31"

    elapsed = round(
        100.0 * (date.fromisoformat(as_of) - date.fromisoformat(project_start)).days
        / (date.fromisoformat(cutover) - date.fromisoformat(project_start)).days,
        1
    )
    harness.check("budget consumed as published", consumed, 71)
    harness.check("elapsed as published", claimed_elapsed, 74)
    harness.check("elapsed recomputed against the committed cutover", elapsed, 68.4)
    harness.check("so the programme was spending AHEAD of elapsed time (Finding 16)", consumed > elapsed, True)

    return {
        "ms_cutover": ms_cutover,
        "ms_parallel": ms_parallel,
        "consumed": consumed,
        "elapsed": elapsed,
        "plan_rows": plan_rows,
        "cutover": cutover,
    }
