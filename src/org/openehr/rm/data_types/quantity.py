"""The data_types.quantity package contains classes for representing different
forms of measured quantity and supporting information for those quantities"""

from abc import abstractmethod
from typing import Optional

import numpy as np

from org.openehr.base.foundation_types.primitive_types import ordered
from org.openehr.base.foundation_types.time import ISOType, ISODate
from org.openehr.base.foundation_types.interval import Interval, ProperInterval, PointInterval
from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.rm.data_types import DataValue
from org.openehr.rm.data_types.text import CodePhrase, DVText
from org.openehr.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_codeset_or_error, OpenEHRCodeSetIdentifiers

# wrapper around an 'ordered' datatype
class DVOrdered(DataValue):
    """Abstract class defining the concept of ordered values, which includes ordinals 
    as well as true quantities. It defines the functions < and is_strictly_comparable_to(), 
    the latter of which must evaluate to True for instances being compared with the < function, 
    or used as limits in the DV_INTERVAL<T> class.

    Data value types which are to be used as limits in the DV_INTERVAL<T> class must inherit from 
    this class, and implement the function is_strictly_comparable_to() to ensure that instances 
    compare meaningfully. For example, instances of DV_QUANTITY can only be compared if they measure 
    the same kind of physical quantity."""

    value: ordered
    """Value of `ordered` type"""

    normal_status: Optional[CodePhrase]
    """Optional normal status indicator of value with respect to normal range for this value. Often 
    included by lab, even if the normal range itself is not included. Coded by ordinals in series 
    HHH, HH, H, (nothing), L, LL, LLL; see openEHR terminology group normal_status."""

    normal_range: Optional['DVInterval']
    """Optional normal range."""

    other_reference_ranges: Optional[list['ReferenceRange']]
    """Optional tagged other reference ranges for this value in its particular measurement context."""

    @abstractmethod
    def __init__(self, value: ordered, normal_status: Optional[CodePhrase] = None, normal_range: Optional['DVInterval'] = None, other_reference_ranges: Optional[list['ReferenceRange']] = None, terminology_service: Optional[TerminologyService] = None):
        """Instantiate new DVOrdered with type conversion from native Python types of 
        float (convered to np.float64) and int (converted to np.integer64)"""

        converted_value = value
        if isinstance(value, int):
            converted_value = np.int64(value)
        if isinstance(value, float):
            converted_value = np.float64(value)
        if not isinstance(converted_value, ordered):
            raise TypeError(f"Value must be of an ordered type, but value of type \'{type(value)}\' was provided")
        self.value = converted_value

        if (normal_status is not None) and (terminology_service is None):
            raise ValueError("If normal_status is provided, a terminology service must be provided to check its validity (invariant: normal_status_validity)")
        if normal_status is not None:
            util_verify_code_in_openehr_codeset_or_error(
                code=normal_status,
                codeset_name=OpenEHRCodeSetIdentifiers.CODE_SET_ID_NORMAL_STATUSES,
                terminology_service=terminology_service,
                invariant_name_for_error="normal_status_validity")
        self.normal_status = normal_status

        self.normal_range = normal_range

        if (other_reference_ranges is not None and len(other_reference_ranges) == 0):
            raise ValueError("other_reference_ranges cannot be an empty list (invariant: other_reference_ranges_validity)")
        self.other_reference_ranges = other_reference_ranges

        super().__init__()

        if (normal_status is not None) and (normal_range is not None):
            if (normal_status.code_string == "N") and (not normal_range.has(self)):
                raise ValueError(f"Normal status was 'N' but value \'{value}\' was not in provided normal range \'{str(normal_range)}\'")
            elif (normal_status.code_string != "N") and (normal_range.has(self)):
                raise ValueError(f"Normal value \'{value}\' was within the normal range \'{str(normal_range)}\' but status was \'{normal_status.code_string}\'")

    def is_equal(self, other: 'DVOrdered'):
        return (type(self) == type(other) and
                self.value == other.value)
    
    @abstractmethod
    def is_strictly_comparable_to(self, other: 'DVOrdered'):
        return not (
            (isinstance(self.value, str) and not isinstance(other.value, str)) or 
            (isinstance(other.value, str) and not isinstance(self.value, str)) or 
            (isinstance(self.value, ISOType) and not isinstance(other.value, ISOType)) or
            (isinstance(other.value, ISOType) and not isinstance(self.value, ISOType))
        )
    
    def _allowed_comparison_check(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"Other type must also be DVOrdered to allow comparison - you provided type \'{type(other)}\' (perhaps you forgot to wrap an ordered value type?)")
        if (not self.is_strictly_comparable_to(other)):
            raise TypeError(f"DVOrdered with value of type \'{type(self.value)}\' is not strictly comparable to DVOrdered with value of type \'{type(other.value)}\'")
        
    def less_than(self, other):
        """True if this Ordered object is less than other. Redefined in descendants."""
        return self < other

    def __lt__(self, other):
        self._allowed_comparison_check(other)
        return self.value < other.value
    
    def __le__(self, other):
        self._allowed_comparison_check(other)
        return self.value <= other.value
    
    def __gt__(self, other):
        self._allowed_comparison_check(other)
        return self.value > other.value
    
    def __ge__(self, other):
        self._allowed_comparison_check(other)
        return self.value >= other.value
    
    def __eq__(self, other):
        return self.is_equal(other)
    
    def is_simple(self) -> bool:
        """True if this quantity has no reference ranges."""
        return ((self.normal_range is None) and (self.other_reference_ranges is None))
    
    def is_normal(self) -> Optional[bool]:
        """Value is in the normal range, determined by comparison of the value to normal_range if present, or by the normal_status marker if present.
        
        Returns `None` if not possible to tell"""
        if self.normal_status is not None:
            return (self.normal_status.code_string == "N")
        elif self.normal_range is not None:
            return self.normal_range.has(self)
        else:
            return None

    def __str__(self):
        return str(self.value)

