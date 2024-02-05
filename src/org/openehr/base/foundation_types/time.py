from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta, time, timezone
from typing import Union, Optional
import re

from org.openehr.base.foundation_types import AnyClass

import numpy as np

# Mapping of openEHR types to Python
# ==================================
# for iso8601_date use datetime.date
# for iso8601_time use datetime.time
# for iso8601_timezone use datetime.timezone
# for iso8601_duration use datetime.timedelta (generated using Duration below)
# for iso8601_date_time use datetime.datetime

temporal = Union[date, time, timezone, timedelta]
"""Abstract ancestor of time-related classes."""

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
    """Number of days in a week, i.e. 7."""
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
    
    ISO8601_DATE_EXTENDED_REGEX = "^(\\d{4}(-\\d\\d(-\\d\\d)?)?)$"
    ISO8601_DATE_COMPACT_REGEX = "^(\\d{4}(\\d\\d(\\d\\d)?)?)$"

    def valid_iso8601_date(s : str) -> bool:
        """String is a valid ISO 8601 date,"""
        format_ok = (re.match(TimeDefinitions.ISO8601_DATE_COMPACT_REGEX, s) is not None or
                re.match(TimeDefinitions.ISO8601_DATE_EXTENDED_REGEX, s) is not None) 
        compact = s.replace("-", "")
        parts = re.split(TimeDefinitions.ISO8601_DATE_COMPACT_REGEX, compact)
        return (format_ok and
                TimeDefinitions.valid_year(int(parts[1][0:4])) and
                ((parts[2] is None) or TimeDefinitions.valid_month(int(parts[2][0:2]))) and
                ((parts[3] is None) or TimeDefinitions.valid_day(int(parts[1][0:4]), int(parts[1][4:6]), int(parts[1][6:8])))
        )

        
    def valid_iso8601_time(s : str) -> bool:
        """String is a valid ISO 8601 time"""
        try:
            t = time.fromisoformat(s)
            return True
        except ValueError:
            return False

    def valid_iso8601_date_time(s : str) -> bool:
        """String is a valid ISO 8601 date-time"""
        try:
            dt = datetime.fromisoformat(s)
            return True
        except ValueError:
            return False

    def valid_iso8601_duration(s : str) -> bool:
        """String is a valid ISO 8601 duration"""
        try:
            dur = Duration.from_openehr_adjusted_isoformat(s)
            return True
        except ValueError:
            return False

class ISOType(AnyClass, ABC):
    """Abstract ancestor type of ISO 8601 types, defining interface 
    for 'extended' and 'partial' concepts from ISO 8601."""

    _value : str
    def _get_value(self) -> str:
        return self._value
    
    value : str = property(
        fget=_get_value
    )
    """ISO 8601 string representation of the type"""

    def __init__(self, iso8601_string : str):
        self._value = iso8601_string

    def __str__(self) -> str:
        return self.value

    def is_equal(self, other) -> bool:
        return (type(self) == type(other) and
            self.value == other.value)

    @abstractmethod
    def is_partial(self) -> bool:
        """True if this date time is partial, i.e. if trailing end 
        (right hand) value(s) is/are missing."""
        pass

    @abstractmethod
    def is_extended(self) -> bool:
        """True if this ISO8601 string is in the 'extended' form, 
        i.e. uses '-' and / or ':' separators. 
        This is the preferred format."""
        pass

class ISODate(ISOType):
    """Represents an ISO 8601 date, including partial and extended forms. Value may be:
    * YYYY-MM-DD (extended, preferred)
    * YYYYMMDD (compact)
    * a partial invariant.

    See TimeDefinitions.valid_iso8601_date() for validity."""

    _year : Optional[np.int32]
    _month : Optional[np.int32]
    _day : Optional[np.int32]

    def __init__(self, iso8601_string: str):
        if not TimeDefinitions.valid_iso8601_date(iso8601_string):
            raise ValueError("Not a valid ISO 8601 date.")
        
        compact = iso8601_string.replace("-", "")
        parts = re.split(TimeDefinitions.ISO8601_DATE_COMPACT_REGEX, compact)
        self._year = parts[1][0:4]
        if parts[2] is not None:
            self._month = parts[2][0:2]
        if parts[3] is not None:
            self._day = parts[3][0:2]

        super().__init__(iso8601_string)

    def is_extended(self) -> bool:
        return "-" in self.value
    
    def is_partial(self) -> bool:
        return self._month is None or self._day is None



class Duration:
    # thanks to - https://stackoverflow.com/questions/32044846/regex-for-iso-8601-durations
    ISO8601_DURATION_REGEX = "^P(?=\\d+[YMWD])(\\d+Y)?(\\d+M)?(\\d+W)?(\\d+D)?(T(?=\\d+[HMS])(\\d+H)?(\\d+M)?(\\d+S)?)?$"
    
    def from_openehr_adjusted_isoformat(iso_str : str) -> timedelta:
        negative = False
        if iso_str[0] == '-':
            negative = True
            iso_str = iso_str[1:]
        if re.match(Duration.ISO8601_DURATION_REGEX, iso_str) is None:
            raise ValueError("Provided string was not a valid ISO8601 duration")
        parts = re.split(Duration.ISO8601_DURATION_REGEX, iso_str)
        y, mo, w, d, h, mi, s = [0] * 7
        if parts[1] is not None:
            y = int(parts[1].replace("Y",""))
        if parts[2] is not None:
            mo = int(parts[2].replace("M", ""))
        if parts[3] is not None:
            w = int(parts[3].replace("W", ""))
        if parts[4] is not None:
            d = int(parts[4].replace("D", ""))
        if parts[6] is not None:
            h = int(parts[6].replace("H", ""))
        if parts[7] is not None:
            mi = int(parts[7].replace("M", ""))
        if parts[8] is not None:
            s = int(parts[8].replace("S", ""))

        delt = timedelta(
            days = float(d + TimeDefinitions.AVERAGE_DAYS_IN_MONTH * mo + TimeDefinitions.AVERAGE_DAYS_IN_YEAR * y),
            weeks = w,
            hours = h,
            minutes = mi,
            seconds = s
        )
        return -delt if negative else delt
    
d = ISODate("2022-01-22")
print(d)
