
from pyehr.core.am.aom14.archetype.ontology import ArchetypeTerm
from pyehr.core.its.adl14 import decode_adl14
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types.text import CodePhrase

def test_archetype_term_keys():
    at = ArchetypeTerm("at0093", 
                       items={
                           "text": "01",
                           "description": "Cancelled for Clinical Reasons"
                           })
    
    atk = at.keys()
    assert atk[0] == "text"
    assert atk[1] == "description"

def test_archetype_ontology_term_definitions_and_term_bindings():
    with open("test/pyehr/core/its/bloodPressure.adl14") as f:
        arch = decode_adl14(f.read())

    assert arch.ontology.term_definitions_for_code("at0000")["en"]["text"] == "Blood pressure"
    assert is_equal_value(arch.ontology.term_bindings_for_code("at0000"), {"SNOMED-CT": CodePhrase("SNOMED-CT(2003)", "364090009")})

