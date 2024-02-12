import pytest

from org.openehr.base.base_types.identification import UID, ISOOID, UUID, InternetID, UIDBasedID, VersionTreeID, ObjectVersionID

def test_uid_from_unknown_uid_type():
    x = UID.from_unknown_uid_type("51d52cf1-83c9-4f02-b117-703ecb728b74")
    assert type(x) == UUID
    x = UID.from_unknown_uid_type("1.2.826")
    assert type(x) == ISOOID
    x = UID.from_unknown_uid_type("abc123-bar-qwerty.foo.com")
    assert type(x) == InternetID
    with pytest.raises(ValueError):
        x = UID.from_unknown_uid_type("25.2432.4123")
    with pytest.raises(ValueError):
        x = UID.from_unknown_uid_type("abacas")

def test_uuid_only_valid_allowed():
    with pytest.raises(ValueError):
        x = UUID("abcasd")
    with pytest.raises(ValueError):
        x = UUID("{51d52cf1-83c9-4f02-b117-703ecb728b74}")
    x = UUID("51d52cf1-83c9-4f02-b117-703ecb728b74")

def test_oid_only_valid_allowed():
    with pytest.raises(ValueError):
        x = ISOOID("abacasd")
    with pytest.raises(ValueError):
        x = ISOOID("25.2432.4123")
    x = ISOOID("0.3.1111")
    x = ISOOID("1.2.826")

def test_internet_id_only_valid_allowed():
    with pytest.raises(ValueError):
        x = InternetID("foo--bar.com")
    with pytest.raises(ValueError):
        x = InternetID("ababasd")
    x = InternetID("abc123-bar-qwerty.foo.com")

def test_uid_based_id_valid_root():
    x = UIDBasedID("51d52cf1-83c9-4f02-b117-703ecb728b74::shazam")
    x = UIDBasedID("51d52cf1-83c9-4f02-b117-703ecb728b74")
    with pytest.raises(ValueError):
        x = UIDBasedID("foo--bar.com::basd")

def test_uid_based_id_other_methods():
    x = UIDBasedID("51d52cf1-83c9-4f02-b117-703ecb728b74::shazam")
    assert x.root().value == "51d52cf1-83c9-4f02-b117-703ecb728b74"
    assert x.extension() == "shazam"
    assert x.has_extension()
    y = UIDBasedID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2")
    assert y.extension() == "uk.nhs.ehr1::2"

def test_version_tree_id_only_valid_allowed():
    x = VersionTreeID("1")
    x = VersionTreeID("1.2.1")
    with pytest.raises(ValueError):
        x = VersionTreeID("1.2")
    with pytest.raises(ValueError):
        x = VersionTreeID("0")
    with pytest.raises(ValueError):
        x = VersionTreeID("abacus")

def test_version_tree_id_other_methods():
    x = VersionTreeID("1.2.3")
    assert x.trunk_version() == "1"
    assert x.branch_number() == "2"
    assert x.branch_version() == "3"
    assert x.is_branch()
    x = VersionTreeID("20")
    assert x.trunk_version() == "20"
    assert x.branch_number() is None
    assert x.branch_version() is None
    assert not x.is_branch()

def test_object_version_id_only_valid_allowed():
    x = ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2")
    with pytest.raises(ValueError):
        x = ObjectVersionID("abacus")
    with pytest.raises(ValueError):
        # missing version tree ID
        x = ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1")
    with pytest.raises(ValueError):
        # missing creating system ID and version tree ID
        x = ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B")
    with pytest.raises(ValueError):
        # invalid version tree ID
        x = ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::20.2")

def test_object_version_id_other_methods():
    x = ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2")
    assert str(x.object_id()) == "87284370-2D4B-4e3d-A3F3-F303D2F4F34B"
    assert str(x.creating_system_id()) == "uk.nhs.ehr1"
    assert str(x.version_tree_id()) == "2"
    assert not x.is_branch()