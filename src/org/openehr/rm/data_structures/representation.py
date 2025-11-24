"""This package contains classes for a simple hierarchical representation 
of any data structure. Compatible with the ISO 13606-1 classes of the same 
names"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.base_types.identification import UIDBasedID
from org.openehr.rm.common.archetyped import FeederAudit, Locatable, Link, Archetyped, Pathable
from org.openehr.rm.data_types.text import DVText, DVCodedText
from org.openehr.rm.data_types import DataValue
from org.openehr.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

class Item(Locatable):
    """The abstract parent of CLUSTER and ELEMENT representation classes."""

    @abstractmethod    
    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

class Cluster(Item):
    """The grouping variant of ITEM, which may contain further instances of 
    ITEM, in an ordered list."""

    items: list[Item]
    """Ordered list of items - CLUSTER or ELEMENT objects - under this CLUSTER."""

    def __init__(self, 
            name: DVText, 
            archetype_node_id: str,
            items: list[Item], 
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        self.items = items
        
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

class Element(Item):
    """The leaf variant of ITEM, to which a DATA_VALUE instance is attached."""

    value : Optional[DataValue]
    """Property representing leaf value object of ELEMENT. In real data, any concrete 
    subtype of DATA_VALUE can be used."""

    null_flavour: Optional[DVCodedText]
    """Flavour of null value, e.g. 253|unknown|, 271|no information|, 272|masked| and 273|not applicable|."""

    null_reason: Optional[DVText]
    """Optional specific reason for null value; if set, null_flavour must be set. Null reason may apply only 
    to a minority of clinical data, commonly needed in reporting contexts."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                value: Optional[DataValue] = None,
                null_flavour: Optional[DVCodedText] = None,
                null_reason: Optional[DVText] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                terminology_service: Optional[TerminologyService] = None,
                **kwargs):
        
        if value is not None:
            if null_flavour is not None or null_reason is not None:
                raise ValueError("If value is provided, null_flavour and null_reason must not be given (invariant: null_flavour_indicated, null_reason_valid)")
        else:
            if terminology_service is None:
                raise ValueError("If value is null, terminology service must be provided to check valid null flavour")
            if null_flavour is None:
                raise ValueError("If value is null, null flavour must be provided (invariant: null_flavour_indiacted)")
            util_verify_code_in_openehr_terminology_group_or_error(null_flavour.defining_code, OpenEHRTerminologyGroupIdentifiers.GROUP_ID_NULL_FLAVOURS, terminology_service, "null_flavour_valid")
        self.value = value
        self.null_flavour = null_flavour
        self.null_reason = null_reason

        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_null(self) -> bool:
        """True if value logically not known, e.g. if indeterminate, not asked etc."""
        return (self.value is None)
    
    def path_exists(self, a_path):
        return (a_path == "" or a_path == "value")
        
    def item_at_path(self, a_path):
        if a_path == "":
            return self
        elif a_path == "value":
            return self.value
        else:
            raise ValueError(f"Item not found: only 'value' exists at element, not {a_path}")
        
    def items_at_path(self, a_path):
        raise ValueError("Items not found: element reached with single value and no children")
    
    def path_unique(self, a_path):
        return (a_path == "" or a_path == "value")
    