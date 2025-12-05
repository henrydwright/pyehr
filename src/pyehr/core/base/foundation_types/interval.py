from abc import abstractmethod
import json
from typing import Optional, Union
import warnings

import numpy as np
from pydantic import ValidationError, field_validator

from pyehr.core.base.foundation_types import AnyClass
from pyehr.core.base.foundation_types.primitive_types import ordered

class Interval[T : ordered](AnyClass):
    """Interval abstraction, featuring upper and lower limits that may be open or closed, 
    included or not included. Interval of ordered items."""

    _lower : Optional[T] = None

    def _get_lower(self) -> Optional[T]:
        return self._lower
    
    def _set_lower(self, value: Optional[T]):
        if self.upper is not None and (not isinstance(value, type(self._upper) or value is None)):
            raise TypeError("Lower bound must be same type as upper bound (or `None`)")
        if self.upper is not None and value > self.upper:
            raise ValueError("Lower bound cannot be larger than upper bound")
        self._lower = value

    lower = property(
        fget=_get_lower,
        fset=_set_lower
    )
    """Lower bound"""

    _upper : Union[T, None] = None
    
    def _get_upper(self) -> Optional[T]:
        return self._upper
    
    def _set_upper(self, value: Optional[T]):
        if value is None:
            self._upper = value
        else:
            if self.lower is not None and not isinstance(value, type(self._lower)):
                raise TypeError("Upper bound must be same type as lower bound")
            if (self.lower is not None) and (value < self.lower):
                raise ValueError("Upper bound cannot be smaller than lower bound")
        self._upper = value

    upper = property(
        fget=_get_upper,
        fset=_set_upper
    )
    """Upper bound"""

    def _get_lower_unbounded(self) -> bool:
        return self._lower is None
    
    def _get_upper_unbounded(self) -> bool:
        return self._upper is None

    lower_unbounded = property(
        fget=_get_lower_unbounded
        )
    """lower boundary open (i.e. = -infinity) when lower is `None`"""

    upper_unbounded = property(
        fget=_get_upper_unbounded
        )
    """upper boundary open (i.e. = +infinity) when upper is `None`"""

    _lower_included : bool = False
    
    def _get_lower_included(self) -> bool:
        return self._lower_included
    
    def _set_lower_included(self, value: bool):
        if self.lower is None and value == True:
            raise ValueError("Cannot include lower, if lower is unbounded (set to `None`)")
        self._lower_included = value

    lower_included = property(
        fget=_get_lower_included,
        fset=_set_lower_included
    )
    """lower boundary value included in range if not lower_unbounded."""
    
    _upper_included: bool = False

    def _get_upper_included(self) -> bool:
        return self._upper_included
    
    def _set_upper_included(self, value: bool):
        if self.upper is None and value == True:
            raise ValueError("Cannot include upper, if upper is unbounded (set to `None`)")
        self._upper_included = value

    upper_included = property(
        fget=_get_upper_included,
        fset=_set_upper_included
    )
    """upper boundary value included in range if not upper_unbounded."""

    @abstractmethod
    def has(self, e : ordered) -> bool:
        """True if the value `e` is properly contained in this Interval. 
        
        True if (lower_unbounded or lower_included and v >= lower) or v > lower and 
        (upper_unbounded or upper_included and v <= upper or v < upper)"""
        pass

    def intersects(self, other: 'Interval[T]'):
        """True if there is any overlap between intervals represented by Current and other. 
        True if at least one limit of other is strictly inside the limits of this interval."""
        return (self.has(other.upper) or self.has(other.lower)) and (other.has(self.upper) or other.has(self.lower))

    def contains(self, other: 'Interval[T]'):
        """True if current interval properly contains other. True if all points of other are 
        inside the current interval."""
        return (self.has(other.upper) and self.has(other.lower))

    @abstractmethod
    def is_equal(self, other):
        """True if current object's interval is semantically same as other."""
        pass

    def __str__(self):
        str_rep = ""
        str_rep += "[" if self.lower_included else "("
        str_rep += str(self.lower) if self.lower is not None else "-INF"
        str_rep += ", "
        str_rep += str(self.upper) if self.upper is not None else "+INF"
        str_rep += "]" if self.upper_included else ")"
        return str_rep
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Foundation_types/Interval.json
        draft = {
            "_type": "INTERVAL",
            "lower_unbounded": self.lower_unbounded,
            "upper_unbounded": self.upper_unbounded,
            "lower_included": self.lower_included,
            "upper_included": self.upper_included
        }
        if self.lower is not None:
            if isinstance(self._lower, AnyClass):
                draft["lower"] = self._lower.as_json()
            else:
                draft["lower"] = {
                    "value": str(self._lower)
                }
        if self.upper is not None:
            if isinstance(self._upper, AnyClass):
                draft["upper"] = self._upper.as_json()
            else:
                draft["upper"] = {
                    "value": str(self._upper)
                }
        return draft


