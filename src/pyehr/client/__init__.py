"""Provides base functions and definitions needed to implement any REST API client
interacting with OpenEHR REST API compliant servers"""

from types import NoneType
from typing import Optional, Union

import requests

from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.generic import RevisionHistory

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

class OpenEHRBaseRestClient():

    _base_url : str

    flag_allow_resolved_references: bool

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

    def _get_XXX_by_version_id(self, target_url: str, target_type: str):
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code == 404:
            raise RuntimeError("404 Not Found: Either EHR with ehr_id does not exist, or given version_uid does not exist.")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        obj = decode_json(result.json(), target=target_type, flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))

    def _create_XXX(self, target_url: str, target_type: str, new_obj: AnyClass):
        result = requests.post(
            url=target_url,
            headers=self._build_headers(),
            json=new_obj.as_json()
        )
        if result.status_code == 400:
            raise ValueError(f"400 Bad Request: request had invalid content. Inner error {json.dumps(result.json(),indent=1)}")
        elif result.status_code == 404:
            raise RuntimeError(f"404 Not Found: EHR with given ehr_id does not exist")
        elif result.status_code == 422:
            raise ValueError(f"422 Unprocessable Entity: content could be converted to desired type but there are semantic validation errors (e.g. template not known or not validating supplied composition)")
        elif result.status_code != 201:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        obj = decode_json(result.json(), target_type=target_type, flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))

    def _update_XXX(self, target_url: str, target_type: str, preceding_version_uid: ObjectVersionID, new_obj: AnyClass) -> OpenEHRRestClientResponse:
        result = requests.put(
            url=target_url,
            headers=self._build_headers({
                "If-Match": preceding_version_uid.value
            }),
            json=new_obj.as_json()
        )
        if result.status_code == 400:
            raise ValueError(f"400 Bad Request: request had invalid content.")
        elif result.status_code == 404:
            raise RuntimeError(f"404 Not Found: Either EHR with given ehr_id does not exist or the object with UID trying to be updated does not exist")
        elif result.status_code == 412:
            raise RuntimeError(f"412 Precondition Failed: preceding_version_uid of {preceding_version_uid.value} did not match latest version on service side.")
        elif not (result.status_code == 200 or result.status_code == 204):
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        obj = decode_json(result.json(), target=target_type, flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))

    def _delete_XXX(self, target_url: str) -> OpenEHRRestClientResponse[NoneType]:
        result = requests.delete(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code == 400:
            raise ValueError("400 Bad Request: request could not be parsed or is invalid")
        elif result.status_code == 404:
            raise RuntimeError("404 Not Found: server could not find an object with given ID to delete")
        elif result.status_code == 409:
            raise RuntimeError("409 Conflict: the given ID was not for the latest version of the object, so could not be deleted.")
        elif result.status_code != 204:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))

    def _get_versioned_XXX(self, target_url: str, target_type: str) -> OpenEHRRestClientResponse:
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code == 404:
            raise RuntimeError(f"404 Not Found: Either EHR with given ehr_id does not exist or object with versioned_object_uid does not exist")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

        obj = decode_json(result.json(), target=target_type, flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))

    def _get_versioned_XXX_revision_history(self, target_url: str) -> OpenEHRRestClientResponse:
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code == 404:
            raise RuntimeError(f"404 Not Found: Either EHR with given ehr_id or object with given versioned_object_uid as not found")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")

        obj = None
        if isinstance(result.json(), list):
            # this is probably an EHRBase like return of just a list, still try to parse
            obj = RevisionHistory(items=[decode_json(item, target="REVISION_HISTORY_ITEM", flag_allow_resolved_references=self.flag_allow_resolved_references) for item in result.json()])
        else:
            obj = decode_json(result.json(), target="REVISION_HISTORY", flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))

    def _get_versioned_XXX_version_at_time(self, target_url: str, target_type: str, version_at_time: Optional[ISODateTime] = None) -> OpenEHRRestClientResponse:
        params = None
        if version_at_time is not None:
            params = {
                "version_at_time": version_at_time.as_string()
            }
        result = requests.get(
            url=target_url,
            headers=self._build_headers(),
            params=params
        )
        if result.status_code == 400:
            raise ValueError(f"400 Bad Request: request had invalid content.")
        elif result.status_code == 404:
            raise RuntimeError(f"404 Not Found: Either EHR with given ehr_id does not exist or no version of {target_type} existed at {version_at_time.as_string()}")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        if "_type" not in result.json():
            raise RuntimeError("Could not decode response as JSON had no '_type' attribute to disambiguate between ORIGINAL_VERSION and IMPORTED_VERSION")
        
        obj = None
        if result.json()["_type"] == "ORIGINAL_VERSION":
            obj = decode_json(result.json(), target="ORIGINAL_VERSION", flag_allow_resolved_references=self.flag_allow_resolved_references)
        elif result.json()["_type"] == "IMPORTED_VERSION":
            obj = decode_json(result.json(), target="IMPORTED_VERSION", flag_allow_resolved_references=self.flag_allow_resolved_references)
        else:
            raise RuntimeError(f"Could not decode response of type \'{result.json()["_type"]}\' - expected ORIGINAL_VERSION or IMPORTED_VERSION")
        
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))
    
    def _get_versioned_XXX_version_by_id(self, target_url: str, target_type: str) -> OpenEHRRestClientResponse:
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )
        if result.status_code == 404:
            raise RuntimeError(f"404 Not Found: Either EHR with ehr_id does not exist, or {target_type} with version_uid does not exist.")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        obj = decode_json(result.json(), target="ORIGINAL_VERSION", flag_allow_resolved_references=self.flag_allow_resolved_references)
        return OpenEHRRestClientResponse(obj, result, self._get_metadata_from_result(result))
    
    def _get_versioned_XXX_version_at_time_or_by_id(self, target_url: str, target_type: str, uid_based_id: Union[HierObjectID, ObjectVersionID], version_at_time: Optional[ISODateTime] = None):
        if isinstance(uid_based_id, ObjectVersionID):
            if version_at_time is not None:
                raise ValueError("If an OBJECT_VERSION_ID is provided, version_at_time should be None")
            return self._get_versioned_XXX_version_by_id(target_url, target_type)
        elif isinstance(uid_based_id, HierObjectID):
            return self._get_versioned_XXX_version_at_time(target_url, target_type, version_at_time)
        else:
            raise TypeError(f"Expected ObjectVersionID or HierObjectID, but {str(type(uid_based_id))} was given")

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
