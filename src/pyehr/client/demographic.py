
from enum import StrEnum
import json
from types import NoneType
from typing import Optional, Union

import requests
from pyehr.client import OpenEHRBaseRestClient, OpenEHRRestClientResponse
from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.json_tools import decode_json
from pyehr.core.its.rest.additions import UpdateAudit, UpdateContribution, UpdateVersion
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, Version
from pyehr.core.rm.common.generic import AuditDetails, PartyProxy, RevisionHistory
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.demographic import Party, Person, VersionedParty
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState

class OpenEHRPartyType(StrEnum):
    """Enum for different subclasses of PARTY that may be interacted with on a demographic server"""
    AGENT = "AGENT"
    GROUP = "GROUP"
    ORGANISATION = "ORGANISATION"
    PERSON = "PERSON"
    ROLE = "ROLE"

class OpenEHRDemographicRestClient(OpenEHRBaseRestClient):
    """Procedural-style REST API client for DEMOGRAPHIC API operations on openEHR servers. Supports the development
    API build as of 2026-01-25 only. Does not support ITEM_TAGs."""

    party: '_PartyClient'
    """Management of the five PARTY classes (AGENT, GROUP, ORGANISATION, PERSON, ROLE)."""

    versioned_party: '_VersionedPartyClient'
    """Management of the VERSIONED_PARTY class."""

    contribution: '_ContributionClient'
    """Creation of objects using OpenEHR native CONTRIBUTION and retrieval of CONTRIBUTIONs from elsewhere"""

    class _PartyClient():

        def __init__(self, outer: 'OpenEHRDemographicRestClient'):
            self.outer = outer

        def create_party(self, 
                         party_type: OpenEHRPartyType, 
                         new_party: Party,
                         version_lifecycle_state: Optional[VersionLifecycleState] = None,
                         version_audit_description: Optional[str] = None,
                         version_committer: Optional[PartyProxy] = None) -> OpenEHRRestClientResponse[Party]:
            """Creates the first version of a new PARTY.
            
            :param party_type: Which type of PARTY is being created
            :param new_party: New AGENT, GROUP, ORGANISATION, PERSON or ROLE to be created"""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}")
            return self.outer._create_XXX(target_url, party_type.value, new_party, version_lifecycle_state, version_audit_description, version_committer)
        
        def get_party(self, party_type: OpenEHRPartyType, uid_based_id: Union[HierObjectID, ObjectVersionID], version_at_time : Optional[ISODateTime] = None):
            """Retrieves a version of the PARTY identified by uid_based_id.

            The uid_based_id can take a form of an OBJECT_VERSION_ID identifier taken 
            from VERSION.uid.value (i.e. a version_uid), or a form of a HIER_OBJECT_ID 
            identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid). 
            The former is used to retrieve a specific known version of the PARTY 
            (e.g. one identified by 8849182c-82ad-4088-a07f-48ead4180515::openEHRSys.example.com::1), 
            whereas the latter (e.g. an identifier like 8849182c-82ad-4088-a07f-48ead4180515) 
            is be used to retrieve a version from the version container whenever the version_tree_id 
            is unknown or irrelevant (such as when most recent version is requested).

            When the uid_based_id has the form of a HIER_OBJECT_ID, if the 
            version_at_time is supplied, retrieves the version extant at specified time, 
            otherwise retrieves the latest PERSON version.
            
            :param uid_based_id: An abstract identifier, it can take a form of an 
                                 OBJECT_VERSION_ID identifier taken from VERSION.uid.value (i.e. a version_uid),
                                 or a form of a HIER_OBJECT_ID identifier taken from 
                                 VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).
            :param version_at_time: A given time in the extended ISO 8601 format. Can only be provided when
                                    uid_based_id is a HIER_OBJECT_ID"""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}/{uid_based_id.value}")
            return self.outer._get_XXX_by_version_id(target_url, party_type.value, version_at_time)

        def update_party(self, 
                         party_type: OpenEHRPartyType, 
                         uid_based_id: HierObjectID, 
                         preceding_version_uid: ObjectVersionID, 
                         new_party: Party,
                         version_lifecycle_state: Optional[VersionLifecycleState] = None,
                         version_audit_change_type: Optional[AuditChangeType] = None,
                         version_audit_description: Optional[str] = None,
                         version_committer: Optional[PartyProxy] = None) -> OpenEHRRestClientResponse[Party]:
            """Updates PARTY identified by uid_based_id.

            The uid_based_id can take only a form of an HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).

            If the request body already contains a PARTY.uid.value, it must match the uid_based_id in the URL.
            
            :param uid_based_id: An identifier in a form of a HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).
            :param preceding_version_uid: Version UID for the previous version that this update is based on
            :param new_party: The contents of the new PARTY to create the version for"""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}/{uid_based_id.value}")
            return self.outer._update_XXX(target_url, party_type.value, preceding_version_uid, new_party, version_lifecycle_state, version_audit_change_type, version_audit_description, version_committer)
        
        def delete_party(self, 
                         party_type: OpenEHRPartyType, 
                         uid_based_id: ObjectVersionID,
                         version_audit_description: Optional[str] = None,
                         version_committer: Optional[PartyProxy] = None) -> OpenEHRRestClientResponse[NoneType]:
            """Deletes the PARTY identified by uid_based_id.

            The uid_based_id MUST be in a form of an OBJECT_VERSION_ID identifier taken from the last (most recent) VERSION.uid.value, representing the preceding_version_uid to be deleted."""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}/{uid_based_id.value}")
            return self.outer._delete_XXX(target_url, version_audit_description=version_audit_description, version_committer=version_committer)

    class _VersionedPartyClient():

        def __init__(self, outer: 'OpenEHRDemographicRestClient'):
            self.outer = outer

        def get_versioned_party(self, versioned_object_uid: HierObjectID) -> OpenEHRRestClientResponse[VersionedParty]:
            """Retrieves a VERSIONED_PARTY identified by versioned_object_uid.

            Executes: `GET` on /demographic/versioned_party/{versioned_object_uid}
            
            :param versioned_object_uid: VERSIONED_PARTY identifier taken from VERSIONED_PARTY.uid.value."""

            target_url = self.outer._url_from_base(f"/demographic/versioned_party/{versioned_object_uid.value}")
            return self.outer._get_versioned_XXX(target_url, "VERSIONED_PARTY")
        
        def get_versioned_party_revision_history(self, versioned_object_uid: HierObjectID) -> OpenEHRRestClientResponse[RevisionHistory]:
            """Retrieves revision history of the VERSIONED_PARTY identified by versioned_object_uid.
            
            Executes: `GET` on /demographic/versioned_party/{versioned_object_uid}/revision_history
            
            :param versioned_object_uid: VERSIONED_PARTY identifier taken from VERSIONED_PARTY.uid.value."""
            
            target_url = self.outer._url_from_base(f"/demographic/versioned_party/{versioned_object_uid.value}/revision_history")
            return self.outer._get_versioned_XXX_revision_history(target_url)
        
        def get_versioned_party_version_at_time(self, versioned_object_uid: HierObjectID, version_at_time: Optional[ISODateTime] = None) -> OpenEHRRestClientResponse[Version[Party]]:
            """Retrieves a VERSION from the VERSIONED_PARTY identified by versioned_object_uid.

            If version_at_time is supplied, retrieves the VERSION extant at specified time, otherwise retrieves the latest VERSION.
            
            Executes: `GET` on /demographic/versioned_party/{versioned_object_uid}/version
            
            :param versioned_object_uid: VERSIONED_PARTY identifier taken from VERSIONED_PARTY.uid.value.
            :param version_at_time: A given time in the extended ISO 8601 format."""

            target_url = self.outer._url_from_base(f"/demographic/versioned_party/{versioned_object_uid.value}/version")
            return self.outer._get_versioned_XXX_version_at_time(target_url, "PARTY", version_at_time)
        
        def get_versioned_party_version_by_id(self, versioned_object_uid: HierObjectID, version_uid: ObjectVersionID) -> OpenEHRRestClientResponse[Version[Party]]:
            """Retrieves a VERSION identified by version_uid of a VERSIONED_PARTY identified by versioned_object_uid.
            
            Executes: `GET` on /demographic/versioned_party/{versioned_object_uid}/version/{version_uid}

            :param versioned_object_uid: VERSIONED_PARTY identifier taken from VERSIONED_PARTY.uid.value.
            :param version_uid: VERSION identifier taken from VERSION.uid.value."""
            target_url = self.outer._url_from_base(f"/demographic/versioned_party/{versioned_object_uid.value}/version/{version_uid.value}")
            return self.outer._get_versioned_XXX_version_by_id(target_url, "PARTY")

    class _ContributionClient():

        def __init__(self, outer: 'OpenEHRDemographicRestClient'):
            self.outer = outer

        def commit_contribution_set(self, versions: list[UpdateVersion], audit: UpdateAudit, uid: Optional[HierObjectID] = None) -> OpenEHRRestClientResponse[Contribution]:
            """Commit (in a database atomic operation) a set of versions to the server as a single CONTRIBUTION

            Note, the version.commit_audit.time_committed and version.commit_audit.system_id 
            will be ignored, not sent to the server, and replaced with server-generated content.
            
            :param versions: List of UPDATE_VERSIONs containing data to commit as part of the contribution
            :param audit: UPDATE_AUDIT containing the audit details to submit alongside the contribution
            :param uid: (Optional) HIER_OBJECT_ID for uid to use for the CONTRIBUTION. If omitted, the server will generate one"""
            target_url = self.outer._url_from_base(f"/demographic/contribution")

            update_contrib = UpdateContribution(
                versions=versions,
                audit=audit,
                uid=uid
            )

            result = requests.post(
                url=target_url,
                headers=self.outer._build_headers(),
                json=update_contrib.as_json()
            )

            if result.status_code == 400:
                raise ValueError(f"400 Bad Request: request had invalid content. Inner error {json.dumps(result.json(),indent=1)}")
            elif result.status_code == 409:
                raise RuntimeError("409 Conflict: the UID submitted was the same as an existing object in the database")
            elif result.status_code != 201:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation. Inner error {bytes.decode(result.content)}")
            
            obj = decode_json(result.json(), target="CONTRIBUTION", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def get_contribution_by_id(self, contribution_uid: HierObjectID):
            """Retrieves a CONTRIBUTION identified by `contribution_uid`"""
            target_url = self.outer._url_from_base(f"/demographic/contribution/{contribution_uid.value}")
            return self.outer._get_XXX_by_version_id(target_url, "CONTRIBUTION")

    def __init__(self, base_url, flag_allow_resolved_references = True):
        super().__init__(base_url, flag_allow_resolved_references)
        self.party = self._PartyClient(self)
        self.versioned_party = self._VersionedPartyClient(self)
        self.contribution = self._ContributionClient(self)