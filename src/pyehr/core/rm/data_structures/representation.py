"""This package contains classes for a simple hierarchical representation 
of any data structure. Compatible with the ISO 13606-1 classes of the same 
names"""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import FeederAudit, Locatable, Link, Archetyped, Pathable, PyehrInternalPathPredicateType, PyehrInternalProcessedPath
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

        if path.current_node_attribute == "items":
            if path.current_node_predicate_type is None:
                ret_item = self.items
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
                ret_item = self.items[int(path.current_node_predicate)]
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
                matches = []
                for item in self.items:
                    if item.archetype_node_id == path.current_node_predicate:
                        matches.append(item)
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
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'items' at ITEM_TREE but found \'{path.current_node_attribute}\'")
        
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

    