import pytest
import json

import jsonschema
import numpy as np

from common import PythonTerminologyService, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR

from org.openehr.base.foundation_types.time import ISODate, ISOTime, ISODuration, ISODateTime
from org.openehr.base.foundation_types.interval import PointInterval, ProperInterval, MultiplicityInterval
from org.openehr.base.foundation_types.primitive_types import Uri
from org.openehr.base.foundation_types.terminology import TerminologyCode, TerminologyTerm
from org.openehr.base.base_types.identification import TerminologyID
from org.openehr.base.base_types.identification import TerminologyID, ISOOID, UUID, InternetID, VersionTreeID, HierObjectID, ObjectVersionID, ArchetypeID, TemplateID, GenericID, ObjectRef, PartyRef
from org.openehr.base.resource import TranslationDetails, ResourceDescriptionItem, ResourceDescription, AuthoredResource

from org.openehr.its.json_tools import OpenEHREncoder

from org.openehr.rm.data_types.text import DVText, DVUri, DVCodedText, CodePhrase, TermMapping, DVParagraph
from org.openehr.rm.data_types.basic import DVIdentifier, DVBoolean, DVState
from org.openehr.rm.data_types.uri import DVEHRUri
from org.openehr.rm.data_types.quantity import DVCount, DVQuantity, DVInterval, DVOrdinal, DVProportion, ProportionKind, DVScale, ReferenceRange
from org.openehr.rm.data_types.quantity.date_time import DVDate, DVTime, DVDuration, DVDateTime
from org.openehr.rm.data_types.encapsulated import DVParsable, DVMultimedia
from org.openehr.rm.data_types.time_specification import DVGeneralTimeSpecification, DVPeriodicTimeSpecification

from org.openehr.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

from org.openehr.rm.common.archetyped import FeederAudit, FeederAuditDetails, Link, Archetyped
from org.openehr.rm.common.generic import Attestation, PartyIdentified, PartyRelated, PartySelf, PartyRef, RevisionHistoryItem, RevisionHistory, AuditDetails, Participation
from org.openehr.rm.common.change_control import OriginalVersion, ImportedVersion, VersionedObject, Contribution
from org.openehr.rm.common.directory import Folder

from org.openehr.rm.data_structures.representation import Cluster, Element
from org.openehr.rm.data_structures.item_structure import ItemSingle, ItemList

# as_json methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-JSON/development/components/

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

def validate(json_obj):
    _schema = json.loads(open("test/org/openehr/its/schemas/openehr_rm_1.1.0_alltypes_strict.json").read())
    # keep this as a separate method so we can switch to a different validator
    #  at a future date if we need to
    jsonschema.validate(json_obj, _schema)

# ==========
# BASE.foundation_types: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Foundation_types

def test_its_json_foundation_date():
    dt = ISODate("2025-11-03").as_json()
    
    validate(dt)

# ARRAY just uses a numpy array so would never be serialised as an object

def test_its_json_foundation_interval():
    pi_json = PointInterval[np.int32](np.int32(0)).as_json()
    validate(pi_json)

    pri_json = ProperInterval[str](lower="SMITH", lower_included=True).as_json()
    validate(pri_json)

    mi_json = MultiplicityInterval(lower=np.int32(0), upper=np.int32(1)).as_json()
    validate(mi_json)

def test_its_json_foundation_time():
    tm = ISOTime("08:48").as_json()

    validate(tm)

def test_its_json_foundation_duration():
    dur = ISODuration("P2Y").as_json()

    validate(dur)

# URI is just represented as a string so would never be serialised as an object

def test_its_json_foundation_terminology_code():
    # TODO: specification and JSON specification disagree on whether Uri is required or not
    #  trusting spec, and modifying JSON spec to pass test
    tc = TerminologyCode("SNOMED-CT", "71341001").as_json()

    validate(tc)

# set and list are represented as built in Python/JSON objects so would never be serialised as an object

def test_its_json_foundation_terminology_term():
    tt = TerminologyTerm(TerminologyCode("SNOMED-CT", "71341001"), "Bone structure of femur (body structure)").as_json()

    validate(tt)

