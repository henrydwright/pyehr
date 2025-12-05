import pytest

from common import PythonTerminologyService, TERMINOLOGY_OPENEHR
from org.core.base.base_types.identification import ObjectRef, TerminologyID, ObjectVersionID, HierObjectID
from org.core.rm.common.change_control import OriginalVersion, ImportedVersion, VersionedObject
from org.core.rm.common.generic import AuditDetails, PartyIdentified, Attestation, RevisionHistory, RevisionHistoryItem
from org.core.rm.data_types.quantity.date_time import DVDateTime
from org.core.rm.data_types.text import DVCodedText, DVText, CodePhrase
from org.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers
from org.core.base.foundation_types.structure import is_equal_value

OPENEHR_TID = TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR)

ts_ok = PythonTerminologyService(code_sets=[], terminologies=[TERMINOLOGY_OPENEHR])
ts_empty = PythonTerminologyService([], [])

ov = OriginalVersion[DVText](
    contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")),
    commit_audit=AuditDetails(
        system_id="net.example.ehr",
        time_committed=DVDateTime("2025-09-22T15:41:00Z"),
        change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
        committer=PartyIdentified(name="Mr A Example"),
        terminology_service=ts_ok),
    uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
    lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
    terminology_service=ts_ok,
    data=DVText("Hello, world! This is some example text")
)

iv = ImportedVersion[DVText](
    contribution=ObjectRef("org.example.ehr.prod", "CONTRIBUTION", HierObjectID("7ad8dcdc-62f1-41f6-b7bd-c1171f50aba5")),
    commit_audit=AuditDetails(
        system_id="net.example.ehr",
        time_committed=DVDateTime("2025-11-09T11:58:02Z"),
        change_type=DVCodedText("format conversion", CodePhrase(OPENEHR_TID, "817")),
        committer=PartyIdentified(name="Anytown NHS Trust ehrBridge"),
        terminology_service=ts_ok
    ),
    item=ov
)

def test_original_version_lifecycle_state_valid():
    # OK (code provided and coded correctly)
    ov = OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some example text")
    )
    # not OK (ts without openehr ts)
    with pytest.raises(ValueError):
        ov = OriginalVersion[DVText](
            contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
            commit_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-22T15:41:00Z"),
                change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
                committer=PartyIdentified(name="Mr A Example"),
                terminology_service=ts_ok),
            uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
            lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
            terminology_service=ts_empty,
            data=DVText("Hello, world! This is some example text")
            )
    # not OK (invalid code)
    with pytest.raises(ValueError):
        ov = OriginalVersion[DVText](
            contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
            commit_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-22T15:41:00Z"),
                change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "10000000000000")),
                committer=PartyIdentified(name="Mr A Example"),
                terminology_service=ts_ok),
            uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
            lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
            terminology_service=ts_ok,
            data=DVText("Hello, world! This is some example text")
        )

def test_original_version_uid_derived_methods():
    assert ov.uid().value == "154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"
    assert ov.is_branch() == False
    assert ov.owner_id().value == "154b1047-23aa-4d4d-8713-df848fd4d60a"
    # preceding_version_uid_validity
    assert ov.uid().version_tree_id().trunk_version() == "1"
    assert ov.preceding_version_uid() is None

def test_original_version_attestations_valid():
    # OK (attestations list)
    OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some example text"),
        attestations=[
            Attestation(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-22T15:41:00Z"),
                change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
                committer=PartyIdentified(name="Mr A Example"),
                reason=DVCodedText("signed", CodePhrase(OPENEHR_TID, "240")),
                is_pending=False,
                terminology_service=ts_ok
            )]
    )
    # not OK (empty attestations list)
    with pytest.raises(ValueError):
        OriginalVersion[DVText](
            contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
            commit_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-22T15:41:00Z"),
                change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
                committer=PartyIdentified(name="Mr A Example"),
                terminology_service=ts_ok),
            uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
            lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
            terminology_service=ts_ok,
            data=DVText("Hello, world! This is some example text"),
            attestations=[]
        )

def test_original_version_is_merged_validity():
    assert ov.is_merged() == False
    ov2 = OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some example text"),
        other_input_version_uids=[
            ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr.prod::1")
        ]
    )
    assert ov2.is_merged() == True

def test_original_version_other_input_version_uids_valid():
    # OK (other_version_uid list filled)
    ov2 = OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some example text"),
        other_input_version_uids=[
            ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr.prod::1")
        ]
    )
    # not OK (empty list for other_input_version_uids)
    with pytest.raises(ValueError):
        ov2 = OriginalVersion[DVText](
            contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", "1826ea47-e98b-4779-b201-80db3af5de92"),
            commit_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-22T15:41:00Z"),
                change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
                committer=PartyIdentified(name="Mr A Example"),
                terminology_service=ts_ok),
            uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
            lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
            terminology_service=ts_ok,
            data=DVText("Hello, world! This is some example text"),
            other_input_version_uids=[]
        )

