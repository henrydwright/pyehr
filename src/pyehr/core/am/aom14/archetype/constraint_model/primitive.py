
from abc import abstractmethod
from typing import Optional

import xml.etree.ElementTree as ET

import numpy as np
import re

from pyehr.core.base.base_types.definitions import ValidityKind
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
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

    list_open: Optional[bool]
    """True if the list is being used to specify the constraint but is not 
    considered exhaustive."""

    assumed_value: Optional[str]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, list_open: Optional[bool] = None, pattern: Optional[str] = None, list_var: Optional[list[str]] = None, assumed_value : Optional[str] = None, **kwargs):
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
        draft = {}
        if self.list_open is not None:
            draft["list_open"] = self.list_open
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

        if self.list_open is not None:
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
        lo = root.findtext("./list_open")
        lo = (lo.lower() == "true") if lo is not None else None
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
    
    def validity_is_range(self) -> bool:
        """True if validity is in the form of a range; useful for developers to 
        check which kind of constraint has been set."""
        return self.range is not None
    
class CTime(CPrimitive):
    """ISO 8601-compatible constraint on instances of Time. There is no validity 
    flag for 'hour', since it must always be by definition mandatory in order to 
    have a sensible time at all. Syntax expressions of instances of this class 
    include “HH:??:xx” (time with optional minutes and seconds not allowed)."""

    minute_validity: Optional[ValidityKind]
    """Validity of minute in constrained time."""

    second_validity: Optional[ValidityKind]
    """Validity of second in constrained time."""

    # although this exists in the AM, it isn't covered in the XML spec, so excluding it here

    # millisecond_validity: Optional[ValidityKind]
    # """Validity of millisecond in constrained time."""

    timezone_validity: Optional[ValidityKind]
    """Validity of timezone in constrained date."""

    range: Optional[Interval[ISOTime]]
    """Interval of Times specifying constraint."""

    assumed_value: Optional[ISOTime]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, minute_validity: Optional[ValidityKind] = None, second_validity: Optional[ValidityKind] = None, timezone_validity: Optional[ValidityKind] = None, range: Optional[Interval[ISOTime]] = None, assumed_value: Optional[ISOTime] = None, **kwargs):
        if minute_validity is not None and second_validity is None:
            raise ValueError("If minute_validity is provided, second_validity must also be provided (invariant: minute_validity_optional)")
        if minute_validity is not None:
            if minute_validity == ValidityKind.PROHIBITED and second_validity != ValidityKind.PROHIBITED:
                raise ValueError("If minute_validity is set to PROHIBITED, second_validity must also be set to PROHIBITED (invariant: minute_validity_disallowed)")
            if minute_validity == ValidityKind.OPTIONAL and second_validity == ValidityKind.MANDATORY:
                raise ValueError("If minute_validity is set to OPTIONAL, second_validity cannot be set to MANDATORY (invariant: minute_validity_optional)")
        self.minute_validity = minute_validity
        self.second_validity = second_validity
        self.timezone_validity = timezone_validity
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.minute_validity, other.minute_validity) and
                is_equal_value(self.second_validity, other.second_validity) and
                is_equal_value(self.timezone_validity, other.timezone_validity) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))

    def as_json(self):
        draft = {}
        if self.minute_validity is not None:
            draft["minute_validity"] = self.minute_validity
        if self.second_validity is not None:
            draft["second_validity"] = self.second_validity
        if self.timezone_validity is not None:
            draft["timezone_validity"] = self.timezone_validity
        if self.range is not None:
            draft["range"] = self.range.as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value.value
        draft["_type"] = "C_TIME"
        return draft

    def as_xml(self, root_tag = None):
        root = ET.Element("c_time" if root_tag is None else root_tag)
        if self.minute_validity is not None or self.second_validity is not None:
            pat = "HH"
            if self.minute_validity is not None:
                if self.minute_validity == ValidityKind.MANDATORY:
                    pat += ":MM"
                elif self.minute_validity == ValidityKind.PROHIBITED:
                    pat += ":XX"
                else:
                    pat += ":??"
            else:
                pat += ":??"
            if self.second_validity is not None:
                if self.second_validity == ValidityKind.MANDATORY:
                    pat += ":SS"
                elif self.second_validity == ValidityKind.PROHIBITED:
                    pat += ":XX"
                else:
                    pat += ":??"
            else:
                pat += ":??"
            pat_el = ET.Element("pattern")
            pat_el.text = pat
            root.append(pat_el)

        if self.timezone_validity is not None:
            root.append(self.timezone_validity.as_xml("timezone_validity"))

        if self.range is not None:
            root.append(self.range.as_xml("range"))

        if self.assumed_value is not None:
            time_el = ET.Element("assumed_value")
            time_el.text = self.assumed_value.value
            root.append(time_el)

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        pattern = root.findtext("./pattern")
        minute_val = None
        second_val = None
        if pattern is not None:
            # Pattern format: HH:MM:SS.zzz
            pat_split = pattern.split(":")
            # Parse minute validity (second element)
            if len(pat_split) > 1:
                if pat_split[1] == "XX":
                    minute_val = ValidityKind.PROHIBITED
                elif pat_split[1] == "??":
                    minute_val = ValidityKind.OPTIONAL
                elif pat_split[1].upper() == "MM":
                    minute_val = ValidityKind.MANDATORY
            
            # Parse second validity (third element)
            if len(pat_split) > 2:
                second_part = pat_split[2]
                if second_part == "XX":
                    second_val = ValidityKind.PROHIBITED
                elif second_part == "??":
                    second_val = ValidityKind.OPTIONAL
                elif second_part.upper() == "SS":
                    second_val = ValidityKind.MANDATORY
        
        tz_val_el = root.find("./timezone_validity")
        tz_val = ValidityKind.from_xml(tz_val_el) if tz_val_el is not None else None

        rang_el = root.find("./range")
        rang = Interval.from_xml(rang_el, ISOTime) if rang_el is not None else None

        ass_val = root.findtext("./assumed_value")
        ass_val = ISOTime(ass_val) if ass_val is not None else None

        return CTime(minute_val, second_val, tz_val, rang, ass_val)

    def default_value(self):
        raise NotImplementedError()

    def valid_value(self, a_value):
        raise NotImplementedError()

    def validity_is_range(self) -> bool:
        """True if validity is in the form of a range; useful for developers to 
        check which kind of constraint has been set."""
        return self.range is not None


