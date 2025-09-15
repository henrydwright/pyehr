"""The archetyped package defines the core types PATHABLE, LOCATABLE, 
ARCHETYPED, and LINK"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.base_types.identification import UIDBasedID
from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.rm.data_types.text import DVText

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

class FeederAudit(AnyClass):
    pass

class Link(AnyClass):
    
    def is_equal(self, other):
        return super().is_equal(other)

class Archetyped(AnyClass):
    
    def is_equal(self, other):
        return super().is_equal(other)

class Locatable(Pathable):
    """Root class of all information model classes that can be archetyped. Most classes 
    in the openEHR reference model inherit from the LOCATABLE class, which defines the 
    idea of locatability in an archetyped structure. LOCATABLE defines a runtime name 
    and an archetype_node_id."""

    name: DVText
    """Runtime name of this fragment, used to build runtime paths. This is the term provided 
    via a clinical application or batch process to name this EHR construct: its retention in 
    the EHR faithfully preserves the original label by which this entry was known to end users."""

    archetype_node_id: str
    """Design-time archetype identifier of this node taken from its generating archetype; used 
    to build archetype paths. Always in the form of an at-code, e.g. at0005. This value enables 
    a 'standardised' name for this node to be generated, by referring to the generating archetype 
    local terminology.

    At an archetype root point, the value of this attribute is always the stringified form of the 
    archetype_id found in the archetype_details object."""

    uid: Optional[UIDBasedID]
    """Optional globally unique object identifier for root points of archetyped structures."""

    links: Optional[list[Link]]
    """Links to other archetyped structures (data whose root object inherits from ARCHETYPED, 
    such as ENTRY, SECTION and so on). Links may be to structures in other compositions."""

    archetype_details: Optional[Archetyped]
    """Details of archetyping used on this node."""

    feeder_audit: Optional[FeederAudit]
    """Audit trail from non-openEHR system of original commit of information forming the content 
    of this node, or from a conversion gateway which has synthesised this node."""

    def __init__(self, 
                 name: DVText, 
                 archetype_node_id: str, 
                 uid : Optional[UIDBasedID] = None, 
                 links : Optional[list[Link]] = None,  
                 archetype_details : Optional[Archetyped] = None,
                 feeder_audit : Optional[FeederAudit] = None,
                 **kwargs):
        self.name = name
        if (len(archetype_node_id) == 0):
            raise ValueError("Archetype node ID cannot be empty (invariant: archetype_node_id_valid)")
        self.archetype_node_id = archetype_node_id
        self.uid = uid
        if (links is not None and len(links) == 0):
            raise ValueError("If list of links is provided, it cannot be empty (invariant: is_archetype_root)")
        self.links = links
        self.archetype_details = archetype_details
        self.feeder_audit = feeder_audit
        super().__init__(**kwargs)

    @abstractmethod
    def concept(self) -> DVText:
        """Clinical concept of the archetype as a whole (= derived from the `archetype_node_id` 
        of the root node)"""
        pass

    def is_archetype_root(self) -> bool:
        """True if this node is the root of an archetyped structure."""
        return not (self.archetype_details is None)

