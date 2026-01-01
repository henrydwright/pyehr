"""The demographic model provided in this module is a generalised model of the 
facts one might expect to see in a demographic server. The purpose of the model 
is as a specification of a demographic service, either standalone, or a "wrapper" 
service for an existing system such as a patient master index (PMI). In the 
latter situation, it is used to add the required openEHR semantics, particularly 
versioning, to an existing service."""

from typing import Optional
from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalProcessedPath
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