class CDateTime(CPrimitive):
    """ISO 8601-compatible constraint on instances of Date_Time. There is no 
    validity flag for 'year', since it must always be by definition mandatory 
    in order to have a sensible date/time at all. Syntax expressions of instances 
    of this class include “YYYY-MM-DDT??:??:??” (date/time with optional time) 
    and “YYYY-MMDDTHH:MM:xx” (date/time, seconds not allowed)."""

    month_validity: Optional[ValidityKind]
    """Validity of month in constrained datetime."""

    day_validity: Optional[ValidityKind]
    """Validity of day in constrained datetime."""

    hour_validity: Optional[ValidityKind]
    """Validity of hour in constrained datetime."""

    minute_validity: Optional[ValidityKind]
    """Validity of minute in constrained datetime."""

    second_validity: Optional[ValidityKind]
    """Validity of second in constrained datetime."""

    timezone_validity: Optional[ValidityKind]
    """Validity of timezone in constrained datetime."""

    range: Optional[Interval[ISODateTime]]
    """Range of Date_times specifying constraint."""

    assumed_value: Optional[ISODateTime]
    """The value to assume if this item is not included in data, due to being part of an optional structure."""

    def __init__(self, month_validity: Optional[ValidityKind] = None, day_validity: Optional[ValidityKind] = None, hour_validity: Optional[ValidityKind] = None, minute_validity: Optional[ValidityKind] = None, second_validity: Optional[ValidityKind] = None, timezone_validity: Optional[ValidityKind] = None, range: Optional[Interval[ISODateTime]] = None, assumed_value: Optional[ISODateTime] = None, **kwargs):
        if month_validity is not None and month_validity == ValidityKind.PROHIBITED:
            raise ValueError("month_validity cannot be set to PROHIBITED (invariant: xml_month_validity)")
        
        if month_validity is not None and day_validity is None:
            raise ValueError("If month_validity is provided, day_validity must also be provided (invariant: month_validity_optional)")
        if day_validity is not None and hour_validity is None:
            raise ValueError("If day_validity is provided, hour_validity must also be provided (invariant: day_validity_optional)")
        if hour_validity is not None and minute_validity is None:
            raise ValueError("If hour_validity is provided, minute_validity must also be provided (invariant: hour_validity_optional)")
        if minute_validity is not None and second_validity is None:
            raise ValueError("If minute_validity is provided, second_validity must also be provided (invariant: minute_validity_optional)")
        if second_validity is not None and minute_validity is None:
            raise ValueError("If second_validity is provided, minute_validity must also be provided (invariant: second_validity_optional)")

        if month_validity is not None:
            if month_validity == ValidityKind.PROHIBITED and (
                day_validity != ValidityKind.PROHIBITED or
                hour_validity != ValidityKind.PROHIBITED or
                minute_validity != ValidityKind.PROHIBITED or
                second_validity != ValidityKind.PROHIBITED
            ):
                raise ValueError("If month_validity is set to PROHIBITED, all later elements must also be set to PROHIBITED (invariant: month_validity_disallowed)")
            if month_validity == ValidityKind.OPTIONAL and (
                day_validity == ValidityKind.MANDATORY or
                hour_validity == ValidityKind.MANDATORY or
                minute_validity == ValidityKind.MANDATORY or
                second_validity == ValidityKind.MANDATORY
            ):
                raise ValueError("If month_validity is set to OPTIONAL, no later element can be set to MANDATORY (invariant: month_validity_optional)")

        if day_validity is not None:
            if day_validity == ValidityKind.PROHIBITED and (
                hour_validity != ValidityKind.PROHIBITED or
                minute_validity != ValidityKind.PROHIBITED or
                second_validity != ValidityKind.PROHIBITED
            ):
                raise ValueError("If day_validity is set to PROHIBITED, all later elements must also be set to PROHIBITED (invariant: day_validity_disallowed)")
            if day_validity == ValidityKind.OPTIONAL and (
                hour_validity == ValidityKind.MANDATORY or
                minute_validity == ValidityKind.MANDATORY or
                second_validity == ValidityKind.MANDATORY
            ):
                raise ValueError("If day_validity is set to OPTIONAL, no later element can be set to MANDATORY (invariant: day_validity_optional)")

        if hour_validity is not None:
            if hour_validity == ValidityKind.PROHIBITED and (
                minute_validity != ValidityKind.PROHIBITED or
                second_validity != ValidityKind.PROHIBITED
            ):
                raise ValueError("If hour_validity is set to PROHIBITED, all later elements must also be set to PROHIBITED (invariant: hour_validity_disallowed)")
            if hour_validity == ValidityKind.OPTIONAL and (
                minute_validity == ValidityKind.MANDATORY or
                second_validity == ValidityKind.MANDATORY
            ):
                raise ValueError("If hour_validity is set to OPTIONAL, no later element can be set to MANDATORY (invariant: hour_validity_optional)")

        if minute_validity is not None:
            if minute_validity == ValidityKind.PROHIBITED and second_validity != ValidityKind.PROHIBITED:
                raise ValueError("If minute_validity is set to PROHIBITED, second_validity must also be set to PROHIBITED (invariant: minute_validity_disallowed)")
            if minute_validity == ValidityKind.OPTIONAL and second_validity == ValidityKind.MANDATORY:
                raise ValueError("If minute_validity is set to OPTIONAL, second_validity cannot be set to MANDATORY (invariant: minute_validity_optional)")

        self.month_validity = month_validity
        self.day_validity = day_validity
        self.hour_validity = hour_validity
        self.minute_validity = minute_validity
        self.second_validity = second_validity
        self.timezone_validity = timezone_validity
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.month_validity, other.month_validity) and
                is_equal_value(self.day_validity, other.day_validity) and
                is_equal_value(self.hour_validity, other.hour_validity) and
                is_equal_value(self.minute_validity, other.minute_validity) and
                is_equal_value(self.second_validity, other.second_validity) and
                is_equal_value(self.timezone_validity, other.timezone_validity) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))

    def as_json(self):
        draft = {}
        if self.month_validity is not None:
            draft["month_validity"] = self.month_validity
        if self.day_validity is not None:
            draft["day_validity"] = self.day_validity
        if self.hour_validity is not None:
            draft["hour_validity"] = self.hour_validity
        if self.minute_validity is not None:
            draft["minute_validity"] = self.minute_validity
        if self.second_validity is not None:
            draft["second_validity"] = self.second_validity
        if self.timezone_validity is not None:
            draft["timezone_validity"] = self.timezone_validity
        if self.range is not None:
            draft["range"] = self.range.as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value.value
        draft["_type"] = "C_DATE_TIME"
        return draft

    def as_xml(self, root_tag = None):
        root = ET.Element("c_date_time" if root_tag is None else root_tag)
        if (self.month_validity is not None or self.day_validity is not None or
                self.hour_validity is not None or self.minute_validity is not None or
                self.second_validity is not None):
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
            if (self.hour_validity is not None or self.minute_validity is not None or
                    self.second_validity is not None):
                pat += "T"
                if self.hour_validity is not None:
                    if self.hour_validity == ValidityKind.MANDATORY:
                        pat += "hh"
                    elif self.hour_validity == ValidityKind.PROHIBITED:
                        pat += "XX"
                    else:
                        pat += "??"
                else:
                    pat += "??"
                pat += ":"
                if self.minute_validity is not None:
                    if self.minute_validity == ValidityKind.MANDATORY:
                        pat += "mm"
                    elif self.minute_validity == ValidityKind.PROHIBITED:
                        pat += "XX"
                    else:
                        pat += "??"
                else:
                    pat += "??"
                pat += ":"
                if self.second_validity is not None:
                    if self.second_validity == ValidityKind.MANDATORY:
                        pat += "ss"
                    elif self.second_validity == ValidityKind.PROHIBITED:
                        pat += "XX"
                    else:
                        pat += "??"
                else:
                    pat += "??"
            pat_el = ET.Element("pattern")
            pat_el.text = pat
            root.append(pat_el)

        if self.timezone_validity is not None:
            root.append(self.timezone_validity.as_xml("timezone_validity"))

        if self.range is not None:
            root.append(self.range.as_xml("range"))

        if self.assumed_value is not None:
            dt_el = ET.Element("assumed_value")
            dt_el.text = self.assumed_value.value
            root.append(dt_el)

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        pattern = root.findtext("./pattern")
        month_val = None
        day_val = None
        hour_val = None
        minute_val = None
        second_val = None
        if pattern is not None:
            pattern_parts = pattern.split("T", 1)
            date_part = pattern_parts[0]
            date_fields = date_part.split("-")
            if len(date_fields) > 1:
                if date_fields[1] == "XX":
                    month_val = ValidityKind.PROHIBITED
                elif date_fields[1] == "??":
                    month_val = ValidityKind.OPTIONAL
                elif date_fields[1].upper() == "MM":
                    month_val = ValidityKind.MANDATORY
            if len(date_fields) > 2:
                if date_fields[2] == "XX":
                    day_val = ValidityKind.PROHIBITED
                elif date_fields[2] == "??":
                    day_val = ValidityKind.OPTIONAL
                elif date_fields[2].upper() == "DD":
                    day_val = ValidityKind.MANDATORY
            if len(pattern_parts) > 1:
                time_fields = pattern_parts[1].split(":")
                if len(time_fields) > 0:
                    if time_fields[0] == "XX":
                        hour_val = ValidityKind.PROHIBITED
                    elif time_fields[0] == "??":
                        hour_val = ValidityKind.OPTIONAL
                    elif time_fields[0].lower() == "hh":
                        hour_val = ValidityKind.MANDATORY
                if len(time_fields) > 1:
                    if time_fields[1] == "XX":
                        minute_val = ValidityKind.PROHIBITED
                    elif time_fields[1] == "??":
                        minute_val = ValidityKind.OPTIONAL
                    elif time_fields[1].lower() == "mm":
                        minute_val = ValidityKind.MANDATORY
                if len(time_fields) > 2:
                    if time_fields[2] == "XX":
                        second_val = ValidityKind.PROHIBITED
                    elif time_fields[2] == "??":
                        second_val = ValidityKind.OPTIONAL
                    elif time_fields[2].lower() == "ss":
                        second_val = ValidityKind.MANDATORY

        tz_val_el = root.find("./timezone_validity")
        tz_val = ValidityKind.from_xml(tz_val_el) if tz_val_el is not None else None

        rang_el = root.find("./range")
        rang = Interval.from_xml(rang_el, ISODateTime) if rang_el is not None else None

        ass_val = root.findtext("./assumed_value")
        ass_val = ISODateTime(ass_val) if ass_val is not None else None

        return CDateTime(month_val, day_val, hour_val, minute_val, second_val, tz_val, rang, ass_val)

    def default_value(self):
        raise NotImplementedError()

    def valid_value(self, a_value):
        raise NotImplementedError()

    def validity_is_range(self) -> bool:
        """True if validity is in the form of a range; useful for developers to 
        check which kind of constraint has been set."""
        return self.range is not None
    