def test_its_json_foundation_date_time():
    dt = ISODateTime("2025-11-03T09:03:00Z").as_json()

    validate(dt)

# ==========
# BASE.base_types: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Base_types

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
# BASE.resource: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Resource

def test_its_json_base_translation_details():
    t_td = TranslationDetails(
        language=TerminologyCode("ISO639-1", "de"),
        author={"name": "Herr H. Potter"},
        version_last_translated="1.2.0"
    ).as_json()

    validate(t_td)

def test_its_json_base_resource_description_item():
    t_rdi = ResourceDescriptionItem(
        language=TerminologyCode("ISO639-1", "en"),
        purpose="To record details about the gender of an individual",
        keywords=["sex", "male", "female"],
        use="Use to record details about the individual's gender, including administrative and legal gender and assigned sex at birth, in addition to gender identity, expression and preferred pronoun.",
        misuse="Not to be used for recording information relating to the sexual orientation or sexual activity of an individual."
    ).as_json()

    validate(t_rdi)

class TestAuthoredResourceImplementation(AuthoredResource):
    __test__ = False

    def __init__(self, original_language, uid = None, is_controlled = None, annotations = None):
        super().__init__(original_language, uid, is_controlled, annotations)

    def current_revision(self) -> str:
        return "(uncontrolled)"
    
    def as_json(self):
        return super().as_json()

def test_its_json_base_resource_description():
    res = TestAuthoredResourceImplementation(TerminologyCode("ISO639-1", "en"), uid=UUID("139940b4-8435-463e-93e6-d9e13b02c282"))
    t_rd = ResourceDescription(
        original_author={"Author name": "Joe Bloggs", "Organisation": "Anytown NHS Trust", "Email": "joe@example.net", "Date originally authored": "2017-11-30"},
        lifecycle_state=TerminologyCode("openehr", "532"),
        parent_resource=res,
        custodian_namespace="org.openehr",
        custodian_organisation="openEHR Foundation"
    ).as_json()

    validate(t_rd)

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

# ==========
# RM.common - https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common

def test_its_json_rm_common_attestation():
    t_att = Attestation(
        system_id="net.example.ehr",
        time_committed=DVDateTime("20251104T181000Z"),
        change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
        committer=PartyIdentified(name="Dr T Test"),
        reason=DVText("Initial version created"),
        is_pending=False,
        terminology_service=test_ts).as_json()
    
    validate(t_att)

def test_its_json_rm_common_contribution():
    t_con = Contribution(
        uid=HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92"),
        versions=[
            ObjectRef("net.example.ehr", "ORIGINAL_VERSION", ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))
        ],
        audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=test_ts)
    ).as_json()

    validate(t_con)

def test_its_json_rm_common_feeder_audit():
    t_fa = FeederAudit(
        originating_system_audit=FeederAuditDetails(
            system_id="net.example.legacy_ehr",
            time=DVDateTime("20251104T183900Z")
        )
    ).as_json()

    validate(t_fa)

def test_its_json_rm_common_link():
    t_lnk = Link(
        meaning=DVText("previous issue"),
        link_type=DVText("history"),
        target=DVEHRUri("ehr:tasks/380daa09-028f-4beb-9803-4aef91644c2a")
    ).as_json()

    validate(t_lnk)

def test_its_json_rm_common_original_version():
    t_ov = OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=test_ts),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        lifecycle_state=DVCodedText("complete", CodePhrase(TerminologyID("openehr"), "532")),
        terminology_service=test_ts,
        data=DVText("Hello, world! This is some example text")
    ).as_json()

    validate(t_ov)

def test_its_json_rm_common_versioned_object():
    t_vo = VersionedObject[DVText](
        uid=HierObjectID("14304fd8-e37f-4ee8-9f39-5566a745ea99"),
        owner_id=ObjectRef("net.example.ehr", "EHR", HierObjectID("2e372186-480e-4555-97ae-1c639829caf4")),
        time_created=DVDateTime("20251109T201900Z")
    ).as_json()

    validate(t_vo)

