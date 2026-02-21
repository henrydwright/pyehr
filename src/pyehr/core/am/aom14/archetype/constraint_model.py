

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.json_tools import json_has_path
from pyehr.core.rm.common.archetyped import Locatable


class ArchetypeConstraint(AnyClass):
    """Archetype equivalent to LOCATABLE class in openEHR Common reference model. 
    Defines common constraints for any inheritor of LOCATABLE in any reference 
    model."""

    _parent: Optional['ArchetypeConstraint']
    """Parent ARCHETYPE_CONSTRAINT object of this ARCHETYPE_CONSTRAINT or None if root-level"""

    _parent_container_attribute_name: Optional[str]
    """The attribute within which this ARCHETYPE_CONSTRAINT is stored in its parent (e.g. 'children' for a child of C_ATTRIBUTE)"""

    _list_index: Optional[int]
    """The index of this item within a parent list, if it is in one"""

    @abstractmethod
    def __init__(self,
                 parent: Optional['ArchetypeConstraint'] = None,
                 parent_container_attribute_name: Optional[str] = None,
                 list_index: Optional[int] = None,
                 **kwargs):
        # n.b this logic is implemented in the same way as in PATHABLE so try
        #      to remember to copy any code changes from there, into here...
        self._parent = parent
        self._parent_container_attribute_name = parent_container_attribute_name
        self._list_index = list_index
        super().__init__(**kwargs)

    @abstractmethod
    def is_subset_of(self, other: 'ArchetypeConstraint') -> bool:
        """True if constraints represented by this node, ignoring any sub-parts, 
        are narrower or the same as other. Typically used during validation of 
        special-ised archetype nodes."""
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    def path(self) -> str:
        """Path of this node relative to root of archetype."""
        if self._parent is None:
            return "/definition"
        else:
            parent_path = self._parent.path()
            plural = self._list_index is not None
            pred = f"[{self._list_index}]" if plural else ""
            if parent_path == "/":
                return parent_path + f"{self._parent_container_attribute_name}{pred}"
            else:
                return parent_path + f"/{self._parent_container_attribute_name}{pred}"

    def has_path(self, a_path: str) -> bool:
        """True if the relative path `a_path` exists at this node."""
        return json_has_path(self.as_json(), a_path)
    
class CObject(ArchetypeConstraint):
    pass

class CDefinedObject(CObject):
    pass

class CComplexObject(CDefinedObject):
    pass