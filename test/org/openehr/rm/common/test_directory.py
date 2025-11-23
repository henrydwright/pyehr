import pytest

from org.openehr.base.base_types.identification import HierObjectID, ObjectRef, ArchetypeID
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.rm.common.archetyped import Archetyped
from org.openehr.rm.common.directory import Folder
from org.openehr.rm.data_types.text import DVText

fcc = Folder(
            name=DVText("standing"),
            archetype_node_id="at0006",
            items=[
                ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("6bac63dd-99f8-4374-a263-c41cfd5215b2")),
                ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("4672c825-c599-4f84-aab6-e342713df133"))
            ]
        )

fc = Folder(
        name=DVText("blood pressure readings"),
        archetype_node_id="at0005",
        folders=[
            fcc,
            Folder(
                name=DVText("sitting"),
                archetype_node_id="at0007",
                items=[
                    ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("b207449e-397b-4c44-8896-81fff5097bad")),
                    ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("c5e85918-e047-4fa9-ac7b-19ed4d8668b0")),
                    ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("18eed64a-1221-4736-ad66-b405615b38e9"))
                ]
            )
        ]
    )

fr = Folder(
        name=DVText("remote monitoring"),
        archetype_node_id="pyehr-EHR-FOLDER.remote_monitoring.v0",
        archetype_details=Archetyped(
            archetype_id=ArchetypeID("pyehr-EHR-FOLDER.remote_monitoring.v0"),
            rm_version="1.1.0"
        ),
        uid=HierObjectID("1d61465e-020c-4d62-b452-5e79312efae7"),
        folders=[
            fc,
            Folder(
                name=DVText("weight readings"),
                archetype_node_id="at0008",
                items=[
                    ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("dddccf1f-17a9-4ede-8f7d-64938ac5b601")),
                    ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("e62003b2-4830-4779-9adf-4927f0cad503"))
                ]
            )
        ],
    )

def test_folder_folders_valid():
    # OK (non-empty list)
    fr.name

    # not OK (empty list of folders)
    with pytest.raises(ValueError):
        f_fail = Folder(
            name=DVText("remote monitoring"),
            archetype_node_id="pyehr-EHR-FOLDER.remote_monitoring.v0",
            uid=HierObjectID("1d61465e-020c-4d62-b452-5e79312efae7"),
            folders=[]
        )

def test_folder_parent():
    # test for child
    assert fc.parent().is_equal(fr)

    # test for root
    assert fr.parent() is None

def test_folder_concept():
    # correct concept returned at all levels
    assert fcc.concept().value == "pyehr-EHR-FOLDER.remote_monitoring.v0"
    assert fc.concept().value == "pyehr-EHR-FOLDER.remote_monitoring.v0"
    assert fr.concept().value == "pyehr-EHR-FOLDER.remote_monitoring.v0"
    
def test_folder_path_of_item():
    assert fcc.path_of_item() == "/folders[blood pressure readings]/folders[standing]"
    assert fc.path_of_item() == "/folders[blood pressure readings]"
    assert fr.path_of_item() == "/"

def test_folder_path_exists():
    # Well formed
    assert fcc.path_exists("items[0]") == True
    assert fcc.path_exists("items[2]") == False
    assert fc.path_exists("folders[sitting]") == True
    assert fc.path_exists("folders[standing]/items") == True
    assert fc.path_exists("folders[standing]/folders") == False
    assert fc.path_exists("folders[standing]/items[0]") == True
    assert fc.path_exists("folders[standing/items[2]") == False
    assert fc.path_exists("folders[lying]") == False
    assert fc.path_exists("folders[lying]/items[2]") == False
    assert fr.path_exists("folders[blood pressure readings]/folders[standing]/items[0]")
    # Mal-formed
    assert fcc.path_exists("abacus") == False
    assert fr.path_exists("folder[sitting]") == False
    assert fr.path_exists("folders(sitting)") == False
    assert fcc.path_exists("items(1)") == False
    assert fcc.path_exists("items[6bac63dd-99f8-4374-a263-c41cfd5215b2]") == False

def test_folder_items_at_path():
    # Well formed and multiple items
    assert is_equal_value(fc.items_at_path("folders[standing]/items"), fcc.items)
    assert is_equal_value(fr.items_at_path("folders[blood pressure readings]/folders"), fc.folders)

    # Well formed but not found or single item
    with pytest.raises(ValueError):
        # valid but single item (item)
        fcc.items_at_path("items[0]")
    with pytest.raises(IndexError):
        # path doesn't exist
        fcc.items_at_path("items[2]")
    with pytest.raises(ValueError):
        # valid but single item (folder)
        fc.items_at_path("folders[standing]")
    with pytest.raises(ValueError):
        fc.items_at_path("folders[standing]/folders")

    # Mal-formed
    with pytest.raises(ValueError):
        fcc.items_at_path("abacus")
    with pytest.raises(ValueError):
        fr.items_at_path("folder[sitting]")
    with pytest.raises(ValueError):
        fr.items_at_path("folders(sitting)")
    with pytest.raises(ValueError):
        fcc.items_at_path("items(1)")
    with pytest.raises(ValueError):
        fcc.items_at_path("items[6bac63dd-99f8-4374-a263-c41cfd5215b2]")

def test_folder_item_at_path():
    # Well formed and single item
    assert is_equal_value(fcc.item_at_path("items[0]"), fcc.items[0])
    assert is_equal_value(fc.item_at_path("folders[standing]"), fc._folders_dict["standing"])

    # Well formed but not found or single item
    with pytest.raises(ValueError):
        # valid but single item (item)
        fc.item_at_path("folders[standing]/items")
    with pytest.raises(IndexError):
        # path doesn't exist
        fcc.item_at_path("items[2]")
    with pytest.raises(ValueError):
        # valid but single item (folder)
        fr.item_at_path("folders[blood pressure readings]/folders")
    with pytest.raises(ValueError):
        fc.item_at_path("folders[standing]/folders")

    # Mal-formed
    with pytest.raises(ValueError):
        fcc.item_at_path("abacus")
    with pytest.raises(ValueError):
        fr.item_at_path("folder[sitting]")
    with pytest.raises(ValueError):
        fr.item_at_path("folders(sitting)")
    with pytest.raises(ValueError):
        fcc.item_at_path("items(1)")
    with pytest.raises(ValueError):
        fcc.item_at_path("items[6bac63dd-99f8-4374-a263-c41cfd5215b2]")

def test_folder_path_unique():
    # Well formed
    assert fcc.path_unique("items[0]") == True
    assert fcc.path_unique("items[2]") == True
    assert fc.path_unique("folders[sitting]") == True
    assert fc.path_unique("folders[standing]/items") == False
    assert fc.path_unique("folders[standing]/folders") == False
    assert fc.path_unique("folders[standing]/items[0]") == True
    assert fc.path_unique("folders[standing/items[2]") == True
    assert fc.path_unique("folders[lying]") == True
    assert fc.path_unique("folders[lying]/items[2]") == True
    assert fr.path_unique("folders[blood pressure readings]/folders[standing]/items[0]") == True
    # Mal-formed
    assert fcc.path_unique("abacus") == False
    assert fr.path_unique("folder[sitting]") == False
    assert fr.path_unique("folders(sitting)") == False
    assert fcc.path_unique("items(1)") == False
    assert fcc.path_unique("items[6bac63dd-99f8-4374-a263-c41cfd5215b2]") == True
