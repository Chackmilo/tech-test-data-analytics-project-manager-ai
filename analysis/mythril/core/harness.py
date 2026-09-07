"""Deterministic verification harness and check registry."""

from typing import Any, List


class VerificationHarness:
    """Manages evaluation checks and generates execution reports."""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.checks: int = 0
        self.failures: List[str] = []

    def check(self, label: str, actual: Any, expected: Any) -> bool:
        """Evaluate an assertion between derived actual value and expected published value."""
        self.checks += 1
        ok = actual == expected
        if not ok:
            self.failures.append(
                f"{label}\n      computed: {actual!r}\n      published: {expected!r}"
            )
        if not self.quiet:
            rep = repr(actual)
            shown = actual if len(rep) < 48 else rep[:45] + "..."
            status = "PASS" if ok else "FAIL"
            print(f"  {status} {label:<64} {shown}")
        return ok

    def section(self, title: str) -> None:
        """Print a formatted section banner."""
        if not self.quiet:
            print(f"\n{title}\n" + "-" * len(title))

    @property
    def passed(self) -> bool:
        return len(self.failures) == 0

    def print_result(self) -> None:
        """Print overall audit summary."""
        self.section("Result")
        if not self.quiet:
            print(f"  {self.checks} checks run, {len(self.failures)} failed")
        if self.failures:
            print("\nFAILURES:")
            for f in self.failures:
                print(f"  - {f}")
        elif not self.quiet:
            print("  Every published figure reproduces from source.")
