from abc import abstractmethod
from typing import Optional, Union

import numpy as np

from org.openehr.base.foundation_types.primitive_types import ordered_numeric
from org.openehr.base.foundation_types.time import ISODuration, ISOTime, ISODateTime, ISODate, TimeDefinitions
from org.openehr.rm.data_types.text import CodePhrase
from org.openehr.rm.data_types.quantity import DVAmount, DVAbsoluteQuantity, DVInterval, DVQuantified, ReferenceRange
from org.openehr.rm.support.terminology import TerminologyService

class DVDuration(DVAmount):
    """Represents a period of time with respect to a notional point in time, which is not specified. A sign 
    may be used to indicate the duration is backwards in time rather than forwards.

    Note: two deviations from ISO 8601 are supported, the first, to allow a negative sign, and the second 
    allowing the 'W' designator to be mixed with other designators. See time types section 
    in the Foundation Types model.
    
    Used for recording the duration of something in the real world, particularly when there is a need 
    a) to represent the duration in customary format, i.e. days, hours, minutes etc, and 
    b) if it will be used in computational operations with date/time quantities, i.e. additions, subtractions etc.

    Misuse: Durations cannot be used to represent points in time, or intervals of time."""

    _value : ISODuration

    def _get_value(self) -> str:
        return self._value.value
    
    value = property(
        fget=_get_value
    )

    # assume that accuracy is in seconds here as magnitude is
    def __init__(self, value: Union[ISODuration, str], normal_status: Optional[CodePhrase] = None, normal_range: Optional[DVInterval] = None, other_reference_ranges: Optional[list['ReferenceRange']] = None, magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, accuracy : Optional[np.float32] = None, accuracy_is_percent: Optional[bool] = None, terminology_service: Optional[TerminologyService] = None):
        converted_value = value
        if isinstance(value, str):
            converted_value = ISODuration(value)
        super().__init__(converted_value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, accuracy_is_percent, terminology_service)

    def is_strictly_comparable_to(self, other: 'DVDuration'):
        return isinstance(other, DVDuration)

    def _allowed_numeric_operation_check(self, other):
        if not isinstance(other, DVDuration):
            raise TypeError(f"Can only add DVDuration to DVDuration but type \'{type(other)}\' was given")
        super()._allowed_numeric_operation_check(other)

    def __add__(self, other: 'DVDuration') -> 'DVDuration':
        self._allowed_numeric_operation_check(other)
        dva = super().__add__(other)
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    def __sub__(self, other: 'DVDuration') -> 'DVDuration':
        self._allowed_numeric_operation_check(other)
        dva = super().__sub__(other)
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    def __mul__(self, other: np.float32):
        dva = super().__mul__(other)
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    def __rmul__(self, other):
        dva = super().__rmul__(other)
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    def __truediv__(self, other):
        dva = super().__mul__(1 / other)
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    def __neg__(self):
        dva = super().__neg__()
        return DVDuration(dva._value, dva.normal_status, dva.normal_range, dva.other_reference_ranges, dva.magnitude_status, dva.accuracy, dva.accuracy_is_percent, dva._terminology_service)
    
    # implement the ISODuration methods for ease
    def is_extended(self) -> bool:
        return self._value.is_extended()
    
    def is_partial(self) -> bool:
        return self._value.is_partial()
    
    def years(self) -> np.int32:
        return self._value.years()
    
    def months(self) -> np.int32:
        return self._value.months()
    
    def days(self) -> np.int32:
        return self._value.days()
    
    def hours(self) -> np.int32:
        return self._value.hours()
    
    def minutes(self) -> np.int32:
        return self._value.minutes()
    
    def seconds(self) -> np.int32:
        return self._value.seconds()
    
    def fractional_seconds(self) -> np.float32:
        return self._value.fractional_seconds()
    
    def weeks(self) -> np.int32:
        return self._value.weeks()
    
    def is_decimal_sign_comma(self) -> bool:
        return self._value.is_decimal_sign_comma()
    
    def to_seconds(self) -> np.float32:
        return self._value.to_seconds()

    def magnitude(self):
        return self.to_seconds()
    
    def __str__(self):
        return self._value.value
    
    def as_string(self) -> str:
        return self._value.as_string()
    
