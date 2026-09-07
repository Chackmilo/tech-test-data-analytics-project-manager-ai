"""Unit tests for report telemetry domain logic."""

from pathlib import Path

from mythril.core.harness import VerificationHarness
from mythril.domain.telemetry import verify_telemetry


def test_telemetry_triage(artifacts_dir: Path):
    """Verify Pareto 80/20 report triage and view sums."""
    harness = VerificationHarness(quiet=True)
    # Plan rows mock for T06 effort
    plan_rows = {"T06": {"effort_days": "40"}}
    res = verify_telemetry(harness, str(artifacts_dir), plan_rows)

    assert harness.passed
    assert len(res["reports"]) == 120
    assert len(res["active"]) == 38
    assert len(res["zero"]) == 56
    assert len(res["dormant"]) == 26
    assert res["total_views"] == 2309
