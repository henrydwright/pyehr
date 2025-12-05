"""The archetyped package defines the core types PATHABLE, LOCATABLE, 
ARCHETYPED, and LINK"""

from abc import abstractmethod
from typing import Optional

from org.core.base.base_types.identification import UIDBasedID, ArchetypeID, TemplateID
from org.core.base.foundation_types.any import AnyClass
from org.core.base.foundation_types.structure import is_equal_value
from org.core.rm.common.generic import PartyIdentified
from org.core.rm.data_types.basic import DVIdentifier
from org.core.rm.data_types.encapsulated import DVEncapsulated
from org.core.rm.data_types.text import DVText
from org.core.rm.data_types.uri import DVEHRUri
from org.core.rm.data_types.quantity.date_time import DVDateTime

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
    def item_at_path(self, a_path: str) -> AnyClass:
        """The item at a path (relative to this item); only 
        valid for unique paths, i.e. paths that resolve to a 
        single item."""
        pass

    @abstractmethod
    def items_at_path(self, a_path: str) -> Optional[list[AnyClass]]:
        """List of items corresponding to a non-unique path."""
        pass

    @abstractmethod
    def path_exists(self, a_path: str) -> bool:
        """True if the path exists in the data with respect 
        to the current item."""
        pass

    @abstractmethod
    def path_unique(self, a_path: str) -> bool:
        """True if the path corresponds to a single item in the data."""
        pass

    @abstractmethod
    def path_of_item(self) -> str:
        """The path to an item relative to the root of this archetyped 
        structure."""
        pass

    def _root_node(self) -> 'Pathable':
        """Get the root node at the top of this pathable structure"""
        if self.parent() is None:
            return self
        else:
            return self.parent()._root_node()

    @abstractmethod
    def as_json(self):
        pass

