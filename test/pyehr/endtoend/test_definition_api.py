from pyehr.client.definition import OpenEHRDefinitionRestClient
from pyehr.client.demographic import OpenEHRDemographicRestClient

from pyehr.client.exceptions import OpenEHRRestObjectNotFoundError
from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.its.xml_tools import decode_xml
import pytest
import os
import time

import threading

from pyehr.server.apps.rest import create_app

@pytest.fixture(scope="module")
def app():
    old_val = os.environ.get("PYEHR_REST_CONFIG")
    os.environ["PYEHR_REST_CONFIG"] = f"{os.getcwd()}/test/pyehr/endtoend/test_config/config.cfg"

    app = create_app()

    test_server = threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 8081}, daemon=True)
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
def cdef(app):
    return OpenEHRDefinitionRestClient("http://127.0.0.1:8081", False, False)

def test_000_list_templates(cdef):
    resp = cdef.adl14_list_templates()
    assert resp.inner_response.status_code == 200

def test_005_get_template_template_not_found(cdef):
    resp = cdef.adl14_get_template("RIPPLE - Conformance Test template")

    assert resp.inner_response.status_code == 404

    cdef.raise_exceptions_on_failure = True
    with pytest.raises(OpenEHRRestObjectNotFoundError):
        resp = cdef.adl14_get_template("RIPPLE - Conformance Test template")

    cdef.raise_exceptions_on_failure = False

def test_010_upload_template(cdef):
    conformance_template_str = open("test/pyehr/endtoend/TEMPLATE_conformance.xml").read()
    conformance_template : OperationalTemplate = decode_xml(conformance_template_str)

    resp = cdef.adl14_upload_template(conformance_template)

    assert resp.inner_response.status_code == 201

def test_015_get_template(cdef):
    resp = cdef.adl14_get_template("RIPPLE - Conformance Test template")

    assert resp.inner_response.status_code == 200