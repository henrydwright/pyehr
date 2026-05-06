
from pyehr.core.am.aom14.archetype.ontology import ArchetypeTerm

def test_archetype_term_keys():
    at = ArchetypeTerm("at0093", 
                       items={
                           "text": "01",
                           "description": "Cancelled for Clinical Reasons"
                           })
    
    atk = at.keys()
    assert atk[0] == "text"
    assert atk[1] == "description"
