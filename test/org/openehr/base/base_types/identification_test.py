import pytest

from org.openehr.base.base_types.identification import *

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

def test_archetype_id_only_valid_allowed():
    # ID containing all elements
    a = ArchetypeID("openEHR-EHR-OBSERVATION.bp_measurement.v1")
    a = ArchetypeID("openEHR-EHR-OBSERVATION.bp_measurement.v021")
    a = ArchetypeID("openEHR-EHR-OBSERVATION.biochemistry_result-cholesterol.v502")
    # OTHER ISSUES
    with pytest.raises(ValueError):
        # lacks concept
        a = ArchetypeID("openEHR-EHR-OBSERVATION.v1")
    with pytest.raises(ValueError):
        # lacks rm_name
        a = ArchetypeID("openEHR-EHR.bp_measurement.v1")
    # VERSION ID ISSUES
    with pytest.raises(ValueError):
        # lacks version ID
        a = ArchetypeID("openEHR-EHR-OBSERVATION.bp_measurement")
    with pytest.raises(ValueError):
        # invalid version ID (no number after v)
        a = ArchetypeID("openEHR-EHR-OBSERVATION.bp_measurement.v")
    with pytest.raises(ValueError):
        # invalid version ID (contains .)
        a = ArchetypeID("openEHR-EHR-OBSERVATION.bp_measurement.v1.3.2")

def test_archetype_id_other_methods_correct():
    a = ArchetypeID("openEHR-EHR-OBSERVATION.biochemistry_result-cholesterol.v502")
    assert a.qualified_rm_entity() == "openEHR-EHR-OBSERVATION"
    assert a.domain_concept() == "biochemistry_result-cholesterol"
    assert a.rm_originator() == "openEHR"
    assert a.rm_name() == "EHR"
    assert a.rm_entity() == "OBSERVATION"
    assert a.specialisation() == "cholesterol"
    assert a.version_id() == "502"

def test_terminology_id_only_valid_allowed():
    t = TerminologyID("SNOMED-CT")
    # Note: the below is allowed according to 5.3.2.3 but not 5.5
    #        we have taken 5.3.2.3 to be truthful (i.e. below is allowed)
    t = TerminologyID("ICD10AM(3rd_ed)")
    with pytest.raises(ValueError):
        t = TerminologyID("2ABC") # cannot start with digit
    with pytest.raises(ValueError):
        t = TerminologyID("ABC&D") # invalid symbol '&'
    with pytest.raises(ValueError):
        t = TerminologyID("ABC(abc)a") # nothing should follow version

def test_terminology_id_other_methods_correct():
    t = TerminologyID("ICD10AM(3rd_ed)")
    assert t.name() == "ICD10AM"
    assert t.version_id() == "3rd_ed"

def test_generic_id_scheme_words():
    g = GenericID("abacus", "local")
    assert g.scheme == "local"

def test_object_ref_only_valid_allowed():
    o = ObjectRef("local", "PARTY", ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2"))
    with pytest.raises(ValueError):
        o = ObjectRef("09ehr", "PERSON", UIDBasedID("uk.nhs::test")) # invalid namespace

def test_object_ref_other_methods_correct():
    o = ObjectRef("local", "PARTY", ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2"))
    assert o.namespace == "local"
    assert o.ref_type == "PARTY"
    assert o.id.is_equal(ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2"))

def test_party_ref_type_validity_enforced():
    p = PartyRef("local", "PERSON", ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2"))
    with pytest.raises(ValueError):
        p = PartyRef("local", "GUIDELINE", ObjectVersionID("87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2")) # doesn't refer to a party
