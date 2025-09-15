"""The archetyped package defines the core types PATHABLE, LOCATABLE, 
ARCHETYPED, and LINK"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass

class Pathable(AnyClass):
    """The PATHABLE class defines the pathing capabilities used by nearly all 
    classes in the openEHR reference model, mostly via inheritance of LOCATABLE. 
    The defining characteristics of PATHABLE objects are that they can locate child 
    objects using paths, and they know their parent object in a compositional hierarchy. 
    The parent feature is defined as abstract in the model, and may be implemented in 
    any way convenient."""

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def parent(self) -> 'Pathable':
        """Parent of this node in a compositional hierarchy."""
        pass

    @abstractmethod
    def item_at_path(a_path: str) -> AnyClass:
        """The item at a path (relative to this item); only 
        valid for unique paths, i.e. paths that resolve to a 
        single item."""
        pass

    @abstractmethod
    def items_at_path(a_path: str) -> Optional[list[AnyClass]]:
        """List of items corresponding to a non-unique path."""
        pass

    @abstractmethod
    def path_exists(a_path: str) -> bool:
        """True if the path exists in the data with respect 
        to the current item."""
        pass

    @abstractmethod
    def path_unique(a_path: str) -> bool:
        """True if the path corresponds to a single item in the data."""
        pass

    @abstractmethod
    def path_of_item(a_loc: 'Pathable') -> str:
        """The path to an item relative to the root of this archetyped 
        structure."""
        pass
    