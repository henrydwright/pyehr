import pytest

from org.openehr.rm.data_types.quantity.date_time import DVDuration
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