import pytest
import numpy as np

from org.openehr.base.foundation_types.time import TimeDefinitions as td

def test_valid_year():
    # True if y >= 0
    assert td.valid_year(0)
    assert td.valid_year(2000)
    assert not td.valid_year(-1)

def test_valid_month():
    # True if m >= 1 and m <= months_in_year.
    assert td.valid_month(1)
    assert td.valid_month(12)
    assert not td.valid_month(-1)
    assert not td.valid_month(0)
    assert not td.valid_month(13)

def test_valid_day():
    # True if d >= 1 and d <= days_in_month (m, y).
    assert td.valid_day(2024, 2, 4)
    assert td.valid_day(1998, 12, 23)
    assert td.valid_day(0, 1, 1)
    assert not td.valid_day(2024, 1, 33)
    assert not td.valid_day(2024, 1, -2)
    # handles leap years
    assert td.valid_day(2012, 2, 29)
    assert not td.valid_day(2021, 2, 29)
    assert td.valid_day(2000, 2, 29)
    assert not td.valid_day(2100, 2, 29)
    # handles invalid other parts (year and month)
    assert not td.valid_day(-1, 1, 1)
    assert not td.valid_day(1, -1, 1)

def test_valid_minute():
    # True if m >= 0 and m < Minutes_in_hour.
    assert td.valid_minute(0)
    assert td.valid_minute(13)
    assert td.valid_minute(59)
    assert not td.valid_minute(-1)
    assert not td.valid_minute(60)

def test_valid_second():
    # True if s >= 0 and s < Seconds_in_minute
    assert td.valid_second(0)
    assert td.valid_second(13)
    assert td.valid_second(59)
    assert not td.valid_second(-1)
    assert not td.valid_second(61)

def test_valid_hour():
    # True if (h >= 0 and h < Hours_in_day) or (h = Hours_in_day and m = 0 and s = 0).
    assert td.valid_hour(13, 12, 0)
    assert td.valid_hour(10, 30, 23)
    # handles 24:00:00 case
    assert td.valid_hour(24, 0, 0)
    assert not td.valid_hour(24, 1, 1)
    # handles invalid parts of other
    assert not td.valid_hour(13, -1, 1)
    assert not td.valid_hour(13, 1, -1)

def test_valid_fractional_second():
    # True if fs >= 0.0 and fs < 1.0.
    assert td.valid_fractional_second(0.0)
    assert td.valid_fractional_second(0.990)
    assert not td.valid_fractional_second(1.0)
    assert not td.valid_fractional_second(-0.1)

def test_valid_iso8601_date():
    assert td.valid_iso8601_date("2024-02-04")
    assert td.valid_iso8601_date("20240204")
    assert td.valid_iso8601_date("2012-02-29")
    assert not td.valid_iso8601_date("2100-02-29") # handles leap year
    assert not td.valid_iso8601_date("ababcas")
    assert not td.valid_iso8601_date("2024-02-04T23:59:00")
    # allows partial dates
    assert td.valid_iso8601_date("2022-02")
    assert td.valid_iso8601_date("202202")
    assert td.valid_iso8601_date("2022")
    
def test_valid_iso8601_time():
    assert td.valid_iso8601_time("01:02:03")
    assert td.valid_iso8601_time("00:00:00")
    assert td.valid_iso8601_time("23:59:59")
    # handles partial times
    assert td.valid_iso8601_time("01:00")
    assert td.valid_iso8601_time("12")
    # handles compact times
    assert td.valid_iso8601_time("010203")
    assert td.valid_iso8601_time("000000")
    assert td.valid_iso8601_time("235959")
    # handles fractional seconds
    assert td.valid_iso8601_time("00:01:02,293")
    assert td.valid_iso8601_time("00:01:02.293")
    # handles timezones
    assert td.valid_iso8601_time("02:02:00Z")
    assert td.valid_iso8601_time("02:02:00+01:00")
    assert td.valid_iso8601_time("02:02:00+14:00")
    assert td.valid_iso8601_time("02:02:00-1300")
    assert td.valid_iso8601_time("02:02:00+1500")
    # rejects wrong times
    assert not td.valid_iso8601_time("abacus")
    assert not td.valid_iso8601_time("24:00:00")
    assert not td.valid_iso8601_time("25:00:00")

def test_valid_iso8601_date_time():
    assert td.valid_iso8601_date_time("2024-02-04T00:01:02.293+01:00")
    assert td.valid_iso8601_date_time("20240204T000102.293+0100")
    # rejects wrong times
    assert not td.valid_iso8601_date_time("2024-02-04T24:00:00")
    assert not td.valid_iso8601_date_time("abacus")
    # rejects times alone
    assert not td.valid_iso8601_date_time("02:02:00+01:00")

def test_valid_iso8601_duration():
    assert td.valid_iso8601_duration("P3W")
    assert td.valid_iso8601_duration("P1Y2M3DT2H30M40S")
    # mix of days and weeks supported
    assert td.valid_iso8601_duration("P3W2D")
    # negative durations supported
    assert td.valid_iso8601_duration("-P3M")
    # invalid durations rejected
    assert not td.valid_iso8601_duration("abacus") # invalid in several ways ;-)
    assert not td.valid_iso8601_duration("3W2D") # missing 'P'






