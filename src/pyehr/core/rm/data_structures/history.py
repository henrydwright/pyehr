"""The `history` package defines classes which formalise the concept of past, 
linear time, via which historical data of any structural complexity can be 
recorded. It supports both instantaneous and interval event samples within 
periodic and aperiodic series."""

from abc import abstractmethod
from typing import Optional

import numpy as np

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalProcessedPath
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

class History(DataStructure):
    
    origin: DVDateTime
    """Time origin of this event history. The first event is not necessarily at the origin point."""

    def __init__(self, name, archetype_node_id, origin, uid = None, links = None, archetype_details = None, feeder_audit = None, parent = None, parent_container_attribute_name = None, **kwargs):
        self.origin = origin
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def as_json(self):
        pass

    def as_hierarchy(self):
        pass

    def item_at_path(self, a_path):
        pass

    def items_at_path(self, a_path):
        pass

    def path_exists(self, a_path):
        pass
    
    def path_unique(self, a_path):
        pass

    def is_equal(self, other):
        pass