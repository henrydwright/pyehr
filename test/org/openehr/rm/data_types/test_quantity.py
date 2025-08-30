import pytest

from org.openehr.base.foundation_types.interval import ProperInterval
from org.openehr.rm.data_types.text import CodePhrase, DVCodedText, DVText
from org.openehr.rm.data_types.quantity import DVOrdered, DVInterval, ReferenceRange, DVOrdinal, DVScale, DVQuantified, DVAmount
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

def test_dv_quantified_accuracy_unknown():
    dvq = _TstDVQuantifiedImpl(5.0)
    assert dvq.accuracy_unknown() == True
    dvq = _TstDVQuantifiedImpl(5.0, accuracy=0.1)
    assert dvq.accuracy_unknown() == False

# source for accuracy combinations: https://www.savemyexams.com/a-level/physics/aqa/17/revision-notes/1-measurements-and-their-errors/1-2-limitation-of-physical-measurements/1-2-2-calculating-uncertainties/

def test_dv_amount_addition_accuracy_correct():
    # no accuracies
    dva1 = DVAmount(5)
    dva2 = DVAmount(6)
    dvar = dva1 + dva2
    assert dvar.value == 11
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on one operand only
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(5)
    dvar = dva1 + dva2
    assert dvar.value == 10
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on both, both absolutes
    dva1 = DVAmount(6, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(6, accuracy=1.0, accuracy_is_percent=False)
    dvar = dva1 + dva2
    assert dvar.value == 12
    assert dvar.accuracy_is_percent == False
    assert dvar.accuracy <= 3.00000001 and dvar.accuracy >= 2.99999999

    # accuracy on both, both percentages
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(50, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 + dva2
    assert dvar.value == 150
    assert dvar.accuracy_is_percent == True
    # abs_accuracy = (100 * 0.1 + 50 * 0.05) = 12.5
    # perc_accuracy = 12.5 / 150.0 = 8.3333333...%
    assert dvar.accuracy <= 8.334 and dvar.accuracy >= 8.332

    # accuracy on both, larger is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=False)
    dvar = dva1 + dva2
    assert dvar.value == 180
    assert dvar.accuracy_is_percent == True
    # abs_accuracy = (100 * 0.1 + 5) = 15
    # perc_accuracy = 15 / 180 = 8.3333333...%
    assert dvar.accuracy <= 8.334 and dvar.accuracy >= 8.332

    # accuracy on both, smaller is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=False)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 + dva2
    assert dvar.value == 180
    assert dvar.accuracy_is_percent == False
    # abs_accuracy = (80 * 0.05 + 10) = 14
    assert dvar.accuracy <= 14.001 and dvar.accuracy >= 13.999

def test_dv_amount_subtract_accuracy_correct():
    # no accuracies
    dva1 = DVAmount(5)
    dva2 = DVAmount(6)
    dvar = dva1 - dva2
    assert dvar.value == -1
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on one operand only
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(5)
    dvar = dva1 - dva2
    assert dvar.value == 0
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on both, both absolutes
    dva1 = DVAmount(6, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(6, accuracy=1.0, accuracy_is_percent=False)
    dvar = dva1 - dva2
    assert dvar.value == 0
    assert dvar.accuracy_is_percent == False
    assert dvar.accuracy <= 3.00000001 and dvar.accuracy >= 2.99999999

    # accuracy on both, both percentages
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(50, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 - dva2
    assert dvar.value == 50
    assert dvar.accuracy_is_percent == True
    # abs_accuracy = (100 * 0.1 + 50 * 0.05) = 12.5
    # perc_accuracy = 12.5 / 50.0 = 25%
    assert dvar.accuracy <= 25.001 and dvar.accuracy >= 24.999

    # accuracy on both, larger is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=False)
    dvar = dva1 - dva2
    assert dvar.value == 20
    assert dvar.accuracy_is_percent == True
    # abs_accuracy = (100 * 0.1 + 5) = 15
    # perc_accuracy = 15 / 20 = 75%
    assert dvar.accuracy <= 75.001 and dvar.accuracy >= 74.999

    # accuracy on both, smaller is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=False)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 - dva2
    assert dvar.value == 20
    assert dvar.accuracy_is_percent == False
    # abs_accuracy = (80 * 0.05 + 10) = 14
    assert dvar.accuracy <= 14.001 and dvar.accuracy >= 13.999

def test_dv_amount_negation_works():
    dva = DVAmount(-100)
    dvar = -dva
    assert dvar.value == 100

def test_dv_amount_multiply_accuracy_correct():
    # no accuracies
    dva1 = DVAmount(5)
    dva2 = DVAmount(6)
    dvar = dva1 * dva2
    assert dvar.value == 30
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on one operand only
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(5)
    dvar = dva1 * dva2
    assert dvar.value == 25
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on both, both absolutes
    dva1 = DVAmount(6, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(6, accuracy=1.0, accuracy_is_percent=False)
    dvar = dva1 * dva2
    assert dvar.value == 36
    assert dvar.accuracy_is_percent == False
    # perc_accuracy = (2/6 + 1/6) = 50%
    # abs_accuracy = 0.5 * 36 = 18
    assert dvar.accuracy <= 18.001 and dvar.accuracy >= 17.999

    # accuracy on both, both percentages
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(50, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 * dva2
    assert dvar.value == 5000
    assert dvar.accuracy_is_percent == True
    # perc_accuracy = 10 + 5 = 15%
    assert dvar.accuracy <= 15.001 and dvar.accuracy >= 14.999

    # accuracy on both, larger is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=False)
    dvar = dva1 * dva2
    assert dvar.value == 8000
    assert dvar.accuracy_is_percent == True
    # perc_accuracy = 0.1 + 5/80 = 16.25%
    assert dvar.accuracy <= 16.251 and dvar.accuracy >= 16.249

    # accuracy on both, smaller is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=False)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 * dva2
    assert dvar.value == 8000
    assert dvar.accuracy_is_percent == False
    # perc_accuracy = 0.05 + 0.1 = 15%
    # abs_accuracy = 0.15 * 8000 = 1200
    assert dvar.accuracy <= 1200.001 and dvar.accuracy >= 1199.999

def test_dv_amount_divide_accuracy_correct():
    # no accuracies
    dva1 = DVAmount(5)
    dva2 = DVAmount(6)
    dvar = dva1 / dva2
    assert dvar.value <= 0.8334 and dvar.value >= 0.8332
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on one operand only
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(5)
    dvar = dva1 / dva2
    assert dvar.value == 1
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy on both, both absolutes
    dva1 = DVAmount(6, accuracy=2.0, accuracy_is_percent=False)
    dva2 = DVAmount(6, accuracy=1.0, accuracy_is_percent=False)
    dvar = dva1 / dva2
    assert dvar.value == 1
    assert dvar.accuracy_is_percent == False
    # perc_accuracy = (2/6 + 1/6) = 50%
    # abs_accuracy = 0.5 * 1 = 0.5
    assert dvar.accuracy <= 0.501 and dvar.accuracy >= 0.499

    # accuracy on both, both percentages
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(50, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 / dva2
    assert dvar.value == 2
    assert dvar.accuracy_is_percent == True
    # perc_accuracy = 10 + 5 = 15%
    assert dvar.accuracy <= 15.001 and dvar.accuracy >= 14.999

    # accuracy on both, larger is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=True)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=False)
    dvar = dva1 / dva2
    assert dvar.value <= 1.2501 and dvar.value >= 1.2499
    assert dvar.accuracy_is_percent == True
    # perc_accuracy = 0.1 + 5/80 = 16.25%
    assert dvar.accuracy <= 16.251 and dvar.accuracy >= 16.249

    # accuracy on both, smaller is percent
    dva1 = DVAmount(100, accuracy=10.0, accuracy_is_percent=False)
    dva2 = DVAmount(80, accuracy=5.0, accuracy_is_percent=True)
    dvar = dva1 / dva2
    assert dvar.value <= 1.2501 and dvar.value >= 1.2499
    assert dvar.accuracy_is_percent == False
    # perc_accuracy = 0.05 + 0.1 = 15%
    # abs_accuracy = 0.15 * 1.25 = 0.1875
    assert dvar.accuracy <= 0.187501 and dvar.accuracy >= 0.187499

def test_dv_amount_accuracy_is_percent_validity():
    # OK
    dva = DVAmount(5, accuracy=0.0, accuracy_is_percent=False)
    # not OK
    with pytest.raises(ValueError):
        dva = DVAmount(5, accuracy=0.0, accuracy_is_percent=True)

def test_dv_amount_accuracy_validity():
    # OK
    dva = DVAmount(900, accuracy=10.0, accuracy_is_percent=True)
    # not OK
    with pytest.raises(ValueError):
        dva = DVAmount(900, accuracy=-10.0, accuracy_is_percent=True)
    
    with pytest.raises(ValueError):
        dva = DVAmount(900, accuracy=100.5, accuracy_is_percent=True)