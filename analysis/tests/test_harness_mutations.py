"""Adversarial mutation testing with pytest to certify the harness can fail."""

from pathlib import Path

import pytest

from mutation_test import CASES
from mythril.engine import AuditEngine


@pytest.mark.parametrize("rel_path,old_text,new_text,description", CASES)
def test_mutation_is_caught(
    root_dir: Path,
    rel_path: str,
    old_text: str,
    new_text: str,
    description: str
):
    """Corrupt one source of truth, run AuditEngine, and verify the mutation is caught."""
    target_file = root_dir / rel_path
    original_content = target_file.read_text(encoding="utf-8")

    assert old_text in original_content, f"Anchor text not found for mutation: {description}"

    mutated_content = original_content.replace(old_text, new_text, 1)
    try:
        target_file.write_text(mutated_content, encoding="utf-8", newline="\n")
        engine = AuditEngine(root_dir=str(root_dir), quiet=True)
        passed, checks, failures = engine.run_all()
        assert not passed, f"Mutation was MISSED: {description}"
        assert failures > 0, f"Expected failures > 0 for {description}"
    finally:
        target_file.write_text(original_content, encoding="utf-8", newline="\n")
