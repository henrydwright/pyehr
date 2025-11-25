import pytest

from org.openehr.base.base_types.identification import ArchetypeID
from org.openehr.rm.common.archetyped import Archetyped
from org.openehr.rm.data_types.text import DVText
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_structures.representation import Element
from org.openehr.rm.data_structures.item_structure import ItemSingle


t = DVDateTime("2025-11-25T23:28:00Z")

e = Element(DVText("admission time"), 
            "at0001",
            value=t)

its = ItemSingle(DVText("admission time container"),
                "pyehr-EHR-ITEM_SINGLE-admission_time.v0",
                archetype_details=Archetyped(ArchetypeID("pyehr-EHR-ITEM_SINGLE.admission_time.v0"), "1.1.0"),
                item=e)

def test_item_single_as_hierarchy():
    assert its.as_hierarchy().is_equal(e)

def test_item_single_item_at_path():
    assert its.item_at_path("").is_equal(its)
    assert its.item_at_path("item").is_equal(e)
    assert its.item_at_path("item/value").is_equal(t)

def test_item_single_items_at_path():
    with pytest.raises(ValueError):
        its.items_at_path("")

def test_element_in_item_single_path_of_item():
    assert e.path_of_item() == "/item"
