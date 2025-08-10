import pytest

from org.openehr.rm.data_types.text import CodePhrase
from org.openehr.base.base_types.identification import TerminologyID

def test_code_phrase_code_string_valid():
    term_id = TerminologyID("ICD10_1998(2019)")
    
    # should be OK
    code = CodePhrase(term_id, "A15", "Respiratory tuberculosis, bacteriologically and histologically confirmed")

    # not OK
    with pytest.raises(ValueError):
        code = CodePhrase(term_id, "", "Respiratory tuberculosis, bacteriologically and histologically confirmed")
        
    

    