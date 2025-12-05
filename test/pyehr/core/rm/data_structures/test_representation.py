import pytest

from pyehr.core.base.base_types.identification import TerminologyID, ArchetypeID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_structures.representation import Element, Cluster
from pyehr.core.rm.data_types.text import DVText, DVCodedText, CodePhrase
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers
from common import PythonTerminologyService, TERMINOLOGY_OPENEHR

OPENEHR_TID = TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR)

ts_ok = PythonTerminologyService(code_sets=[], terminologies=[TERMINOLOGY_OPENEHR])
ts_empty = PythonTerminologyService([], [])

postal_code = Element(DVText("postal code"),
            archetype_node_id="at0005",
            value=DVText("SW1A 1AA"))

addr_items = [
    Element(DVText("address line"),
            archetype_node_id="at0001",
            value=DVText("Buckingham Palace")),
    Element(DVText("city/town"),
            archetype_node_id="at0002",
            value=DVText("London")),
    postal_code,
    Element(DVText("type"),
            archetype_node_id="at0010",
            value=DVCodedText("Physical", CodePhrase(TerminologyID("local"), "at0011")))
]

c = Cluster(DVText("address"),
            archetype_node_id="openEHR-EHR-CLUSTER.address.v1",
            archetype_details=Archetyped(
                archetype_id=ArchetypeID("openEHR-EHR-CLUSTER.address.v1"),
                rm_version="1.1.0"
            ),
            items=addr_items)

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

def test_cluster_items_at_path():
    assert is_equal_value(c.items_at_path("items"), addr_items) == True
    with pytest.raises(ValueError):
        c.items_at_path("items[at0005]")
    with pytest.raises(ValueError):
        c.items_at_path("folders")

def test_cluster_item_at_path():
    assert c.item_at_path("").is_equal(c)
    assert c.item_at_path("items[at0005]").is_equal(postal_code)
    assert c.item_at_path("items[at0005]/value").is_equal(DVText("SW1A 1AA"))
    with pytest.raises(ValueError):
        c.item_at_path("folders[at0005]")
    with pytest.raises(ValueError):
        c.item_at_path("items")
    with pytest.raises(ValueError):
        c.item_at_path("items[at0100]")

def test_cluster_path_unique():
    assert c.path_unique("") == True
    assert c.path_unique("items") == False
    assert c.path_unique("items[at0001]") == True

def test_cluster_path_exists():
    assert c.path_exists("") == True
    assert c.path_exists("items") == True
    assert c.path_exists("items[at0001]") == True
    assert c.path_exists("items[at0001]/value") == True
    assert c.path_exists("folders") == False
    assert c.path_exists("items[at0004]") == False

def test_element_in_cluster_path_of_item():
    assert postal_code.path_of_item() == "/items[at0005]"
    e = Element(DVText("element"), archetype_node_id="at0003", value=DVText("Hello, world!"))
    deep_c = Cluster(DVText("test cluster"), 
                     archetype_node_id="pyehr-EHR-CLUSTER.path_of_item_test.v0",
                     archetype_details=Archetyped(ArchetypeID("pyehr-EHR-CLUSTER.path_of_item_test.v0"), rm_version="1.1.0"),
                     items=[Cluster(DVText("level1"), archetype_node_id="at0001", items=[Cluster(DVText("level2"), archetype_node_id="at0002", items=[e])])]
                     )
    assert e.path_of_item() == "/items[at0001]/items[at0002]/items[at0003]"

def test_element_in_cluster_parent():
    assert postal_code.parent().is_equal(c)