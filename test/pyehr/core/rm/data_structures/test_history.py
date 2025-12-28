import pytest

from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_structures.history import PointEvent, IntervalEvent, History
from pyehr.core.rm.data_structures.item_structure import ItemSingle
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.quantity import DVProportion, ProportionKind
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime, DVDuration
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText

hs = History(
    DVText("pain scores over time"),
    archetype_node_id="at0010",
    origin=DVDateTime("2025-12-28T12:00:00Z")
)
da = ItemSingle(
        name=DVText("@ internal @"),
        archetype_node_id="at0012",
        item=Element(
            name=DVText("pain score"),
            archetype_node_id="at0020",
            value=DVProportion(1.0, 10.0, ProportionKind.PK_RATIO)
        )
    )
st = ItemSingle(
        name=DVText("@ internal @"),
        archetype_node_id="at0013",
        item=Element(
            name=DVText("patient state"),
            archetype_node_id="at0030",
            value=DVCodedText("Lying position", CodePhrase(TerminologyID("SNOMED-CT"), "102538003"))
        )
    )
ev = PointEvent[ItemSingle](
    name=DVText("1"),
    archetype_node_id="at0011",
    time=DVDateTime("2025-12-28T13:00:00Z"),
    data=da,
    state=st,
    parent=hs
)

def test_event_offset():
    assert ev.offset().is_equal(DVDuration("PT3600S"))

def test_event_item_at_path():
    assert is_equal_value(ev.item_at_path(""), ev)
    assert is_equal_value(ev.item_at_path("data"), da)
    assert is_equal_value(ev.item_at_path("state"), st)
    with pytest.raises(ValueError):
        ev.item_at_path("folders")
        ev.item_at_path("items[87]")
        ev.item_at_path("abacus")

def test_event_items_at_path():
    with pytest.raises(ValueError):
        ev.items_at_path("")

def test_event_path_unique():
    assert ev.path_unique("") == True
    assert ev.path_unique("data") == True
    assert ev.path_unique("state") == True
    assert ev.path_unique("ABACUS") == False

def test_event_path_exists():
    assert ev.path_unique("") == True
    assert ev.path_unique("data") == True
    assert ev.path_unique("state") == True
    assert ev.path_unique("ABACUS") == False