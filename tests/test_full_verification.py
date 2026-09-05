"""End-to-end test certifying all 276 verification checks pass."""

from mythril.engine import AuditEngine


def test_full_verification_suite(audit_engine: AuditEngine):
    """Assert that the complete audit pipeline succeeds with zero failures."""
    passed, checks, failures = audit_engine.run_all()
    assert passed, f"Verification failed with {failures} defects: {audit_engine.harness.failures}"
    assert checks == 276, f"Expected 276 checks, ran {checks}"
    assert failures == 0, f"Expected 0 failures, got {failures}"
