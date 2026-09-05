#!/usr/bin/env python3
"""
Mythril Programme assessment - reproducibility harness.

Design rule: this script derives its expectations by PARSING the artifacts and the
deliverables. It does not hardcode figures that merely restate what the documents
say. If an artifact changes, or a date in PLAN.md is edited, checks here fail.

An earlier version of this file failed that rule: it hardcoded the reconciliation
figures without opening the file, hardcoded the revised schedule without reading
PLAN.md, and contained assertions that could not fail (`check(x, True, True)`,
`pct(x, x)`, string comparisons between literals). Five of the eight artifacts were
never read. That version passed 109 checks and proved almost nothing. See
AI_WORKFLOW.md section 3.

Run from the repository root:

    python verify.py            # verify
    python verify.py --selftest # prove the harness can fail (mutation test)

Exit 0 = every published figure reproduces from source. Non-zero = a document
states something this script cannot derive, and the document is wrong until
proven otherwise.
"""

import os
import subprocess
import sys

# Ensure modular src package is importable without requiring pre-installation
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from mythril.engine import AuditEngine  # noqa: E402  (import follows the sys.path bootstrap above)


def main() -> int:
    if "--selftest" in sys.argv:
        mutation_script = os.path.join(ROOT, "mutation_test.py")
        res = subprocess.run([sys.executable, mutation_script], cwd=ROOT)
        return res.returncode

    quiet = "--quiet" in sys.argv
    engine = AuditEngine(root_dir=ROOT, quiet=quiet)
    passed, checks, failures = engine.run_all()
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
