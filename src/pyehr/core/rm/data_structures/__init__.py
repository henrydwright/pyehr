"""The rm.data_structures package contains two packages: the `item_structure` package and the 
`history` package. The first (alongside `representation`) describes generic, path-addressable 
data structures, while the latter describes a generic notion of linear history, for recording 
events in past time."""

from abc import abstractmethod

from pyehr.core.rm.common.archetyped import Locatable
from pyehr.core.rm.data_structures.representation import Item

class DataStructure(Locatable):
    """Abstract parent class of all data structure types. Includes the as_hierarchy function 
    which can generate the equivalent CEN EN13606 single hierarchy for each subtype's physical 
    representation. For example, the physical representation of an ITEM_LIST is List<ELEMENT>; 
    its implementation of as_hierarchy will generate a CLUSTER containing the set of ELEMENT 
    nodes from the list."""

    @abstractmethod
    def as_hierarchy(self) -> Item:
        """Hierarchical equivalent of the physical representation of each subtype, compatible 
        with CEN EN 13606 structures."""
        pass