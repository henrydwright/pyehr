import pytest
import json

import jsonschema
import numpy as np

from org.openehr.base.foundation_types.interval import PointInterval, ProperInterval, MultiplicityInterval
from org.openehr.base.base_types.identification import TerminologyID
from org.openehr.its.json_tools import OpenEHREncoder

from org.openehr.base.base_types.identification import TerminologyID, ISOOID, UUID, InternetID, VersionTreeID, HierObjectID, ObjectVersionID, ArchetypeID, TemplateID, GenericID, ObjectRef, PartyRef
from org.openehr.rm.data_types.text import DVText, DVUri
from org.openehr.rm.data_types.basic import DVIdentifier

# as_json methods are not tested in individual module tests, rather they are tested
#  here so they can be assessed against the list at https://specifications.openehr.org/releases/ITS-JSON/development/components/

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