import json

from pyehr.client.definition import OpenEHRDefinitionRestClient
from pyehr.client.ehr import OpenEHREHRRestClient
from pyehr.client.exceptions import OpenEHRRestObjectAlreadyExistsError, OpenEHRRestObjectNotFoundError
from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.base.base_types.identification import ArchetypeID, GenericID, HierObjectID, ObjectRef, ObjectVersionID, PartyRef, TemplateID, TerminologyID

from pyehr.core.base.foundation_types.time import ISODateTime
from pyehr.core.its.json_tools import decode_json
from pyehr.core.its.rest.additions import UpdateAudit, UpdateVersion
from pyehr.core.its.xml_tools import decode_xml
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

@pytest.fixture(scope="module")
def app():
    old_val = os.environ.get("PYEHR_REST_CONFIG")
    os.environ["PYEHR_REST_CONFIG"] = f"{os.getcwd()}/test/pyehr/endtoend/test_config/config.cfg"

    app = create_app()

    test_server = threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 8084}, daemon=True)
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
def c(app):
    return OpenEHREHRRestClient("http://127.0.0.1:8084", False, False)

@pytest.fixture(scope="module")
def cdef(app):
    return OpenEHRDefinitionRestClient("http://127.0.0.1:8084", False, False)

@pytest.fixture(scope="module")
def test_state():
    return {
        "comp_id": None
    }

EHR_ID = HierObjectID("ada9ec92-aca5-4076-aa5b-5eade3eaedb8")

COMP_ID = ""

def test_000_check_then_upload_template(cdef):
    r = cdef.adl14_get_template("simple_template")
    assert r.pyehr_obj is None
    assert r.inner_response.status_code == 404

    if r.pyehr_obj is None:
        with open("test/pyehr/core/am/aom14/archetype/constraint_model/simpleTemplate.xml") as f:
            opt : OperationalTemplate = decode_xml(f.read())
            r = cdef.adl14_upload_template(opt)

            assert r.pyehr_obj.is_equal(opt)
            assert r.inner_response.status_code == 201

            r = cdef.adl14_get_template("simple_template")
            assert r.pyehr_obj.is_equal(opt)
            assert r.inner_response.status_code == 200

def test_001_constraint_fails_with_template_id(c):
    r = c.ehr.create_ehr_with_id(EHR_ID)

    assert r.pyehr_obj.ehr_id.is_equal(EHR_ID)
    assert r.inner_response.status_code == 201

    r = c.composition.create_composition(
        ehr_id=EHR_ID,
        new_composition=Composition(
            name=DVText("wrong comp"),
            archetype_node_id="at0000",
            language=CodePhrase("ISO_639-1", "en"),
            territory=CodePhrase("ISO_3166-1", "GB"),
            category=DVCodedText("event", defining_code=CodePhrase("openehr", "433")),
            composer=PartySelf(),
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.simple.v0"), "1.1.0", template_id=TemplateID("simple_template"))
        )
    )

    print(r.inner_response.text)
    assert r.inner_response.status_code == 422

def test_002_constraint_success_with_template_id(c, test_state):
    with open("test/pyehr/core/am/aom14/archetype/constraint_model/simpleTemplateInstance.json", "r") as f:
        comp : Composition= decode_json(json.loads(f.read()))
        r = c.composition.create_composition(
            ehr_id=EHR_ID,
            new_composition=comp
        )

        assert r.inner_response.status_code == 201

        comp.uid = r.pyehr_obj.uid
        test_state["comp_id"] = r.pyehr_obj.uid
        assert comp.is_equal(r.pyehr_obj)

def test_003_retrieve_and_update_composition(c, test_state):
    r = c.composition.get_composition(EHR_ID, test_state["comp_id"])

    assert r.inner_response.status_code == 200
    comp = r.pyehr_obj
    ver_id = ObjectVersionID(r.metadata.etag[3:-1])

    comp.category = DVCodedText("report", CodePhrase("openehr", "815"))

    r = c.composition.update_composition(EHR_ID, HierObjectID(ver_id.object_id().value), comp, ver_id)

    assert r.inner_response.status_code == 422

    comp.category = DVCodedText("event", CodePhrase("openehr", "433"))
    comp.composer = PartyIdentified(name="Dr T Test")

    r = c.composition.update_composition(EHR_ID, HierObjectID(ver_id.object_id().value), comp, ver_id)

    assert r.inner_response.status_code == 200

