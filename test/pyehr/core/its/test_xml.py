from uuid import UUID

import numpy as np
import pytest
from xmlschema import XMLSchema

import xml.etree.ElementTree as ET

from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CQuantityItem, CSingleAttribute
from pyehr.core.am.aom14.archetype.ontology import ArchetypeTerm, TermBindingItem
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectVersionID, TemplateID, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Cardinality, Interval, MultiplicityInterval, PointInterval, ProperInterval
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
from pyehr.core.base.resource import AuthoredResource, ResourceDescription, ResourceDescriptionItem
from pyehr.core.its.xml import IXMLSupport
from pyehr.core.rm.data_types.quantity import DVCount, DVInterval, DVOrdinal, DVProportion, DVQuantity, DVScale, ProportionKind
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime, DVDuration, DVTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, TermMapping
from pyehr.core.rm.data_types.uri import DVUri
from term import CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR, PythonTerminologyService

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

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
    obj_there_and_back : AnyClass = cls.from_xml(obj_there, term_svc=test_ts)
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

def test_its_xml_basetypes_archetype_id():
    aid = ArchetypeID("openEHR-EHR-INSTRUCTION.medication_order.v3")
    validate(aid, "BaseTypes.xsd", "ARCHETYPE_ID")
    check_from_xml(aid, ArchetypeID)

def test_its_xml_basetypes_template_id():
    tid = TemplateID("Glucose test result example")
    validate(tid, "BaseTypes.xsd", "TEMPLATE_ID")
    check_from_xml(tid, TemplateID)

def test_its_xml_basetypes_terminology_id():
    tid = TerminologyID("SNOMED-CT")
    validate(tid, "BaseTypes.xsd", "TERMINOLOGY_ID")
    check_from_xml(tid, TerminologyID)

def test_its_xml_basetypes_object_version_id():
    ovid = ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1")
    validate(ovid, "BaseTypes.xsd", "OBJECT_VERSION_ID")
    check_from_xml(ovid, ObjectVersionID)

def test_its_xml_basetypes_hier_object_id():
    hid = HierObjectID("93f49724-c066-40f5-aea0-5d0ff1184326::abacus")
    validate(hid, "BaseTypes.xsd", "HIER_OBJECT_ID")
    check_from_xml(hid, HierObjectID)

# DV_BOOLEAN

# DV_IDENTIFIER

# DV_STATE

def test_its_xml_basetypes_dv_interval():
    low = DVQuantity(97.5, "cm")
    high = DVQuantity(122.0, "cm")
    t_dvi = DVInterval(ProperInterval[DVQuantity](lower=low, upper=high, lower_included=True, upper_included=True))
    # XML schema validator has issues with the inheritance when validating this, so conciously skipped
    # validate(t_dvi, "BaseTypes.xsd", "DV_INTERVAL")
    check_from_xml(t_dvi, DVInterval)

# REFERENCE_RANGE

# DV_QUANTIFIED

def test_its_xml_datatypes_dv_count():
    cnt = DVCount(5)

    validate(cnt, "BaseTypes.xsd", "DV_COUNT")
    check_from_xml(cnt, DVCount)

def test_its_xml_datatypes_dv_quantity():
    qty = DVQuantity(97.5, "cm", precision=np.int32(1))

    validate(qty, "BaseTypes.xsd", "DV_QUANTITY")
    check_from_xml(qty, DVQuantity)

def test_its_xml_datatypes_dv_ordinal():
    ordinal = DVOrdinal(2, DVCodedText("Moderate", CodePhrase(TerminologyID("local"), "at0001")))
    
    validate(ordinal, "BaseTypes.xsd", "DV_ORDINAL")
    check_from_xml(ordinal, DVOrdinal)

# PROPORTION_KIND

def test_its_xml_datatypes_dv_proportion():
    prop = DVProportion(1.0, 128.0, ProportionKind.PK_RATIO)

    validate(prop, "BaseTypes.xsd", "DV_PROPORTION")
    check_from_xml(prop, DVProportion)

