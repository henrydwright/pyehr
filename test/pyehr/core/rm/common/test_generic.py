import pytest

from common import PythonTerminologyService, TERMINOLOGY_OPENEHR
from pyehr.core.base.base_types.identification import PartyRef, ObjectID, TerminologyID, ObjectVersionID
from pyehr.core.rm.common.generic import PartyIdentified, PartyRelated, Participation, AuditDetails, Attestation, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.text import DVCodedText, CodePhrase, DVText
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.uri import DVEHRUri
from pyehr.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

ts_ok = PythonTerminologyService(code_sets=[], terminologies=[TERMINOLOGY_OPENEHR])
ts_empty = PythonTerminologyService(code_sets=[], terminologies=[])

def test_party_identified_basic_validity():
    # OK (one of three not void)
    pi = PartyIdentified(external_ref=PartyRef("gmc_number", "PERSON", ObjectID("9999999")))
    pi = PartyIdentified(name="Dr. Test Example")
    pi = PartyIdentified(identifiers=[DVIdentifier("9999999", issuer="General Medical Council")])

    # not OK (all void)
    with pytest.raises(ValueError):
        pi = PartyIdentified()

def test_party_identified_name_valid():
    # OK (name not empty)
    pi = PartyIdentified(name="Dr. Test Example")

    # not OK (name empty)
    with pytest.raises(ValueError):
        pi = PartyIdentified(name="")

def test_party_identified_identifiers_valid():
    # OK (list of identifiers not empty)
    pi = PartyIdentified(identifiers=[DVIdentifier("9999999", issuer="General Medical Council")])

    # not OK (identifiers empty)
    with pytest.raises(ValueError):
        pi = PartyIdentified(identifiers=[])

def test_party_related_relationship_valid():
    PartyRelated(
        relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "10", "mother")),
        terminology_service=ts_ok,
        name="Ms. A Example"
        )
    # not OK (term svc without openehr)
    with pytest.raises(ValueError):
        PartyRelated(
            relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "10", "mother")),
            terminology_service=ts_empty,
            name="Ms. A Example"
            )
    # not OK (code not in terminology group)
    with pytest.raises(ValueError):
        PartyRelated(
            relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "1000", "mum")),
            terminology_service=ts_ok,
            name="Ms. A Example"
            )

def test_participation_function_valid():
    # OK (text, not coded)
    Participation(DVText("observer"), PartyIdentified(name="Ms. A Student"))
    # OK (coded text, uses right coding, provides TS)
    Participation(
        function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
        performer=PartyIdentified(name="MRS J TEST"),
        terminology_service=ts_ok)
    # not OK (coded text, uses wrong coding)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("anesthesia nurse", CodePhrase(TerminologyID("HL7v3"), "ANRS")),
            performer=PartyIdentified(name="MRS J TEST"),
            terminology_service=ts_ok)
    # not OK (terminology service empty)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
            performer=PartyIdentified(name="MRS J TEST"),
            terminology_service=ts_empty)
    # not OK (no term svc)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
            performer=PartyIdentified(name="MRS J TEST"))
        
def test_participation_mode_valid():
    # OK (coded text, uses right coding, provides ts)
    Participation(
        function=DVText("observer"), 
        performer=PartyIdentified(name="Ms. A Student"),
        mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")),
        terminology_service=ts_ok)
    # not OK (uses invalid code)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "524", "initial")),
            terminology_service=ts_ok)
    # not OK (empty ts)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")),
            terminology_service=ts_empty)
    # not OK (no termsvc)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")))
        
def test_audit_details_system_id_valid():
    # OK
    AuditDetails(
        system_id="example_hospital_ehr",
        time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
        change_type=DVCodedText("creation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "249", "creation")),
        committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
        terminology_service=ts_ok
    )
    # not OK (system_id empty string)
    with pytest.raises(ValueError):
        AuditDetails(
            system_id="",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "249", "creation")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            terminology_service=ts_ok
        )

def test_audit_details_change_type_valid():
    # OK
    AuditDetails(
        system_id="example_hospital_ehr",
        time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
        change_type=DVCodedText("creation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "249", "creation")),
        committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
        terminology_service=ts_ok
    )
    # not OK (invalid code)
    with pytest.raises(ValueError):
        AuditDetails(
            system_id="example_hospital_ehr",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "524", "initial")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            terminology_service=ts_ok
        )
    # not OK (empty ts)
    with pytest.raises(ValueError):
        AuditDetails(
            system_id="example_hospital_ehr",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "524", "initial")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            terminology_service=ts_empty
        )

