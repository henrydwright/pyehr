import pytest
import json

import jsonschema
import numpy as np

from common import CODESET_OPENEHR_COUNTRIES, PythonTerminologyService, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR

from pyehr.core.base.foundation_types.time import ISODate, ISOTime, ISODuration, ISODateTime
from pyehr.core.base.foundation_types.interval import PointInterval, ProperInterval, MultiplicityInterval
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.base.foundation_types.terminology import TerminologyCode, TerminologyTerm
from pyehr.core.base.base_types.identification import LocatableRef, TerminologyID
from pyehr.core.base.base_types.identification import TerminologyID, ISOOID, UUID, InternetID, VersionTreeID, HierObjectID, ObjectVersionID, ArchetypeID, TemplateID, GenericID, ObjectRef, PartyRef
from pyehr.core.base.resource import TranslationDetails, ResourceDescriptionItem, ResourceDescription, AuthoredResource

from pyehr.core.its.json_tools import OpenEHREncoder

from pyehr.core.rm.data_structures.history import History, IntervalEvent, PointEvent
from pyehr.core.rm.data_types.text import DVText, DVUri, DVCodedText, CodePhrase, TermMapping, DVParagraph
from pyehr.core.rm.data_types.basic import DVIdentifier, DVBoolean, DVState
from pyehr.core.rm.data_types.uri import DVEHRUri
from pyehr.core.rm.data_types.quantity import DVCount, DVQuantity, DVInterval, DVOrdinal, DVProportion, ProportionKind, DVScale, ReferenceRange
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVTime, DVDuration, DVDateTime
from pyehr.core.rm.data_types.encapsulated import DVParsable, DVMultimedia
from pyehr.core.rm.data_types.time_specification import DVGeneralTimeSpecification, DVPeriodicTimeSpecification

from pyehr.core.rm.ehr.composition import Composition, EventContext
from pyehr.core.rm.ehr.composition.content.entry import Activity, AdminEntry, Evaluation, Instruction, InstructionDetails, Observation
from pyehr.core.rm.ehr.composition.content.navigation import Section
from pyehr.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

from pyehr.core.rm.common.archetyped import FeederAudit, FeederAuditDetails, Link, Archetyped
from pyehr.core.rm.common.generic import Attestation, PartyIdentified, PartyRelated, PartySelf, PartyRef, RevisionHistoryItem, RevisionHistory, AuditDetails, Participation
from pyehr.core.rm.common.change_control import OriginalVersion, ImportedVersion, VersionedObject, Contribution
from pyehr.core.rm.common.directory import Folder

from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemList, ItemTable, ItemTree

from pyehr.core.rm.ehr.ehr import EHR

# as_json methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-JSON/development/components/

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

def validate(json_obj):
    _schema = json.loads(open("test/pyehr/core/its/schemas/openehr_rm_1.1.0_alltypes_strict.json").read())
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

def test_its_json_base_locatable_ref():
    v_lr = LocatableRef("local", "INSTRUCTION", HierObjectID("d2adf197-dfed-43d0-81f8-ccd27e5e127c"), "content[0]").as_json()

    validate(v_lr)

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

def test_its_json_rm_data_structures_interval_event():
    hs = History(
        DVText("pain scores over time"),
        archetype_node_id="at0010",
        origin=DVDateTime("2025-12-28T12:00:00Z")
    )
    t_iev = IntervalEvent[ItemSingle](
        name=DVText("overnight pain score average"),
        archetype_node_id="at0014",
        time=DVDateTime("2025-12-29T08:00:00Z"),
        data=ItemSingle(
            name=DVText("@ internal @"),
            archetype_node_id="at0015",
            item=Element(
                DVText("pain score"),
                archetype_node_id="at0016",
                value=DVProportion(5.6, 10.0, ProportionKind.PK_RATIO)
            )
        ),
        width=DVDuration("PT12H"),
        math_function=DVCodedText("mean", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "146")),
        terminology_service=test_ts,
        parent=hs
    ).as_json()

    print(t_iev)

    validate(t_iev)

