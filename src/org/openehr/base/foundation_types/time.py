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
    
    def days_in_month(m: np.int32, y: np.int32) -> np.int32:
        """[Not in spec] Returns the number of days in month `m` and year `y`"""
        return 31 - ((m - 1) % 7 % 2) if m != 2 else 28 + (1 if TimeDefinitions._is_leap_year(y) else 0)

    def valid_day(y : np.int32, m: np.int32, d: np.int32) -> bool:
        """True if d >= 1 and d <= days_in_month (m, y)."""
        if not (TimeDefinitions.valid_year(y) and TimeDefinitions.valid_month(m)):
            return False
        
        days_in_month = TimeDefinitions.days_in_month(m, y)

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
            dur = ISODuration(s)
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

    _year : np.int32 = 0
    _month : np.int32 = 0
    _day : np.int32 = 0

    def __init__(self, iso8601_string: str):
        # test validity
        s = iso8601_string
        format_ok = (re.match(TimeDefinitions.ISO8601_DATE_COMPACT_REGEX, s) is not None or
        re.match(TimeDefinitions.ISO8601_DATE_EXTENDED_REGEX, s) is not None) 
        compact = s.replace("-", "")
        parts = re.split(TimeDefinitions.ISO8601_DATE_COMPACT_REGEX, compact)
        if not (format_ok and
                TimeDefinitions.valid_year(int(parts[1][0:4])) and
                ((parts[2] is None) or TimeDefinitions.valid_month(int(parts[2][0:2]))) and
                ((parts[3] is None) or TimeDefinitions.valid_day(int(parts[1][0:4]), int(parts[1][4:6]), int(parts[1][6:8])))):
            raise ValueError("Not a valid ISO 8601 date.")
        
        # init components
        self._year = np.int32(parts[1][0:4])
        if parts[2] is not None:
            self._month = np.int32(parts[2][0:2])
        if parts[3] is not None:
            self._day = np.int32(parts[3][0:2])

        super().__init__(iso8601_string)
    
    def to_python_date(self) -> Optional[date]:
        """Converts this to a Python date object, or `None` if 
        it is a partial date (which is not valid in Python)"""
        if self.is_partial():
            return None
        else:
            return date(self._year, self._month, self._day)
        
    def year(self) -> np.int32:
        """Extract the year part of the date as an Integer."""
        return self._year
    
    def month(self) -> np.int32:
        """Extract the month part of the date as an Integer, or return 0 if not present."""
        return self._month
    
    def day(self) -> np.int32:
        """Extract the day part of the date as an Integer, or return 0 if not present."""
        return self._day

    def timezone(self) -> None:
        """Not relevant for a Date, so always `None`"""
        return None
    
    def month_unknown(self) -> bool:
        """Indicates whether month in year is unknown. 
        If so, the date is of the form "YYYY"."""
        return self._month == 0
    
    def day_unknown(self) -> bool:
        """Indicates whether day in month is unknown. 
        If so, and month is known, the date is of 
        the form "YYYY-MM" or "YYYYMM"."""
        return self._day == 0
    
    def is_extended(self) -> bool:
        return ("-" in self.value or self.month_unknown())
    
    def is_partial(self) -> bool:
        return self._month == 0 or self._day == 0
    
    def as_string(self) -> str:
        """Return string value in extended format."""
        if self.is_extended():
            return self.value
        else:
            if self.day_unknown():
                return f"{self._year}-{self._month:02d}"
            else:
                return f"{self._year}-{self._month:02d}-{self._day:02d}"
            
    def __str__(self):
        return self.as_string()
    
    def add(self, a_diff: 'ISODuration'):
        """Arithmetic addition of a duration to a date.
        Will cause a `ValueError` if the date is partial."""
        if self.is_partial():
            raise ValueError("Cannot add a duration to a partial date.")
        else:
            # use built-in Python logic to create a new date
            added = self.to_python_date() + a_diff.to_python_timedelta()
            return ISODate(added.isoformat())
        
    def subtract(self, a_diff: 'ISODuration'):
        """Arithmetic subtraction of a duration from a date.
        Will cause a `ValueError` if the date is partial."""
        if self.is_partial():
            raise ValueError("Cannot subtract a duration from a partial date.")
        else:
            subtracted = self.to_python_date() - a_diff.to_python_timedelta()
            return ISODate(subtracted.isoformat())
        
    def diff(self, a_date: 'ISODate'):
        """Difference of two dates.
        Will cause a `ValueError` if either date is partial."""
        if self.is_partial() or a_date.is_partial():
            raise ValueError("Cannot get the difference between two dates, if either is partial.")
        else:
            difference = self.to_python_date() - a_date.to_python_date()
            return ISODuration.fromtimedelta(difference)
        
    def __add__(self, value : 'ISODuration') -> 'ISODate':
        return self.add(value)
    
    def __sub__(self, value : Union['ISODuration', 'ISODate']) -> Union['ISODate', 'ISODuration']:
        if isinstance(value, ISODate):
            return self.diff(value)
        else:
            return self.subtract(value)
    
    def add_nominal(self, a_diff: 'ISODuration') -> 'ISODate':
        """**NOT IMPLEMENTED** Addition of nominal duration represented by a_diff. 
        For example, a duration of 'P1Y' means advance to the same date next year, 
        with the exception of the date 29 February in a leap year, to which the 
        addition of a nominal year will result in 28 February of the following year. 
        Similarly, 'P1M' is understood here as a nominal month, the addition of which 
        will result in one of:
        * the same day in the following month, if it exists, or;
        * one or two days less where the following month is shorter, or;
        * in the case of adding a month to the date 31 Jan, the result will be 28 Feb 
        in a non-leap year (i.e. three less) and 29 Feb in a leap year (i.e. two less)."""
        raise NotImplementedError("ISODate.add_nominal() is not yet implemented.")
        # if self.month_unknown():
        #     if (a_diff.months() == 0 and
        #         a_diff.days() == 0 and
        #         a_diff.hours() == 0 and
        #         a_diff.minutes() == 0 and
        #         a_diff.seconds() == 0 and
        #         a_diff.fractional_seconds() == 0.0):
        #         # we can safely add years
        #         return ISODate(str(self.year() + a_diff.years()))
        #     else:
        #         raise ValueError("Cannot add duration with granularity above years to partial date with only years")
        # elif self.day_unknown():
        #     if (a_diff.days() == 0 and
        #         a_diff.hours() == 0 and
        #         a_diff.minutes() == 0 and
        #         a_diff.seconds() == 0 and
        #         a_diff.fractional_seconds() == 0.0):
        #         # we can safely add months and years
        #         new_months = (self.month() + a_diff.months()) % 12
        #         new_years = (self.year() + a_diff.years()) + (self.month() + a_diff.months()) // 12
        #         return ISODate(f"{new_years:02d}-{new_months:02d}")
        #     else:
        #         raise ValueError("Cannot add duration with granularity above months to partial date with only months and years")
        # else:
        #     # full date
    
    def subtract_nominal(a_diff : 'ISODuration') -> 'ISODate':
        """**NOT IMPLEMENTED** Subtraction of nominal duration represented by a_diff. 
        See add_nominal() for semantics."""
        raise NotImplementedError("ISODate.subtract_nominal() is not yet implemented.")



        
    



