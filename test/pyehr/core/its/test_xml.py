import numpy as np
from xmlschema import XMLSchema

import xml.etree.ElementTree as ET

from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CSingleAttribute
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Cardinality, Interval, MultiplicityInterval, PointInterval, ProperInterval
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
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
    xml_obj = obj.as_xml(data_type.lower())
    xml_obj.attrib["xmlns"] = "http://schemas.openehr.org/v1"
    _schema.validate(ET.tostring(xml_obj))

def check_from_xml(obj: IXMLSupport, cls):
    print(obj.as_json())
    print("\n")
    obj_there = obj.as_xml(root_tag="example")
    obj_there_and_back : AnyClass = cls.from_xml(obj_there)
    print(obj_there_and_back.as_json())
    assert obj_there_and_back.is_equal(obj) == True

# as_xml methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-XML/Release-2.0.0

# THIS FILE SHOULD ONLY BE USED TO TEST INDIVIDUAL CLASSES, NOT "PROPER" SCHEMAS FOR FULL DOCUMENTS

# ========
# BaseTypes - https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/BaseTypes.xsd

# Interval
def test_its_xml_basetypes_interval():
    int1 = PointInterval(1)

    validate(int1, "BaseTypes.xsd", "IntervalOfInteger")
    int1_there_and_back = Interval.from_xml(int1.as_xml(), int)
    assert int1.is_equal(int1_there_and_back)

    int2 = ProperInterval(0.5, 1.5, lower_included=True)
    validate(int2, "BaseTypes.xsd", "IntervalOfReal")
    int2_there_and_back = Interval.from_xml(int2.as_xml(), float)
    assert int2.is_equal(int2_there_and_back)

    int3 = PointInterval(ISODate("2026-03-01"))
    validate(int3, "BaseTypes.xsd", "IntervalOfDate")
    int3_there_and_back = Interval.from_xml(int3.as_xml(), ISODate)
    assert int3.is_equal(int3_there_and_back)

    int4 = PointInterval(ISODateTime("20251231T235959"))
    validate(int4, "BaseTypes.xsd", "IntervalOfDateTime")
    int4_there_and_back = Interval.from_xml(int4.as_xml(), ISODateTime)
    assert int4.is_equal(int4_there_and_back)

    int5 = ProperInterval(ISOTime("09:00:00"), ISOTime("17:00:00"), lower_included=True, upper_included=True)
    validate(int5, "BaseTypes.xsd", "IntervalOfTime")
    int5_there_and_back = Interval.from_xml(int5.as_xml(), ISOTime)
    assert int5.is_equal(int5_there_and_back)

    int6 = ProperInterval(ISODuration("PT1H"), ISODuration("PT2H"))
    validate(int6, "BaseTypes.xsd", "IntervalOfDuration")
    int6_there_and_back = Interval.from_xml(int6.as_xml(), ISODuration)
    assert int6.is_equal(int6_there_and_back)


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

def test_its_xml_basetypes_code_phrase():
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

# =========
# Archetype - https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/Archetype.xsd

def test_its_xml_archetype_c_single_attribute():
    csa = CSingleAttribute(
        "value", 
        ProperInterval(np.int32(0), np.int32(1), lower_included=True, upper_included=True),
        children=[
            CComplexObject("DV_DATE_TIME", PointInterval(np.int32(1)), "")
        ])
    validate(csa, "Archetype.xsd", "C_SINGLE_ATTRIBUTE")
    check_from_xml(csa, CSingleAttribute)

def test_its_xml_archetype_c_multiple_attribute():
    cma = CMultipleAttribute(
        "items",
        PointInterval(np.int32(1)),
        Cardinality(False, False, ProperInterval(lower=np.int32(1), lower_included=True)),
        children=[
            CComplexObject("ELEMENT", ProperInterval(lower=np.int32(0), lower_included=True), "at0001"),
            CComplexObject("ELEMENT", PointInterval(np.int32(1)), "at0002")
        ]
    )
    validate(cma, "Archetype.xsd", "C_MULTIPLE_ATTRIBUTE")
    check_from_xml(cma, CMultipleAttribute)

def test_its_xml_archetype_cardinality():
    card = Cardinality(True, False, MultiplicityInterval(np.int32(1)))
    validate(card, "Archetype.xsd", "CARDINALITY")
    check_from_xml(card, Cardinality)

def test_its_xml_archetype_c_complex_object():
    cco1 = CComplexObject("DV_DATE_TIME", PointInterval(np.int32(1)), "")
    validate(cco1, "Archetype.xsd", "C_COMPLEX_OBJECT")
    check_from_xml(cco1, CComplexObject)
    
    cco2 = CComplexObject("ELEMENT", 
                          ProperInterval(lower=np.int32(0), upper=np.int32(1), lower_included=True, upper_included=True),
                          "at0004",
                          attributes=[
                              CSingleAttribute("value", ProperInterval(np.int32(0), np.int32(1), lower_included=True, upper_included=True))
                          ])
    validate(cco2, "Archetype.xsd", "C_COMPLEX_OBJECT")
    check_from_xml(cco2, CComplexObject)
    
    
# C_PRIMITIVE_OBJECT

# ARCHETYPE_SLOT

# ARCHETYPE_INTERNAL_REF

# CONSTRAINT_REF

