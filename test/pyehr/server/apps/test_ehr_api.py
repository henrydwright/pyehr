from pyehr.client.ehr import OpenEHREHRRestClient
from pyehr.core.base.base_types.identification import ArchetypeID, GenericID, HierObjectID, ObjectRef, ObjectVersionID, PartyRef, TerminologyID

from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.rest.additions import UpdateAudit, UpdateVersion
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.directory import Folder
from pyehr.core.rm.composition import Composition
from pyehr.core.rm.data_types.text import CodePhrase, DVText
from pyehr.core.rm.ehr import EHRStatus
from pyehr.core.rm.common.generic import DVCodedText, PartyIdentified, PartySelf
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState

import pytest
import os
import time

import threading

from flask.testing import FlaskClient

from pyehr.server.apps.rest import create_app

DEFINED_EHR_ID = HierObjectID("a912f347-6ea1-4f1a-a39a-4d2596b8aa79")
DEFINED_EHR_STATUS_ID = HierObjectID("75d52140-989e-4099-a48f-f74f0d698da9")
SYSTEM_ID = "test.system"

DEFINED_CONTRIBUTION_ID = HierObjectID("09cb9c21-4987-4e4f-b75a-17962512634e")

@pytest.fixture(scope="module")
def app():
    old_val = os.environ.get("PYEHR_REST_CONFIG")
    os.environ["PYEHR_REST_CONFIG"] = f"{os.getcwd()}/test/pyehr/server/apps/test_config/config.cfg"

    app = create_app()

    test_server = threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 8080}, daemon=True)
    test_server.start()
    time.sleep(1.0)

    yield app

    os.environ["PYEHR_REST_CONFIG"] = old_val

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def c(app):
    return OpenEHREHRRestClient("http://127.0.0.1:8080", False, False)

def test_000_options(c):
    resp = c.options()
    assert resp.pyehr_obj["solution"] == "pyehr"
    assert "/" in resp.pyehr_obj["endpoints"]
    assert "/ehr" in resp.pyehr_obj["endpoints"]
    assert "/demographic" in resp.pyehr_obj["endpoints"]
    print(resp.pyehr_obj)

def test_005_get_ehr_by_id_doesnt_exist(c):
    resp = c.ehr.get_ehr_by_id(DEFINED_EHR_ID)
    assert resp.inner_response.status_code == 404
    assert resp.inner_response.json()["error"] == f"404 Not Found: No EHR exists with id '{DEFINED_EHR_ID.value}'"

def test_010_create_ehr_with_id_works_first_time_fails_on_conflict(c):
    sub = PartySelf(PartyRef("nhs_pds", "PERSON", GenericID("9449306583", "nhs_number")))
    resp1 = c.ehr.create_ehr_with_id(ehr_id=DEFINED_EHR_ID, 
                                  ehr_status=EHRStatus(
                                      name=DVText("EHR status (with nhs number)"),
                                      archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
                                      subject=sub,
                                      is_queryable=True,
                                      is_modifiable=True,
                                      archetype_details=Archetyped(
                                            archetype_id=ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"),
                                            rm_version="1.1.0"
                                        ),
                                      uid=DEFINED_EHR_STATUS_ID
                                  ))
    assert resp1.inner_response.status_code == 201

    resp2 = c.ehr.create_ehr_with_id(ehr_id=DEFINED_EHR_ID, 
                                  ehr_status=EHRStatus(
                                      name=DVText("EHR status (with nhs number)"),
                                      archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
                                      subject=sub,
                                      is_queryable=True,
                                      is_modifiable=True,
                                      archetype_details=Archetyped(
                                            archetype_id=ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"),
                                            rm_version="1.1.0"
                                        ),
                                      uid=DEFINED_EHR_STATUS_ID
                                  ))
    assert resp2.inner_response.status_code == 409

def test_015_get_ehr_by_id_does_exist(c):
    resp = c.ehr.get_ehr_by_id(DEFINED_EHR_ID)
    assert resp.inner_response.status_code == 200
    assert resp.pyehr_obj.ehr_id.is_equal(DEFINED_EHR_ID)

def test_020_get_ehr_status_by_version_id_version_exists(c):
    resp = c.ehr_status.get_ehr_status_by_version_id(DEFINED_EHR_ID, ObjectVersionID(f"{DEFINED_EHR_STATUS_ID.value}::{SYSTEM_ID}::1"))
    assert resp.inner_response.status_code == 200
    assert resp.pyehr_obj.subject.external_ref.id.value == "9449306583"