def test_original_version_inherited_version_methods_correct():
    assert ov.data().is_equal(DVText("Hello, world! This is some example text"))
    assert ov.lifecycle_state().is_equal(DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")))

def test_imported_version_inherited_version_methods_correct():
    # these all just take the values from the encapsulated item member
    assert iv.uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
    assert iv.preceding_version_uid() is None
    assert iv.lifecycle_state().is_equal(DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")))
    assert iv.data().is_equal(DVText("Hello, world! This is some example text"))
    assert iv.owner_id().value == "154b1047-23aa-4d4d-8713-df848fd4d60a"
    assert iv.is_branch() == False

def _generate_versioned_object_empty():
    return VersionedObject[DVText](
        uid=HierObjectID("154b1047-23aa-4d4d-8713-df848fd4d60a"),
        owner_id=ObjectRef("net.example.ehr", "EHR", HierObjectID("5ecf06cf-c754-4ab6-afb6-19666e510395")),
        time_created=DVDateTime("2025-09-20T17:00:00Z")
    )

def _generate_versioned_object_one_version():
    vo = _generate_versioned_object_empty()
    vo.commit_original_version(
        a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")),
        a_new_version_uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        a_preceding_version_id=None,
        an_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-21T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=ts_ok),
        a_lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        a_data=DVText("Hello, world! This is some example text"),
        terminology_service=ts_ok
    )
    return vo

def _generate_versioned_object_two_versions():
    vo = _generate_versioned_object_one_version()
    vo.commit_original_version(
        a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("baf97527-5c6f-422c-9c4f-48c37a3d8e0a")),
        a_new_version_uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
        a_preceding_version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        an_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-21T15:41:00Z"),
            change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
            committer=PartyIdentified(name="Ms C Test"),
            terminology_service=ts_ok),
        a_lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        a_data=DVText("Hello, world! This is some edited example text (saved as a new version!)"),
        terminology_service=ts_ok
    )
    vo.commit_attestation(
        an_attestation=Attestation(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-21T16:19:30+00:00"),
            change_type=DVCodedText("attestation", CodePhrase(OPENEHR_TID, "666")),
            committer=PartyIdentified(name="Mr A Example"),
            reason=DVText("Accept modifications"),
            is_pending=False,
            terminology_service=ts_ok
        ),
        a_ver_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2")
    )
    return vo

def _generate_versioned_object_three_versions():
    vo = _generate_versioned_object_two_versions()
    ov = OriginalVersion(
        contribution=ObjectRef("org.example.ehr2", "CONTRIBUTION", HierObjectID("d2fabe65-73fc-4e7a-aa46-13a50f48885c")),
        commit_audit=AuditDetails(
            system_id="org.example.ehr2",
            time_committed=DVDateTime("2025-11-11T08:23:40Z"),
            change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
            committer=PartyIdentified(name="Dr B Bexample"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr2::3"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some edited example text (saved as a new version!) and then modified on another system"),
        preceding_version_uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2")
    )
    vo.commit_imported_version(
        a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("5fc1da8e-88c0-4fa9-9ee3-06aeaead03cc")),
        an_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-11-11T08:30:00Z"),
            change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
            committer=PartyIdentified(name="RECORD IMPORTER"),
            terminology_service=ts_ok),
        a_version=ov
    )
    return vo

def test_versioned_object_version_count():
    vo1 = _generate_versioned_object_empty()
    assert vo1.version_count() == 0
    vo2 = _generate_versioned_object_two_versions()
    assert vo2.version_count() == 2

def test_versioned_object_all_version_ids():
    vo = _generate_versioned_object_two_versions()
    test_id_list = [ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"), ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2")]
    assert is_equal_value(vo.all_version_ids(), test_id_list)

def test_versioned_object_all_versions():
    vo = _generate_versioned_object_two_versions()
    versions = vo.all_versions()
    assert versions[0].uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
    assert versions[1].uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"))

def test_versioned_object_has_version_at_time():
    vo = _generate_versioned_object_two_versions()
    assert vo.has_version_at_time(DVDateTime("2025-09-21T15:41:00Z")) == True
    assert vo.has_version_at_time(DVDateTime("20250921T154100Z")) == True
    assert vo.has_version_at_time(DVDateTime("2025-09-20T17:00:00Z")) == False
    assert vo.has_version_at_time(DVDateTime("2025-11-09T22:30:00Z")) == False