class FeederAuditDetails(AnyClass):
    """Audit details for any system in a feeder system chain. Audit details here means the general notion 
    of who/where/when the information item to which the audit is attached was created. None of the 
    attributes is defined as mandatory, however, in different scenarios, various combinations of attributes 
    will usually be mandatory. This can be controlled by specifying feeder audit details in legacy archetypes."""

    system_id: str
    """Identifier of the system which handled the information item. This is the IT system owned by the organisation 
    legally responsible for handling the data, and at which the data were previously created or passed by an earlier 
    system."""

    location: Optional[PartyIdentified]
    """Identifier of the particular site/facility within an organisation which handled the item. For computability, 
    this identifier needs to be e.g. a PKI identifier which can be included in the identifier list of the 
    PARTY_IDENTIFIED object."""

    subject: Optional[PartyIdentified]
    """Identifiers for subject of the received information item."""

    provider: Optional[PartyIdentified]
    """Optional provider(s) who created, committed, forwarded or otherwise handled the item."""

    time: Optional[DVDateTime]
    """Time of handling the item. For an originating system, this will be time of creation, for an intermediate 
    feeder system, this will be a time of accession or other time of handling, where available."""

    version_id: Optional[str]
    """Any identifier used in the system such as "interim", "final", or numeric versions if available."""

    other_details: Optional['ItemStructure']
    """Optional attribute to carry any custom meta-data. May be archetyped."""

    def __init__(
        self,
        system_id: str,
        location: Optional[PartyIdentified] = None,
        subject: Optional[PartyIdentified] = None,
        provider: Optional[PartyIdentified] = None,
        time: Optional[DVDateTime] = None,
        version_id: Optional[str] = None,
        other_details: Optional['ItemStructure'] = None,
        **kwargs
    ):
        from org.core.rm.data_structures.item_structure import ItemStructure
        if len(system_id) == 0:
            raise ValueError("system_id cannot be an empty string (invariant: system_id_valid)")
        self.system_id = system_id
        self.location = location
        self.subject = subject
        self.provider = provider
        self.time = time
        self.version_id = version_id
        self.other_details = other_details
        super().__init__(**kwargs)

    def is_equal(self, other):
        return (
            type(self) == type(other) and
            self.system_id == other.system_id and
            is_equal_value(self.location, other.location) and
            is_equal_value(self.subject, other.subject) and
            is_equal_value(self.provider, other.provider) and
            is_equal_value(self.time, other.time) and
            self.version_id == other.version_id and
            is_equal_value(self.other_details, other.other_details)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/FEEDER_AUDIT_DETAILS.json
        draft = {
            "_type": "FEEDER_AUDIT_DETAILS",
            "system_id": self.system_id,
        }
        if self.location is not None:
            draft["location"] = self.location.as_json()
        if self.provider is not None:
            draft["provider"] = self.provider.as_json()
        if self.subject is not None:
            draft["subject"] = self.subject.as_json()
        if self.time is not None:
            draft["time"] = self.time.as_json()
        if self.version_id is not None:
            draft["version_id"] = self.version_id
        if self.other_details is not None:
            draft["other_details"] = self.other_details.as_json()
        
        return draft

class FeederAudit(AnyClass):
    """The FEEDER_AUDIT class defines the semantics of an audit trail which is constructed to describe 
    the origin of data that have been transformed into openEHR form and committed to the system."""

    originating_system_item_ids: Optional[list[DVIdentifier]]
    """Identifiers used for the item in the originating system, e.g. filler and placer ids."""

    feeder_system_item_ids: Optional[list[DVIdentifier]]
    """Identifiers used for the item in the feeder system, where the feeder system is distinct from 
    the originating system."""

    original_content: Optional[DVEncapsulated]
    """Optional inline inclusion of or reference to original content corresponding to the openEHR 
    content at this node. Typically a URI reference to a document or message in a persistent store 
    associated with the EHR."""

    originating_system_audit: FeederAuditDetails
    """Any audit information for the information item from the originating system."""

    feeder_system_audit: Optional[FeederAuditDetails]
    """Any audit information for the information item from the feeder system, if different from the 
    originating system."""

    def __init__(
        self,
        originating_system_audit: FeederAuditDetails,
        originating_system_item_ids: Optional[list[DVIdentifier]] = None,
        feeder_system_item_ids: Optional[list[DVIdentifier]] = None,
        original_content: Optional[DVEncapsulated] = None,
        feeder_system_audit: Optional[FeederAuditDetails] = None,
        **kwargs
    ):
        self.originating_system_item_ids = originating_system_item_ids
        self.feeder_system_item_ids = feeder_system_item_ids
        self.original_content = original_content
        self.originating_system_audit = originating_system_audit
        self.feeder_system_audit = feeder_system_audit
        super().__init__(**kwargs)
        
    def is_equal(self, other: 'FeederAudit'):
        return (
            type(self) == type(other) and
            is_equal_value(self.originating_system_item_ids, other.originating_system_item_ids) and
            is_equal_value(self.feeder_system_item_ids, other.feeder_system_item_ids) and
            is_equal_value(self.original_content, other.original_content) and
            is_equal_value(self.originating_system_audit, other.originating_system_audit) and
            is_equal_value(self.feeder_system_audit, other.feeder_system_audit)
        )
        
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/FEEDER_AUDIT.json
        draft = {
            "_type": "FEEDER_AUDIT",
            "originating_system_audit": self.originating_system_audit.as_json()
        }
        
        if self.originating_system_item_ids is not None:
            draft["originating_system_item_ids"] = [id.as_json() for id in self.originating_system_item_ids]
        if self.feeder_system_item_ids is not None:
            draft["feeder_system_item_ids"] = [id.as_json() for id in self.feeder_system_item_ids]
        if self.original_content is not None:
            draft["original_content"] = self.original_content.as_json()
        if self.feeder_system_audit is not None:
            draft["feeder_system_audit"] = self.feeder_system_audit.as_json()
            
        return draft


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
    
    def is_equal(self, other: 'Link'):
        return (
            type(self) == type(other) and
            self.meaning.is_equal(other.meaning) and
            self.link_type.is_equal(other.link_type) and
            self.target.is_equal(other.target)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/LINK.json
        return {
            "_type": "LINK",
            "meaning": self.meaning.as_json(),
            "type": self.link_type.as_json(),
            "target": self.target.as_json()
        }

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
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/ARCHETYPED.json
        draft = {
            "_type": "ARCHETYPED",
            "archetype_id": self.archetype_id.as_json(),
            "rm_version": self.rm_version
        }
        if self.template_id is not None:
            draft["template_id"] = self.template_id.as_json()
        return draft

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

    _parent: Optional[Pathable]
    """Parent PATHABLE object of this LOCATABLE or None if root-level"""

    _parent_container_attribute_name: Optional[str]
    """The attribute within which this LOCATABLE is stored in its parent (e.g. 'folders' for a sub-folder in a folder)"""

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

        self._parent = parent
        self._parent_container_attribute_name = parent_container_attribute_name

        super().__init__(**kwargs)

    def concept(self) -> DVText:
        """Clinical concept of the archetype as a whole (= derived from the `archetype_node_id` 
        of the root node)"""
        if self.is_archetype_root():
            # TODO: should this method return DVText or str?
            return DVText(self.archetype_node_id)
        else:
            p = self.parent()
            if p is None:
                raise ValueError("No root node found in LOCATABLE structure.")
            if isinstance(p, Locatable):
                return p.concept()
            else:
                raise TypeError("Met non-LOCATABLE node before root found.")

    def is_archetype_root(self) -> bool:
        """True if this node is the root of an archetyped structure."""
        return not (self.archetype_details is None)
    
    def as_json(self):
        draft = {
            "name": self.name.as_json(),
            "archetype_node_id": self.archetype_node_id
        }
        if self.uid is not None:
            draft["uid"] = self.uid.as_json()
        if self.links is not None:
            draft["links"] = [link.as_json() for link in self.links]
        if self.archetype_details is not None:
            draft["archetype_details"] = self.archetype_details.as_json()
        if self.feeder_audit is not None:
            draft["feeder_audit"] = self.feeder_audit.as_json()
        return draft
    
    def is_equal(self, other):
        return (
            type(self) == type(other) and
            is_equal_value(self.name, other.name) and
            is_equal_value(self.archetype_node_id, other.archetype_node_id) and
            is_equal_value(self.uid, other.uid) and
            is_equal_value(self.links, other.links) and
            is_equal_value(self.archetype_details, other.archetype_details) and
            is_equal_value(self.feeder_audit, other.feeder_audit)
        )
        
    def path_of_item(self):
        # TODO: removed the argument as not sure if spec is correct, may need to 
        #        fix this later if the spec was right
        if self.parent() is None:
            return "/"
        else:
            parent_path = self.parent().path_of_item()
            plural = (self._parent_container_attribute_name[-1:] == "s")
            pred = f"[{self.archetype_node_id}]" if plural else ""
            if parent_path == "/":
                return parent_path + f"{self._parent_container_attribute_name}{pred}"
            else:
                return parent_path + f"/{self._parent_container_attribute_name}{pred}"
            
    def parent(self):
        return self._parent
