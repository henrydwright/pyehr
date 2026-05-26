

from logging import Logger, getLogger
from typing import Optional

from pyehr.client.demographic import OpenEHRDemographicRestClient, OpenEHRPartyType
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectID, ObjectRef, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.rest.additions import UpdateAudit, UpdateVersion
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, Version, VersionedObject
from pyehr.core.rm.common.generic import PartyProxy, RevisionHistory
from pyehr.core.rm.data_types.encapsulated import DVMultimedia
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.demographic import Party, VersionedParty
from pyehr.core.rm.support.terminology import TerminologyService
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState
from pyehr.utils import PYTHON_TYPE_TO_STRING_TYPE_MAP

from pyehr.term import PyehrGlobalTerminologyService

DEMOGRAPHIC_CLIENT_TYPE = {"AGENT", "GROUP", "ORGANISATION", "PERSON", "ROLE"}

class VersionedStoreClient():
    """Class which provides a persistent, version-controlled, store for all pyehr objects via
    methods which work with `VERSIONED_OBJECTs` and `VERSIONs` on a remote server via the 
    OpenEHR REST API.
    
    Client version of VersionedStore."""

    base_url : str

    _ts: TerminologyService

    _log: Logger

    def __init__(self, base_url: str, terminology_service: Optional[TerminologyService] = None):
        self.base_url = base_url
        self._log = getLogger("client.versionedStoreClient")
        if terminology_service is None:
            self._ts = PyehrGlobalTerminologyService.get_global_terminology_service()
        else:
            self._ts = terminology_service

    def _str_type_or_error(self, obj: AnyClass):
        if type(obj) not in PYTHON_TYPE_TO_STRING_TYPE_MAP:
            raise NotImplementedError(f"Object of type `{str(type(obj))}` is not yet supported or is not a valid OpenEHR type")
        else:
            return PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

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
            description: Optional[DVText] = None) -> tuple[ObjectVersionID, Contribution, VersionedObject]:
        """Create the first version `obj_id::sys_id::1` of a versioned object into the store.
        
        Generates, saves and returns a `CONTRIBUTION`; and `VERSIONED_OBJECT` containing a new `VERSION` and associated `REVISION_HISTORY_ITEM`.
        `AUDIT_DETAILS` will use change_type of `249|creation`.
        
        Raises an error if a `VERSIONED_OBJECT` with the uid in `obj` (if it has one) already exists."""
        oe_type = self._str_type_or_error(obj)
        if oe_type in DEMOGRAPHIC_CLIENT_TYPE:
            demo_client = OpenEHRDemographicRestClient(self.base_url)
            self._log.info(f"Creating new \'{oe_type}\' on remote server")

            desc_str = None if description is None else description.value

            # create party on remote
            resp = demo_client.party.create_party(OpenEHRPartyType(oe_type), obj, lifecycle_state, desc_str, committer)
            ovid : ObjectVersionID = resp.pyehr_obj.uid
            vp_uid = HierObjectID(ovid.object_id().value)
            self._log.info(f"Created \'{oe_type}\' with Object Version ID {ovid.value}. Retrieving new VERSION object.")

            # get version metadata to be able to recreate VERSIONED_PARTY
            resp_ver = demo_client.versioned_party.get_versioned_party_version_by_id(vp_uid, ovid)
            ver: OriginalVersion[Party] = resp_ver.pyehr_obj
            contrib_id = ver.contribution.id
            vp = VersionedParty(
                uid=vp_uid,
                owner_id=ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000")),
                time_created=ver.commit_audit.time_committed
            )
            vp.commit_original_version(
                a_contribution=ver.contribution,
                a_new_version_uid=ver.uid(),
                a_preceding_version_id=ver.preceding_version_uid(),
                an_audit=ver.commit_audit,
                a_lifecycle_state=ver.lifecycle_state(),
                a_data=ver.data(),
                terminology_service=self._ts
            )

            # retrieve the contribution to be able to return it
            resp_contrib = demo_client.contribution.get_contribution_by_id(contrib_id)
            contrib = resp_contrib.pyehr_obj

            return (ovid, contrib, vp)
        else:
            raise NotImplementedError(f"Cannot create object of type `{oe_type}` as the client does not yet support this type")
        
            
    
    def update(self, 
            obj: AnyClass, 
            committer: PartyProxy,
            lifecycle_state: VersionLifecycleState,
            change_type: AuditChangeType,
            preceding_version_uid: Optional[ObjectVersionID] = None,
            description: Optional[DVText] = None,
            local_versioned_object: Optional[VersionedObject] = None,
            explicit_obj_type: Optional[str] = None) -> tuple[ObjectVersionID, Contribution, Optional[VersionedObject]]:
        """Update a given version and create a new trunk version. Unless specified, finds latest version
        and assumes this is the preceding version.
        
        Generates, saves and returns a `CONTRIBUTION` and `VERSION` and `REVISION_HISTORY_ITEM` and modifies existing `VERSIONED_OBJECT`.
        
        Raises an error if no previous version exists, if `obj` has no UID and no preceding_version_uid was given, or if the version given by preceding_version_uid does not exist.
        
        :param preceding_version_uid: Mandatory if `obj` does not contain a UID. Otherwise, if not provided, the latest version of `obj` on the remote server
                                      will be taken as the preceding version for this update.
        :param user: The user which will be recorded in the database logs
        :param obj_type: Needed if obj is `None` (i.e. blank version is being created) so type cannot be inferred."""
        
        desc_str = None if description is None else description.value

        oe_type = explicit_obj_type if explicit_obj_type is not None else self._str_type_or_error(obj)
        if oe_type in DEMOGRAPHIC_CLIENT_TYPE:
            demo_client = OpenEHRDemographicRestClient(self.base_url)
            uid = self._get_uid_from_object_if_exists(obj)

            # find the preceding version UID if not given
            if preceding_version_uid is None:
                self._log.info("Preceding version not explicitly given, finding latest version")
                revhis_resp = demo_client.versioned_party.get_versioned_party_revision_history(uid)
                revhis : RevisionHistory = revhis_resp.pyehr_obj
                preceding_version_uid = ObjectVersionID(revhis.most_recent_version())
                self._log.info(f"Assuming this version based off {preceding_version_uid.value}")

            self._log.info(f"Updating \'{oe_type}\' with UID {uid.value} on remote server")
            resp = demo_client.party.update_party(
                party_type=OpenEHRPartyType(oe_type),
                uid_based_id=uid,
                preceding_version_uid=preceding_version_uid,
                new_party=obj,
                version_lifecycle_state=lifecycle_state,
                version_audit_change_type=change_type,
                version_audit_description=desc_str,
                version_committer=committer)
            
            new_ovid = resp.pyehr_obj.uid
            self._log.info(f"Updated \'{oe_type}\' has object version ID {new_ovid.value}. Retrieving new VERSION object.")

            # get version metadata to be able to update VERSIONED_PARTY (and return contribution)
            resp_ver = demo_client.versioned_party.get_versioned_party_version_by_id(uid, new_ovid)
            ver: OriginalVersion[Party] = resp_ver.pyehr_obj
            contrib_id = ver.contribution.id
            
            if local_versioned_object is not None:
                local_versioned_object.commit_original_version(
                    a_contribution=ver.contribution,
                    a_new_version_uid=ver.uid(),
                    a_preceding_version_id=ver.preceding_version_uid(),
                    an_audit=ver.commit_audit,
                    a_lifecycle_state=ver.lifecycle_state(),
                    a_data=ver.data(),
                    terminology_service=self._ts
                )

            # retrieve the contribution to be able to return it
            resp_contrib = demo_client.contribution.get_contribution_by_id(contrib_id)
            contrib = resp_contrib.pyehr_obj

            return (new_ovid, contrib, local_versioned_object)
        else:
            raise NotImplementedError(f"Cannot create object of type `{oe_type}` as the client does not yet support this type")

    
    def delete(self, 
            obj_type: str,
            deleter: PartyProxy,
            preceding_version_uid: ObjectVersionID,
            description: Optional[DVText] = None,
            local_versioned_object: Optional[VersionedObject] = None):
        """(Soft) delete an object by creating a new `VERSION` with no content, and marking relevant fields as inactive/delete.
        
        Shorthand for VersionedStore.update with relevant audit change type, version lifecycle state, etc. set.
        
        :param preceding_version_uid: Object version ID of the last version prior to deletion."""
        return self.update(None, deleter, VersionLifecycleState.DELETE, AuditChangeType.DELETED, preceding_version_uid, description, local_versioned_object, explicit_obj_type=obj_type)

    def commit(self,
            owner_id: ObjectRef,
            committer: PartyProxy,
            commit_change_type: AuditChangeType,
            objects: list[tuple[AnyClass, VersionLifecycleState, AuditChangeType, Optional[ObjectVersionID], Optional[DVText], Optional[VersionedObject]]],
            commit_description: Optional[DVText] = None) -> tuple[list[ObjectVersionID], Contribution, list[Optional[VersionedObject]]]:
        """Commit a set of new object versions at the same time. If change type is creation, object is created as first version, otherwise 
        updated.
        
        Generates, saves and returns a `CONTRIBUTION`, list of new `VERSIONs` and `REVISION_HSITORY_ITEMs` and modifies existing `VERSIONED_OBJECTs`.
        
        For objects being updated, raises an error if no previous version exists, or if the version given by preceding_version_uid does not exist."""
        if len(objects) == 0:
            raise ValueError("Cannot produce an empty commit (empty objects list provided).")
        all_demographic_type = True
        all_ehr_type = True

        # check all objects in the array are of the same type category (i.e. EHR or DEMOGRAPHIC)
        for (obj, vls, act, ovid, desc, local_vo) in objects:
            oe_type = self._str_type_or_error(obj)
            all_demographic_type = all_demographic_type and (oe_type in DEMOGRAPHIC_CLIENT_TYPE)
            all_ehr_type = all_ehr_type and (oe_type not in DEMOGRAPHIC_CLIENT_TYPE)

        
        if not all_demographic_type and not all_ehr_type:
            raise TypeError("Found mixed types between DEMOGRAPHIC and EHR types in objects list, but this is not possible for a commit.")
        elif all_demographic_type:
            demo_client = OpenEHRDemographicRestClient(self.base_url)

            self._log.info(f"Started preparing commit for CONTRIBUTION.")

            commit_audit = UpdateAudit(
                change_type=commit_change_type.value,
                committer=committer,
                terminology_service=self._ts,
                description=commit_description
            )
            
            versions = []
            preceding_version_uids = []
            local_versioned_object_list = []
            oe_types = []

            for i in range(0, len(objects)):
                obj_tuple = objects[i]

                obj = obj_tuple[0]
                lifecycle_state = obj_tuple[1]
                audit_change_type = obj_tuple[2]
                preceding_version_uid = obj_tuple[3]
                description = obj_tuple[4]
                local_versioned_object = obj_tuple[5]

                local_versioned_object_list.append(local_versioned_object)

                oe_type = self._str_type_or_error(obj)

                # create an audit details, same as commit except change_type reflects changes to this object in particular
                obj_audit = UpdateAudit(
                    change_type=audit_change_type.value,
                    committer=committer,
                    terminology_service=self._ts,
                    description=(description if description is not None else commit_description)
                )

                if audit_change_type == AuditChangeType.CREATION:
                    # create a new version
                    if preceding_version_uid is not None:
                        raise ValueError(f"Aborting commit. objects[{str(i)}] had change type of CREATION but a preceding_version_uid was given")

                    # create a version to add to the commit
                    created_version = UpdateVersion(
                        commit_audit=obj_audit,
                        lifecycle_state=lifecycle_state.value,
                        terminology_service=self._ts,
                        data=obj
                    )

                    versions.append(created_version)
                    preceding_version_uids.append(None)
                    oe_types.append(f"VERSION<{oe_type}>")
                    
                    self._log.info(f"Added creation of VERSION<{oe_type}> to commit")
                else:
                    if preceding_version_uid is None:
                        raise ValueError(f"Aborting commit. objects[{str(i)}] was lacking a preceding_version_uid but was not marked as change type CREATION")
                    
                    # otherwise prepare a version for an update
                    update_version = UpdateVersion(
                        commit_audit=obj_audit,
                        lifecycle_state=lifecycle_state.value,
                        terminology_service=self._ts,
                        preceding_version_uid=preceding_version_uid,
                        data=obj
                    )

                    versions.append(update_version)
                    preceding_version_uids.append(preceding_version_uid)
                    oe_types.append(f"VERSION<{oe_type}>")

                    self._log.info(f"Added update of VERSION<{oe_type}> to commit")

            # now commit
            self._log.info(f"Committing a CONTRIBUTION of {len(versions)} items to the server")
            cont_resp = demo_client.contribution.commit_contribution_set(versions, commit_audit)
            contrib : Contribution = cont_resp.pyehr_obj

            ovid_list = []

            self._log.info(f"CONTRIBUTION (uid=\'{contrib.uid.value}\') committed on server with {len(contrib.versions)} items")

            # write to local versions
            if len(contrib.versions) != len(local_versioned_object_list):
                self._log.warning(f"Contribution returned by server contained less versions than in request ({len(contrib.versions)} in response versus {len(local_versioned_object_list)} in request)")
            else:
                # update local objects - assumes remote server returns in the same order requested...
                self._log.info("Updating local VERSIONED_OBJECTs. Assuming server returned versions in same order as client.")
                for i in range(len(local_versioned_object_list)):
                    local_vo : VersionedObject = local_versioned_object_list[i]
                    if local_vo is None:
                        continue
                    else:
                        version : UpdateVersion = versions[i]
                        ver_ref = contrib.versions[i]
                        oe_type = oe_types[i]
                        if ver_ref.ref_type != oe_type:
                            self._log.warning(f"Mismatch for item {str(i)} between request ({oe_type}) and response ({ver_ref.ref_type})")
                        ovid_list.append(ObjectVersionID(ver_ref.id.value))
                        local_vo.commit_original_version(
                            a_contribution=ObjectRef("local", "CONTRIBUTION", contrib.uid),
                            a_new_version_uid=ver_ref.id,
                            a_preceding_version_id=version._inner_original_version.preceding_version_uid_var,
                            an_audit=contrib.audit,
                            a_lifecycle_state=version._inner_original_version.lifecycle_state_var,
                            a_data=version._inner_original_version.data_var,
                            terminology_service=self._ts
                        )
            
            return (ovid_list, contrib, local_versioned_object_list)

        elif all_ehr_type:
            # ehr
            raise NotImplementedError("Cannot commit objects relating to EHR types as the client does not yet support this")

    def attest(self,
            obj_type: str,
            obj_version_id: ObjectVersionID,
            attester: PartyProxy,
            reason: DVText,
            is_pending: bool,
            description: Optional[DVText] = None,
            attested_view: Optional[DVMultimedia] = None,
            local_versioned_object: Optional[VersionedObject] = None) -> Optional[VersionedObject]:
        """Updates a given version to note that a clinician has explicitly attested the given content.
        
        Updates an existing object with a new trunk version to add the attestation and creates a new `REVISION_HISTORY_ITEM`"""
        # TODO: see if there is something clever that can be done with commits
        raise NotImplementedError("Cannot attest objects using client, as OpenEHR API does not support this.")

    def read(self,
            obj_type: str,
            obj_id: HierObjectID,
            version_at_time: Optional[DVDateTime] = None) -> Optional[Version]:
        """Retrieves the latest version of the object of the given type, or the version extant at `version_at_time` if this is provided."""
        
        if obj_type in DEMOGRAPHIC_CLIENT_TYPE:
            demo_client = OpenEHRDemographicRestClient(self.base_url)
            dt = None if version_at_time is None else ISODateTime(version_at_time.as_string())
            try:
                resp = demo_client.versioned_party.get_versioned_party_version_at_time(obj_id, dt)
                return resp.pyehr_obj
            except RuntimeError:
                return None
        else:
            raise NotImplementedError(f"Cannot read object of type `{obj_type}` as the client does not yet support this type")

    def read_version(self,
                    obj_type: str,
                    obj_version_id: ObjectVersionID) -> Version:
        """Retrieves a given version of the object of the given type."""
        if obj_type in DEMOGRAPHIC_CLIENT_TYPE:
            demo_client = OpenEHRDemographicRestClient(self.base_url)
            try:
                resp = demo_client.versioned_party.get_versioned_party_version_by_id(HierObjectID(obj_version_id.object_id().value), obj_version_id)
                return resp.pyehr_obj
            except RuntimeError:
                return None
        else:
            raise NotImplementedError(f"Cannot read object of type `{obj_type}` as the client does not yet support this type")

    def query_equal(self,
            obj_type: str,
            archetype_id: ArchetypeID,
            query_dict: dict[str, list[str]]) -> Version:
        """Retrieves a version of the object of the given type with parameters equal to those in query dict.
        
        :param query_dict: OpenEHR path for target attribute and list of possible values (e.g. {'details/items[at0002]/value/id': ['9449305552']})"""
        raise NotImplementedError("Cannot query for objects as QUERY API not supported")

    def retrieve_versioned_object(self, 
                                uid: HierObjectID,
                                is_demographic_type: bool = False,
                                metadata_only_versioned_object: bool = True) -> Optional[tuple[VersionedObject, RevisionHistory]]:
        """Retrieve a VERSIONED_OBJECT and its underlying REVISION_HISTORY."""
        if is_demographic_type:
            demo_client = OpenEHRDemographicRestClient(self.base_url)
            try:
                resp_vp = demo_client.versioned_party.get_versioned_party(uid)
                resp_rhi = demo_client.versioned_party.get_versioned_party_revision_history(uid)
                return (resp_vp.pyehr_obj, resp_rhi.pyehr_obj)
            except RuntimeError:
                return None