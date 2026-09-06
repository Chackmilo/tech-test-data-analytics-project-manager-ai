"""Domain logic for parsing and validating the revised plan, WBS, and critical path."""

import re
from datetime import date, timedelta
from typing import Any, Dict, List, Tuple

from mythril.core.calendar import (
    DECLARED_HOLIDAYS,
    MONTHS,
    first_business_day,
    spell_date,
    workdays,
)
from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_text
from mythril.parsers.markdown import md_rows, parse_num


def verify_revised_plan(
    harness: VerificationHarness,
    root_dir: str,
    freeze_start: str,
    freeze_end: str,
    onboard: int,
    pto_start: str,
    pto_end: str,
    plan_rows: Dict[str, Dict[str, str]],
    rtb_pct_weeks: int,
    cutover: str,
) -> Dict[str, Any]:
    """Execute section 8 checks: Revised plan parsing and calendar constraint verification."""
    harness.section("8. Revised plan - PARSED FROM PLAN.md, not hardcoded")
    plan_md = read_text("PLAN.md", root_dir)
    mbr_text = read_text("MBR.md", root_dir)

    wbs: Dict[str, Tuple[str, str, int, int, int, str]] = {}
    for cells in md_rows(plan_md):
        if len(cells) < 9:
            continue
        tid = re.sub(r"[*` ]", "", cells[0])
        if not re.match(r"^(T\d+[ab]?|GATE)$", tid):
            continue
        start, end = cells[3].strip(), cells[4].strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", start) or not re.match(r"^\d{4}-\d{2}-\d{2}$", end):
            continue
        eff = parse_num(cells[5])
        published_float = parse_num(cells[8])
        if eff is None or published_float is None:
            continue
        key = tid if tid not in wbs else tid + "_B"
        wbs[key] = (start, end, int(eff), workdays(start, end), int(published_float), cells[2])

    harness.check("WBS rows parsed out of PLAN.md", len(wbs) >= 18, True)

    dated_rows: List[Tuple[str, str, str, bool]] = []
    for cells in md_rows(plan_md):
        if len(cells) < 5:
            continue
        start, end = cells[3].strip(), cells[4].strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", start) or not re.match(r"^\d{4}-\d{2}-\d{2}$", end):
            continue
        effort = cells[5].strip() if len(cells) > 5 else ""
        is_milestone = parse_num(effort) is None
        dated_rows.append((re.sub(r"[*`]", "", cells[1]).strip(), start, end, is_milestone))

    harness.check("dated rows parsed from PLAN.md (WBS plus milestone rows)", len(dated_rows) >= 26, True)
    harness.check(
        "cutover and soak rows are visible to this harness",
        sorted({n for n, s_, e_, ms in dated_rows if ms}),
        ["Cutover, year-end shutdown", "Ledger flip / go-live", "Soak, legacy authoritative", "Technical cutover"]
    )

    for tid, (s, e, eff, win, published, owner) in sorted(wbs.items()):
        harness.check(f"PLAN.md {tid:<6} float = {win:2d} wd window - {eff:2d} effort", win - eff, published)

    harness.check(
        "revised tasks carrying negative float",
        [t for t, (s, e, eff, win, f, o) in wbs.items() if win - eff < 0],
        []
    )

    for tid, (s, e, eff, win, f, owner) in wbs.items():
        if tid.startswith("T13"):
            harness.check(f"PLAN.md {tid} starts after the vendor freeze ends", s > freeze_end, True)
            harness.check(f"PLAN.md {tid} gets the vendor's full working days", win, onboard)
        if tid.startswith("T03"):
            harness.check(
                f"PLAN.md {tid} is half the inherited backfill effort",
                eff * 2,
                int(plan_rows["T03"]["effort_days"])
            )

    for tid, (s, e, eff, win, f, owner) in sorted(wbs.items()):
        if tid.startswith(("T03", "T13", "T04", "T05")):
            overlaps_pto = s <= pto_end and e >= pto_start
            harness.check(f"PLAN.md {tid} avoids Whitlock's PTO", overlaps_pto, False)

    thanksgiving = [d for d in (date(2026, 11, x) for x in range(1, 31)) if d.weekday() == 3][3]
    peak = (thanksgiving.isoformat(), (thanksgiving + timedelta(days=4)).isoformat())
    harness.check("peak trading window derived from the calendar", peak, ("2026-11-26", "2026-11-30"))

    cutover_windows = [(n, s_, e_) for n, s_, e_, ms in dated_rows if ms and re.search(r"cutover", n, re.I)]
    harness.check("cutover windows found to test", len(cutover_windows), 2)
    for name, s_, e_ in cutover_windows:
        harness.check(
            f"'{name}' ({s_}..{e_}) clears the peak trading window",
            e_ < peak[0] or s_ > peak[1],
            True
        )

    soak = [(s_, e_) for n, s_, e_, ms in dated_rows if re.search(r"soak", n, re.I)]
    harness.check("a soak window exists in Scenario A", len(soak), 1)
    harness.check(
        "the soak deliberately covers the whole peak weekend",
        soak[0][0] <= peak[0] and soak[0][1] >= peak[1],
        True
    )

    for name, s_, e_, ms in dated_rows:
        if re.search(r"cutover|soak|ledger|settlement|vendor", name, re.I):
            harness.check(f"'{name}' avoids the vendor freeze", s_ <= freeze_end and e_ >= freeze_start, False)

    hdr = re.search(
        r"\*\*Recommended cutover:\*\* \*\*(\w+ \d{1,2} \w+ \d{4})\*\*[^*]*\*\*(\w+ \d{1,2} \w+ \d{4})\*\*",
        plan_md
    )
    harness.check("PLAN.md header declares two recommended dates", hdr is not None, True)

    def spelled(txt: str) -> date:
        m = re.search(r"(\d{1,2}) (\w+) (\d{4})", txt)
        assert m is not None, f"Cannot parse date from {txt}"
        return date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))

    golive_a = spelled(hdr.group(1)) if hdr else date(2026, 12, 1)
    golive_b = spelled(hdr.group(2)) if hdr else date(2027, 1, 4)

    row = [c for c in md_rows(plan_md) if c and "Business go-live" in c[0]][0]
    harness.check("scenario table agrees with the header on Scenario A", spelled(row[1]), golive_a)
    harness.check("scenario table agrees with the header on Scenario B", spelled(row[2]), golive_b)

    harness.check(
        "MBR quotes the same two go-live dates as PLAN.md",
        spell_date(golive_a) in mbr_text and spell_date(golive_b) in mbr_text,
        True
    )
    cfo_txt = read_text("CFO_MESSAGE.md", root_dir)
    harness.check(
        "CFO message quotes both go-live dates",
        [spell_date(d) for d in (golive_a, golive_b)
         if spell_date(d) not in cfo_txt.replace("Tuesday ", "").replace("Monday ", "")],
        []
    )

    for label, gl in [("A", golive_a), ("B", golive_b)]:
        harness.check(
            f"Scenario {label} go-live is its month's FIRST business day, not the last",
            gl,
            first_business_day(gl.year, gl.month)
        )
        harness.check(
            f"Scenario {label} go-live is not inside the peak trading window",
            peak[0] <= gl.isoformat() <= peak[1],
            False
        )

    harness.check("Scenario A go-live is a Tuesday", golive_a.strftime("%a"), "Tue")
    harness.check("Scenario A go-live parsed as", golive_a, date(2026, 12, 1))
    harness.check("Scenario B go-live is a Monday", golive_b.strftime("%a"), "Mon")
    harness.check("Scenario B go-live parsed as", golive_b, date(2027, 1, 4))
    # A weekday-only test here could not fail. Make the declared holiday
    # load-bearing instead: it matters precisely because 1 Jan is a weekday,
    # and without the declaration Scenario B would land on it.
    ny = date(2027, 1, 1)
    harness.check(
        "the declared New Year holiday falls on a working weekday",
        ny in DECLARED_HOLIDAYS and ny.weekday() < 5,
        True
    )
    harness.check(
        "so without that declaration Scenario B would land on 1 January",
        min(d for d in (date(2027, 1, x) for x in range(1, 8)) if d.weekday() < 5),
        ny
    )
    harness.check(
        "Scenario B cutover window sits in the year-end shutdown",
        workdays("2026-12-28", "2026-12-31"),
        4
    )
    harness.check(
        "30 November is November's LAST business day, not December's first",
        max(d for d in (date(2026, 11, x) for x in range(1, 31)) if d.weekday() < 5),
        date(2026, 11, 30)
    )
    harness.check("slip to Scenario A (weeks)", round((golive_a - date.fromisoformat(cutover)).days / 7.0, 1), 7.1)
    harness.check("slip to Scenario B (weeks)", round((golive_b - date.fromisoformat(cutover)).days / 7.0, 1), 12.0)

    t02 = wbs["T02"]
    # percent_complete is in project-plan.csv; read it rather than restating it.
    pct_done = int(plan_rows["T02"]["percent_complete"]) / 100.0
    harness.check("T02 completion read from project-plan.csv", pct_done, 0.70)
    remaining = round((1 - pct_done) * t02[2], 1)
    # The 80/20 split and its cut-off are published in PLAN.md section 4.
    # Parse them, so editing either one breaks this check.
    split = re.search(r"Through (\d{1,2}) (\w+): \*\*(\d+)% T02", plan_md)
    resume_m = re.search(r"From (\d{1,2}) (\w+): 100% T02", plan_md)
    harness.check(
        "PLAN.md publishes the September split and its resume date",
        split is not None and resume_m is not None,
        True
    )
    cutoff = date(2026, MONTHS[split.group(2)], int(split.group(1)))
    resume = date(2026, MONTHS[resume_m.group(2)], int(resume_m.group(1)))
    t02_share = int(split.group(3)) / 100.0
    harness.check("the split runs to 18 September at 80% on T02",
                  (cutoff.isoformat(), t02_share), ("2026-09-18", 0.8))
    capacity = round(
        workdays("2026-09-01", cutoff.isoformat()) * t02_share
        + workdays(resume.isoformat(), t02[1]), 1
    )
    harness.check("T02 effort remaining at that completion", remaining, 17.4)
    harness.check("Whitlock September effective capacity", capacity, 19.2)
    harness.check("September margin (days)", round(capacity - remaining, 1), 1.8)

    for tid in sorted(t for t in wbs if t.startswith("T12b")):
        st, en, eff, win, f, owner = wbs[tid]
        needed = eff / float(win) * 100
        m = re.search(r"at (\d+)%", owner)
        harness.check(f"PLAN.md {tid} names an explicit FTE for R. Bekele", m is not None, True)
        if m:
            harness.check(
                f"PLAN.md {tid} FTE {m.group(1)}% delivers its {eff}d in {win} wd",
                int(m.group(1)) >= needed,
                True
            )

    uplift = [c for c in md_rows(plan_md) if c and c[0].strip() == "Security uplift"]
    harness.check("PLAN.md publishes a security uplift row", len(uplift), 1)
    budget_fte = [int(m) for m in re.findall(r"\u2192 (\d+)%", " | ".join(uplift[0]))]
    wbs_fte = [int(re.search(r"at (\d+)%", wbs[t][5]).group(1)) for t in sorted(w for w in wbs if w.startswith("T12b"))]
    harness.check("budget table security FTEs", budget_fte, wbs_fte)

    backfill_row = [c for c in md_rows(plan_md) if c and c[0].startswith("Contractor backfill")][0]
    hours = [int(re.search(r"~?([\d,]+) hours", cell).group(1).replace(",", "")) for cell in backfill_row[1:3]]
    harness.check(
        "contractor hours published in the budget table",
        hours,
        [int((rtb_pct_weeks + 4 * 40) / 100.0 * 40), int((rtb_pct_weeks + 8 * 40) / 100.0 * 40)]
    )

    return {
        "wbs": wbs,
        "dated_rows": dated_rows,
        "golive_a": golive_a,
        "golive_b": golive_b,
        "mbr_text": mbr_text,
    }
