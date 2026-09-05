"""Domain logic for inherited schedule, dependency inversions, and float analysis."""

import re
from datetime import date, timedelta
from typing import Any, Dict

from mythril.core.calendar import get_thanksgiving, workdays
from mythril.core.harness import VerificationHarness


def verify_inherited_plan(
    harness: VerificationHarness,
    plan_rows: Dict[str, Dict[str, str]],
    freeze_start: str,
    freeze_end: str,
    onboard: int,
    pto_start: str,
    pto_end: str,
) -> Dict[str, Any]:
    """Execute section 5 checks: Inherited project plan constraints."""
    harness.section("5. Inherited plan - parsed from artifacts/project-plan.csv")

    inversions = sorted(
        (tid, dep)
        for tid, t in plan_rows.items()
        for dep in filter(None, t["depends_on"].split(";"))
        if t["planned_start"] < plan_rows[dep]["planned_end"]
    )
    harness.check("dependency inversions (Finding 5)", len(inversions), 4)
    harness.check(
        "the inverted pairs",
        inversions,
        [("T03", "T02"), ("T04", "T13"), ("T07", "T06"), ("T08", "T05")]
    )

    zero_float = sorted(
        tid for tid, t in plan_rows.items()
        if workdays(t["planned_start"], t["planned_end"]) == int(t["effort_days"])
    )
    harness.check("tasks at exactly zero float (Finding 6)", len(zero_float), 9)
    harness.check("which tasks", zero_float, ["T02", "T04", "T05", "T06", "T07", "T08", "T09", "T10", "T11"])

    t06 = plan_rows["T06"]
    harness.check(
        "T06 window equals its effort exactly",
        workdays(t06["planned_start"], t06["planned_end"]),
        int(t06["effort_days"])
    )
    harness.check("T06 elapsed days needed at 0.9 FTE (Finding 8)", round(int(t06["effort_days"]) / 0.9, 1), 44.4)

    t13 = plan_rows["T13"]
    harness.check(
        "T13 sits wholly inside the vendor freeze (Finding 3)",
        t13["planned_start"] >= freeze_start and t13["planned_end"] <= freeze_end,
        True
    )
    harness.check("T13 effort matches the vendor's stated requirement", int(t13["effort_days"]), onboard)

    whit_in_pto = sorted(
        tid for tid, t in plan_rows.items()
        if t["owner"] == "D. Whitlock"
        and t["planned_start"] <= pto_end and t["planned_end"] >= pto_start
    )
    harness.check("Whitlock tasks overlapping his own PTO (Finding 2)", whit_in_pto, ["T04", "T08", "T09", "T13"])

    t11 = plan_rows["T11"]
    thanksgiving = get_thanksgiving(2026)
    harness.check(
        "legacy decommission completes before peak trading (Finding 7)",
        t11["planned_end"] < thanksgiving.isoformat(),
        True
    )
    harness.check(
        "days between decommission and Black Friday",
        (thanksgiving + timedelta(days=1) - date.fromisoformat(t11["planned_end"])).days,
        14
    )
    harness.check(
        "no rollback or dual-run task exists in the inherited plan",
        [t for t in plan_rows.values() if re.search(r"rollback|dual|retention", t["task_name"], re.I)],
        []
    )

    return {
        "inversions": inversions,
        "zero_float": zero_float,
        "whit_in_pto": whit_in_pto,
        "thanksgiving": thanksgiving,
    }
