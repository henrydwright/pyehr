

from uuid import uuid4

from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.aql import parse_aql
from pyehr.server.database import IDatabaseEngine
from pyehr.server.database.mongodb import MongoDBDatabaseEngine

from pymongo import MongoClient
import pytest
import mongomock

from test.pyehr.server.db_test_data import create_test_data
from os import getenv
from dotenv import load_dotenv

load_dotenv()
USE_REAL_MONGODB = (getenv("PYEHR_TEST_USE_REAL_MONGODB") is not None)

@pytest.fixture(scope="module")
def mongodb(request: pytest.FixtureRequest):
    db = None
    if USE_REAL_MONGODB:
        client = MongoClient("mongodb://localhost:27017/?directConnection=true")
        db_name = f"testdb-{str(uuid4())}"
        db = MongoDBDatabaseEngine("mongodb://localhost:27017/?directConnection=true", db_name, mongo_client=client)
        request.addfinalizer(lambda: client.drop_database(db_name))
    else:
        db = MongoDBDatabaseEngine("mongodb://localhost:27017/?directConnection=true", f"testdb-{str(uuid4())}", mongo_client=mongomock.MongoClient("mongodb://localhost:27017/?directConnection=true"))

    create_test_data(db)
    return db
    

def test_single_no_predicate_from(mongodb: MongoDBDatabaseEngine):
    r = mongodb.execute_aql_query(parse_aql("SELECT e/system_id/value AS sys_id, e/ehr_id/value AS ehr_id FROM EHR e"), _mongomock_compatibility_fixes=(not USE_REAL_MONGODB))

    assert (len(r.rows)==5)

    assert r.columns[0][0] == "sys_id"
    assert r.columns[0][1] == "/system_id/value"
    assert r.columns[1][0] == "ehr_id"
    assert r.columns[1][1] == "/ehr_id/value"

    expected_ehr_id_set = set(["8d7f36c1-c2d0-4332-895c-4a3cab3446b6", "209ff927-3777-4360-b09c-f8e50ae5b1e7", "a2906af1-cc9f-4ef2-879b-9a3c22737b23", "726f23bb-5b8d-4b24-bb7e-545fc698b068", "def83fa8-3c37-4fd4-89ec-143de9401563"])
    actual_ehr_id_set = set()

    for row in r.rows:
        assert row[0] == "8addce0e-2289-420e-adf8-3400907c0d3e"
        actual_ehr_id_set.add(row[1])

    assert is_equal_value(expected_ehr_id_set, actual_ehr_id_set)

def test_single_with_predicate_from(mongodb: MongoDBDatabaseEngine):
    r = mongodb.execute_aql_query(parse_aql("SELECT p/uid/value FROM PERSON p [pyehr-DEMOGRAPHIC-PERSON.nhs_patient.v0]"), _mongomock_compatibility_fixes=(not USE_REAL_MONGODB))

    assert (len(r.rows)==3)
    assert r.columns[0][0] == "#0"
    assert r.columns[0][1] == "/uid/value"

    expected_person_id_set = set(["0c4823c7-15f0-4310-991d-ab4a7a35d11e", "01302448-0377-4dcd-be5f-9f16bad3812b", "f6f094c5-b21b-4dd6-8b53-d99437fa25e6"])
    actual_person_id_set = set()
    for row in r.rows:
        actual_person_id_set.add(row[0])
    assert is_equal_value(expected_person_id_set, actual_person_id_set)

def test_single_contains_no_predicate_from(mongodb: MongoDBDatabaseEngine):
    if not USE_REAL_MONGODB:
        pytest.skip("Mongomock doesn't implement the required 'pipeline' operator within $lookup so this can't be tested")
    r = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS ehr_id, es/subject/name AS subject FROM EHR e CONTAINS EHR_STATUS es"))

    assert len(r.rows) == 5

    expected_row_tuples = [(
        "8d7f36c1-c2d0-4332-895c-4a3cab3446b6",
        "AINDOW, Comfort Zula"
    ),
        (
        "209ff927-3777-4360-b09c-f8e50ae5b1e7",
        "CHISLETT, Octavia"
        ),
        (
        "a2906af1-cc9f-4ef2-879b-9a3c22737b23",
        "SHIPPERBOTTOM, Beryl"
        ),
        (
        "726f23bb-5b8d-4b24-bb7e-545fc698b068",
        "ANDERTON, Briar Chadwick"
        ),
        (
        "def83fa8-3c37-4fd4-89ec-143de9401563",
        "GILMAN, Percy"
        )]
    expected_row_set = set(expected_row_tuples)
    actual_row_set = set()
    for row in r.rows:
        actual_row_set.add((row[0], row[1]))

    assert is_equal_value(expected_row_set, actual_row_set)

def test_single_contains_predicate_from(mongodb: MongoDBDatabaseEngine):
    if not USE_REAL_MONGODB:
         pytest.skip("Mongomock doesn't implement the required 'pipeline' operator within $lookup so this can't be tested")
    r = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS id FROM EHR e CONTAINS EHR_STATUS es [openEHR-EHR-EHR_STATUS.generic.v2]"))
    assert len(r.rows) == 0

    r2 = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS id FROM EHR e CONTAINS EHR_STATUS es [openEHR-EHR-EHR_STATUS.generic.v1]"))
    assert len(r2.rows) == 5

def test_contains_chain_from(mongodb: MongoDBDatabaseEngine):
    if not USE_REAL_MONGODB:
         pytest.skip("Mongomock doesn't implement the required 'pipeline' operator within $lookup so this can't be tested")
    
    r = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS p_id, c/uid/value AS c_id FROM EHR e CONTAINS COMPOSITION c CONTAINS ACTION act"))
    assert len(r.rows) == 1
    assert r.rows[0][0] == "8d7f36c1-c2d0-4332-895c-4a3cab3446b6"

    r2 = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS p_id, c/uid/value AS c_id FROM EHR e CONTAINS COMPOSITION c CONTAINS ACTION act [openEHR-EHR-ACTION.medication.v1]"))
    assert len(r2.rows) == 1
    assert r2.rows[0][0] == "8d7f36c1-c2d0-4332-895c-4a3cab3446b6"

    r3 = mongodb.execute_aql_query(parse_aql("SELECT e/ehr_id/value AS p_id, c/uid/value AS c_id FROM EHR e CONTAINS COMPOSITION c CONTAINS ACTION act [openEHR-EHR-ACTION.other.v1]"))
    assert len(r3.rows) == 0