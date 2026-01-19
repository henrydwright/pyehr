"""Provides a client for interacting with any server implementing the openEHR 
REST APIs"""

import json
import requests
from typing import Optional, Union

from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus, VersionedEHRStatus

from pyehr.core.its.json_tools import decode_json

class OpenEHRRestOperationMetadata():
    """Class representing metadata that may be returned on executing an 
    OpenEHRRestClient operation (e.g. `Location` and `ETag`)."""

    location: Optional[str]
    """Services MUST return this header whenever a create or update operation was 
    performed, but it MAY return this header on other operation or action."""

    openEHR_uri: Optional[str]
    """If services have support to generate resource URL as specified by the 
    DV_URI/DV_EHR_URI format, then they MAY send also openEHR-uri response header."""

    etag: Optional[str]
    """The ETag response HTTP header contains a string token that the server 
    associates with a resource in order to uniquely identify the state of that 
    resource over its lifetime. The value of the token changes as soon as the 
    resource changes.
    
    Servers MAY choose their own format for this header, but the recommended 
    value is the unique identifier of the requested resource 
    (e.g. VERSIONED_OBJECT.uid.value, VERSION.uid.value, EHR.ehr_id.value, etc)."""

    last_modified: Optional[str]
    """Contains the datetime of the last modification of targeted resource 
    which should be taken from VERSION.commit_audit.time_committed.value."""

    def __init__(self, location: Optional[str] = None, openEHR_uri: Optional[str] = None, etag: Optional[str] = None, last_modified: Optional[str] = None):
        self.location = location
        self.openEHR_uri = openEHR_uri
        self.etag = etag
        self.last_modified = last_modified

    def as_dict(self):
        return {
            "location": self.location,
            "openEHR_uri": self.openEHR_uri,
            "etag": self.etag,
            "last_modified": self.last_modified
        }

class OpenEHRRestClientResponse[T]():
    """Response returned by OpenEHR client operations containing pyehr object,
    response metadata and inner response (from requests.Response)"""

    pyehr_obj: Optional[T]
    """pyehr object representation of the response to the request"""

    inner_response: requests.Response
    """requests.Response that generated this client response"""

    metadata: OpenEHRRestOperationMetadata
    """Metadata returned by the server on executing the request (e.g. ETag, Location, etc.)"""

    def __init__(self, pyehr_obj: Optional[T], inner_response: requests.Response, metadata: OpenEHRRestOperationMetadata):
        self.pyehr_obj = pyehr_obj
        self.inner_response = inner_response
        self.metadata = metadata

