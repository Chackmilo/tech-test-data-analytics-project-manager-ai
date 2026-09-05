"""Pytest fixtures for Mythril Programme verification test suite."""

from pathlib import Path

import pytest

from mythril.engine import AuditEngine


@pytest.fixture(scope="session")
def root_dir() -> Path:
    """Fixture returning the root directory of the repository."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def artifacts_dir(root_dir: Path) -> Path:
    """Fixture returning the artifacts directory path."""
    return root_dir / "artifacts"


@pytest.fixture
def audit_engine(root_dir: Path) -> AuditEngine:
    """Fixture returning a fresh AuditEngine instance."""
    return AuditEngine(root_dir=str(root_dir), quiet=True)
