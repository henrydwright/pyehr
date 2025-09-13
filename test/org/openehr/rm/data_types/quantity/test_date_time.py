import pytest

from org.openehr.rm.data_types.quantity.date_time import DVDuration, DVDate, DVTime, DVDateTime
from org.openehr.rm.data_types.quantity import DVAmount
from org.openehr.base.foundation_types.time import ISODate

def test_dv_duration_add():
    dvd1 = DVDuration("P30D")
    dvd2 = DVDuration("P2D")
    dvdr = dvd1 + dvd2
    assert dvdr.value == "P32D"

def test_dv_duration_subtract():
    dvd1 = DVDuration("P40D")
    dvd2 = DVDuration("P10D")
    dvdr = dvd1 - dvd2
    assert dvdr.value == "P30D"

def test_dv_duration_multiply():
    dvd1 = DVDuration("P20D")
    dvdr = dvd1 * 2.0
    assert dvdr.value == "P40D"
    dvdr = 2.0 * dvd1
    assert dvdr.value == "P40D"

def test_dv_duration_truediv():
    dvd1 = DVDuration("P20D")
    dvdr = dvd1 / 5.0
    assert dvdr.value == "P4D"

def test_dv_duration_ordered_operators():
    dvd1 = DVDuration("P1Y")
    dvd2 = DVDuration("PT2.5S")
    assert dvd2 < dvd1
    assert dvd1 > dvd2
    assert dvd2 <= dvd1
    assert dvd1 >= dvd2

    with pytest.raises(TypeError):
        dvd1 < DVAmount(5)

def test_dv_duration_negative():
    dvd1 = DVDuration("P1Y")
    dvdr = -dvd1
    assert dvdr.value == "-P1Y"
    dvd2 = DVDuration("-P2M")
    dvdr = -dvd2
    assert dvdr.value == "P2M"

def test_dv_duration_magnitude():
    dvd = DVDuration("P44D")
    assert dvd.magnitude() <= 3801600.001 and dvd.magnitude() >= 3801599.999

def test_dv_duration_is_equal():
    assert DVDuration("P30D").is_equal(DVDuration("P30D"))

def test_dv_date_magnitude():
    dvdate = DVDate("0001-01-03")
    assert dvdate.magnitude() == 2
    dvdate = DVDate("2025-09-02")
    assert dvdate.magnitude() == 739495

def test_dv_date_addition():
    dvd1 = DVDate("2025-09-02")
    dvdr = dvd1 + DVDuration("P2D")
    assert dvdr.value == "2025-09-04"

    dvd2 = DVDate("2020-01-20")
    dvdr = dvd2 + DVDuration("-P5D")
    assert dvdr.value == "2020-01-15"

    with pytest.raises(TypeError):
        dvd2 + dvd1

    # check accuracies
    dvdr = DVDate("2020-01-03", accuracy=DVDuration("P3D")) + DVDuration("P2D", accuracy=86400.0, accuracy_is_percent=False)
    assert dvdr.accuracy.is_equal(DVDuration("P4D"))

def test_dv_date_subtract():
    dvd1 = DVDate("2025-09-02")
    dvdr = dvd1 - DVDuration("-P2D")
    assert dvdr.value == "2025-09-04"

    dvd2 = DVDate("2020-01-20")
    dvdr = dvd2 - DVDuration("P5D")
    assert dvdr.value == "2020-01-15"

    # check accuracies
    dvdr = DVDate("2020-01-03", accuracy=DVDuration("P3D")) - DVDuration("P2D", accuracy=86400.0, accuracy_is_percent=False)
    assert dvdr.accuracy.is_equal(DVDuration("P4D"))

def test_dv_date_diff():
    dvdr = DVDate("2025-09-02") - DVDate("0001-01-01")
    assert dvdr.value == "P739495D"

    # check accuracies
    dvdr = DVDate("2025-09-02", accuracy=DVDuration("P2D")) - DVDate("0001-01-01", accuracy=DVDuration("PT0S"))
    assert dvdr.accuracy.is_equal(DVDuration("P2D"))

def test_dv_date_comparison():
    assert DVDate("2025-09-02") > DVDate("2024-09-02")
    assert DVDate("2025-09-02") <= DVDate("2025-09-02")
    assert DVDate("0001-02-03") >= DVDate("0001-01-01")
    assert DVDate("2025-02-01") == DVDate("2025-02-01")
    assert DVDate("2025-09-02") < DVDate("2026-09-02")

def test_dv_date_value_valid():
    dvd1 = DVDate("2025-09-02")
    dvd2 = DVDate("2025-09")
    dvd3 = DVDate("2025")
    with pytest.raises(ValueError):
        dvd4 = DVDate("1")
    with pytest.raises(ValueError):
        dvd5 = DVDate("Abacus")
    with pytest.raises(ValueError):
        dvd6 = DVDate("23-12-1998")

def test_dv_date_is_equal():
    assert DVDate("2024-03-20").is_equal(DVDate("2024-03-20")) == True
    assert DVDate("2024-03-20").is_equal(ISODate("2024-03-20")) == False

def test_dv_time_value_valid():
    dvtp = DVTime("10:30")
    dvt1 = DVTime("10:30:00")
    dvt2 = DVTime("10:00:00.000Z")
    dvt3 = DVTime("10:00:00.000+01:00")
    with pytest.raises(ValueError):
        dvt4 = DVTime("1")
    with pytest.raises(ValueError):
        dvt5 = DVTime("Abacus")
    with pytest.raises(ValueError):
        dvd6 = DVTime("1:00")

