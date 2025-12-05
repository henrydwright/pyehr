import numpy as np
import pytest

from pyehr.core.base.foundation_types.interval import ProperInterval, PointInterval, MultiplicityInterval, Cardinality

def _get_bounded_proper_interval():
    i = ProperInterval()
    i.upper = np.int32(10)
    i.lower = np.int32(-10)
    return i

def _get_lower_unbounded_proper_interval():
    i = ProperInterval()
    i.upper = np.int32(10)
    i.upper_included = True
    return i

# test invariants on https://specifications.openehr.org/releases/BASE/Release-1.2.0/foundation_types.html#_interval
def test_new_proper_interval_satisfies_invariants():
    i = ProperInterval[str]()
    assert i.lower_unbounded == True and i.lower_included == False
    assert i.upper_unbounded == True and i.upper_included == False

def test_proper_interval_lower_included_valid():
    i = _get_lower_unbounded_proper_interval()
    assert i.lower_unbounded == True
    assert i.lower_included == False

def test_proper_interval_lower_included_invalid_raises_error():
    with pytest.raises(ValueError):
        i = ProperInterval()
        assert i.lower_unbounded == True
        i.lower_included = True

def test_proper_interval_upper_included_invalid_raises_error():
    with pytest.raises(ValueError):
        i = ProperInterval()
        assert i.upper_unbounded == True
        i.upper_included = True

def test_proper_interval_limits_consistent_invalid_raises_error():
    with pytest.raises(ValueError):
        i = ProperInterval()
        i.upper = np.int32(10)
        i.lower = np.int32(20)

    with pytest.raises(ValueError):
        i = ProperInterval()
        i.lower = np.int32(10)
        i.upper = np.int32(-10)

def test_proper_interval_limits_comparable_invalid_raises_error():
    with pytest.raises(TypeError):
        i = ProperInterval()
        i.lower = np.int32(10)
        i.upper = "hello"

    with pytest.raises(TypeError):
        i = ProperInterval()
        i.upper = np.int64(1023)
        i.lower = np.int32(-2)

def test_proper_interval_limits_consistent_valid_setup():
    i = _get_bounded_proper_interval()
    assert i.upper_unbounded == False
    assert i.lower_unbounded == False
    assert i.lower <= i.upper

def test_proper_interval_has_both_bounds_defined():
    a = ProperInterval()
    a.lower = np.int32(6)
    a.lower_included = True
    a.upper = np.int32(10)
    a.upper_included = False

    assert not a.has(np.int32(11))
    assert not a.has(np.int32(10))
    assert not a.has(np.int32(5))
    assert a.has(np.int32(6))
    assert a.has(np.int32(8))

def test_proper_interval_one_bound_defined():
    a = ProperInterval()
    a.lower = np.int32(6)
    a.lower_included = True
    assert a.has(np.int32(6))
    assert a.has(np.int32(2000))
    assert not a.has(np.int32(5))
    assert not a.has(np.int32(-1000))

    a.lower = None
    a.upper = np.int32(6)
    assert a.has(-2000)
    assert a.has(5)
    assert not a.has(6)
    assert not a.has(2000)

def test_proper_interval_inv_not_point():
    i = ProperInterval[str]()
    i.upper = "c"
    i.lower = "a"
    # should be OK
    with pytest.raises(ValueError):
        i.upper = "a"

def test_point_interval_default_attributes():
    i = PointInterval[np.int32](np.int32(0))
    assert not i.lower_unbounded
    assert not i.upper_unbounded
    assert i.lower_included
    assert i.upper_included

def test_point_interval_inv_point_consistent():
    i = PointInterval[np.int32](np.int32(0))
    i.lower = np.int32(10)
    assert i.lower == i.upper
    i.upper = np.int32(32)
    assert i.lower == i.upper

def test_point_interval_has_only_under_equality():
    a = PointInterval[np.int32](np.int32(20))
    assert not a.has(np.int32(234))
    assert not a.has(np.int32(21))
    a.lower_included = False
    a.upper_included = False
    assert not a.has(np.int32(20))
    a.lower_included = True
    assert a.has(np.int32(20))

def test_multiplicity_interval_only_accepts_integers():
    i = MultiplicityInterval()
    with pytest.raises(TypeError):
        i.lower = "ababac"
    with pytest.raises(TypeError):
        i.lower = np.int64(2344444)
    with pytest.raises(TypeError):
        i.lower = np.uint32(222)
    i.lower = None
    i.lower = np.int32(0)

def test_multiplicity_interval_is_open():
    i = MultiplicityInterval()
    i.lower = np.int32(0)
    i.lower_included = True
    assert i.is_open()
    assert i.has(0)
    assert i.has(2000)
    i.upper = np.int32(3)
    assert not i.is_open()

def test_multiplicity_interval_is_optional():
    i = MultiplicityInterval()
    i.lower = np.int32(0)
    i.upper = np.int32(1)
    i.lower_included = True
    i.upper_included = True
    assert i.is_optional()
    assert i.has(0)
    assert i.has(1)
    assert not i.has(2)
    i.lower_included = False
    assert not i.is_optional()

def test_multiplicity_interval_is_mandatory():
    i = MultiplicityInterval()
    i.lower = np.int32(0)
    i.upper = np.int32(1)
    i.lower_included = False
    i.upper_included = True
    assert i.is_mandatory()
    assert not i.has(np.int32(0))
    assert i.has(np.int32(1))
    assert not i.has(np.int32(2))
    i.lower_included = True
    assert not i.is_mandatory()

def test_multiplicity_interval_is_prohibited():
    i = MultiplicityInterval()
    i.lower = np.int32(0)
    i.upper = np.int32(1)
    i.lower_included = True
    i.upper_included = False
    assert i.is_prohibited()
    assert not i.has(np.int32(2))
    assert i.has(np.int32(0))
    i.upper_included = True
    assert not i.is_prohibited()

def test_interval_intersects():
    # overlap
    a = ProperInterval()
    a.lower = 10
    a.upper = 20
    b = ProperInterval()
    b.lower = 15
    b.upper = 25
    assert a.intersects(b)
    assert b.intersects(a)
    # no intersection
    b.upper = 50
    b.lower = 40
    assert not a.intersects(b)
    assert not b.intersects(a)
    # intersection only on included bounds
    b.lower = 20
    b.lower_included = True
    a.upper_included = True
    assert a.intersects(b)
    assert b.intersects(a)
    # no intersection only on not included bounds
    a.upper_included = False
    assert not a.intersects(b)
    assert not b.intersects(a)

def test_interval_contains():
    # one way, but not other
    a = ProperInterval()
    a.lower = -10
    a.upper = 10
    b = ProperInterval()
    b.lower = -20
    b.upper = 20
    assert b.contains(a)
    assert not a.contains(b)
    # no containing relationship
    b.upper = -15
    assert not b.contains(a)
    assert not a.contains(b)

def test_cardinality_is_bag():
    c = Cardinality(False, False, MultiplicityInterval())
    assert c.is_bag()
    c.is_unique = True
    assert not c.is_bag()

def test_cardinality_is_list():
    c = Cardinality(True, False, MultiplicityInterval())
    assert c.is_list()
    c.is_ordered = False
    assert not c.is_list()

def test_cardinality_is_set():
    c = Cardinality(False, True, MultiplicityInterval())
    assert c.is_set()
    c.is_unique = False
    assert not c.is_set()