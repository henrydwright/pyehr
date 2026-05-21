
from abc import abstractmethod
from typing import Optional

import xml.etree.ElementTree as ET

import numpy as np
import re

from pyehr.core.base.base_types.definitions import ValidityKind
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.foundation_types.time import ISODate
from pyehr.core.its.xml import IXMLSupport


class CPrimitive(AnyClass, IXMLSupport):
    """(Abstract) Parent of types representing constraints on primitive types."""

    assumed_value: Optional[AnyClass]
    """Value to be assumed if none sent in data."""

    @abstractmethod
    def __init__(self, assumed_value: Optional[AnyClass] = None, **kwargs):
        # TODO: add checks against assumed value here
        self.assumed_value = assumed_value
        super().__init__(**kwargs)

    @abstractmethod
    def default_value(self) -> AnyClass:
        """Generate a default value from this constraint object."""
        pass

    def has_assumed_value(self) -> bool:
        """True if there is an assumed value."""
        return (self.assumed_value is not None)
    
    @abstractmethod
    def valid_value(self, a_value: AnyClass) -> bool:
        """True if a_value is valid with respect to constraint expressed in concrete 
        instance of this type."""
        pass

    @abstractmethod
    def is_equal(self, other):
        return (type(self) == type(other))

class CBoolean(CPrimitive):
    """Constraint on instances of Boolean. Both attributes cannot be set to False, 
    since this would mean that the Boolean value being constrained cannot be True 
    or False."""

    true_valid: bool
    """True if the value True is allowed."""

    false_valid: bool
    """True if the value False is allowed."""

    assumed_value : Optional[bool]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, true_valid: bool, false_valid: bool, assumed_value : Optional[bool] = None, **kwargs):
        if (not true_valid) and (not false_valid):
            raise ValueError("true_valid and false_valid cannot both be set to 'false'")
        self.true_valid = true_valid
        self.false_valid = false_valid
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other: 'CBoolean'):
        return (super().is_equal(other) and
                self.true_valid == other.true_valid and
                self.false_valid == other.false_valid and
                self.assumed_value == other.assumed_value)

    def as_json(self):
        draft = {
            "true_valid": self.true_valid,
            "false_valid": self.false_valid
        }
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value
        draft["_type"] = "C_BOOLEAN"
        return draft
    
    def as_xml(self, root_tag = None):
        tag = "c_boolean" if root_tag is None else root_tag
        root = ET.Element(tag)
        tv_el = ET.Element("true_valid")
        tv_el.text = str(self.true_valid).lower()
        root.append(tv_el)

        fv_el = ET.Element("false_valid")
        fv_el.text = str(self.false_valid).lower()
        root.append(fv_el)

        if self.assumed_value is not None:
            av_el = ET.Element("assumed_value")
            av_el.text = str(self.assumed_value).lower()
            root.append(av_el)

        return root
    
    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        tv = (root.findtext("./true_valid") == "true")
        fv = (root.findtext("./false_valid") == "true")
        av = root.findtext("./assumed_value")
        if av is not None:
            av = (av == "true")
        return CBoolean(tv, fv, av)
    
    def default_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()
    
class CString(CPrimitive):
    """Constraint on instances of STRING."""

    pattern: Optional[str]
    """Regular expression pattern for proposed instances of String to match."""

    list_var: Optional[list[str]]
    """Set of Strings specifying constraint."""

    list_open: bool
    """True if the list is being used to specify the constraint but is not 
    considered exhaustive."""

    assumed_value: Optional[str]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, list_open: bool, pattern: Optional[str] = None, list_var: Optional[list[str]] = None, assumed_value : Optional[str] = None, **kwargs):
        self.pattern = pattern
        self.list_var = list_var
        self.list_open = list_open
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.pattern, other.pattern) and
                is_equal_value(self.list_var, other.list_var) and
                is_equal_value(self.list_open, other.list_open) and
                is_equal_value(self.assumed_value, other.assumed_value))
    
    def as_json(self):
        draft = {
            "list_open": self.list_open
        }
        if self.pattern is not None:
            draft["pattern"] = self.pattern
        if self.list_var is not None:
            draft["list"] = self.list_var
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value
        draft["_type"] = "C_STRING"
        return draft
    
    def as_xml(self, root_tag = None):
        tag = "c_string" if root_tag is None else root_tag
        root = ET.Element(tag)

        if self.pattern is not None:
            p_el = ET.Element("pattern")
            p_el.text = self.pattern
            root.append(p_el)

        if self.list_var is not None:
            for item in self.list_var:
                item_el = ET.Element("list")
                item_el.text = item
                root.append(item_el)

        lo_el = ET.Element("list_open")
        lo_el.text = str(self.list_open).lower()
        root.append(lo_el)

        if self.assumed_value is not None:
            av_el = ET.Element("assumed_value")
            av_el.text = self.assumed_value
            root.append(av_el)

        return root
    
    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        lo = (root.findtext("./list_open") == "true")
        pattern = root.findtext("./pattern")
        list_var = None
        list_els = root.findall("./list")
        if len(list_els) > 0:
            list_var = [item.text for item in list_els]
        av = root.findtext("./assumed_value")
        return CString(lo, pattern, list_var, av)
    
    def default_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

