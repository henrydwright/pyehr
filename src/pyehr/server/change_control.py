
from enum import Enum
from typing import Optional
from logging import Logger, getLogger

from common import TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import UUID, ArchetypeID, HierObjectID, ObjectID, ObjectRef, ObjectVersionID, PartyRef, UIDBasedID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.archetyped import Locatable
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, Version, VersionedObject
from pyehr.core.rm.common.generic import Attestation, AuditDetails, PartyProxy, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.encapsulated import DVMultimedia
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.support.terminology import TerminologyService
from pyehr.server.database import IDatabaseEngine
from pyehr.utils import PYTHON_TYPE_TO_STRING_TYPE_MAP

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
    """Class which provides a persistent, version-controlled, store for all pyehr objects via
    methods which work with `VERSIONED_OBJECTs` and `VERSIONs` within a given database."""

    _log: Logger

    _ts: TerminologyService

    db: IDatabaseEngine

    system_id: str

    def __init__(self, db_engine: IDatabaseEngine, system_id: str, terminology_service: Optional[TerminologyService] = None):
        """Create a new versioned store, to be used for interacting with a database
        in a versioned manner.
        
        :param terminology_service: Terminology service containing OpenEHR support terminology. If not provided, pyehr's default service
                                     is used."""
        self.db = db_engine
        self.system_id = system_id
        self._log = getLogger("VersionedStore")
        if terminology_service is None:
            self._ts = PythonTerminologyService([], [TERMINOLOGY_OPENEHR])
        else:
            self._ts = terminology_service
        
    def _get_uid_from_object_if_exists(self, obj: AnyClass) -> Optional[ObjectID]:
        uid = None
        if hasattr(obj, "uid"):
            uid = obj.uid
            if callable(uid):
                uid = uid()
        return uid

    def create(self, 
               obj: AnyClass, 
               owner_id: ObjectRef,
               committer: PartyProxy,
               lifecycle_state: VersionLifecycleState,
               description: Optional[DVText] = None,
               user: Optional[PartyRef] = None) -> tuple[ObjectVersionID, Contribution, VersionedObject]:
        """Create the first version `obj_id::sys_id::1` of a versioned object into the store.
        
        Generates, saves and returns a `CONTRIBUTION`; and `VERSIONED_OBJECT` containing a new `VERSION` and associated `REVISION_HISTORY_ITEM`.
        `AUDIT_DETAILS` will use change_type of `249|creation`.
        
        Raises an error if a `VERSIONED_OBJECT` with the uid in `obj` (if it has one) already exists.
        
        :param user: The user which will be recorded in the database logs"""
        # find the UID if the object has one, otherwise generate one
        uid = self._get_uid_from_object_if_exists(obj)

        if uid is not None:
            meta = self.db.retrieve_db_metadata(uid, reader=user)
            if meta is not None:
                raise ValueError(f"Cannot store first version of object with UID {uid.value} as it already exists in database")
        else:
            uid = self.db.generate_hier_object_id(generator=user)

        # get the object's string type
        obj_type = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]
        
        # create the versioned object that will hold the versions of this item
        self._log.info(f"Creating VERSIONED_OBJECT (uid=\'{uid.value}\')")
        vo = VersionedObject(
            uid=uid,
            owner_id=owner_id,
            time_created=DVDateTime(Env.current_date_time())
        )

        ver_id = ObjectVersionID(uid.value + "::" + self.system_id + "::1")
        contrib_id = self.db.generate_hier_object_id()

        audit = AuditDetails(
            system_id=self.system_id,
            time_committed=DVDateTime(Env.current_date_time()),
            change_type=AuditChangeType.CREATION.value,
            committer=committer,
            terminology_service=self._ts,
            description=description
        )

        # create the contribution
        self._log.info(f"Creating CONTRIBUTION (uid=\'{contrib_id.value}\')")
        contrib = Contribution(
            uid=contrib_id,
            versions=[ObjectRef("local", f"VERSION<{obj_type}>", ver_id)],
            audit=audit
        )

        # create the version in the VERSIONED_OBJECT
        self._log.info(f"Creating VERSION<{obj_type}> (uid=\'{ver_id.value}\')")
        vo.commit_original_version(
            a_contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
            a_new_version_uid=ver_id,
            a_preceding_version_id=None,
            an_audit=audit,
            a_lifecycle_state=lifecycle_state.value,
            a_data=obj,
            terminology_service=self._ts
        )

        # save to the database
        self._log.info("Saving to database")
        self.db.create_versioned_object(vo, create_underlying_versions=True, creator=user)
        self.db.create_uid_object(contrib, creator=user)

        return (ver_id, contrib, vo)
    
    def update(self, 
               obj: AnyClass, 
               committer: PartyProxy,
               lifecycle_state: VersionLifecycleState,
               change_type: AuditChangeType,
               preceding_version_uid: Optional[ObjectVersionID] = None,
               description: Optional[DVText] = None,
               user: Optional[PartyRef] = None,
               local_versioned_object: Optional[VersionedObject] = None) -> tuple[ObjectVersionID, Contribution, Optional[VersionedObject]]:
        """Update a given version and create a new trunk version. Unless specified, finds latest version
        and assumes this is the preceding version.
        
        Generates, saves and returns a `CONTRIBUTION` and `VERSION` and `REVISION_HISTORY_ITEM` and modifies existing `VERSIONED_OBJECT`.
        
        Raises an error if no previous version exists, if `obj` has no UID and no preceding_version_uid was given, or if the version given by preceding_version_uid does not exist.
        
        :param preceding_version_uid: Mandatory if `obj` does not contain a UID. Otherwise, if not provided, the latest version of `obj` in the database
                                      will be taken as the preceding version for this update."""
        # get UID from object if it exists
        uid = self._get_uid_from_object_if_exists(obj)

        if uid is not None:
            if isinstance(uid, HierObjectID) and preceding_version_uid is not None and preceding_version_uid.object_id().value != uid.value:
                raise ValueError(f"UID within `preceding_version_uid` ({preceding_version_uid.value}) does not match the UID within the object ({uid.value})")
            elif isinstance(uid, ObjectVersionID) and preceding_version_uid is not None and preceding_version_uid.object_id().value != uid.object_id().value:
                raise ValueError(f"UID within `preceding_version_uid` ({preceding_version_uid.value}) does not match the UID within the object version ID ({uid.value})")
        else:
            if preceding_version_uid is None:
                raise ValueError(f"Cannot update object as object did not have a UID and `preceding_version_uid` was not provided.")
            else:
                uid = preceding_version_uid.object_id()
            
        # find the preceding version UID
        if preceding_version_uid is None:
            self._log.info("Preceding version not explicitly given, finding latest version")
            vo_meta, rev_his = self.db.retrieve_versioned_object(uid, reader=user)

            prev_ver = rev_his.most_recent_version()
            self._log.info(f"Assuming this version based off {preceding_version_uid}")
            preceding_version_uid = ObjectVersionID(prev_ver)

        obj_type = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

        # make the new version ID and contribution ID
        new_version_id = uid
        if isinstance(uid, HierObjectID) or isinstance(uid, UUID):
            # new version ID not given in object so bump the trunk up
            new_trunk = int(preceding_version_uid.version_tree_id().trunk_version()) + 1
            new_version_id = ObjectVersionID(uid.value + "::" + self.system_id + "::" + str(new_trunk))
        contrib_id = self.db.generate_hier_object_id()

        # set object UID field to the version ID
        if hasattr(obj, "uid"):
            obj.uid = new_version_id

        commit_time = DVDateTime(Env.current_date_time())

        audit = AuditDetails(
            system_id=self.system_id,
            time_committed=commit_time,
            change_type=change_type.value,
            committer=committer,
            terminology_service=self._ts,
            description=description
        )

        # create the contribution
        self._log.info(f"Creating CONTRIBUTION (uid=\'{contrib_id.value}\')")
        contrib = Contribution(
            uid=contrib_id,
            versions=[ObjectRef("local", f"VERSION<{obj_type}>", new_version_id)],
            audit=audit
        )

        # make the new version
        self._log.info(f"Creating VERSION<{obj_type}> (uid=\'{new_version_id.value}\')")
        ov = OriginalVersion(
            contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
            commit_audit=audit,
            uid=new_version_id,
            lifecycle_state=lifecycle_state.value,
            terminology_service=self._ts,
            data=obj,
            preceding_version_uid=preceding_version_uid
        )

        # and a revision history item
        self._log.info("Creating REVISION_HISTORY_ITEM")
        rhi = RevisionHistoryItem(
            version_id=new_version_id,
            audits=[audit]
        )
        
        # save to database
        self._log.info("Saving to database")
        self.db.create_uid_object(ov, creator=user)
        self.db.add_revision_history_item(uid, rhi, creator=user)
        self.db.create_uid_object(contrib, creator=user)

        # if provided, update the versioned object
        if local_versioned_object is not None:
            local_versioned_object.commit_original_version(
                a_contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
                a_new_version_uid=new_version_id,
                a_preceding_version_id=preceding_version_uid,
                an_audit=audit,
                a_lifecycle_state=lifecycle_state.value,
                a_data=obj,
                terminology_service=self._ts
            )

        return (new_version_id, contrib, local_versioned_object)

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

