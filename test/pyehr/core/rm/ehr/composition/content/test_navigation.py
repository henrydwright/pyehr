import pytest

from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.ehr.composition.content.navigation import Section

ins = Section(
    name=DVText("inner"),
    archetype_node_id="at0012"
)

os = Section(
    name=DVText("outer"),
    archetype_node_id="at0011",
    items=[ins]
)

def test_section_items_valid():
    # NOT OK - empty list for items
    with pytest.raises(ValueError):
        Section(
            name=DVText("inner"),
            archetype_node_id="at0012",
            items=[]
        )

def test_section_item_at_path():
    assert is_equal_value(os.item_at_path(""), os)
    assert is_equal_value(os.item_at_path("items[at0012]"), ins)
    with pytest.raises(ValueError):
        os.item_at_path("items")

def test_section_items_at_path():
    assert is_equal_value(os.items_at_path("items"), [ins])
    with pytest.raises(ValueError):
        os.items_at_path("items[at0012]")


