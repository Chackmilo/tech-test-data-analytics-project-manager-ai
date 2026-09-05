"""Domain logic for resource allocation matrix, peak over-allocations, and contractor models."""

from typing import Any, Dict

from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_csv_rows


def verify_resources(
    harness: VerificationHarness,
    art_dir: str,
    plan_rows: Dict[str, Dict[str, str]],
    alvear_exit: str,
) -> Dict[str, Any]:
    """Execute section 6 checks: Resource allocation analysis."""
    harness.section("6. Resource allocation - parsed from artifacts/resource-allocation.csv")
    alloc = read_csv_rows("resource-allocation.csv", art_dir)
    for a in alloc:
        a["pct"] = int(a["allocation_pct"])

    def load(person: str, week: str) -> int:
        return sum(a["pct"] for a in alloc if a["person"] == person and a["week_starting"] == week)

    weeks = sorted({a["week_starting"] for a in alloc})
    w_weeks = sorted({a["week_starting"] for a in alloc if a["person"] == "D. Whitlock"})
    over = sorted(w for w in w_weeks if load("D. Whitlock", w) > 100)

    harness.check("Whitlock peak allocation (Finding 2)", max(load("D. Whitlock", w) for w in w_weeks), 160)
    harness.check(
        "weeks at that peak",
        [w for w in w_weeks if load("D. Whitlock", w) == 160],
        ["2026-10-05", "2026-10-12"]
    )
    harness.check("Whitlock weeks planned over 100%", len(over), 8)
    harness.check("cutover week is one of them", plan_rows["T08"]["planned_start"][:7] in " ".join(over), True)

    reyes_close = [a for a in alloc if a["person"] == "J. Reyes" and a["workstream"] == "Fiscal year-end close"]
    harness.check("Reyes peak on year-end close (Finding 9)", max(a["pct"] for a in reyes_close), 90)
    harness.check(
        "weeks at 90% on close",
        sorted(a["week_starting"] for a in reyes_close if a["pct"] == 90),
        ["2026-10-05", "2026-10-12"]
    )
    harness.check("Reyes hours per week left for Mythril during close", load("J. Reyes", "2026-10-05") - 90, 10)

    post_exit = [a for a in alloc if a["person"] == "S. Alvear" and a["week_starting"] > alvear_exit]
    harness.check("Alvear weeks allocated after departure (Finding 10)", len(post_exit), 5)
    harness.check("at what allocation", sorted({a["pct"] for a in post_exit}), [60])

    bek = sorted(a["week_starting"] for a in alloc if a["person"] == "R. Bekele")
    harness.check("last week with any security allocation (Finding 14)", max(bek), "2026-10-05")
    harness.check(
        "security allocation from cutover week onward",
        sum(a["pct"] for a in alloc
            if a["person"] == "R. Bekele" and a["week_starting"] >= plan_rows["T08"]["planned_start"]),
        0
    )

    harness.check("resource file stops here, so November is an assumption", max(weeks), "2026-11-02")

    rtb = [a for a in alloc if a["workstream"].startswith("Run-the-business")]
    rtb_pct_weeks = sum(a["pct"] for a in rtb)
    harness.check("RTB percentage-weeks present in the artifact", rtb_pct_weeks, 390)
    harness.check(
        "contractor hours, scenario A (+4 assumed weeks at 40%)",
        (rtb_pct_weeks + 4 * 40) / 100.0 * 40,
        220.0
    )
    harness.check(
        "contractor hours, scenario B (+8 assumed weeks at 40%)",
        (rtb_pct_weeks + 8 * 40) / 100.0 * 40,
        284.0
    )

    return {
        "alloc": alloc,
        "rtb_pct_weeks": rtb_pct_weeks,
    }
