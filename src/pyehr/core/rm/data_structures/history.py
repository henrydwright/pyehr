"""The `history` package defines classes which formalise the concept of past, 
linear time, via which historical data of any structural complexity can be 
recorded. It supports both instantaneous and interval event samples within 
periodic and aperiodic series."""

from abc import abstractmethod
from typing import Optional

import numpy as np

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalPathPredicateType, PyehrInternalProcessedPath
from pyehr.core.rm.data_structures import DataStructure
from pyehr.core.rm.data_structures.item_structure import ItemStructure
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime, DVDuration
from pyehr.core.rm.data_types.text import DVCodedText, DVText
from pyehr.core.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

class Event[T : ItemStructure](Locatable):
    """Defines the abstract notion of a single event in a series. This class 
    is generic, allowing types to be generated which are locked to particular 
    spatial types, such as EVENT<ITEM_LIST>. Subtypes express point or intveral 
    data."""

    time : DVDateTime
    """Time of this event. If the width is non-zero, it is the time point of 
    the trailing edge of the event."""

    state: Optional[ItemStructure]
    """Optional state data for this event."""

    data: T
    """The data of this event."""

    @abstractmethod
    def __init__(self, 
                 name: DVText, 
                 archetype_node_id: str, 
                 time: DVDateTime,
                 data: T,
                 parent: 'History',
                 state: Optional[ItemStructure] = None,
                 uid : Optional[UIDBasedID] = None, 
                 links : Optional[list[Link]] = None,  
                 archetype_details : Optional[Archetyped] = None,
                 feeder_audit : Optional[FeederAudit] = None,
                 parent_container_attribute_name: Optional[str] = None,
                 **kwargs):
        self.time = time
        self.data = data
        self.state = state
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def offset(self) -> DVDuration:
        return self.time.diff(self.parent().origin)
    
    @abstractmethod
    def as_json(self):
        # intermediate step has no schema
        draft = super().as_json()
        draft["time"] = self.time.as_json()
        draft["data"] = self.data.as_json()
        if self.state:
            draft["state"] = self.state.as_json()
        return draft
    
    def item_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            return self
        
        if path.current_node_attribute == "data":
            return self.data.item_at_path(path.remaining_path if path.remaining_path is not None else "")
        elif path.current_node_attribute == "state":
            return self.state.item_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Item not found: expected 'data' or 'state' at EVENT but got \'{path.current_node_attribute}\'")
    
    def items_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            raise ValueError("Items not found: path resulted in single item (EVENT)")
        
        if path.current_node_attribute == "data":
            return self.data.items_at_path(path.remaining_path if path.remaining_path is not None else "")
        elif path.current_node_attribute == "state":
            return self.state.items_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Items not found: expected 'data' or 'state' at EVENT but got \'{path.current_node_attribute}\'")
    
    def path_exists(self, a_path):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "data":
            return self.data.path_exists(path.remaining_path if path.remaining_path is not None else "")
        elif path.current_node_attribute == "state":
            return self.state.path_exists(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
    
    def path_unique(self, a_path):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "data":
            return self.data.path_unique(path.remaining_path if path.remaining_path is not None else "")
        elif path.current_node_attribute == "state":
            return self.state.path_unique(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
    
class PointEvent[T: ItemStructure](Event[T]):
    """Defines a single point event in a series."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                time: DVDateTime,
                data: T,
                parent: 'History',
                state: Optional[ItemStructure] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        super().__init__(name, archetype_node_id, time, data, parent, state, uid, links, archetype_details, feeder_audit, parent_container_attribute_name, **kwargs)

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/POINT_EVENT.json
        draft = super().as_json()
        draft["_type"] = "POINT_EVENT"
        return draft
    
class IntervalEvent[T: ItemStructure](Event[T]):
    """Defines a single interval event in a series."""

    width: DVDuration
    """Duration of the time interval during which the values recorded under data 
    are true and, if set, the values recorded under state are true. Void if an 
    instantaneous event."""

    sample_count: Optional[np.int32]
    """Optional count of original samples to which this event corresponds."""

    math_function: DVCodedText
    """Mathematical function of the data of this event, e.g. maximum, mean etc. 
    Coded using openEHR vocabulary event math function. 
    Default value 640|actual|, meaning 'actual value'."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                time: DVDateTime,
                data: T,
                width: DVDuration,
                math_function: DVCodedText,
                terminology_service: TerminologyService,
                parent: 'History',
                sample_count: Optional[np.int32] = None,
                state: Optional[ItemStructure] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        self.width = width
        util_verify_code_in_openehr_terminology_group_or_error(
            code=math_function.defining_code,
            terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_EVENT_MATH_FUNCTION,
            terminology_service=terminology_service,
            invariant_name_for_error="math_function_validity"
        )
        self.math_function = math_function
        self.sample_count = sample_count
        super().__init__(name, archetype_node_id, time, data, parent, state, uid, links, archetype_details, feeder_audit, parent_container_attribute_name, **kwargs)

    def interval_start_time(self) -> DVDateTime:
        """Start time of the interval of this event."""
        return self.time - self.width
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/INTERVAL_EVENT.json
        draft = super().as_json()
        draft["width"] = self.width.as_json()
        draft["math_function"] = self.math_function.as_json()
        if self.sample_count is not None:
            draft["sample_count"] = self.sample_count
        draft["_type"] = "INTERVAL_EVENT"
        return draft

class History[T : ItemStructure](DataStructure):
    """Root object of a linear history, i.e. time series structure. This is a 
    generic class whose type parameter must be a descendant of ITEM_STRUCTURE, 
    ensuring that each Event in the events of a given instance is of the same 
    structural type, i.e. ITEM_TREE, ITEM_LIST etc.

    For a periodic series of events, period will be set, and the time of each 
    Event in the History must correspond; i.e. the EVENT.offset must be a multiple
    of period for each Event. Missing events in a period History are however 
    allowed."""
    
    origin: DVDateTime
    """Time origin of this event history. The first event is not necessarily at 
    the origin point."""

    period: Optional[DVDuration]
    """Period between samples in this segment if periodic."""

    duration: Optional[DVDuration]
    """Duration of the entire History; either corresponds to the duration of all 
    the events, and/or the duration represented by the summary, if it exists."""

    summary: Optional[ItemStructure]
    """Optional summary data that aggregates, organizes, reduces and transforms 
    the event series. This may be a text or image that presents a graphical 
    presentation, or some data that assists with the interpretation of the data."""

    events: Optional[list[Event[T]]]
    """The events in the series. This attribute is of a generic type whose 
    parameter must be a descendant of ITEM_SUTRUCTURE."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                origin: DVDateTime,
                period: Optional[DVDuration] = None,
                duration: Optional[DVDuration] = None,
                summary: Optional[ItemStructure] = None,
                events: Optional[list[Event[T]]] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        self.origin = origin
        self.period = period
        self.duration = duration
        self.summary = summary
        if events is not None:
            if len(events) == 0:
                raise ValueError("If events is provided it cannot be an empty list (invariant: events_valid)")
        self.events = events
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_periodic(self) -> bool:
        """Indicates whether history is periodic."""
        return self.period is not None

    def as_json(self):
        pass

    def as_hierarchy(self):
        pass

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ITEM_TREE)")
        
        ret_item = None

        if path.current_node_attribute == "events":
            if path.current_node_predicate_type is None:
                ret_item = self.events
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
                ret_item = self.events[int(path.current_node_predicate)]
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
                matches = []
                for event in self.events:
                    if event.archetype_node_id == path.current_node_predicate:
                        matches.append(event)
                if len(matches) == 0:
                    ret_item = None
                elif len(matches) == 1:
                    ret_item = matches[0]
                else:
                    ret_item = matches

            if path.remaining_path is None:
                if check_only:
                    return (ret_item is not None)
                if single_item:
                    if ret_item is not None and not isinstance(ret_item, list):
                        return ret_item
                    else:
                        raise ValueError("Item not found: multiple items returned by query.")
                else:
                    if isinstance(ret_item, list):
                        return ret_item
                    else:
                        raise ValueError("Items not found: single item returned by query")
            else:
                if isinstance(ret_item, list):
                    raise ValueError("Path invalid: ambiguous intermediate path step containing multiple items")
                else:
                    if check_only:
                        return ret_item.path_exists(path.remaining_path)
                    if single_item:
                        return ret_item.item_at_path(path.remaining_path)
                    else:
                        return ret_item.items_at_path(path.remaining_path)
        elif path.current_node_attribute == "summary":
            if check_only:
                return self.summary.path_exists(path.remaining_path if path.remaining_path is not None else "")
            if single_item:
                return self.summary.item_at_path(path.remaining_path if path.remaining_path is not None else "")
            else:
                return self.summary.items_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'events' or 'summary' at HISTORY but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False

    def is_equal(self, other: 'History'):
        return (super().is_equal(other) and
                is_equal_value(self.origin, other.origin) and
                is_equal_value(self.period, other.period) and
                is_equal_value(self.duration, other.duration) and
                is_equal_value(self.summary, other.summary) and
                is_equal_value(self.events, other.events))