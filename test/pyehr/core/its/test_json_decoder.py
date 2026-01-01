import pytest

from pyehr.core.its.json_tools import decode_json

from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, ObjectVersionID, GenericID
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.rm.data_types.text import DVText, DVUri
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.ehr import EHR, EHRStatus

def test_decode_json_base_object_version_id():
    j_ovid = {"_type": "OBJECT_VERSION_ID", "value": "154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"}
    d = decode_json(j_ovid)
    assert d.is_equal(ObjectVersionID("154b1047-23aa-4d4d-8713-df848fd4d60a::net.example.ehr::1"))

def test_decode_json_base_object_ref():
    j_oref = {"_type": "OBJECT_REF", "id": {"_type": "HIER_OBJECT_ID", "value": "1826ea47-e98b-4779-b201-80db3af5de92"}, "namespace": "net.example.ehr", "type": "CONTRIBUTION"}
    d = decode_json(j_oref)
    assert d.is_equal(ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("1826ea47-e98b-4779-b201-80db3af5de92")))

def test_decode_json_base_hier_object_id():
    j_hid = {"_type": "HIER_OBJECT_ID", "value": "b6e8c15d-c376-4ebe-b140-5aafe9b13e06"}
    d = decode_json(j_hid)
    assert d.is_equal(HierObjectID("b6e8c15d-c376-4ebe-b140-5aafe9b13e06"))

def test_decode_json_rm_data_types_dv_text():
    j_txt = {"_type": "DV_TEXT", "value": "NICE guidance on 'Overweight and obesity management'", "hyperlink": {"_type": "DV_URI", "value": "https://www.nice.org.uk/guidance/ng246"}, "formatting": "plain_no_newlines"}
    d = decode_json(j_txt)
    assert d.is_equal(DVText("NICE guidance on 'Overweight and obesity management'", 
                   hyperlink=DVUri("https://www.nice.org.uk/guidance/ng246"),
                   formatting="plain_no_newlines"))
    
def test_decode_json_rm_data_types_dv_uri():
    j_uri = {"_type": "DV_URI", "value": "https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_URI.json"}
    d = decode_json(j_uri)
    assert d.is_equal(DVUri("https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_URI.json"))

def test_decode_json_rm_data_types_dv_datetime():
    j_dt = {"value": "2025-11-02T19:41:00Z", "_type": "DV_DATE_TIME"}
    d = decode_json(j_dt)
    assert d.is_equal(DVDateTime("2025-11-02T19:41:00Z"))

def test_decode_json_rm_common_party_self():
    j_ps = {"_type": "PARTY_SELF"}
    d = decode_json(j_ps)
    assert d.is_equal(PartySelf())

def test_decode_json_rm_ehr_ehr_refs_resolved():
    # this is the result of GET /ehr/{ehr_id} from an EHRBase system
    j_ehr = {"system_id": {"_type": "HIER_OBJECT_ID", "value": "local.ehrbase.org"}, "ehr_id": {"_type": "HIER_OBJECT_ID", "value": "b6e8c15d-c376-4ebe-b140-5aafe9b13e06"}, "ehr_status": {"uid": {"_type": "OBJECT_VERSION_ID", "value": "3fc55311-f4bc-44da-a123-1417ad35b09c::local.ehrbase.org::1"}, "archetype_node_id": "openEHR-EHR-EHR_STATUS.generic.v1", "name": {"_type": "DV_TEXT", "value": "EHR Status"}, "subject": {"_type": "PARTY_SELF"}, "is_queryable": True, "is_modifiable": True, "_type": "EHR_STATUS"}, "time_created": {"_type": "DV_DATE_TIME", "value": "2025-12-06T16:53:48.006423Z"}}
    d_lst = decode_json(j_ehr, target="EHR")
    es = EHRStatus(
        name=DVText("EHR Status"),
        archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
        uid=ObjectVersionID("3fc55311-f4bc-44da-a123-1417ad35b09c::local.ehrbase.org::1"),
        subject=PartySelf(),
        is_queryable=True,
        is_modifiable=True,
        archetype_details=Archetyped(archetype_id=ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"), rm_version="1.1.0")
    )
    assert d_lst[0].is_equal(es)

    assert d_lst[1].is_equal(EHR(
        system_id=HierObjectID("local.ehrbase.org"),
        ehr_id=HierObjectID("b6e8c15d-c376-4ebe-b140-5aafe9b13e06"),
        ehr_status=ObjectRef("pyehr_decode_json", "VERSIONED_EHR_STATUS", GenericID("0", "list_index")),
        ehr_access=ObjectRef("null", "VERSIONED_EHR_ACCESS", HierObjectID("00000000-0000-0000-0000-000000000000")),
        time_created=DVDateTime("2025-12-06T16:53:48.006423Z")
    ))