class CInteger(CPrimitive):
    """Constraint on instances of Integer."""

    list_var : Optional[list[np.int32]]
    """Set of Integers specifying constraint."""

    range: Optional[Interval[np.int32]]
    """Range of Integers specifying constraint."""

    assumed_value: Optional[np.int32]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, list_var: Optional[list[np.int32]] = None, range: Optional[Interval[np.int32]] = None, assumed_value : Optional[np.int32] = None, **kwargs):
        self.list_var = list_var
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.list_var, other.list_var) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))
    
    def as_json(self):
        draft = {}
        if self.list_var is not None:
            draft["list"] = self.list_var
        if self.range is not None:
            draft["range"] = self.range.as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value
        draft["_type"] = "C_INTEGER"
        return draft

    def as_xml(self, root_tag=None):
        tag = "c_integer" if root_tag is None else root_tag
        root = ET.Element(tag)

        if self.list_var is not None:
            for item in self.list_var:
                item_el = ET.Element("list")
                item_el.text = str(item)
                root.append(item_el)

        if self.range is not None:
            range_el = self.range.as_xml("range")
            root.append(range_el)

        if self.assumed_value is not None:
            av_el = ET.Element("assumed_value")
            av_el.text = str(self.assumed_value)
            root.append(av_el)

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        list_els = root.findall("./list")
        list_var = None
        if len(list_els) > 0:
            list_var = [np.int32(item.text) for item in list_els if item.text is not None]

        range_el = root.find("./range")
        range_value = None
        if range_el is not None:
            range_value = Interval.from_xml(range_el)

        av = root.findtext("./assumed_value")
        if av is not None:
            av = np.int32(av)

        return CInteger(list_var, range_value, av)
    
    def default_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

class CReal(CPrimitive):
    """Constraint on instances of Rnteger."""

    list_var : Optional[list[np.float32]]
    """Set of Rntegers specifying constraint."""

    range: Optional[Interval[np.float32]]
    """Range of Rntegers specifying constraint."""

    assumed_value: Optional[np.float32]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, list_var: Optional[list[np.float32]] = None, range: Optional[Interval[np.float32]] = None, assumed_value : Optional[np.float32] = None, **kwargs):
        self.list_var = list_var
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.list_var, other.list_var) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))
    
    def as_json(self):
        draft = {}
        if self.list_var is not None:
            draft["list"] = self.list_var
        if self.range is not None:
            draft["range"] = self.range.as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value
        draft["_type"] = "C_REAL"
        return draft

    def as_xml(self, root_tag=None):
        tag = "c_real" if root_tag is None else root_tag
        root = ET.Element(tag)

        if self.list_var is not None:
            for item in self.list_var:
                item_el = ET.Element("list")
                item_el.text = str(item)
                root.append(item_el)

        if self.range is not None:
            range_el = self.range.as_xml("range")
            root.append(range_el)

        if self.assumed_value is not None:
            av_el = ET.Element("assumed_value")
            av_el.text = str(self.assumed_value)
            root.append(av_el)

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        list_els = root.findall("./list")
        list_var = None
        if len(list_els) > 0:
            list_var = [np.float32(item.text) for item in list_els if item.text is not None]

        range_el = root.find("./range")
        range_value = None
        if range_el is not None:
            range_value = Interval.from_xml(range_el)

        av = root.findtext("./assumed_value")
        if av is not None:
            av = np.float32(av)

        return CReal(list_var, range_value, av)
    
    def default_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

