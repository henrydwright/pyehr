"""The `directory` package provides a simple abstraction of a versioned folder 
structure."""

from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.base_types.identification import ObjectRef, UIDBasedID
from org.openehr.rm.common.archetyped import Locatable, Link, Archetyped, FeederAudit, Pathable
from org.openehr.rm.common.change_control import VersionedObject
from org.openehr.rm.data_structures.item_structure import ItemStructure
from org.openehr.rm.data_types.text import DVText
from org.openehr.base.foundation_types.structure import is_equal_value

class Folder(Locatable):
    """The concept of a named folder."""

    details: Optional[ItemStructure] = None
    """Archetypable meta-data for FOLDER."""

    _parent: Optional[Pathable] = None
    """Parent PATHABLE object of this FOLDER or None if root-level"""

    _folders_dict: Optional[dict[str, 'Folder']] = None
    """Dict of sub-folders keyed by name"""

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
                 **kwargs):
        self.items = items

        if folders is not None:
            if len(folders) == 0:
                raise ValueError("If provided, list of sub-folders must not be empty (invariant: folders_valid)")
            self._folders_dict = dict()
            for folder in folders:
                folder._parent = self
                self._folders_dict[folder.name.value] = folder

        self.details = details
        self._parent = parent
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, **kwargs)

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
    
    def parent(self) -> Optional[Pathable]:
        return self._parent
    
    def _navigate_relative_path(self, a_path:str, return_value:bool, multiple_items:Optional[bool] = None):
        if a_path == "":
            if return_value:
                if not multiple_items:
                    return self
                else:
                    raise ValueError("Single item found but items_at_path was used")
            else:
                return True
        
        pth = a_path.split("/")
        print(pth)
        next_node = pth[0]
        next_node_split = next_node.replace("]","").split("[")
        print(next_node_split)

        if next_node_split[0] == "items":
            if len(next_node_split) == 1:
                path_exists = (self.items is not None)
                if not return_value:
                    return path_exists
                elif not path_exists:
                    raise ValueError("Provided path did not exist")
                else:
                    if multiple_items:
                        return self.items
                    else:
                        raise ValueError("Multiple items found but item_at_path was used")

            elif len(next_node_split) == 2:
                try:
                    item_idx = int(next_node_split[1])
                except ValueError:
                    if return_value:
                        raise ValueError("Invalid path provided (items index was not a number)")
                    else:
                        return False
                path_exists = item_idx <= (len(self.items) - 1)
                if not return_value:
                    return path_exists
                elif not path_exists:
                    raise IndexError("Provided path did not exist (items index out of range)")
                else:
                    if not multiple_items:
                        return self.items[item_idx]
                    else:
                        raise ValueError("Single item found but items_at_path was used")
            else:
                if not return_value:
                    return False
                else:
                    raise ValueError("Invalid path provided")
            
        elif next_node_split[0] == "folders":
            if len(next_node_split) == 1:
                path_exists = (self.folders is not None)

                if not return_value:
                    return path_exists
                elif not path_exists:
                    raise ValueError("Provided path did not exist")
                else:
                    if multiple_items:
                        return self.folders
                    else:
                        raise ValueError("Multiple items found but item_at_path was used")
                
            elif len(next_node_split) == 2:
                folder_name = next_node_split[1]

                if folder_name in self._folders_dict:
                    next_folder = self._folders_dict[folder_name]
                    next_pth = "/".join(pth[1:])
                    print(next_pth)
                    return next_folder._navigate_relative_path(next_pth, return_value, multiple_items)
                else:
                    if not return_value:
                        return False
                    else:
                        raise ValueError("Provided path did not exist")
            else:
                if not return_value:
                    return False
                else:
                    raise ValueError("Invalid path provided")
        else:
            if not return_value:
                return False
            else:
                raise ValueError(f"Invalid path provided (expected items or folder but \'{next_node_split[0]}\' was found)")
    
    def path_exists(self, a_path) -> bool:
        return self._navigate_relative_path(a_path, False)

    def item_at_path(self, a_path) -> AnyClass:
        return self._navigate_relative_path(a_path, True, False)
    
    def items_at_path(self, a_path) -> Optional[list[AnyClass]]:
        return self._navigate_relative_path(a_path, True, True)

    def path_unique(self, a_path) -> bool:
        pth = a_path.split("/")
        last_node = pth[-1]
        last_node_split = last_node.replace("]", "").split("[")
        return (len(last_node_split) == 2 and (last_node_split[0] == "items" or last_node_split[0] == "folders"))

    def path_of_item(self) -> str:
        # TODO: removed the argument as not sure if spec is correct, may need to 
        #        fix this later if the spec was right
        if self.parent() is None:
            return "/"
        else:
            parent_path = self.parent().path_of_item()
            if parent_path == "/":
                return parent_path + "folders[" + self.name.value + "]"
            else:
                return parent_path + "/folders[" + self.name.value + "]"
    
class VersionedFolder(VersionedObject[Folder]):
    pass