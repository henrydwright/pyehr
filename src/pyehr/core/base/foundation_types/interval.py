from abc import abstractmethod
import xml.etree.ElementTree as ET
from typing import Optional, Union
import warnings

import numpy as np
from pydantic import ValidationError, field_validator

from pyehr.core.base.foundation_types import AnyClass
from pyehr.core.base.foundation_types.primitive_types import ordered
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.foundation_types.time import ISODateTime, ISOType
from pyehr.core.its.xml import IXMLSupport

class Interval[T : ordered](AnyClass, IXMLSupport):
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
            elif isinstance(self._lower, np.int32):
                draft["lower"] = int(self._lower)
            elif isinstance(self._lower, np.float32):
                draft["lower"] = float(self._lower)
            else:
                draft["lower"] = self._lower
        if self.upper is not None:
            if isinstance(self._upper, AnyClass):
                draft["upper"] = self._upper.as_json()
            elif isinstance(self._upper, np.int32):
                draft["upper"] = int(self._upper)
            elif isinstance(self._lower, np.float32):
                draft["upper"] = float(self._upper)
            else:
                draft["upper"] = self._upper
        return draft
    
    def as_xml(self, root_tag = None, dv_interval_ordering=False):
        tag = "interval" if root_tag is None else root_tag
        root = ET.Element(tag)

        if not dv_interval_ordering:
            low_inc = ET.Element("lower_included")
            low_inc.text = str(self.lower_included).lower()
            root.append(low_inc)

            up_inc = ET.Element("upper_included")
            up_inc.text = str(self.upper_included).lower()
            root.append(up_inc)

            low_unb = ET.Element("lower_unbounded")
            low_unb.text = str(self.lower_unbounded).lower()
            root.append(low_unb)

            up_unb = ET.Element("upper_unbounded")
            up_unb.text = str(self.upper_unbounded).lower()
            root.append(up_unb)

        if self.lower is not None:
            low = ET.Element("lower")
            if isinstance(self._lower, ISOType):
                low.text = str(self._lower.value)
            elif isinstance(self._lower, IXMLSupport):
                low = self._lower.as_xml("lower")
            else:
                low.text = str(self._lower)
            root.append(low)

        if self.upper is not None:
            up = ET.Element("upper")
            if isinstance(self._upper, ISOType):
                up.text = str(self._upper.value)
            elif isinstance(self._upper, IXMLSupport):
                up = self._upper.as_xml("upper")
            else:
                up.text = str(self._upper)
            root.append(up)

        if dv_interval_ordering:
            low_inc = ET.Element("lower_included")
            low_inc.text = str(self.lower_included).lower()
            root.append(low_inc)

            up_inc = ET.Element("upper_included")
            up_inc.text = str(self.upper_included).lower()
            root.append(up_inc)

            low_unb = ET.Element("lower_unbounded")
            low_unb.text = str(self.lower_unbounded).lower()
            root.append(low_unb)

            up_unb = ET.Element("upper_unbounded")
            up_unb.text = str(self.upper_unbounded).lower()
            root.append(up_unb)

        return root
    
    @staticmethod
    def from_xml(root: ET.Element, typ, **kwargs) -> 'Interval':
        # typ is the class for the contents of lower/upper
        low_inc_el = root.findtext("./lower_included")
        low_inc = (low_inc_el.capitalize() == "True") if low_inc_el is not None else None
        up_inc_el = root.findtext("./upper_included")
        up_inc = (up_inc_el.capitalize() == "True") if up_inc_el is not None else None
        
        low = None
        up = None
        if issubclass(typ, IXMLSupport):
            low_el = root.find("./lower")
            if low_el is not None:
                low = typ.from_xml(low_el)
            up_el = root.find("./upper")
            if up_el is not None:
                up = typ.from_xml(up_el)
        else:
            low_txt = root.findtext("./lower")
            if low_txt is not None:
                low = typ(low_txt)
            up_txt = root.findtext("./upper")
            if up_txt is not None:
                up = typ(up_txt)

        if low_inc == up_inc and is_equal_value(low, up):
            pi = PointInterval(low)
            pi.lower_included = low_inc
            return pi
        else:
            propi = ProperInterval(low, up, low_inc, up_inc)
            return propi

class PointInterval[T : ordered](Interval[T]):
    """Type representing an `Interval` that happens to be a point value. 
    Provides an efficient representation that is substitutable for Interval<T> 
    where needed."""

    def __init__(self, point_value : ordered, **kwargs):
        self.point = point_value
        super().__init__()

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
                is_equal_value(self.lower, other.lower) and
                is_equal_value(self.upper, other.upper) and
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
                is_equal_value(self.lower, other.lower) and
                is_equal_value(self.upper, other.upper) and
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
    
class Cardinality(AnyClass, IXMLSupport):
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
        return {
            "interval": self.interval.as_json(),
            "is_ordered": self.is_ordered,
            "is_unique": self.is_unique
        }
    
    def as_xml(self, root_tag = None):
        # https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/Archetype.xsd
        tag = "cardinality" if root_tag is None else root_tag
        root = ET.Element(tag)

        ord = ET.Element("is_ordered")
        ord.text = str(self.is_ordered).lower()
        root.append(ord)

        uni = ET.Element("is_unique")
        uni.text = str(self.is_unique).lower()
        root.append(uni)

        root.append(self.interval.as_xml("interval"))

        return root
    
    def from_xml(root: ET.Element, **kwargs) -> 'Cardinality':
        ord = root.findtext("./is_ordered").capitalize() == "True"
        uni = root.findtext("./is_unique").capitalize() == "True"
        inter = Interval.from_xml(root.find("./interval"), np.int32)
        return Cardinality(ord, uni, inter)
