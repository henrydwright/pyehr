import pytest

from pyehr.core.am.aom14.archetype.constraint_model.primitive import CDate
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