
from datetime import datetime, timedelta
from typing import Optional, Union
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.rm.data_types.text import CodePhrase
import requests as r

from pyehr.core.base.foundation_types.primitive_types import Uri


class FHIRTerminologyClient:
    """Client for working with remote FHIR terminology servers using
    CodeSystem, ValueSet, code, Coding, CodeableConcept but using pyehr
    OpenEHR based resources"""

    base_url: str
    system_mapping: dict

    _client_credentials_token_url: Optional[str]
    _client_credentials_body: Optional[dict]

    _client_credentials_token: Optional[str] = None
    _client_credentials_valid_until: Optional[datetime] = None

    def _get_client_creds_token(self):
        if self._client_credentials_token is not None:
            if self._client_credentials_valid_until < datetime.now():
                # old token still valid
                return self._client_credentials_token
        
        # in all other circumstances get a new token
        token_response = r.post(url=self._client_credentials_token_url, data=self._client_credentials_body)
        if token_response.status_code != 200:
            raise RuntimeError(f"Not possible to retrieve FHIR terminology server auth token: {bytes.decode(token_response.content)}")
        
        try:
            token_response_body = token_response.json()
            if "access_token" not in token_response_body:
                raise RuntimeError("Not possible to retrieve FHIR terminology server auth token: no 'access_token' found in response")
            
            self._client_credentials_token = token_response_body["access_token"]
            
            if "expires_in" in token_response_body:
                self._client_credentials_valid_until = datetime.now() + timedelta(seconds=(int(token_response_body["expires_in"]) - 30))
            
            return self._client_credentials_token
            
        except r.exceptions.JSONDecodeError as ex:
            raise RuntimeError(f"Expected JSON auth token but got: {bytes.decode(token_response.content)}")
        
    def _get_request_headers(self):
        headers = {}
        if self._client_credentials_token_url is not None:
            headers["Authorization"] = f"Bearer {self._get_client_creds_token()}"
        return headers
    
    def _get_system_url(self, term_id: TerminologyID):
        term_id_str = term_id.value
        if term_id_str in self.system_mapping:
            return self.system_mapping[term_id_str]
        else:
            raise RuntimeError(f"Provided TERMINOLOGY_ID \'{term_id_str}\' is not resolvable in this service (did you provide this in id_to_system_mapping?)")

    def _build_parameter_dict(self, fhir_parameters: Union[dict, list]):
        if "resourceType" not in fhir_parameters or fhir_parameters["resourceType"] != "Parameters":
            raise ValueError("Resource type of provided FHIR resource was not 'Parameters'")
    
        param_list = fhir_parameters["parameter"]
        param_dict = dict()

        for param in param_list:
            types = {"valueCode", "valueString", "valueBoolean", "valueUri", "valueCoding", "part"}
            param_name = param["name"]
            param_val = param
            for val_type in types:
                if val_type in param:
                    param_val = param[val_type]

            param_dict[param_name] = param_val
        
        return param_dict

    def __init__(self, 
                 base_url: str, 
                 id_to_system_mapping: dict[str, str],
                 client_creds_token_url: Optional[str] = None,
                 client_creds_client_id: Optional[str] = None, 
                 client_creds_client_secret: Optional[str] = None):
        """Initialise a client, with OAuth client credentials if needed.

        Provide all of the client_creds_xxx parameters if the server requires client_credentials authorisation.
        
        :param base_url: Base URL for FHIR terminology server (e.g. https://ontology.nhs.uk/production1/fhir)
        :param id_to_system_mapping: Mapping of openEHR TERMINOLOGY_ID.value statements to FHIR CodeSystem URLs"""
        self.base_url = base_url
        self.system_mapping = id_to_system_mapping
        if client_creds_token_url is None and (client_creds_client_id is not None or client_creds_client_secret is not None):
            raise ValueError("Must provide token_url to use client_credentials authorisation")
        if client_creds_token_url is not None and (client_creds_client_id is None or client_creds_client_secret is None):
            raise ValueError("Must provide client_id and client_secret to use client_credentials authorisation")
        if client_creds_token_url is not None:
            self._client_credentials_token_url = client_creds_token_url
            self._client_credentials_body = {
                        "grant_type": "client_credentials",
                        "client_id": client_creds_client_id,
                        "client_secret": client_creds_client_secret
            }

    def get_code(self,
                    terminology_id: TerminologyID,
                    code: str) -> Optional[CodePhrase]:
        """Return a CODE_PHRASE from terminology ID and code"""

        resp = r.get(
            url=f"{self.base_url}/CodeSystem/$lookup?system={self._get_system_url(terminology_id)}&code={code}",
            headers=self._get_request_headers()
        )

        resp_obj = resp.json()
        resp_dict = None
        if "resourceType" in resp_obj and resp_obj["resourceType"] == "Parameters":
            resp_dict = self._build_parameter_dict(resp_obj)
        else:
            return None

        return CodePhrase(terminology_id, resp_dict["code"], resp_dict.get("display"))
    
    def validate_code_phrase(self,
                      code_phrase: CodePhrase) -> Optional[bool]:
        """Returns whether a CODE_PHRASE is valid - i.e. whether the code in the phrase is within the terminology in the phrase"""
        system = self._get_system_url(code_phrase.terminology_id)

        resp = r.get(
            url=f"{self.base_url}/CodeSystem/$validate-code?url={system}&code={code_phrase.code_string}",
            headers=self._get_request_headers()
        )
        resp_obj = resp.json()
        if "resourceType" in resp_obj and resp_obj["resourceType"] == "Parameters":
            resp_dict = self._build_parameter_dict(resp_obj)
            return resp_dict["result"]
        else:
            return None

    def code_in_code_set(self, code_set_url: Uri, code_phrase: CodePhrase) -> Optional[bool]:
        """Returns whether a CODE_PHRASE is in a code set referenced by a given URL."""
        system = self._get_system_url(code_phrase.terminology_id)

        resp = r.get(
            url=f"{self.base_url}/ValueSet/$validate-code?code={code_phrase.code_string}&url={code_set_url}&system={system}",
            headers=self._get_request_headers()
        )
        resp_obj = resp.json()

        if "resourceType" in resp_obj and resp_obj["resourceType"] == "Parameters":
            resp_dict = self._build_parameter_dict(resp_obj)
            return resp_dict["result"]
        else:
            return None
        
    def get_code_set_from_url(self, system_term_id: TerminologyID, code_set_url: Uri, filter: Optional[str] = None, active_only: bool = True, limit: Optional[int] = None) -> list[CodePhrase]:
        """Returns a list of CODE_PHRASEs in a code set referenced by a given URL.
        
        :param filter: Provide a text filter to restrict the number of elements returned by the search
        :param active_only: Whether to only return codes marked as 'active' in the service
        :param limit: Return no more than 'limit' results"""
        system = self._get_system_url(system_term_id)

        url = f"{self.base_url}/ValueSet/$expand?url={code_set_url}&system={system}&activeOnly={str(active_only).lower()}"
        if filter is not None:
            url += f"&filter={filter}"
        if limit is not None:
            url += f"&count={str(limit)}"

        resp = r.get(
            url=url,
            headers=self._get_request_headers()
        )

        resp_obj = resp.json()
        code_phrase_list = []
        if "resourceType" in resp_obj and resp_obj["resourceType"] == "ValueSet":
            if "expansion" not in resp_obj or "contains" not in resp_obj["expansion"]:
                return []
            fhir_codings = resp_obj["expansion"]["contains"]
            for coding in fhir_codings:
                if "code" not in coding:
                    continue
                code_phrase_list.append(CodePhrase(system_term_id, coding["code"], coding.get("display")))
            return code_phrase_list
        else:
            return []


    def get_code_set_from_snomed_ecl(self, ecl_str: str, snomed_term_id : TerminologyID = TerminologyID("SNOMED-CT"), filter: Optional[str] = None, active_only: bool = True, limit: Optional[int] = None) -> list[CodePhrase]:
        """Returns a list of CODE_PHRASEs resulting from a SNOMED CT Expression Constraint Language (ECL) constraint.
        
        Assumes that the terminology server provided supports system of http://snomed.info/sct.
        
        Shorthand for get_code_set_from_url with url set to http://snomed.info/sct?fhir_vs=ecl/{ecl_str}"""

        return self.get_code_set_from_url(snomed_term_id, f"http://snomed.info/sct?fhir_vs=ecl/{ecl_str}", filter=filter, active_only=active_only, limit=limit)
        
    def get_code_set_from_snomed_search(self, search_term: str, limit: int = 20, active_only : bool = True, snomed_term_id : TerminologyID = TerminologyID("SNOMED-CT")):
        """Search the full SNOMED CT set of codes for a certain code (can be code or description).
        
        Shorthand for get_code_set_from_url with code_set_url set to http://snomed.info/sct?fhir_vs, and defaults applied."""
        return self.get_code_set_from_url(snomed_term_id, "http://snomed.info/sct?fhir_vs", filter=search_term, active_only=active_only, limit=limit)

    def code_in_snomed_ecl_set(self, ecl_str: str, code_phrase: CodePhrase) -> Optional[bool]:
        """Returns whether or not a given CodePhrase is covered by a SNOMED CT Expression Constraint Language (ECL) constraint.
        
        Assumes that the terminology server provided supports system of http://snomed.info/sct.
        
        Shorthand for code_in_code_set with url set to http://snomed.info/sct?fhir_vs=ecl/{ecl_str}"""

        return self.code_in_code_set(f"http://snomed.info/sct?fhir_vs=ecl/{ecl_str}", code_phrase)

