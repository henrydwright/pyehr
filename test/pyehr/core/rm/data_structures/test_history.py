import pytest

from term import TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_structures.history import PointEvent, IntervalEvent, History
from pyehr.core.rm.data_structures.item_structure import ItemSingle
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.quantity import DVProportion, ProportionKind
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime, DVDuration
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

import json

test_ts = PythonTerminologyService([], [TERMINOLOGY_OPENEHR])

su = ItemSingle(
        DVText("@ internal @"),
        archetype_node_id="at0080",
        item=Element(
            name=DVText("commentary"),
            archetype_node_id="at0081",
            value=DVText("pain scores mild during day and overnight")
        )
    )

hs = History[ItemSingle](
    DVText("pain scores over time"),
    archetype_node_id="at0010",
    origin=DVDateTime("2025-12-28T12:00:00Z"),
    summary=su
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

iev = IntervalEvent[ItemSingle](
    name=DVText("overnight pain score average"),
    archetype_node_id="at0014",
    time=DVDateTime("2025-12-29T08:00:00Z"),
    data=ItemSingle(
        name=DVText("@ internal @"),
        archetype_node_id="at0015",
        item=Element(
            DVText("pain score"),
            archetype_node_id="at0016",
            value=DVProportion(5.6, 10.0, ProportionKind.PK_RATIO)
        )
    ),
    width=DVDuration("PT12H"),
    math_function=DVCodedText("mean", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "146")),
    terminology_service=test_ts,
    parent=hs
)

def test_interval_event_interval_start_time():
    assert iev.interval_start_time().is_equal(DVDateTime("2025-12-28T20:00:00Z"))

def test_interval_event_math_function_validity():
    with pytest.raises(ValueError):
        IntervalEvent[ItemSingle](
            name=DVText("overnight pain score average"),
            archetype_node_id="at0014",
            time=DVDateTime("2025-12-29T08:00:00Z"),
            data=ItemSingle(
                name=DVText("@ internal @"),
                archetype_node_id="at0015",
                item=Element(
                    DVText("pain score"),
                    archetype_node_id="at0016",
                    value=DVProportion(5.6, 10.0, ProportionKind.PK_RATIO)
                )
            ),
            width=DVDuration("PT12H"),
            math_function=DVCodedText("square_root", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "999")),
            terminology_service=test_ts,
            parent=hs
        )

hs.events = [ev, iev]

def test_history_periodic_validity():
    assert hs.is_periodic() == False
    p_his = History(
        name=DVText("hourly heartrate measurements"),
        archetype_node_id="at0040",
        origin=DVDateTime("2025-08-01T09:30:00+01:00"),
        period=DVDuration("PT1H")
    )
    assert p_his.is_periodic() == True

def test_history_item_at_path():
    assert is_equal_value(hs.item_at_path(""), hs)
    assert is_equal_value(hs.item_at_path("summary"), su)
    assert is_equal_value(hs.item_at_path("events[0]"), ev)
    assert is_equal_value(hs.item_at_path("events[at0014]"), iev)
    assert is_equal_value(hs.item_at_path("events[at0011]/data"), da)
    with pytest.raises(IndexError):
        hs.item_at_path("events[3]")

def test_history_items_at_path():
    assert is_equal_value(hs.items_at_path("events"), [ev, iev])
    with pytest.raises(ValueError):
        hs.items_at_path("")
    with pytest.raises(ValueError):
        hs.items_at_path("events[1]")

def test_history_events_valid():
    with pytest.raises(ValueError):
        empty_his = History(
            name=DVText("hourly heartrate measurements"),
            archetype_node_id="at0040",
            origin=DVDateTime("2025-08-01T09:30:00+01:00"),
            events=[]
        )

def test_history_as_hierarchy():
    hier = hs.as_hierarchy()
    target = Cluster(
        name=DVText("pain scores over time"),
        archetype_node_id="at0010",
        items=[
            Cluster(
                name=DVText("summary (GENERATED)"),
                archetype_node_id="at0080",
                items=[
                    Element(
                        name=DVText("commentary"),
                        archetype_node_id="at0081",
                        value=DVText("pain scores mild during day and overnight")
                    )
                ]
            ),
            Cluster(
                name=DVText("events (GENERATED)"),
                archetype_node_id="at9999",
                items=[
                    Cluster(
                        name=DVText("1"),
                        archetype_node_id="at0011",
                        items=[
                            Cluster(
                                name=DVText("data (GENERATED)"),
                                archetype_node_id="at0012",
                                items=[
                                    Element(
                                        name=DVText("pain score"),
                                        archetype_node_id="at0020",
                                        value=DVProportion(1.0, 10.0, ProportionKind.PK_RATIO)
                                    )
                                ]
                            ),
                            Cluster(
                                name=DVText("state (GENERATED)"),
                                archetype_node_id="at0013",
                                items=[
                                    Element(
                                        name=DVText("patient state"),
                                        archetype_node_id="at0030",
                                        value=DVCodedText("Lying position", CodePhrase(TerminologyID("SNOMED-CT"), "102538003"))
                                    )
                                ]
                            )
                        ]
                    ),
                    Cluster(
                        name=DVText("overnight pain score average"),
                        archetype_node_id="at0014",
                        items=[
                            Cluster(
                                name=DVText("data (GENERATED)"),
                                archetype_node_id="at0015",
                                items=[
                                    Element(
                                        DVText("pain score"),
                                        archetype_node_id="at0016",
                                        value=DVProportion(5.6, 10.0, ProportionKind.PK_RATIO)
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )]
        )

    assert hier.is_equal(target)