class DVInterval(DataValue):
    """Generic class defining an interval (i.e. range) of a comparable type. An interval is a 
    contiguous subrange of a comparable base type. Used to define intervals of dates, times, 
    quantities (whose units match) and so on. The type parameter, T, must be a descendant of the 
    type DV_ORDERED, which is necessary (but not sufficient) for instances to be compared 
    (strictly_comparable is also needed).

    Without the DV_INTERVAL class, quite a few more DV_ classes would be needed to express 
    logical intervals, namely interval versions of all the date/time classes, and of quantity 
    classes. Further, it allows the semantics of intervals to be stated in one place unequivocally, 
    including the conditions for strict comparison.

    The basic semantics are derived from the class Interval\\<T\\>, described in the support RM."""
    
    # invariant limits_consistent met because all subclasses of Interval check that lower and upper
    #  bounds have the same type

    value: Interval[DVOrdered]

    def _attempt_set_value(self, value: Interval[DVOrdered]):
        if ((value.lower is not None) and (not isinstance(value.lower, DVOrdered))) or ((value.upper is not None) and (not isinstance(value.upper, DVOrdered))):
                raise TypeError("DVInterval values must be of type DVOrdered (did you forget to wrap an ordered value in DVOrdered first?)")
        self.value = value

    def __init__(self, value: Optional[Interval[DVOrdered]] = None, lower: Optional[DVOrdered] = None, upper: Optional[DVOrdered] = None):
        """If value filled it is used, otherwise lower and upper are taken (defaults to a completely unbounded proper interval)"""
        if value is not None:
            self._attempt_set_value(value)
        else:
            if (lower is not None and (not isinstance(lower, DVOrdered))) or (upper is not None and (not isinstance(upper, DVOrdered))):
                raise ValueError("If lower or upper bounds are proivded, they must be of type DVOrdered or `None` (did you forget to wrap an ordered value in DVOrdered first?)")
            
            if (lower is None and upper is None):
                self._attempt_set_value(ProperInterval[DVOrdered]())
            elif (lower is None and upper is not None) or (lower is not None and upper is None):
                self._attempt_set_value(ProperInterval[DVOrdered](lower=lower, upper=upper))
            else:
                if lower.is_equal(upper):
                    self._attempt_set_value(PointInterval(point_value=lower))
                else:
                    self._attempt_set_value(ProperInterval[DVOrdered](lower=lower, upper=upper))

        super().__init__()

    def __str__(self):
        return str(self.value)

    def is_equal(self, other):
        return (type(self) == type(other) and
        self.value.is_equal(other.value))
    
    def has(self, e: DVOrdered) -> bool:
        return self.value.has(e)
    
    def intersects(self, other: 'DVInterval'):
        return self.value.intersects(other.value)
    
    def contains(self, other: 'DVInterval'):
        return self.value.contains(other.value)
    

class ReferenceRange(AnyClass):
    """Defines a named range to be associated with any DV_ORDERED datum. Each such range is particular 
    to the patient and context, e.g. sex, age, and any other factor which affects ranges. May be 
    used to represent normal, therapeutic, dangerous, critical etc ranges."""

    meaning: DVText
    """Term whose value indicates the meaning of this range, e.g. normal, critical, therapeutic etc."""

    range: DVInterval
    """The data range for this meaning, e.g. critical etc."""

    def __init__(self, meaning : DVText, range: DVInterval, **kwargs):
        self.meaning = meaning
        if (range.value.lower is not None):
            print("lower_simple:", str(range.value.lower.is_simple()))
        if (range.value.lower is not None and (not range.value.lower.is_simple())) or (range.value.upper is not None and (not range.value.upper.is_simple())):
            raise ValueError("Upper and lower bound values in reference range must not have a normal range (invariant: range_is_simple)")
        self.range = range
        super().__init__(**kwargs)

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.meaning, other.meaning) and
                is_equal_value(self.range, other.range))

    def is_in_range(self, v: DVOrdered):
        """Indicates if the value v is inside the range."""
        return self.range.has(v)