class PointInterval[T : ordered](Interval[T]):
    """Type representing an `Interval` that happens to be a point value. 
    Provides an efficient representation that is substitutable for Interval<T> 
    where needed."""

    def __init__(self, point_value : ordered, **kwargs):
        self.point = point_value
        super().__init__(**kwargs)

    # change default field values
    _lower_included : bool = True
    _upper_included : bool = True

    # override - to reset property
    def _get_lower(self) -> T:
        return self._lower

    # override - tighten type as a point must exist
    def _set_lower(self, value: T):
        self._lower = value
        self._upper = value

    lower = property(
        fget= _get_lower,
        fset= _set_lower
    )
    """Lower bound. Changing this sets `upper===lower===value`"""

    point = property(
        fget= _get_lower,
        fset= _set_lower
    )
    """Point value of interval. Changing this sets `upper===lower===value`"""


    # override - to reset property
    def _get_upper(self) -> T:
        return self._upper

    # override - tighten type as a point must exist
    def _set_upper(self, value: T):
        self._lower = value
        self._upper = value

    upper = property(
        fget=_get_upper,
        fset=_set_upper
    )
    """Upper bound. Changing this sets `upper===lower===value`"""

    # override
    def is_equal(self, other) -> bool:
        return (type(self) == type(other) and
                self.lower == other.lower and
                self.upper == other.upper and
                self.lower_included == other.lower_included and
                self.upper_included == other.upper_included
                )

    # override - for point interval, can only contain if included and equal
    def has(self, e: ordered) -> bool:
        return ((self.lower_included or self.upper_included) and self.lower == e)
    
class ProperInterval[T: ordered](Interval[T]):
    """Type representing a 'proper' Interval, i.e. any two-sided 
    or one-sided interval."""

    def __init__(self, lower: Optional[T] = None, upper: Optional[T] = None, lower_included: bool = False, upper_included: bool = False):
        self.lower = lower
        self.upper = upper
        self.upper_included = upper_included
        self.lower_included = lower_included
        super().__init__()

    # override
    def is_equal(self, other) -> bool:
        return (type(self) == type(other) and
                self.lower == other.lower and
                self.upper == other.upper and
                self.lower_included == other.lower_included and
                self.upper_included == other.upper_included
                )
    # override
    def has(self, e: ordered) -> bool:
        return (
            (self.lower_unbounded or (self.lower_included and e >= self.lower) or e > self.lower) and
            (self.upper_unbounded or (self.upper_included and e <= self.upper) or e < self.upper))
    
    def _get_lower(self) -> Optional[T]:
        return super()._get_lower()
    
    def _set_lower(self, value: Optional[T]):
        if self.upper is not None and value == self.upper:
            raise ValueError("Cannot set upper bound to same value as lower bound for `ProperInterval`. Did you intend `PointInterval`?")
        return super()._set_lower(value)
    
    lower = property(
        fget=_get_lower,
        fset=_set_lower
    )
    """Lower bound."""

    def _get_upper(self) -> Optional[T]:
        return super()._get_upper()
    
    def _set_upper(self, value: Optional[T]):
        if self.lower is not None and value == self.lower:
            raise ValueError("Cannot set lower bound to same value as upper bound for `ProperInterval`. Did you intend `PointInterval`?")
        return super()._set_upper(value)
    
    upper = property(
        fget=_get_upper,
        fset=_set_upper
    )
    """Upper bound."""
    
