"""This package contains classes for a simple hierarchical representation 
of any data structure. Compatible with the ISO 13606-1 classes of the same 
names"""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import FeederAudit, Locatable, Link, Archetyped, Pathable
from pyehr.core.rm.data_types.text import DVText, DVCodedText
from pyehr.core.rm.data_types import DataValue
from pyehr.core.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

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

    _items_dict: dict[str, Item]
    """dict of items keyed by archetype_node_id"""

    def _get_items(self):
        return list(self._items_dict.values())

    items = property(
        fget=_get_items
    )
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
        self._items_dict = dict()
        for item in items:
            item._parent = self
            item._parent_container_attribute_name = "items"
            self._items_dict[item.archetype_node_id] = item
        
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_at_path(self, a_path):
        if a_path == "":
            return self
        pth = a_path.split("/")

        current_node = pth[0]
        current_node_split = current_node.replace("]", "").split("[")

        attr = current_node_split[0]
        pred = None
        if len(current_node_split) > 1:
            pred = current_node_split[1]
        
        if len(pth) == 1:
            # leaf
            if attr == "items":
                if pred is None:
                    raise ValueError(f"Item not found: path results in multiple items, not single item")
                else:
                    if pred in self._items_dict:
                        return self._items_dict[pred]
                    else:
                        raise ValueError("Item not found: no item with given archetype_node_id was present in Cluster")
            else:
                raise ValueError(f"Item not found: expected 'items' at Cluster but got \'{attr}\'")
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "items":
                if pred is None:
                    raise ValueError(f"Invalid path: path was ambiguous as no specific item in the cluster was given")
                else:
                    if pred in self._items_dict:
                        return self._items_dict[pred].item_at_path(next_pth)
                    else:
                        raise ValueError("Item not found: no item with given archetype_node_id was present in Cluster")
            else:
                raise ValueError(f"Item not found: expected 'items' at Cluster but got \'{attr}\'")

    
    def items_at_path(self, a_path):
        if a_path == "":
            raise ValueError("Items not found: path results in single item, not multiple items")
        pth = a_path.split("/")

        current_node = pth[0]
        current_node_split = current_node.replace("]", "").split("[")

        attr = current_node_split[0]
        pred = None
        if len(current_node_split) > 1:
            pred = current_node_split[1]
        
        if len(pth) == 1:
            # leaf
            if attr == "items":
                if pred is None:
                    return self.items
                else:
                    raise ValueError("Items not found: path results in a single item, not multiple items")
            else:
                raise ValueError(f"Items not found: expected 'items' at Cluster but got \'{attr}\'")
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "items":
                if pred is None:
                    raise ValueError(f"Invalid path: path was ambiguous as no specific item in the cluster was given")
                else:
                    if pred in self._items_dict:
                        return self._items_dict[pred].items_at_path(next_pth)
                    else:
                        raise ValueError("Items not found: no item with given archetype_node_id was present in Cluster")
            else:
                raise ValueError(f"Items not found: expected 'items' at Cluster but got \'{attr}\'")
    
    def path_exists(self, a_path):
        if a_path == "":
            return True
        pth = a_path.split("/")

        current_node = pth[0]
        current_node_split = current_node.replace("]", "").split("[")

        attr = current_node_split[0]
        pred = None
        if len(current_node_split) > 1:
            pred = current_node_split[1]
        
        if len(pth) == 1:
            # leaf
            if attr == "items":
                if pred is None:
                    return True
                else:
                    return (pred in self._items_dict)
            else:
                return False
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "items":
                if pred is None:
                    return False
                else:
                    if pred in self._items_dict:
                        return self._items_dict[pred].path_exists(next_pth)
                    else:
                        return False
            else:
                return False
    
    def path_unique(self, a_path):
        if a_path == "":
            return True
        pth = a_path.split("/")

        current_node = pth[0]
        current_node_split = current_node.replace("]", "").split("[")

        attr = current_node_split[0]
        pred = None
        if len(current_node_split) > 1:
            pred = current_node_split[1]
        
        if len(pth) == 1:
            # leaf
            if attr == "items":
                if pred is None:
                    return False
                else:
                    return True
            else:
                return False
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "items":
                if pred is None:
                    return False
                else:
                    if pred in self._items_dict:
                        return self._items_dict[pred].path_unique(next_pth)
                    else:
                        return True
            else:
                return False
            
    def as_json(self):
        draft = super().as_json()
        draft["items"] = [item.as_json() for item in self.items]
        draft["_type"] = "CLUSTER"
        return draft

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
    
    def as_json(self):
        draft = super().as_json()
        if self.value is not None:
            draft["value"] = self.value.as_json()
        if self.null_reason is not None:
            draft["null_reason"] = self.null_reason.as_json()
        if self.null_flavour is not None:
            draft["null_flavour"] = self.null_flavour.as_json()
        draft["_type"] = "ELEMENT"
        return draft

    