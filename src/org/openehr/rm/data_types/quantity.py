"""The data_types.quantity package contains classes for representing different
forms of measured quantity and supporting information for those quantities"""

from abc import abstractmethod
from enum import StrEnum
from typing import Optional, Union

import numpy as np

from org.openehr.base.foundation_types.primitive_types import ordered, integer_type, ordered_numeric
from org.openehr.base.foundation_types.time import ISOType, ISODate
from org.openehr.base.foundation_types.interval import Interval, ProperInterval, PointInterval
from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.rm.data_types import DataValue
from org.openehr.rm.data_types.text import CodePhrase, DVCodedText, DVText
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

    _terminology_service : Optional[TerminologyService]
    """PRIVATE: Keep track of TerminologyService used at initialization for later re-use if needed"""

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

        self._terminology_service = terminology_service

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

class DVOrdinal(DVOrdered):
    """A data type that represents integral score values, e.g. pain, Apgar values, etc, where there is:

    a) implied ordering, b) no implication that the distance between each value is constant, 
    c) the total number of values is finite and d) integer values only.

    Note that although the term 'ordinal' in mathematics means natural numbers only, here any integer is allowed, 
    since negative and zero values are often used by medical professionals for values around a neutral point. 
    Examples of sets of ordinal values:

    -3, -2, -1, 0, 1, 2, 3 - reflex response values

    0, 1, 2 - Apgar values

    This class is used for recording any clinical datum which is customarily recorded using symbolic values. 
    Example: the results on a urinalysis strip, e.g. `{neg, trace, +, , +}` are used for leucocytes, protein, 
    nitrites etc; for non-haemolysed blood `{neg, trace, moderate}`; for haemolysed blood `{small, moderate, large}`.

    For scores or scales that include Real numbers (or might in the future, i.e. not fixed for all time, such as Apgar), 
    use DV_SCALE. DV_SCALE may also be used in future for representing purely Integer-based scales, however, 
    the DV_ORDINAL type should continue to be supported in software implementations in order to accommodate existing 
    data that are instances of this type."""

    symbol : DVCodedText
    """Coded textual representation of this value in the enumeration, which may be strings made from + symbols, or 
    other enumerations of terms such as mild, moderate, severe, or even the same number series as the values, 
    e.g. 1, 2, 3."""

    def __init__(self, value: Union[integer_type, int], symbol: DVCodedText, normal_status = None, normal_range = None, other_reference_ranges = None, terminology_service = None):
        if not (isinstance(value, integer_type) or isinstance(value, int)):
            raise TypeError("DVOrdinal value must be of integer type")
        self.symbol = symbol
        super().__init__(value, normal_status, normal_range, other_reference_ranges, terminology_service)

    def is_strictly_comparable_to(self, other):
        return super().is_strictly_comparable_to(other)
    
class DVScale(DVOrdered):
    """A data type that represents scale values, where there is:

    a) implied ordering, b) no implication that the distance between each value is constant, and 
    c) the total number of values is finite; d) non-integer values are allowed.

    Example:
    ```
        Borg CR 10 Scale

        0    No Breathlessness at all
        0.5  Very Very Slight (Just Noticeable)
        1    Very Slight
        2    Slight Breathlessness
        3    Moderate
        ... etc
    ```
    For scores that include only Integers, DV_SCALE may also be used, but DV_ORDINAL should be supported to accommodate 
    existing data instances of that type."""

    symbol : DVCodedText
    """Coded textual representation of this value in the scale range, which may be strings made from symbols or other 
    enumerations of terms such as no breathlessness, very very slight, slight breathlessness. Codes come from archetypes.

    In some cases, a scale may include values that have no code/symbol. In this case, the symbol will be a DV-CODED_TEXT 
    including the terminology_id and a blank String value for code_string."""

    def __init__(self, value: Union[np.float32, float], symbol: DVCodedText, normal_status = None, normal_range = None, other_reference_ranges = None, terminology_service = None):
        if not (isinstance(value, np.float32) or isinstance(value, float)):
            raise TypeError("DVScale value must be of float type")
        self.symbol = symbol
        super().__init__(value, normal_status, normal_range, other_reference_ranges, terminology_service)

    def is_strictly_comparable_to(self, other):
        return super().is_strictly_comparable_to(other)
    

