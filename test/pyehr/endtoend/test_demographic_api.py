from pyehr.client.demographic import OpenEHRDemographicRestClient, OpenEHRPartyType
from pyehr.client.ehr import OpenEHREHRRestClient
from pyehr.core.base.base_types.identification import ArchetypeID, GenericID, HierObjectID, ObjectRef, ObjectVersionID, PartyRef, TerminologyID

from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.rest.additions import UpdateAudit, UpdateVersion
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.directory import Folder
from pyehr.core.rm.composition import Composition
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDate
from pyehr.core.rm.data_types.text import CodePhrase, DVText
from pyehr.core.rm.demographic import Address, Contact, Organisation, PartyIdentity, Person
from pyehr.core.rm.ehr import EHRStatus
from pyehr.core.rm.common.generic import DVCodedText, PartyIdentified, PartySelf
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState

import pytest
import os
import time

import threading

from flask.testing import FlaskClient

from pyehr.server.apps.rest import create_app

DEFINED_PERSON_UID = HierObjectID("d8c0810c-1071-4fd8-b588-36405d09b209")
SYSTEM_ID = "test.system"

DEFINED_CONTRIBUTION_ID = HierObjectID("9866c697-6c41-49d1-86e8-5ba0b791f948")

@pytest.fixture(scope="module")
def app():
    old_val = os.environ.get("PYEHR_REST_CONFIG")
    os.environ["PYEHR_REST_CONFIG"] = f"{os.getcwd()}/test/pyehr/endtoend/test_config/config.cfg"

    app = create_app()

    test_server = threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 8082}, daemon=True)
    test_server.start()
    time.sleep(1.0)

    yield app

    if old_val is not None:
        os.environ["PYEHR_REST_CONFIG"] = old_val
    else:
        del os.environ["PYEHR_REST_CONFIG"]

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def cdem(app):
    return OpenEHRDemographicRestClient("http://127.0.0.1:8082", False, False)

def test_000_create_person(cdem):
    p1_result = cdem.party.create_party(
        OpenEHRPartyType.PERSON,
        Person(
            actor_type=DVText("Patient"),
            archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_patient.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_patient.v0"), "1.1.0"),
            identities=[
                PartyIdentity(
                    purpose=DVText("NHS Identity"),
                    archetype_node_id="at0001",
                    details=ItemSingle(
                        name=DVText("INTERNAL"),
                        archetype_node_id="at0002",
                        item=Element(
                            name=DVText("NHS Number"),
                            archetype_node_id="at0003",
                            value=DVIdentifier("999999999", "NHS Digital", "NHS Digital", "NHS Number")
                        )
                    )
                )
            ],
            uid=DEFINED_PERSON_UID
        ),
        version_lifecycle_state=VersionLifecycleState.INCOMPLETE,
        version_audit_description="Create test patient"
    )

    assert p1_result.inner_response.status_code == 201

def test_005_get_person(cdem):
    result = cdem.party.get_party(OpenEHRPartyType.PERSON, DEFINED_PERSON_UID)

    assert result.inner_response.status_code == 200

def test_010_update_person(cdem):
    preciding_vid = ObjectVersionID(f"{DEFINED_PERSON_UID.value}::{SYSTEM_ID}::1")
    p2_result = cdem.party.update_party(
        OpenEHRPartyType.PERSON,
        DEFINED_PERSON_UID, 
        preciding_vid, 
        new_party=Person(
            actor_type=DVText("Patient"),
            archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_patient.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_patient.v0"), "1.1.0"),
            identities=[
                PartyIdentity(
                    purpose=DVText("NHS Identity"),
                    archetype_node_id="at0001",
                    details=ItemSingle(
                        name=DVText("INTERNAL"),
                        archetype_node_id="at0002",
                        item=Element(
                            name=DVText("NHS Number"),
                            archetype_node_id="at0003",
                            value=DVIdentifier("999999999", "NHS England", "NHS England", "NHS Number")
                        )
                    )
                )
            ],
            uid=DEFINED_PERSON_UID
        ),
        version_committer=PartyIdentified(name="ANOTHER LOGGED IN USER"),
        version_audit_description="Bulk change identifier issuer for NHS Number from NHS England to NHS Digital",
        version_lifecycle_state=VersionLifecycleState.COMPLETE,
        version_audit_change_type=AuditChangeType.MODIFICATION)

    assert p2_result.inner_response.status_code == 200

def test_015_get_versioned_party_version_at_time(cdem):
    resp = cdem.versioned_party.get_versioned_party_version_at_time(DEFINED_PERSON_UID)

    assert resp.inner_response.status_code == 200

def test_020_get_versioned_party_version_by_id(cdem):
    resp = cdem.versioned_party.get_versioned_party_version_by_id(DEFINED_PERSON_UID, ObjectVersionID(f"{DEFINED_PERSON_UID.value}::{SYSTEM_ID}::1"))

    assert resp.inner_response.status_code == 200

def test_025_delete_party(cdem):
    resp = cdem.party.delete_party(OpenEHRPartyType.PERSON, ObjectVersionID(f"{DEFINED_PERSON_UID.value}::{SYSTEM_ID}::2"), version_audit_description="Deleted after test script completed")

    assert resp.inner_response.status_code == 204

    resp = cdem.versioned_party.get_versioned_party_version_at_time(DEFINED_PERSON_UID)

    assert resp.inner_response.status_code == 200

    resp = cdem.party.get_party(OpenEHRPartyType.PERSON, DEFINED_PERSON_UID)

    assert resp.inner_response.status_code == 204