class DVTemporal(DVAbsoluteQuantity):
    """Specialised temporal variant of DV_ABSOLUTE_QUANTITY whose diff type is DV_DURATION."""

    accuracy : Optional[DVDuration]
    """Time accuracy, expressed as a duration."""

    def __init__(self, 
                 value: Union[ISOTime, ISODateTime, ISODate, str], 
                 normal_status: Optional[CodePhrase] = None, 
                 normal_range: Optional['DVInterval'] = None, 
                 other_reference_ranges: Optional[list['ReferenceRange']] = None, 
                 magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, 
                 accuracy : Optional[DVDuration] = None, 
                 terminology_service: Optional[TerminologyService] = None):
        if accuracy is not None and not isinstance(accuracy, DVDuration):
            raise TypeError(f"Accuracy must be DVDuration for subclasses of DVTemporal but \'{type(accuracy)}\' was given")
        super().__init__(value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, terminology_service)

    @abstractmethod
    def __add__(self, other: DVDuration) -> 'DVTemporal':
        pass
    
    @abstractmethod
    def subtract(self, a_diff: DVDuration) -> 'DVTemporal':
        """Subtract a Duration from this temporal entity."""
        pass

    @abstractmethod
    def diff(self, other: 'DVTemporal') -> DVDuration:
        """Difference between this temporal entity and other."""
        pass

    @abstractmethod
    def __sub__(self, other: Union[DVDuration, 'DVTemporal']) -> Union['DVTemporal', DVDuration]:
        pass


class DVDate(DVTemporal):
    """Represents an absolute point in time, as measured on the Gregorian calendar,
      and specified only to the day. Semantics defined by ISO 8601. Used for recording 
      dates in real world time. The partial form is used for approximate birth dates, 
      dates of death, etc."""
    
    _value : ISODate

    def _get_value(self) -> str:
        return self._value.value
    
    value = property(
        fget=_get_value
    )
    
    def __init__(self, 
                 value: Union[ISODate, str], 
                 normal_status: Optional[CodePhrase] = None, 
                 normal_range: Optional['DVInterval'] = None, 
                 other_reference_ranges: Optional[list['ReferenceRange']] = None, 
                 magnitude_status : Optional[Union[DVQuantified.MagnitudeStatus, str]] = None, 
                 accuracy : Optional[DVDuration] = None, 
                 terminology_service: Optional[TerminologyService] = None):
        converted_value = value
        if isinstance(value, str):
            converted_value = ISODate(value)
        super().__init__(converted_value, normal_status, normal_range, other_reference_ranges, magnitude_status, accuracy, terminology_service)

    def magnitude(self):
        """Numeric value of the date as days since the calendar origin date `0001-01-01`."""
        return np.int32((self._value - ISODate("0001-01-01")).to_seconds() / 86400)
    
    def is_equal(self, other: 'DVDate'):
        """Return True if this `DV_QUANTIFIED` is considered equal to other."""
        return (
            type(self) == type(other) and
            self._value.is_equal(other._value)
            )
    
    def is_strictly_comparable_to(self, other: 'DVDate'):
        """True, for any two Dates."""
        return isinstance(other, DVDate)

    def _combine_accuracies(self, other: Union[DVDuration, 'DVDate']) -> Optional[DVDuration]:
        if self.accuracy is None or other.accuracy is None:
            return None
        else:
            if isinstance(other, DVDate):
                return self.accuracy + other.accuracy
            else:
                if other.accuracy_is_percent:
                    absolute_accuracy = (other.accuracy / 100) * other.to_seconds()
                    return self.accuracy + DVDuration(f"PT{absolute_accuracy}S")
                else:
                    return self.accuracy + DVDuration(f"PT{other.accuracy}S")
                

    def __add__(self, other: 'DVDuration'):
        """Addition of a Duration to this Date."""
        if not isinstance(other, DVDuration):
            raise TypeError(f"Can only add DVDuration to DVDate, not \'{type(other)}\'")
        new_value = self._value.add(other._value)
        new_accuracy = self._combine_accuracies(other)
        return DVDate(new_value, self.normal_status, self.normal_range, self.other_reference_ranges, self.magnitude_status, new_accuracy, self._terminology_service)
    
    def subtract(self, a_diff):
        """Subtract a Duration from this Date."""
        return self._value.subtract(a_diff._value)
    
    def diff(self, other):
        """Difference between this Date and other."""
        return self._value.diff(other._value)
    
    def __sub__(self, other: Union['DVDate', DVDuration]):
        if isinstance(other, DVDate):
            return self.diff(other)
        elif isinstance(other, DVDuration):
            return self.subtract(other)
        else:
            raise TypeError(f"Can only subtract DVDuration or DVDate from date, not \'{type(other)}\'")