class CDate(CPrimitive):
    """ISO 8601-compatible constraint on instances of Date in the form either 
    of a set of validity values, or an actual date range. There is no validity 
    flag for 'year', since it must always be by definition mandatory in order 
    to have a sensible date at all. Syntax expressions of instances of this 
    class include “YYYY-??-??” (date with optional month and day)."""

    day_validity: Optional[ValidityKind]
    """Validity of day in constrained date."""

    month_validity: Optional[ValidityKind]
    """Validity of month in constrained date."""

    timezone_validity: Optional[ValidityKind]
    """Validity of timezone in constrained date."""

    range: Optional[Interval[ISODate]]
    """Interval of Dates specifying constraint."""

    assumed_value: Optional[ISODate]
    """The value to assume if this item is not included in data, due to being part of an optional structure."""

    def __init__(self, month_validity: Optional[ValidityKind] = None, day_validity: Optional[ValidityKind] = None, timezone_validity: Optional[ValidityKind] = None, range: Optional[Interval[ISODate]] = None, assumed_value: Optional[ISODate] = None, **kwargs):
        if month_validity is not None and day_validity is None:
            raise ValueError("If month_validity is provided, day_validity must also be provided (invariant: month_validity_optional)")
        if month_validity is not None:
            if month_validity == ValidityKind.PROHIBITED and day_validity != ValidityKind.PROHIBITED:
                raise ValueError("If month_validity is set to PROHIBITED, day_validity must also be set to PROHIBITED (invariant: month_validity_disallowed)")
            if month_validity == ValidityKind.OPTIONAL and day_validity == ValidityKind.MANDATORY:
                raise ValueError("If month_validity is set to OPTIONAL, day_validity cannot be set to MANDATORY (invariant: month_validity_optional)")
        self.day_validity = day_validity
        self.month_validity = month_validity
        self.timezone_validity = timezone_validity
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.day_validity, other.day_validity) and
                is_equal_value(self.month_validity, other.month_validity) and
                is_equal_value(self.timezone_validity, other.timezone_validity) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))
    
    def as_json(self):
        draft = {}
        if self.day_validity is not None:
            draft["day_validity"] = self.day_validity
        if self.month_validity is not None:
            draft["month_validity"] = self.month_validity
        if self.timezone_validity is not None:
            draft["timezone_validity"] = self.timezone_validity
        if self.range is not None:
            draft["range"] = self.range.as_json()
        draft["_type"] = "C_DATE"

    def as_xml(self, root_tag = None):
        root = ET.Element("c_date" if root_tag is None else root_tag)
        if self.month_validity is not None or self.day_validity is not None:
            pat = "YYYY"
            if self.month_validity is not None:
                if self.month_validity == ValidityKind.MANDATORY:
                    pat += "-MM"
                elif self.month_validity == ValidityKind.PROHIBITED:
                    pat += "-XX"
                else:
                    pat += "-??"
            else:
                pat += "-??"
            if self.day_validity is not None:
                if self.day_validity == ValidityKind.MANDATORY:
                    pat += "-DD"
                elif self.day_validity == ValidityKind.PROHIBITED:
                    pat += "-XX"
                else:
                    pat += "-??"
            else:
                pat += "-??"
            pat_el = ET.Element("pattern")
            pat_el.text = pat
            root.append(pat_el)

        if self.timezone_validity is not None:
            root.append(self.timezone_validity.as_xml("timezone_validity"))

        if self.range is not None:
            root.append(self.range.as_xml("range"))

        if self.assumed_value is not None:
            dat_el = ET.Element("assumed_value")
            dat_el.text = self.assumed_value.value
            root.append(dat_el)

        return root
    
    def from_xml(root: ET.Element, **kwargs):
        pattern = root.findtext("./pattern")
        day_val = None
        month_val = None
        if pattern is not None:
            pat_split = pattern.split("-")
            if pat_split[1] == "XX":
                month_val = ValidityKind.PROHIBITED
            elif pat_split[1] == "??":
                month_val = ValidityKind.OPTIONAL
            elif pat_split[1].upper() == "MM":
                month_val = ValidityKind.MANDATORY

            if pat_split[2] == "XX":
                day_val = ValidityKind.PROHIBITED
            elif pat_split[2] == "??":
                day_val = ValidityKind.OPTIONAL
            elif pat_split[2].upper() == "DD":
                day_val = ValidityKind.MANDATORY
        
        tz_val_el = root.find("./timezone_validity")
        tz_val = ValidityKind.from_xml(tz_val_el) if tz_val_el is not None else None

        rang_el = root.find("./range")
        rang = Interval.from_xml(rang_el, ISODate) if rang_el is not None else None

        ass_val = root.findtext("./assumed_value")
        ass_val = ISODate(ass_val) if ass_val is not None else None

        return CDate(month_val, day_val, tz_val, rang, ass_val)
    
    def default_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()