import pytest

from org.openehr.base.base_types.identification import TerminologyID
from org.openehr.rm.data_structures.representation import Element
from org.openehr.rm.data_types.text import DVText, DVCodedText, CodePhrase
from org.openehr.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers
from common import PythonTerminologyService, TERMINOLOGY_OPENEHR

OPENEHR_TID = TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR)

ts_ok = PythonTerminologyService(code_sets=[], terminologies=[TERMINOLOGY_OPENEHR])
ts_empty = PythonTerminologyService([], [])

def test_element_null_flavour_valid():
    # OK (valid code provided)
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(OPENEHR_TID, "273")),
        terminology_service=ts_ok
    )
    # not OK (invalid code)
    with pytest.raises(ValueError):
        e = Element(
            name=DVText("test_element"),
            archetype_node_id="at0007",
            null_flavour=DVCodedText("abacus", CodePhrase(OPENEHR_TID, "2000")),
            terminology_service=ts_ok
        )

def test_element_is_null():
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(OPENEHR_TID, "273")),
        terminology_service=ts_ok
    )
    assert e.is_null() == True
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        value=DVText("Test value"),
        terminology_service=ts_ok
    )
    assert e.is_null() == False

def test_element_item_at_path():
    dv = DVText("Test value")
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(OPENEHR_TID, "273")),
        terminology_service=ts_ok
    )
    assert e.item_at_path("").is_equal(e)
    assert e.item_at_path("value") is None
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        value=dv,
        terminology_service=ts_ok
    )
    assert e.item_at_path("").is_equal(e)
    assert e.item_at_path("value").is_equal(dv)

def test_element_items_at_path():
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(OPENEHR_TID, "273")),
        terminology_service=ts_ok
    )
    with pytest.raises(ValueError):
        e.items_at_path("")
    with pytest.raises(ValueError):
        e.items_at_path("value")

def test_element_path_unique():
    e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(OPENEHR_TID, "273")),
        terminology_service=ts_ok
    )
    assert e.path_unique("") == True
    assert e.path_unique("value") == True