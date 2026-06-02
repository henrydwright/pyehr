from uuid import UUID

import numpy as np
from pyehr.core.am.opt14 import TView, TViewConstraint
from pyehr.core.rm.data_types.basic import DVState
import pytest
from xmlschema import XMLSchema

import xml.etree.ElementTree as ET

from pyehr.core.am.aom14.archetype.assertion import Assertion, AssertionVariable, ExprBinaryOperator, ExprLeaf, ExprUnaryOperator, OperatorKind
from pyehr.core.am.aom14.archetype.constraint_model import AMNonTerminalState, AMStateMachine, AMTerminalState, AMTransition, CCodePhrase, CComplexObject, CDVOrdinal, CDVQuantity, CDVState, CMultipleAttribute, CQuantityItem, CSingleAttribute
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CBoolean, CDate, CDateTime, CDuration, CInteger, CReal, CString, CTime
from pyehr.core.am.aom14.archetype.ontology import ArchetypeTerm, TermBindingItem
from pyehr.core.base.base_types.definitions import ValidityKind
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

from pyehr.term import PyehrGlobalTerminologyService

test_ts = PyehrGlobalTerminologyService.get_global_terminology_service()

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

def test_its_xml_basetypes_dv_state():
    st = DVState(DVCodedText("prescription_fulfilled", CodePhrase("local", "prescription_fulfilled")), True)
    validate(st, "BaseTypes.xsd", "DV_STATE")
    check_from_xml(st, DVState)

def test_its_xml_basetypes_dv_interval():
    low = DVQuantity(97.5, "cm")
    high = DVQuantity(122.0, "cm")
    t_dvi = DVInterval(ProperInterval[DVQuantity](lower=low, upper=high, lower_included=True, upper_included=True))
    validate(t_dvi, "BaseTypes.xsd", "DV_INTERVAL")
    check_from_xml(t_dvi, DVInterval)

# REFERENCE_RANGE

# DV_QUANTIFIED

def test_its_xml_basetypes_dv_count():
    cnt = DVCount(5)

    validate(cnt, "BaseTypes.xsd", "DV_COUNT")
    check_from_xml(cnt, DVCount)

def test_its_xml_basetypes_dv_quantity():
    qty = DVQuantity(97.5, "cm", precision=np.int32(1))

    validate(qty, "BaseTypes.xsd", "DV_QUANTITY")
    check_from_xml(qty, DVQuantity)

def test_its_xml_basetypes_dv_ordinal():
    ordinal = DVOrdinal(2, DVCodedText("Moderate", CodePhrase(TerminologyID("local"), "at0001")))
    
    validate(ordinal, "BaseTypes.xsd", "DV_ORDINAL")
    check_from_xml(ordinal, DVOrdinal)

# PROPORTION_KIND

def test_its_xml_basetypes_dv_proportion():
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

def test_its_xml_basetypes_dv_date_time():
    dt = DVDateTime("20251231T143000")

    validate(dt, "BaseTypes.xsd", "DV_DATE_TIME")
    check_from_xml(dt, DVDateTime)

def test_its_xml_basetypes_dv_time():
    time = DVTime("14:30:00")

    validate(time, "BaseTypes.xsd", "DV_TIME")
    check_from_xml(time, DVTime)

def test_its_xml_basetypes_dv_date():    
    date = DVDate("2025-12-31")

    validate(date, "BaseTypes.xsd", "DV_DATE")
    check_from_xml(date, DVDate)

def test_its_xml_basetypes_dv_duration():    
    dur = DVDuration("P1DT2H30M")

    validate(dur, "BaseTypes.xsd", "DV_DURATION")
    check_from_xml(dur, DVDuration)

# DV_PERIODIC_TIME_SPECIFICATION

# DV_GENERAL_TIME_SPECIFICATION

# DV_MULTIMEDIA

# DV_PARSABLE

def test_its_xml_basetypes_dv_uri():
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

def test_its_xml_archetype_assertion():
    ass = Assertion(
        expression=ExprBinaryOperator(
            "Boolean",
            ExprLeaf(
                "String",
                "attribute",
                "archetype_id/value"
            ),
            OperatorKind.MATCHES,
            ExprLeaf(
                "C_STRING",
                "constraint",
                CString(pattern=".*")
            ),
        ),
        string_expression="archetype_id/value matches {/.*/}"
    )
    validate(ass, "Archetype.xsd", "ASSERTION")
    check_from_xml(ass, Assertion)