def test_versioned_object_has_version_id():
    vo = _generate_versioned_object_two_versions()
    assert vo.has_version_id(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1")) == True
    assert vo.has_version_id(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1.1.1")) == False
    assert vo.has_version_id(ObjectVersionID("7117d71d-130e-444b-ba7e-fb6e0b59ce8f::org.example.ehr2::1")) == False

def test_versioned_object_version_with_id():
    vo = _generate_versioned_object_one_version()
    # works if version exists
    ov = vo.version_with_id(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
    assert ov.preceding_version_uid() is None
    assert ov.uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
    # raises error if version does not exist
    with pytest.raises(KeyError):
        vo.version_with_id(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1.1.1"))

def test_versioned_object_is_original_version():
    vo = _generate_versioned_object_three_versions()
    # works if versions exist
    assert vo.is_original_version(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1")) == True
    assert vo.is_original_version(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr2::3")) == False
    # raises error if version does not exist
    with pytest.raises(ValueError):
        vo.is_original_version(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1.1.1"))

def test_versioned_object_version_at_time():
    vo = _generate_versioned_object_two_versions()
    # works if version exists
    ov = vo.version_at_time(DVDateTime("20250921T154100Z"))
    assert ov.preceding_version_uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
    assert ov.uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"))
    # raises error if version does not exist
    with pytest.raises(KeyError):
        vo.version_at_time(DVDateTime("20171111T084700"))

def test_versioned_object_revision_history():
    vo = _generate_versioned_object_three_versions()
    rh = RevisionHistory([
        # v1
        RevisionHistoryItem(
            version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
            audits=[
                AuditDetails(
                    system_id="net.example.ehr",
                    time_committed=DVDateTime("2025-09-21T15:41:00Z"),
                    change_type=DVCodedText("creation", CodePhrase(OPENEHR_TID, "249")),
                    committer=PartyIdentified(name="Mr A Example"),
                    terminology_service=ts_ok)
            ]
        ),
        # v2
        RevisionHistoryItem(
            version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
            audits=[
                AuditDetails(
                    system_id="net.example.ehr",
                    time_committed=DVDateTime("2025-09-21T15:41:00Z"),
                    change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                    committer=PartyIdentified(name="Ms C Test"),
                    terminology_service=ts_ok),
                Attestation(
                    system_id="net.example.ehr",
                    time_committed=DVDateTime("2025-09-21T16:19:30+00:00"),
                    change_type=DVCodedText("attestation", CodePhrase(OPENEHR_TID, "666")),
                    committer=PartyIdentified(name="Mr A Example"),
                    reason=DVText("Accept modifications"),
                    is_pending=False,
                    terminology_service=ts_ok
                )
            ]
        ),
        # v3
        RevisionHistoryItem(
            version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr2::3"),
            audits=[
                AuditDetails(
                    system_id="net.example.ehr",
                    time_committed=DVDateTime("2025-11-11T08:30:00Z"),
                    change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                    committer=PartyIdentified(name="RECORD IMPORTER"),
                    terminology_service=ts_ok)
            ]
        )
    ])
    vo_rh = vo.revision_history()
    print(vo_rh.as_json())
    assert vo_rh.is_equal(rh) == True

def test_versioned_object_latest_version():
    vo = _generate_versioned_object_two_versions()
    v = vo.latest_version()
    assert v.uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"))
    vo2 = _generate_versioned_object_empty()
    assert vo2.latest_version() is None

def test_versioned_object_latest_trunk_version():
    vo = _generate_versioned_object_three_versions()
    v = vo.latest_trunk_version()
    assert v.uid().is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr2::3"))
    vo2 = _generate_versioned_object_empty()
    assert vo2.latest_trunk_version() is None

def test_versioned_object_trunk_lifecycle_state():
    vo = _generate_versioned_object_two_versions()
    assert vo.trunk_lifecycle_state().is_equal(DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")))
    vo2 = _generate_versioned_object_empty()
    assert vo2.trunk_lifecycle_state() is None

def test_versioned_object_commit_original_version():
    # works for OK original version
    vo = _generate_versioned_object_one_version()
    # invariants met
    assert vo.version_count() == 1
    assert len(vo.all_version_ids()) == vo.version_count()
    assert len(vo.all_versions()) == vo.version_count()
    assert vo.latest_version() is not None

    # doesn't allow UID mismatch
    with pytest.raises(ValueError):
        vo.commit_original_version(
            a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("baf97527-5c6f-422c-9c4f-48c37a3d8e0a")),
            a_new_version_uid=ObjectVersionID("48c46c4f-6351-4f85-9aa7-f31d69752f5f::net.example.ehr::2"),
            a_preceding_version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
            an_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-21T15:41:00Z"),
                change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                committer=PartyIdentified(name="Ms C Test"),
                terminology_service=ts_ok),
            a_lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
            a_data=DVText("Hello, world! This is some edited example text (saved as a new version!)"),
            terminology_service=ts_ok
        )

    # doesn't allow non-existing preceding version uid
    with pytest.raises(ValueError):
        vo.commit_original_version(
                a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("baf97527-5c6f-422c-9c4f-48c37a3d8e0a")),
                a_new_version_uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2"),
                a_preceding_version_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.evilehr::1"),
                an_audit=AuditDetails(
                    system_id="net.example.ehr",
                    time_committed=DVDateTime("2025-09-21T15:41:00Z"),
                    change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                    committer=PartyIdentified(name="Ms C Test"),
                    terminology_service=ts_ok),
                a_lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
                a_data=DVText("Hello, world! This is some edited example text (saved as a new version!)"),
                terminology_service=ts_ok
            )

def test_versioned_object_commit_imported_version():
    # works OK for imported version
    vo = _generate_versioned_object_three_versions()
    # invariants met
    assert vo.version_count() == 3
    assert len(vo.all_version_ids()) == vo.version_count()
    assert len(vo.all_versions()) == vo.version_count()
    assert vo.latest_version() is not None

    # doesn't allow UID mismatch
    ov = OriginalVersion(
        contribution=ObjectRef("org.example.ehr2", "CONTRIBUTION", HierObjectID("d2fabe65-73fc-4e7a-aa46-13a50f48885c")),
        commit_audit=AuditDetails(
            system_id="org.example.ehr2",
            time_committed=DVDateTime("2025-11-11T08:23:40Z"),
            change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
            committer=PartyIdentified(name="Dr B Bexample"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("ff6e0432-6bfa-49c9-b868-39c88cca1ad1::org.example.ehr2::3"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some edited example text (saved as a new version!) and then modified on another system"),
        preceding_version_uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::2")
    )
    with pytest.raises(ValueError):
        vo.commit_imported_version(
            a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("5fc1da8e-88c0-4fa9-9ee3-06aeaead03cc")),
            an_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-11-11T08:30:00Z"),
                change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                committer=PartyIdentified(name="RECORD IMPORTER"),
                terminology_service=ts_ok),
            a_version=ov
        )

    # doesn't allow non-existing preceding version uid
    ov = OriginalVersion(
        contribution=ObjectRef("org.example.ehr2", "CONTRIBUTION", HierObjectID("d2fabe65-73fc-4e7a-aa46-13a50f48885c")),
        commit_audit=AuditDetails(
            system_id="org.example.ehr2",
            time_committed=DVDateTime("2025-11-11T08:23:40Z"),
            change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
            committer=PartyIdentified(name="Dr B Bexample"),
            terminology_service=ts_ok),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::org.example.ehr2::3"),
        lifecycle_state=DVCodedText("complete", CodePhrase(OPENEHR_TID, "532")),
        terminology_service=ts_ok,
        data=DVText("Hello, world! This is some edited example text (saved as a new version!) and then modified on another system"),
        preceding_version_uid=ObjectVersionID("ff6e0432-6bfa-49c9-b868-39c88cca1ad1::net.example.ehr::2")
    )
    with pytest.raises(ValueError):
        vo.commit_imported_version(
            a_contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("5fc1da8e-88c0-4fa9-9ee3-06aeaead03cc")),
            an_audit=AuditDetails(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-11-11T08:30:00Z"),
                change_type=DVCodedText("modification", CodePhrase(OPENEHR_TID, "251")),
                committer=PartyIdentified(name="RECORD IMPORTER"),
                terminology_service=ts_ok),
            a_version=ov
        )

def test_versioned_object_commit_attestation():
    # works OK for committing attestation
    vo = _generate_versioned_object_two_versions()
    
    # doesn't work if version doesn't exist
    with pytest.raises(ValueError):
        vo.commit_attestation(
            an_attestation=Attestation(
                system_id="net.example.ehr",
                time_committed=DVDateTime("2025-09-21T16:19:30+00:00"),
                change_type=DVCodedText("attestation", CodePhrase(OPENEHR_TID, "666")),
                committer=PartyIdentified(name="Mr A Example"),
                reason=DVText("Accept modifications"),
                is_pending=False,
                terminology_service=ts_ok
            ),
            a_ver_id=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::9")
        )

def test_versioned_object_uid_validity():
    # works OK for normal creation
    vo = _generate_versioned_object_empty()

    # does not work if UID has extension
    with pytest.raises(ValueError):
        vo2 = VersionedObject[DVText](
            uid=HierObjectID("6cd3b6a4-212b-4f42-a3f2-7d3984d5657b::foxtrot"),
            owner_id=ObjectRef("net.example.ehr", "EHR", HierObjectID("5ecf06cf-c754-4ab6-afb6-19666e510395")),
            time_created=DVDateTime("2025-09-20T17:00:00Z")
            )

