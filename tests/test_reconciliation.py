"""Unit tests for financial reconciliation domain logic."""

from pathlib import Path

from mythril.core.harness import VerificationHarness
from mythril.domain.reconciliation import verify_reconciliation


def test_reconciliation_math(artifacts_dir: Path):
    """Verify that financial variance calculations and order count anomalies match."""
    harness = VerificationHarness(quiet=True)
    res = verify_reconciliation(harness, str(artifacts_dir))

    assert harness.passed
    assert res["fy_delta"] == 59724.92
    assert res["mar_delta"] == 59724.92
    assert res["row_delta"] == 2998
