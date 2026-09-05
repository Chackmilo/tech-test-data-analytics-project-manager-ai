"""Markdown document and table parsing utilities."""

import re
from typing import Generator, List, Optional


def parse_num(cell: str) -> Optional[float]:
    """Parse a numerical value out of a markdown table cell or string, or None."""
    m = re.search(r"-?[\d,]+\.?\d*", cell.replace("**", ""))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def md_rows(body: str) -> Generator[List[str], None, None]:
    """Yield lists of stripped cells for every markdown table row in a block of text."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            yield [c.strip() for c in line.strip("|").split("|")]
