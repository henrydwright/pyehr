
from enum import Enum
from typing import Optional
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectVersionID, UIDBasedID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.archetyped import Locatable
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, Version, VersionedObject
from pyehr.core.rm.common.generic import Attestation, PartyProxy, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.encapsulated import DVMultimedia
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.server.database import IDatabaseEngine

class AuditChangeType(Enum):
    """Enum of coded audit change types to use with VersionedStore methods for ease."""
    CREATION = DVCodedText("creation", CodePhrase("openehr", "249"))
    AMENDMENT = DVCodedText("amendment", CodePhrase("openehr", "250"))
    MODIFICATION = DVCodedText("modification", CodePhrase("openehr", "251"))
    SYNTHESIS = DVCodedText("synthesis", CodePhrase("openehr", "252"))
    DELETED = DVCodedText("deleted", CodePhrase("openehr", "523"))
    ATTESTATION = DVCodedText("attestation", CodePhrase("openehr", "666"))
    RESTORATION = DVCodedText("restoration", CodePhrase("openehr", "816"))
    FORMAT_CONVERSION = DVCodedText("format conversion", CodePhrase("openehr", "817"))
    UNKNOWN = DVCodedText("unknown", CodePhrase("openehr", "253"))

class VersionLifecycleState(Enum):
    """Enum of coded version lifecycle state to used with VersionedStore methods for ease."""
    COMPLETE = DVCodedText("complete", CodePhrase("openehr", "532"))
    INCOMPLETE = DVCodedText("incomplete", CodePhrase("openehr", "553"))
    DELETE = DVCodedText("deleted", CodePhrase("openehr", "523"))
    INACTIVE = DVCodedText("inactive", CodePhrase("openehr", "800"))
    ABANDONED = DVCodedText("abandoned", CodePhrase("openehr", "801"))

class VersionedStore():

    db: IDatabaseEngine

    system_id: str

    def __init__(self, db_engine: IDatabaseEngine, system_id: str):
        """Create a new versioned store, to be used for interacting with a database
        in a versioned manner."""
        self.db = db_engine
        self.system_id = system_id
        
    def create(self, 
               object: AnyClass, 
               committer: PartyProxy,
               lifecycle_state: VersionLifecycleState,
               description: Optional[DVText] = None) -> tuple[OriginalVersion, Contribution, VersionedObject, RevisionHistoryItem]:
        """Create the first version `obj_id::sys_id::1` of a versioned object into the store.
        
        Generates, saves and returns a `CONTRIBUTION` and `VERSION` and creates a `VERSIONED_OBJECT` and `REVISION_HISTORY_ITEM` and returns these also.
        `AUDIT_DETAILS` will use change_type of `249|creation`.
        
        Raises an error if this version, or associated `VERSIONED_OBJECT` already exists."""
        pass

    def update(self, 
               object: AnyClass, 
               committer: PartyProxy,
               lifecycle_state: VersionLifecycleState,
               change_type: AuditChangeType,
               preceding_version_uid: Optional[ObjectVersionID] = None,
               description: Optional[DVText] = None,
               local_versioned_object: Optional[VersionedObject] = None) -> Optional[VersionedObject]:
        """Update a given version and create a new trunk version. Unless specified, finds latest version
        and assumes this is the preceding version.
        
        Generates, saves and returns a `CONTRIBUTION` and `VERSION` and `REVISION_HISTORY_ITEM` and modifies existing `VERSIONED_OBJECT`.
        
        Raises an error if no previous version exists, or if the version given by preceding_version_uid does not exist."""
        pass

    def commit(self,
               committer: PartyProxy,
               commit_change_type: AuditChangeType,
               objects: list[tuple[AnyClass, VersionLifecycleState, AuditChangeType, Optional[ObjectVersionID], Optional[DVText], Optional[VersionedObject]]],
               commit_description: Optional[DVText] = None):
        """Commit a set of new object versions at the same time. If change type is creation, object is created as first version, otherwise 
        updated.
        
        Generates, saves and returns a `CONTRIBUTION`, list of new `VERSIONs` and `REVISION_HSITORY_ITEMs` and modifies existing `VERSIONED_OBJECTs`.
        
        For objects being updated, raises an error if no previous version exists, or if the version given by preceding_version_uid does not exist."""
        pass
    
    def attest(self,
               obj_type: str,
               obj_version_id: ObjectVersionID,
               attester: PartyProxy,
               reason: DVText,
               is_pending: bool,
               attested_view: Optional[DVMultimedia],
               local_versioned_object: Optional[VersionedObject] = None):
        """Updates a given version to note that a clinician has explicitly attested the given content.
        
        Updates an existing object with a new trunk version to add the attestation and creates a new `REVISION_HISTORY_ITEM`"""

    def read_latest(self,
             obj_type: str,
             obj_id: HierObjectID,
             reader: PartyProxy) -> Version:
        """Retrieves the latest version of the object of the given type."""
        pass

    def read_version(self,
                     obj_type: str,
                     obj_version_id: ObjectVersionID,
                     reader: PartyProxy) -> Version:
        """Retrieves a given version of the object of the given type."""
        pass

    def query_equal(self,
              obj_type: str,
              archetype_id: ArchetypeID,
              query_dict: dict[str, list[str]], 
              reader: PartyProxy) -> Version:
        """Retrieves a version of the object of the given type with parameters equal to those in query dict.
        
        :param query_dict: OpenEHR path for target attribute and list of possible values (e.g. {'details/items[at0002]/value/id': ['9449305552']})"""
        pass

    def retrieve_versioned_object(self, 
                                  uid: HierObjectID, 
                                  reader: PartyProxy,
                                  metadata_only_versioned_object: bool = True) -> tuple[VersionedObject, RevisionHistory]:
        """Retrieve a VERSIONED_OBJECT and its underlying REVISION_HISTORY."""
        pass

