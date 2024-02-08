import pytest
import numpy as np

from org.openehr.base.foundation_types.time import TimeDefinitions as td
from org.openehr.base.foundation_types.time import ISODate, ISODuration, ISOTimeZone, ISOTime, ISODateTime

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
    # allows partial date times
    assert td.valid_iso8601_date_time("2024")
    assert td.valid_iso8601_date_time("2024-02")
    assert td.valid_iso8601_date_time("2024-02-04")
    assert td.valid_iso8601_date_time("2024-02-04T00+01:00")
    assert td.valid_iso8601_date_time("2024-02-04T00:01+01:00")
    assert td.valid_iso8601_date_time("2024-02-04T00:01:02+01:00")
    assert td.valid_iso8601_date_time("2024-02-04T00:01:02.293+01:00")
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
    # fractional seconds supported
    assert td.valid_iso8601_duration("PT2.509S")
    assert td.valid_iso8601_duration("PT2,509S")
    # invalid durations rejected
    assert not td.valid_iso8601_duration("abacus") # invalid in several ways ;-)
    assert not td.valid_iso8601_duration("3W2D") # missing 'P'

def test_iso_date_is_partial():
    d = ISODate("2022-02")
    assert d.is_partial()
    d = ISODate("2022")
    assert d.is_partial()
    d = ISODate("2024-02-05")
    assert not d.is_partial()

def test_iso_date_is_extended():
    d = ISODate("2022-02")
    assert d.is_extended()
    d = ISODate("202202")
    assert not d.is_extended()
    d = ISODate("2022")
    assert d.is_extended()

def test_iso_date_as_string():
    d = ISODate("20240205")
    assert str(d) == "2024-02-05"
    d = ISODate("202405")
    assert d.as_string() == "2024-05"
    d = ISODate("2025")
    assert d.as_string() == "2025"

def test_iso_date_add_throws_type_error_when_partial():
    du = ISODuration("P1Y2M3DT2H30M")
    d = ISODate("2023-01")
    with pytest.raises(ValueError):
        nd = d + du

def test_iso_date_add_correct():
    du = ISODuration("P30D")
    d = ISODate("2022-01-01")
    nd = d + du
    assert str(nd) == "2022-01-31"
    du = ISODuration("P1Y2D")
    nd = d + du
    assert str(nd) == "2023-01-03"

def test_iso_date_subtract_correct():
    du = ISODuration("P30D")
    d = ISODate("2022-01-31")
    nd = d - du
    assert str(nd) == "2022-01-01"
    d = ISODate("2023-01-03")
    du = ISODuration("P1Y2D")
    nd = d - du
    assert str(nd) == "2022-01-01"

def test_iso_date_diff_correct():
    d1 = ISODate("2022-01-31")
    d2 = ISODate("2022-01-01")
    du = d1 - d2
    assert str(du) == "P30D"
    du = d2 - d1
    assert str(du) == "-P30D"
    d1 = ISODate("2023-01-03")
    du = d1 - d2
    assert str(du) == "P367D"

def test_iso_duration_secs_and_fracsecs_correct():
    du = ISODuration("PT1.25S")
    assert du.seconds() == 1
    assert du.fractional_seconds() == 0.25

def test_iso_duration_is_decimal_sign_comma():
    du = ISODuration("PT1,25S")
    assert du.is_decimal_sign_comma()
    du = ISODuration("PT5.125S")
    assert not du.is_decimal_sign_comma()
    du = ISODuration("P1Y")
    assert not du.is_decimal_sign_comma()

def test_iso_duration_add_correct():
    du1 = ISODuration("P1D")
    du2 = ISODuration("PT24H")
    assert str(du1 + du2) == "P2D"
    du1 = ISODuration("P1D")
    du2 = ISODuration("P3W2D")
    assert str(du1 + du2) == "P24D"

def test_iso_duration_multiply_correct():
    du1 = ISODuration("PT50S")
    assert str(du1 * 10) == "PT500S"
    # handles reals
    du1 = ISODuration("P2D")
    assert str(du1 * 0.5) == "P1D"

def test_iso_duration_divide_correct():
    du1 = ISODuration("P2D")
    assert str(du1 / 2.0) == "P1D"

def test_iso_duration_negative_correct():
    du1 = ISODuration("P1Y2M")
    assert str(-du1) == "-P1Y2M"

