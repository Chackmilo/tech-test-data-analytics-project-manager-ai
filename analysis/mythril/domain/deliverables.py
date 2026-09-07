"""Domain logic for cross-checking deliverables, citations, word count limits, and executive alignment."""

import os
import re
from typing import Any, Dict, List, Set

from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_lines, read_text

DELIVERABLES = [
    "ASSESSMENT.md",
    "PLAN.md",
    "SCOPE.md",
    "MBR.md",
    "CFO_MESSAGE.md",
    "AI_WORKFLOW.md",
]


def verify_deliverables(
    harness: VerificationHarness,
    root_dir: str,
    art_dir: str,
    active_reports: List[Dict[str, Any]],
    mbr_text: str,
) -> Dict[str, Any]:
    """Execute section 9 checks: Assessment deliverables and citation verification."""
    harness.section("9. Deliverables - parsed from the documents themselves")

    for name in DELIVERABLES:
        harness.check(f"{name} exists", os.path.exists(os.path.join(root_dir, name)), True)

    # The brief requires the deliverables at the repository root. Anything else
    # sitting there competes with them for a reviewer's attention, so the root
    # markdown set is asserted to be exactly the brief plus the six documents.
    # Supporting prose and the harness itself live in analysis/.
    root_md = sorted(f for f in os.listdir(root_dir) if f.endswith(".md"))
    harness.check(
        "root holds only the brief and the six deliverables",
        root_md,
        sorted(["README.md"] + list(DELIVERABLES)),
    )
    harness.check(
        "README.md is present and is the brief, not a deliverable",
        "README.md" in root_md and "README.md" not in DELIVERABLES,
        True,
    )

    cfo_words = len(read_text("CFO_MESSAGE.md", root_dir).split())
    harness.check(f"CFO_MESSAGE.md is under the 300-word brief limit ({cfo_words})", cfo_words < 300, True)

    assessment = read_text("ASSESSMENT.md", root_dir)
    findings = re.findall(r"^### Finding \d+ —.*$", assessment, re.M)
    harness.check("findings in ASSESSMENT.md", len(findings), 16)

    cited: Set[str] = set()
    citation_matches = re.findall(
        r"`(?:artifacts/)?([\w.-]+\.(?:md|csv))((?::\d+(?:-\d+)?)(?:, ?\d+(?:-\d+)?)*)`",
        assessment
    )
    for fname, spans in citation_matches:
        path = os.path.join(art_dir, fname)
        exists = os.path.exists(path)
        harness.check(f"cited artifact exists: {fname}", exists, True)
        if not exists:
            continue
        file_lines = read_lines(fname, art_dir)
        n_lines = len(file_lines)
        for span in re.findall(r"\d+(?:-\d+)?", spans):
            hi = int(span.split("-")[-1])
            harness.check(f"{fname}:{span} is within the file ({n_lines} lines)", hi <= n_lines, True)
        cited.add(fname)

    unreferenced_findings = [
        f for f in re.split(r"^### Finding ", assessment, flags=re.M)[1:]
        if "artifacts/" not in f and not re.search(r"`[\w.-]+\.(md|csv)[:`]", f)
    ]
    harness.check("findings citing no artifact at all", unreferenced_findings, [])

    real_artifacts = set(os.listdir(art_dir))
    harness.check("every cited filename is a real artifact", sorted(cited - real_artifacts), [])
    harness.check("assessment cites most of the folder", len(cited) >= len(real_artifacts) - 1, True)

    scope_md = read_text("SCOPE.md", root_dir)
    family_block = scope_md.split("24 base reporting families")[1].split("---")[0]
    harness.check(
        "SCOPE.md lists exactly the 38 active report ids",
        sorted(set(re.findall(r"RPT-\d{3}", family_block))),
        sorted(r["report_id"] for r in active_reports)
    )

    harness.check("MBR declares RED", "\U0001F534 **RED**" in mbr_text, True)
    harness.check("MBR carries explicit asks", "decisions we need" in mbr_text.lower(), True)
    harness.check(
        "MBR names both scenario dates",
        "1 December 2026" in mbr_text and "4 January 2027" in mbr_text,
        True
    )

    return {
        "findings": findings,
        "cfo_words": cfo_words,
        "cited_artifacts": cited,
    }
