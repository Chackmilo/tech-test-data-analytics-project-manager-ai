"""Unit tests for calendar and temporal scheduling logic."""

from datetime import date

from mythril.core.calendar import (
    first_business_day,
    get_peak_trading_window,
    get_thanksgiving,
    workdays,
)


def test_workdays_calculation():
    """Test business day counting excluding weekends."""
    # Oct 1 (Thu) to Oct 8 (Thu) is 6 business days
    assert workdays("2026-10-01", "2026-10-08") == 6
    # Oct 9 (Fri) to Oct 20 (Tue) is 8 business days
    assert workdays("2026-10-09", "2026-10-20") == 8


def test_first_business_day():
    """Verify first business day of the month calculation."""
    # Dec 2026: Dec 1 is Tuesday
    assert first_business_day(2026, 12) == date(2026, 12, 1)
    # Jan 2027: Jan 1 is holiday (Fri), Jan 2-3 weekend, first business day is Jan 4 (Mon)
    assert first_business_day(2027, 1) == date(2027, 1, 4)


def test_peak_trading_window():
    """Verify Black Friday through Cyber Monday peak window derivation."""
    thanksgiving = get_thanksgiving(2026)
    assert thanksgiving == date(2026, 11, 26)
    start, end = get_peak_trading_window(2026)
    assert start == "2026-11-26"
    assert end == "2026-11-30"