class CDuration(CPrimitive):
    """ISO 8601-compatible constraint on instances of Duration. In ISO 8601 terms, constraints might are of the 
    form “PWD” (weeks and/or days), “PDTHMS” (days, hours, minutes, seconds) and so on.

    Both range and the constraint pattern can be set at the same time, corresponding to the ADL constraint "PWD/|P0W..P50W|".

    As for all of openEHR, two ISO 8601 exceptions are allowed:
    * the 'W' (week) designator can be mixed in - the allowed patterns are: P[Y|y][M|m][D|d][T[H|h][M|m][S|s]] and P[W|w];
    * the values used in an interval constraint may be negated, i.e. a leading minus ('-') sign may be used."""

    # these have cardinality 0..1 in spec but are 1..1 here due to how XML spec is implemented
    #  as the pattern either allows it, or not, nowhere inbetween.

    years_allowed: bool
    """True if years are allowed in the constrained Duration"""

    months_allowed: bool
    """True if months are allowed in the constrained Duration"""

    weeks_allowed: bool
    """True if weeks are allowed in the constrained Duration"""

    days_allowed: bool
    """True if days are allowed in the constrained Duration"""

    hours_allowed: bool
    """True if hours are allowed in the constrained Duration"""

    minutes_allowed: bool
    """True if minutes are allowed in the constrained Duration"""

    seconds_allowed: bool
    """True if seconds are allowed in the constrained Duration"""

    # the spec includes a section for fractional_seconds_allowed but this is
    #  not permitted in the XML so this code does not include it to match

    range: Optional[Interval[ISODuration]]
    """Range of Durations specifying constraint."""

    assumed_value: Optional[ISODuration]
    """The value to assume if this item is not included in data, due to being 
    part of an optional structure."""

    def __init__(self, years_allowed: bool = False, months_allowed: bool = False, weeks_allowed: bool = False, days_allowed: bool = False, hours_allowed: bool = False, minutes_allowed: bool = False, seconds_allowed: bool = False, range: Optional[Interval[ISODuration]] = None, assumed_value: Optional[ISODuration] = None, **kwargs):
        self.years_allowed = years_allowed
        self.months_allowed = months_allowed
        self.weeks_allowed = weeks_allowed
        self.days_allowed = days_allowed
        self.hours_allowed = hours_allowed
        self.minutes_allowed = minutes_allowed
        self.seconds_allowed = seconds_allowed
        self.range = range
        super().__init__(assumed_value, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.years_allowed, other.years_allowed) and
                is_equal_value(self.months_allowed, other.months_allowed) and
                is_equal_value(self.weeks_allowed, other.weeks_allowed) and
                is_equal_value(self.days_allowed, other.days_allowed) and
                is_equal_value(self.hours_allowed, other.hours_allowed) and
                is_equal_value(self.minutes_allowed, other.minutes_allowed) and
                is_equal_value(self.seconds_allowed, other.seconds_allowed) and
                is_equal_value(self.range, other.range) and
                is_equal_value(self.assumed_value, other.assumed_value))

    def as_json(self):
        draft = {}
        if self.years_allowed is not None:
            draft["years_allowed"] = self.years_allowed
        if self.months_allowed is not None:
            draft["months_allowed"] = self.months_allowed
        if self.weeks_allowed is not None:
            draft["weeks_allowed"] = self.weeks_allowed
        if self.days_allowed is not None:
            draft["days_allowed"] = self.days_allowed
        if self.hours_allowed is not None:
            draft["hours_allowed"] = self.hours_allowed
        if self.minutes_allowed is not None:
            draft["minutes_allowed"] = self.minutes_allowed
        if self.seconds_allowed is not None:
            draft["seconds_allowed"] = self.seconds_allowed
        if self.range is not None:
            draft["range"] = self.range.as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value.value
        draft["_type"] = "C_DURATION"
        return draft

    def as_xml(self, root_tag=None):
        root = ET.Element("c_duration" if root_tag is None else root_tag)

        # Build pattern if any of the component flags are present
        if (self.years_allowed or self.months_allowed or
                self.weeks_allowed or self.days_allowed or
                self.hours_allowed or self.minutes_allowed or
                self.seconds_allowed):
            pat = "P"

            # Weeks form uses 'W' exclusively
            if self.years_allowed:
                pat += "Y"
            if self.months_allowed:
                pat += "M"
            if self.weeks_allowed:
                pat += "W"
            if self.days_allowed:
                pat += "D"

            # Time components must be prefixed by 'T'
            if (self.hours_allowed or self.minutes_allowed or self.seconds_allowed):
                pat += "T"
                if self.hours_allowed:
                    pat += "H"
                if self.minutes_allowed:
                    pat += "M"
                if self.seconds_allowed:
                    pat += "S"

            pat_el = ET.Element("pattern")
            pat_el.text = pat
            root.append(pat_el)

        if self.range is not None:
            root.append(self.range.as_xml("range"))

        if self.assumed_value is not None:
            av_el = ET.Element("assumed_value")
            av_el.text = self.assumed_value.value
            root.append(av_el)

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        pattern = root.findtext("./pattern")
        years = False
        months = False
        weeks = False
        days = False
        hours = False
        minutes = False
        seconds = False
        if pattern is not None:
            # Normalize and strip leading 'P' if present
            pat = pattern.strip()
            if len(pat) > 0 and (pat[0] == 'P' or pat[0] == 'p'):
                pat = pat[1:]
            pat = pat.upper()

            date_part = None
            time_part = None
            if 'T' in pat:
                parts = pat.split('T')
                if len(parts[0]) > 0:
                    date_part = parts[0]
                if len(parts[1]) > 0:
                    time_part = parts[1]
            else:
                date_part = pat

            if date_part:
                if 'Y' in date_part:
                    years = True
                if 'M' in date_part:
                    months = True
                if 'W' in date_part:
                    weeks = True
                if 'D' in date_part:
                    days = True

            if time_part:
                if 'H' in time_part:
                    hours = True
                if 'M' in time_part:
                    minutes = True
                if 'S' in time_part:
                    seconds = True

        rang_el = root.find("./range")
        rang = Interval.from_xml(rang_el, ISODuration) if rang_el is not None else None

        ass_val = root.findtext("./assumed_value")
        ass_val = ISODuration(ass_val) if ass_val is not None else None

        return CDuration(years, months, weeks, days, hours, minutes, seconds, rang, ass_val)

    def default_value(self):
        raise NotImplementedError()

    def valid_value(self, a_value):
        raise NotImplementedError()

    