def test_025_get_ehr_status_at_time_no_time_provided(c):
    resp = c.ehr_status.get_ehr_status_at_time(DEFINED_EHR_ID)
    assert resp.inner_response.status_code == 200
    assert resp.pyehr_obj.subject.external_ref.id.value == "9449306583"

def test_030_get_ehr_status_at_time_in_future(c):
    resp = c.ehr_status.get_ehr_status_at_time(DEFINED_EHR_ID, ISODateTime("20261201T200000Z"))
    assert resp.inner_response.status_code == 200

def test_035_update_ehr_status(c):
    latest_ehr_status = c.ehr_status.get_ehr_status_at_time(DEFINED_EHR_ID)
    new_ehr_status : EHRStatus = latest_ehr_status.pyehr_obj
    new_ehr_status.is_queryable = not new_ehr_status.is_queryable
    preceding_version_uid = ObjectVersionID(latest_ehr_status.metadata.etag.replace("\"", "").replace("W/", ""))
    new_ehr_status.uid = None
    resp = c.ehr_status.update_ehr_status(DEFINED_EHR_ID, preceding_version_uid, new_ehr_status)

    assert resp.inner_response.status_code == 200
    assert resp.pyehr_obj.is_queryable == False

def test_040_update_ehr_status_fails_when_preciding_version_invalid(c):
    latest_ehr_status = c.ehr_status.get_ehr_status_at_time(DEFINED_EHR_ID)
    new_ehr_status : EHRStatus = latest_ehr_status.pyehr_obj
    new_ehr_status.is_queryable = not new_ehr_status.is_queryable
    new_ehr_status.uid = None
    resp = c.ehr_status.update_ehr_status(DEFINED_EHR_ID, ObjectVersionID("75d52140-989e-4099-a48f-f74f0d698da9::local.ehrbase.org::1"), new_ehr_status)

    assert resp.inner_response.status_code == 412

def test_045_get_versioned_ehr_status(c):
    resp = c.ehr_status.get_versioned_ehr_status(DEFINED_EHR_ID)

    assert resp.inner_response.status_code == 200

def test_050_get_versioned_ehr_status_revision_history(c):
    resp = c.ehr_status.get_versioned_ehr_status_revision_history(DEFINED_EHR_ID)

    assert resp.inner_response.status_code == 200

def test_055_get_versioned_ehr_status_version_by_id(c):
    resp = c.ehr_status.get_versioned_ehr_status_version_by_id(DEFINED_EHR_ID, ObjectVersionID(f"{DEFINED_EHR_STATUS_ID.value}::{SYSTEM_ID}::1"))

    assert resp.inner_response.status_code == 200

def test_060_get_versioned_ehr_status_version_at_time(c):
    resp = c.ehr_status.get_versioned_ehr_status_version_at_time(DEFINED_EHR_ID)

    assert resp.inner_response.status_code == 200

def test_065_create_composition_and_retrieve_and_update_and_versioned_methods(c):
    resp = c.composition.create_composition(
        ehr_id=DEFINED_EHR_ID,
        new_composition=Composition(
            name=DVText("GP appointment - 29th Dec 2025"),
            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
            territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
            category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
            composer=PartyIdentified(name="Dr Test General-Practitioner"),
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0")
        )
    )

    assert resp.inner_response.status_code == 201

    res_comp : Composition = resp.pyehr_obj
    ovid = ObjectVersionID(res_comp.uid.value)

    resp = c.composition.get_composition(DEFINED_EHR_ID, ovid)

    assert resp.inner_response.status_code == 200

    resp = c.composition.update_composition(DEFINED_EHR_ID, 
                                          HierObjectID(ovid.object_id().value),
                                          new_composition=Composition(
                                            name=DVText("GP appointment - 29th Dec 2025 (corrected)"),
                                            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
                                            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
                                            territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
                                            category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
                                            composer=PartyIdentified(name="Dr Maureen Example"),
                                            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0")
                                        ),
                                        preceding_version_uid=ovid,
                                        version_audit_change_type=AuditChangeType.AMENDMENT,
                                        version_audit_description="Corrected practitioner seen")

    assert resp.inner_response.status_code == 200

    result = c.composition.get_versioned_composition(DEFINED_EHR_ID, HierObjectID(ovid.object_id().value))
    assert resp.inner_response.status_code == 200

    result = c.composition.get_versioned_composition_revision_history(DEFINED_EHR_ID, HierObjectID(ovid.object_id().value))
    assert resp.inner_response.status_code == 200

    result = c.composition.get_versioned_composition_version_at_time(DEFINED_EHR_ID, HierObjectID(ovid.object_id().value))
    assert resp.inner_response.status_code == 200

    result = c.composition.get_versioned_composition_version_by_id(DEFINED_EHR_ID, HierObjectID(ovid.object_id().value), ovid)
    assert resp.inner_response.status_code == 200

