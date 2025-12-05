"""The `directory` package provides a simple abstraction of a versioned folder 
structure."""

from typing import Optional

from org.core.base.foundation_types.any import AnyClass
from org.core.base.base_types.identification import ObjectRef, UIDBasedID
from org.core.rm.common.archetyped import Locatable, Link, Archetyped, FeederAudit, Pathable
from org.core.rm.common.change_control import VersionedObject
from org.core.rm.data_structures.item_structure import ItemStructure
from org.core.rm.data_types.text import DVText
from org.core.base.foundation_types.structure import is_equal_value

class Folder(Locatable):
    """The concept of a named folder."""

    details: Optional[ItemStructure] = None
    """Archetypable meta-data for FOLDER."""

    _folders_dict: Optional[dict[str, 'Folder']] = None
    """Dict of sub-folders keyed by archetype_node_id"""

    def _get_folders(self):
        if self._folders_dict is None:
            return None
        else:
            return list(self._folders_dict.values())
    
    folders = property(
        fget=_get_folders
    )
    """Sub-folders of this FOLDER."""
    
    items: Optional[list[ObjectRef]] = None
    """The list of references to other (usually) versioned objects logically 
    in this folder."""

    def __init__(self, 
                 name: DVText, 
                 archetype_node_id: str, 
                 uid : Optional[UIDBasedID] = None, 
                 links : Optional[list[Link]] = None,  
                 archetype_details : Optional[Archetyped] = None,
                 feeder_audit : Optional[FeederAudit] = None,
                 items: Optional[list[ObjectRef]] = None,
                 folders: Optional[list['Folder']] = None,
                 details: Optional[ItemStructure] = None,
                 parent: Optional[Pathable] = None,
                 parent_container_attribute_name: Optional[str] = None,
                 **kwargs):
        self.items = items

        if folders is not None:
            if len(folders) == 0:
                raise ValueError("If provided, list of sub-folders must not be empty (invariant: folders_valid)")
            self._folders_dict = dict()
            for folder in folders:
                folder._parent = self
                folder._parent_container_attribute_name = "folders"
                self._folders_dict[folder.archetype_node_id] = folder

        self.details = details
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Folder') -> bool:
        return (
            super().is_equal(other) and
            is_equal_value(self.items, other.items) and
            is_equal_value(self.folders, other.folders) and
            is_equal_value(self.details, other.details)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/FOLDER.json
        draft = super().as_json()
        if self.items is not None:
            draft["items"] = [item.as_json() for item in self.items]
        if self.folders is not None:
            draft["folders"] = [folder.as_json() for folder in self.folders]
        if self.details is not None:
            draft["details"] = self.details.as_json()
        draft["_type"] = "FOLDER"
        return draft
    
    def path_exists(self, a_path) -> bool:
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
                    return (self.items is not None)
                
                try:
                    item_idx = int(pred)
                except ValueError:
                    return False
                
                return item_idx < len(self.items)
            elif attr == "folders":
                if pred is None:
                    return (self.folders is not None)
                
                return (self._folders_dict is not None) and (pred in self._folders_dict)
            else:
                return False
        else:
            # not leaf
            if attr == "items":
                try:
                    item_idx = int(pred)
                except ValueError:
                    raise ValueError(f"Invalid path: expected integer index into folder items, instead got \'{pred}\'")
                
                if item_idx >= len(self.items):
                    return False
                elif isinstance(self.items[item_idx], Pathable):
                    next_pth = "/".join(pth[1:])
                    return self.items[item_idx].path_exists(next_pth)
                else:
                    return False
            elif attr == "folders":
                if pred not in self._folders_dict:
                    return False
                else:
                    next_pth = "/".join(pth[1:])
                    return self._folders_dict[pred].path_exists(next_pth)
            else:
                return False

    def item_at_path(self, a_path) -> AnyClass:
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
                    raise ValueError("Item not found: path led to potentially multiple items")
                
                try:
                    item_idx = int(pred)
                except ValueError:
                    raise ValueError(f"Invalid path: items must be indexed by integer but \'{pred}\' was provided")
                
                if item_idx >= len(self.items):
                    raise ValueError(f"Item not found: index for item was out of range in items")
                else:
                    return self.items[item_idx]
            elif attr == "folders":
                if pred is None:
                    raise ValueError("Item not found: path led to potentially multiple folders")
                
                if (self._folders_dict is None):
                    raise ValueError("Item not found: no sub-folders existed at this folder")
                
                if pred not in self._folders_dict:
                    raise ValueError("Item not found: no folder existed with given archetype_node_id")
                else:
                    return self._folders_dict[pred]
            else:
                raise ValueError(f"Invalid path: children of folder are 'items' and 'folders', not \'{attr}\'")
        else:
            # not leaf
            if attr == "items":
                try:
                    item_idx = int(pred)
                except ValueError:
                    raise ValueError(f"Invalid path: expected integer index into folder items, instead got \'{pred}\'")
                
                if item_idx >= len(self.items):
                    raise ValueError(f"Item not found: index for item was out of range in items")
                elif isinstance(self.items[item_idx], Pathable):
                    next_pth = "/".join(pth[1:])
                    return self.items[item_idx].item_at_path(next_pth)
                else:
                    raise ValueError("Invalid path: given item in items was not PATHABLE")
            elif attr == "folders":
                if pred not in self._folders_dict:
                    raise ValueError("Item not found: no folder existed with given archetype_node_id")
                else:
                    next_pth = "/".join(pth[1:])
                    return self._folders_dict[pred].item_at_path(next_pth)
            else:
                raise ValueError(f"Invalid path: children of folder are 'items' and 'folders', not \'{attr}\'")
        
        
    def items_at_path(self, a_path) -> Optional[list[AnyClass]]:
        if a_path == "":
            raise ValueError("Items not found: path led to single item")
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
                    if self.items is None:
                        raise ValueError("Items not found: this folder had no items to return")
                    else:
                        return self.items
                else:
                    raise ValueError("Items not found: path led to single item")
            elif attr == "folders":
                if pred is None:
                    if self.folders is None:
                        raise ValueError("Items not found: this folder had no sub-folders to return")
                    else:
                        return self.folders
                else:
                    raise ValueError("Items not found: path led to single item")
            else:
                raise ValueError(f"Invalid path: children of folder are 'items' and 'folders', not \'{attr}\'")
        else:
            # not leaf
            if attr == "items":
                try:
                    item_idx = int(pred)
                except ValueError:
                    raise ValueError(f"Invalid path: expected integer index into folder items, instead got \'{pred}\'")
                
                if item_idx >= len(self.items):
                    raise ValueError(f"Item not found: index for item was out of range in items")
                elif isinstance(self.items[item_idx], Pathable):
                    next_pth = "/".join(pth[1:])
                    return self.items[item_idx].items_at_path(next_pth)
                else:
                    raise ValueError("Invalid path: given item in items was not PATHABLE")
            elif attr == "folders":
                if pred not in self._folders_dict:
                    raise ValueError("Item not found: no folder existed with given archetype_node_id")
                else:
                    next_pth = "/".join(pth[1:])
                    return self._folders_dict[pred].items_at_path(next_pth)
            else:
                raise ValueError(f"Invalid path: children of folder are 'items' and 'folders', not \'{attr}\'")

    def path_unique(self, a_path) -> bool:
        pth = a_path.split("/")
        last_node = pth[-1]
        last_node_split = last_node.replace("]", "").split("[")
        return (len(last_node_split) == 2 and (last_node_split[0] == "items" or last_node_split[0] == "folders"))

    
class VersionedFolder(VersionedObject[Folder]):
    pass