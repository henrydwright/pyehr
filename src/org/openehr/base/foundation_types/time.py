from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta, time, timezone
from typing import Union, Optional
import re

from org.openehr.base.foundation_types import AnyClass

import numpy as np

# Most of the logic of the time classes uses native
#  Python logic from datetime types, wrapped to allow
#  ISO 8601 string preservation and partial dates and
#  partial date/times

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
        """String is a valid ISO 8601 date"""
        try:
            d = ISODate(s)
            return True
        except ValueError:
            return False

        
    def valid_iso8601_time(s : str) -> bool:
        """String is a valid ISO 8601 time"""
        try:
            t = ISOTime(s)
            return True
        except ValueError:
            return False

    def valid_iso8601_date_time(s : str) -> bool:
        """String is a valid ISO 8601 date-time"""
        try:
            dt = ISODateTime(s)
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
    def __lt__(self, other) -> bool:
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass

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
        
    def _comparison_check(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare type of \'{type(self)}\' with type of \'{type(other)}\'")
        if self.is_partial() or other.is_partial():
            raise ValueError("Cannot compare partial dates.")

    def __ge__(self, other: 'ISODate'):
        self._comparison_check(other)
        return (self.to_python_date() >= other.to_python_date())
    
    def __gt__(self, other: 'ISODate'):
        self._comparison_check(other)
        return (self.to_python_date() > other.to_python_date())
    
    def __le__(self, other: 'ISODate'):
        self._comparison_check(other)
        return (self.to_python_date() <= other.to_python_date())
    
    def __lt__(self, other: 'ISODate'):
        self._comparison_check(other)
        return (self.to_python_date() < other.to_python_date())
        
    def add_nominal(self, a_diff: 'ISODuration') -> 'ISODate':
        """Addition of nominal duration represented by a_diff. 
        For example, a duration of 'P1Y' means advance to the same date next year, 
        with the exception of the date 29 February in a leap year, to which the 
        addition of a nominal year will result in 28 February of the following year. 
        Similarly, 'P1M' is understood here as a nominal month, the addition of which 
        will result in one of:
        * the same day in the following month, if it exists, or;
        * one or two days less where the following month is shorter, or;
        * in the case of adding a month to the date 31 Jan, the result will be 28 Feb 
        in a non-leap year (i.e. three less) and 29 Feb in a leap year (i.e. two less)."""

        if self.is_partial():
            if self._day == 0 and a_diff.days() > 0:
                raise ValueError("Cannot add a nominal period in days to a partial date (year and month only)")
            elif self._month == 0 and a_diff.months() > 0:
                raise ValueError("Cannot add a nominal period in months to a partial date (year only)")

        y = self._year
        m = self._month
        d = self._day

        years = a_diff.years()
        months = a_diff.months()
        days = a_diff.days()

        # Add years and months
        new_year = y + years
        new_month = m + months

        # Adjust year and month if month > 12
        while new_month > 12:
            new_year += 1
            new_month -= 12

        if not self.is_partial():
            # Find max day in new month/year
            max_day = TimeDefinitions.days_in_month(new_month, new_year)

            # Special case: 29 Feb in leap year + 1Y => 28 Feb next year if not leap
            if d == 29 and m == 2 and years > 0 and not TimeDefinitions._is_leap_year(np.int32(new_year)):
                new_day = 28
            else:
                new_day = min(d, max_day)

            # Add days
            try:
                result_date = date(new_year, new_month, new_day) + timedelta(days=days)
            except ValueError:
                # If day is out of range, fallback to last day of month
                result_date = date(new_year, new_month, max_day) + timedelta(days=days)

            return ISODate(result_date.isoformat())
        
        # partial dates
        if self._month == 0:
            return ISODate(f"{new_year:04d}")
        else:
            return ISODate(f"{new_year:04d}-{new_month:02d}")

    
    def subtract_nominal(self, a_diff : 'ISODuration') -> 'ISODate':
        """Subtraction of nominal duration represented by a_diff. 
        For example, a duration of 'P1Y' means go back to the same date last year, 
        with the exception of the date 29 February in a leap year, to which the 
        subtraction of a nominal year will result in 28 February of the previous year. 
        Similarly, 'P1M' is understood here as a nominal month, the subtraction of which 
        will result in one of:
        * the same day in the previous month, if it exists, or;
        * one or two days less where the previous month is shorter, or;
        * in the case of taking away a month from the date 31 Mar, the result will be 28 Feb 
        in a non-leap year (i.e. three less) and 29 Feb in a leap year (i.e. two less)."""

        if self.is_partial():
            if self._day == 0 and a_diff.days() > 0:
                raise ValueError("Cannot subtract a nominal period in days from a partial date (year and month only)")
            elif self._month == 0 and a_diff.months() > 0:
                raise ValueError("Cannot subtract a nominal period in months from a partial date (year only)")

        y = self._year
        m = self._month
        d = self._day

        years = a_diff.years()
        months = a_diff.months()
        days = a_diff.days()

        # Subtract years and months
        new_year = y - years
        new_month = m - months

        # Adjust year and month if month < 0
        while new_month < 0:
            new_year -= 1
            new_month += 12

        if not self.is_partial():
            # Find max day in new month/year
            max_day = TimeDefinitions.days_in_month(new_month, new_year)

            # Special case: 29 Feb in leap year - 1Y => 28 Feb previous year if not leap
            if d == 29 and m == 2 and years > 0 and not TimeDefinitions._is_leap_year(np.int32(new_year)):
                new_day = 28
            else:
                new_day = min(d, max_day)

            # Subtract days
            try:
                result_date = date(new_year, new_month, new_day) - timedelta(days=days)
            except ValueError:
                # If day is out of range, fallback to last day of month
                result_date = date(new_year, new_month, max_day) - timedelta(days=days)

            return ISODate(result_date.isoformat())
        
        # partial dates
        if self._month == 0:
            return ISODate(f"{new_year:04d}")
        else:
            return ISODate(f"{new_year:04d}-{new_month:02d}")

class ISOTime(ISOType):
    """Represents an ISO 8601 time, including partial and extended forms. Value may be:
    * hh:mm:ss[(,|.)sss][Z|±hh[:mm]] (extended, preferred) or
    * hhmmss[(,|.)sss][Z|±hh[mm]] (compact)
    * or a partial invariant.
    
    See `TimeDefinitions.valid_iso8601_time()` for validity."""

    ISO8601_TIME_REGEX= "^(\\d\\d(\\d\\d(\\d\\d(.\\d\\d?\\d?\\d?\\d?\\d?)?)?)?)?([Z]|([+-])(\\d\\d)(\\d\\d)?)?$"

    _time : time
    _minute_unknown : bool = True
    _second_unknown : bool = True
    _has_fractional_second : bool = False
    _timezone : Optional['ISOTimeZone'] = None

    def __init__(self, iso8601_string: str):
        self._time = time.fromisoformat(iso8601_string)
        s = iso8601_string.replace(":", "").replace(",", ".")
        parts = re.split(ISOTime.ISO8601_TIME_REGEX, s)
        if parts[2] is not None:
            self._minute_unknown = False
        if parts[3] is not None:
            self._second_unknown = False
        if parts[4] is not None:
            self._has_fractional_second = True
        if parts[5] is not None:
            tz_index = iso8601_string.index(parts[5][0:1])
            self._timezone = ISOTimeZone(iso8601_string[tz_index:])
        super().__init__(iso8601_string)

    def to_python_time(self) -> time:
        """Return the Python `time` repesentation of this object"""
        return self._time

    def hour(self) -> np.int32:
        """Extract the hour part of the date/time as an Integer."""
        return np.int32(self._time.hour)
    
    def minute(self) -> np.int32:
        """Extract the minute part of the time as an Integer, or return 0 if not present."""
        return np.int32(self._time.minute)

    def second(self) -> np.int32:
        """Extract the integral seconds part of the time (i.e. prior to any decimal sign) as an Integer, or return 0 if not present."""
        return np.int32(self._time.second)

    def fractional_second(self) -> np.float32:
        """Extract the fractional seconds part of the time (i.e. following to any decimal sign) as a Real, or return 0.0 if not present."""
        return np.float32(self._time.microsecond / 1000000.0)

    def timezone(self) -> Optional['ISOTimeZone']:
        """Timezone; may be Void."""
        return self._timezone

    def minute_unknown(self) -> bool:
        """Indicates whether minute is unknown. If so, the time is of the form “hh”."""
        return self._minute_unknown

    def second_unknown(self) -> bool:
        """Indicates whether second is unknown. If so and month is known, the time is of the form "hh:mm" or "hhmm"."""
        return self._second_unknown

    def is_decimal_sign_comma(self) -> bool:
        """True if this time has a decimal part indicated by ',' (comma) rather than '.' (period)."""
        return "," in self.value

    def is_partial(self) -> bool:
        """True if this time is partial, i.e. if seconds or more is missing."""
        return (self._minute_unknown or self._second_unknown)
    
    def is_extended(self) -> bool:
        """True if this time uses '-', ':' separators."""
        return ":" in self.value
    
    def has_fractional_second(self) -> bool:
        """True if the fractional_second part is significant (i.e. even if = 0.0)."""
        return self._has_fractional_second

    def as_string(self) -> str:
        """Return string value in extended format."""
        if self.is_extended():
            return self.value
        else:
            return self._time.isoformat()

    def __str__(self) -> str:
        return self.as_string()
    
    def add(self, a_diff : 'ISODuration') -> 'ISOTime':
        """Arithmetic addition of a duration to a time"""
        t = datetime(2000,1,1,self.hour(), self.minute(), self.second(), self._time.microsecond) + a_diff.to_python_timedelta()
        tstr = (t.time().isoformat() + str(self.timezone())) if self.timezone() is not None else t.time().isoformat()
        return ISOTime(tstr)

    def __add__(self, value: 'ISODuration') -> 'ISOTime':
        return self.add(value)
    
    def subtract(self, a_diff: 'ISODuration') -> 'ISOTime':
        """Arithmetic subtraction of a duration from a time."""
        t = datetime(2000,1,1,self.hour(), self.minute(), self.second(), self._time.microsecond) - a_diff.to_python_timedelta()
        tstr = (t.time().isoformat() + str(self.timezone())) if self.timezone() is not None else t.time().isoformat()
        return ISOTime(tstr)

    def diff(self, a_time: 'ISOTime') -> 'ISODuration':
        """Difference of two times."""
        t1 = datetime(2000,1,1,self._time.hour, self._time.minute, self._time.second, self._time.microsecond)
        t2 = datetime(2000,1,1,a_time._time.hour, a_time._time.minute, a_time._time.second, a_time._time.microsecond)
        t = t1 - t2
        return ISODuration.fromtimedelta(t)

    def __sub__(self, value : Union['ISODuration', 'ISOTime']) -> Union['ISOTime', 'ISODuration']:
        if isinstance(value, ISOTime):
            return self.diff(value)
        else:
            return self.subtract(value)
        
    def _comparison_check(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare type of \'{type(self)}\' with type of \'{type(other)}\'")

    def __ge__(self, other: 'ISOTime'):
        self._comparison_check(other)
        return (self.to_python_time() >= other.to_python_time())
    
    def __gt__(self, other: 'ISOTime'):
        self._comparison_check(other)
        return (self.to_python_time() > other.to_python_time())
    
    def __le__(self, other: 'ISOTime'):
        self._comparison_check(other)
        return (self.to_python_time() <= other.to_python_time())
    
    def __lt__(self, other: 'ISOTime'):
        self._comparison_check(other)
        return (self.to_python_time() < other.to_python_time())

class ISODateTime(ISOType):
    """Represents an ISO 8601 date/time, including partial and extended forms. Value may be:
    * YYYY-MM-DDThh:mm:ss[(,|.)sss][Z | ±hh[:mm]] (extended, preferred) or
    * YYYYMMDDThhmmss[(,|.)sss][Z | ±hh[mm]] (compact)
    * or a partial variant.
    
    See `TimeDefinitions.valid_iso8601_date_time()` for validity.

    Note that this class includes 2 deviations from ISO 8601:2004:
    * for partial date/times, any part of the date/time up to the month may be missing, not just seconds and minutes as in the standard;
    * the time 24:00:00 is not allowed, since it would mean the date was really on the next day."""

    _date : ISODate
    _time : Optional[ISOTime] = None

    _python_datetime : Optional[datetime] = None

    def __init__(self, iso8601_string: str):
        s = iso8601_string
        if "T" in s:
            date_str = s[:s.index("T")]
            time_str = s[s.index("T") + 1:]
            self._date = ISODate(date_str)
            if self._date.is_partial():
                raise ValueError("Cannot have time with partial date")
            self._time = ISOTime(time_str)
            if ((self._date.is_extended() and not self._time.is_extended()) or 
            (self._time.is_extended() and not self._date.is_extended())):
                raise ValueError("Both date and time must use extended form, or compact form, not a combination")
            self._python_datetime = datetime.fromisoformat(iso8601_string)
        else:
            self._date = ISODate(s)
            if not self._date.is_partial():
                self._python_datetime = datetime.fromisoformat(iso8601_string)
        super().__init__(iso8601_string)

    def is_partial(self) -> bool:
        """True if this date time is partial, i.e. if seconds or more is missing."""
        return (self._date.is_partial() or self._time.is_partial())
    
    def is_extended(self) -> bool:
        """True if this date/time uses '-', ':' separators."""
        return self._date.is_extended()
    
    # date methods
    def year(self) -> np.int32:
        """Extract the year part of the date as an Integer."""
        return self._date.year()
    
    def month(self) -> np.int32:
        """Extract the month part of the date/time as an Integer, or return 0 if not present."""
        return self._date.month()
    
    def day(self) -> np.int32:
        """Extract the day part of the date/time as an Integer, or return 0 if not present."""
        return self._date.day()
    
    def month_unknown(self) -> bool:
        """Indicates whether month in year is unknown."""
        return self._date.month_unknown()
    
    def day_unknown(self) -> bool:
        """Indicates whether day in month is unknown."""
        return self._date.day_unknown()
    
    # time methods
    def hour(self) -> np.int32:
        """Extract the hour part of the date/time as an Integer, or return 0 if not present."""
        return self._time.hour()
    
    def minute(self) -> np.int32:
        """Extract the minute part of the date/time as an Integer, or return 0 if not present."""
        return self._time.minute()
    
    def second(self) -> np.int32:
        """Extract the integral seconds part of the date/time (i.e. prior to any decimal sign) as an Integer, or return 0 if not present."""
        return self._time.second()
    
    def fractional_second(self) -> np.float32:
        """Extract the fractional seconds part of the date/time (i.e. following to any decimal sign) as a Real, or return 0.0 if not present."""
        return self._time.fractional_second()
    
    def timezone(self) -> 'ISOTimeZone':
        """Timezone; may be Void."""
        return self._time.timezone()
    
    def minute_unknown(self) -> bool:
        """Indicates whether minute in hour is known."""
        return self._time.minute_unknown()
    
    def second_unknown(self) -> bool:
        """Indicates whether minute in hour is known."""
        return self._time.second_unknown()
    
    def is_decimal_sign_comma(self) -> bool:
        """True if this time has a decimal part indicated by ',' (comma) rather than '.' (period)."""
        return self._time.is_decimal_sign_comma()
    
    def has_fractional_second(self) -> bool:
        """True if the fractional_second part is significant (i.e. even if = 0.0)."""
        return self._time.has_fractional_second()
    
    # date/time specific methods

    def as_string(self) -> str:
        """Return the string value in extended format."""
        if self._time is None:
            return str(self._date)
        else:
            return str(self._date) + "T" + str(self._time)
        
    def __str__(self):
        return self.as_string()
    
    def add(self, a_diff: 'ISODuration') -> 'ISODateTime':
        """Arithmetic addition of a duration to a date/time."""
        if self._date.is_partial():
            return ISODateTime(str(self._date.add(a_diff)))
        else:
            dt = self._python_datetime + a_diff.to_python_timedelta()
            return ISODateTime(dt.isoformat())

    def __add__(self, value: 'ISODuration') -> 'ISODateTime':
        return self.add(value)
    
    def subtract(self, a_diff: 'ISODuration') -> 'ISODateTime':
        """Arithmetic subtraction of a duration from a date/time."""
        if self._date.is_partial():
            return ISODateTime(str(self._date.subtract(a_diff)))
        else:
            dt = self._python_datetime - a_diff.to_python_timedelta()
            return ISODateTime(dt.isoformat())
        
    def diff(self, a_diff: 'ISODateTime') -> 'ISODuration':
        if self._date.is_partial() or a_diff._date.is_partial():
            raise ValueError("Difference between a partial date/time and another partial date/time is not defined")
        else:
            td = self._python_datetime - a_diff._python_datetime
            return ISODuration.fromtimedelta(td)
        
    def __sub__(self, value : Union['ISODuration', 'ISODateTime']) -> Union['ISODateTime', 'ISODuration']:
        if isinstance(value, ISODateTime):
            return self.diff(value)
        else:
            return self.subtract(value)
        
    def _comparison_check(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare type of \'{type(self)}\' with type of \'{type(other)}\'")
        if self.is_partial() or other.is_partial():
            raise ValueError("Cannot compare partial datetimes.")

    def __ge__(self, other: 'ISODateTime'):
        self._comparison_check(other)
        return (self._python_datetime >= other._python_datetime)
    
    def __gt__(self, other: 'ISODateTime'):
        self._comparison_check(other)
        return (self._python_datetime > other._python_datetime)
    
    def __le__(self, other: 'ISODateTime'):
        self._comparison_check(other)
        return (self._python_datetime <= other._python_datetime)
    
    def __lt__(self, other: 'ISODateTime'):
        self._comparison_check(other)
        return (self._python_datetime < other._python_datetime)


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
            td = -td # makes negative timedeltas appear correctly
        iso_str += "P"
        
        if td.days != 0:
            iso_str += str(abs(td.days)) + "D"
        if (td.seconds != 0 or td.microseconds != 0) or (td.total_seconds() == 0.0):
            total_secs = float(td.seconds)
            if td.microseconds != 0:
                total_secs += td.microseconds / 1000000.0
                print(td.microseconds)
            iso_str += f"T{abs(total_secs):g}S"
        
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
    
    def add(self, a_val : 'ISODuration') -> 'ISODuration':
        """Arithmetic addition of a duration to a duration, via conversion 
        to seconds, using TimeDefinitions.Average_days_in_year and 
        TimeDefinitions.Average_days_in_month
        
        Result string will be in days and seconds"""
        return ISODuration.fromtimedelta(self.to_python_timedelta() + a_val.to_python_timedelta())
    
    def __add__(self, value : 'ISODuration') -> 'ISODuration':
        return self.add(value)
    
    def subtract(self, a_val : 'ISODuration') -> 'ISODuration':
        """Arithmetic subtraction of a duration from a duration, via conversion 
        to seconds, using Time_definitions.Average_days_in_year and 
        Time_definitions.Average_days_in_month
        
        Result string will be in days and seconds"""
        return ISODuration.fromtimedelta(self.to_python_timedelta() - a_val.to_python_timedelta())
    
    def __sub__(self, value : 'ISODuration') -> 'ISODuration':
        return self.subtract(value)
    
    def multiply(self, a_val : np.float32) -> 'ISODuration':
        """Arithmetic multiplication a duration by a number.
        
        Result string will be in days and seconds"""
        return ISODuration.fromtimedelta(self.to_python_timedelta() * a_val)
    
    def __mul__(self, value: np.float32) -> 'ISODuration':
        return self.multiply(value)
    
    def divide(self, a_val : np.float32) -> 'ISODuration':
        """Arithmetic division of a duration by a number.
        
        Result string will be in days and seconds"""
        return ISODuration.fromtimedelta(self.to_python_timedelta() / a_val)   

    def __truediv__(self, value: np.float32) -> 'ISODuration':
        return self.divide(value)  

    def negative(self) -> 'ISODuration':
        """Generate negative of current duration value."""
        if self._negative:
            return ISODuration(self.value[1:])
        else:
            return ISODuration("-" + self.value)
    
    def __neg__(self) -> 'ISODuration':
        return self.negative()
    
    def _comparison_check(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare type of \'{type(self)}\' with type of \'{type(other)}\'")
        if self.is_partial() or other.is_partial():
            raise ValueError("Cannot compare partial durations.")

    def __ge__(self, other: 'ISODuration'):
        self._comparison_check(other)
        return (self.to_python_timedelta() >= other.to_python_timedelta())
    
    def __gt__(self, other: 'ISODuration'):
        self._comparison_check(other)
        return (self.to_python_timedelta() > other.to_python_timedelta())
    
    def __le__(self, other: 'ISODuration'):
        self._comparison_check(other)
        return (self.to_python_timedelta() <= other.to_python_timedelta())
    
    def __lt__(self, other: 'ISODuration'):
        self._comparison_check(other)
        return (self.to_python_timedelta() < other.to_python_timedelta())

class ISOTimeZone(ISOType):
    """ISO8601 timezone string, in format:
    
    `Z | ±hh[mm]`
    
    where:
    * `hh` is "00" - "23" (0-filled to two digits)
    * `mm` is "00" - "59" (0-filled to two digits)
    * `Z` is a literal meaning UTC (modern replacement for GMT), i.e. timezone `+0000`"""

    ISO8601_TIMEZONE_REGEX = "^[Z]|([+-])(\\d\\d)(\\:?\\d\\d)?$"

    _hour : np.int32 = 0
    _minute : np.int32 = 0
    _sign : np.int32 = 1

    _is_extended : bool = True
    _is_partial : bool = True

    def __init__(self, iso8601_string: str):
        if re.match(ISOTimeZone.ISO8601_TIMEZONE_REGEX, iso8601_string) is None:
            raise ValueError("Given string was not a valid ISO 8601 Timezone")
        s = iso8601_string
        if s == "Z":
            self._is_partial = False
            # other defaults are OK
        else:
            s = s.replace(":", "")
            parts = re.split(ISOTimeZone.ISO8601_TIMEZONE_REGEX, s)
            self._sign = -1 if parts[1] == "-" else 1
            self._hour = int(parts[2])

            # ensure hour is valid
            if ((self._sign == -1 and self._hour > TimeDefinitions.MIN_TIMEZONE_HOUR) or
                (self._sign == 1 and self._hour > TimeDefinitions.MAX_TIMEZONE_HOUR)):
                raise ValueError("Timezone must be between -12:59 and +14:59")
            
            # if minutes present, then not partial
            if parts[3] is not None:
                self._minute = int(parts[3])
                if not TimeDefinitions.valid_minute(self._minute):
                    raise ValueError("Minutes must be strictly between 00 and 59")
                self._is_partial = False
                self._is_extended = ":" in iso8601_string

        super().__init__(iso8601_string)

    def to_python_timezone(self) -> timezone:
        """Converts this to a Python `timezone` object"""
        return timezone(self.sign() * timedelta(hours=self._hour, minutes=self._minute))

    def is_partial(self) -> bool:
        """True if this time zone is partial, i.e. if minutes is missing."""
        return self._is_partial
    
    def is_extended(self) -> bool:
        """True if this time-zone uses ':' separators."""
        return self._is_extended
    
    def hour(self) -> np.int32:
        """Extract the hour part of timezone, as an Integer in the range 00 - 14."""
        return self._hour

    def minute(self) -> np.int32:
        """Extract the hour part of timezone, as an Integer, usually either 0 or 30."""
        return self._minute

    def sign(self) -> np.int32:
        """Direction of timezone expresssed as +1 or -1."""
        return self._sign

    def minute_unknown(self) -> bool:
        """Indicates whether minute part known."""
        return self.is_partial()

    def is_gmt(self) -> bool:
        """True if timezone is UTC, i.e. +0000."""
        return self.value == "Z" or (self._hour == 0 and self._minute == 0)

    def as_string(self) -> str:
        """Return timezone string in extended format."""
        if self._is_extended:
            return self.value
        elif self._sign == 1:
            return f"+{self._hour:02d}:{self._minute:02d}"
        else:
            return f"-{self._hour:02d}:{self._minute:02d}"

    def __str__(self) -> str:
        return self.as_string()
    
    def _comparison_check(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare type of \'{type(self)}\' with type of \'{type(other)}\'")

    def __ge__(self, other: 'ISOTimeZone'):
        self._comparison_check(other)
        return (self.is_equal(other) or self > other)
    
    def __gt__(self, other: 'ISOTimeZone'):
        self._comparison_check(other)
        val_self = self._sign * ((self._hour * 60) + self._minute)
        val_other = other._sign * ((other._hour * 60) + other._minute)
        return (val_self > val_other)
    
    def __le__(self, other: 'ISOTimeZone'):
        self._comparison_check(other)
        return (self.is_equal(other) or self < other)
    
    def __lt__(self, other: 'ISOTimeZone'):
        self._comparison_check(other)
        val_self = self._sign * ((self._hour * 60) + self._minute)
        val_other = other._sign * ((other._hour * 60) + other._minute)
        return (val_self < val_other)
    
temporal = ISOType
"""Abstract ancestor of time-related classes."""