def test_its_xml_archetype_assertion_variable():
    av = AssertionVariable("a", "a_definition")
    validate(av, "Archetype.xsd", "ASSERTION_VARIABLE")
    check_from_xml(av, AssertionVariable)

def test_its_xml_archetype_expr_leaf():
    el = ExprLeaf("String", "attribute", "archetype_id/value")
    validate(el, "Archetype.xsd", "EXPR_LEAF")
    check_from_xml(el, ExprLeaf)

def test_its_xml_archetype_expr_unary_operator():
    euo = ExprUnaryOperator("Boolean", OperatorKind.NOT, ExprLeaf("Boolean", "constant", True))
    validate(euo, "Archetype.xsd", "EXPR_UNARY_OPERATOR")
    check_from_xml(euo, ExprUnaryOperator)

def test_its_xml_archetype_expr_binary_operator():
    ebo = ExprBinaryOperator("Boolean", 
                             ExprLeaf(
                                 type_var="String",
                                 reference_type="attribute",
                                 item="archetype_id/value"
                             ),
                             OperatorKind.MATCHES,
                             ExprLeaf(
                                 type_var="String",
                                 reference_type="constraint",
                                 item=CString(pattern="openEHR-EHR-CLUSTER\.health_event(-[a-zA-Z0-9_]+)*\.v0|openEHR-EHR-CLUSTER\.issue(-[a-zA-Z0-9_]+)*\.v0|openEHR-EHR-CLUSTER\.symptom_sign(-[a-zA-Z0-9_]+)*\.v2")
                             ))
    validate(ebo, "Archetype.xsd", "EXPR_BINARY_OPERATOR")
    check_from_xml(ebo, ExprBinaryOperator)

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

# C_PRIMITIVE

def test_its_xml_archetype_c_boolean():
    cbool = CBoolean(True, True, True)
    validate(cbool, "Archetype.xsd", "C_BOOLEAN")
    check_from_xml(cbool, CBoolean)

def test_its_xml_archetype_c_string():
    cstr = CString(False, None, ["alpha", "beta", "live"], "beta")
    validate(cstr, "Archetype.xsd", "C_STRING")
    check_from_xml(cstr, CString)

def test_its_xml_archetype_c_integer():
    cint = CInteger([np.int32(1), np.int32(2), np.int32(3)], None, np.int32(1))
    validate(cint, "Archetype.xsd", "C_INTEGER")
    check_from_xml(cint, CInteger)

def test_its_xml_archetype_c_real():
    cint = CReal([np.float32(1.0), np.float32(1.5), np.float32(4.25)], None, np.float32(4.25))
    validate(cint, "Archetype.xsd", "C_REAL")
    check_from_xml(cint, CReal)

def test_its_xml_archetype_c_date():
    cdat = CDate(ValidityKind.OPTIONAL, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, None, ISODate("2026-01-01"))
    validate(cdat, "Archetype.xsd", "C_DATE")
    check_from_xml(cdat, CDate)

def test_its_xml_archetype_c_date_time():
    c_dati = CDateTime(ValidityKind.OPTIONAL, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, ValidityKind.PROHIBITED, assumed_value=ISODateTime("1998"))
    validate(c_dati, "Archetype.xsd", "C_DATE_TIME")
    check_from_xml(c_dati, CDateTime)

def test_its_xml_archetype_c_time():
    ctim = CTime(ValidityKind.MANDATORY, ValidityKind.OPTIONAL, ValidityKind.PROHIBITED, None, ISOTime("09:00"))
    validate(ctim, "Archetype.xsd", "C_TIME")
    check_from_xml(ctim, CTime)

def test_its_xml_archetype_c_duration():
    cdur1 = CDuration(True, False, True, True, False, False, False)
    validate(cdur1, "Archetype.xsd", "C_DURATION")
    check_from_xml(cdur1, CDuration)
    
    cdur2 = CDuration(False, False, False, False, True, False, True)
    validate(cdur2, "Archetype.xsd", "C_DURATION")
    check_from_xml(cdur2, CDuration)

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

def test_its_xml_openehrprofile_c_code_phrase():
    t_cc = CCodePhrase(
        "CODE_PHRASE",
        PointInterval(np.int32(1)),
        "",
        assumed_value=CodePhrase("SNOMED_CT", "49872002"),
        code_list=["49872002", "84676004"]
    )
    validate(t_cc, "OpenehrProfile.xsd", "C_CODE_PHRASE")
    check_from_xml(t_cc, CCodePhrase)

