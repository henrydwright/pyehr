import logging
from typing import Union

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.database import Database

from pyehr.core.rm.common.change_control import Version, VersionedObject
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.utils import PYTHON_TYPE_TO_STRING_TYPE_MAP
from pyehr.core.rm.demographic import Party
from pyehr.server.database import IDatabaseEngine
from pyehr.core.its.json_tools import decode_json

# TODO: redo this now the interface has been rewritten
class MongoDBDatabaseEngine(IDatabaseEngine):

    _client : MongoClient

    _database: Database

    _logger: logging.Logger

    def _decode_json(self, json_obj, target):
        return decode_json(json_obj, target, flag_allow_resolved_references=False, flag_infer_missing_type_details=False)

    def __init__(self, connection_string: str, database_name: str):
        self._logger = logging.getLogger("database.mongo")
        try:
            self._client = MongoClient(connection_string)
            self._logger.info("Connected to MongoDB at " + str(self._client.address))
            self._database = self._client.get_database(database_name)
            self._logger.info(f"Using database name=\'{database_name}\'")
        except Exception as e:
            self._logger.error("Could not connect to database. Exception details: " + str(e))
        super().__init__()

    def create_uid_object(self, obj: Union[Party, Version]):
        try:
            attempted_id = obj.uid.value
            collection_name = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]
            collection = self._database.get_collection(collection_name)
            db_obj = obj.as_json()
            db_obj["_id"] = attempted_id
            collection.insert_one(db_obj)
            self._logger.info(f"Inserted \'{collection_name}\' with UID \'{attempted_id}\' into database")
        except DuplicateKeyError as dke:
            self._logger.error(f"Could not insert \'{collection_name}\' with UID of \'{attempted_id}\', as this object already exists in the database. Exception details: " + str(dke))
            raise RuntimeError(f"Could not insert \'{collection_name}\' with UID of \'{attempted_id}\', as this object already exists in the database. Exception details: " + str(dke))
    
    def retrieve_query_match_object(self, obj_type, archetype_id, query_dict):
        return super().retrieve_query_match_object(obj_type, archetype_id, query_dict)
    
    def retrieve_uid_object(self, obj_type, uid):
        collection = self._database.get_collection(obj_type)
        db_obj = collection.find_one({"_id": uid.value})
        if db_obj is not None:
            del db_obj["_id"]
            self._logger.info(f"Retrieved \'{obj_type}\' with UID of '{uid.value}'")
            return self._decode_json(db_obj, obj_type)
        else:
            self._logger.info(f"Could not find \'{obj_type}\' with UID of '{uid.value}'")
            return None
    


