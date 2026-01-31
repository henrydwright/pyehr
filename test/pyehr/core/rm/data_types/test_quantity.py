import pytest

from pyehr.core.base.foundation_types.interval import ProperInterval
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.data_types.quantity import DVOrdered, DVInterval, ReferenceRange, DVOrdinal, DVScale, DVQuantified, DVAmount, DVQuantity, DVCount, ProportionKind, DVProportion, DVAbsoluteQuantity
from pyehr.core.base.base_types.identification import TerminologyID
from term import PythonTerminologyService, CODESET_OPENEHR_NORMAL_STATUSES

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
    
class _TstDVAbsoluteQuantityImpl(DVAbsoluteQuantity):
    def __init__(self, value, normal_status = None, normal_range = None, other_reference_ranges = None, magnitude_status = None, accuracy = None, terminology_service = None):
        super().__init__(value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, terminology_service)

    def __add__(self, other):
        return super().__add__(other)
    
    def __sub__(self, other):
        return super().__sub__(other)
    
    def diff(self, other):
        return super().diff(other)
    
    def subtract(self, a_diff):
        return super().subtract(a_diff)

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
    # no accuracies (maintained)
    dva1 = DVAmount(5)
    dvar = dva1 * 6.0
    dva2 = DVAmount(6)
    dvar = 5.0 * dva2
    assert dvar.value == 30
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy (maintained)
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dvar = dva1 * 5.0
    assert dvar.value == 25
    assert dvar.accuracy_is_percent is False
    assert dvar.accuracy == 2.0

def test_dv_amount_divide_accuracy_correct():
    # no accuracy (maintained)
    dva1 = DVAmount(5)
    dvar = dva1 / 6.0
    assert dvar.value <= 0.8334 and dvar.value >= 0.8332
    assert dvar.accuracy_is_percent is None
    assert dvar.accuracy is None

    # accuracy (maintained)
    dva1 = DVAmount(5, accuracy=2.0, accuracy_is_percent=False)
    dvar = dva1 / 5.0
    assert dvar.value <= 1.001 and dvar.value >= 0.999
    assert dvar.accuracy_is_percent == False
    assert dvar.accuracy == 2.0

def test_dv_amount_rdivide_not_possible():
    # reasoning - if you do x / quantity the units might change
    dva = DVAmount(6)
    with pytest.raises(TypeError):
        dvar = 5.0 / dva

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

def test_dv_quantity_numeric_operation_checks_units_and_units_system():
    # OK
    dvq1 = DVQuantity(5.0, "m")
    dvq2 = DVQuantity(6.0, "m")
    dvqr = dvq1 + dvq2
    assert dvqr.units == "m"

    dvq1 = DVQuantity(6.0, "258669008", "http://snomed.info/sct", "meter(s)")
    dvq2 = DVQuantity(7.0, "258669008", "http://snomed.info/sct", "meter")
    dvqr = dvq2 - dvq1
    assert dvqr.units == "258669008"
    assert dvqr.units_system == "http://snomed.info/sct"
    assert dvqr.units_display_name == "meter"

    # maintains with mult/div
    dvq = DVQuantity(5.0, "m")
    dvqr = dvq / 5.0
    assert dvqr.units == "m"
    dvqr = dvq * 5.0
    assert dvqr.units == "m"

    dvq1 = DVQuantity(5.0, "m")
    dvq2 = DVQuantity(6.0, "kg")
    # not OK
    with pytest.raises(ValueError):
        dvqr = dvq1 + dvq2
    with pytest.raises(ValueError):
        dvqr = dvq1 - dvq2

    dvq1 = DVQuantity(6.0, "258669008", "http://snomed.info/sct", "meter(s)")
    dvq2 = DVQuantity(7.0, "m")
    # not OK
    with pytest.raises(ValueError):
        dvqr = dvq1 + dvq2
    with pytest.raises(ValueError):
        dvqr = dvq1 - dvq2

def test_dv_quantity_addsub_precision_correct():
    # custom is that precision is bounded by lowest precision
    # both have precision
    dvq1 = DVQuantity(5.25, "m", precision=2)
    dvq2 = DVQuantity(5.0, "m", precision=0)
    dvqr = dvq1 + dvq2
    assert dvqr.precision == 0

    # both have precision, one is unlimited
    dvq1 = DVQuantity(5.25, "m", precision=2)
    dvq2 = DVQuantity(5.0, "m", precision=-1)
    dvqr = dvq1 - dvq2
    assert dvqr.precision == 2

    # only one has precision
    dvq1 = DVQuantity(5.25, "m", precision=2)
    dvq2 = DVQuantity(5.0, "m")
    dvqr = dvq1 + dvq2
    assert dvqr.precision is None

    # neither have precision
    dvq1 = DVQuantity(5.25, "m")
    dvq2 = DVQuantity(5.0, "m")
    dvqr = dvq1 - dvq2
    assert dvqr.precision is None