def test_its_xml_openehrprofile_c_dv_ordinal():
    t_dvo = CDVOrdinal(
        rm_type_name="DV_ORDINAL",
        occurrences=PointInterval(np.int32(1)),
        node_id="",
        list_var=[
            DVOrdinal(
                value=0,
                symbol=DVCodedText("", defining_code=CodePhrase("local", "at0005"))
            )
        ]
    )

    validate(t_dvo, "OpenehrProfile.xsd", "C_DV_ORDINAL")
    check_from_xml(t_dvo, CDVOrdinal)

def test_its_xml_openehrprofile_c_dv_quantity():
    t_cdvq = CDVQuantity(
        rm_type_name="DV_QUANTITY",
        occurrences=PointInterval(np.int32(1)),
        node_id="",
        property_var=CodePhrase("openehr", "122"),
        list_var=[
            CQuantityItem(
                units="cm",
                magnitude=ProperInterval[np.float32](
                    lower=np.float32(0.0),
                    upper=np.float32(500.0),
                    lower_included=True,
                    upper_included=True
                )
            ),
            CQuantityItem(
                units="[in_i]",
                magnitude=ProperInterval[np.float32](
                    lower=np.float32(0.0),
                    upper=np.float32(250.0),
                    lower_included=True,
                    upper_included=True
                )
            )
        ]
    )

    validate(t_cdvq, "OpenehrProfile.xsd", "C_DV_QUANTITY")
    check_from_xml(t_cdvq, CDVQuantity)

def test_its_xml_openehrprofile_c_quantity_item():
    t_cqi = CQuantityItem("mm[Hg]", ProperInterval(np.float32(0.0), np.float32(1000.0), True, False), PointInterval(np.int32(0)))

    validate(t_cqi, "OpenehrProfile.xsd", "C_QUANTITY_ITEM")
    check_from_xml(t_cqi, CQuantityItem)

def test_its_xml_openehrprofile_c_dv_state():
    t_cdvs = CDVState(
        "DV_STATE",
        PointInterval(np.int32(1)),
        node_id="",
        value=AMStateMachine(
            states=[
                AMTerminalState("test_state")
            ]
        ),
        assumed_value=DVState(
            value=DVCodedText("test_state", CodePhrase("local", "test_state")),
            is_terminal=True
        )
    )

    validate(t_cdvs, "OpenehrProfile.xsd", "C_DV_STATE")
    check_from_xml(t_cdvs, CDVState)

def test_its_xml_openehrprofile_state_machine():
    t_sm = AMStateMachine(
        states=[
            AMTerminalState("test_state")
        ]
    )

def test_its_xml_openehrprofile_non_terminal_state():
    t_nts = AMNonTerminalState(
        name="prescription_drafted",
        transitions=[
            AMTransition(
                event="sign_prescription",
                action="sign",
                guard="check_authority",
                next_state=AMTerminalState("prescription_signed")
            )
        ])
    
    validate(t_nts, "OpenehrProfile.xsd", "NON_TERMINAL_STATE")
    check_from_xml(t_nts, AMNonTerminalState)

def test_its_xml_openehrprofile_terminal_state():
    t_ts = AMTerminalState("prescription_fulfilled")

    validate(t_ts, "OpenehrProfile.xsd", "TERMINAL_STATE")
    check_from_xml(t_ts, AMTerminalState)

def test_its_xml_openehrprofile_transition():
    t_t = AMTransition(
        event="prescribe",
        action="provide medication",
        guard="check prescription"
    )

    validate(t_t, "OpenehrProfile.xsd", "TRANSITION")
    check_from_xml(t_t, AMTransition)

# =============
# Template.xsd

# OPERATIONAL_TEMPLATE

# C_ARCHETYPE_ROOT

# FLAT_ARCHETYPE_ONTOLOGY

# ANNOTATION

def test_its_xml_template_t_view():
    t_v = TView(
        constraints=[
            TViewConstraint(
                path="[openEHR-EHR-COMPOSITION.prescription.v0]/content[openEHR-EHR-INSTRUCTION.medication_order.v0]/protocol[at0005]",
                items={"pass_through": True}
            )
        ]
    )

    validate(t_v, "Template.xsd", "T_VIEW")
    check_from_xml(t_v, TView)

# T_CONSTRAINT

# T_ATTRIBUTE

# T_COMPLEX_OBJECT

# C_CODE_REFERENCE