class DVQuantified(DVOrdered):
    """Abstract class defining the concept of true quantified values, i.e. values which are not only ordered, but which 
    have a precise magnitude."""

    magnitude_status: Optional[str]
    """Optional status of magnitude with values:
    * `"="` : magnitude is a point value
    * `"<"` : value is < magnitude
    * `">"` : value is > magnitude
    * `"<="` : value is <= magnitude
    * `">="` : value is >= magnitude
    * `"~"` : value is approximately magnitude

    If not present, assumed meaning is "=" ."""

    accuracy : Optional[AnyClass]
    """Accuracy of measurement. Exact form of expression determined in descendants."""

    class MagnitudeStatus(StrEnum):
        POINT_VALUE = "="
        """magnitude is a point value"""
        APPROXIMATE_VALUE = "~"
        """true value is approximately magnitude"""
        VALUE_LESS_THAN_MANGITUDE = "<"
        """true value is < magnitude"""
        VALUE_GREATER_THAN_MAGNITUDE = ">"
        """true value is > magnitude"""
        VALUE_LESS_THAN_OR_EQUAL_TO_MAGNITUDE = "<="
        """true value is <= magnitude"""
        VALUE_GREATER_THAN_OR_EQUAL_TO_MAGNITUDE = ">="
        """true value is >= magnitude"""


    @abstractmethod
    def __init__(self, value: ordered_numeric, normal_status: Optional[CodePhrase] = None, normal_range: Optional['DVInterval'] = None, other_reference_ranges: Optional[list['ReferenceRange']] = None, magnitude_status : Optional[Union[MagnitudeStatus, str]] = None, accuracy : Optional[AnyClass] = None, terminology_service: Optional[TerminologyService] = None):
        if not (isinstance(value, ordered_numeric) or isinstance(value, float) or isinstance(value, int)):
            raise TypeError("Quantified value must be of an ordered_numeric type")
        
        if (magnitude_status is not None) and (not DVQuantified.valid_magnitude_status(magnitude_status)):
            raise ValueError("Provided magnitude status was not one of the valid values (invariant: magnitude_status_valid)")
        
        self.magnitude_status = magnitude_status
        self.accuracy = accuracy

        super().__init__(value, normal_status, normal_range, other_reference_ranges, terminology_service)

    # TODO: seems like specificaion is missing a string argument 's'
    def valid_magnitude_status(s: Union[MagnitudeStatus, str]):
        """Test whether a string value is one of the valid values for the magnitude_status attribute."""
        return (s in {"=", "<", ">", "<=", ">=", "~"})

    def magnitude(self) -> ordered_numeric:
        return self.value

    def accuracy_unknown(self) -> bool:
        """True if accuracy is not known, e.g. due to not being recorded or discernable."""
        return (self.accuracy is None)

    def is_equal(self, other: 'DVQuantified'):
        return (
            super().is_equal(other) and
            is_equal_value(self.accuracy, other.accuracy) and
            self.magnitude_status == other.magnitude_status
        )
    
    def is_strictly_comparable_to(self, other):
        return super().is_strictly_comparable_to(other)