def test_attestation_items_valid():
    # OK (non-empty items)
    Attestation(
        system_id="example_hospital_ehr",
        time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
        change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
        committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
        reason=DVText("signing prescription"),
        is_pending=False,
        terminology_service=ts_ok,
        items=[DVEHRUri("ehr:tasks/380daa09-028f-4beb-9803-4aef91644c2a")]
    )
    # not OK (empty items list)
    with pytest.raises(ValueError):
        Attestation(
            system_id="example_hospital_ehr",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            reason=DVText("signing prescription"),
            is_pending=False,
            terminology_service=ts_ok,
            items=[]
        )

def test_attestation_reason_valid():
    # OK (non-coded text for reason)
    Attestation(
        system_id="example_hospital_ehr",
        time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
        change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
        committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
        reason=DVText("signed prescription"),
        is_pending=False,
        terminology_service=ts_ok
    )
    # OK (coded text for reason, valid code)
    Attestation(
        system_id="example_hospital_ehr",
        time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
        change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
        committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
        reason=DVCodedText("signed prescription", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "240", "signed")),
        is_pending=False,
        terminology_service=ts_ok
    )
    # not OK (coded text for reason, wrong terminology)
    with pytest.raises(ValueError):
        Attestation(
            system_id="example_hospital_ehr",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            reason=DVCodedText("signed advance decision to refuse treatment", CodePhrase(TerminologyID("SNOMED-CT"), "711281000000107", "Advance decision to refuse treatment signed")),
            is_pending=False,
            terminology_service=ts_ok
        )
    # not OK (empty TS)
    with pytest.raises(ValueError):
        Attestation(
            system_id="example_hospital_ehr",
            time_committed=DVDateTime("2025-09-21T15:58:02.128Z"),
            change_type=DVCodedText("attestation", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "666", "attestation")),
            committer=PartyIdentified(external_ref=PartyRef("local_active_directory", "PERSON", ObjectID("TU999"))),
            reason=DVCodedText("signed prescription", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "240", "signed")),
            is_pending=False,
            terminology_service=ts_empty
        )

valid_rh_example = RevisionHistory([
        RevisionHistoryItem(
            version_id=ObjectVersionID("1d34aa7a-9e2c-49ff-a539-53c926107df6::ehr.example.net::1"),
            audits=[
                AuditDetails(
                    system_id="ehr.example.net",
                    time_committed=DVDateTime("2025-09-21T18:20:00Z"),
                    change_type=DVCodedText("created initial draft", CodePhrase(TerminologyID("openehr"), "249", "creation")),
                    committer=PartyIdentified(name="Dr A General-Practitioner"),
                    terminology_service=ts_ok
                    ),
                Attestation(
                    system_id="ehr.example.net",
                    time_committed=DVDateTime("2025-09-21T18:22:00Z"),
                    change_type=DVCodedText("signed DNACPR section", CodePhrase(TerminologyID("openehr"), "666", "attestation")),
                    committer=PartyIdentified(name="Dr A General-Practitioner"),
                    reason=DVCodedText("signed", CodePhrase(TerminologyID("openehr"), "240", "signed")),
                    is_pending=False,
                    terminology_service=ts_ok
                )
            ]),
        RevisionHistoryItem(
            version_id=ObjectVersionID("1d34aa7a-9e2c-49ff-a539-53c926107df6::ehr.example.net::2"),
            audits=[
                AuditDetails(
                    system_id="ehr.example.net",
                    time_committed=DVDateTime("2025-09-21T18:32:00Z"),
                    change_type=DVCodedText("amended preferred name", CodePhrase(TerminologyID("openehr"), "250", "amendment")),
                    committer=PartyIdentified(name="Ms C Test"),
                    terminology_service=ts_ok
                )
            ]
        )
    ])

def test_revision_history_most_recent_version():
    assert valid_rh_example.most_recent_version() == "1d34aa7a-9e2c-49ff-a539-53c926107df6::ehr.example.net::2"

def test_revision_history_most_recent_version_time_committed():
    assert valid_rh_example.most_recent_version_time_committed() == "2025-09-21T18:32:00Z"