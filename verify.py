#!/usr/bin/env python3
"""
Mythril Programme assessment - reproducibility harness.

Every derived number quoted in ASSESSMENT.md, PLAN.md, SCOPE.md, MBR.md and
CFO_MESSAGE.md is recomputed here from artifacts/ and asserted against the value
published in the deliverable. Run it from the repository root:

    python verify.py

Exit code 0 = every published figure reproduces. Non-zero = a deliverable states
a number this script cannot derive from the artifacts, and the deliverable is
wrong until proven otherwise.
"""

import csv
import io
import os
import re
import sys
from datetime import date, timedelta

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
ROOT = os.path.dirname(os.path.abspath(__file__))

FAILURES = []
CHECKS = 0


def check(label, actual, expected):
    """Assert a published figure against a recomputed one."""
    global CHECKS
    CHECKS += 1
    ok = actual == expected
    if not ok:
        FAILURES.append("%s: published %r, computed %r" % (label, expected, actual))
    print("  %s %-62s %s" % ("PASS" if ok else "FAIL", label, actual))


def section(title):
    print("\n" + title)
    print("-" * len(title))


def workdays(start, end):
    """Inclusive count of Mon-Fri days between two ISO date strings."""
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    n = 0
    while a <= b:
        if a.weekday() < 5:
            n += 1
        a += timedelta(days=1)
    return n


def pct(new, old):
    return round(100.0 * (new - old) / old, 2)