class DVAmount(DVQuantified):
    """Abstract class defining the concept of relative quantified 'amounts'. For relative quantities, 
    the + and - operators are defined (unlike descendants of DV_ABSOLUTE_QUANTITY, such as the date/time types)."""
    
    value: ordered_numeric

    accuracy_is_percent : Optional[bool]
    """If `True`, indicates that when this object was created, accuracy was recorded as a percent value; 
    if `False`, as an absolute quantity value."""

    accuracy : Optional[np.float32]
    """Accuracy of measurement, expressed either as a half-range percent value (`accuracy_is_percent == True`) or a half-range quantity. A value of 0 means that accuracy is 100%, i.e. no error.
    
    A value of `None` means that accuracy was not recorded."""

    def valid_percentage(number: ordered_numeric) -> bool:
        """Test whether a number is a valid percentage, i.e. between 0 and 100."""
        return (number >= 0) and (number <= 100)

    def __init__(self, value: ordered_numeric, normal_status: Optional[CodePhrase] = None, normal_range: Optional['DVInterval'] = None, other_reference_ranges: Optional[list['ReferenceRange']] = None, magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, accuracy : Optional[np.float32] = None, accuracy_is_percent: Optional[bool] = None, terminology_service: Optional[TerminologyService] = None):
        converted_accuracy = accuracy
        if accuracy is not None:
            if (not isinstance(accuracy, np.float32)) and (not isinstance(accuracy, float)):
                raise TypeError("Accuracy must be a Real value")
            if isinstance(accuracy, float):
                converted_accuracy = np.float32(accuracy)

            if accuracy_is_percent is None:
                raise ValueError("If accuracy is provided, so must be accuracy_is_percent")
            
            if accuracy == 0.0 and accuracy_is_percent:
                raise ValueError("If accuracy is 0 (i.e amount is exact) then accuracy_is_percent must be False (invariant: accuracy_is_percent_validity)")
            
            if not DVAmount.valid_percentage(accuracy) and accuracy_is_percent:
                raise ValueError(f"Percentage accuracies must be a value between 0 and 100 inclusive, but \'{accuracy}\' was given (invariant: accuracy_validity)")

        self.accuracy_is_percent = accuracy_is_percent
        super().__init__(value, normal_status, normal_range, other_reference_ranges, magnitude_status, converted_accuracy, terminology_service)

    def is_equal(self, other):
        return (
            super().is_equal(other) and
            self.accuracy_is_percent == other.accuracy_is_percent
        )
    
    def _allowed_numeric_operation_check(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Other type must also be DVAmount to allow numerical operations - you provided type \'{type(other)}\' (perhaps you forgot to wrap an ordered_numeric value type?)")
        if (not self.is_strictly_comparable_to(other)):
            raise TypeError(f"DVAmount with value of type \'{type(self.value)}\' is not strictly comparable to DVAmount with value of type \'{type(other.value)}\'")

    def __neg__(self):
        return DVAmount(-self.value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, self.accuracy, self.accuracy_is_percent, self._terminology_service)

    def _combine_accuracies_addsub(self, other: 'DVAmount', new_value: ordered_numeric) -> tuple[Optional[np.float32], Optional[bool]]:
        new_accuracy = None
        new_accuracy_is_percent = None
        # from spec: The result is ... unknown, if either or both operand accuracies are unknown.
        if not self.accuracy_unknown() and not other.accuracy_unknown():
            # from spec: The result is the sum of the accuracies of the operands, if both present, or;
            self_absolute_accuracy = abs(self.accuracy if not self.accuracy_is_percent else ((self.accuracy / 100) * self.value))
            other_absolute_accuracy = abs(other.accuracy if not other.accuracy_is_percent else ((other.accuracy / 100) * other.value))
            new_absolute_accuracy = self_absolute_accuracy + other_absolute_accuracy

            # from spec: If the accuracy value is a percentage in one operand and not in the other, the form in the result is that of the larger operand.
            if self.value >= other.value:
                new_accuracy_is_percent = self.accuracy_is_percent
            else:
                new_accuracy_is_percent = other.accuracy_is_percent

            new_accuracy = new_absolute_accuracy if not new_accuracy_is_percent else ((new_absolute_accuracy / new_value) * 100)

        return (new_accuracy, new_accuracy_is_percent)


    def __add__(self, other: 'DVAmount'):
        self._allowed_numeric_operation_check(other)
        new_value = self.value + other.value
        new_accuracy, new_accuracy_is_percent = self._combine_accuracies_addsub(other, new_value)

        return DVAmount(new_value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, new_accuracy, new_accuracy_is_percent, self._terminology_service)
    
    def __sub__(self, other: 'DVAmount'):
        self._allowed_numeric_operation_check(other)
        new_value = self.value - other.value
        new_accuracy, new_accuracy_is_percent = self._combine_accuracies_addsub(other, new_value)

        return DVAmount(new_value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, new_accuracy, new_accuracy_is_percent, self._terminology_service)
    
    def _combine_accuracies_muldiv(self, other: 'DVAmount', new_value: ordered_numeric) -> tuple[Optional[np.float32], Optional[bool]]:
        new_accuracy = None
        new_accuracy_is_percent = None

        if not self.accuracy_unknown() and not other.accuracy_unknown():
            self_perc_accuracy = abs(self.accuracy if self.accuracy_is_percent else ((self.accuracy / self.value) * 100))
            other_perc_accuracy = abs(other.accuracy if other.accuracy_is_percent else ((other.accuracy / other.value) * 100))
            new_perc_accuracy = self_perc_accuracy + other_perc_accuracy

            if self.value >= other.value:
                new_accuracy_is_percent = self.accuracy_is_percent
            else:
                new_accuracy_is_percent = other.accuracy_is_percent

            new_accuracy = new_perc_accuracy if new_accuracy_is_percent else ((new_perc_accuracy / 100) * new_value)

        return (new_accuracy, new_accuracy_is_percent)

    def __mul__(self, other: np.float32):
        if not (isinstance(other, np.float32) or isinstance(other, float)):
            raise TypeError(f"Can only multiply a DVAmount by Real, not \'{type(other)}\'")
        new_value = self.value * other

        return DVAmount(new_value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, self.accuracy, self.accuracy_is_percent, self._terminology_service)
    
    def __rmul__(self, other: np.float32):
        return self.__mul__(other)

    def __truediv__(self, other: np.float32):
        if not (isinstance(other, np.float32) or isinstance(other, float)):
            raise TypeError(f"Can only multiply a DVAmount by Real, not \'{type(other)}\'")
        new_value = self.value / other

        return DVAmount(new_value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, self.accuracy, self.accuracy_is_percent, self._terminology_service)
    

class DVQuantity(DVAmount):
    """Quantitified type representing scientific quantities, i.e. quantities expressed as a magnitude and units. 
    Units are expressed in the UCUM syntax (Unified Code for Units of Measure (UCUM), by Gunther Schadow and Clement 
    J. McDonald of The Regenstrief Institute) (case-sensitive form) by default, or another system if units_system is set.

    Can also be used for time durations, where it is more convenient to treat these as simply a number of seconds rather 
    than days, months, years (in the latter case, DV_DURATION may be used)."""

    value: np.float32

    def _get_magnitude(self) -> np.float32:
        return self.value

    magnitude = property(
        fget=_get_magnitude
    )
    """Numeric magnitude of the quantity."""

    precision : Optional[np.int32]
    """Precision to which the value of the quantity is expressed, in terms of number of decimal places. The value 0 
    implies an integral quantity. The value -1 implies no limit, i.e. any number of decimal places."""

    units: str
    """Quantity units, expressed as a code or syntax string from either UCUM (the default) or the units system 
    specified in `units_system`, when set.

    In either case, the value is the code or syntax - normally formed of standard ASCII - which is in principal 
    not the same as the display string, although in simple cases such as 'm' (for meters) it will be.

    If the `units_display_name` field is set, this may be used for display. If not, the implementations must effect 
    the resolution of the `units` value to a display form locally, e.g. by lookup of reference tables, request to 
    a terminology service etc.

    Example values from UCUM: "kg/m^2", “mm[Hg]", "ms-1", "km/h"."""

    units_system: Optional[str]
    """Optional field used to specify a units system from which codes in units are defined. Value is a URI 
    identifying a terminology containing units concepts from the ([HL7 FHIR terminologies list](https://www.hl7.org/fhir/terminologies-systems.html)).

    If not set, the UCUM standard (case-sensitive codes) is assumed as the units system."""

    units_display_name : Optional[str]
    """Optional field containing the displayable form of the units field, e.g. '°C'.

    If not set, the application environment needs to determine the displayable form."""

    # n.B: normal_range and other_reference_ranges must now have DVQuantity, not DVOrdered

    def __init__(self, 
                 value: np.float32,
                 units: str, 
                 units_system: Optional[str] = None,
                 units_display_name: Optional[str] = None,
                 normal_status: Optional[CodePhrase] = None, 
                 normal_range: Optional['DVInterval'] = None, 
                 other_reference_ranges: Optional[list['ReferenceRange']] = None, 
                 magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, 
                 accuracy : Optional[np.float32] = None, 
                 accuracy_is_percent: Optional[bool] = None, 
                 precision: Optional[np.int32] = None,
                 terminology_service: Optional[TerminologyService] = None):
        converted_value = value
        if not (isinstance(value, np.float32) or isinstance(value, float)):
            raise TypeError("Value/magnitude must be a Real")
        if isinstance(value, float):
            converted_value = np.float32(value)
        
        if normal_range is not None:
            if normal_range.value.upper is not None and not isinstance(normal_range.value.upper, DVQuantity):
                raise TypeError(f"Normal range values must each be DVQuantity, but \'{type(normal_range.value.upper)}\' was given")
            if normal_range.value.lower is not None and not isinstance(normal_range.value.lower, DVQuantity):
                raise TypeError(f"Normal range values must each be DVQuantity, but \'{type(normal_range.value.upper)}\' was given")

        self.value = converted_value
        self.units = units
        self.units_system = units_system
        self.units_display_name = units_display_name
        self.precision = precision

        super().__init__(value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, accuracy_is_percent, terminology_service)

    def is_strictly_comparable_to(self, other: 'DVQuantity'):
        return (
            super().is_strictly_comparable_to(other) and
            self.units == other.units and
            self.units_system == other.units_system
        )
    
    # overridden to improve error messages
    def _allowed_numeric_operation_check(self, other: 'DVQuantity'):
        if not isinstance(other, type(self)):
            raise TypeError(f"Other type must also be DVQuantity to allow numerical operations - you provided type \'{type(other)}\' (perhaps you forgot to wrap an Real value type?)")
        if self.units_system != other.units_system:
            raise ValueError(f"Cannot add two quantities with different units systems - \'{self.units_system if self.units_system is not None else "http://unitsofmeasure.org (default)"}\' and \'{other.units_system if other.units_system is not None else "http://unitsofmeasure.org (default)"}\'")
        if self.units != other.units:
            raise ValueError(f"Cannot add two quantities with different units - \'{self.units}\' and \'{other.units}\'")
        if (not self.is_strictly_comparable_to(other)):
            raise TypeError(f"DVQuantity with value of type \'{type(self.value)}\' is not strictly comparable to DVQuantity with value of type \'{type(other.value)}\'")

    def _combine_precision(self, other: 'DVQuantity') -> Optional[np.int32]:
        if self.precision is None or other.precision is None:
            return None
        else:
            if self.precision == -1 and other.precision == -1:
                return -1
            elif self.precision == -1:
                return other.precision
            elif other.precision == -1:
                return self.precision
            else:
                return min(self.precision, other.precision)


    def __add__(self, other) -> 'DVQuantity':
        amount_result = super().__add__(other)
        new_precision = self._combine_precision(other)
        return DVQuantity(amount_result.value, self.units, self.units_system, self.units_display_name, amount_result.normal_status, amount_result.normal_range, amount_result.other_reference_ranges, amount_result.magnitude_status, amount_result.accuracy, amount_result.accuracy_is_percent, new_precision, amount_result._terminology_service)
    
    def __sub__(self, other) -> 'DVQuantity':
        amount_result = super().__sub__(other)
        new_precision = self._combine_precision(other)
        return DVQuantity(amount_result.value, self.units, self.units_system, self.units_display_name, amount_result.normal_status, amount_result.normal_range, amount_result.other_reference_ranges, amount_result.magnitude_status, amount_result.accuracy, amount_result.accuracy_is_percent, new_precision, amount_result._terminology_service)
    
    def __mul__(self, other: np.float32):
        amount_result = super().__mul__(other)
        new_precision = self.precision
        return DVQuantity(amount_result.value, self.units, self.units_system, self.units_display_name, amount_result.normal_status, amount_result.normal_range, amount_result.other_reference_ranges, amount_result.magnitude_status, amount_result.accuracy, amount_result.accuracy_is_percent, new_precision, amount_result._terminology_service)
    
    def __truediv__(self, other):
        amount_result = super().__truediv__(other)
        new_precision = self.precision
        return DVQuantity(amount_result.value, self.units, self.units_system, self.units_display_name, amount_result.normal_status, amount_result.normal_range, amount_result.other_reference_ranges, amount_result.magnitude_status, amount_result.accuracy, amount_result.accuracy_is_percent, new_precision, amount_result._terminology_service)

    def is_integral(self) -> bool:
        """True if precision = 0, meaning that the magnitude is a whole number."""
        return self.precision == 0
    
class DVCount(DVAmount):
    """Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy patient), number of cigarettes smoked in a day.

    Misuse: Not to be used for amounts of physical entities (which all have units)."""

    value: np.int64

    def _get_magnitude(self) -> np.int64:
        return self.value

    magnitude = property(
        fget=_get_magnitude
    )
    """Numeric magnitude of the quantity."""

    # n.B: normal_range and other_reference_ranges must now have DVQuantity, not DVOrdered

    def __init__(self, value: np.int64, normal_status: Optional[CodePhrase] = None, normal_range: Optional['DVInterval'] = None, other_reference_ranges: Optional[list['ReferenceRange']] = None, magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, accuracy : Optional[np.float32] = None, accuracy_is_percent: Optional[bool] = None, terminology_service: Optional[TerminologyService] = None):
        converted_value = value
        if not (isinstance(value, np.int64) or isinstance(value, int)):
            raise TypeError("Value/magnitude must be a Integer64")
        if isinstance(value, int):
            converted_value = np.int64(value)
        
        super().__init__(converted_value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, accuracy_is_percent, terminology_service)