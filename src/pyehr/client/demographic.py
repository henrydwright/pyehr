
from types import NoneType
from typing import Optional, Union
from pyehr.client import OpenEHRBaseRestClient, OpenEHRRestClientResponse
from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.rm.demographic import Person


class OpenEHRDemographicRestClient(OpenEHRBaseRestClient):
    """Procedural-style REST API client for DEMOGRAPHIC API operations on openEHR servers. Supports the development
    API build as of 2026-01-25 only. Does not support ITEM_TAGs."""

    person: '_PersonClient'
    """Management of the PERSON class."""

    class _PersonClient():

        def __init__(self, outer: 'OpenEHRDemographicRestClient'):
            self.outer = outer

        def create_person(self, new_person: Person) -> OpenEHRRestClientResponse[Person]:
            """Creates the first version of a new PERSON.
            
            :param new_person: New PERSON to be created"""
            target_url = self.outer._url_from_base("/demographic/person")
            return self.outer._create_XXX(target_url, "PERSON", new_person)
        
        def get_person(self, uid_based_id: Union[HierObjectID, ObjectVersionID], version_at_time : Optional[ISODateTime] = None):
            """Retrieves a version of the PERSON identified by uid_based_id.

            The uid_based_id can take a form of an OBJECT_VERSION_ID identifier taken 
            from VERSION.uid.value (i.e. a version_uid), or a form of a HIER_OBJECT_ID 
            identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid). 
            The former is used to retrieve a specific known version of the PERSON 
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
            target_url = self.outer._url_from_base(f"/demographic/person/{uid_based_id.value}")
            return self.outer._get_XXX_by_version_id(target_url, "PERSON", version_at_time)

        def update_person(self, uid_based_id: HierObjectID, preceding_version_uid: ObjectVersionID, new_person: Person) -> OpenEHRRestClientResponse[Person]:
            """Updates PERSON identified by uid_based_id.

            The uid_based_id can take only a form of an HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).

            If the request body already contains a PERSON.uid.value, it must match the uid_based_id in the URL.
            
            :param uid_based_id: An identifier in a form of a HIER_OBJECT_ID identifier taken from VERSIONED_OBJECT.uid.value (i.e. a versioned_object_uid).
            :param preceding_version_uid: Version UID for the previous version that this update is based on
            :param new_person: The contents of the new PERSON to create the version for"""
            target_url = self.outer._url_from_base(f"/demographic/person/{uid_based_id.value}")
            return self.outer._update_XXX(target_url, "PERSON", preceding_version_uid, new_person)
        
        def delete_person(self, uid_based_id: ObjectVersionID) -> OpenEHRRestClientResponse[NoneType]:
            """Deletes the PERSON identified by uid_based_id.

            The uid_based_id MUST be in a form of an OBJECT_VERSION_ID identifier taken from the last (most recent) VERSION.uid.value, representing the preceding_version_uid to be deleted."""
            target_url = self.outer._url_from_base(f"/demographic/person/{uid_based_id.value}")
            return self.outer._delete_XXX(target_url)

    def __init__(self, base_url, flag_allow_resolved_references = True):
        super().__init__(base_url, flag_allow_resolved_references)
        self.person = self._PersonClient(self)