from abc import ABC, abstractmethod
import datetime
from enum import Enum, StrEnum
from typing import Optional, Union

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, ObjectVersionID, PartyRef, UIDBasedID
from pyehr.core.rm.common.change_control import Contribution, Version, VersionedObject
from pyehr.core.rm.common.generic import Attestation, PartyProxy, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText
from pyehr.core.rm.demographic import Party


class DBActionType(StrEnum):
    """Type of database action performed"""
    CREATE = "c"
    READ = "r"
    UPDATE = "u"
    DELETE = "d"
    GENERATE_HID = "c_id"
    READ_METADATA = "r_mt"
    UPDATE_VERSION_ATTESTATIONS = "u_at"

class DBActionItem():
    party : Optional[PartyRef]
    """Refernce to the party performing the action on the database"""

    action_time: str
    """Datetime of action, following ISO8601 standards"""

    action: DBActionType
    """Type of action performed on the database"""

    query: Optional[dict[str, str]]
    """Query that was carried out to perform operation, if used"""

    def __init__(self, action : DBActionType, party: Optional[PartyRef] = None, query: Optional[dict[str, str]] = None, action_time : str = None):
        self.action = action
        self.party = party
        self.query = query
        if action_time is None:
            self.action_time = Env.current_date_time().as_string()
        else:
            self.action_time = action_time
            

    def as_json(self):
        draft = {
            "action": str(self.action),
            "action_time": self.action_time
        }
        if self.party is not None:
            draft["party"] = self.party.as_json()
        if self.query is not None:
            draft["query"] = self.query
        return draft

class DBMetadata():
    uid: UIDBasedID
    """Database unique UIDBasedID for the object this metadata relates to"""

    obj_type: Optional[str]
    """OpenEHR object type of the object"""

    is_deleted: Optional[bool]
    """Whether or not this object should be treated as deleted"""

    action_history: list[DBActionItem]
    """List of actions carried out on this item"""

    def __init__(self, uid: UIDBasedID, obj_type: Optional[str], is_deleted: Optional[bool], action_history: list[DBActionItem]):
        self.uid = uid
        self.obj_type = obj_type
        self.is_deleted = is_deleted
        self.action_history = action_history

    def as_json(self):
        return {
            "_id": self.uid.value,
            "type": self.obj_type,
            "is_deleted": self.is_deleted,
            "action_history": [a.as_json() for a in self.action_history]
        }

class IDatabaseEngine(ABC):
    """Define an interface for pyehr compliant database engines to return. Allows 
    for multiple different underlying implementations at different dates/times."""

    UID_OBJECT_TYPE = Union[Party]
    """Type of all top-level pyehr objects it is possible to store in the database"""

    @abstractmethod
    def generate_hier_object_id(self, generator: Optional[PartyRef] = None) -> HierObjectID:
        """Generates a UUID that is guaranteed, at a minimum, to be database unique.
        
        :param generator: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def create_uid_object(self, obj: UID_OBJECT_TYPE, creator: Optional[PartyRef] = None):
        """Create a single new pyehr object with a UID field in the database.
        
        :param creator: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def retrieve_uid_object(self, obj_type: str, uid: UIDBasedID, reader: Optional[PartyRef] = None) -> UID_OBJECT_TYPE:
        """Retrieve any pyehr object with a UID field
        
        :param obj_type: OpenEHR type of object being retrieved (e.g. CONTRIBUTION, VERSIONED_OBJECT, etc.)
        :param uid: UID based identifier for the object to be retrieved.
        :param reader: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def retrieve_db_metadata(self, uid: UIDBasedID, reader: Optional[PartyRef] = None) -> Optional[list[DBActionItem]]:
        """Retrieve the database metadata for an object with a given UID.
        
        :param uid: UID based identifier for the items whose associated db metadata is to be retrieved.
        :param reader: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def retrieve_query_match_object(self, obj_type: str, archetype_id: ArchetypeID, query_dict: dict[str, list[str]], reader: Optional[PartyRef] = None) -> list[UID_OBJECT_TYPE]:
        """Retrieve any archetype root LOCATABLE pyehr object archetyped with 
        `archetype_id` AND which has path values and attributes matching the
        `query_dict`.
        
        :param obj_type: OpenEHR type of object being retrieved (e.g. CONTRIBUTION, VERSIONED_OBJECT, etc.)
        :param archetype_id: Archetype ID after which the object is modelled (e.g. 'pyEHR-DEMOGRAPHIC-PERSON.nhs_patient.v1')
        :param query_dict: OpenEHR path for target attribute and list of possible values (e.g. {'details/items[at0002]/value/id': ['9449305552']})
        :param reader: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def update_uid_object(self, obj: UID_OBJECT_TYPE, updater: Optional[PartyRef] = None):
        """Update the provided pyehr object in the database.
        
        :param updater: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def create_versioned_object(self, vo: VersionedObject, create_underlying_versions: bool = False, creator: Optional[PartyRef] = None):
        """Create a new VERSIONED_OBJECT and its underlying REVISION_HISTORY (if not None) in the database.
        
        :param create_underlying_versions: If set to True, then the VERSIONS within the VERSIONED_OBJECT will also be created.
        :param creator: If provided, this is stored in an audit trail of database actions associated with users."""
        pass

    @abstractmethod
    def add_revision_history_item(self, uid: HierObjectID, item: RevisionHistoryItem, creator: Optional[PartyRef] = None):
        """Adds a new REVISION_HISTORY_ITEM to the existing REVISION_HISTORY in the database for VERSIONED_OBJECT with given UID.
        
        Creates a new REVISION_HISTORY if it does not already exist.
        
        :param creator: If provided, this is stored in an audit trail of database actions for the VERSIONED_OBJECT associated with users."""
        pass

    @abstractmethod
    def add_attestation(self, version_id: ObjectVersionID, attestation: Attestation, attester: Optional[PartyRef] = None):
        """Adds a new ATTESTATION to given VERSION (only if it is an ORIGINAL_VERSION) and updates the relevant REVISION_HISTORY_ITEM.
        
        :param attester: If provided, this is stored in an audit trail of database actions for the VERSIONED_OBJECT and VERSION altered by adding this attestation."""
        pass

    @abstractmethod
    def retrieve_versioned_object(self, 
                                  uid: HierObjectID, 
                                  reader: Optional[PartyRef] = None,
                                  metadata_only_versioned_object: bool = True) -> tuple[VersionedObject, RevisionHistory]:
        """Retrieve a VERSIONED_OBJECT and its underlying REVISION_HISTORY.
        
        :returns tuple[0]: `VersionedObject` created with only metadata (i.e. methods will not work as no revision history / versions restored) unless `metadata_only_versioned_object` set to False.
        :returns tuple[1]: `RevisionHistory` associated with the `VersionedObject`."""
        pass

    @abstractmethod
    def commit_contribution_set(self, contrib: Contribution, versions: list[Version], owner_id: Optional[ObjectRef] = None, committer: Optional[PartyRef] = None):
        """Create a `CONTRIBUTION` and its `VERSIONs` in the database. The versions and references to those versions in the
        `CONTRIBUTION` will be verified by this method prior to committing.
        
        This is conducted as a single atomic database action.
        
        :param owner_id: If a VERSIONED_OBJECT needs creating during this commit, an owner_id must be provided or an error will be raised."""
        pass


    