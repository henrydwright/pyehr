import pytest
import json

import jsonschema
import numpy as np

from common import PythonTerminologyService, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR
from org.openehr.base.foundation_types.interval import PointInterval, ProperInterval, MultiplicityInterval
from org.openehr.base.base_types.identification import TerminologyID
from org.openehr.its.json_tools import OpenEHREncoder

from org.openehr.base.base_types.identification import TerminologyID, ISOOID, UUID, InternetID, VersionTreeID, HierObjectID, ObjectVersionID, ArchetypeID, TemplateID, GenericID, ObjectRef, PartyRef
from org.openehr.rm.data_types.text import DVText, DVUri, DVCodedText, CodePhrase, TermMapping, DVParagraph
from org.openehr.rm.data_types.basic import DVIdentifier, DVBoolean, DVState
from org.openehr.rm.data_types.uri import DVEHRUri
from org.openehr.rm.data_types.quantity import DVCount, DVQuantity, DVInterval, DVOrdinal, DVProportion, ProportionKind, DVScale, ReferenceRange
from org.openehr.rm.data_types.quantity.date_time import DVDate, DVTime, DVDuration, DVDateTime
from org.openehr.rm.data_types.encapsulated import DVParsable, DVMultimedia
from org.openehr.rm.data_types.time_specification import DVGeneralTimeSpecification, DVPeriodicTimeSpecification
from org.openehr.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

# as_json methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-JSON/development/components/

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

def validate(json_obj):
    _schema = json.loads(open("test/org/openehr/its/schemas/openehr_rm_1.1.0_alltypes_strict.json").read())
    # keep this as a separate method so we can switch to a different validator
    #  at a future date if we need to
    jsonschema.validate(json_obj, _schema)

# ==========
# FOUNDATION: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Foundation_types

def test_its_json_foundation_interval():
    pi_json = PointInterval[np.int32](np.int32(0)).as_json()
    validate(pi_json)

    pri_json = ProperInterval[str](lower="SMITH", lower_included=True).as_json()
    validate(pri_json)

    mi_json = MultiplicityInterval(lower=np.int32(0), upper=np.int32(1)).as_json()
    validate(mi_json)


# ==========
# BASE: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Base_types

def test_its_json_base_internet_id():
    ii_json = InternetID("org.example.ehr").as_json()

    validate(ii_json)

# TODO: ACCESS_GROUP_REF is in the JSON spec, but not in the actual base spec so treating
#  this as an issue to raise with spec

def test_its_json_base_object_ref():
    orf_json = ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")).as_json()

    validate(orf_json)

def test_its_json_base_party_ref():
    prf_json = PartyRef("local_active_directory", "PERSON", GenericID("TU999", "local")).as_json()

    validate(prf_json)

def test_its_json_base_template_id():
    tid_json = TemplateID("Glucose test result example").as_json()

    validate(tid_json)

def test_its_json_base_object_version_id():
    ovd_json = ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1").as_json()

    validate(ovd_json)

# VERSION_STATUS is implemented as an enum so will need to be tested in somewhere
#  that uses VERSION_STATUS

def test_its_json_base_version_tree_id():
    v_json = VersionTreeID("1.2.2").as_json()

    validate(v_json)

# TODO: LOCATABLE_REF

def test_its_json_base_generic_id():
    gid_json = GenericID("QQ123456A", "https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim39110").as_json()

    validate(gid_json)

def test_its_json_base_archetype_id():
    a_json = ArchetypeID("openEHR-EHR-INSTRUCTION.medication_order.v3").as_json()

    validate(a_json)

def test_its_json_base_hier_object_id():
    h_json = HierObjectID("93f49724-c066-40f5-aea0-5d0ff1184326::abacus").as_json()

    validate(h_json)

def test_its_json_base_uuid():
    u_json = UUID("82901b2e-0920-4cbe-913e-fa119258a94b").as_json()

    validate(u_json)

# VALIDITY_KIND is implemented as an enum so will need to be tested in somewhere
#  that uses VALIDITY_KIND

def test_its_json_base_iso_oid():
    i_json = ISOOID("2.16.840.1.113883.2.1.10").as_json()

    validate(i_json)

# TODO: ARCHETYPE_HRID is in the JSON spec, but not in the actual base spec so treating
#  this as an issue to raise with spec

def test_its_json_base_terminology_id():
    t_json = TerminologyID("SNOMED-CT").as_json()

    validate(t_json)

# ==========
# RM.data_types: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types

def test_its_json_rm_data_type_dv_text():
    t_dvt = DVText("NICE guidance on 'Overweight and obesity management'", 
                   hyperlink=DVUri("https://www.nice.org.uk/guidance/ng246"),
                   formatting="plain_no_newlines").as_json()

    validate(t_dvt)

def test_its_json_rm_data_type_dv_identifier():
    t_dvi = DVIdentifier("9990548609", issuer="NHS Digital", id_type="NHS Number").as_json()

    validate(t_dvi)

def test_its_json_rm_data_type_dv_date():
    t_dvd = DVDate("2025-10-27").as_json()

    validate(t_dvd)

def test_its_json_rm_data_type_dv_coded_text():
    t_dvct = DVCodedText(
        "Asthma",
        defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "195967001", "Asthma (disorder)"),
        mappings=[
            TermMapping('=', CodePhrase(TerminologyID("ICD-10"), "J45", "Asthma"))
        ]).as_json()

    validate(t_dvct)

