
from enum import Enum
from typing import Optional
from logging import Logger, getLogger

from term import TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import UUID, ArchetypeID, HierObjectID, ObjectID, ObjectRef, ObjectVersionID, PartyRef, UIDBasedID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.time import ISODateTime
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
        
    def _get_uid_from_object_if_exists(self, obj: Optional[AnyClass]) -> Optional[ObjectID]:
        if obj is None:
            return None
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

        commit_time = DVDateTime(Env.current_date_time())
    
        audit = AuditDetails(
            system_id=self.system_id,
            time_committed=commit_time,
            change_type=AuditChangeType.CREATION.value,
            committer=committer,
            terminology_service=self._ts,
            description=description
        )

        # create the contribution
        self._log.info(f"Creating CONTRIBUTION (uid=\'{contrib_id.value}\', commit_time=\'{commit_time.as_string()}\')")
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
        
        # set object UID field to the version ID
        if hasattr(obj, "uid"):
            obj.uid = ver_id

        # save to the database
        self._log.info("Saving to database")
        self.db.create_versioned_object(vo, create_underlying_versions=True, creator=user)
        self.db.create_uid_object(contrib, creator=user)

        return (ver_id, contrib, vo)
    
    def _update_version(self,
                        obj: AnyClass,
                        lifecycle_state: VersionLifecycleState,
                        contrib_id: HierObjectID,
                        audit: AuditDetails,
                        preceding_version_uid: Optional[ObjectVersionID] = None,
                        user: Optional[PartyRef] = None) -> tuple[str, OriginalVersion]:
        # get UID from object if it exists
        uid = self._get_uid_from_object_if_exists(obj)

        if uid is not None:
            if isinstance(uid, HierObjectID) and preceding_version_uid is not None and preceding_version_uid.object_id().value != uid.value:
                raise ValueError(f"UID within `preceding_version_uid` ({preceding_version_uid.value}) does not match the UID within the object ({uid.value})")
            elif isinstance(uid, ObjectVersionID) and preceding_version_uid is not None and preceding_version_uid.object_id().value != uid.object_id().value:
                raise ValueError(f"UID within `preceding_version_uid` ({preceding_version_uid.value}) does not match the UID within the object version ID ({uid.value})")
        else:
            if preceding_version_uid is None:
                raise ValueError(f"Cannot update/delete object as object did not have a UID and `preceding_version_uid` was not provided.")
            else:
                uid = preceding_version_uid.object_id()
            
        # find the preceding version UID
        if preceding_version_uid is None:
            self._log.info("Preceding version not explicitly given, finding latest version")
            vo_meta, rev_his = self.db.retrieve_versioned_object(uid, reader=user)

            prev_ver = rev_his.most_recent_version()
            self._log.info(f"Assuming this version based off {preceding_version_uid}")
            preceding_version_uid = ObjectVersionID(prev_ver)

        obj_type = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)] if obj is not None else None

        # make the new version ID and contribution ID
        new_version_id = uid
        if isinstance(uid, HierObjectID) or isinstance(uid, UUID):
            # new version ID not given in object so bump the trunk up
            new_trunk = int(preceding_version_uid.version_tree_id().trunk_version()) + 1
            new_version_id = ObjectVersionID(uid.value + "::" + self.system_id + "::" + str(new_trunk))

        # set object UID field to the version ID
        if obj is not None and hasattr(obj, "uid"):
            obj.uid = new_version_id

        return (obj_type, OriginalVersion(
            contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
            commit_audit=audit,
            uid=new_version_id,
            lifecycle_state=lifecycle_state.value,
            terminology_service=self._ts,
            data=obj,
            preceding_version_uid=preceding_version_uid
        ))
        

    def update(self, 
               obj: AnyClass, 
               committer: PartyProxy,
               lifecycle_state: VersionLifecycleState,
               change_type: AuditChangeType,
               preceding_version_uid: Optional[ObjectVersionID] = None,
               description: Optional[DVText] = None,
               user: Optional[PartyRef] = None,
               local_versioned_object: Optional[VersionedObject] = None,
               explicit_obj_type: Optional[str] = None) -> tuple[ObjectVersionID, Contribution, Optional[VersionedObject]]:
        """Update a given version and create a new trunk version. Unless specified, finds latest version
        and assumes this is the preceding version.
        
        Generates, saves and returns a `CONTRIBUTION` and `VERSION` and `REVISION_HISTORY_ITEM` and modifies existing `VERSIONED_OBJECT`.
        
        Raises an error if no previous version exists, if `obj` has no UID and no preceding_version_uid was given, or if the version given by preceding_version_uid does not exist.
        
        :param preceding_version_uid: Mandatory if `obj` does not contain a UID. Otherwise, if not provided, the latest version of `obj` in the database
                                      will be taken as the preceding version for this update.
        :param user: The user which will be recorded in the database logs
        :param obj_type: Needed if obj is `None` (i.e. blank version is being created) so type cannot be inferred."""

        contrib_id = self.db.generate_hier_object_id()

        commit_time = DVDateTime(Env.current_date_time())

        audit = AuditDetails(
            system_id=self.system_id,
            time_committed=commit_time,
            change_type=change_type.value,
            committer=committer,
            terminology_service=self._ts,
            description=description
        )

        # make the new version
        obj_type, ov = self._update_version(
            obj=obj,
            lifecycle_state=lifecycle_state,
            contrib_id=contrib_id,
            audit=audit,
            preceding_version_uid=preceding_version_uid,
            user=user
        )
        if obj_type is None:
            if explicit_obj_type is None:
                raise ValueError("Cannot have obj of `None` without explicit_obj_type set")
            obj_type = explicit_obj_type
        new_version_id = ov.uid()
        uid = ov.uid().object_id()
        self._log.info(f"Created {'(deletion)' if obj is None else ''} VERSION<{obj_type}> (uid=\'{new_version_id.value}\')")

        # create the contribution
        self._log.info(f"Creating CONTRIBUTION (uid=\'{contrib_id.value}\', commit_time=\'{commit_time.as_string()}\')")
        contrib = Contribution(
            uid=contrib_id,
            versions=[ObjectRef("local", f"VERSION<{obj_type}>", new_version_id)],
            audit=audit
        )

        # and a revision history item
        self._log.info("Creating REVISION_HISTORY_ITEM")
        rhi = RevisionHistoryItem(
            version_id=new_version_id,
            audits=[audit]
        )
        
        # save to database
        self._log.info("Saving to database")
        if obj is None:
            self.db.create_uid_object(ov, creator=user, type_override=f"VERSION<{obj_type}>")
        else:
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

    def delete(self, 
               obj_type: str,
               deleter: PartyProxy,
               preceding_version_uid: ObjectVersionID,
               description: Optional[DVText] = None,
               user: Optional[PartyRef] = None,
               local_versioned_object: Optional[VersionedObject] = None):
        """(Soft) delete an object by creating a new `VERSION` with no content, and marking relevant fields as inactive/delete.
        
        Shorthand for VersionedStore.update with relevant audit change type, version lifecycle state, etc. set.
        
        :param preceding_version_uid: Object version ID of the last version prior to deletion.
        :param user: The user which will be recorded in the database logs"""
        return self.update(None, deleter, VersionLifecycleState.DELETE, AuditChangeType.DELETED, preceding_version_uid, description, user, local_versioned_object, explicit_obj_type=obj_type)

    def commit(self,
               owner_id: ObjectRef,
               committer: PartyProxy,
               commit_change_type: AuditChangeType,
               objects: list[tuple[AnyClass, VersionLifecycleState, AuditChangeType, Optional[ObjectVersionID], Optional[DVText], Optional[VersionedObject]]],
               commit_description: Optional[DVText] = None,
               user: Optional[PartyRef] = None) -> tuple[list[ObjectVersionID], Contribution, list[Optional[VersionedObject]]]:
        """Commit a set of new object versions at the same time. If change type is creation, object is created as first version, otherwise 
        updated.
        
        Generates, saves and returns a `CONTRIBUTION`, list of new `VERSIONs` and `REVISION_HSITORY_ITEMs` and modifies existing `VERSIONED_OBJECTs`.
        
        For objects being updated, raises an error if no previous version exists, or if the version given by preceding_version_uid does not exist."""
        contrib_id = self.db.generate_hier_object_id()
        commit_time = Env.current_date_time()

        self._log.info(f"Started preparing commit for CONTRIBUTION (uid=\'{contrib_id.value}\', commit_time=\'{commit_time}\')")

        commit_audit = AuditDetails(
            system_id=self.system_id,
            time_committed=commit_time,
            change_type=commit_change_type.value,
            committer=committer,
            terminology_service=self._ts,
            description=commit_description
        )
        
        versions = []
        versions_references = []
        versions_id_list = []
        local_versioned_object_list = []

        for i in range(0, len(objects)):
            obj_tuple = objects[i]

            obj = obj_tuple[0]
            lifecycle_state = obj_tuple[1]
            audit_change_type = obj_tuple[2]
            preceding_version_uid = obj_tuple[3]
            description = obj_tuple[4]
            local_versioned_object = obj_tuple[5]

            # create an audit details, same as commit except change_type reflects changes to this object in particular
            obj_audit = AuditDetails(
                system_id=self.system_id,
                time_committed=commit_time,
                change_type=audit_change_type.value,
                committer=committer,
                terminology_service=self._ts,
                description=(description if description is not None else commit_description)
            )

            if audit_change_type == AuditChangeType.CREATION:
                # create a new version
                if preceding_version_uid is not None:
                    raise ValueError(f"Aborting commit. objects[{str(i)}] had change type of CREATION but a preceding_version_uid was given")
                
                # find the UID if the object has one, otherwise generate one
                uid = self._get_uid_from_object_if_exists(obj)

                if uid is not None:
                    meta = self.db.retrieve_db_metadata(uid, reader=user)
                    if meta is not None:
                        raise ValueError(f"Aborting commit. objects[{str(i)}] with UID {uid.value} could not be created it already exists in database")
                else:
                    uid = self.db.generate_hier_object_id(generator=user)

                # create the object ID
                created_verid = ObjectVersionID(uid.value + "::" + self.system_id + "::1")
                obj_type = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

                # create a version to add to the commit
                created_version = OriginalVersion(
                    contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
                    commit_audit=obj_audit,
                    uid=created_verid,
                    lifecycle_state=lifecycle_state.value,
                    terminology_service=self._ts,
                    data=obj
                )

                versions.append(created_version)
                versions_references.append(ObjectRef("local", f"VERSION<{obj_type}>", created_verid))
                versions_id_list.append(created_verid)

                if local_versioned_object is not None:
                    local_versioned_object.commit_original_version(
                        a_contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
                        a_new_version_uid=created_verid,
                        a_preceding_version_id=None,
                        an_audit=obj_audit,
                        a_lifecycle_state=lifecycle_state.value,
                        a_data=obj,
                        terminology_service=self._ts
                    )
                    local_versioned_object_list.append(local_versioned_object)
                else:
                    local_versioned_object_list.append(None)
                
                self._log.info(f"Added creation of VERSION<{obj_type}> to commit (uid=\'{created_verid.value}\')")
            else:
                # otherwise prepare a version for an update
                obj_type, updated_version = self._update_version(
                    obj=obj,
                    lifecycle_state=lifecycle_state,
                    contrib_id=contrib_id,
                    audit=obj_audit,
                    preceding_version_uid=preceding_version_uid,
                    user=user
                )

                versions.append(updated_version)
                versions_references.append(ObjectRef("local", f"VERSION<{obj_type}>", updated_version.uid()))
                versions_id_list.append(updated_version.uid())

                if local_versioned_object is not None:
                    local_versioned_object.commit_original_version(
                        a_contribution=ObjectRef("local", "CONTRIBUTION", contrib_id),
                        a_new_version_uid=updated_version.uid(),
                        a_preceding_version_id=preceding_version_uid,
                        an_audit=obj_audit,
                        a_lifecycle_state=lifecycle_state.value,
                        a_data=obj,
                        terminology_service=self._ts
                    )
                    local_versioned_object_list.append(local_versioned_object)
                else:
                    local_versioned_object_list.append(None)

                self._log.info(f"Added update of VERSION<{obj_type}> to commit (uid=\'{updated_version.uid().value}\')")
        
        # create contribution
        contrib = Contribution(
            uid=contrib_id,
            versions=versions_references,
            audit=commit_audit
        )
        self._log.info("Created CONTRIBUTION for commit")

        self._log.info("Committing to database")
        self.db.commit_contribution_set(
            contrib=contrib,
            versions=versions,
            owner_id=owner_id,
            committer=user
        )

        return (versions_id_list, contrib, local_versioned_object_list)
    
    def attest(self,
               obj_type: str,
               obj_version_id: ObjectVersionID,
               attester: PartyProxy,
               reason: DVText,
               is_pending: bool,
               description: Optional[DVText] = None,
               attested_view: Optional[DVMultimedia] = None,
               local_versioned_object: Optional[VersionedObject] = None,
               user: Optional[PartyRef] = None) -> Optional[VersionedObject]:
        """Updates a given version to note that a clinician has explicitly attested the given content.
        
        Updates an existing object with a new trunk version to add the attestation and creates a new `REVISION_HISTORY_ITEM`
        
        :param user: """
        self._log.info(f"Created new ATTESTATION for {obj_version_id.value}")
        attest = Attestation(
            system_id=self.system_id,
            time_committed=Env.current_date_time(),
            change_type=AuditChangeType.ATTESTATION.value,
            committer=attester,
            reason=reason,
            is_pending=is_pending,
            terminology_service=self._ts,
            description=description,
            attested_view=attested_view
        )
        self._log.info("Saving to database")
        self.db.add_attestation(obj_version_id, attest, user)

        if local_versioned_object is not None:
            local_versioned_object.commit_attestation(
                attest,
                obj_version_id
            )
            return local_versioned_object
        else:
            return None

    def read(self,
             obj_type: str,
             obj_id: HierObjectID,
             version_at_time: Optional[DVDateTime] = None,
             user: Optional[PartyRef] = None) -> Version:
        """Retrieves the latest version of the object of the given type, or the version extant at `version_at_time` if this is provided."""
        # get the versioned object with list of versions
        vo, revs = self.db.retrieve_versioned_object(obj_id, user)

        ver_id_to_get = None

        if version_at_time is None:
            self._log.info(f"Retrieving latest VERSION<{obj_type}> for VERSIONED_OBJECT (uid=\'{obj_id.value}\')")
            # most recent last so most recent version is last item
            ver_id_to_get = revs.items[-1].version_id
        else:
            self._log.info(f"Retrieving VERSION<{obj_type}> extant at {version_at_time.as_string()} for VERSIONED_OBJECT (uid=\'{obj_id.value}\')")
            for rev_history_item in revs.items[::-1]:
                # start with most recent and go backwards until version_at_time is larger than the committed_time
                #  (i.e. the most recent version extant at `version_at_time`)
                if version_at_time >= rev_history_item.audits[0].time_committed:
                    ver_id_to_get = rev_history_item.version_id
                    break

        if ver_id_to_get is None:
            self._log.warning(f"No VERSION<{obj_type}> extant at \'{version_at_time}\'")
            return None
        else:
            return self.db.retrieve_uid_object(f"VERSION<{obj_type}>", ver_id_to_get, user)

    def read_version(self,
                     obj_type: str,
                     obj_version_id: ObjectVersionID,
                     user: Optional[PartyRef] = None) -> Version:
        """Retrieves a given version of the object of the given type."""
        return self.db.retrieve_uid_object(f"VERSION<{obj_type}>", obj_version_id, user)

    def query_equal(self,
              obj_type: str,
              archetype_id: ArchetypeID,
              query_dict: dict[str, list[str]], 
              user: Optional[PartyRef] = None) -> Version:
        """Retrieves a version of the object of the given type with parameters equal to those in query dict.
        
        :param query_dict: OpenEHR path for target attribute and list of possible values (e.g. {'details/items[at0002]/value/id': ['9449305552']})"""
        return self.db.retrieve_query_match_object(obj_type, archetype_id, query_dict, user)

    def retrieve_versioned_object(self, 
                                  uid: HierObjectID, 
                                  user: Optional[PartyRef] = None,
                                  metadata_only_versioned_object: bool = True) -> tuple[VersionedObject, RevisionHistory]:
        """Retrieve a VERSIONED_OBJECT and its underlying REVISION_HISTORY."""
        return self.db.retrieve_versioned_object(uid, user, metadata_only_versioned_object)

