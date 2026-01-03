"""The demographic model provided in this module is a generalised model of the 
facts one might expect to see in a demographic server. The purpose of the model 
is as a specification of a demographic service, either standalone, or a "wrapper" 
service for an existing system such as a patient master index (PMI). In the 
latter situation, it is used to add the required openEHR semantics, particularly 
versioning, to an existing service."""

from abc import abstractmethod
from typing import Optional
from pyehr.core.base.base_types.identification import LocatableRef, PartyRef, UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalProcessedPath
from pyehr.core.rm.common.change_control import VersionedObject
from pyehr.core.rm.data_structures.item_structure import ItemStructure
from pyehr.core.rm.data_types.quantity import DVInterval
from pyehr.core.rm.data_types.quantity.date_time import DVDate
from pyehr.core.rm.data_types.text import DVText


class PartyIdentity(Locatable):
    """An identity owned by a Party, such as a person name or company name, and 
    which is used by the Party to identify itself. Actual structure is archetyped."""

    details: ItemStructure
    """The value of the identity. This will often taken the form of a parseable 
    string or a small structure of strings."""

    def __init__(self, 
                purpose: DVText, 
                archetype_node_id: str, 
                details: ItemStructure,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        self.details = details
        super().__init__(purpose, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.details, other.details))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Demographic/PARTY_IDENTITY.json
        draft = super().as_json()
        draft["details"] = self.details.as_json()
        draft["_type"] = "PARTY_IDENTITY"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (PARTY_IDENTITY)")

        if path.current_node_attribute == "details":
            return self._path_resolve_single(path, self.details, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'details' at PARTY_IDENTITY but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False

    def purpose(self) -> DVText:
        """Purpose of identity, e.g. legal , stagename, nickname, tribal name, 
        trading name. Taken from value of inherited name attribute."""
        return self.name
    
class Address(Locatable):
    """Address of contact, which may be electronic or geographic."""

    details: ItemStructure
    """Archetypable structured address."""

    def __init__(self, 
            addr_type: DVText, 
            archetype_node_id: str, 
            details: ItemStructure,
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        self.details = details
        super().__init__(addr_type, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Address'):
        return (super().is_equal(other) and
                is_equal_value(self.details, other.details))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Demographic/ADDRESS.json
        draft = super().as_json()
        draft["details"] = self.details.as_json()
        draft["_type"] = "ADDRESS"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ADDRESS)")

        if path.current_node_attribute == "details":
            return self._path_resolve_single(path, self.details, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'details' at ADDRESS but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
        
    def address_type(self) -> DVText:
        """Type of address, e.g. electronic, locality. Taken from value of 
        inherited name attribute."""
        return self.name


class Contact(Locatable):
    """Description of a means of contact of a Party. Actual structure is archetyped."""

    addresses: list[Address]
    """A set of address alternatives for this contact purpose and time validity 
    combination."""

    time_validity: Optional[DVInterval[DVDate]]
    """Valid time interval for this contact descriptor."""

    def __init__(self, 
            purpose: DVText, 
            archetype_node_id: str, 
            addresses: list[Address],
            time_validity: Optional[DVInterval[DVDate]] = None,
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        self.addresses = addresses
        self.time_validity = time_validity
        super().__init__(purpose, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Contact'):
        return (super().is_equal(other)
                and is_equal_value(self.addresses, other.addresses)
                and is_equal_value(self.time_validity, other.time_validity))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Demographic/CONTACT.json
        draft = super().as_json()
        draft["addresses"] = [a.as_json() for a in self.addresses]
        if self.time_validity is not None:
            draft["time_validity"] = self.time_validity.as_json()
        draft["_type"] = "CONTACT"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (CONTACT)")

        if path.current_node_attribute == "addresses":
            return self._path_resolve_item_list(path, self.addresses, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'addresses' at CONTACT but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
        
    def purpose(self) -> DVText:
        """Purpose for which this contact is used, e.g. mail, daytime phone, etc. 
        Taken from value of inherited name attribute."""
        return self.name
    
class PartyRelationship(Locatable):
    """Generic description of a relationship between parties."""

    details: Optional[ItemStructure]
    """The detailed description of the relationship."""

    target: PartyRef
    """Target of relationship."""

    time_validity: Optional[DVInterval[DVDate]]
    """Valid time interval for this relationship."""

    source: PartyRef
    """Source of relationship."""

    def __init__(self, 
                rel_type: DVText, 
                archetype_node_id: str, 
                source: PartyRef,
                target: PartyRef,
                details: Optional[ItemStructure] = None,
                time_validity: Optional[DVInterval[DVDate]] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
            self.details = details
            self.target = target
            self.time_validity = time_validity
            self.source = source
            super().__init__(rel_type, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'PartyRelationship'):
        return (super().is_equal(other)
                and is_equal_value(self.details, other.details)
                and is_equal_value(self.target, other.target)
                and is_equal_value(self.time_validity, other.time_validity)
                and is_equal_value(self.source, other.source))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Demographic/PARTY_RELATIONSHIP.json
        draft = super().as_json()
        draft["target"] = self.target.as_json()
        draft["source"] = self.source.as_json()
        if self.details is not None:
            draft["details"] = self.details.as_json()
        if self.time_validity is not None:
            draft["time_validity"] = self.time_validity.as_json()
        draft["_type"] = "PARTY_RELATIONSHIP"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (PARTY_RELATIONSHIP)")

        if path.current_node_attribute == "details":
            return self._path_resolve_single(path, self.details, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'details' at PARTY_RELATIONSHIP but found \'{path.current_node_attribute}\'")
            
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
        
    def relationship_type(self):
        """Type of relationship, such as employment, authority, health provision"""
        return self.name

class Party(Locatable):
    """Ancestor of all Party types, including real world entities and their roles. A Party is any entity which can participate in an activity. The name attribute inherited from LOCATABLE is used to indicate the actual type of party (note that the actual names, i.e. identities of parties are indicated in the identities attribute, not the name attribute).

    Note: It is strongly recommended that the inherited attribute uid be populated
    in PARTY objects, using the UID copied from the object_id() of the uid field
    of the enclosing VERSION object.
    For example, the ORIGINAL_VERSION.uid `87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2` 
    would be copied to the uid field of the PARTY object."""

    identities: list[PartyIdentity]
    """Identities used by the party to identify itself, such as legal name, 
    stage names, aliases, nicknames and so on."""

    contacts: Optional[list[Contact]]
    """Contacts for this party."""

    details: Optional[ItemStructure]
    """All other details for this Party."""

    reverse_relationships: Optional[list[LocatableRef]]
    """References to relationships in which this Party takes part as target."""

    relationships: Optional[list[PartyRelationship]]
    """Relationships in which this Party takes part as source."""

    @abstractmethod
    def __init__(self,
                party_type: DVText,
                archetype_node_id: str,
                archetype_details: Archetyped,
                identities: list[PartyIdentity],
                uid: UIDBasedID,
                contacts: Optional[list[Contact]] = None,
                details: Optional[ItemStructure] = None,
                relationships: Optional[list[PartyRelationship]] = None,
                reverse_relationships: Optional[list[LocatableRef]] = None,
                links: Optional[list[Link]] = None,
                feeder_audit: Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
            self.identities = identities
            if contacts is not None and len(contacts) == 0:
                raise ValueError("If provided, contacts cannot be an empty list (invariant: contacts_valid)")
            self.contacts = contacts
            self.details = details
            if relationships is not None and len(relationships) == 0:
                raise ValueError("If provided, relationships cannot be an empty list (invariant: relationships_valid)")
            self.relationships = relationships
            if reverse_relationships is not None and len(reverse_relationships) == 0:
                raise ValueError("If provided, reverse_relationships cannot be an empty list (invariant: reverse_relationships_validity)")
            self.reverse_relationships = reverse_relationships
            super().__init__(party_type, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    @abstractmethod
    def is_equal(self, other: 'Party'):
        return (super().is_equal(other)
                and is_equal_value(self.identities, other.identities)
                and is_equal_value(self.contacts, other.contacts)
                and is_equal_value(self.details, other.details)
                and is_equal_value(self.relationships, other.relationships)
                and is_equal_value(self.reverse_relationships, other.reverse_relationships))

    @abstractmethod
    def as_json(self):
        draft = super().as_json()
        draft["identities"] = [i.as_json() for i in self.identities]
        if self.contacts is not None:
            draft["contacts"] = [c.as_json() for c in self.contacts]
        if self.details is not None:
            draft["details"] = self.details.as_json()
        if self.relationships is not None:
            draft["relationships"] = [r.as_json() for r in self.relationships]
        if self.reverse_relationships is not None:
            draft["reverse_relationships"] = [rr.as_json() for rr in self.reverse_relationships]
        return draft
    
    def type_party(self):
        """Type of party, such as PERSON, ORGANISATION, etc. Role name, 
        e.g. general practitioner , nurse , private citizen. Taken from inherited 
        name attribute."""
        return self.name

class Actor(Party):
    """Ancestor of all real-world types, including people and organisations. An 
    actor is any real-world entity capable of taking on a role."""

    languages: Optional[list[DVText]]
    """Languages which can be used to communicate with this actor, in preferred 
    order of use (if known, else order irrelevant)."""

    roles: Optional[list[PartyRef]]
    """Identifiers of the Version container for each Role played by this Party."""

    @abstractmethod
    def __init__(self,
                actor_type: DVText,
                archetype_node_id: str,
                archetype_details: Archetyped,
                identities: list[PartyIdentity],
                uid: UIDBasedID,
                contacts: Optional[list[Contact]] = None,
                details: Optional[ItemStructure] = None,
                relationships: Optional[list[PartyRelationship]] = None,
                reverse_relationships: Optional[list[LocatableRef]] = None,
                languages: Optional[list[DVText]] = None,
                roles: Optional[list[PartyRef]] = None,
                links: Optional[list[Link]] = None,
                feeder_audit: Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
            self.languages = languages
            self.roles = roles
            super().__init__(actor_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Actor'):
        return (super().is_equal(other)
                and is_equal_value(self.languages, other.languages)
                and is_equal_value(self.roles, other.roles))

    @abstractmethod
    def as_json(self):
        draft = super().as_json()
        if self.languages is not None:
            draft["languages"] = [l.as_json() for l in self.languages]
        if self.roles is not None:
            draft["roles"] = [r.as_json() for r in self.roles]
        return draft
    
    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (subclass of ACTOR)")

        if path.current_node_attribute == "identities":
            return self._path_resolve_item_list(path, self.identities, single_item, check_only)
        elif path.current_node_attribute == "contacts":
            return self._path_resolve_item_list(path, self.contacts, single_item, check_only)
        elif path.current_node_attribute == "details":
            return self._path_resolve_single(path, self.details, single_item, check_only)
        elif path.current_node_attribute == "relationships":
            return self._path_resolve_item_list(path, self.relationships, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected one of 'identities', 'contacts', 'details', 'relationships', or 'reverse_relationships' at subclass of ACTOR but found '{path.current_node_attribute}'")

    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)

    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)

    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)

    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
    
class Person(Actor):
    """Generic description of persons. Provides a dedicated type to which Person 
    archetypes can be targeted."""

    def __init__(self,
            actor_type: DVText,
            archetype_node_id: str,
            archetype_details: Archetyped,
            identities: list[PartyIdentity],
            uid: UIDBasedID,
            contacts: Optional[list[Contact]] = None,
            details: Optional[ItemStructure] = None,
            relationships: Optional[list[PartyRelationship]] = None,
            reverse_relationships: Optional[list[LocatableRef]] = None,
            languages: Optional[list[DVText]] = None,
            roles: Optional[list[PartyRef]] = None,
            links: Optional[list[Link]] = None,
            feeder_audit: Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        super().__init__(actor_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, languages, roles, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def as_json(self):
        draft = super().as_json()
        draft["_type"] = "PERSON"
        return draft
    
class Organisation(Actor):
    """Generic description of organisations. An organisation is a legally constituted body whose existence (in general) outlives the existence of parties considered to be part of it."""

    def __init__(self,
        actor_type: DVText,
        archetype_node_id: str,
        archetype_details: Archetyped,
        identities: list[PartyIdentity],
        uid: UIDBasedID,
        contacts: Optional[list[Contact]] = None,
        details: Optional[ItemStructure] = None,
        relationships: Optional[list[PartyRelationship]] = None,
        reverse_relationships: Optional[list[LocatableRef]] = None,
        languages: Optional[list[DVText]] = None,
        roles: Optional[list[PartyRef]] = None,
        links: Optional[list[Link]] = None,
        feeder_audit: Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        super().__init__(actor_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, languages, roles, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def as_json(self):
        draft = super().as_json()
        draft["_type"] = "ORGANISATION"
        return draft
    
class Group(Actor):
    """A group is a real world group of parties which is created by another party,
    usually an organisation, for some specific purpose. A typical clinical example
    is that of the specialist care team, e.g. cardiology team. The members of 
    the group usually work together."""

    def __init__(self,
        actor_type: DVText,
        archetype_node_id: str,
        archetype_details: Archetyped,
        identities: list[PartyIdentity],
        uid: UIDBasedID,
        contacts: Optional[list[Contact]] = None,
        details: Optional[ItemStructure] = None,
        relationships: Optional[list[PartyRelationship]] = None,
        reverse_relationships: Optional[list[LocatableRef]] = None,
        languages: Optional[list[DVText]] = None,
        roles: Optional[list[PartyRef]] = None,
        links: Optional[list[Link]] = None,
        feeder_audit: Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        super().__init__(actor_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, languages, roles, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def as_json(self):
        draft = super().as_json()
        draft["_type"] = "GROUP"
        return draft
    
class Agent(Actor):
    """Generic concept of any kind of agent, including devices, software systems, 
    but not humans or organisations."""

    def __init__(self,
        actor_type: DVText,
        archetype_node_id: str,
        archetype_details: Archetyped,
        identities: list[PartyIdentity],
        uid: UIDBasedID,
        contacts: Optional[list[Contact]] = None,
        details: Optional[ItemStructure] = None,
        relationships: Optional[list[PartyRelationship]] = None,
        reverse_relationships: Optional[list[LocatableRef]] = None,
        languages: Optional[list[DVText]] = None,
        roles: Optional[list[PartyRef]] = None,
        links: Optional[list[Link]] = None,
        feeder_audit: Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        super().__init__(actor_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, languages, roles, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def as_json(self):
        draft = super().as_json()
        draft["_type"] = "AGENT"
        return draft
    
class VersionedParty(VersionedObject[Party]):
    """Static type formed by binding generic parameter of `VERSIONED_OBJECT<T>` 
    to `PARTY`."""
    pass

class Capability(Locatable):
    """Capability of a role, such as ehr modifier, health care provider. 
    Capability should be backed up by credentials."""

    credentials: ItemStructure
    """The qualifications of the performer of the role for this capability. 
    This might include professional qualifications and official identifications 
    such as provider numbers etc."""

    time_validity: Optional[DVInterval[DVDate]]
    """Valid time interval for the credentials of this capability."""

    def __init__(self,
        name: DVText,
        archetype_node_id: str,
        credentials: ItemStructure,
        time_validity: Optional[DVInterval[DVDate]] = None,
        uid: Optional[UIDBasedID] = None,
        links: Optional[list[Link]] = None,
        archetype_details: Optional[Archetyped] = None,
        feeder_audit: Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        self.credentials = credentials
        self.time_validity = time_validity
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Capability'):
        return (super().is_equal(other)
            and is_equal_value(self.credentials, other.credentials)
            and is_equal_value(self.time_validity, other.time_validity))

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Demographic/CAPABILITY.json
        draft = super().as_json()
        draft["credentials"] = self.credentials.as_json()
        if self.time_validity is not None:
            draft["time_validity"] = self.time_validity.as_json()
        draft["_type"] = "CAPABILITY"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (CAPABILITY)")

        if path.current_node_attribute == "credentials":
            return self._path_resolve_single(path, self.credentials, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'credentials' at CAPABILITY but found '{path.current_node_attribute}'")

    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)

    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)

    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)

    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False

class Role(Party):
    """Generic description of a role performed by an Actor. The role corresponds 
    to a competency of the Party. Roles are used to define the responsibilities 
    undertaken by a Party for a purpose. Roles should have credentials qualifying 
    the performer to perform the role."""
    
    time_validity: Optional[DVInterval[DVDate]]
    """Valid time interval for this role."""

    performer: PartyRef
    """Reference to Version container of Actor playing the role."""

    capabilities: Optional[list[Capability]]
    """The capabilities of this role."""

    def __init__(self,
        role_type: DVText,
        archetype_node_id: str,
        archetype_details: Archetyped,
        identities: list[PartyIdentity],
        uid: UIDBasedID,
        performer: PartyRef,
        contacts: Optional[list[Contact]] = None,
        details: Optional[ItemStructure] = None,
        relationships: Optional[list[PartyRelationship]] = None,
        reverse_relationships: Optional[list[LocatableRef]] = None,
        time_validity: Optional[DVInterval[DVDate]] = None,
        capabilities: Optional[list[Capability]] = None,
        links: Optional[list[Link]] = None,
        feeder_audit: Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        self.time_validity = time_validity
        self.performer = performer
        if capabilities is not None and len(capabilities) == 0:
            raise ValueError("If provided, capabilities cannot be an empty list (invariant: capabilities_valid)")
        self.capabilities = capabilities
        super().__init__(role_type, archetype_node_id, archetype_details, identities, uid, contacts, details, relationships, reverse_relationships, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other: 'Role'):
        return (super().is_equal(other)
            and is_equal_value(self.time_validity, other.time_validity)
            and is_equal_value(self.performer, other.performer)
            and is_equal_value(self.capabilities, other.capabilities))

    def as_json(self):
        draft = super().as_json()
        draft["performer"] = self.performer.as_json()
        if self.time_validity is not None:
            draft["time_validity"] = self.time_validity.as_json()
        if self.capabilities is not None:
            draft["capabilities"] = [c.as_json() for c in self.capabilities]
        draft["_type"] = "ROLE"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ROLE)")

        if path.current_node_attribute == "identities":
            return self._path_resolve_item_list(path, self.identities, single_item, check_only)
        elif path.current_node_attribute == "contacts":
            return self._path_resolve_item_list(path, self.contacts, single_item, check_only)
        elif path.current_node_attribute == "details":
            return self._path_resolve_single(path, self.details, single_item, check_only)
        elif path.current_node_attribute == "relationships":
            return self._path_resolve_item_list(path, self.relationships, single_item, check_only)
        elif path.current_node_attribute == "capabilities":
            return self._path_resolve_item_list(path, self.capabilities, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected one of 'identities', 'contacts', 'details', 'relationships', 'capabilities' at ROLE but found '{path.current_node_attribute}'")

    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)

    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)

    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)

    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False