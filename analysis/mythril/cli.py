"""Command-line interface for the Mythril Programme audit engine."""

import argparse
import os
import sys

from mythril.engine import AuditEngine


def run_selftest(root_dir: str) -> int:
    """Run adversarial mutation testing to prove harness catches defects."""
    # Import mutation test cases dynamically
    import subprocess

    mutation_script = os.path.join(root_dir, "analysis", "mutation_test.py")
    if not os.path.exists(mutation_script):
        print(f"Error: mutation script not found at {mutation_script}")
        return 1

    print("Running adversarial mutation test suite...")
    res = subprocess.run([sys.executable, mutation_script], cwd=root_dir)
    return res.returncode


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Mythril Programme deterministic verification and audit engine."
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-check output; only report failures and summary."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Path to repository root (defaults to the directory above analysis/)."
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="Run adversarial mutation testing to prove the harness can fail."
    )

    args = parser.parse_args()

    root = args.root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if args.selftest:
        return run_selftest(root)

    engine = AuditEngine(root_dir=root, quiet=args.quiet)
    passed, checks, failures = engine.run_all()
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
