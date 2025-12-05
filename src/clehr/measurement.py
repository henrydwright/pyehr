from typing import Optional
import requests as r

from org.core.rm.support.measurement import MeasurementService

class NLMMeasurementService(MeasurementService):
    """Measurement service making use of the NLM ucum-service API"""
    
    _base_url : str

    def __init__(self, base_url: str = "https://ucum.nlm.nih.gov/ucum-service"):
        self._base_url = base_url

    def is_valid_units_string(self, units):
        units_response = r.get(f"{self._base_url}/v1/isValidUCUM/{units}")
        result = bytes.decode(units_response.content)
        return (result == "true")
    
    def units_equivalent(self, units1, units2):
        if not self.is_valid_units_string(units1):
            raise ValueError("units1 was not a valid UCUM units string")
        if not self.is_valid_units_string(units2):
            raise ValueError("units2 was not a valid UCUM units string")
        
        units1_response = r.get(
            url=f"{self._base_url}/v1/toBaseUnits/{units1}",
            headers={
                "Accept": "application/json"
            })
        if units1_response.status_code != 200:
            raise ValueError(f"Error converting units1 to base units. HTTP status code {units1_response.status_code}")
        
        units2_response = r.get(
            url=f"{self._base_url}/v1/toBaseUnits/{units2}",
            headers={
                "Accept": "application/json"
            })
        if units2_response.status_code != 200:
            raise ValueError(f"Error converting units2 to base units. HTTP status code {units2_response.status_code}")

        return (units1_response.json()['UCUMWebServiceResponse']['Response']['ResultBaseUnits'] == units2_response.json()['UCUMWebServiceResponse']['Response']['ResultBaseUnits'])