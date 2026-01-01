"""Provides a client for interacting with any server implementing the openEHR 
REST APIs"""

import requests
from typing import Optional, Union

from pyehr.core.base.base_types.identification import HierObjectID
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus

from pyehr.core.its.json_tools import decode_json

class OpenEHRRestClient():
    """Procedural-style REST API client for openEHR servers. Supports API 
    version 1.0.3 only."""

    _base_url : str

    flag_allow_resolved_references: bool

    ehr: '_EHRClient'
    """Management of EHRs. Actions upon resources of this group are also formally 
    described in the I_EHR_SERVICE Abstract Service Model interface."""

    def _url_from_base(self, relative_path: str) -> str:
        """Turns a relative API URL (e.g. '/') into a full URL using the base"""
        return self._base_url + relative_path
    
    def _build_headers(self, extra_headers: Optional[object] = None) -> object:
        headers = {
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        if extra_headers is not None:
            for (k,v) in extra_headers:
                if k in headers:
                    raise ValueError(f"Cannot overwrite base header \'{k}\'")
                headers[k] = v
        return headers
    
    class _EHRClient:

        def __init__(self, outer: 'OpenEHRRestClient'):
            self.outer = outer

        def get_ehr_by_id(self, ehr_id: HierObjectID) -> Union[EHR, list[Union[EHR, EHRAccess, EHRStatus]]]:
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
            
            return decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)
        
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

            return decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)

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

            return decode_json(result.json(), target="EHR", flag_allow_resolved_references=self.outer.flag_allow_resolved_references)

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

