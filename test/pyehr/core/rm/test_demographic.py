import pytest

from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_structures.item_structure import ItemTree
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.demographic import PartyIdentity

def test_party_identity_purpose_valid():
    pur = DVCodedText(
            value="Official",
            defining_code=CodePhrase(
                terminology_id=TerminologyID("FHIR-R4-name-use"),
                code_string="official"
            )
        )
    pi = PartyIdentity(
        purpose=pur,
        archetype_node_id="at0002",
        details=ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0003",
            items=[]
        )
    )
    assert pi.purpose().is_equal(pur)

def test_party_identity_item_at_path():
    pur = DVCodedText(
        value="Official",
        defining_code=CodePhrase(
            terminology_id=TerminologyID("FHIR-R4-name-use"),
            code_string="official"
        )
    )
    det = ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0003",
            items=[]
        )
    pi = PartyIdentity(
        purpose=pur,
        archetype_node_id="at0002",
        details=det
    )
    assert is_equal_value(pi.item_at_path("details"), det)
    assert is_equal_value(pi.item_at_path(""), pi)