def test_iso_timezone_valid():
    with pytest.raises(ValueError):
        tz = ISOTimeZone("1200")
    tz = ISOTimeZone("+13")
    assert tz.hour() == 13
    assert tz.minute_unknown()
    assert not tz.is_gmt()
    assert tz.is_partial()
    assert tz.is_extended()
    tz = ISOTimeZone("Z")
    assert tz.hour() == 0
    assert tz.minute() == 0
    assert tz.sign() == 1
    assert tz.is_gmt()
    assert not tz.is_partial()
    assert tz.is_extended()
    tz = ISOTimeZone("-12:00")
    assert tz.hour() == 12
    assert tz.minute() == 0
    assert tz.sign() == -1
    assert not tz.is_gmt()
    assert not tz.is_partial()
    assert tz.is_extended()

def test_iso_timezone_invariants():
    # min_hour_valid: hour <= 12 if sign == -1
    tz = ISOTimeZone("-12:59")
    assert tz.sign() == -1
    with pytest.raises(ValueError):
        tz = ISOTimeZone("-13:00")
    # max_hour_valid: hour <= 14 if sign == 1
    tz = ISOTimeZone("+1459")
    assert tz.sign() == 1
    with pytest.raises(ValueError):
        tz = ISOTimeZone("+1500")
    # minute_valid
    with pytest.raises(ValueError):
        tz = ISOTimeZone("+1399")
    
def test_iso_timezone_is_partial():
    tz = ISOTimeZone("-1100")
    assert not tz.is_extended()
    tz = ISOTimeZone("+12:30")
    assert tz.is_extended()

def test_iso_timezone_as_string():
    tz = ISOTimeZone("Z")
    assert str(tz) == "Z"
    tz = ISOTimeZone("+13:00")
    assert str(tz) == "+13:00"
    tz = ISOTimeZone("-0130")
    assert str(tz) == "-01:30"

def test_iso_time_is_decimal_sign_comma():
    t = ISOTime("12:20:33.599Z")
    assert not t.is_decimal_sign_comma()
    t = ISOTime("12:20:33,599Z")
    assert t.is_decimal_sign_comma()

def test_iso_time_simple_functions():
    t = ISOTime("12:30:45.125+01:30")
    assert t.hour() == 12
    assert t.minute() == 30
    assert t.second() == 45
    assert t.has_fractional_second()
    assert t.fractional_second() == 0.125
    assert t.timezone().value == "+01:30"
    assert t.is_extended()
    assert not t.is_partial()
    t = ISOTime("1445-0200")
    assert t.hour() == 14
    assert t.minute() == 45
    assert t.second() == 0
    assert not t.has_fractional_second()
    assert t.fractional_second() == 0.0
    assert t.timezone().value == "-0200"
    assert not t.is_extended()
    assert t.is_partial()

def test_iso_time_add():
    t1 = ISOTime("12:30:30")
    du = ISODuration("PT2H")
    t2 = t1 + du
    assert str(t2) == "14:30:30"
    t1 = ISOTime("002000.125+0200")
    du = ISODuration("P1DT2H")
    t2 = t1 + du
    assert str(t2) == "02:20:00.125000+02:00"

def test_iso_time_diff():
    t1 = ISOTime("13:00:00")
    t2 = ISOTime("12:01:00")
    du = t1 - t2
    assert str(du) == "PT3540S"
    du = t2 - t1
    assert str(du) == "-PT3540S"

def test_iso_time_subtract():
    t1 = ISOTime("12:30:30Z")
    du = ISODuration("PT2H")
    t2 = t1 - du
    assert str(t2) == "10:30:30Z"

def test_iso_date_time_add():
    td1 = ISODateTime("2024-02-04T00:01:02.293+01:00")
    du = ISODuration("PT2H")
    td2 = td1 + du
    assert str(td2) == "2024-02-04T02:01:02.293000+01:00"

def test_iso_date_time_subtract():
    du = ISODuration("P30D")
    d = ISODateTime("2022-01-31T01:00:00+01:00")
    nd = d - du
    assert str(nd) == "2022-01-01T01:00:00+01:00"
    d = ISODateTime("2023-01-03T00:00:00.000")
    du = ISODuration("P367D")
    nd = d - du
    assert str(nd) == "2022-01-01T00:00:00"

def test_iso_date_time_diff():
    d1 = ISODateTime("2022-01-31T01:00")
    d2 = ISODateTime("2022-01-01T00:00")
    du = d1 - d2
    assert str(du) == "P30DT3600S"
    du = d2 - d1
    assert str(du) == "-P30DT3600S"
    d1 = ISODateTime("2023-01-03")
    du = d1 - d2
    assert str(du) == "P367D"