def test_its_json_rm_data_structures_item_table():
    ev = DVProportion(6.0, 6.0, ProportionKind.PK_RATIO)

    el01 = Element(name=DVText("visual acuity"),
                            archetype_node_id="at0021",
                            value=ev)

    row0 = Cluster(
                name=DVText("1"),
                archetype_node_id="at0010",
                items=[
                    Element(name=DVText("eye(s)"),
                            archetype_node_id="at0020",
                            value=DVCodedText(value="right", defining_code=CodePhrase(TerminologyID("local"), "at0030"))),
                    el01])

    el10 = Element(name=DVText("eye(s)"),
                            archetype_node_id="at0020",
                            value=DVCodedText(value="left", defining_code=CodePhrase(TerminologyID("local"), "at0031")))

    row1 = Cluster(
                name=DVText("2"),
                archetype_node_id="at0010",
                items=[
                    el10,
                    Element(name=DVText("visual acuity"),
                            archetype_node_id="at0021",
                            value=DVProportion(6.0, 18.0, ProportionKind.PK_RATIO))])

    row2 = Cluster(
                name=DVText("3"),
                archetype_node_id="at0010",
                items=[
                    Element(name=DVText("eye(s)"),
                            archetype_node_id="at0020",
                            value=DVCodedText(value="both", defining_code=CodePhrase(TerminologyID("local"), "at0030"))),
                    Element(name=DVText("visual acuity"),
                            archetype_node_id="at0021",
                            value=DVProportion(6.0, 6.0, ProportionKind.PK_RATIO))])

    t_itbl = ItemTable(
        name=DVText("vision"),
        archetype_node_id="at0002",
        rows=[
            row0,
            row1,
            row2
        ]
    ).as_json()

    validate(t_itbl)

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

def test_its_json_rm_data_structures_item_tree():
    val0 = DVCodedText("Serum (substance)", CodePhrase(TerminologyID("SNOMED-CT"), "67922002"))

    it0 = Element(
        name=DVText("sample"),
        archetype_node_id="at0010",
        value=val0
        )


    it1el0 = Element(
        name=DVText("total cholestrol"),
        archetype_node_id="at0020",
        value=DVQuantity(6.1, "mmol/L")
    )

    it1el1 = Element(
                name=DVText("HDL cholestrol"),
                archetype_node_id="at0021",
                value=DVQuantity(0.9, "mmol/L")
            )

    it1el2 = Element(
                name=DVText("LDL cholestrol"),
                archetype_node_id="at0022",
                value=DVQuantity(5.2, "mmol/L")
            )

    it1 = Cluster(
        name=DVText("lipid studies"),
        archetype_node_id="at0011",
        items=[
            it1el0,
            it1el1,
            it1el2
        ]
    )

    it2 = Element(
        name=DVText("comment"),
        archetype_node_id="at0012",
        value=DVText("xxxx")
    )

    t_itr = ItemTree(
        name=DVText("Biochemistry Result"),
        archetype_node_id="at0002",
        items=[
            it0,
            it1,
            it2
        ]
    ).as_json()

    validate(t_itr)

def test_its_json_rm_data_structures_history():
    su = ItemSingle(
        DVText("@ internal @"),
        archetype_node_id="at0080",
        item=Element(
            name=DVText("commentary"),
            archetype_node_id="at0081",
            value=DVText("pain scores mild during day and overnight")
        )
    )

    t_hs = History[ItemSingle](
        DVText("pain scores over time"),
        archetype_node_id="at0010",
        origin=DVDateTime("2025-12-28T12:00:00Z"),
        summary=su
    ).as_json()

    validate(t_hs)


