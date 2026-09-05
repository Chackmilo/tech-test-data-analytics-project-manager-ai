"""Domain logic for personnel, PTO, and steering meeting commitments."""

import re
from typing import Any, Dict

from mythril.core.calendar import workdays
from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_text


def verify_team(harness: VerificationHarness, art_dir: str) -> Dict[str, Any]:
    """Execute section 3 checks: Team notes and steering notes analysis."""
    harness.section("3. People - parsed from artifacts/team-notes.md and steering-notes")
    team = read_text("team-notes.md", art_dir)
    pto = re.search(r"PTO approved (\d+)[–-](\d+) October", team)
    pto_start = f"2026-10-{int(pto.group(1)):02d}"
    pto_end = f"2026-10-{int(pto.group(2)):02d}"
    alvear_exit = "2026-09-30"

    harness.check("Whitlock PTO parsed from team notes", (pto_start, pto_end), ("2026-10-09", "2026-10-20"))
    harness.check("PTO length in business days", workdays(pto_start, pto_end), 8)
    harness.check("no runbook exists for the legacy loader", "No runbook exists" in team, True)
    harness.check("Whitlock is the only loader operator", "only person who can operate the legacy loader" in team, True)
    harness.check(
        "Okonkwo full-catalogue estimate (working days)",
        int(re.search(r"Estimated (\d+) working days", team).group(1)),
        40
    )
    harness.check("Alvear departure stated in team notes", "Leaving the company on 30 September" in team, True)

    steer = read_text("steering-notes-2026-08.md", art_dir)
    harness.check(
        "CFO confirms Finance must sign off before cutover",
        "needs to sign off the reconciliation before cutover" in steer,
        True
    )
    harness.check(
        "committee was told nothing threatened the date",
        "Asked whether anything threatens it. Told no." in steer,
        True
    )
    harness.check(
        "scorecard commitment was news to the programme team",
        "first the programme team has heard of that commitment" in steer,
        True
    )
    harness.check(
        "single-operator risk raised with no owner",
        "Action logged, no owner assigned" in steer,
        True
    )

    return {
        "pto_start": pto_start,
        "pto_end": pto_end,
        "alvear_exit": alvear_exit,
        "team_text": team,
        "steer_text": steer,
    }
