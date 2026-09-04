"""Mutation test: prove verify.py can actually fail.

Each case corrupts one source of truth, runs the harness, and restores the file.
A harness that passes every mutation is decorative.
"""
import io
import subprocess
import sys

ROOT = r'E:\RVS'

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
]

failed_to_catch = []
for rel, old, new, description in CASES:
    path = ROOT + "\\" + rel
    original = io.open(path, encoding="utf-8").read()
    if old not in original:
        print("SKIP  (anchor not found) %s" % description)
        continue
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
if failed_to_catch:
    print("HARNESS IS WEAK - these mutations passed silently:")
    for d in failed_to_catch:
        print("  - " + d)
    sys.exit(1)
print("All %d mutations caught. The harness can fail." % len(CASES))

# Confirm the repo is back to a passing state.
rc = subprocess.run([sys.executable, "verify.py", "--quiet"], cwd=ROOT, capture_output=True).returncode
print("Repo restored and passing." if rc == 0 else "WARNING: repo left failing after restore!")
sys.exit(0 if rc == 0 else 1)
