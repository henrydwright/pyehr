from xmlschema import XMLSchema

import xml.etree.ElementTree as ET

from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.xml import IXMLSupport
from pyehr.core.rm.data_types.text import CodePhrase

def get_single_element_schema(schema_path: str, data_type: str):
    # this generates a single element schema to allow us to test a single element at a time
    return f"""<?xml version="1.0" encoding="utf-8"?>
       <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns="http://schemas.openehr.org/v1" targetNamespace="http://schemas.openehr.org/v1" elementFormDefault="qualified"
           id="AllTypes.xsd" version="v1.0.2">
	       <xs:include schemaLocation="{schema_path}"/>
	       <xs:element name="{data_type.lower()}" type="{data_type}"/>
       </xs:schema>"""

def validate(obj: IXMLSupport, schema_path: str, data_type: str):
    _schema = XMLSchema(get_single_element_schema(schema_path, data_type), base_url=f"test/pyehr/core/its/schemas/xml/")
    
    # check produced version against schema
    xml_obj = obj.as_xml()
    xml_obj.attrib["xmlns"] = "http://schemas.openehr.org/v1"
    _schema.validate(ET.tostring(xml_obj))

def check_from_xml(obj: IXMLSupport, cls):
    obj_there_and_back : AnyClass = cls.from_xml(obj.as_xml(root_tag="example"))
    assert obj_there_and_back.is_equal(obj) == True

# as_xml methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-XML/Release-2.0.0

# THIS FILE SHOULD ONLY BE USED TO TEST INDIVIDUAL CLASSES, NOT "PROPER" SCHEMAS FOR FULL DOCUMENTS

# ========
# RM.DataTypes.xsd - https://specifications.openehr.org/releases/ITS-XML/Release-2.0.0/components/RM/latest/DataTypes.xsd

# DV_BOOLEAN

# DV_IDENTIFIER

# DV_STATE

# DV_INTERVAL

# REFERENCE_RANGE

# DV_QUANTIFIED

# DV_COUNT

# DV_QUANTITY

# DV_ORDINAL

# DV_SCALE

# PROPORTION_KIND

# DV_PROPORTION

# DV_PARAGRAPH

# DV_TEXT

# DV_CODED_TEXT

def test_its_xml_rm_data_type_code_phrase():
    cd_phrse = CodePhrase(TerminologyID("SNOMED-CT"), "1069221000000106")

    validate(cd_phrse, "BaseTypes.xsd", "CODE_PHRASE")
    check_from_xml(cd_phrse, CodePhrase)

# TERM_MAPPING

# DV_DATE_TIME

# DV_TIME

# DV_DATE

# DV_DURATION

# DV_PERIODIC_TIME_SPECIFICATION

# DV_GENERAL_TIME_SPECIFICATION

# DV_MULTIMEDIA

# DV_PARSABLE

# DV_URI

# DV_EHR_URI