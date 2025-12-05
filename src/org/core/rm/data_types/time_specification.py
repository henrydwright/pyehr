"""Time specification is about potentiality rather than actuality, and needs its own types. 
The openEHR data_types.time_specification package provides such types, based on the HL7 types 
of the same names."""

from abc import abstractmethod
import re
from typing import Optional, Union
import warnings

from common import PythonTerminologyService, ListCodeSetAccess

from org.core.base.base_types.identification import TerminologyID
from org.core.rm.data_types import DataValue
from org.core.rm.data_types.encapsulated import DVParsable
from org.core.rm.data_types.text import CodePhrase
from org.core.rm.data_types.quantity.date_time import DVDuration, DVDateTime

TERMINOLOGY_ID_CALENDAR_CYCLE = TerminologyID("CalendarCycle")
TERMINOLOGY_ID_TIMING_EVENT = TerminologyID("TimingEvent")

CODELIST_CALENDAR_CYCLE = [
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CD", "day (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CH", "hour (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CM", "month (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CN", "minute (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CS", "second (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CW", "week (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "CY", "year"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "DM", "day of the month"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "DW", "day of the week (begins with Monday)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "DY", "day of the year"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "HD", "hour of the day"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "MY", "month of the year"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "NH", "minute of the hour"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "SN", "second of the minute"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "WM", "week of the month"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "WY", "week of the year"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "D", "day of the month"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "H", "hour of the day"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "J", "day of the week (begins with Monday)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "M", "month of the year"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "N", "minute of the hour"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "S", "second of the minute"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "W", "week (continuous)"),
    CodePhrase(TERMINOLOGY_ID_CALENDAR_CYCLE, "Y", "year")
]
CODELIST_TIMING_EVENT = [
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "AC", "AC"),     # before meal (from lat. ante cibus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ACD", "ACD"),   # before lunch (from lat. ante cibus diurnus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ACM", "ACM"),   # before breakfast (from lat. ante cibus matutinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ACV", "ACV"),   # before dinner (from lat. ante cibus vespertinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "C", "C"),       # meal (from lat. ante cibus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "CD", "CD"),     # lunch (from lat. cibus diurnus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "CM", "CM"),     # breakfast (from lat. cibus matutinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "CV", "CV"),     # dinner (from lat. cibus vespertinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "HS", "HS"),     # Prior to beginning a regular period of extended sleep (this would exclude naps).
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "IC", "IC"),     # between meals (from lat. inter cibus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ICD", "ICD"),   # between lunch and dinner
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ICM", "ICM"),   # between breakfast and lunch
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "ICV", "ICV"),   # between dinner and the hour of sleep
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "PC", "PC"),     # after meal (from lat. post cibus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "PCD", "PCD"),   # after lunch (from lat. post cibus diurnus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "PCM", "PCM"),   # after breakfast (from lat. post cibus matutinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "PCV", "PCV"),   # after dinner (from lat. post cibus vespertinus)
    CodePhrase(TERMINOLOGY_ID_TIMING_EVENT, "WAKE", "WAKE"), # Upon waking up from a regular period of sleep, in order to start regular activities (this would exclude waking up from a nap or temporarily waking up during a period of sleep)
]

CODESET_CALENDAR_CYCLE = ListCodeSetAccess(TERMINOLOGY_ID_CALENDAR_CYCLE.name(), "en", CODELIST_CALENDAR_CYCLE)
CODESET_TIMING_EVENT = ListCodeSetAccess(TERMINOLOGY_ID_TIMING_EVENT.name(), "en", CODELIST_TIMING_EVENT)

TIME_SPEC_TERMINOLOGY_SERVICE = PythonTerminologyService(code_sets=[CODESET_CALENDAR_CYCLE, CODESET_TIMING_EVENT], terminologies=None)

class DVTimeSpecification(DataValue):
    """This is an abstract class of which all timing specifications are specialisations. 
    Specifies points in time, possibly linked to the calendar, or a real world repeating event, 
    such as breakfast."""

    value: DVParsable
    """The specification, in the HL7v3 syntax for PIVL or EIVL types."""

    @abstractmethod
    def __init__(self, value: DVParsable):
        if not isinstance(value, DVParsable):
            raise TypeError("Value must be of type DV_PARSABLE")
        self.value = value
        super().__init__()

    @abstractmethod
    def calendar_alignment(self) -> str:
        """Indicates what prototypical point in the calendar the specification is aligned to, e.g. 
        5th of the month . Empty if not aligned. Extracted from the value' attribute."""
        pass

    @abstractmethod
    def event_alignment(self) -> str:
        """Indicates what real-world event the specification is aligned to if any. Extracted 
        from the `value` attribute."""
        pass

    @abstractmethod
    def institution_specified(self) -> bool:
        """Indicates if the specification is aligned with institution schedules, 
        e.g. a hospital nursing changeover or meal serving times. Extracted from the 
        `value` attribute."""
        pass

    def is_equal(self, other):
        return (
            type(self) == type(other) and
            self.value.is_equal(other.value)
        )
    
    def as_json(self):
        # taken from relevant parts of https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_PERIODIC_TIME_SPECIFICATION.json
        return {
            "value": self.value.as_json()
        }

class DVPeriodicTimeSpecification(DVTimeSpecification):
    """Specifies periodic points in time, linked to the calendar (phase-linked), or a real 
    world repeating event, such as breakfast (event-linked). Based on the HL7v3 data types 
    PIVL<T> and EIVL<T>.

    Used in therapeutic prescriptions, expressed as INSTRUCTIONs in the openEHR model."""

    OPENEHR_PIVL_REGEX = "^\\[(.{4,29})?;(.{4,29})?\\]/\\((.*)\\)(?:@([a-zA-Z][a-zA-Z]?))?( IST)?$"
    OPENEHR_EIVL_REGEX = "^([A-Za-z]{1,4})(?:(\\+|\\-)\\[(P.*)?;(P.*)?\\])?$"

    _calendar_alignment : Optional[str]
    _phase_start : Optional[Union[DVDateTime, DVDuration]]
    _phase_end : Optional[Union[DVDateTime, DVDuration]]
    _phase_width : Optional[DVDuration]
    _period : Optional[DVDuration]
    _event_alignment : Optional[str]
    _after_event : Optional[bool]
    _institution_specified : Optional[bool]

    def __init__(self, value):
        super().__init__(value)
        if (value.formalism != "HL7:PIVL" and value.formalism != "HL7:EIVL"):
            raise ValueError(f"Formalism of value must be 'HL7:PIVL' or 'HL7:EIVL' but \'{value.formalism}\' was given (invariant: value_valid)")
        
        # TODO: The parsing spec does not match with the examples given, have gone with parsing spec but may
        #        need to allow the actual HL7v3 data types spec at a future date...
        
        # based on the spec a PIVL can be represented as [ISODateTime/"";ISODateTime/""]/(ISODuration)@CodePhrase[CalendarCycle]/"" IST/""
        if (value.formalism == "HL7:PIVL"):
            self._event_alignment = None
            self._after_event = None
            if re.match(DVPeriodicTimeSpecification.OPENEHR_PIVL_REGEX, value.value) is None:
                raise ValueError("Given string was not in valid Phase-linked Time Specification Syntax")
            parts = re.split(DVPeriodicTimeSpecification.OPENEHR_PIVL_REGEX, value.value)
            self._phase_start = None
            if (parts[1] is not None):
                self._phase_start = DVDateTime(parts[1])
            self._phase_end = None
            if (parts[2] is not None):
                self._phase_end = DVDateTime(parts[2])
            if (self._phase_start and self._phase_end):
                if (self._phase_start > self._phase_end):
                    raise ValueError("Phase start datetime must be smaller than or equal to the phase end datetime")
                self._phase_width = self._phase_end - self._phase_start
            self._period = DVDuration(parts[3])
            self._calendar_alignment = None
            if (parts[4] is not None):
                calendar_cycle_code_set = TIME_SPEC_TERMINOLOGY_SERVICE.code_set("CalendarCycle")
                if not calendar_cycle_code_set.has_code(parts[4]):
                    raise ValueError(f"Provided alignment of \'{parts[4]}\' was not in the HL7v3 'CalendarCycle' CodeSet")
            self._calendar_alignment = parts[4]
            self._institution_specified = (parts[5] == " IST")
        elif (value.formalism == "HL7:EIVL"):
            self._period = None
            self._calendar_alignment = None
            self._institution_specified = None
            if re.match(DVPeriodicTimeSpecification.OPENEHR_EIVL_REGEX, value.value) is None:
                raise ValueError("Given string was not in valid Event-linked Periodic Time Specification Syntax")
            parts = re.split(DVPeriodicTimeSpecification.OPENEHR_EIVL_REGEX, value.value)
            event_timing_code_set = TIME_SPEC_TERMINOLOGY_SERVICE.code_set("TimingEvent")
            if not event_timing_code_set.has_code(parts[1]):
                raise ValueError(f"Provided event of \'{parts[1]}\' was not in the HL7v3 'TimingEvent' CodeSet")
            self._event_alignment = parts[1]
            self._after_event = None
            if parts[2] is not None:
                self._after_event = (parts[2] == "+")
                self._phase_start = None
                if self._after_event:
                    if parts[3] is not None:
                        self._phase_start = DVDuration(parts[3])
                    self._phase_end = None
                    if parts[4] is not None:
                        self._phase_end = DVDuration(parts[4])
                else:
                    if parts[4] is not None:
                        self._phase_start = DVDuration("-" + parts[4])
                    self._phase_end = None
                    if parts[3] is not None:
                        self._phase_end = DVDuration("-" + parts[3])
                if (self._phase_start and self._phase_end):
                    if (self._phase_start > self._phase_end):
                        raise ValueError("Lower interval duration must be smaller than upper interval duration (e.g. -[PT50m;PT1h] is OK but -[PT50m; PT49m] is not as would result in negative event duration)")
                    self._phase_width = self._phase_end - self._phase_start

    def __str__(self) -> str:
        return self.value.value

    def period(self) -> Optional[DVDuration]:
        """The period of the repetition, computationally derived from the syntax representation. 
        Extracted from the `value` attribute for PIVL otherwise None."""
        return self._period

    def calendar_alignment(self) -> Optional[str]:
        """Calendar alignment extracted from value for PIVL (if present) otherwise None"""
        return self._calendar_alignment
    
    def event_alignment(self) -> Optional[str]:
        """Event alignment extracted from value for EIVL otherwise None"""
        return self._event_alignment
    
    def institution_specified(self) -> Optional[bool]:
        """Extracted from value for PIVL otherwise None"""
        return self._institution_specified
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_PERIODIC_TIME_SPECIFICATION.json
        draft = super().as_json()
        draft["_type"] = "DV_PERIODIC_TIME_SPECIFICATION"
        return draft
    
class DVGeneralTimeSpecification(DVTimeSpecification):
    """Specifies points in time in a general syntax. Based on the HL7v3 GTS data type."""

    def __init__(self, value):
        super().__init__(value)
        if (value.formalism != "HL7:GTS"):
            raise ValueError(f"Formalism must be set to 'HL7:GTS' but \'{value.formalism}\' was given")
        warnings.warn("DVGeneralTimeSpecification does not parse input, so cannot be sure if input was valid GTS value.", category=RuntimeWarning, stacklevel=2)

    def calendar_alignment(self):
        raise NotImplementedError("DVGeneralTimeSpecification has not implemented parsing its input value, so calendar_alignment() is not supported")
    
    def event_alignment(self):
        raise NotImplementedError("DVGeneralTimeSpecification has not implemented parsing its input value, so event_alignment() is not supported")
    
    def institution_specified(self):
        raise NotImplementedError("DVGeneralTimeSpecification has not implemented parsing its input value, so institution_specified() is not supported")
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_GENERAL_TIME_SPECIFICATION.json
        draft = super().as_json()
        draft["_type"] = "DV_GENERAL_TIME_SPECIFICATION"
        return draft
