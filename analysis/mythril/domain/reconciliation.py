"""Domain logic for parallel-run financial reconciliation verification."""

import re
from typing import Any, Dict, Tuple

from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_text
from mythril.parsers.markdown import md_rows, parse_num


def verify_reconciliation(harness: VerificationHarness, art_dir: str) -> Dict[str, Any]:
    """Execute section 1 checks: Parallel-run financial reconciliation."""
    harness.section("1. Reconciliation - parsed from artifacts/reconciliation-2026-08-28.md")
    recon = read_text("reconciliation-2026-08-28.md", art_dir)

    recon_rows: Dict[str, Tuple[float, float, float]] = {}
    for cells in md_rows(recon):
        if len(cells) < 4:
            continue
        legacy, new = parse_num(cells[1]), parse_num(cells[2])
        published = parse_num(cells[3])
        if legacy is None or new is None or published is None or legacy == 0:
            continue
        label = re.sub(r"[`*]", "", cells[0]).strip()
        recon_rows[label] = (legacy, new, published)
        computed = round(100.0 * (new - legacy) / legacy, 2)
        harness.check(f"artifact arithmetic holds: {label}", computed, published)

    harness.check("rows with a published delta found in the artifact", len(recon_rows) >= 8, True)

    fy = recon_rows["Net revenue, FY2026 total"]
    mar = recon_rows["Mar 2026"]
    q2 = recon_rows["FY2026 Q2 (Jan-Mar 2026)"] if "FY2026 Q2 (Jan-Mar 2026)" in recon_rows else \
        next(v for k, v in recon_rows.items() if k.startswith("FY2026 Q2"))
    orders = recon_rows["fact_order row count"]

    fy_delta = round(fy[1] - fy[0], 2)
    mar_delta = round(mar[1] - mar[0], 2)
    row_delta = int(orders[1] - orders[0])

    harness.check("FY2026 variance in USD", fy_delta, 59724.92)
    harness.check("March 2026 variance in USD", mar_delta, 59724.92)
    harness.check("the annual variance IS the March variance", fy_delta == mar_delta, True)
    harness.check("Q2 variance is also entirely March", round(q2[1] - q2[0], 2), mar_delta)
    harness.check("phantom order count", row_delta, 2998)
    harness.check("USD per phantom order (Finding 1 inference)", round(fy_delta / row_delta, 4), 19.9216)

    clean = [k for k, (legacy, new, _pct) in recon_rows.items() if legacy == new]
    harness.check(
        "periods reconciling at exactly 0.00%",
        sorted(clean),
        sorted([
            "FY2026 Q1 (Oct–Dec 2025)", "FY2026 Q3 (Apr–Jun 2026)", "Jan 2026",
            "Feb 2026", "Distinct titles", "Distinct storefronts"
        ])
    )

    tol = parse_num(re.search(r"Tolerance agreed at programme kick-off: ±(\d+)%", recon).group(0))
    harness.check("kick-off tolerance from the artifact (%)", tol, 5.0)
    harness.check("annual delta passes that tolerance", abs(fy[2]) < tol, True)
    harness.check("March delta fails that tolerance by a factor of", round(abs(mar[2]) / tol, 1), 10.0)

    return {
        "recon_rows": recon_rows,
        "fy_delta": fy_delta,
        "mar_delta": mar_delta,
        "row_delta": row_delta,
    }