class ISODuration(ISOType):
    """Represents an ISO 8601 duration, which may have multiple parts from years down to seconds."""

    # thanks to - https://stackoverflow.com/questions/32044846/regex-for-iso-8601-durations
    ISO8601_DURATION_REGEX = "^P(?!$)(\\d+Y)?(\\d+M)?(\\d+W)?(\\d+D)?(T(?=\\d)(\\d+H)?(\\d+M)?(\\d+(?:[\\.,]\\d+)?S)?)?$"
    
    _negative : bool = False
    _years : np.int32 = 0
    _months : np.int32 = 0
    _weeks : np.int32 = 0
    _days : np.int32 = 0
    _hours : np.int32 = 0
    _minutes : np.int32 = 0
    _seconds : np.int32 = 0
    _fractional_seconds : np.float32 = 0

    def __init__(self, iso8601_string: str):
        raw = iso8601_string
        iso8601_string = iso8601_string.replace(",", ".")
        if iso8601_string[0] == '-':
            self._negative = True
            iso8601_string = iso8601_string[1:]
        if re.match(ISODuration.ISO8601_DURATION_REGEX, iso8601_string) is None:
            raise ValueError(f"Provided string '{iso8601_string}' was not a valid ISO8601 duration")
        parts = re.split(ISODuration.ISO8601_DURATION_REGEX, iso8601_string)
        if parts[1] is not None:
            self._years = int(parts[1].replace("Y",""))
        if parts[2] is not None:
            self._months = int(parts[2].replace("M", ""))
        if parts[3] is not None:
            self._weeks = int(parts[3].replace("W", ""))
        if parts[4] is not None:
            self._days = int(parts[4].replace("D", ""))
        if parts[6] is not None:
            self._hours = int(parts[6].replace("H", ""))
        if parts[7] is not None:
            self._minutes = int(parts[7].replace("M", ""))
        if parts[8] is not None:
            real_secs = float(parts[8].replace("S", ""))
            self._seconds = int(real_secs)
            self._fractional_seconds = real_secs - float(self._seconds)

        super().__init__(raw)

    def fromtimedelta(td : timedelta) -> 'ISODuration':
        """Create an ISO 8601 duration from a timedelta."""
        iso_str = ""
        if td.total_seconds() < 0.0:
            iso_str += "-"
        iso_str += "P"
        
        if td.days != 0:
            iso_str += str(abs(td.days)) + "D"
        if td.seconds != 0:
            iso_str += "T" + str(abs(td.seconds)) + "S"
        
        return ISODuration(iso_str)

    def is_extended(self) -> bool:
        """Returns True."""
        return True
    
    def is_partial(self) -> bool:
        """Returns False."""
        return False

    def to_python_timedelta(self) -> timedelta:
        """Converts this to a Python `timedelta` object"""
        delt = timedelta(
            days = float(self._days + TimeDefinitions.AVERAGE_DAYS_IN_MONTH * self._months + TimeDefinitions.AVERAGE_DAYS_IN_YEAR * self._years),
            weeks = self._weeks,
            hours = self._hours,
            minutes = self._minutes,
            seconds = (float(self._seconds) + self._fractional_seconds)
        )
        return -delt if self._negative else delt
    
    def years(self) -> np.int32:
        """Number of years in the value, i.e. the number preceding the
         'Y' in the 'YMD' part, if one exists."""
        return self._years
    
    def months(self) -> np.int32:
        """Number of months in the value, i.e. the value preceding the 
        'M' in the 'YMD' part, if one exists."""
        return self._months
    
    def days(self) -> np.int32:
        """Number of days in the value, i.e. the number preceding the 
        'D' in the 'YMD' part, if one exists."""
        return self._days
    
    def hours(self) -> np.int32:
        """Number of hours in the value, i.e. the number preceding the 
        'H' in the 'HMS' part, if one exists."""
        return self._hours
    
    def minutes(self) -> np.int32:
        """Number of minutes in the value, i.e. the number preceding the 
        'M' in the 'HMS' part, if one exists."""
        return self._minutes
    
    def seconds(self) -> np.int32:
        """Number of seconds in the value, i.e. the integer number preceding the 
        'S' in the 'HMS' part, if one exists."""
        return self._seconds
    
    def fractional_seconds(self) -> np.int32:
        """Fractional seconds in the value, i.e. the decimal part of the number 
        preceding the 'S' in the 'HMS' part, if one exists."""
        return self._fractional_seconds
    
    def weeks(self) -> np.int32:
        """Number of weeks in the value, i.e. the value preceding the 
        W, if one exists."""
        return self._weeks
    
    def is_decimal_sign_comma(self) -> bool:
        """True if this time has a decimal part indicated by ',' (comma) 
        rather than '.' (period)."""
        return ("," in self.value)
    
    def to_seconds(self) -> np.float32:
        """Total number of seconds equivalent (including fractional) 
        of entire duration. Where non-definite elements such as year 
        and month (i.e. 'Y' and 'M') are included, the corresponding 
        'average' durations from TimeDefinitions are used to compute 
        the result."""
        return self.to_python_timedelta().total_seconds()
    
    def as_string(self) -> str:
        return self.value
    
    # TODO: add, subtract, multiply, divide, negative