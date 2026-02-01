
from enum import StrEnum
from types import NoneType
from typing import Optional, Union
from pyehr.client import OpenEHRBaseRestClient, OpenEHRRestClientResponse
from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.rm.common.change_control import Version
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.core.rm.demographic import Party, Person, VersionedParty

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

    class _PartyClient():

        def __init__(self, outer: 'OpenEHRDemographicRestClient'):
            self.outer = outer

        def create_party(self, party_type: OpenEHRPartyType, new_party: Person) -> OpenEHRRestClientResponse[Party]:
            """Creates the first version of a new PARTY.
            
            :param party_type: Which type of PARTY is being created
            :param new_party: New AGENT, GROUP, ORGANISATION, PERSON or ROLE to be created"""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}")
            return self.outer._create_XXX(target_url, party_type.value, new_party)
        
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

        def update_party(self, party_type: OpenEHRPartyType, uid_based_id: HierObjectID, preceding_version_uid: ObjectVersionID, new_party: Person) -> OpenEHRRestClientResponse[Person]:
            """Updates PARTY identified by uid_based_id.

            The uid_based_id can take only a form of an HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).

            If the request body already contains a PARTY.uid.value, it must match the uid_based_id in the URL.
            
            :param uid_based_id: An identifier in a form of a HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).
            :param preceding_version_uid: Version UID for the previous version that this update is based on
            :param new_party: The contents of the new PARTY to create the version for"""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}/{uid_based_id.value}")
            return self.outer._update_XXX(target_url, party_type.value, preceding_version_uid, new_party)
        
        def delete_party(self, party_type: OpenEHRPartyType, uid_based_id: ObjectVersionID) -> OpenEHRRestClientResponse[NoneType]:
            """Deletes the PARTY identified by uid_based_id.

            The uid_based_id MUST be in a form of an OBJECT_VERSION_ID identifier taken from the last (most recent) VERSION.uid.value, representing the preceding_version_uid to be deleted."""
            target_url = self.outer._url_from_base(f"/demographic/{party_type.value.lower()}/{uid_based_id.value}")
            return self.outer._delete_XXX(target_url)

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


    def __init__(self, base_url, flag_allow_resolved_references = True):
        super().__init__(base_url, flag_allow_resolved_references)
        self.party = self._PartyClient(self)
        self.versioned_party = self._VersionedPartyClient(self)