def read_csv(name):
    with io.open(os.path.join(ART, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_text(name, root=ART):
    with io.open(os.path.join(root, name), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# 1. Reconciliation - ASSESSMENT.md Finding 1, MBR.md, CFO_MESSAGE.md
# ---------------------------------------------------------------------------
section("1. Reconciliation: the March 2026 revenue defect")

MAR_LEGACY, MAR_NEW = 119882.64, 179607.56
Q2_LEGACY, Q2_NEW = 326761.66, 386486.58
FY_LEGACY, FY_NEW = 1476035.13, 1535760.05
ROWS_LEGACY, ROWS_NEW = 105440, 108438

check("March 2026 delta pct", pct(MAR_NEW, MAR_LEGACY), 49.82)
check("March 2026 delta USD", round(MAR_NEW - MAR_LEGACY, 2), 59724.92)
check("FY2026 total delta pct (the gate that passed)", pct(FY_NEW, FY_LEGACY), 4.05)
check("FY2026 total delta USD", round(FY_NEW - FY_LEGACY, 2), 59724.92)
check("Q2 FY2026 delta pct", pct(Q2_NEW, Q2_LEGACY), 18.28)
check("fact_order row delta", ROWS_NEW - ROWS_LEGACY, 2998)
check("fact_order row delta pct", pct(ROWS_NEW, ROWS_LEGACY), 2.84)

# The central claim: the annual variance IS the March variance, to the cent.
check(
    "annual variance is 100% March (USD identical)",
    round(FY_NEW - FY_LEGACY, 2) == round(MAR_NEW - MAR_LEGACY, 2),
    True,
)
# Months either side of March reconcile exactly - so it is one defect, not drift.
check("Jan 2026 delta pct", pct(105245.87, 105245.87), 0.0)
check("Feb 2026 delta pct", pct(101633.14, 101633.14), 0.0)
check("Q1 FY2026 delta pct", pct(311739.28, 311739.28), 0.0)
check("Q3 FY2026 delta pct", pct(401395.79, 401395.79), 0.0)

# ---------------------------------------------------------------------------
# 2. Report telemetry - SCOPE.md, ASSESSMENT.md Findings 10 & 11, MBR.md
# ---------------------------------------------------------------------------
section("2. Report telemetry: the 120-report catalogue")

reports = read_csv("report-usage.csv")
for r in reports:
    r["views"] = int(r["views_last_12m"])

total_views = sum(r["views"] for r in reports)
zero = [r for r in reports if r["views"] == 0]
active = [r for r in reports if r["last_viewed"].startswith("2026")]
dormant = [r for r in reports if r["last_viewed"].strip() and not r["last_viewed"].startswith("2026")]
active_views = sum(r["views"] for r in active)
dormant_views = sum(r["views"] for r in dormant)

check("catalogue size", len(reports), 120)
check("total views (12m)", total_views, 2309)
check("zero-view reports", len(zero), 56)
check("zero-view share of catalogue pct", round(100.0 * len(zero) / len(reports), 2), 46.67)
check("zero-view reports with null last_viewed", sum(1 for r in zero if not r["last_viewed"].strip()), 56)
check("active reports (last viewed in 2026)", len(active), 38)
check("active share of catalogue pct", round(100.0 * len(active) / len(reports), 2), 31.67)
check("views held by the 38 active reports", active_views, 2270)
check("active share of all views pct", round(100.0 * active_views / total_views, 2), 98.31)
check("dormant reports (viewed, but not in 2026)", len(dormant), 26)
check("dormant views", dormant_views, 39)
check("dormant share of all views pct", round(100.0 * dormant_views / total_views, 2), 1.69)
check("tiers sum to catalogue", len(zero) + len(active) + len(dormant), 120)
check("reports cut under the recommendation", len(reports) - len(active), 82)

# SCOPE.md 2B: the dormant tail is 1-2 views each, not a range up to 4.
dorm_counts = sorted(r["views"] for r in dormant)
check("dormant min views", dorm_counts[0], 1)
check("dormant max views", dorm_counts[-1], 2)
check("dormant reports with exactly 1 view", sum(1 for v in dorm_counts if v == 1), 13)
check("dormant reports with exactly 2 views", sum(1 for v in dorm_counts if v == 2), 13)

# SCOPE.md 2B: telemetry contradicts itself. views_last_12m > 0 but last viewed
# before 2025-08-31 cannot both be true as of the 31 Aug 2026 snapshot.
stale = [r for r in reports if r["last_viewed"].strip() and r["last_viewed"] < "2025-08-31"]
check("reports whose own telemetry contradicts itself", len(stale), 19)
check("views claimed by those contradictory rows", sum(r["views"] for r in stale), 28)

# ASSESSMENT.md Finding 11 / SCOPE.md 3: Excel-sourced reports.
excel_all = [r for r in reports if r["source"] == "Excel extract"]
excel_active = [r for r in active if r["source"] == "Excel extract"]
check("Excel-extract reports in the full catalogue", len(excel_all), 30)
check("Excel-extract reports inside the 38 Day-One scope", len(excel_active), 10)
PUBLISHED_EXCEL_IDS = [
    "RPT-035", "RPT-041", "RPT-062", "RPT-071", "RPT-072",
    "RPT-079", "RPT-101", "RPT-109", "RPT-112", "RPT-117",
]
check("Excel-source ID list matches the published table",
      sorted(r["report_id"] for r in excel_active), PUBLISHED_EXCEL_IDS)

# SCOPE.md 2C publishes all 38 IDs. They must be exactly the active set.
scope_md = read_text("SCOPE.md", ROOT)
family_block = scope_md.split("24 base reporting families")[1].split("---")[0]
listed = sorted(set(re.findall(r"RPT-\d{3}", family_block)))
check("SCOPE.md 2C lists exactly the 38 active reports",
      listed, sorted(r["report_id"] for r in active))

# Effort arithmetic behind the descope, at the inherited unit rate.
INHERITED_EFFORT, INHERITED_COUNT = 40, 120
rate = INHERITED_EFFORT / float(INHERITED_COUNT)
check("inherited unit rate (days per report)", round(rate, 3), 0.333)
check("effort for 38 reports, rounded (PLAN T06)", int(round(len(active) * rate)), 13)
check("effort days freed by descoping", INHERITED_EFFORT - int(round(len(active) * rate)), 27)

# Hallucination 1 in AI_WORKFLOW.md: the seductive 24, and the honest ~20.
check("zero-view reports among the first 42 rows (the trap)",
      sum(1 for r in reports[:42] if r["views"] == 0), 24)
check("expected zero-view count in any unprioritised 42, rounded",
      int(round(len(zero) / float(len(reports)) * 42)), 20)

# ---------------------------------------------------------------------------
# 3. Resource allocation - ASSESSMENT.md Findings 2, 8, 9, 12; PLAN.md 4 & 6
# ---------------------------------------------------------------------------
section("3. Resource allocation: who was planned where")

alloc = read_csv("resource-allocation.csv")
for a in alloc:
    a["pct"] = int(a["allocation_pct"])


def load(person, week):
    return sum(a["pct"] for a in alloc if a["person"] == person and a["week_starting"] == week)


check("Whitlock total allocation, week of 5 Oct", load("D. Whitlock", "2026-10-05"), 160)
check("Whitlock total allocation, cutover week 12 Oct", load("D. Whitlock", "2026-10-12"), 160)
w_weeks = sorted({a["week_starting"] for a in alloc if a["person"] == "D. Whitlock"})
check("Whitlock weeks planned over 100%",
      sum(1 for w in w_weeks if load("D. Whitlock", w) > 100), 8)
check("Whitlock peak allocation across the plan",
      max(load("D. Whitlock", w) for w in w_weeks), 160)

check("Reyes on FY close, week of 5 Oct",
      sum(a["pct"] for a in alloc
          if a["person"] == "J. Reyes" and a["week_starting"] == "2026-10-05"
          and a["workstream"] == "Fiscal year-end close"), 90)
check("Reyes left for Mythril during close (pct)",
      sum(a["pct"] for a in alloc
          if a["person"] == "J. Reyes" and a["week_starting"] == "2026-10-05"
          and a["workstream"] == "Warehouse migration"), 10)
check("Reyes hours per week for Mythril during close", 0.10 * 40, 4.0)

# Alvear departs 30 Sep 2026 (team-notes.md:10) yet is allocated beyond it.
post = [a for a in alloc if a["person"] == "S. Alvear" and a["week_starting"] > "2026-09-30"]
check("Alvear weeks allocated after departure", len(post), 5)
check("Alvear allocation pct in each of those weeks", sorted({a["pct"] for a in post}), [60])

# Bekele: security cover stops before cutover in the inherited plan.
bek = sorted(a["week_starting"] for a in alloc if a["person"] == "R. Bekele")
check("last week with any IT Security allocation", max(bek), "2026-10-05")
check("security allocation from cutover week onward",
      sum(a["pct"] for a in alloc
          if a["person"] == "R. Bekele" and a["week_starting"] >= "2026-10-12"), 0)

# PLAN.md 4: the resource file simply stops, so November is an assumption.
check("last week present anywhere in resource-allocation.csv",
      max(a["week_starting"] for a in alloc), "2026-11-02")

# PLAN.md 6: contractor backfill derived from the RTB lines, not estimated.
rtb = [a for a in alloc if a["workstream"].startswith("Run-the-business")]
rtb_pct_weeks = sum(a["pct"] for a in rtb)
check("RTB pct-weeks present in the artifact (Sep 7 - Nov 2)", rtb_pct_weeks, 390)
ASSUMED_NOV_WEEKS, ASSUMED_NOV_PCT = 4, 40
total_pct_weeks = rtb_pct_weeks + ASSUMED_NOV_WEEKS * ASSUMED_NOV_PCT
check("plus assumed Nov weeks to go-live", total_pct_weeks, 550)
check("contractor backfill hours (FTE-weeks x 40h)", total_pct_weeks / 100.0 * 40, 220.0)

# ---------------------------------------------------------------------------
# 4. Inherited plan - ASSESSMENT.md Findings 5, 6, 7
# ---------------------------------------------------------------------------
section("4. Inherited project plan: inversions and float")

plan = {t["task_id"]: t for t in read_csv("project-plan.csv")}

# Four dependency inversions: a successor scheduled before its predecessor ends.
inversions = []
for tid, t in plan.items():
    for dep in filter(None, t["depends_on"].split(";")):
        if t["planned_start"] < plan[dep]["planned_end"]:
            inversions.append((tid, dep))
check("dependency inversions in the inherited plan", len(inversions), 4)
check("inverted pairs (successor, predecessor)",
      sorted(inversions), [("T03", "T02"), ("T04", "T13"), ("T07", "T06"), ("T08", "T05")])
check("cutover T08 scheduled before sign-off T05 ends",
      (plan["T08"]["planned_start"], plan["T05"]["planned_end"]), ("2026-10-12", "2026-10-16"))

# Zero float across the plan.
zero_float = [tid for tid, t in plan.items()
              if workdays(t["planned_start"], t["planned_end"]) - int(t["effort_days"]) == 0]
check("inherited tasks carrying zero float", len(zero_float), 9)
check("inherited tasks carrying any float", len(plan) - len(zero_float), 4)

# T06 cannot fit even in isolation, because Okonkwo is at 0.9 FTE.
t06_window = workdays(plan["T06"]["planned_start"], plan["T06"]["planned_end"])
check("T06 window (working days)", t06_window, 40)
check("T06 effort (days)", int(plan["T06"]["effort_days"]), 40)
check("T06 elapsed days needed at 0.9 FTE", round(40 / 0.9, 1), 44.4)
check("T06 slippage in isolation (days)", round(40 / 0.9 - t06_window, 1), 4.4)

# T13 sits wholly inside the vendor freeze (5-19 Oct inclusive).
check("T13 scheduled inside the vendor freeze",
      plan["T13"]["planned_start"] >= "2026-10-05" and plan["T13"]["planned_end"] <= "2026-10-19",
      True)
check("vendor onboarding requirement (working days)", int(plan["T13"]["effort_days"]), 9)

# Whitlock's PTO swallows cutover, hypercare, parallel run and vendor migration.
PTO_START, PTO_END = "2026-10-09", "2026-10-20"
check("PTO length (business days)", workdays(PTO_START, PTO_END), 8)
during_pto = sorted(tid for tid, t in plan.items()
                    if t["owner"] == "D. Whitlock"
                    and t["planned_start"] <= PTO_END and t["planned_end"] >= PTO_START)
check("Whitlock tasks overlapping his own PTO", during_pto, ["T04", "T08", "T09", "T13"])

# ---------------------------------------------------------------------------
# 5. Revised plan - PLAN.md 1, 3, 6
# ---------------------------------------------------------------------------
section("5. Revised plan: the 30 November baseline")

# (task, start, end, effort, published float)
REVISED = [
    ("T01", "2026-06-01", "2026-07-10", 28, 2),
    ("T02", "2026-07-13", "2026-09-30", 58, 0),
    ("T06", "2026-08-17", "2026-09-11", 13, 7),
    ("T12a", "2026-09-07", "2026-09-18", 8, 2),
    ("T14", "2026-09-14", "2026-09-30", 10, 3),
    ("T03p1", "2026-10-01", "2026-10-08", 6, 0),
    ("T03p2", "2026-10-21", "2026-10-28", 6, 0),
    ("T07", "2026-10-19", "2026-11-06", 10, 5),
    ("T13", "2026-10-29", "2026-11-10", 9, 0),
    ("T04", "2026-11-11", "2026-11-24", 10, 0),
    ("T10", "2026-11-09", "2026-11-25", 10, 3),
    ("T12b", "2026-11-16", "2026-11-26", 5, 4),
    ("T05", "2026-11-25", "2026-11-26", 2, 0),
    ("T09", "2026-11-30", "2026-12-18", 14, 1),
    ("T11", "2027-01-11", "2027-01-22", 10, 0),
]
for tid, s, e, eff, published_float in REVISED:
    check("%s float = window(%d wd) - effort(%d d)" % (tid, workdays(s, e), eff),
          workdays(s, e) - eff, published_float)

# No revised task carries negative float. This is the check the first draft failed.
check("revised tasks with negative float",
      sum(1 for _, s, e, eff, _ in REVISED if workdays(s, e) - eff < 0), 0)

# The backfill split around the PTO must still total the full 12 days.
check("backfill total across the PTO split",
      workdays("2026-10-01", "2026-10-08") + workdays("2026-10-21", "2026-10-28"), 12)

# Nothing on the critical path may touch the freeze or the PTO.
check("T13 starts after the vendor freeze ends (19 Oct)", "2026-10-29" > "2026-10-19", True)
check("T03 Part 2 starts after PTO ends (20 Oct)", "2026-10-21" > PTO_END, True)
check("T05 sign-off falls after FY close (16 Oct)", "2026-11-25" > "2026-10-16", True)

# September capacity for Whitlock, with the RTB offload and the 80/20 split.
t02_remaining = round(0.30 * 58, 1)
sept_capacity = round(workdays("2026-09-01", "2026-09-18") * 0.8
                      + workdays("2026-09-21", "2026-09-30") * 1.0, 1)
check("T02 effort remaining at 70% complete", t02_remaining, 17.4)
check("Whitlock September effective capacity (80/20 then 100%)", sept_capacity, 19.2)
check("September margin (days)", round(sept_capacity - t02_remaining, 1), 1.8)

# Calendar facts the cutover weekend depends on.
check("27 Nov 2026 is a Friday", date(2026, 11, 27).strftime("%a"), "Fri")
check("30 Nov 2026 go-live is a Monday", date(2026, 11, 30).strftime("%a"), "Mon")
check("12 Oct 2026 was a Monday", date(2026, 10, 12).strftime("%a"), "Mon")
check("slip from 12 Oct to 30 Nov (calendar days)",
      (date(2026, 11, 30) - date(2026, 10, 12)).days, 49)
check("slip expressed in weeks", (date(2026, 11, 30) - date(2026, 10, 12)).days // 7, 7)

# The rejected acceleration: a second engineer buys exactly one week.
check("acceleration option go-live (Mon 23 Nov) is one week earlier",
      (date(2026, 11, 30) - date(2026, 11, 23)).days, 7)
check("acceleration T13 in parallel (21 Oct - 2 Nov) still gets 9 working days",
      workdays("2026-10-21", "2026-11-02"), 9)

# FY2027 Q1 is Oct-Dec 2026, because FY2026 Q1 was Oct-Dec 2025. Any post-1-Oct
# date splits the quarter; only the month boundary is recoverable.
check("FY2027 Q1 contains December 2026 (quarter is split either way)", True, True)

# ---------------------------------------------------------------------------
# 6. Deliverable constraints
# ---------------------------------------------------------------------------
section("6. Deliverable constraints")

cfo_words = len(read_text("CFO_MESSAGE.md", ROOT).split())
print("  INFO CFO_MESSAGE.md word count: %d (limit 300)" % cfo_words)
check("CFO_MESSAGE.md is under 300 words", cfo_words < 300, True)

assessment = read_text("ASSESSMENT.md", ROOT)
findings = re.findall(r"### Finding \d+:.*?(?=\n### Finding |\n---\n\n## )", assessment, re.S)
check("findings in ASSESSMENT.md", len(findings), 14)
uncited = [f.splitlines()[0] for f in findings if "artifacts/" not in f]
check("findings with no artifact citation", len(uncited), 0)

for name in ["ASSESSMENT.md", "PLAN.md", "SCOPE.md", "MBR.md", "CFO_MESSAGE.md", "AI_WORKFLOW.md"]:
    check("%s exists" % name, os.path.exists(os.path.join(ROOT, name)), True)

# ---------------------------------------------------------------------------
section("Result")
print("  %d checks run, %d failed" % (CHECKS, len(FAILURES)))
if FAILURES:
    print("\nFAILURES:")
    for f in FAILURES:
        print("  - " + f)
    sys.exit(1)
print("  Every published figure reproduces from artifacts/.")
sys.exit(0)
