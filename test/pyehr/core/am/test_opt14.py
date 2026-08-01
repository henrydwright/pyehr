from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.its.json_tools import decode_json
from pyehr.core.its.xml_tools import decode_xml
import pytest

@pytest.fixture(scope="module")
def conformance_xml_str():
    with open("./test/pyehr/endtoend/TEMPLATE_conformance.xml") as f:
        xml_str = f.read()

    return xml_str

def test_conformance_xml_loads(conformance_xml_str):
    opt : OperationalTemplate = decode_xml(conformance_xml_str)

def test_conformance_xml_as_json_decode_json_works(conformance_xml_str):
    # regression for #100 - decode_json does not work for opt classes
    opt : OperationalTemplate = decode_xml(conformance_xml_str)

    opt_js = opt.as_json()

    opt2 = decode_json(opt_js)

    assert opt.is_equal(opt2)