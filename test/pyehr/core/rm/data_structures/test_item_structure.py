import pytest

from pyehr.core.base.base_types.identification import ArchetypeID, TerminologyID
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types.text import DVText, DVCodedText, CodePhrase
from pyehr.core.rm.data_types.quantity import DVProportion, ProportionKind, DVQuantity
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_structures.representation import Element, Cluster
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemList, ItemTable


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

def test_item_list_item_at_path_archetype_path():
    assert itl.item_at_path("").is_equal(itl)
    assert itl.item_at_path("items[at0002]").is_equal(e2)
    assert itl.item_at_path("items[at0001]/value").is_equal(t)

def test_item_list_item_at_path_positional_param():
    assert itl.item_at_path("items[1]").is_equal(e2)
    assert itl.item_at_path("items[0]/value").is_equal(t)

def test_item_list_items_at_path_archetype_path():
    assert is_equal_value(itl.items_at_path("items"), [e, e2, e3])
    with pytest.raises(ValueError):
        itl.items_at_path("items[at0002]")
    with pytest.raises(ValueError):
        itl.items_at_path("")

def test_item_list_items_at_path_positional_param():
    with pytest.raises(ValueError):
        itl.items_at_path("items[1]")
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

ev = DVProportion(6.0, 6.0, ProportionKind.PK_RATIO)

el01 = Element(name=DVText("visual acuity"),
                        archetype_node_id="at0021",
                        value=ev)

row0 = Cluster(
            name=DVText("1"),
            archetype_node_id="at0010",
            items=[
                Element(name=DVText("eye(s)"),
                        archetype_node_id="at0020",
                        value=DVCodedText(value="right", defining_code=CodePhrase(TerminologyID("local"), "at0030"))),
                el01])

el10 = Element(name=DVText("eye(s)"),
                        archetype_node_id="at0020",
                        value=DVCodedText(value="left", defining_code=CodePhrase(TerminologyID("local"), "at0031")))

row1 = Cluster(
            name=DVText("2"),
            archetype_node_id="at0010",
            items=[
                el10,
                Element(name=DVText("visual acuity"),
                        archetype_node_id="at0021",
                        value=DVProportion(6.0, 18.0, ProportionKind.PK_RATIO))])

row2 = Cluster(
            name=DVText("3"),
            archetype_node_id="at0010",
            items=[
                Element(name=DVText("eye(s)"),
                        archetype_node_id="at0020",
                        value=DVCodedText(value="both", defining_code=CodePhrase(TerminologyID("local"), "at0030"))),
                Element(name=DVText("visual acuity"),
                        archetype_node_id="at0021",
                        value=DVProportion(6.0, 6.0, ProportionKind.PK_RATIO))])

itbl = ItemTable(
    name=DVText("vision"),
    archetype_node_id="at0002",
    rows=[
        row0,
        row1,
        row2
    ]
)

def test_item_table_column_names_match():
    with pytest.raises(ValueError):
        etbl = ItemTable(
            name="test",
            archetype_node_id="at0010",
            rows=[
                Cluster(
                    name=DVText("1"),
                    archetype_node_id="at0020",
                    items=[
                        Element(
                            name=DVText("State"),
                            archetype_node_id="at0030",
                            value=DVCodedText("Sitting", defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "33586001"))
                        ),
                        Element(
                            name=DVText("Systolic"),
                            archetype_node_id="at0031",
                            value=DVQuantity(120.0, "mmHg")
                        )
                    ]
                ),
                Cluster(
                    name=DVText("2"),
                    archetype_node_id="at0020",
                    items=[
                        Element(
                            name=DVText("State"),
                            archetype_node_id="at0030",
                            value=DVCodedText("Standing", defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "10904000"))
                        ),
                        Element(
                            name=DVText("Diastolic"),
                            archetype_node_id="at0032",
                            value=DVQuantity(80.0, "mmHg")
                        )
                    ]
                )
            ])

def test_item_table_row_count():
    assert itbl.row_count() == 3

def test_item_table_column_count():
    assert itbl.column_count() == 2

def test_item_table_row_names():
    assert is_equal_value(itbl.row_names(), [DVText("1"), DVText("2"), DVText("3")])

def test_item_table_column_names():
    assert is_equal_value(itbl.column_names(), [DVText("eye(s)"), DVText("visual acuity")])

def test_item_table_ith_row():
    assert is_equal_value(itbl.ith_row(0), row0)
    assert is_equal_value(itbl.ith_row(2), row2)
    with pytest.raises(IndexError):
        itbl.ith_row(3)
    with pytest.raises(IndexError):
        itbl.ith_row(-1)

def test_item_table_has_row_with_name():
    assert itbl.has_row_with_name("2") == True
    assert itbl.has_row_with_name("3") == True
    assert itbl.has_row_with_name("4") == False
    assert itbl.has_row_with_name("eye(s)") == False

def test_item_table_has_column_with_name():
    assert itbl.has_column_with_name("eye(s)") == True
    assert itbl.has_column_with_name("visual acuity") == True
    assert itbl.has_column_with_name("2") == False

def test_item_table_named_row():
    assert is_equal_value(itbl.named_row("2"), row1)
    with pytest.raises(KeyError):
        itbl.named_row("abacus")

def test_item_table_has_row_with_key():
    # TODO: replace test once meaning of method worked out
    with pytest.raises(NotImplementedError):
        itbl.has_row_with_key([])

def test_item_table_row_with_key():
    # TODO: replace test once meaning of method worked out
    with pytest.raises(NotImplementedError):
        itbl.row_with_key([])

def test_item_table_element_at_cell_ij():
    assert is_equal_value(itbl.element_at_cell_ij(0, 1), el01)
    assert is_equal_value(itbl.element_at_cell_ij(1, 0), el10)
    with pytest.raises(IndexError):
        itbl.element_at_cell_ij(3, 0)
    with pytest.raises(IndexError):
        itbl.element_at_cell_ij(0, 2)

def test_item_table_as_hierarchy():
    assert is_equal_value(itbl.as_hierarchy(), Cluster(name=DVText("vision"), archetype_node_id="at0002", items=[row0, row1, row2]))

def test_item_table_items_at_path():
    assert is_equal_value(itbl.items_at_path("rows[at0010]"), [row0, row1, row2])
    assert is_equal_value(itbl.items_at_path("rows"), [row0, row1, row2])

def test_item_table_item_at_path():
    assert is_equal_value(itbl.item_at_path("rows[0]/items[at0021]/value"), ev)
    assert is_equal_value(itbl.item_at_path("rows[1]"), row1)
    assert is_equal_value(itbl.item_at_path(""), itbl)