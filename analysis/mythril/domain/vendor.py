"""Domain logic for vendor freeze notice and storefront onboarding constraints."""

import re
from typing import Any, Dict

from mythril.core.calendar import workdays
from mythril.core.harness import VerificationHarness
from mythril.parsers.artifacts import read_text


def verify_vendor(harness: VerificationHarness, art_dir: str) -> Dict[str, Any]:
    """Execute section 2 checks: Vendor freeze notice analysis."""
    harness.section("2. Vendor freeze - parsed from artifacts/vendor-notice.md")
    vendor = read_text("vendor-notice.md", art_dir)
    freeze = re.search(r"from Monday (\d+) October 2026 through Monday (\d+) October 2026", vendor)
    freeze_start = f"2026-10-{int(freeze.group(1)):02d}"
    freeze_end = f"2026-10-{int(freeze.group(2)):02d}"
    onboard = int(re.search(r"\*\*(\d+) working days\*\*", vendor).group(1))

    harness.check("freeze start parsed from the notice", freeze_start, "2026-10-05")
    harness.check("freeze end parsed from the notice", freeze_end, "2026-10-19")
    harness.check("freeze length in business days", workdays(freeze_start, freeze_end), 11)
    harness.check("vendor onboarding requirement (working days)", onboard, 9)
    harness.check("notice states no exceptions are possible", "unable to make exceptions" in vendor, True)

    return {
        "freeze_start": freeze_start,
        "freeze_end": freeze_end,
        "onboard": onboard,
        "vendor_text": vendor,
    }