def test_its_json_rm_data_type_dv_time():
    t_dvt = DVTime(
        "13:00",
        accuracy=DVDuration("PT15M")
    ).as_json()

    validate(t_dvt)

def test_its_json_rm_data_type_dv_boolean():
    t_dvb = DVBoolean(False).as_json()

    validate(t_dvb)

def test_its_json_rm_data_type_code_phrase():
    cd_phrse = CodePhrase(TerminologyID("SNOMED-CT"), "1069221000000106", "Does not shop at supermarket (finding)").as_json()

    validate(cd_phrse)

def test_its_json_rm_data_type_dv_parsable():
    t_dvp = DVParsable("{\"val\":\"test\"}", 
                       formalism="json",
                       charset=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
                       terminology_service=test_ts).as_json()

    validate(t_dvp)

def test_its_json_rm_data_type_term_mapping():
    t_dtm = TermMapping('=', CodePhrase(TerminologyID("ICD-10"), "J45", "Asthma")).as_json()
    
    validate(t_dtm)

def test_its_json_rm_data_type_dv_ehr_uri():
    t_dveu = DVEHRUri("ehr:tasks/380daa09-028f-4beb-9803-4aef91644c2a").as_json()

    validate(t_dveu)

def test_its_json_rm_data_type_dv_uri():
    t_dvu = DVUri("https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_URI.json").as_json()

    validate(t_dvu)

def test_its_json_rm_data_type_dv_count():
    t_dvc = DVCount(3000, accuracy=0.05, accuracy_is_percent=True).as_json()

    validate(t_dvc)

# accepts warning until DV_GENERAL_TIME_SPECIFICATION is fully implemented
@pytest.mark.filterwarnings("ignore: DVGeneralTimeSpecification does not")
def test_its_json_rm_data_type_dv_general_time_specification():
    t_dvgts = DVGeneralTimeSpecification(DVParsable("WAKE+[50m;1h]", "HL7:GTS")).as_json()

    validate(t_dvgts)

def test_its_json_rm_data_type_dv_multimedia():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()

    # inline
    t_dvmi = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes).as_json()
    
    validate(t_dvmi)
    
    # external
    t_dvme = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/pdf"),
        size=549453,
        terminology_service=test_ts,
        uri=DVUri("https://ruh.nhs.uk/patients/patient_information/HTH024_Wrist_Exercises.pdf")
    ).as_json()

    validate(t_dvme)

def test_its_json_rm_data_type_dv_date_time():
    t_dvdt = DVDateTime("20251102T194100Z").as_json()

    validate(t_dvdt)

def test_its_json_rm_data_type_dv_quantity():
    t_dvq = DVQuantity(200.6, 
                       units="cm",
                       units_display_name="cm",
                       precision=1,
                       magnitude_status="=").as_json()
    
    validate(t_dvq)

def test_its_json_rm_data_type_dv_duration():
    t_dvd = DVDuration("P3D",
                       magnitude_status="~",
                       normal_status=CodePhrase(TerminologyID("openehr_normal_statuses"), "L"),
                       terminology_service=test_ts).as_json()
    
    validate(t_dvd)

def test_its_json_rm_data_type_dv_interval():
    low = DVQuantity(97.5, "cm")
    high = DVQuantity(122.0, "cm")
    t_dvi = DVInterval(ProperInterval[DVQuantity](lower=low, upper=high, lower_included=True, upper_included=True)).as_json()

    validate(t_dvi)

def test_its_json_rm_data_type_dv_ordinal():
    t_dvo = DVOrdinal(3, 
                      symbol=DVCodedText("Canadian Study of Health and Aging Clinical Frailty Scale level 3 - managing well (finding)",
                                         defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "1129351000000108"))).as_json()
    
    validate(t_dvo)

def test_its_json_rm_data_type_dv_paragraph():
    t_dvp = DVParagraph([
        DVText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
        DVText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    ]).as_json()

    validate(t_dvp)

def test_its_json_rm_data_type_dv_state():
    t_dvs = DVState(
                    value=DVCodedText("planned", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "526", "planned")),
                    is_terminal=False).as_json()
    
    validate(t_dvs)

def test_its_json_rm_data_type_dv_periodic_time_specification():
    t_dvpts = DVPeriodicTimeSpecification(DVParsable("[20250914;]/(PT1M)@DM", "HL7:PIVL")).as_json()

    validate(t_dvpts)

def test_its_json_rm_data_type_dv_proportion():
    t_dvp = DVProportion(95.0, 100.0, ProportionKind.PK_PERCENT).as_json()

    validate(t_dvp)

def test_its_json_rm_data_type_dv_scale():
    t_dvs = DVScale(0.5, DVCodedText("Borg Breathlessness Score: 0.5 very, very slight (just noticeable) (finding)", 
                                     defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "401323002"))).as_json()
    
    validate(t_dvs)

def test_its_json_rm_data_type_reference_range():
    t_rr = ReferenceRange(meaning=DVText("Reduced healthy BMI range due to Asian family background"), 
                          range=DVInterval(value=ProperInterval[DVQuantity](
                                                                            lower=DVQuantity(18.5, "kg/m2"),
                                                                            upper=DVQuantity(23.0, "kg/m2"),
                                                                            lower_included=True,
                                                                            upper_included=False))).as_json()
    validate(t_rr)