def test_030_commit_contribution_set(cdem):
    org1 = Organisation(
        actor_type=DVText("PRESCRIBING COST CENTRE"),
        archetype_node_id="openEHR-demographic-ORGANISATION.nhs_organisation.v0",
        archetype_details=Archetyped(
            archetype_id=ArchetypeID("openEHR-demographic-ORGANISATION.nhs_organisation.v0"),
            rm_version="1.1.0"
        ),
        identities=[
            PartyIdentity(
                purpose=DVText("ODS"),
                archetype_node_id="at0001",
                details=ItemSingle(
                    name=DVText("@ internal @"),
                    archetype_node_id="at0002",
                    item=Element(
                        name=DVText("ODS Code"),
                        archetype_node_id="at0003",
                        value=DVIdentifier(id="K81605", id_type="nhs_ods")
                    )
                )
            )
        ],
        contacts=[
            Contact(
                purpose=DVText("official"),
                archetype_node_id="at0201",
                addresses=[
                    Address(
                        addr_type=DVText("postal"),
                        archetype_node_id="at0202",
                        details=ItemTree(
                            name=DVText("address"),
                            archetype_node_id="at0203",
                            items=[
                                Element(
                                    name=DVText("line"),
                                    archetype_node_id="at0204",
                                    value=DVText("UNIVERSITY HEALTH CENTRE\n 9-11 NORTHCOURT AVENUE")
                                ),
                                Element(
                                    name=DVText("city"),
                                    archetype_node_id="at0205",
                                    value=DVText("READING")
                                ),
                                Element(
                                    name=DVText("postalCode"),
                                    archetype_node_id="at0206",
                                    value=DVText("RG2 7HE")
                                )
                            ]
                        )
                    )
                ]
            )
        ],
        details=ItemTree(
            name=DVText("@ internal @"),
            archetype_node_id="at0101",
            items=[
                Element(
                    name=DVText("operational start date"),
                    archetype_node_id="at0102",
                    value=DVDate("1974-04-01")
                ),
                Element(
                    name=DVText("commissioner"),
                    archetype_node_id="at0103",
                    value=DVIdentifier("15A", id_type="nhs_ods")
                )
            ]
        )
    )

    org2 = Organisation(
        actor_type=DVText("NHS TRUST"),
        archetype_node_id="openEHR-demographic-ORGANISATION.nhs_organisation.v0",
        archetype_details=Archetyped(
            archetype_id=ArchetypeID("openEHR-demographic-ORGANISATION.nhs_organisation.v0"),
            rm_version="1.1.0"
        ),
        identities=[
            PartyIdentity(
                purpose=DVText("ODS"),
                archetype_node_id="at0001",
                details=ItemSingle(
                    name=DVText("@ internal @"),
                    archetype_node_id="at0002",
                    item=Element(
                        name=DVText("ODS Code"),
                        archetype_node_id="at0003",
                        value=DVIdentifier(id="RHW", id_type="nhs_ods")
                    )
                )
            )
        ],
        contacts=[
            Contact(
                purpose=DVText("official"),
                archetype_node_id="at0201",
                addresses=[
                    Address(
                        addr_type=DVText("postal"),
                        archetype_node_id="at0202",
                        details=ItemTree(
                            name=DVText("address"),
                            archetype_node_id="at0203",
                            items=[
                                Element(
                                    name=DVText("line"),
                                    archetype_node_id="at0204",
                                    value=DVText("ROYAL BERKSHIRE HOSPITAL, LONDON ROAD")
                                ),
                                Element(
                                    name=DVText("city"),
                                    archetype_node_id="at0205",
                                    value=DVText("READING")
                                ),
                                Element(
                                    name=DVText("postalCode"),
                                    archetype_node_id="at0206",
                                    value=DVText("RG1 5AN")
                                )
                            ]
                        )
                    )
                ]
            )
        ],
        details=ItemTree(
            name=DVText("@ internal @"),
            archetype_node_id="at0101",
            items=[
                Element(
                    name=DVText("operational start date"),
                    archetype_node_id="at0102",
                    value=DVDate("1993-04-01")
                ),
                Element(
                    name=DVText("higher health geography"),
                    archetype_node_id="at0103",
                    value=DVIdentifier("QU9", id_type="nhs_ods")
                )
            ]
        )
    )

    aud = UpdateAudit(
        change_type=AuditChangeType.CREATION.value,
        committer=PartySelf(),
        description=DVText("uploaded several organisations")
    )

    result_c = cdem.contribution.commit_contribution_set(
        versions=[
            UpdateVersion(
                commit_audit=aud,
                lifecycle_state=VersionLifecycleState.COMPLETE.value,
                data=org1
            ),
            UpdateVersion(
                commit_audit=aud,
                lifecycle_state=VersionLifecycleState.COMPLETE.value,
                data=org2
            )
        ],
        audit=aud,
        uid=DEFINED_CONTRIBUTION_ID
    )

    assert result_c.inner_response.status_code == 201

def test_035_get_contribution_by_id(cdem):
    resp = cdem.contribution.get_contribution_by_id(DEFINED_CONTRIBUTION_ID)

    assert resp.inner_response.status_code == 200