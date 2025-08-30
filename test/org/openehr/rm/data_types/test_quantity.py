import pytest

from org.openehr.base.foundation_types.interval import ProperInterval
from org.openehr.rm.data_types.text import CodePhrase, DVCodedText, DVText
from org.openehr.rm.data_types.quantity import DVOrdered, DVInterval, ReferenceRange, DVOrdinal, DVScale, DVQuantified
from org.openehr.base.base_types.identification import TerminologyID
from common import PythonTerminologyService, CODESET_OPENEHR_NORMAL_STATUSES

test_ts = PythonTerminologyService([CODESET_OPENEHR_NORMAL_STATUSES], [])
test_ts_empty = PythonTerminologyService([], [])

class _TstDVOrderedImpl(DVOrdered):
    def __init__(self, value, normal_status = None, normal_range = None, other_reference_ranges = None, terminology_service = None):
        super().__init__(value, normal_status, normal_range, other_reference_ranges, terminology_service)

    def is_strictly_comparable_to(self, other):
        return super().is_strictly_comparable_to(other)
    
class _TstDVQuantifiedImpl(DVQuantified):
    def __init__(self, value, normal_status=None, normal_range=None, other_reference_ranges=None, magnitude_status=None, accuracy=None, terminology_service=None):
        super().__init__(value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, terminology_service)
    
    def is_strictly_comparable_to(self, other):
        return super().is_strictly_comparable_to(other)

def test_other_reference_ranges_validity():
    # OK
    dvo = _TstDVOrderedImpl(4, other_reference_ranges=[ReferenceRange(DVText("theraputic"), DVInterval(lower=_TstDVOrderedImpl(3), upper=_TstDVOrderedImpl(5)))])
    # not OK
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, other_reference_ranges=[])

def test_is_simple_validity():
    dvo = _TstDVOrderedImpl(4, other_reference_ranges=[ReferenceRange(DVText("theraputic"), DVInterval(lower=_TstDVOrderedImpl(3), upper=_TstDVOrderedImpl(5)))])
    assert dvo.is_simple() == False

    dvo = _TstDVOrderedImpl(4, normal_range=DVInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5)))
    assert dvo.is_simple() == False

    dvo = _TstDVOrderedImpl(4)
    assert dvo.is_simple() == True

def test_normal_status_validity():
    # should be OK
    dvo = _TstDVOrderedImpl(4)
    dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), terminology_service=test_ts)

    # not OK (missing terminology service)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"))

    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), terminology_service=test_ts_empty)

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "NORMAL"), terminology_service=test_ts)

def test_normal_range_and_status_consistency():
    # should be OK
    dvo = _TstDVOrderedImpl(4)
    dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), terminology_service=test_ts)
    dvo = _TstDVOrderedImpl(4, normal_range=DVInterval(ProperInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5))))
    dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), normal_range=DVInterval(ProperInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5))), terminology_service=test_ts)
    dvo = _TstDVOrderedImpl(1, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "L"), normal_range=DVInterval(ProperInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5))), terminology_service=test_ts)

    # not OK (mismatch between status and range - status = normal, range = too low)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), normal_range=DVInterval(lower=_TstDVOrderedImpl(10), upper=_TstDVOrderedImpl(20)), terminology_service=test_ts)

    # not OK (mismatch between status and range - status = normal, range = too high)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), normal_range=DVInterval(lower=_TstDVOrderedImpl(1), upper=_TstDVOrderedImpl(2)), terminology_service=test_ts)

    # not OK (mismatch between status and range - status = high, range = normal)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "H"), normal_range=DVInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5)), terminology_service=test_ts)

    # not OK (mismatch between status and range - status = critically low, range = normal)
    with pytest.raises(ValueError):
        dvo = _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "LLL"), normal_range=DVInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5)), terminology_service=test_ts)

def test_is_normal():
    assert _TstDVOrderedImpl(4).is_normal() is None
    assert _TstDVOrderedImpl(4, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "N"), terminology_service=test_ts).is_normal() == True
    assert _TstDVOrderedImpl(4, normal_range=DVInterval(lower=_TstDVOrderedImpl(2), upper=_TstDVOrderedImpl(5))).is_normal() == True
    assert _TstDVOrderedImpl(1, normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "L"), terminology_service=test_ts).is_normal() == False
    assert _TstDVOrderedImpl(4, normal_range=DVInterval(lower=_TstDVOrderedImpl(1), upper=_TstDVOrderedImpl(3))).is_normal() == False

def test_reference_range_range_is_simple():
    # OK
    r = ReferenceRange(DVText("test"), DVInterval())
    r = ReferenceRange(DVText("test"), DVInterval(lower=_TstDVOrderedImpl(1.0)))
    r = ReferenceRange(DVText("test"), DVInterval(upper=_TstDVOrderedImpl(2.0)))
    r = ReferenceRange(DVText("test"), DVInterval(lower=_TstDVOrderedImpl(1.0), upper=_TstDVOrderedImpl(2.0)))
    # Not OK (non simple lower bound)
    with pytest.raises(ValueError):
        r = ReferenceRange(DVText("test"), DVInterval(lower=_TstDVOrderedImpl(1.0, normal_range=DVInterval(upper=_TstDVOrderedImpl(5.0)))))
    # Not OK (non simple upper bound)
    with pytest.raises(ValueError):
        r = ReferenceRange(DVText("test"), DVInterval(upper=_TstDVOrderedImpl(5.0, normal_range=DVInterval(upper=_TstDVOrderedImpl(6.0)))))
    
def test_dv_ordinal_only_integers_accepted():
    # OK
    dvo = DVOrdinal(1, DVCodedText("Moderate amount of hemolyzed blood detected in urine by dipstick (finding)", CodePhrase(TerminologyID("SNOMED-CT"), "1348318004")))
    # Not OK
    with pytest.raises(TypeError):
        dvo = DVOrdinal("Moderate", DVCodedText("Moderate amount of hemolyzed blood detected in urine by dipstick (finding)", CodePhrase(TerminologyID("SNOMED-CT"), "1348318004")))

def test_dv_scale_only_reals_accepted():
    # OK
    dvs = DVScale(0.5, DVCodedText("Borg Breathlessness Score: 0.5 very, very slight (just noticeable) (finding)", CodePhrase(TerminologyID("SNOMED-CT"), "401323002")))
    dvs = DVScale(10.0, DVCodedText("Borg Breathlessness Score: 10 maximal (finding)", CodePhrase(TerminologyID("SNOMED-CT"), "401293009")))
    # Not OK
    with pytest.raises(TypeError):
        dvs = DVScale(10, DVCodedText("Borg Breathlessness Score: 10 maximal (finding)", CodePhrase(TerminologyID("SNOMED-CT"), "401293009")))

def test_dv_quantified_valid_magnitude_status_correct():
    valid_statues = {"=", "<", ">", "<=", ">=", "~"}
    for status in valid_statues:
        assert DVQuantified.valid_magnitude_status(status) == True
    assert DVQuantified.valid_magnitude_status("!=") == False
    assert DVQuantified.valid_magnitude_status("ABACUS") == False

def test_dv_quantified_magnitude_status_valid():
    # OK
    dvq = _TstDVQuantifiedImpl(5.0, magnitude_status=DVQuantified.MagnitudeStatus.APPROXIMATE_VALUE)
    # not OK
    with pytest.raises(ValueError):
        dvq = _TstDVQuantifiedImpl(5.0, magnitude_status="ABABABA")