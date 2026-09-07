"""Executable module entrypoint: python -m mythril."""

import sys

from mythril.cli import main

if __name__ == "__main__":
    sys.exit(main())
