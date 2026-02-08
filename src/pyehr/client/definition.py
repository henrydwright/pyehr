import json
import requests

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

    def __init__(self, base_url, flag_allow_resolved_references = True):
        super().__init__(base_url, flag_allow_resolved_references)

    def adl14_get_list_templates(self) -> OpenEHRRestClientResponse[list[OpenEHRRestTemplateDefinitionItem]]:
        """List the available ADL 1.4 operational templates (OPT) on the system."""
        target_url = self._url_from_base("/definition/template/adl1.4")
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )

        if result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        ret_list = []
        for item in result.json():
            ret_list.append(OpenEHRRestTemplateDefinitionItem.from_json(item))

        return OpenEHRRestClientResponse(ret_list, result, self._get_metadata_from_result(result))
    
    def adl14_get_template(self, template_id: str) -> str:
        """Retrieves the ADL 1.4 operational template (OPT) identified by template_id identifier."""
        target_url = self._url_from_base(f"/definition/template/adl1.4/{template_id}")
        result = requests.get(
            url=target_url,
            headers=self._build_headers()
        )

        if result.status_code == 400:
            raise ValueError("400 Bad Request: request has invalid (incorrectly formatted) template_id")
        elif result.status_code == 404:
            raise RuntimeError("404 Not Found: template with specified template_id does not exist")
        elif result.status_code == 406:
            raise RuntimeError("406 Not Acceptable: service cannot produce response in 'application/json' format required by this client")
        elif result.status_code != 200:
            raise RuntimeError(f"Received status code \'{result.status_code}\' when attempting operation")
        
        return bytes.decode(result.content)