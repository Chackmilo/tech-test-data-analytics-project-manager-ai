"""Artifact reading and CSV ingestion utilities."""

import csv
import io
import os
from pathlib import Path
from typing import Dict, List, Union


def read_text(name: str, root: Union[str, Path]) -> str:
    """Read full text of a file using utf-8 encoding."""
    path = os.path.join(root, name)
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def read_lines(name: str, root: Union[str, Path]) -> List[str]:
    """Read lines of a file as a list of strings."""
    return read_text(name, root).splitlines()


def read_csv_rows(name: str, root: Union[str, Path]) -> List[Dict[str, str]]:
    """Read a CSV file into a list of row dictionaries."""
    path = os.path.join(root, name)
    with io.open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))
