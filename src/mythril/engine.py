"""Audit engine orchestrating all 9 verification sections across the Mythril Programme."""

import os
from typing import Optional, Tuple

from mythril.core.harness import VerificationHarness
from mythril.domain.deliverables import verify_deliverables
from mythril.domain.inherited_plan import verify_inherited_plan
from mythril.domain.reconciliation import verify_reconciliation
from mythril.domain.resources import verify_resources
from mythril.domain.revised_plan import verify_revised_plan
from mythril.domain.status_report import verify_status_report
from mythril.domain.team import verify_team
from mythril.domain.telemetry import verify_telemetry
from mythril.domain.vendor import verify_vendor


class AuditEngine:
    """Orchestrates all domain audits and verifies reproducibility."""

    def __init__(self, root_dir: Optional[str] = None, quiet: bool = False):
        self.root_dir = root_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.art_dir = os.path.join(self.root_dir, "artifacts")
        self.quiet = quiet
        self.harness = VerificationHarness(quiet=quiet)

    def run_all(self) -> Tuple[bool, int, int]:
        """Execute full 9-section verification harness. Returns (passed, checks_count, failures_count)."""
        # 1. Reconciliation
        verify_reconciliation(self.harness, self.art_dir)

        # 2. Vendor freeze
        v_out = verify_vendor(self.harness, self.art_dir)

        # 3. People
        t_out = verify_team(self.harness, self.art_dir)

        # 4. Status report
        sr_out = verify_status_report(self.harness, self.art_dir)

        # 5. Inherited plan
        verify_inherited_plan(
            self.harness,
            plan_rows=sr_out["plan_rows"],
            freeze_start=v_out["freeze_start"],
            freeze_end=v_out["freeze_end"],
            onboard=v_out["onboard"],
            pto_start=t_out["pto_start"],
            pto_end=t_out["pto_end"],
        )

        # 6. Resource allocation
        res_out = verify_resources(
            self.harness,
            self.art_dir,
            plan_rows=sr_out["plan_rows"],
            alvear_exit=t_out["alvear_exit"],
        )

        # 7. Report telemetry
        tel_out = verify_telemetry(
            self.harness,
            self.art_dir,
            plan_rows=sr_out["plan_rows"],
        )

        # 8. Revised plan
        rp_out = verify_revised_plan(
            self.harness,
            self.root_dir,
            freeze_start=v_out["freeze_start"],
            freeze_end=v_out["freeze_end"],
            onboard=v_out["onboard"],
            pto_start=t_out["pto_start"],
            pto_end=t_out["pto_end"],
            plan_rows=sr_out["plan_rows"],
            rtb_pct_weeks=res_out["rtb_pct_weeks"],
            cutover=sr_out["cutover"],
        )

        # 9. Deliverables
        verify_deliverables(
            self.harness,
            self.root_dir,
            self.art_dir,
            active_reports=tel_out["active"],
            mbr_text=rp_out["mbr_text"],
        )

        self.harness.print_result()
        return self.harness.passed, self.harness.checks, len(self.harness.failures)
