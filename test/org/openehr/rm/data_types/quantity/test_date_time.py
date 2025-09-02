import pytest

from org.openehr.rm.data_types.quantity.date_time import DVDuration, DVDate
from org.openehr.rm.data_types.quantity import DVAmount
from org.openehr.base.foundation_types.time import ISODuration

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

def test_dv_date_subtract():
    dvd1 = DVDate("2025-09-02")
    dvdr = dvd1 - DVDuration("-P2D")
    assert dvdr.value == "2025-09-04"

    dvd2 = DVDate("2020-01-20")
    dvdr = dvd2 - DVDuration("P5D")
    assert dvdr.value == "2020-01-15"

def test_dv_date_diff():
    dvdr = DVDate("2025-09-02") - DVDate("0001-01-01")
    assert dvdr.value == "P739495D"

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