from uuid import uuid4
import pytest
import mongomock

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, InternetID, ObjectRef, ObjectVersionID
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.change_control import Contribution, VersionedObject
from pyehr.core.rm.common.generic import AuditDetails, PartyIdentified
from pyehr.core.rm.data_structures.item_structure import ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.demographic import PartyIdentity, Person
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState
from pyehr.server.database import IDatabaseEngine
from pyehr.server.database.local import InMemoryDB
from pyehr.server.database.mongodb import MongoDBDatabaseEngine
from term import TERMINOLOGY_OPENEHR, PythonTerminologyService

USE_REAL_MONGODB = False

def _generate_hier_object_ids(db: IDatabaseEngine):
    hid_set = set()
    for i in range(1000):
        hid_set.add(db.generate_hier_object_id().value)
    return hid_set

def _get_local_db_engine() -> IDatabaseEngine:
    return InMemoryDB()

def _get_mongodb_engine():
    if USE_REAL_MONGODB:
        return MongoDBDatabaseEngine("mongodb://localhost:27017/?directConnection=true", f"testdb-{str(uuid4())}")
    else:
        return MongoDBDatabaseEngine("mongodb://localhost:27017/?directConnection=true", f"testdb-{str(uuid4())}", mongo_client=mongomock.MongoClient("mongodb://localhost:27017/?directConnection=true"))
        
def _get_test_person() -> Person:
    return Person(
        actor_type=DVText("patient"),
        archetype_node_id="pyEHR-DEMOGRAPHIC-PERSON.patient.v0",
        archetype_details=Archetyped(ArchetypeID("pyEHR-DEMOGRAPHIC-PERSON.patient.v0"), "1.1.0"),
        uid=HierObjectID(str(uuid4())),
        identities=[
            PartyIdentity(
                purpose=DVText("nhs"),
                archetype_node_id="at0001",
                details=ItemTree(
                    name=DVText("tree"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("NHS Number"),
                            archetype_node_id="at0004",
                            value=DVIdentifier("9449305552", "NHS Digital", id_type="NHS Number")
                        ),
                        Cluster(
                            name=DVText("Name"),
                            archetype_node_id="at0005",
                            items=[
                                Element(
                                    name=DVText("Family Name"),
                                    archetype_node_id="at0006",
                                    value=DVText("CHISLETT")
                                ),
                                Element(
                                    name=DVText("Given Name"),
                                    archetype_node_id="at0007",
                                    value=DVText("OCTAVIA")
                                ),
                                Element(
                                    name=DVText("Title"),
                                    archetype_node_id="at0009",
                                    value=DVText("MS")
                                )
                            ]
                        ),
                        Element(
                            name=DVText("Gender"),
                            archetype_node_id="at0010",
                            value=DVCodedText("Female", CodePhrase("fhir-R4-administrative-gender", "female"))
                        )
                    ]
                )
            )
        ],
    )

def _get_test_person_updated(uid: HierObjectID) -> Person:
    return Person(
        actor_type=DVText("patient"),
        archetype_node_id="pyEHR-DEMOGRAPHIC-PERSON.patient.v0",
        archetype_details=Archetyped(ArchetypeID("pyEHR-DEMOGRAPHIC-PERSON.patient.v0"), "1.1.0"),
        uid=uid,
        identities=[
            PartyIdentity(
                purpose=DVText("nhs"),
                archetype_node_id="at0001",
                details=ItemTree(
                    name=DVText("tree"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("NHS Number"),
                            archetype_node_id="at0004",
                            value=DVIdentifier("9449305552", "NHS Digital", id_type="NHS Number")
                        ),
                        Cluster(
                            name=DVText("Name"),
                            archetype_node_id="at0005",
                            items=[
                                Element(
                                    name=DVText("Family Name"),
                                    archetype_node_id="at0006",
                                    value=DVText("CHISLETT")
                                ),
                                Element(
                                    name=DVText("Given Name"),
                                    archetype_node_id="at0007",
                                    value=DVText("OSCAR")
                                ),
                                Element(
                                    name=DVText("Title"),
                                    archetype_node_id="at0009",
                                    value=DVText("MR")
                                )
                            ]
                        ),
                        Element(
                            name=DVText("Gender"),
                            archetype_node_id="at0010",
                            value=DVCodedText("Male", CodePhrase("fhir-R4-administrative-gender", "male"))
                        )
                    ]
                )
            )
        ],
    )