def test_dv_quantity_muldiv_precision_correct():
    dvq = DVQuantity(5.25, "m", precision=2)
    dvqr = dvq * 5.0
    assert dvqr.precision == 2

    dvq = DVQuantity(5.0, "m", precision=-1)
    dvqr = dvq / 5.0
    assert dvqr.precision == -1

def test_dv_quantity_normal_range_is_quantities():
    # OK
    dvq = DVQuantity(9.0, "m", normal_range=DVInterval(lower=DVQuantity(8.0, "m"), upper=DVQuantity(10.0, "m")))
    # Not OK
    with pytest.raises(TypeError):
        dvq = DVQuantity(9.0, "m", normal_range=DVInterval(lower=_TstDVQuantifiedImpl(2.0), upper=_TstDVQuantifiedImpl(10.0)))

def test_dv_count_integer_only():
    # OK
    dvc = DVCount(6)
    # not OK
    with pytest.raises(TypeError):
        dvc = DVCount(7.1)

def test_proportion_kind_valid_proportion_kind():
    assert ProportionKind.valid_proportion_kind(5) == False
    for val in {0, 1, 2, 3, 4}:
        assert ProportionKind.valid_proportion_kind(val) == True

def test_dv_proportion_precision_validity():
    dvp = DVProportion(5.0, 100.0, ProportionKind.PK_PERCENT, 0)
    assert dvp.is_integral() == True

def test_dv_proportion_is_integral_validity():
    # OK
    dvp = DVProportion(1.0, 8.0, ProportionKind.PK_FRACTION, 0)
    dvp = DVProportion(1.0, 8.5, ProportionKind.PK_RATIO, 1)
    # not OK
    with pytest.raises(ValueError):
        dvp = DVProportion(1.0, 8.5, ProportionKind.PK_RATIO, 0)

def test_dv_proportion_fraction_validity():
    # OK
    dvp = DVProportion(1.0, 2.0, ProportionKind.PK_FRACTION, 0)
    dvp = DVProportion(7.0, 3.0, ProportionKind.PK_INTEGER_FRACTION, 0)
    # not OK
    with pytest.raises(ValueError):
        dvp = DVProportion(1.0, 2.5, ProportionKind.PK_FRACTION, 1)
    with pytest.raises(ValueError):
        dvp = DVProportion(7.0, 3.5, ProportionKind.PK_INTEGER_FRACTION, 1)

def test_dv_proportion_unitary_validity():
    # OK
    dvp = DVProportion(48.9, 1.0, ProportionKind.PK_UNITARY)
    # not OK
    with pytest.raises(ValueError):
        dvp = DVProportion(48.9, 1.5, ProportionKind.PK_UNITARY)
    
def test_dv_proportion_percent_validity():
    # OK
    dvp = DVProportion(69.0, 100.0, ProportionKind.PK_PERCENT)
    # not OK
    with pytest.raises(ValueError):
        dvp = DVProportion(69.0, 100.5, ProportionKind.PK_PERCENT)

def test_dv_proportion_valid_denominator():
    # not OK
    with pytest.raises(ValueError):
        dvp = DVProportion(100.0, 0.0, ProportionKind.PK_RATIO)

def test_dv_proportion_addition_correct():
    # percentages
    dvp1 = DVProportion(20.0, 100.0, ProportionKind.PK_PERCENT)
    dvp2 = DVProportion(30.0, 100.0, ProportionKind.PK_PERCENT)
    dvpr = dvp1 + dvp2
    assert dvpr.numerator <= 50.001 and dvpr.numerator > 49.999
    assert dvpr.proportion_type == ProportionKind.PK_PERCENT

    # fractions
    dvp1 = DVProportion(2.0, 8.0, ProportionKind.PK_FRACTION, 0)
    dvp2 = DVProportion(1.0, 16.0, ProportionKind.PK_FRACTION, 0)
    dvpr = dvp1 + dvp2
    assert dvpr.denominator <= 16.001 and dvpr.denominator >= 15.999
    assert dvpr.numerator <= 5.001 and dvpr.numerator >= 4.999
    assert dvpr.proportion_type == ProportionKind.PK_FRACTION

