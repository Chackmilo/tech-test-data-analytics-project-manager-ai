"""End-to-end test certifying all 281 verification checks pass."""

from mythril.engine import AuditEngine


def test_full_verification_suite(audit_engine: AuditEngine):
    """Assert that the complete audit pipeline succeeds with zero failures."""
    passed, checks, failures = audit_engine.run_all()
    assert passed, f"Verification failed with {failures} defects: {audit_engine.harness.failures}"
    assert checks == 281, f"Expected 281 checks, ran {checks}"
    assert failures == 0, f"Expected 0 failures, got {failures}"
