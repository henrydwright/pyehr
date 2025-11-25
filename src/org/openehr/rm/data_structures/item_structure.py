"""The `item_structure` package classes are a formalisation of the need for 
generic, archetypable data structures, and are used by all openEHR 
reference models."""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.base_types.identification import UIDBasedID
from org.openehr.rm.common.archetyped import Link, Archetyped, Pathable, FeederAudit
from org.openehr.rm.data_structures import DataStructure
from org.openehr.rm.data_structures.representation import Element
from org.openehr.rm.data_types.text import DVText

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
            if attr == "item":
                return self.item
            else:
                raise ValueError(f"Item not found: expected 'item' at ItemSingle but got \'{attr}\'")
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "item":
                return self.item.item_at_path(next_pth)
            else:
                raise ValueError(f"Item not found: expected 'item' at ItemSingle but got \'{attr}\'")
            
    def items_at_path(self, a_path):
        raise ValueError("Items not found: path would always result in single item, not multiple items")

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
            if attr == "item":
                return True
            else:
                return False
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "item":
                return self.item.path_exists(next_pth)
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
            if attr == "item":
                return True
            else:
                return False
        else:
            # not leaf
            next_pth = "/".join(pth[1:])
            if attr == "item":
                return self.item.path_unique(next_pth)
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
    