def test_dv_proportion_addition_checks_strictly_comparable():
    # OK
    dvp1 = DVProportion(128.0, 1.0, ProportionKind.PK_UNITARY)
    dvp2 = DVProportion(64.0, 1.0, ProportionKind.PK_UNITARY)
    dvpr = dvp1 + dvp2
    assert dvpr.numerator <= 192.001 and dvpr.numerator >= 191.999

    # not OK
    dvp1 = DVProportion(1.0, 2.0, ProportionKind.PK_FRACTION, 0)
    dvp2 = DVProportion(1.0, 2.0, ProportionKind.PK_INTEGER_FRACTION, 0)
    with pytest.raises(ValueError):
        dvpr = dvp1 + dvp2

def test_dv_proportion_multiply_correct():
    dvp1 = DVProportion(1.0, 2.0, ProportionKind.PK_FRACTION, 0)
    dvp2 = DVProportion(1.0, 3.0, ProportionKind.PK_FRACTION, 0)
    dpvr = dvp1 * 5.0
    dvpr = 5.0 * dvp1
    assert dvpr.numerator <= 5.001 and dvpr.numerator >= 4.999
    assert dvpr.denominator == 2.0
    # fraction multiplied by non integral number gives error
    with pytest.raises(ValueError):
        dvpr = 3.5 * dvp1
    # multiplying two proportions gives error
    with pytest.raises(TypeError):
        dvpr = dvp1 * dvp2

def test_dv_proportion_divide_correct():
    dvp1 = DVProportion(20.0, 100.0, ProportionKind.PK_PERCENT)
    dvpr = dvp1 / 4.0
    assert dvpr.numerator <= 5.001 and dvpr.numerator >= 4.999
    assert dvpr.denominator == 100.0

    dvp2 = DVProportion(7.0, 6.0, ProportionKind.PK_INTEGER_FRACTION, 0)
    dvpr = dvp2 / 5.0
    assert dvpr.numerator == 7.0
    assert dvpr.denominator <= 30.001 and dvpr.denominator >= 29.999

    # integral divided by non integral gives error
    dvp3 = DVProportion(30.0, 100.0, ProportionKind.PK_PERCENT, 0)
    with pytest.raises(ValueError):
        dvpr = dvp3 / 5.9

    # proportion divided by proportion gives error
    with pytest.raises(TypeError):
        dvp3 / dvp1

    # number divided by proportion gives error
    with pytest.raises(TypeError):
        5.0 / dvp1

def test_dv_proportion_subtract_correct():
    # percentages
    dvp1 = DVProportion(20.0, 100.0, ProportionKind.PK_PERCENT)
    dvp2 = DVProportion(30.0, 100.0, ProportionKind.PK_PERCENT)
    dvpr = dvp1 - dvp2
    assert dvpr.numerator <= -9.999 and dvpr.numerator > -10.001
    assert dvpr.proportion_type == ProportionKind.PK_PERCENT

    # fractions
    dvp1 = DVProportion(2.0, 8.0, ProportionKind.PK_FRACTION, 0)
    dvp2 = DVProportion(1.0, 16.0, ProportionKind.PK_FRACTION, 0)
    dvpr = dvp1 - dvp2
    assert dvpr.denominator <= 16.001 and dvpr.denominator >= 15.999
    assert dvpr.numerator <= 3.001 and dvpr.numerator >= 2.999
    assert dvpr.proportion_type == ProportionKind.PK_FRACTION

def test_dv_proportion_comparisons_correct():
    dvp1 = DVProportion(1.0, 2.0, ProportionKind.PK_INTEGER_FRACTION, 0) 
    dvp2 = DVProportion(9.0, 4.0, ProportionKind.PK_INTEGER_FRACTION, 0)
    assert dvp1 < dvp2

    dvp1 = DVProportion(20.0, 100.0, ProportionKind.PK_PERCENT)
    dvp2 = DVProportion(29.9, 100.0, ProportionKind.PK_PERCENT)
    assert dvp2 >= dvp1
    assert dvp2 >= dvp2

def test_dv_absolute_quantity_accuracy_redefined():
    # OK
    dvaq = _TstDVAbsoluteQuantityImpl(5.0)
    dvaq = _TstDVAbsoluteQuantityImpl(5.0, accuracy=DVAmount(5))
    # Not OK
    with pytest.raises(TypeError):
        dvaq = _TstDVAbsoluteQuantityImpl(5.0, accuracy=5.0)