"""Calendar and temporal constraint utilities for the Mythril Programme."""

from datetime import date, timedelta
from typing import Optional, Set, Tuple

MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

MONTH_NAMES = {v: k for k, v in MONTHS.items()}

# Declared outside knowledge: 1 January is a public holiday
DECLARED_HOLIDAYS: Set[date] = {date(2027, 1, 1)}


def to_date(val: str | date) -> date:
    """Convert an ISO string or date object to a date object."""
    if isinstance(val, date):
        return val
    return date.fromisoformat(str(val))


def workdays(start: str | date, end: str | date) -> int:
    """Count Monday-Friday business days between start and end (inclusive)."""
    a, b = to_date(start), to_date(end)
    n = 0
    while a <= b:
        if a.weekday() < 5:
            n += 1
        a += timedelta(days=1)
    return n


def first_business_day(year: int, month: int, holidays: Optional[Set[date]] = None) -> date:
    """Find the first non-weekend, non-holiday business day of the month."""
    holidays = holidays if holidays is not None else DECLARED_HOLIDAYS
    for x in range(1, 9):
        d = date(year, month, x)
        if d.weekday() < 5 and d not in holidays:
            return d
    raise ValueError(f"Could not find first business day for {year}-{month}")


def get_thanksgiving(year: int = 2026) -> date:
    """Calculate US Thanksgiving (fourth Thursday of November)."""
    thursdays = [d for d in (date(year, 11, x) for x in range(1, 31)) if d.weekday() == 3]
    return thursdays[3]


def get_peak_trading_window(year: int = 2026) -> Tuple[str, str]:
    """Calculate the Thanksgiving through Cyber Monday retail peak window (ISO strings)."""
    thanksgiving = get_thanksgiving(year)
    cyber_monday = thanksgiving + timedelta(days=4)
    return thanksgiving.isoformat(), cyber_monday.isoformat()


def spell_date(d: date) -> str:
    """Format date in UK business style: '1 December 2026'."""
    return f"{d.day} {MONTH_NAMES[d.month]} {d.year}"