def _get_versioned_object_contribution() -> tuple[VersionedObject, Contribution]:
    ts = PythonTerminologyService([], [TERMINOLOGY_OPENEHR])

    id2 = HierObjectID(str(uuid4()))
    vid2 = ObjectVersionID(id2.value + "::net.example.demographics::1")
    id3 = HierObjectID(str(uuid4()))
    
    p2 = Person(
        actor_type=DVText("patient"),
        archetype_node_id="pyEHR-DEMOGRAPHIC-PERSON.patient.v0",
        archetype_details=Archetyped(ArchetypeID("pyEHR-DEMOGRAPHIC-PERSON.patient.v0"), "1.1.0"),
        uid=id2,
        identities=[
            PartyIdentity(
                purpose=DVText("nhs"),
                archetype_node_id="at0001",
                details=ItemTree(
                    name=DVText("tree"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("NHS Number"),
                            archetype_node_id="at0004",
                            value=DVIdentifier("9449305994", "NHS Digital", id_type="NHS Number")
                        ),
                        Cluster(
                            name=DVText("Name"),
                            archetype_node_id="at0005",
                            items=[
                                Element(
                                    name=DVText("Family Name"),
                                    archetype_node_id="at0006",
                                    value=DVText("STAPLES")
                                ),
                                Element(
                                    name=DVText("Given Name"),
                                    archetype_node_id="at0007",
                                    value=DVText("JOSSLYN")
                                ),
                                Element(
                                    name=DVText("Title"),
                                    archetype_node_id="at0009",
                                    value=DVText("MRS")
                                )
                            ]
                        ),
                        Element(
                            name=DVText("Gender"),
                            archetype_node_id="at0010",
                            value=DVCodedText("Other", CodePhrase("fhir-R4-administrative-gender", "other"))
                        )
                    ]
                )
            )
        ],
    )

    vo = VersionedObject[Person](
        uid=id2,
        owner_id=ObjectRef("local", "PYEHR_DEMOGRAPHIC_SERVICE", InternetID("net.example.demographics")),
        time_created=DVDateTime(Env.current_date_time())
    )

    aud = AuditDetails(
        system_id="net.example.demographics",
        time_committed=DVDateTime(Env.current_date_time()),
        change_type=AuditChangeType.CREATION.value,
        committer=PartyIdentified(name="henry"),
        terminology_service=ts
    )

    vo.commit_original_version(
        a_contribution=ObjectRef("local", "CONTRIBUTION", id3),
        a_new_version_uid=vid2,
        a_preceding_version_id=None,
        an_audit=aud,
        a_lifecycle_state=VersionLifecycleState.COMPLETE.value,
        a_data=p2,
        terminology_service=ts
    )

    cont = Contribution(
        uid=id3,
        versions=[
            ObjectRef("local", "VERSION<PERSON>", vid2)
        ],
        audit=aud
    )
    return (vo, cont)

dbs_under_test = [
    pytest.param(_get_local_db_engine, id="local"),
    pytest.param(_get_mongodb_engine, id="mongodb")
]

@pytest.mark.parametrize("get_db_func", dbs_under_test)
def test_generate_hier_object_id(get_db_func):
    db = get_db_func()
    hid_set = _generate_hier_object_ids(db)
    
    # uniqueness
    assert len(hid_set) == 1000 

    # metadata generation
    hid1 = hid_set.pop()
    met1 = db.retrieve_db_metadata(HierObjectID(hid1))
    assert met1.is_deleted is None
    assert met1.obj_type is None
    assert len(met1.action_history) == 2

@pytest.mark.parametrize("get_db_func", dbs_under_test)
def test_create_and_retrieve_uid_object(get_db_func):
    db = get_db_func()
    per = _get_test_person()

    db.create_uid_object(per)

    # metadata generation (create only)
    met = db.retrieve_db_metadata(per.uid)
    assert met.is_deleted == False
    assert met.obj_type == "PERSON"
    assert len(met.action_history) == 2

    per2 = db.retrieve_uid_object("PERSON", per.uid)

    # metadata generation (read)
    met2 = db.retrieve_db_metadata(per.uid)
    assert len(met2.action_history) == 4

    assert per.is_equal(per2)

@pytest.mark.parametrize("get_db_func", dbs_under_test)
def test_update_uid_object(get_db_func):
    db = get_db_func()
    per = _get_test_person()

    db.create_uid_object(per)

    per_updated = _get_test_person_updated(per.uid)

    db.update_uid_object(per_updated)

    # metadata generation (update only)
    met = db.retrieve_db_metadata(per.uid)
    assert met.is_deleted == False
    assert met.obj_type == "PERSON"
    assert len(met.action_history) == 3

    per_updated2 = db.retrieve_uid_object("PERSON", per.uid)

    assert per_updated.is_equal(per_updated2)


@pytest.mark.parametrize("get_db_func", dbs_under_test)
def test_retrieve_query_match_object(get_db_func):    
    db = get_db_func()

    if not USE_REAL_MONGODB and isinstance(db, MongoDBDatabaseEngine):
        pytest.skip("mongomock does not support a method used by retrieve_query_match_object")

    per = _get_test_person()

    db.create_uid_object(per)

    # gets one result
    per_res = db.retrieve_query_match_object("PERSON", 
                                    archetype_id=ArchetypeID("pyEHR-DEMOGRAPHIC-PERSON.patient.v0"), 
                                    query_dict={
                                        "uid/value": [per.uid.value],
                                        "identities[at0001]/details/items[at0004]/value/id": ["9449305552"]
                                    })
    
    assert len(per_res) == 1
    assert per.is_equal(per_res[0])

    # should return no results
    per_res2 = db.retrieve_query_match_object("PERSON", 
                                    archetype_id=ArchetypeID("pyEHR-DEMOGRAPHIC-PERSON.patient.v0"), 
                                    query_dict={
                                        "identities[at0001]/details/items[at0004]/value/id": ["9449305551"]
                                    })
    
    assert len(per_res2) == 0

@pytest.mark.parametrize("get_db_func", dbs_under_test)
def test_create_and_retrieve_versioned_object(get_db_func):
    db = get_db_func()

    vo, cont = _get_versioned_object_contribution()

    db.create_versioned_object(vo, create_underlying_versions=True)
    db.create_uid_object(cont)

    vo_meta = db.retrieve_db_metadata(vo.uid)
    assert vo_meta.obj_type == "VERSIONED_OBJECT"
    assert vo_meta.is_deleted == False
    assert len(vo_meta.action_history) == 2

    vo_ret, rhis_ret = db.retrieve_versioned_object(vo.uid, metadata_only_versioned_object=False)
    assert vo.is_equal(vo_ret)
