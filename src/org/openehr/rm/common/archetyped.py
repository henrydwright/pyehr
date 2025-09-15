"""The archetyped package defines the core types PATHABLE, LOCATABLE, 
ARCHETYPED, and LINK"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.base_types.identification import UIDBasedID, ArchetypeID, TemplateID
from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.rm.data_types.text import DVText
from org.openehr.rm.data_types.uri import DVEHRUri

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
    """The LINK type defines a logical relationship between two items, such as two ENTRYs or an 
    ENTRY and a COMPOSITION. Links can be used across compositions, and across EHRs. Links can 
    potentially be used between interior (i.e. non archetype root) nodes, although this probably 
    should be prevented in archetypes. Multiple LINKs can be attached to the root object of any 
    archetyped structure to give the effect of a 1→N link.

    1:1 and 1:N relationships between archetyped content elements (e.g. ENTRYs) can be expressed 
    by using one, or more than one, respectively, LINKs. Chains of links can be used to see problem 
    threads or other logical groupings of items.

    Links should be between archetyped structures only, i.e. between objects representing complete 
    domain concepts because relationships between sub-elements of whole concepts are not necessarily 
    meaningful, and may be downright confusing. Sensible links only exist between whole ENTRYs, 
    SECTIONs, COMPOSITIONs and so on."""

    meaning: DVText
    """Used to describe the relationship, usually in clinical terms, such as in response to (the 
    relationship between test results and an order), follow-up to and so on. Such relationships 
    can represent any clinically meaningful connection between pieces of information. Values for 
    meaning include those described in Annex C, ENV 13606 pt 2 under the categories of generic, 
    documenting and reporting, organisational, clinical, circumstancial, and view management."""

    link_type: DVText
    """The type attribute is used to indicate a clinical or domain-level meaning for the kind of 
    link, for example problem or issue . If type values are designed appropriately, they can be 
    used by the requestor of EHR extracts to categorise links which must be followed and which 
    can be broken when the extract is created."""

    target: DVEHRUri
    """The logical to object in the link relation, as per the linguistic sense of the meaning 
    attribute."""

    def __init__(self, meaning: DVText, link_type: DVText, target: DVEHRUri, **kwargs):
        self.meaning = meaning
        self.link_type = link_type
        self.target = target
        super().__init__(**kwargs)
    
    def is_equal(self, other):
        return super().is_equal(other)

class Archetyped(AnyClass):
    """Archetypes act as the configuration basis for the particular structures of instances 
    defined by the reference model. To enable archetypes to be used to create valid data, key 
    classes in the reference model act as root points for archetyping; accordingly, these classes 
    have the archetype_details attribute set.

    An instance of the class ARCHETYPED contains the relevant archetype identification information, 
    allowing generating archetypes to be matched up with data instances."""
    
    archetype_id : ArchetypeID
    """Globally unique archetype identifier."""

    template_id: Optional[TemplateID]
    """Globally unique template identifier, if a template was active at this point in the structure. 
    Normally, a template would only be used at the top of a top-level structure, but the possibility 
    exists for templates at lower levels."""

    rm_version: str
    """Version of the openEHR reference model used to create this object. Expressed in terms of the 
    release version string, e.g. 1.0 , 1.2.4."""

    def __init__(self, archetype_id: ArchetypeID, rm_version: str, template_id: Optional[TemplateID] = None, **kwargs):
        self.archetype_id = archetype_id
        if (len(rm_version) == 0):
            raise ValueError("rm_version cannot be empty (invariant: rm_version_valid)")
        self.rm_version = rm_version
        self.template_id = template_id
        super().__init__(**kwargs)

    def is_equal(self, other: 'Archetyped'):
        return (
            type(self) == type(other) and
            self.archetype_id.is_equal(other.archetype_id) and
            ((self.template_id is None and other.template_id is None) or (self.template_id.is_equal(other.template_id))) and
            self.rm_version == other.rm_version
        )

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

