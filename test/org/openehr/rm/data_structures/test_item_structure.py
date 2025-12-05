import pytest

from org.openehr.base.base_types.identification import ArchetypeID, TerminologyID
from org.openehr.rm.common.archetyped import Archetyped
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.rm.data_types.text import DVText, DVCodedText, CodePhrase
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_structures.representation import Element, Cluster
from org.openehr.rm.data_structures.item_structure import ItemSingle, ItemList


t = DVDateTime("2025-11-25T23:28:00Z")
t2 = DVDateTime("2025-12-05T20:25:04Z")

es = Element(DVText("admission time"), 
            "at0001",
            value=t)

e = Element(DVText("admission time"), 
            "at0001",
            value=t)

e2 = Element(DVText("discharge time"),
             "at0002",
             value=t2)

e3 = Element(DVText("admission reason"),
             "at0003",
             value=DVCodedText("Assault", defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "52684005", "Assault (event)")))

its = ItemSingle(DVText("admission time container"),
                "pyehr-EHR-ITEM_SINGLE-admission_time.v0",
                item=es,
                archetype_details=Archetyped(ArchetypeID("pyehr-EHR-ITEM_SINGLE.admission_time.v0"), "1.1.0"))

itl = ItemList(DVText("admission metadata"), 
               archetype_node_id="pyehr-EHR-ITEM_LIST.admission.v0",
               items=[e, e2, e3],
               archetype_details=Archetyped(ArchetypeID("pyehr-EHR-ITEM_LIST.admission.v0"), "1.1.0"))

def test_item_single_as_hierarchy():
    assert its.as_hierarchy().is_equal(e)

def test_item_single_item_at_path():
    assert its.item_at_path("").is_equal(its)
    assert its.item_at_path("item").is_equal(e)
    assert its.item_at_path("item/value").is_equal(t)

def test_item_single_items_at_path():
    with pytest.raises(ValueError):
        its.items_at_path("")

def test_item_single_path_unique():
    assert its.path_unique("") == True
    assert its.path_unique("item") == True
    assert its.path_unique("item/value") == True

def test_item_single_path_exists():
    assert its.path_exists("item") == True
    assert its.path_exists("items") == False
    assert its.path_exists("item/val") == False
    assert its.path_exists("") == True

def test_element_in_item_single_path_of_item():
    assert es.path_of_item() == "/item"

def test_item_list_as_hierarchy():
    ash = itl.as_hierarchy()
    assert isinstance(ash, Cluster)
    assert is_equal_value(ash.items, [e, e2, e3])

def test_item_list_item_at_path():
    assert itl.item_at_path("").is_equal(itl)
    assert itl.item_at_path("items[at0002]").is_equal(e2)
    assert itl.item_at_path("items[at0001]/value").is_equal(t)

def test_item_list_items_at_path():
    assert is_equal_value(itl.items_at_path("items"), [e, e2, e3])
    with pytest.raises(ValueError):
        itl.items_at_path("items[at0002]")
    with pytest.raises(ValueError):
        itl.items_at_path("")

def test_item_list_path_unique():
    assert itl.path_unique("") == True
    assert itl.path_unique("items[at0002]") == True
    assert itl.path_unique("items[at0001]/value") == True
    assert itl.path_unique("items") == False

def test_item_list_path_exists():
    assert itl.path_exists("") == True
    assert itl.path_exists("items[at0002]") == True
    assert itl.path_exists("items[at0001]/value") == True
    assert itl.path_exists("items") == True
    assert itl.path_exists("it") == False

def test_element_in_item_list_path_of_item():
    assert e2.path_of_item() == "/items[at0002]"