class MultiplicityInterval(ProperInterval[np.int32]):
    """An Interval of Integer, used to represent multiplicity, cardinality and 
    optionality in models."""

    MULTIPLICITY_RANGE_MARKER : str = ".."
    MULTIPLICITY_UNBOUNDED_MARKER : str = "*"

    def __init__(self, lower: Optional[np.int32] = None, upper: Optional[np.int32] = None):
        super().__init__(lower=lower, upper=upper)

    def _get_upper(self) -> Optional[np.int32]:
        return super()._get_upper()
    
    def _set_upper(self, value: Optional[np.int32]):
        if not (isinstance(value, np.int32) or value is None):
            raise TypeError("Multiplicity interval only allows np.int32 type (or `None`)")
        super()._set_upper(value)

    upper = property(
        fget=_get_upper,
        fset=_set_upper
    )
    """Upper bound. Integer value or `None`"""

    def _get_lower(self) -> Optional[np.int32]:
        return super()._get_lower()
    
    def _set_lower(self, value: Optional[np.int32]):
        if not (isinstance(value, np.int32) or value is None):
            raise TypeError("Multiplicity interval only allows np.int32 type (or `None`)")
        super()._set_lower(value)

    lower = property(
        fget=_get_lower,
        fset=_set_lower
    )
    """Lower bound. Integer value or `None`"""

    def is_equal(self, other) -> bool:
        return super().is_equal(other)
    
    def has(self, e: ordered) -> bool:
        return super().has(e)
    
    def is_open(self) -> bool:
        """True if this interval imposes no constraints, i.e. is set to 0..*."""
        return self.upper_unbounded and self.lower == 0 and self.lower_included
    
    def is_optional(self) -> bool:
        """True if this interval expresses optionality, i.e. 0..1."""
        return self.lower == 0 and self.upper == 1 and self.lower_included and self.upper_included
    
    def is_mandatory(self) -> bool:
        """True if this interval expresses mandation, i.e. 1..1."""
        return self.lower == 0 and self.upper == 1 and self.upper_included and not self.lower_included
    
    def is_prohibited(self) -> bool:
        """True if this interval is set to 0..0."""
        return self.lower == 0 and self.upper == 1 and self.lower_included and not self.upper_included
    
class Cardinality(AnyClass):
    """Express constraints on the cardinality of container objects which are the values of 
    multiply-valued attributes, including uniqueness and ordering, providing the means to 
    state that a container acts like a logical list, set or bag."""

    interval : MultiplicityInterval
    """The interval of this cardinality."""
    
    is_ordered : bool = False
    """True if the members of the container attribute to which this cardinality refers are ordered."""
    is_unique : bool = False
    """True if the members of the container attribute to which this cardinality refers are unique."""

    def __init__(self, ordered : bool, unique : bool, interval : MultiplicityInterval):
        self.is_ordered = ordered
        self.is_unique = unique
        self.interval = interval

    def is_equal(self, other) -> bool:
        return (type(self) == type(other) and
                self.is_ordered == other.is_ordered and 
                self.is_unique == other.is_unique)

    def is_bag(self) -> bool:
        """True if the semantics of this cardinality represent a bag, 
        i.e. unordered, non-unique membership."""
        return not self.is_ordered and not self.is_unique

    def is_list(self) -> bool:
        """True if the semantics of this cardinality represent a list, 
        i.e. ordered, non-unique membership."""
        return self.is_ordered and not self.is_unique

    def is_set(self) -> bool:
        """True if the semantics of this cardinality represent a set, 
        i.e. unordered, unique membership."""
        return self.is_unique and not self.is_ordered
    
    def as_json(self):
        warnings.warn("Cardinality does not have a valid ITS JSON schema, potentially non-standard JSON emitted.", RuntimeWarning)
        return {
            "interval": self.interval.as_json(),
            "is_ordered": self.is_ordered,
            "is_unique": self.is_unique
        }