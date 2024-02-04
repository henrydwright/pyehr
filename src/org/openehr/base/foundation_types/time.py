from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta, time, timezone

from org.openehr.base.foundation_types import AnyClass

import numpy as np

# Mapping of openEHR types to Python
# ==================================
# for iso8601_date use datetime.date
# for iso8601_time use datetime.time
# for iso8601_timezone use datetime.timezone
# for iso8601_duration use duration class below
# for iso8601_date_time use datetime.datetime

class TimeDefinitions:
    """Definitions for date/time classes. Note that the timezone limits are 
    set by where the international dateline is. Thus, time in New Zealand is quoted using +12:00, not -12:00."""

    SECONDS_IN_MINUTE : np.int32 = np.int32(60)
    """Number of seconds in a minute."""
    MINUTES_IN_HOUR : np.int32 = np.int32(60)
    """Number of minutes in an hour."""
    HOURS_IN_DAY : np.int32 = np.int32(24)
    """Number of clock hours in a day, i.e. 24."""
    AVERAGE_DAYS_IN_MONTH : np.float32 = np.float32(30.42)
    """Used for conversions of durations containing months to days and / or seconds."""
    MAX_DAYS_IN_MONTH : np.int32 = np.int32(31)
    """Maximum number of days in any month."""
    DAYS_IN_YEAR : np.int32 = np.int32(365)
    """Calendar days in a normal year, i.e. 365."""
    AVERAGE_DAYS_IN_YEAR : np.float32 = np.float32(365.24)
    """Used for conversions of durations containing years to days and / or seconds."""
    DAYS_IN_LEAP_YEAR : np.int32 = np.int32(366)
    """Calendar days in a standard leap year, i.e. 366."""
    MAX_DAYS_IN_YEAR : np.int32 = DAYS_IN_LEAP_YEAR
    """Maximum number of days in a year, i.e. accounting for leap years."""
    DAYS_IN_WEEK : np.int32 = np.int32(7)
    """Number of days in a week."""
    MONTHS_IN_YEAR : np.int32 = np.int32(12)
    """Number of months in a year."""
    MIN_TIMEZONE_HOUR : np.int32 = np.int32(12)
    """Minimum hour value of a timezone according to ISO 8601 
    (note that the -ve sign is supplied in the `ISO8601_TIMEZONE` class)."""
    MAX_TIMEZONE_HOUR : np.int32 = np.int32(14)
    """Maximum hour value of a timezone according to ISO 8601."""
    NOMINAL_DAYS_IN_MONTH : np.float32 = np.float32(30.42)
    """Used for conversions of durations containing months to days and / or seconds."""
    NOMINAL_DAYS_IN_YEAR : np.float32 = np.float32(365.24)
    """Used for conversions of durations containing years to days and / or seconds."""

    def valid_year(y : np.int32) -> bool:
        """True if y >= 0."""
        return (y >= np.int32(0))

    def valid_month(m : np.int32) -> bool:
        """True if m >= 1 and m <= months_in_year."""
        return (m >= np.int32(1) and m <= TimeDefinitions.MONTHS_IN_YEAR)

    def _is_leap_year(y: np.int32) -> bool:
        """True if the given year is a leap year."""
        return ((y % 4 == 0) and (y % 100 > 0)) or ((y % 100 == 0) and (y % 400 == 0))

    def valid_day(y : np.int32, m: np.int32, d: np.int32) -> bool:
        """True if d >= 1 and d <= days_in_month (m, y)."""
        if not (TimeDefinitions.valid_year(y) and TimeDefinitions.valid_month(m)):
            return False
        
        days_in_month = 31 - ((m - 1) % 7 % 2) if m != 2 else 28 + (1 if TimeDefinitions._is_leap_year(y) else 0)

        return d >= 1 and d <= days_in_month

    def valid_hour(h: np.int32, m : np.int32, s: np.int32) -> bool:
        """True if (h >= 0 and h < Hours_in_day) or (h = Hours_in_day and m = 0 and s = 0)."""
        if not (TimeDefinitions.valid_minute(m) and TimeDefinitions.valid_second(s)):
            return False
        return (h >= 0 and h < TimeDefinitions.HOURS_IN_DAY) or (h == TimeDefinitions.HOURS_IN_DAY and m == 0 and s == 0)

    def valid_minute(m : np.int32) -> bool:
        """True if m >= 0 and m < Minutes_in_hour."""
        return m >= 0 and m < TimeDefinitions.MINUTES_IN_HOUR

    def valid_second(s: np.int32) -> bool:
        """True if s >= 0 and s < Seconds_in_minute"""
        return s >= 0 and s < TimeDefinitions.SECONDS_IN_MINUTE

    def valid_fractional_second(fs: np.float64) -> bool:
        """True if fs >= 0.0 and fs < 1.0 ."""
        return fs >= 0.0 and fs < 1.0

    def valid_iso8601_date(s : str) -> bool:
        try:
            d = date.fromisoformat(s)
            return True
        except ValueError:
            return False
        
    def valid_iso8601_time(s : str) -> bool:
        try:
            t = time.fromisoformat(s)
            return True
        except ValueError:
            return False

    def valid_iso8601_date_time(s : str) -> bool:
        try:
            dt = datetime.fromisoformat(s)
            return True
        except ValueError:
            return False

    def valid_iso8601_duration(s : str) -> bool:
        pass

class Duration:
    def from_openehr_adjusted_isoformat(s : str) -> timedelta:
        pass

