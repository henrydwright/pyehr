import pytest

from pyehr.core.am.aom14.archetype.constraint_model.primitive import CDate, CDateTime
from pyehr.core.base.base_types.definitions import ValidityKind

def test_c_date_month_validity_disallowed():
    # not OK
    with pytest.raises(ValueError):
        d = CDate(ValidityKind.PROHIBITED, ValidityKind.MANDATORY)
    with pytest.raises(ValueError):
        d = CDate(ValidityKind.PROHIBITED, ValidityKind.OPTIONAL)
    # OK
    d = CDate(ValidityKind.PROHIBITED, ValidityKind.PROHIBITED)

def test_c_date_month_validity_optional():
    # not OK
    with pytest.raises(ValueError):
        d = CDate(ValidityKind.OPTIONAL, ValidityKind.MANDATORY)
    # OK
    d = CDate(ValidityKind.OPTIONAL, ValidityKind.PROHIBITED) 

def test_c_date_time_validity_chains():
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.OPTIONAL, None)
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.MANDATORY, ValidityKind.MANDATORY, None)
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.OPTIONAL, None)
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.OPTIONAL, None)


def test_c_date_time_disallowed_invariant():
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.OPTIONAL, ValidityKind.PROHIBITED, ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.MANDATORY)
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.MANDATORY, ValidityKind.PROHIBITED, ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.MANDATORY)


def test_c_date_time_optional_invariant():
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.OPTIONAL, ValidityKind.OPTIONAL, ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.MANDATORY)
    with pytest.raises(ValueError):
        CDateTime(ValidityKind.MANDATORY, ValidityKind.OPTIONAL, ValidityKind.MANDATORY, ValidityKind.MANDATORY, ValidityKind.MANDATORY)
    # OK
    CDateTime(ValidityKind.OPTIONAL, ValidityKind.OPTIONAL, ValidityKind.OPTIONAL, ValidityKind.OPTIONAL, ValidityKind.OPTIONAL)
    CDateTime(ValidityKind.OPTIONAL, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED)