def test_dv_time_magnitude():
    assert DVTime("10:00:00").magnitude() == 36000.0
    assert DVTime("00:00:01.500").magnitude() == 1.5
    assert DVTime("00:15:00Z").magnitude() == 900.0
    assert DVTime("01:01:00+01:10").magnitude() == 3660.0

def test_dv_time_add():
    assert (DVTime("03:00:00") + DVDuration("PT2H")).is_equal(DVTime("05:00:00"))
    assert (DVTime("01:00:00") + DVDuration("P1D")).is_equal(DVTime("01:00:00"))

    # check accuracies
    dvt1 = DVTime("01:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVDuration("PT2H", accuracy=60.0, accuracy_is_percent=False)
    assert (dvt1 + dvt2).accuracy.is_equal(DVDuration("PT90S"))

def test_dv_time_subtract():
    assert (DVTime("03:00:00") - DVDuration("PT2H")) == DVTime("01:00:00")
    assert (DVTime("01:00:00") - DVDuration("P1D")) == DVTime("01:00:00")

    # check accuracies
    dvt1 = DVTime("03:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVDuration("PT2H", accuracy=60.0, accuracy_is_percent=False)
    assert (dvt1 - dvt2).accuracy.is_equal(DVDuration("PT90S"))

def test_dv_time_diff():
    assert (DVTime("03:00:00") - DVTime("02:00:00")).is_equal(DVDuration("PT3600S"))
    assert (DVTime("01:00:00") - DVTime("01:00:00")).is_equal(DVDuration("PT0S"))

    # check accuracies
    dvt1 = DVTime("03:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVTime("01:00:00", accuracy=DVDuration("PT60S"))
    assert (dvt1 - dvt2).accuracy == 90.0

def test_dv_time_has_iso_time_methods():
    dvt = DVTime("05:04:03.128+02:00")
    assert dvt.hour() == 5
    assert dvt.minute() == 4
    assert dvt.second() == 3
    assert dvt.fractional_second() > 0.12
    assert dvt.timezone().value == "+02:00"
    assert dvt.minute_unknown() == False
    assert dvt.second_unknown() == False
    assert dvt.is_decimal_sign_comma() == False
    assert dvt.is_partial() == False
    assert dvt.is_extended() == True
    assert dvt.has_fractional_second() == True
    assert dvt.as_string() == "05:04:03.128+02:00"

def test_dv_datetime_value_valid():
    dvdtp = DVDateTime("2025")
    dvdt1 = DVDateTime("2025-09-13T10:30:00")
    dvdt2 = DVDateTime("2024-03-02T10:00:00.000Z")
    dvdt3 = DVDateTime("20240302T100000.000+0100")
    with pytest.raises(ValueError):
        dvt4 = DVDateTime("1")
    with pytest.raises(ValueError):
        dvt5 = DVDateTime("Abacus")
    with pytest.raises(ValueError):
        dvd6 = DVDateTime("1:00")

def test_dv_datetime_magnitude():
    assert DVDateTime("0001-01-01T10:00:00+01:00").magnitude() == 32400.0
    assert DVDateTime("0001-01-21T10:00:00Z").magnitude() == 1764000.0


def test_dv_datetime_add():
    assert (DVDateTime("2025-01-01T03:00:00") + DVDuration("PT2H")).is_equal(DVDateTime("2025-01-01T05:00:00"))
    assert (DVDateTime("2025-01-01T01:00:00") + DVDuration("P1D")).is_equal(DVDateTime("2025-01-02T01:00:00"))

    # check accuracies
    dvt1 = DVDateTime("2025-01-01T01:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVDuration("PT2H", accuracy=60.0, accuracy_is_percent=False)
    assert (dvt1 + dvt2).accuracy.is_equal(DVDuration("PT90S"))

def test_dv_datetime_subtract():
    assert (DVDateTime("2025-01-01T03:00:00") - DVDuration("PT2H")) == DVDateTime("2025-01-01T01:00:00")
    assert (DVDateTime("2025-01-02T01:00:00") - DVDuration("P1D")) == DVDateTime("2025-01-01T01:00:00")

    # check accuracies
    dvt1 = DVDateTime("2025-01-01T03:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVDuration("PT2H", accuracy=60.0, accuracy_is_percent=False)
    assert (dvt1 - dvt2).accuracy.is_equal(DVDuration("PT90S"))

def test_dv_datetime_diff():
    assert (DVDateTime("2025-01-01T03:00:00") - DVDateTime("2025-01-01T02:00:00")).is_equal(DVDuration("PT3600S"))
    assert (DVDateTime("2025-01-01T01:00:00") - DVDateTime("2025-01-01T01:00:00")).is_equal(DVDuration("PT0S"))

    # check accuracies
    dvt1 = DVDateTime("2025-01-01T03:00:00", accuracy=DVDuration("PT30S"))
    dvt2 = DVDateTime("2025-01-01T01:00:00", accuracy=DVDuration("PT60S"))
    assert (dvt1 - dvt2).accuracy == 90.0

def test_dv_datetime_has_iso_datetime_methods():
    dvdt = DVDateTime("2025-01-01T03:00:00.128-01:30")
    assert dvdt.year() == 2025
    assert dvdt.month() == 1
    assert dvdt.day() == 1
    assert dvdt.hour() == 3
    assert dvdt.minute() == 0
    assert dvdt.second() == 0
    assert dvdt.fractional_second() > 0.12
    assert dvdt.timezone().value == "-01:30"
    assert dvdt.minute_unknown() == False
    assert dvdt.second_unknown() == False
    assert dvdt.is_decimal_sign_comma() == False
    assert dvdt.is_partial() == False
    assert dvdt.is_extended() == True
    assert dvdt.has_fractional_second() == True
    assert dvdt.as_string() == "2025-01-01T03:00:00.128-01:30"