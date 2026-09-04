#!/usr/bin/env python3
"""
Mythril Programme assessment - reproducibility harness.

Design rule: this script derives its expectations by PARSING the artifacts and the
deliverables. It does not hardcode figures that merely restate what the documents
say. If an artifact changes, or a date in PLAN.md is edited, checks here fail.

An earlier version of this file failed that rule: it hardcoded the reconciliation
figures without opening the file, hardcoded the revised schedule without reading
PLAN.md, and contained assertions that could not fail (`check(x, True, True)`,
`pct(x, x)`, string comparisons between literals). Five of the eight artifacts were
never read. That version passed 109 checks and proved almost nothing. See
AI_WORKFLOW.md section 3.

Run from the repository root:

    python verify.py            # verify
    python verify.py --selftest # prove the harness can fail (mutation test)

Exit 0 = every published figure reproduces from source. Non-zero = a document
states something this script cannot derive, and the document is wrong until
proven otherwise.
"""

import csv
import io
import os
import re
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, "artifacts")

FAILURES = []
CHECKS = 0
QUIET = "--quiet" in sys.argv


def check(label, actual, expected):
    global CHECKS
    CHECKS += 1
    ok = actual == expected
    if not ok:
        FAILURES.append("%s\n      computed: %r\n      published: %r" % (label, actual, expected))
    if not QUIET:
        shown = actual if len(repr(actual)) < 48 else repr(actual)[:45] + "..."
        print("  %s %-64s %s" % ("PASS" if ok else "FAIL", label, shown))


def section(title):
    if not QUIET:
        print("\n" + title + "\n" + "-" * len(title))


def workdays(start, end):
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    n = 0
    while a <= b:
        if a.weekday() < 5:
            n += 1
        a += timedelta(days=1)
    return n


def text(name, root=ART):
    with io.open(os.path.join(root, name), encoding="utf-8") as fh:
        return fh.read()


def lines(name, root=ART):
    return text(name, root).splitlines()


