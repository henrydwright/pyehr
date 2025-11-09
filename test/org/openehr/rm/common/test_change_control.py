import pytest

from common import PythonTerminologyService, TERMINOLOGY_OPENEHR
from org.openehr.base.base_types.identification import ObjectRef, TerminologyID, ObjectVersionID, HierObjectID
from org.openehr.rm.common.change_control import OriginalVersion, ImportedVersion
from org.openehr.rm.common.generic import AuditDetails, PartyIdentified, Attestation
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_types.text import DVCodedText, DVText, CodePhrase
from org.openehr.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

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
