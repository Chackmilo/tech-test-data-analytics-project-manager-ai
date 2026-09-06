"""Mutation test: prove verify.py can actually fail.

Each case corrupts one source of truth, runs the harness, and restores the file.
A harness that passes every mutation is decorative.
"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

CASES = [
    ("PLAN.md", "| T04 | Parallel run | D. Whitlock | 2026-11-03 | 2026-11-16 |",
     "| T04 | Parallel run | D. Whitlock | 2026-11-03 | 2026-11-13 |",
     "shorten a critical-path task window in PLAN.md by 3 days"),
    (r"artifacts\reconciliation-2026-08-28.md", "| Mar 2026 | 119,882.64 | 179,607.56 | +49.82% |",
     "| Mar 2026 | 119,882.64 | 129,607.56 | +49.82% |",
     "alter the March revenue figure in the artifact"),
    (r"artifacts\vendor-notice.md", "through Monday 19 October 2026",
     "through Monday 30 October 2026",
     "extend the vendor freeze so T13 now starts inside it"),
    (r"artifacts\report-usage.csv", "RPT-049,Studio scorecard archive",
     "RPT-049,Studio dashboard archive",
     "rename a scorecard so Finding 12's count drops to 5"),
    ("PLAN.md", "R. Bekele **at 65%**", "R. Bekele **at 15%**",
     "under-staff T12b below what its effort needs"),

    # The three below came from an external adversarial audit. All three passed
    # silently against the previous harness: the cutover rows carry an em-dash
    # id and were invisible to the WBS parser, the peak-trading guard looped
    # over an empty list, and neither the go-live header nor the budget table
    # was parsed at all. They are permanent cases now.
    ("PLAN.md", "| 2026-11-20 | 2026-11-22 |", "| 2026-11-27 | 2026-11-29 |",
     "move the technical cutover ONTO the Black Friday weekend"),
    ("PLAN.md", "**Tuesday 1 December 2026**", "**Wednesday 9 December 2026**",
     "change the recommended go-live to a mid-month date that splits December"),
    ("PLAN.md", "Bekele 10% → 65% for 8 working days", "Bekele 10% → 10% for 8 working days",
     "under-staff security in the budget table while the WBS still says 65%"),
]

def run_mutation_suite() -> int:
    failed_to_catch = []
    skipped = []
    executed = 0
    for rel, old, new, description in CASES:
        path = os.path.join(ROOT, rel)
        original = io.open(path, encoding="utf-8").read()
        if old not in original:
            # Each case is pinned to an exact literal. If that literal has moved,
            # the case tests nothing. A suite that quietly shrinks while still
            # announcing success is the precise failure it exists to prevent.
            print("SKIP  (anchor no longer present) %s" % description)
            skipped.append(description)
            continue
        executed += 1
        try:
            io.open(path, "w", encoding="utf-8", newline="\n").write(original.replace(old, new, 1))
            rc = subprocess.run([sys.executable, "verify.py", "--quiet"], cwd=ROOT,
                                capture_output=True).returncode
        finally:
            io.open(path, "w", encoding="utf-8", newline="\n").write(original)
        caught = rc != 0
        print("%s  %s" % ("CAUGHT" if caught else "MISSED", description))
        if not caught:
            failed_to_catch.append(description)

    print()
    if skipped:
        print("SUITE DEGRADED - %d of %d cases never ran; their anchor text has moved."
              % (len(skipped), len(CASES)))
        for d in skipped:
            print("  - " + d)
        print("Re-pin each anchor to the current file contents, then re-run.")
        return 1
    if failed_to_catch:
        print("HARNESS IS WEAK - these mutations passed silently:")
        for d in failed_to_catch:
            print("  - " + d)
        return 1
    print("All %d of %d mutations executed and caught. The harness can fail."
          % (executed, len(CASES)))

    # Confirm the repo is back to a passing state.
    rc = subprocess.run([sys.executable, "verify.py", "--quiet"], cwd=ROOT, capture_output=True).returncode
    print("Repo restored and passing." if rc == 0 else "WARNING: repo left failing after restore!")
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(run_mutation_suite())