def test_its_json_rm_common_archetyped():
    t_ach = Archetyped(
        archetype_id=ArchetypeID("openEHR-EHR-OBSERVATION.blood_pressure.v2"),
        rm_version="1.1.0"
    ).as_json()

    validate(t_ach)

def test_its_json_rm_common_party_related():
    t_pr = PartyRelated(
        relationship=DVCodedText("brother", CodePhrase(TerminologyID("openehr"), "23")),
        terminology_service=test_ts,
        name="Brian Bloggs"
    ).as_json()

    validate(t_pr)

def test_its_json_rm_common_revision_history_item():
    t_rhi = RevisionHistoryItem(
        version_id=ObjectVersionID("5f99cf14-3494-4a47-9051-91822d59468f::net.example.ehr::3"),
        audits=[
            AuditDetails(system_id="net.example.ehr", 
                         time_committed=DVDateTime("2025-11-04T20:49:02Z"), 
                         change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
                         committer=PartySelf(),
                         terminology_service=test_ts)
        ]
    ).as_json()

    validate(t_rhi)

def test_its_json_rm_common_folder():
    t_fr = Folder(
        name=DVText("remote monitoring"),
        archetype_node_id="pyehr-EHR-FOLDER.remote_monitoring.v0",
        archetype_details=Archetyped(
            archetype_id=ArchetypeID("pyehr-EHR-FOLDER.remote_monitoring.v0"),
            rm_version="1.1.0"
        ),
        uid=HierObjectID("1d61465e-020c-4d62-b452-5e79312efae7"),
        folders=[
            Folder(
                name=DVText("blood pressure readings"),
                archetype_node_id="at0005",
                folders=[
                    Folder(
                        name=DVText("sitting"),
                        archetype_node_id="at0007",
                        items=[
                            ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("b207449e-397b-4c44-8896-81fff5097bad")),
                            ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("c5e85918-e047-4fa9-ac7b-19ed4d8668b0")),
                            ObjectRef("net.example.ehr", "OBSERVATION", HierObjectID("18eed64a-1221-4736-ad66-b405615b38e9"))
                        ]
                    )
                ]
            )
        ]
    ).as_json()

    validate(t_fr)

def test_its_json_rm_common_feeder_audit_details():
    t_fad = FeederAuditDetails(
            system_id="net.example.legacy_ehr",
            time=DVDateTime("20251104T183900Z")
        ).as_json()
    
    validate(t_fad)

def test_its_json_rm_common_participation():
    t_ptc = Participation(
        function=DVText("observer"), 
        performer=PartyIdentified(name="Ms. A Student"),
        mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")),
        terminology_service=test_ts).as_json()
    
    validate(t_ptc)

def test_its_json_rm_common_imported_version():
    ov = OriginalVersion[DVText](
        contribution=ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-09-22T15:41:00Z"),
            change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
            committer=PartyIdentified(name="Mr A Example"),
            terminology_service=test_ts),
        uid=ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"),
        lifecycle_state=DVCodedText("complete", CodePhrase(TerminologyID("openehr"), "532")),
        terminology_service=test_ts,
        data=DVText("Hello, world! This is some example text")
    )
    t_iv = ImportedVersion[DVText](
        contribution=ObjectRef("org.example.ehr.prod", "CONTRIBUTION", HierObjectID("7ad8dcdc-62f1-41f6-b7bd-c1171f50aba5")),
        commit_audit=AuditDetails(
            system_id="net.example.ehr",
            time_committed=DVDateTime("2025-11-09T11:58:02Z"),
            change_type=DVCodedText("format conversion", CodePhrase(TerminologyID("openehr"), "817")),
            committer=PartyIdentified(name="Anytown NHS Trust ehrBridge"),
            terminology_service=test_ts
        ),
        item=ov
    ).as_json()

    validate(t_iv)


def test_its_json_rm_common_party_self():
    t_ps = PartySelf().as_json()

    validate(t_ps)

