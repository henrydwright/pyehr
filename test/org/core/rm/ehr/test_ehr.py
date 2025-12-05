import pytest

from org.core.base.base_types.identification import HierObjectID, ObjectRef
from org.core.base.foundation_types.any import AnyClass
from org.core.rm.data_types.quantity.date_time import DVDateTime
from org.core.rm.ehr.ehr import EHR

def test_ehr_contributions_valid():
    # OK - no contributions
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z")
    )
    # OK - contributions and all are contributions
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z"),
        contributions=[ObjectRef("net.example.ehr", "CONTRIBUTION", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
    )
    # not OK - empty list
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            contributions=[]
        )
    # not OK - wrong reference type
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            contributions=[ObjectRef("net.example.ehr", "FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
        )

def test_ehr_ehr_access_valid():
    # OK
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z")
    )
    # not OK
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VEHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z")
        )

def test_ehr_ehr_status_valid():
    # OK
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z")
    )
    # not OK
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z")
        )

def test_ehr_compositions_valid():
    # OK - no compositions
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z")
    )
    # OK - compositions and all are compositions
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z"),
        compositions=[ObjectRef("net.example.ehr", "VERSIONED_COMPOSITION", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
    )
    # not OK - empty list
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            compositions=[]
        )
    # not OK - wrong reference type
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            compositions=[ObjectRef("net.example.ehr", "FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
        )

def test_ehr_folders_valid():
    # OK - no folders
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z")
    )
    # OK - folders and all are folders
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z"),
        folders=[ObjectRef("net.example.ehr", "VERSIONED_FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
    )
    # not OK - empty list
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            folders=[]
        )
    # not OK - wrong reference type
    with pytest.raises(ValueError):
        e = EHR(
            system_id=HierObjectID("net.example.ehr"),
            ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
            ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
            ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
            time_created=DVDateTime("20251205T220900Z"),
            folders=[ObjectRef("net.example.ehr", "FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))]
        )

def test_ehr_directory_valid_directory_in_folders():
    f = ObjectRef("net.example.ehr", "VERSIONED_FOLDER", HierObjectID("597a04f6-a738-4914-9d02-df95e67644d5"))
    e = EHR(
        system_id=HierObjectID("net.example.ehr"),
        ehr_id=HierObjectID("35f656ae-dca4-4979-bac1-2fe1f0228614"),
        ehr_status=ObjectRef("net.example.ehr", "VERSIONED_EHR_STATUS", id=HierObjectID("f87df864-2b0f-406b-94b6-cdc1d2589691")),
        ehr_access=ObjectRef("net.example.ehr", "VERSIONED_EHR_ACCESS", id=HierObjectID("7eef792c-acae-4641-9280-2a54d1690672")),
        time_created=DVDateTime("20251205T220900Z"),
        folders=[f]
    )
    assert e.directory.is_equal(f)
    assert e.directory.ref_type == "VERSIONED_FOLDER"
