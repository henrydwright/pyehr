import json
from pyehr.client.exceptions import OpenEHRRestBadRequestError, OpenEHRRestObjectAlreadyExistsError, OpenEHRRestObjectNotFoundError, OpenEHRRestOperationError
from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.its.xml_tools import decode_xml
import requests

import xml.etree.ElementTree as ET
from typing import Optional
from pyehr.client import OpenEHRBaseRestClient, OpenEHRRestClientResponse
from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.time import ISODateTime

class OpenEHRRestTemplateDefinitionItem():
    """Represents metadata for a single ADL 1.4 operational template
    as returned by the 'List templates' Definition API operation"""

    template_id: str

    version: Optional[str]

    concept: str

    archetype_id: str

    created_timestamp: ISODateTime

    def __init__(self, template_id: str, concept: str, archetype_id: str, created_timestamp: ISODateTime, version: Optional[str] = None):
        self.template_id = template_id
        self.version = version
        self.concept = concept
        self.archetype_id = archetype_id
        self.created_timestamp = created_timestamp

    def as_json(self):
        draft = {
            "template_id": self.template_id,
            "concept": self.concept,
            "archetype_id": self.archetype_id,
            "created_timestamp": self.created_timestamp.as_string()
        }
        if self.version is not None:
            draft["version"] = self.version
        return draft

    def from_json(json_obj: dict) -> 'OpenEHRRestTemplateDefinitionItem':
        ver = None
        if "version" in json_obj:
            ver = json_obj["version"]
        
        return OpenEHRRestTemplateDefinitionItem(
            template_id=json_obj["template_id"],
            concept=json_obj["concept"],
            archetype_id=json_obj["archetype_id"],
            created_timestamp=ISODateTime(json_obj["created_timestamp"])
        )

class OpenEHRDefinitionRestClient(OpenEHRBaseRestClient):
    """Procedural-style REST API client for Definition API operations on openEHR servers. Supports API 
    version 1.0.3 only."""

    def __init__(self, base_url, flag_allow_resolved_references = True, raise_exceptions_on_failure: bool = True):
        super().__init__(base_url, flag_allow_resolved_references, raise_exceptions_on_failure)

    def adl14_list_templates(self) -> OpenEHRRestClientResponse[list[OpenEHRRestTemplateDefinitionItem]]:
        """List the available ADL 1.4 operational templates (OPT) on the system."""
        target_url = self._url_from_base("/definition/template/adl1.4")
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )

        if result.status_code != 200:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestOperationError(f"Received status code \'{result.status_code}\' when attempting operation", result.status_code, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        
        ret_list = []
        for item in result.json():
            ret_list.append(OpenEHRRestTemplateDefinitionItem.from_json(item))

        return OpenEHRRestClientResponse(ret_list, result, self._get_metadata_from_result(result))
    
    def adl14_get_template(self, template_id: str) -> OpenEHRRestClientResponse[OperationalTemplate]:
        """Retrieves the ADL 1.4 operational template (OPT) identified by template_id identifier."""
        target_url = self._url_from_base(f"/definition/template/adl1.4/{template_id}")
        result = requests.get(
            url=target_url,
            headers={"Accept": "application/xml","Prefer": "return=representation"}
        )

        if result.status_code == 400:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestBadRequestError("Request has invalid (incorrectly formatted) template_id", 400, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        elif result.status_code == 404:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestObjectNotFoundError("Template with specified template_id does not exist", 404, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        elif result.status_code == 406:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestOperationError("Service cannot produce response in 'application/json' format required by this client", 406, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        elif result.status_code != 200:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestOperationError(f"Received status code \'{result.status_code}\' when attempting operation", result.status_code, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        
        templ_str = bytes.decode(result.content)
        ret = decode_xml(templ_str, "TEMPLATE")
        return OpenEHRRestClientResponse(ret, result, self._get_metadata_from_result(result))
    
    def adl14_upload_template(self, opt: OperationalTemplate) -> OpenEHRRestClientResponse[OperationalTemplate]:
        """Upload a new ADL 1.4 operational template (OPT)."""
        target_url = self._url_from_base(f"/definition/template/adl1.4")
        opt_xml = opt.as_xml("template")
        opt_xml.attrib["xmlns"] = "http://schemas.openehr.org/v1"
        opt_str = ET.tostring(opt_xml)
        result = requests.post(
            url=target_url,
            headers={"Content-Type": "application/xml","Prefer": "return=representation"},
            data=opt_str
        )

        if result.status_code == 400:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestBadRequestError(f"Server could not parse template.", 400, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        elif result.status_code == 409:
            if self.raise_exceptions_on_failure:
                raise OpenEHRRestObjectAlreadyExistsError(f"Template with same template ID already exists", 409, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))
        elif result.status_code not in {200, 201}:
            if self.raise_exceptions_on_failure:
                raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation", result.status_code, result.text)
            return OpenEHRRestClientResponse(None, result, self._get_metadata_from_result(result))

        templ_str = bytes.decode(result.content)
        ret = decode_xml(templ_str, "TEMPLATE")
        return OpenEHRRestClientResponse(ret, result, self._get_metadata_from_result(result))
