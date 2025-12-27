"""The `item_structure` package classes are a formalisation of the need for 
generic, archetypable data structures, and are used by all openEHR 
reference models."""

from abc import abstractmethod
from typing import Optional

import numpy as np

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Link, Archetyped, Pathable, FeederAudit, PyehrInternalProcessedPath, PyehrInternalPathPredicateType
from pyehr.core.rm.data_structures import DataStructure
from pyehr.core.rm.data_structures.representation import Element, Cluster
from pyehr.core.rm.data_types.text import DVText

class ItemStructure(DataStructure):
    """Abstract parent class of all spatial data types."""

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

class ItemSingle(ItemStructure):
    """Logical single value data structure. Used to represent any data which is 
    logically a single value, such as a person's height or weight."""

    item: Element

    def __init__(self, 
            name: DVText, 
            archetype_node_id: str, 
            item: Element,
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        item._parent = self
        item._parent_container_attribute_name = "item"
        self.item = item
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return self
        
        if path.current_node_attribute == "item":
            return self.item.item_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Item not found: expected 'item' at ItemSingle but got \'{path.current_node_attribute}\'")
            
    def items_at_path(self, a_path):
        raise ValueError("Items not found: path would always result in single item, not multiple items")

    def path_exists(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "item":
            return self.item.path_exists(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
               
    def path_unique(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "item":
            return self.item.path_unique(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
            
    def as_hierarchy(self):
        return self.item
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/ITEM_SINGLE.json
        draft = super().as_json()
        draft["item"] = self.item.as_json()
        draft["_type"] = "ITEM_SINGLE"
        return draft
    
class ItemList(ItemStructure):
    """Logical list data structure, where each item has a value and can be 
    referred to by a name and a positional index in the list. The list may be empty.

    ITEM_LIST is used to represent any data which is logically a list of values, 
    such as blood pressure, most protocols, many blood tests etc.

    Not to be used for time-based lists, which should be represented with the 
    proper temporal class, i.e. HISTORY."""

    _items_name_dict : Optional[dict[str, Element]]
    """Internal map of name to elements"""

    _items_archid_dict: Optional[dict[str, Element]]
    """Internal map of archetype_node_id to elements"""

    def _get_items(self):
        return list(self._items_name_dict.values())

    items = property(
        fget=_get_items
    )
    """Physical representation of the list."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str, 
        items: Optional[list[Element]],
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        archetype_details : Optional[Archetyped] = None,
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
            if items is not None:
                self._items_name_dict = dict()
                self._items_archid_dict = dict()
                for item in items:
                    item._parent = self
                    item._parent_container_attribute_name = "items"
                    self._items_name_dict[item.name.value] = item
                    self._items_archid_dict[item.archetype_node_id] = item
            else:
                self._items_name_dict = None
            super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_count(self) -> np.int32:
        """Count of all items."""
        return np.int32(len(self.items))
    
    def names(self) -> Optional[list[DVText]]:
        """Retrieve the names of all items."""
        if self._items_name_dict is None:
            return None
        else:
            return [item.name for item in self.items]
        
    def named_item(self, a_name : str) -> Element:
        """Retrieve the item with name `a_name`."""
        if self._items_name_dict is None:
            raise ValueError("Cannot retrieve item from empty ITEM_LIST")
        elif a_name in self._items_name_dict:
            return self._items_name_dict[a_name]
        else:
            raise ValueError(f"Item not found: Named item \'{a_name}\' not found in this item list")
        
    def _archid_item(self, a_id : str) -> Element:
        if self._items_archid_dict is None:
            raise ValueError("Cannot retrieve item from empty ITEM_LIST")
        elif a_id in self._items_archid_dict:
            return self._items_archid_dict[a_id]
        else:
            raise ValueError(f"Item not found: Item with archetype node ID \'{a_id}\' not found in this item list")

    def _pred_item(self, pred, pred_type: PyehrInternalPathPredicateType):
        if pred_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
            return self._archid_item(pred)
        elif pred_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
            return self.ith_item(int(pred))
        else:
            raise ValueError(f"Cannot process path with predicate of type \'{str(pred_type)}\'")
            
    def ith_item(self, i: np.int32) -> Element:
        """Retrieve the i-th item with name."""
        if self._items_name_dict is None:
            raise ValueError("Item not found: Cannot retrieve item from empty ITEM_LIST")
        else:
            return self.items[i]
        
    def as_hierarchy(self):
        """Generate a CEN EN13606-compatible hierarchy consisting of a single 
        CLUSTER containing the ELEMENTs of this list."""
        return Cluster(
            name=self.name,
            archetype_node_id=self.archetype_node_id,
            items=self.items,
            uid=self.uid,
            links=self.links,
            archetype_details=self.archetype_details,
            feeder_audit=self.feeder_audit
        )
    
    def item_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return self
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None:
                raise ValueError(f"Item not found: path led to potentially multiple items")            
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).item_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Item not found: expected 'items' at ItemList but got \'{path.current_node_attribute}\'")
    
    def items_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            raise ValueError("Items not found: path led to a single ITEM_LIST")
        
        if path.current_node_attribute == "items":
            if path.remaining_path is None:
                # leaf
                if path.current_node_predicate is not None:
                    raise ValueError(f"Items not found: path led to single item")
                return self.items
            else:
                # intermediate
                if path.current_node_predicate is None:
                    raise ValueError("Invalid path: ambiguous path provided - item in list not specified")
                return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).items_at_path(path.remaining_path)
        else:
            raise ValueError(f"Items not found: expected 'items' at ItemList but got \'{path.current_node_attribute}\'")
        
    def path_exists(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None and path.remaining_path is None:
                return True           
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).path_exists(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
    
    def path_unique(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None and path.remaining_path is None:
                return False      
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).path_unique(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
            
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/ITEM_LIST.json
        draft = super().as_json()
        if self.items is not None:
            draft["items"] = [e.as_json() for e in self.items]
        draft["_type"] = "ITEM_LIST"
        return draft
    
class ItemTable(ItemStructure):
    """Logical relational database style table data structure, in which columns 
    are named and ordered with respect to each other. Implemented using 
    Cluster-per-row encoding. Each row Cluster must have an identical number 
    of Elements, each of which in turn must have identical names and value 
    types in the corresponding positions in each row.
    
    Some columns may be designated key' columns, containing key data for each 
    row, in the manner of relational tables. This allows row-naming, where each 
    row represents a body site, a blood antigen etc. All values in a column have 
    the same data type.
    
    Used for representing any data which is logically a table of values, such as 
    blood pressure, most protocols, many blood tests etc.
    
    Misuse: Not to be used for time-based data, which should be represented with 
    the temporal class HISTORY. The table may be empty."""
    pass