def test_its_json_rm_common_revision_history():
    t_rs = RevisionHistory([
        RevisionHistoryItem(
            version_id=ObjectVersionID("5f99cf14-3494-4a47-9051-91822d59468f::net.example.ehr::3"),
            audits=[
                AuditDetails(system_id="net.example.ehr", 
                            time_committed=DVDateTime("2025-11-04T20:49:02Z"), 
                            change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
                            committer=PartySelf(),
                            terminology_service=test_ts)
            ]
        )
    ]).as_json()

    validate(t_rs)

def test_its_json_rm_common_audit_details():
    t_ad = AuditDetails(system_id="net.example.ehr", 
                            time_committed=DVDateTime("2025-11-04T20:49:02Z"), 
                            change_type=DVCodedText("creation", CodePhrase(TerminologyID("openehr"), "249")),
                            committer=PartySelf(),
                            terminology_service=test_ts).as_json()
    
    validate(t_ad)

def test_its_json_rm_common_party_identified():
    t_pi = PartyIdentified(external_ref=PartyRef("net.example.employees", "PARTY", GenericID("5928123", "employee_number"))).as_json()

    validate(t_pi)

# ==========
# RM.data_structures: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures

# TODO: interval_event

# TODO: item_table

def test_its_json_rm_data_structures_cluster():
    postal_code = Element(DVText("postal code"),
                archetype_node_id="at0005",
                value=DVText("SW1A 1AA"))

    addr_items = [
        Element(DVText("address line"),
                archetype_node_id="at0001",
                value=DVText("Buckingham Palace")),
        Element(DVText("city/town"),
                archetype_node_id="at0002",
                value=DVText("London")),
        postal_code,
        Element(DVText("type"),
                archetype_node_id="at0010",
                value=DVCodedText("Physical", CodePhrase(TerminologyID("local"), "at0011")))
    ]

    t_c = Cluster(DVText("address"),
                archetype_node_id="openEHR-EHR-CLUSTER.address.v1",
                archetype_details=Archetyped(
                    archetype_id=ArchetypeID("openEHR-EHR-CLUSTER.address.v1"),
                    rm_version="1.1.0"
                ),
                items=addr_items).as_json()
    
    validate(t_c)

def test_its_json_rm_data_structures_item_list():
    t = DVDateTime("2025-11-25T23:28:00Z")
    t2 = DVDateTime("2025-12-05T20:25:04Z")
    e = Element(DVText("admission time"), 
            "at0001",
            value=t)

    e2 = Element(DVText("discharge time"),
                "at0002",
                value=t2)

    e3 = Element(DVText("admission reason"),
                "at0003",
                value=DVCodedText("Assault", defining_code=CodePhrase(TerminologyID("SNOMED-CT"), "52684005", "Assault (event)")))

    t_itl = ItemList(DVText("admission metadata"), 
                archetype_node_id="pyehr-EHR-ITEM_LIST.admission.v0",
                items=[e, e2, e3],
                archetype_details=Archetyped(ArchetypeID("pyehr-EHR-ITEM_LIST.admission.v0"), "1.1.0")).as_json()
    
    validate(t_itl)

# TODO: item_tree

# TODO: history

# TODO: point_event

def test_its_json_rm_data_structures_element():
    t_e = Element(
        name=DVText("test_element"),
        archetype_node_id="at0007",
        null_flavour=DVCodedText("not applicable", CodePhrase(TerminologyID("openehr"), "273")),
        terminology_service=test_ts
    ).as_json()

    validate(t_e)

def test_its_json_rm_data_structures_item_single():
    t = DVDateTime("2025-11-25T23:28:00Z")

    e = Element(DVText("admission time"), 
                "at0001",
                value=t)

    t_its = ItemSingle(DVText("admission time container"),
                    "pyehr-EHR-ITEM_SINGLE-admission_time.v0",
                    archetype_details=Archetyped(ArchetypeID("pyehr-EHR-ITEM_SINGLE.admission_time.v0"), "1.1.0"),
                    item=e).as_json()
    
    validate(t_its)