# DV_PARAGRAPH

# DV_TEXT

# DV_CODED_TEXT

def test_its_xml_basetypes_code_phrase():
    cd_phrse = CodePhrase(TerminologyID("SNOMED-CT"), "1069221000000106")

    validate(cd_phrse, "BaseTypes.xsd", "CODE_PHRASE")
    check_from_xml(cd_phrse, CodePhrase)

def test_its_xml_basetypes_term_mapping():
    tm = TermMapping('=', CodePhrase("SNOMED_CT", "260205009"))

    validate(tm, "BaseTypes.xsd", "TERM_MAPPING")
    check_from_xml(tm, TermMapping)

def test_its_xml_datatypes_dv_date_time():
    dt = DVDateTime("20251231T143000")

    validate(dt, "BaseTypes.xsd", "DV_DATE_TIME")
    check_from_xml(dt, DVDateTime)

def test_its_xml_datatypes_dv_time():
    time = DVTime("14:30:00")

    validate(time, "BaseTypes.xsd", "DV_TIME")
    check_from_xml(time, DVTime)

def test_its_xml_datatypes_dv_date():    
    date = DVDate("2025-12-31")

    validate(date, "BaseTypes.xsd", "DV_DATE")
    check_from_xml(date, DVDate)

def test_its_xml_datatypes_dv_duration():    
    dur = DVDuration("P1DT2H30M")

    validate(dur, "BaseTypes.xsd", "DV_DURATION")
    check_from_xml(dur, DVDuration)

# DV_PERIODIC_TIME_SPECIFICATION

# DV_GENERAL_TIME_SPECIFICATION

# DV_MULTIMEDIA

# DV_PARSABLE

def test_its_xml_datatypes_dv_uri():
    ur = DVUri("https://www.bbc.co.uk/news")

    validate(ur, "BaseTypes.xsd", "DV_URI")
    check_from_xml(ur, DVUri)

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

def test_its_xml_archetype_term():
    at = ArchetypeTerm("at0093", 
                       items={
                           "text": "01",
                           "description": "Cancelled for Clinical Reasons"
                           })
    validate(at, "Archetype.xsd", "ARCHETYPE_TERM")
    check_from_xml(at, ArchetypeTerm)

def test_its_xml_archetype_term_binding_item():
    tbi = TermBindingItem("at0001", CodePhrase("SNOMED-CT", "95883001"))
    validate(tbi, "Archetype.xsd", "TERM_BINDING_ITEM")
    check_from_xml(tbi, TermBindingItem)

# ===========
# Resource

def test_its_xml_resource_resource_description():
    t_rd = ResourceDescription(
        original_author={"Author name": "Joe Bloggs", "Organisation": "Anytown NHS Trust", "Email": "joe@example.net", "Date originally authored": "2017-11-30"},
        lifecycle_state=TerminologyCode("openehr", "532"),
        details={"en": ResourceDescriptionItem(
            language=TerminologyCode("ISO_639-1", "en"),
            purpose="Not Specified"
        )}
    )

    validate(t_rd, "Resource.xsd", "RESOURCE_DESCRIPTION")
    check_from_xml(t_rd, ResourceDescription)

# =========
# OpenehrProfile

# C_CODE_PHRASE

# C_DV_ORDINAL

# C_DV_QUANTITY

def test_its_xml_openehrprofile_c_quantity_item():
    t_cqi = CQuantityItem("mm[Hg]", ProperInterval(np.float32(0.0), np.float32(1000.0), True, False), PointInterval(np.int32(0)))

    # validator once again struggles with inheritance of types
    # validate(t_cqi, "OpenehrProfile.xsd", "C_QUANTITY_ITEM")
    check_from_xml(t_cqi, CQuantityItem)

# C_DV_STATE

# STATE_MACHINE

# NON_TERMINAL_STATE

# TERMINAL_STATE

# TRANSITION