class OpenEHRRestClient():
    """Procedural-style REST API client for openEHR servers. Supports API 
    version 1.0.3 only."""

    _base_url : str

    flag_allow_resolved_references: bool

    ehr: '_EHRClient'
    """Management of EHRs."""

    ehr_status: '_EHRStatusClient'
    """Management of EHR_STATUS and VERSIONED_EHR_STATUS resources."""

    def _url_from_base(self, relative_path: str) -> str:
        """Turns a relative API URL (e.g. '/') into a full URL using the base"""
        return self._base_url + relative_path
    
    def _build_headers(self, extra_headers: Optional[dict] = None) -> object:
        headers = {
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        if extra_headers is not None:
            for (k,v) in extra_headers.items():
                if k in headers:
                    raise ValueError(f"Cannot overwrite base header \'{k}\'")
                headers[k] = v
        return headers
    
    def _get_metadata_from_result(self, result: requests.Response):
        location = None
        openEHR_uri = None
        etag = None
        last_modified = None
        if "Location" in result.headers:
            location = result.headers["Location"]
        if "openEHR-uri" in result.headers:
            openEHR_uri = result.headers["openEHR-uri"]
        if "ETag" in result.headers:
            etag = result.headers["ETag"]
        if "Last-Modified" in result.headers:
            last_modified = result.headers["Last-Modified"]
        return OpenEHRRestOperationMetadata(location=location, openEHR_uri=openEHR_uri, etag=etag, last_modified=last_modified)

    
    class _EHRClient:

        def __init__(self, outer: 'OpenEHRRestClient'):
            self.outer = outer

        def get_ehr_by_id(self, ehr_id: HierObjectID) -> OpenEHRRestClientResponse[Union[EHR, list[Union[EHR, EHRAccess, EHRStatus]]]]:
            """
            Retrieve the EHR with the specified `ehr_id`.

            Executes: `GET` on `/ehr/{ehr_id}`
            
            :param ehr_id: EHR identifier taken from EHR.ehr_id.value. Example: `7d44b88c-4199-4bad-97dc-d78268e01398`.
            """
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}")
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers()
            )
            if result.status_code == 404:
                raise RuntimeError("404 Not Found: EHR with supplied subject parameters does not exist.")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
            
            obj = decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def get_ehr_by_subject_id(self, subject_id: str, subject_namespace: str) -> Union[EHR, list[Union[EHR, EHRAccess, EHRStatus]]]:
            """Retrieve the EHR with the specified subject_id and subject_namespace.

            These subject parameters will be matched against EHR's EHR_STATUS.subject.external_ref.id.value and EHR_STATUS.subject.external_ref.namespace values.
            
            Executes: `GET` on /ehr
            
            :param subject_id: The EHR subject id. Example: `ins01`
            :param subject_namespace: The EHR subject id namespace. Example: `examples`"""
            target_url = self.outer._url_from_base("/ehr")
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers(),
                params={
                    "subject_id": subject_id,
                    "subject_namespace": subject_namespace
                }
            )
            if result.status_code == 404:
                raise RuntimeError("404 Not Found: EHR with supplied subject parameters does not exist.")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

            obj = decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))

        def create_ehr(self, ehr_status: Optional[EHRStatus] = None) -> Union[EHR, list[Union[EHR, EHRAccess, EHRStatus]]]:
            """Create a new EHR with an auto-generated identifier.

            An EHR_STATUS resource needs to be always created and committed in the new EHR. This resource MAY be also supplied by the client as the request body. If not supplied, a default EHR_STATUS will be used by the service with following attributes:

            * is_queryable: true
            * is_modifiable: true
            * subject: a PARTY_SELF object

            All other required EHR attributes and resources will be automatically created as needed by the EHR creation semantics.
            
            Executes: `POST` on `/ehr`"""
            target_url = self.outer._url_from_base("/ehr")
            request_body = None
            if ehr_status is not None:
                request_body = ehr_status.as_json()
            result = requests.post(
                url=target_url,
                headers=self.outer._build_headers(),
                json=request_body
            )
            if result.status_code == 400:
                raise ValueError(f"400 Bad Request: Server did not accept provided ehr_status. Body: {str(result.content)}")
            elif result.status_code == 409:
                raise RuntimeError("409 Conflict: Unable to create a new EHR due to a conflict with an already existing EHR with the same subject id, namespace pair, whenever EHR_STATUS is supplied.")
            elif result.status_code != 201:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

            obj = decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def create_ehr_with_id(self, ehr_id: HierObjectID, ehr_status: Optional[EHRStatus] = None):
            """Create a new EHR with the specified ehr_id identifier.

            The value of the ehr_id unique identifier MUST be valid HIER_OBJECT_ID value. It is strongly RECOMMENDED that an UUID always be used for this.

            An EHR_STATUS resource needs to be always created and committed in the new EHR. This resource MAY be also supplied by the client as the request body. If not supplied, a default EHR_STATUS will be used by the service with following attributes:

            * is_queryable: true
            * is_modifiable: true
            * subject: a PARTY_SELF object
            
            All other required EHR attributes and resources will be automatically created as needed by the EHR creation semantics.
            
            Executes: `PUT` on `/ehr/{ehr_id}`

            :param ehr_id: EHR identifier taken from EHR.ehr_id.value. Example: `7d44b88c-4199-4bad-97dc-d78268e01398`
            """
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}")
            request_body = None
            if ehr_status is not None:
                request_body = ehr_status.as_json()
            result = requests.put(
                url=target_url,
                headers=self.outer._build_headers(),
                json=request_body
            )
            if result.status_code == 400:
                raise ValueError(f"400 Bad Request: Server did not accept provided ehr_status. Body: {str(result.content)}")
            elif result.status_code == 409:
                raise RuntimeError("409 Conflict: Unable to create a new EHR due to a conflict with an already existing EHR with the same ehr_id or subject id, namespace pair, whenever EHR_STATUS is supplied.")
            elif result.status_code != 201:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
            
            obj = decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))

    class _EHRStatusClient:

        def __init__(self, outer: 'OpenEHRRestClient'):
            self.outer = outer

        def get_ehr_status_by_version_id(self, ehr_id : HierObjectID, version_uid : ObjectVersionID) -> Optional[EHRStatus]:
            """Retrieves a particular version of the EHR_STATUS identified by `version_uid` and associated with 
            the EHR identified by `ehr_id`.

            Executes: `GET` on /ehr/{ehr_id}/ehr_status/{version_uid}
            
            :param ehr_id: EHR identifier taken from EHR.ehr_id.value.
            :param version_uid: VERSION identifier taken from VERSION.uid.value."""
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}/ehr_status/{version_uid.value}")
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers()
            )
            if result.status_code == 404:
                raise RuntimeError("404 Not Found: Either EHR with ehr_id does not exist, or given version_uid does not exist.")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
            
            obj = decode_json(result.json(), target="EHR_STATUS", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def get_ehr_status_at_time(self, ehr_id: HierObjectID, version_at_time: Optional[ISODateTime] = None):
            """Retrieves a version of the EHR_STATUS associated with the EHR identified by ehr_id.

            If version_at_time is supplied, retrieves the version extant at specified time, otherwise retrieves 
            the latest EHR_STATUS version.
            
            Executes: `GET` on /ehr/{ehr_id}/ehr_status

            :param ehr_id: EHR identifier taken from EHR.ehr_id.value.
            :param version_at_time: A given time in the extended ISO 8601 format."""
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}/ehr_status")
            params = None
            if version_at_time is not None:
                params = {
                    "version_at_time": version_at_time.as_string()
                }
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers(),
                params=params
            )
            if result.status_code == 400:
                raise ValueError(f"400 Bad Request: request had invalid content.")
            elif result.status_code == 404:
                raise RuntimeError(f"404 Not Found: Either EHR with ehr_id {ehr_id.value} does not exist or no version of EHR_STATUS existed at {version_at_time.as_string()}")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
            
            obj = decode_json(result.json(), target="EHR_STATUS", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def update_ehr_status(self, ehr_id: HierObjectID, preceding_version_uid: ObjectVersionID, new_ehr_status: EHRStatus):
            """Updates EHR_STATUS associated with the EHR identified by ehr_id. Performs client-side check for ID consistency
            before executing (i.e. checks new_ehr_status.uid and preceding_version_uid are consistent)
            
            Executes: `PUT` on /ehr/{ehr_id}/ehr_status

            :param ehr_id: EHR identifier taken from EHR.ehr_id.value
            :param preceding_version_uid: Used to prevent simultaneous operations. Update only performed if latest version ID matches this ID.
            :param new_ehr_status: New EHR_STATUS to replace existing EHR_STATUS with"""
            if new_ehr_status.uid is not None and preceding_version_uid.object_id().value != new_ehr_status.uid.value:
                raise ValueError("Mismatch between preceding_version_uid object ID and new_ehr_status UID field.")
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}/ehr_status")
            result = requests.put(
                url=target_url,
                headers=self.outer._build_headers({
                    "If-Match": preceding_version_uid.value
                }),
                json=new_ehr_status.as_json()
            )
            if result.status_code == 400:
                raise ValueError(f"400 Bad Request: request had invalid content.")
            elif result.status_code == 404:
                raise RuntimeError(f"404 Not Found: EHR with ehr_id {ehr_id.value} does not exist")
            elif result.status_code == 412:
                raise RuntimeError(f"412 Precondition Failed: preceding_version_uid of {preceding_version_uid.value} did not match latest version on service side.")
            elif not (result.status_code == 200 or result.status_code == 204):
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
            
            obj = decode_json(result.json(), target="EHR_STATUS", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))

        def get_versioned_ehr_status(self, ehr_id: HierObjectID) -> OpenEHRRestClientResponse[VersionedEHRStatus]:
            """Retrieves a VERSIONED_EHR_STATUS (metadata only) associated with an EHR identified by ehr_id.
            
            :param ehr_id: EHR identifier taken from EHR.ehr_id.value."""
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}/versioned_ehr_status")
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers()
            )
            if result.status_code == 404:
                raise RuntimeError(f"404 Not Found: EHR with ehr_id {ehr_id.value} does not exist")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

            obj = decode_json(result.json(), target="VERSIONED_EHR_STATUS", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))
        
        def get_versioned_ehr_status_revision_history(self, ehr_id: HierObjectID) -> OpenEHRRestClientResponse[RevisionHistory]:
            """Retrieves revision history of the VERSIONED_EHR_STATUS associated with the EHR identified by ehr_id.
            
            :param ehr_id: EHR identifier taken from EHR.ehr_id.value."""
            target_url = self.outer._url_from_base(f"/ehr/{ehr_id.value}/versioned_ehr_status/revision_history")
            result = requests.get(
                url=target_url,
                headers=self.outer._build_headers()
            )
            if result.status_code == 404:
                raise RuntimeError(f"404 Not Found: EHR with ehr_id {ehr_id.value} does not exist")
            elif result.status_code != 200:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

            obj = None
            if isinstance(result.json(), list):
                # this is probably an EHRBase like return of just a list, still try to parse
                obj = RevisionHistory(items=[decode_json(item, target="REVISION_HISTORY_ITEM", flag_allow_resolved_references=self.outer.flag_allow_resolved_references) for item in result.json()])
            else:
                obj = decode_json(result.json(), target="REVISION_HISTORY", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
            return OpenEHRRestClientResponse(obj, result, self.outer._get_metadata_from_result(result))

    def __init__(self, base_url: Uri, flag_allow_resolved_references : bool = True):
        """
        Initialise a new client for communicating with a particular server.
        
        :param base_url: Base URL for the target server, without the trailing slash,
                          but possibly with version included (e.g. `https://ehr.example.net/v1`)
        :param flag_allow_resolved_references: (default=True) Some servers (e.g. ehrBase) either allow
                                               or default to returning objects with OBJECT_REFs resolved
                                               to the referenced objects. When this is set to True
                                               this is permitted by the client despite not matching
                                               the default REST API specification. This will often
                                               cause the client to return a list of several pyehr.core
                                               objects with resolved references replaced with OBJECT_REFs 
                                               of scheme 'pyehr_decode_json' + GENERIC_IDs with scheme 'list_index'
                                               to match the RM.
        """
        self._base_url = base_url
        self.flag_allow_resolved_references = flag_allow_resolved_references
        self.ehr = self._EHRClient(self)
        self.ehr_status = self._EHRStatusClient(self)

    def options(self) -> object:
        """Get system options and conformance information.
        
        Services SHOULD respond to this method with at least appropriate HTTP 
        codes, headers and potentially with a payload revealing more details 
        about themselves.
        
        Executes: `OPTIONS` on `/`"""
        target_url = self._url_from_base("/")
        result = requests.options(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        return result.json()