def test_070_commit_contribution_set_and_get_by_id(c):
    comp1 = Composition(
        name=DVText("GP appointment - 29th Dec 2025 (corrected again)"),
        archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
        category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
        composer=PartyIdentified(name="Dr Test Generally-Praciting"),
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0")
    )

    comp2 = Composition(
        name=DVText("ED attendance"),
        archetype_node_id="openEHR-EHR-COMPOSITION.ed_attendance.v0",
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
        category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
        composer=PartyIdentified(name="Dr Important Consultant"),
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.ed_attendance.v0"), "1.1.0")
    )

    cont_id = DEFINED_CONTRIBUTION_ID

    resp = c.contribution.commit_contribution_set(
        ehr_id=HierObjectID("a912f347-6ea1-4f1a-a39a-4d2596b8aa79"),
        versions=[
            UpdateVersion(
                commit_audit=UpdateAudit(
                    change_type=AuditChangeType.AMENDMENT.value,
                    committer=PartySelf(),
                    description=DVText("Correcting the GP that saw the patient again")
                ),
                lifecycle_state=VersionLifecycleState.COMPLETE.value,
                data=comp1,
            ),
            UpdateVersion(
                commit_audit=UpdateAudit(
                    change_type=AuditChangeType.CREATION.value,
                    committer=PartySelf(),
                    description=DVText("Adding recent ED attendance to record")
                ),
                lifecycle_state=VersionLifecycleState.COMPLETE.value,
                data=comp2
            )
        ],
        audit=UpdateAudit(
            change_type=AuditChangeType.CREATION.value,
            committer=PartySelf(),
            description=DVText("Added ED attendance and corrected GP appointment issue in record")
        ),
        uid=cont_id
    )

    assert resp.inner_response.status_code == 201

    resp = c.contribution.get_contribution_by_id(DEFINED_EHR_ID, cont_id)

    assert resp.inner_response.status_code == 200

def test_075_create_get_update_delete_directory(c):
    test_folder = Folder(
                        name=DVText("A&E amends"),
                        archetype_node_id="openEHR-EHR-FOLDER.generic.v1",
                        items=[
                            ObjectRef("local", "CONTRIBUTION", DEFINED_CONTRIBUTION_ID)
                        ],
                        folders=[
                            Folder(
                                uid=HierObjectID("f1ec0da4-2e4f-4d43-ba97-054ee86c5879"),
                                name=DVText("archived"),
                                archetype_node_id="at0001"
                            )
                        ]
                    )

    result = c.directory.create_directory(DEFINED_EHR_ID,
                                        new_folder=test_folder)
    assert result.inner_response.status_code == 201

    obj_id = ObjectVersionID(result.pyehr_obj.uid.value)

    result = c.directory.get_folder(DEFINED_EHR_ID, obj_id)

    assert result.inner_response.status_code == 200

    folder_ver_id = ObjectVersionID(result.pyehr_obj.uid.value)

    test_folder.folders[0].items = [ObjectRef("local", "CONTRIBUTION", HierObjectID("fd77b46a-958b-4ecd-8c02-e1e28297c574"))]
    result = c.directory.update_directory(DEFINED_EHR_ID,
                                        new_folder=test_folder,
                                        preceding_folder_version_uid=folder_ver_id)

    assert result.inner_response.status_code == 200

    folder_ver_id = ObjectVersionID(result.pyehr_obj.uid.value)

    result = c.directory.delete_directory(HierObjectID("a912f347-6ea1-4f1a-a39a-4d2596b8aa79"),
                                        folder_ver_id)

    assert result.inner_response.status_code == 204

def test_080_get_folder_in_directory_version_at_time_after_deleted(c):
    result = c.directory.get_folder_in_directory_version_at_time(DEFINED_EHR_ID, path="folders[at0001]")

    assert result.inner_response.status_code == 404