def test_its_json_rm_data_structures_point_event():
    hs = History(
    DVText("pain scores over time"),
    archetype_node_id="at0010",
    origin=DVDateTime("2025-12-28T12:00:00Z")
    )
    da = ItemSingle(
            name=DVText("@ internal @"),
            archetype_node_id="at0012",
            item=Element(
                name=DVText("pain score"),
                archetype_node_id="at0020",
                value=DVProportion(1.0, 10.0, ProportionKind.PK_RATIO)
            )
        )
    st = ItemSingle(
            name=DVText("@ internal @"),
            archetype_node_id="at0013",
            item=Element(
                name=DVText("patient state"),
                archetype_node_id="at0030",
                value=DVCodedText("Lying position", CodePhrase(TerminologyID("SNOMED-CT"), "102538003"))
            )
        )
    t_ev = PointEvent[ItemSingle](
        name=DVText("1"),
        archetype_node_id="at0011",
        time=DVDateTime("2025-12-28T13:00:00Z"),
        data=da,
        state=st,
        parent=hs
    ).as_json()

    print(t_ev)

    validate(t_ev)

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

# ==========
# RM.ehr: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Ehr

# TODO: EHR_STATUS

# TODO: EHR_ACCESS

def test_its_json_rm_ehr_ehr():
    t_ehr = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z"),
        folders=[ObjectRef("net.example.ehr", "VERSIONED_FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
    ).as_json()

    validate(t_ehr)

# ==========
# RM.ehr.composition: release 1.1.0 - https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition

# TODO: ISM_TRANSACTION

def test_its_json_rm_ehr_composition_instruction():
    desc = ItemTree(
        name=DVText("Tree"),
        archetype_node_id="at0002",
        items=[
            Cluster(
                name=DVText("medication details"),
                archetype_node_id="at0143",
                items=[
                    Element(
                        name=DVText("Name"),
                        archetype_node_id="at0132",
                        value=DVCodedText("Paracetamol 500mg tablets (product)", CodePhrase(TerminologyID("SNOMED-CT"), "42109611000001109"))
                    )
                ]
            ),
            Element(
                name=DVText("route"),
                archetype_node_id="at0091",
                value=DVCodedText("Oral", CodePhrase(TerminologyID("SNOMED-CT"), "26643006"))
            )
        ]
    )

    act = Activity(
        name=DVText("Order (Paracetamol 500mg tablets)"),
        archetype_node_id="at0001",
        description=desc,
        timing=DVParsable(
            value="R1000/2026-01-01T13:29:00Z/PT6H",
            formalism="ISO8601"
        )
    )

    t_ins = Instruction(
        name=DVText("Medication order"),
        archetype_node_id="openEHR-EHR-INSTRUCTION.medication_order.v3",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-INSTRUCTION.medication_order.v3"), "1.1.0"),
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
        subject=PartySelf(),
        narrative=DVText("500mg paracetamol tablets to be taken orally 4 times a day"),
        terminology_service=test_ts,
        activities=[
            act
        ]
    ).as_json()

    validate(t_ins)

def test_its_json_rm_ehr_composition_admin_entry():
    it0 = Element(
                name=DVText("hospital provider spell identifier"),
                archetype_node_id="at0011",
                value=DVIdentifier("AA-000-000-000")
            )

    it_lst = ItemList(
            name=DVText("admission characteristics"),
            archetype_node_id="at0001",
            items=[
                it0,
                Element(
                    name=DVText("administrative category code (on admission)"),
                    archetype_node_id="at0012",
                    value=DVCodedText("NHS PATIENT, including Overseas Visitors charged under the National Health Service (Overseas Visitors Hospital Charging Regulations)", CodePhrase(TerminologyID("NHS_NATIONAL_ADMINISTRATIVE_CATEGORY_CODE"), "01"))
                ),
                Element(
                    name=DVText("patient classification code"),
                    archetype_node_id="at0013",
                    value=DVCodedText("Ordinary admission", CodePhrase(TerminologyID("NHS_NATIONAL_PATIENT_CLASSIFICATION_CODE"), "1"))
                )
            ]
        )

    t_ae = AdminEntry(
        name=DVText("Admission 30/12/2025"),
        archetype_node_id="openEHR-EHR-ADMIN_ENTRY.cds_admission.v0",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.cds_admission.v0"), "1.1.0"),
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb", "English (United Kingdom)"),
        encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
        subject=PartySelf(),
        data=it_lst,
        terminology_service=test_ts,
        other_participations=[
            Participation(DVText("observer"), PartyIdentified(name="Miss M Student"))
        ]
    ).as_json()

    validate(t_ae)

def test_its_json_rm_ehr_composition_activity():
    desc = ItemTree(
        name=DVText("Tree"),
        archetype_node_id="at0002",
        items=[
            Cluster(
                name=DVText("medication details"),
                archetype_node_id="at0143",
                items=[
                    Element(
                        name=DVText("Name"),
                        archetype_node_id="at0132",
                        value=DVCodedText("Paracetamol 500mg tablets (product)", CodePhrase(TerminologyID("SNOMED-CT"), "42109611000001109"))
                    )
                ]
            ),
            Element(
                name=DVText("route"),
                archetype_node_id="at0091",
                value=DVCodedText("Oral", CodePhrase(TerminologyID("SNOMED-CT"), "26643006"))
            )
        ]
    )

    t_act = Activity(
        name=DVText("Order (paracetamol)"),
        archetype_node_id="at0001",
        description=desc,
        timing=DVParsable(
            value="R1000/2026-01-01T13:29:00Z/PT6H",
            formalism="ISO8601"
        )
    ).as_json()

    validate(t_act)

def test_its_json_rm_ehr_composition():
    t_c = Composition(
        name=DVText("GP appointment - 29th Dec 2025"),
        archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
        category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
        composer=PartyIdentified(name="Dr Test General-Practitioner"),
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
        terminology_service=test_ts
    ).as_json()

    validate(t_c)

def test_its_json_rm_ehr_composition_instruction_details():
    t_insd = InstructionDetails(
        instruction_id=LocatableRef("local", "INSTRUCTION", HierObjectID("d2adf197-dfed-43d0-81f8-ccd27e5e127c"), "content[0]"),
        activity_id="activities[at0001]"
    ).as_json()

    validate(t_insd)

def test_its_json_rm_ehr_composition_evaluation():
    t_ev = Evaluation(
        name=DVText("Tobacco smoking summary"),
        archetype_node_id="openEHR-EHR-EVALUATION.tobacco_smoking_summary.v1",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.tobacco_smoking_summary.v1"), "1.1.0"),
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
        subject=PartySelf(),
        data=ItemTree(
            DVText("Tree"),
            archetype_node_id="at0001",
            items=[
                Element(
                    name=DVText("Overall status"),
                    archetype_node_id="at0089",
                    value=DVCodedText("Never smoked", CodePhrase(TerminologyID("local"), "at0006"))
                )
            ]
        ),
        terminology_service=test_ts
    ).as_json()

    validate(t_ev)

# TODO: GENERIC_ENTRY

def test_its_json_rm_ehr_composition_event_context():
    t_ec = EventContext(
        start_time=DVDateTime("2025-12-29"),
        setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
        terminology_service=test_ts,
        participations=[Participation(DVText("observer"), PartyIdentified(name="Miss M Student"))]
    ).as_json()

    validate(t_ec)

def test_its_json_rm_ehr_composition_section():
    t_s = Section(
        name=DVText("subjective"),
        archetype_node_id="at0011"
    ).as_json()

    validate(t_s)

def test_its_json_rm_ehr_composition_observation():
    
    his = History[ItemTree](
            name=DVText("history"),
            archetype_node_id="at0002",
            origin=DVDateTime("2026-01-01T12:28:00Z")
        )
    his.events = [
                PointEvent[ItemTree](
                    name=DVText("weight at 12:28"),
                    archetype_node_id="at0003",
                    time=DVDateTime("2026-01-01T12:28:00Z"),
                    data=ItemTree(
                        name=DVText("weight observation"),
                        archetype_node_id="at0001",
                        items=[
                            Element(
                                name=DVText("weight"),
                                archetype_node_id="at0004",
                                value=DVQuantity(82.0, "kg")
                            )
                        ]
                    ),
                    parent=his
                )
            ]
    t_obs = Observation(
        name=DVText("Body weight"),
        archetype_node_id="openEHR-EHR-OBSERVATION.body_weight.v2",
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
        subject=PartySelf(),
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-OBSERVATION.body_weight.v2"), "1.1.0"),
        data=his,
        terminology_service=test_ts
    ).as_json()

    validate(t_obs)

# TODO: ACTION