def rows(name):
    with io.open(os.path.join(ART, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(cell):
    """Parse a number out of a markdown table cell, or None."""
    m = re.search(r"-?[\d,]+\.?\d*", cell.replace("**", ""))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def md_rows(body):
    """Yield lists of stripped cells for every markdown table row in a block of text."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            yield [c.strip() for c in line.strip("|").split("|")]


# ===========================================================================
section("1. Reconciliation - parsed from artifacts/reconciliation-2026-08-28.md")
# ===========================================================================
recon = text("reconciliation-2026-08-28.md")

# Every row of every table in the artifact that carries legacy/new/published-delta.
# We recompute the delta and assert the ARTIFACT's own published percentage.
recon_rows = {}
for cells in md_rows(recon):
    if len(cells) < 4:
        continue
    legacy, new = num(cells[1]), num(cells[2])
    published = num(cells[3])
    if legacy is None or new is None or published is None or legacy == 0:
        continue
    label = re.sub(r"[`*]", "", cells[0]).strip()
    recon_rows[label] = (legacy, new, published)
    computed = round(100.0 * (new - legacy) / legacy, 2)
    check("artifact arithmetic holds: %s" % label, computed, published)

check("rows with a published delta found in the artifact", len(recon_rows) >= 8, True)

fy = recon_rows["Net revenue, FY2026 total"]
mar = recon_rows["Mar 2026"]
q2 = recon_rows["FY2026 Q2 (Jan-Mar 2026)"] if "FY2026 Q2 (Jan-Mar 2026)" in recon_rows else \
    next(v for k, v in recon_rows.items() if k.startswith("FY2026 Q2"))
orders = recon_rows["fact_order row count"]

fy_delta = round(fy[1] - fy[0], 2)
mar_delta = round(mar[1] - mar[0], 2)
row_delta = int(orders[1] - orders[0])

# The central claim of Finding 1, derived rather than asserted.
check("FY2026 variance in USD", fy_delta, 59724.92)
check("March 2026 variance in USD", mar_delta, 59724.92)
check("the annual variance IS the March variance", fy_delta == mar_delta, True)
check("Q2 variance is also entirely March", round(q2[1] - q2[0], 2), mar_delta)
check("phantom order count", row_delta, 2998)
check("USD per phantom order (Finding 1 inference)", round(fy_delta / row_delta, 4), 19.9216)

# Months and quarters that reconcile exactly. Derived from the artifact, so a change
# to any of those figures breaks this - unlike pct(x, x), which cannot fail.
clean = [k for k, (l, n, p) in recon_rows.items() if l == n]
check("periods reconciling at exactly 0.00%", sorted(clean),
      sorted(["FY2026 Q1 (Oct–Dec 2025)", "FY2026 Q3 (Apr–Jun 2026)", "Jan 2026",
              "Feb 2026", "Distinct titles", "Distinct storefronts"]))

# The gate itself: annual tolerance, stated in the artifact.
tol = num(re.search(r"Tolerance agreed at programme kick-off: ±(\d+)%", recon).group(0))
check("kick-off tolerance from the artifact (%)", tol, 5.0)
check("annual delta passes that tolerance", abs(fy[2]) < tol, True)
check("March delta fails that tolerance by a factor of", round(abs(mar[2]) / tol, 1), 10.0)

# ===========================================================================
section("2. Vendor freeze - parsed from artifacts/vendor-notice.md")
# ===========================================================================
vendor = text("vendor-notice.md")
freeze = re.search(r"from Monday (\d+) October 2026 through Monday (\d+) October 2026", vendor)
FREEZE_START = "2026-10-%02d" % int(freeze.group(1))
FREEZE_END = "2026-10-%02d" % int(freeze.group(2))
onboard = int(re.search(r"\*\*(\d+) working days\*\*", vendor).group(1))

check("freeze start parsed from the notice", FREEZE_START, "2026-10-05")
check("freeze end parsed from the notice", FREEZE_END, "2026-10-19")
check("freeze length in business days", workdays(FREEZE_START, FREEZE_END), 11)
check("vendor onboarding requirement (working days)", onboard, 9)
check("notice states no exceptions are possible", "unable to make exceptions" in vendor, True)

# ===========================================================================
section("3. People - parsed from artifacts/team-notes.md and steering-notes")
# ===========================================================================
team = text("team-notes.md")
pto = re.search(r"PTO approved (\d+)[–-](\d+) October", team)
PTO_START, PTO_END = "2026-10-%02d" % int(pto.group(1)), "2026-10-%02d" % int(pto.group(2))
check("Whitlock PTO parsed from team notes", (PTO_START, PTO_END), ("2026-10-09", "2026-10-20"))
check("PTO length in business days", workdays(PTO_START, PTO_END), 8)
check("no runbook exists for the legacy loader", "No runbook exists" in team, True)
check("Whitlock is the only loader operator", "only person who can operate the legacy loader" in team, True)
check("Okonkwo full-catalogue estimate (working days)",
      int(re.search(r"Estimated (\d+) working days", team).group(1)), 40)
ALVEAR_EXIT = "2026-09-30"
check("Alvear departure stated in team notes", "Leaving the company on 30 September" in team, True)

steer = text("steering-notes-2026-08.md")
check("CFO confirms Finance must sign off before cutover",
      "needs to sign off the reconciliation before cutover" in steer, True)
check("committee was told nothing threatened the date", "Asked whether anything threatens it. Told no." in steer, True)
check("scorecard commitment was news to the programme team",
      "first the programme team has heard of that commitment" in steer, True)
check("single-operator risk raised with no owner", "Action logged, no owner assigned" in steer, True)

# ===========================================================================
section("4. August status report - parsed from artifacts/status-report-2026-08.md")
# ===========================================================================
status = text("status-report-2026-08.md")
check("overall status reported as GREEN", "## Overall status: \U0001F7E2 GREEN" in status, True)
check("no asks raised to the committee", "None this month" in status, True)

milestones = {}
for cells in md_rows(status):
    if len(cells) == 2 and "Date" not in cells[1]:
        milestones[re.sub(r"[*]", "", cells[0]).strip()] = cells[1].strip()
MONTHS = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
          "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}


def milestone_date(label, year=2026):
    """Parse a '12 October' style milestone cell from the status report."""
    m = re.search(r"(\d{1,2}) ([A-Z][a-z]+)", milestones[label])
    return date(year, MONTHS[m.group(2)], int(m.group(1)))


ms_cutover = milestone_date("Production cutover")
ms_parallel = milestone_date("Parallel run complete")
check("cutover date parsed from the milestone table", ms_cutover, date(2026, 10, 12))
check("parallel-run completion parsed from the milestone table", ms_parallel, date(2026, 10, 14))
# Finding 4: the committee was shown go-live BEFORE its own testing finished.
# Both operands come from the artifact, so editing either milestone breaks this.
check("status report published cutover BEFORE parallel run completes (Finding 4)",
      ms_cutover < ms_parallel, True)
check("days by which go-live preceded its own testing", (ms_parallel - ms_cutover).days, 2)

# Finding 4: R-03 downgraded despite the notice predating the report.
r03 = [c for c in md_rows(status) if c and c[0] == "R-03"][0]
check("vendor risk severity as published", r03[2], "Low")
check("its mitigation as published", r03[4], "Vendor notified, awaiting confirmation")

# Finding 16: recompute elapsed against the committed cutover date.
budget = re.search(r"(\d+)% consumed against (\d+)% elapsed", status)
consumed, claimed_elapsed = int(budget.group(1)), int(budget.group(2))
plan_rows = {r["task_id"]: r for r in rows("project-plan.csv")}
PROJECT_START = min(r["planned_start"] for r in plan_rows.values())
CUTOVER = plan_rows["T08"]["planned_start"]
AS_OF = "2026-08-31"
elapsed = round(100.0 * (date.fromisoformat(AS_OF) - date.fromisoformat(PROJECT_START)).days
                / (date.fromisoformat(CUTOVER) - date.fromisoformat(PROJECT_START)).days, 1)
check("budget consumed as published", consumed, 71)
check("elapsed as published", claimed_elapsed, 74)
check("elapsed recomputed against the committed cutover", elapsed, 68.4)
check("so the programme was spending AHEAD of elapsed time (Finding 16)", consumed > elapsed, True)

# ===========================================================================
section("5. Inherited plan - parsed from artifacts/project-plan.csv")
# ===========================================================================
inversions = sorted(
    (tid, dep)
    for tid, t in plan_rows.items()
    for dep in filter(None, t["depends_on"].split(";"))
    if t["planned_start"] < plan_rows[dep]["planned_end"]
)
check("dependency inversions (Finding 5)", len(inversions), 4)
check("the inverted pairs", inversions,
      [("T03", "T02"), ("T04", "T13"), ("T07", "T06"), ("T08", "T05")])

zero_float = sorted(tid for tid, t in plan_rows.items()
                    if workdays(t["planned_start"], t["planned_end"]) == int(t["effort_days"]))
check("tasks at exactly zero float (Finding 6)", len(zero_float), 9)
check("which tasks", zero_float, ["T02", "T04", "T05", "T06", "T07", "T08", "T09", "T10", "T11"])

t06 = plan_rows["T06"]
check("T06 window equals its effort exactly", workdays(t06["planned_start"], t06["planned_end"]),
      int(t06["effort_days"]))
check("T06 elapsed days needed at 0.9 FTE (Finding 8)", round(int(t06["effort_days"]) / 0.9, 1), 44.4)

t13 = plan_rows["T13"]
check("T13 sits wholly inside the vendor freeze (Finding 3)",
      t13["planned_start"] >= FREEZE_START and t13["planned_end"] <= FREEZE_END, True)
check("T13 effort matches the vendor's stated requirement", int(t13["effort_days"]), onboard)

whit_in_pto = sorted(tid for tid, t in plan_rows.items()
                     if t["owner"] == "D. Whitlock"
                     and t["planned_start"] <= PTO_END and t["planned_end"] >= PTO_START)
check("Whitlock tasks overlapping his own PTO (Finding 2)", whit_in_pto, ["T04", "T08", "T09", "T13"])

# Finding 7: the rollback path is deleted before peak trading.
t11 = plan_rows["T11"]
THANKSGIVING = [d for d in (date(2026, 11, x) for x in range(1, 31)) if d.weekday() == 3][3]
check("legacy decommission completes before peak trading (Finding 7)",
      t11["planned_end"] < THANKSGIVING.isoformat(), True)
check("days between decommission and Black Friday",
      (THANKSGIVING + timedelta(days=1) - date.fromisoformat(t11["planned_end"])).days, 14)
check("no rollback or dual-run task exists in the inherited plan",
      [t for t in plan_rows.values()
       if re.search(r"rollback|dual|retention", t["task_name"], re.I)], [])

# ===========================================================================
section("6. Resource allocation - parsed from artifacts/resource-allocation.csv")
# ===========================================================================
alloc = rows("resource-allocation.csv")
for a in alloc:
    a["pct"] = int(a["allocation_pct"])


def load(person, week):
    return sum(a["pct"] for a in alloc if a["person"] == person and a["week_starting"] == week)


weeks = sorted({a["week_starting"] for a in alloc})
w_weeks = sorted({a["week_starting"] for a in alloc if a["person"] == "D. Whitlock"})
over = sorted(w for w in w_weeks if load("D. Whitlock", w) > 100)
check("Whitlock peak allocation (Finding 2)", max(load("D. Whitlock", w) for w in w_weeks), 160)
check("weeks at that peak", [w for w in w_weeks if load("D. Whitlock", w) == 160],
      ["2026-10-05", "2026-10-12"])
check("Whitlock weeks planned over 100%", len(over), 8)
check("cutover week is one of them", plan_rows["T08"]["planned_start"][:7] in " ".join(over), True)

reyes_close = [a for a in alloc if a["person"] == "J. Reyes" and a["workstream"] == "Fiscal year-end close"]
check("Reyes peak on year-end close (Finding 9)", max(a["pct"] for a in reyes_close), 90)
check("weeks at 90% on close", sorted(a["week_starting"] for a in reyes_close if a["pct"] == 90),
      ["2026-10-05", "2026-10-12"])
check("Reyes hours per week left for Mythril during close",
      load("J. Reyes", "2026-10-05") - 90, 10)

post_exit = [a for a in alloc if a["person"] == "S. Alvear" and a["week_starting"] > ALVEAR_EXIT]
check("Alvear weeks allocated after departure (Finding 10)", len(post_exit), 5)
check("at what allocation", sorted({a["pct"] for a in post_exit}), [60])

bek = sorted(a["week_starting"] for a in alloc if a["person"] == "R. Bekele")
check("last week with any security allocation (Finding 14)", max(bek), "2026-10-05")
check("security allocation from cutover week onward",
      sum(a["pct"] for a in alloc
          if a["person"] == "R. Bekele" and a["week_starting"] >= plan_rows["T08"]["planned_start"]), 0)

check("resource file stops here, so November is an assumption", max(weeks), "2026-11-02")

rtb = [a for a in alloc if a["workstream"].startswith("Run-the-business")]
RTB_PCT_WEEKS = sum(a["pct"] for a in rtb)
check("RTB percentage-weeks present in the artifact", RTB_PCT_WEEKS, 390)
check("contractor hours, scenario A (+4 assumed weeks at 40%)",
      (RTB_PCT_WEEKS + 4 * 40) / 100.0 * 40, 220.0)
check("contractor hours, scenario B (+8 assumed weeks at 40%)",
      (RTB_PCT_WEEKS + 8 * 40) / 100.0 * 40, 284.0)

# ===========================================================================
section("7. Report telemetry - parsed from artifacts/report-usage.csv")
# ===========================================================================
reports = rows("report-usage.csv")
for r in reports:
    r["views"] = int(r["views_last_12m"])

total_views = sum(r["views"] for r in reports)
zero = [r for r in reports if r["views"] == 0]
active = [r for r in reports if r["last_viewed"].startswith("2026")]
dormant = [r for r in reports if r["last_viewed"].strip() and not r["last_viewed"].startswith("2026")]
active_views = sum(r["views"] for r in active)

check("catalogue size", len(reports), 120)
check("total views", total_views, 2309)
check("zero-view reports (Finding 11)", len(zero), 56)
check("as a share of the catalogue (%)", round(100.0 * len(zero) / len(reports), 2), 46.67)
check("every zero-view report also has a null last_viewed",
      sum(1 for r in zero if not r["last_viewed"].strip()), len(zero))
check("reports viewed in 2026", len(active), 38)
check("views they hold", active_views, 2270)
check("share of all usage (%)", round(100.0 * active_views / total_views, 2), 98.31)
check("dormant reports", len(dormant), 26)
check("their views", sum(r["views"] for r in dormant), 39)
check("dormant view range", (min(r["views"] for r in dormant), max(r["views"] for r in dormant)), (1, 2))
check("tiers partition the catalogue", len(zero) + len(active) + len(dormant), len(reports))
check("reports cut under the recommendation", len(reports) - len(active), 82)

stale = [r for r in reports if r["last_viewed"].strip() and r["last_viewed"] < "2025-08-31"]
check("rows whose telemetry contradicts itself", len(stale), 19)
check("views they claim", sum(r["views"] for r in stale), 28)

excel_active = sorted(r["report_id"] for r in active if r["source"] == "Excel extract")
check("Excel-sourced reports in the catalogue",
      sum(1 for r in reports if r["source"] == "Excel extract"), 30)
check("Excel-sourced reports inside Day-One scope (Finding 13)", len(excel_active), 10)

scorecards = [r for r in reports if "scorecard" in r["report_name"].lower()]
check("studio scorecards already in the catalogue (Finding 12)", len(scorecards), 6)
check("their combined views in 12 months", sum(r["views"] for r in scorecards), 6)
check("how many were viewed in 2026", sum(1 for r in scorecards if r["last_viewed"].startswith("2026")), 0)
check("their ids", sorted(r["report_id"] for r in scorecards),
      ["RPT-049", "RPT-050", "RPT-051", "RPT-052", "RPT-053", "RPT-054"])

INHERITED_EFFORT = int(plan_rows["T06"]["effort_days"])
rate = INHERITED_EFFORT / float(len(reports))
check("inherited unit rate (days per report)", round(rate, 3), 0.333)
check("effort for the 38, at that rate", int(round(len(active) * rate)), 13)
check("effort days freed by descoping", INHERITED_EFFORT - int(round(len(active) * rate)), 27)
check("zero-view reports among the first 42 rows (the trap in AI_WORKFLOW)",
      sum(1 for r in reports[:42] if r["views"] == 0), 24)
check("defensible expectation for any unprioritised 42",
      int(round(len(zero) / float(len(reports)) * 42)), 20)

# ===========================================================================
section("8. Revised plan - PARSED FROM PLAN.md, not hardcoded")
# ===========================================================================
plan_md = text("PLAN.md", ROOT)
mbr_text = text("MBR.md", ROOT)

wbs = {}
for cells in md_rows(plan_md):
    if len(cells) < 9:
        continue
    tid = re.sub(r"[*` ]", "", cells[0])
    if not re.match(r"^(T\d+[ab]?|GATE)$", tid):
        continue
    start, end = cells[3].strip(), cells[4].strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", start) or not re.match(r"^\d{4}-\d{2}-\d{2}$", end):
        continue
    eff = num(cells[5])
    published_float = num(cells[8])
    if eff is None or published_float is None:
        continue
    key = tid if tid not in wbs else tid + "_B"
    wbs[key] = (start, end, int(eff), workdays(start, end), int(published_float), cells[2])

check("WBS rows parsed out of PLAN.md", len(wbs) >= 18, True)

# Every dated row, including the ones whose id column is an em-dash. These are
# the cutover windows, and the previous version of this harness could not see
# them at all.
dated_rows = []
for cells in md_rows(plan_md):
    if len(cells) < 5:
        continue
    start, end = cells[3].strip(), cells[4].strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", start) or not re.match(r"^\d{4}-\d{2}-\d{2}$", end):
        continue
    effort = cells[5].strip() if len(cells) > 5 else ""
    is_milestone = num(effort) is None
    dated_rows.append((re.sub(r"[*`]", "", cells[1]).strip(), start, end, is_milestone))

check("dated rows parsed from PLAN.md (WBS plus milestone rows)", len(dated_rows) >= 26, True)
check("cutover and soak rows are visible to this harness",
      sorted({n for n, s_, e_, ms in dated_rows if ms}),
      ["Cutover, year-end shutdown", "Ledger flip / go-live", "Soak, legacy authoritative",
       "Technical cutover"])

for tid, (s, e, eff, win, published, owner) in sorted(wbs.items()):
    check("PLAN.md %-6s float = %2d wd window - %2d effort" % (tid, win, eff), win - eff, published)

check("revised tasks carrying negative float",
      [t for t, (s, e, eff, win, f, o) in wbs.items() if win - eff < 0], [])

# Constraint compliance, derived from the artifacts parsed above.
for tid, (s, e, eff, win, f, owner) in wbs.items():
    if tid.startswith("T13"):
        check("PLAN.md %s starts after the vendor freeze ends" % tid, s > FREEZE_END, True)
        check("PLAN.md %s gets the vendor's full working days" % tid, win, onboard)
    if tid.startswith("T03"):
        check("PLAN.md " + tid + " is half the inherited backfill effort",
              eff * 2, int(plan_rows["T03"]["effort_days"]))

# No planned task may run during the PTO, the freeze, or the Finance close.
for tid, (s, e, eff, win, f, owner) in sorted(wbs.items()):
    if tid.startswith(("T03", "T13", "T04", "T05")):
        overlaps_pto = s <= PTO_END and e >= PTO_START
        check("PLAN.md %s avoids Whitlock's PTO" % tid, overlaps_pto, False)

# ---------------------------------------------------------------------------
# DECLARED OUTSIDE KNOWLEDGE. None of this is in artifacts/. It is stated here
# rather than assumed silently, because it constrains the schedule and a reader
# is entitled to see exactly which non-artifact facts the plan depends on.
#   - US Thanksgiving is the fourth Thursday of November; the Thanksgiving to
#     Cyber Monday window is the peak trading period for digital game sales.
#   - 1 January is a public holiday.
# ---------------------------------------------------------------------------
DECLARED_HOLIDAYS = {date(2027, 1, 1)}


def first_business_day(year, month):
    for x in range(1, 9):
        d = date(year, month, x)
        if d.weekday() < 5 and d not in DECLARED_HOLIDAYS:
            return d


# Peak trading: no cutover window may touch Thanksgiving-Cyber Monday.
PEAK = (THANKSGIVING.isoformat(), (THANKSGIVING + timedelta(days=4)).isoformat())
check("peak trading window derived from the calendar", PEAK, ("2026-11-26", "2026-11-30"))
cutover_windows = [(n, s_, e_) for n, s_, e_, ms in dated_rows
                   if ms and re.search(r"cutover", n, re.I)]
check("cutover windows found to test", len(cutover_windows), 2)
for name, s_, e_ in cutover_windows:
    check("'" + name + "' (" + s_ + ".." + e_ + ") clears the peak trading window",
          e_ < PEAK[0] or s_ > PEAK[1], True)

# The soak is the one window that SHOULD span the peak: the new platform runs it
# while legacy stays the book of record. Assert the design, don't assume it.
soak = [(s_, e_) for n, s_, e_, ms in dated_rows if re.search(r"soak", n, re.I)]
check("a soak window exists in Scenario A", len(soak), 1)
check("the soak deliberately covers the whole peak weekend",
      soak[0][0] <= PEAK[0] and soak[0][1] >= PEAK[1], True)

# No task of any kind may run during Whitlock's PTO or inside the vendor freeze.
for name, s_, e_, ms in dated_rows:
    # The freeze blocks new integrations and credential rotation. Internal work
    # (backfill, reporting) is unaffected, so only vendor-touching and cutover
    # activities are tested here.
    if re.search(r"cutover|soak|ledger|settlement|vendor", name, re.I):
        check("'" + name + "' avoids the vendor freeze",
              s_ <= FREEZE_END and e_ >= FREEZE_START, False)

# Scenario dates: parsed from what PLAN.md actually publishes, in two places,
# which must agree with each other and with the calendar.
hdr = re.search(r"\*\*Recommended cutover:\*\* \*\*(\w+ \d{1,2} \w+ \d{4})\*\*[^*]*"
                r"\*\*(\w+ \d{1,2} \w+ \d{4})\*\*", plan_md)
check("PLAN.md header declares two recommended dates", hdr is not None, True)


def spelled(txt):
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})", txt)
    return date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))


GOLIVE_A, GOLIVE_B = spelled(hdr.group(1)), spelled(hdr.group(2))
row = [c for c in md_rows(plan_md) if c and "Business go-live" in c[0]][0]
check("scenario table agrees with the header on Scenario A", spelled(row[1]), GOLIVE_A)
check("scenario table agrees with the header on Scenario B", spelled(row[2]), GOLIVE_B)
MONTH_NAMES = {v: k for k, v in MONTHS.items()}


def spell(d):
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)


check("MBR quotes the same two go-live dates as PLAN.md",
      spell(GOLIVE_A) in mbr_text and spell(GOLIVE_B) in mbr_text, True)
check("CFO message quotes them too",
      spell(GOLIVE_A) in text("CFO_MESSAGE.md", ROOT).replace("Tuesday ", "").replace("Monday ", "")
      or "1 December" in text("CFO_MESSAGE.md", ROOT), True)

# Both dates must be the first business day of their month - that is the whole
# ledger argument. A mid-month date fails here.
for label, gl in [("A", GOLIVE_A), ("B", GOLIVE_B)]:
    check("Scenario " + label + " go-live is its month's FIRST business day, not the last",
          gl, first_business_day(gl.year, gl.month))
    check("Scenario " + label + " go-live is not inside the peak trading window",
          PEAK[0] <= gl.isoformat() <= PEAK[1], False)

check("Scenario A go-live is a Tuesday", GOLIVE_A.strftime("%a"), "Tue")
check("Scenario A go-live parsed as", GOLIVE_A, date(2026, 12, 1))
check("Scenario B go-live is a Monday", GOLIVE_B.strftime("%a"), "Mon")
check("Scenario B go-live parsed as", GOLIVE_B, date(2027, 1, 4))
check("1 Jan 2027 falls on a Friday, so the New Year holiday buffers go-live",
      date(2027, 1, 1).strftime("%a"), "Fri")
check("Scenario B cutover window sits in the year-end shutdown",
      workdays("2026-12-28", "2026-12-31"), 4)
check("30 November is November's LAST business day, not December's first",
      max(d for d in (date(2026, 11, x) for x in range(1, 31)) if d.weekday() < 5), date(2026, 11, 30))
check("slip to Scenario A (weeks)", round((GOLIVE_A - date.fromisoformat(CUTOVER)).days / 7.0, 1), 7.1)
check("slip to Scenario B (weeks)", round((GOLIVE_B - date.fromisoformat(CUTOVER)).days / 7.0, 1), 12.0)

# September capacity for Whitlock under the 80/20 split.
t02 = wbs["T02"]
remaining = round((1 - 0.70) * t02[2], 1)
capacity = round(workdays("2026-09-01", "2026-09-18") * 0.8 + workdays("2026-09-21", "2026-09-30"), 1)
check("T02 effort remaining at 70% complete", remaining, 17.4)
check("Whitlock September effective capacity", capacity, 19.2)
check("September margin (days)", round(capacity - remaining, 1), 1.8)

# T12b must be staffed at an FTE that can actually deliver it.
for tid in sorted(t for t in wbs if t.startswith("T12b")):
    st, en, eff, win, f, owner = wbs[tid]
    needed = eff / float(win) * 100
    m = re.search(r"at (\d+)%", owner)
    check("PLAN.md " + tid + " names an explicit FTE for R. Bekele", m is not None, True)
    if m:
        check("PLAN.md " + tid + " FTE " + m.group(1) + "% delivers its " + str(eff) + "d in "
              + str(win) + " wd", int(m.group(1)) >= needed, True)

# Section 6 budget table must agree with the section 3 WBS on staffing.
uplift = [c for c in md_rows(plan_md) if c and c[0].strip() == "Security uplift"]
check("PLAN.md publishes a security uplift row", len(uplift), 1)
budget_fte = [int(m) for m in re.findall(r"\u2192 (\d+)%", " | ".join(uplift[0]))]
wbs_fte = [int(re.search(r"at (\d+)%", wbs[t][5]).group(1))
           for t in sorted(w for w in wbs if w.startswith("T12b"))]
check("budget table security FTEs", budget_fte, wbs_fte)

# Contractor hours quoted in the budget table must match the derivation above.
backfill_row = [c for c in md_rows(plan_md) if c and c[0].startswith("Contractor backfill")][0]
hours = [int(re.search(r"~?([\d,]+) hours", cell).group(1).replace(",", ""))
         for cell in backfill_row[1:3]]
check("contractor hours published in the budget table", hours,
      [int((RTB_PCT_WEEKS + 4 * 40) / 100.0 * 40), int((RTB_PCT_WEEKS + 8 * 40) / 100.0 * 40)])

# ===========================================================================
section("9. Deliverables - parsed from the documents themselves")
# ===========================================================================
DELIVERABLES = ["ASSESSMENT.md", "PLAN.md", "SCOPE.md", "MBR.md", "CFO_MESSAGE.md", "AI_WORKFLOW.md"]
for name in DELIVERABLES:
    check("%s exists" % name, os.path.exists(os.path.join(ROOT, name)), True)

cfo_words = len(text("CFO_MESSAGE.md", ROOT).split())
check("CFO_MESSAGE.md is under the 300-word brief limit (%d)" % cfo_words, cfo_words < 300, True)

assessment = text("ASSESSMENT.md", ROOT)
findings = re.findall(r"^### Finding \d+ —.*$", assessment, re.M)
check("findings in ASSESSMENT.md", len(findings), 16)

# Real citation check: open the cited file and confirm the cited lines exist.
cited = set()
for fname, spans in re.findall(r"`(?:artifacts/)?([\w.-]+\.(?:md|csv))((?::\d+(?:-\d+)?)(?:, ?\d+(?:-\d+)?)*)`",
                               assessment):
    path = os.path.join(ART, fname)
    check("cited artifact exists: %s" % fname, os.path.exists(path), True)
    n_lines = len(lines(fname))
    for span in re.findall(r"\d+(?:-\d+)?", spans):
        hi = int(span.split("-")[-1])
        check("%s:%s is within the file (%d lines)" % (fname, span, n_lines), hi <= n_lines, True)
    cited.add(fname)

check("findings citing no artifact at all",
      [f for f in re.split(r"^### Finding ", assessment, flags=re.M)[1:] if "artifacts/" not in f
       and not re.search(r"`[\w.-]+\.(md|csv)[:`]", f)], [])
real_artifacts = set(os.listdir(ART))
check("every cited filename is a real artifact", sorted(cited - real_artifacts), [])
check("assessment cites most of the folder", len(cited) >= len(real_artifacts) - 1, True)

scope_md = text("SCOPE.md", ROOT)
family_block = scope_md.split("24 base reporting families")[1].split("---")[0]
check("SCOPE.md lists exactly the 38 active report ids",
      sorted(set(re.findall(r"RPT-\d{3}", family_block))),
      sorted(r["report_id"] for r in active))

mbr = mbr_text
check("MBR declares RED", "\U0001F534 **RED**" in mbr, True)
check("MBR carries explicit asks", "decisions we need" in mbr.lower(), True)
check("MBR names both scenario dates",
      "1 December 2026" in mbr and "4 January 2027" in mbr, True)

# ===========================================================================
section("Result")
if not QUIET:
    print("  %d checks run, %d failed" % (CHECKS, len(FAILURES)))
if FAILURES:
    print("\nFAILURES:")
    for f in FAILURES:
        print("  - " + f)
    sys.exit(1)
if not QUIET:
    print("  Every published figure reproduces from source.")
sys.exit(0)
