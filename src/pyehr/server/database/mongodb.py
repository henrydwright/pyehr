import json
from logging import getLogger, Logger
from typing import Optional, Union
from uuid import uuid4
from warnings import warn

from pyehr.core.rm.ehr import EHR
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import HierObjectID, PartyRef, UIDBasedID
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.archetyped import Locatable, PyehrInternalProcessedPath
from pyehr.core.rm.common.change_control import OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import RevisionHistoryItem
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.server.database import DBActionItem, DBActionType, DBMetadata, IDatabaseEngine, IncorrectVersionTypeError, ObjectAlreadyExistsError, ObjectDoesNotExistError
from pyehr.types import get_openehr_type_str
from pyehr.utils import get_uid_from_object_if_exists

class MongoDBDatabaseEngine(IDatabaseEngine):
    """Provides a persistent pyehr database with MongoDB"""
    
    _log : Logger

    _client: MongoClient

    _database : Database

    _meta: Collection

    def __init__(self, connection_string: str, database_name: str, mongo_client: Optional[MongoClient] = None):
        """Initialise a new MongoDBDatabaseEngine, creates a new connection
        to the database
        
        :param connection_string: The connection string to be used to create a new MongoDB connection
        :param database_name: The database name within MongoDB to use for this engine
        :param mongo_client: (Optional) If provided, do not connect using connection string, and instead use the MongoClient provided"""
        self._log = getLogger("database.mongodb")
        if mongo_client is None:
            self._log.info(f"Connecting to MongoDB database at {connection_string}")
            self._client = MongoClient(connection_string)
        else:
            self._log.info(f"Using provided mongo_client")
            self._client = mongo_client
        self._log.info(f"Using database \'{database_name}\'")
        self._database = self._client.get_database(database_name)

        self._log.info("Getting 'pyehr_metadata' collection")
        self._meta = self._database.get_collection("pyehr_metadata")

    def generate_hier_object_id(self, generator = None):
        gen = str(uuid4())
        while (self._meta.find_one({"_id": gen}) is not None):
            gen = str(uuid4())
        ret_id = HierObjectID(gen)

        meta_ob = DBMetadata(
            uid=ret_id,
            obj_type=None,
            is_deleted=None,
            action_history=[
                DBActionItem(DBActionType.GENERATE_HID, party=generator)
            ],
            obj_archetype_id=None
        )

        self._meta.insert_one(meta_ob.as_json())

        self._log.info(f"{gen}:Generated")
        return ret_id
    
    def _meta_add_db_action_item(self, uid: UIDBasedID, action_item: DBActionItem):
          self._meta.update_one(
              filter={"_id": uid.value},
              update={
                  "$push": {
                      "action_history": action_item.as_json()
                      }
                  }
          )

    def retrieve_db_metadata(self, uid: Union[UIDBasedID, str], reader = None, record_audit = True):
        uid_str = None
        if isinstance(uid, UIDBasedID):
            uid_str = uid.value
        else:
            uid_str = uid

        meta = self._meta.find_one(uid_str)
        if meta is None:
            return meta
        
        meta = DBMetadata.from_json(meta)

        if record_audit:
            self._meta_add_db_action_item(uid, DBActionItem(DBActionType.READ_METADATA, party=reader))
            meta.action_history.append(DBActionItem(DBActionType.READ_METADATA, party=reader))
            self._log.info(f"{uid_str}:Retrieved metadata")
        return meta
        
    def create_uid_object(self, obj, creator: Optional[PartyRef] = None, type_override : Optional[str] = None, uid_override: Optional[str] = None):
        uid = get_uid_from_object_if_exists(obj)
        if uid is None and uid_override is None:
            raise ValueError("Cannot create object. Object did not have uid and uid_override was not set.")
        uid_str = uid.value
        if uid_override is not None:
            uid_str = uid_override
        
        meta : DBMetadata = self.retrieve_db_metadata(uid, record_audit=False)

        if meta is not None and meta.obj_type is not None:
            raise ObjectAlreadyExistsError(f"Item with UID of {uid_str} already exists in database so could not be created.")
        
        type_str = get_openehr_type_str(obj) if type_override is None else type_override
        arch_id = self._get_archetype_node_id_from_object(obj)

        if meta is None:
            meta = DBMetadata(
                uid=uid_str,
                obj_type=type_str,
                is_deleted=False,
                action_history=[],
                obj_archetype_id=arch_id
            )
            self._meta.insert_one(meta.as_json())
        else:
            self._meta.update_one(
                filter={"_id": uid_str},
                update={
                    "$set": {
                        "type": type_str,
                        "is_deleted": False
                    }
                }
            )

        type_collection = self._database.get_collection(type_str)

        obj_json = obj.as_json()
        obj_json["_id"] = uid_str

        type_collection.insert_one(obj_json)
        self._meta_add_db_action_item(uid, DBActionItem(DBActionType.CREATE, party=creator))
        self._log.info(f"{uid_str}:Created new {type_str} {'[type set explicitly]' if type_override is not None else ''} {'[uid overridden]' if uid_override is not None else ''}")

    def update_uid_object(self, obj, updater: Optional[PartyRef] = None, uid_override: Optional[str] = None):
        uid = get_uid_from_object_if_exists(obj)
        if uid is None and uid_override is None:
            raise ValueError("Cannot update object. Object did not have uid and uid_override was not set.")
        uid_str = uid.value
        if uid_override is not None:
            uid_str = uid_override

        meta = self.retrieve_db_metadata(uid, record_audit=False)
        if meta is None or (meta is not None and meta.obj_type is None):
            raise ObjectDoesNotExistError(f"Item with UID of {uid_str} did not exist in database so could not be updated")
        
        type_str = get_openehr_type_str(obj)

        collection = self._database.get_collection(type_str)
        replace_obj = obj.as_json()
        replace_obj["_id"] = uid_str

        collection.replace_one(
            filter={"_id": uid_str},
            replacement=replace_obj
        )
        self._meta_add_db_action_item(uid, DBActionItem(DBActionType.UPDATE, party=updater))
        self._log.info(f"{uid_str}:Updated {type_str}")
    
    def retrieve_uid_object(self, obj_type, uid, reader = None):
        uid_str = None
        if isinstance(uid, UIDBasedID):
            uid_str = uid.value
        else:
            uid_str = uid
        
        collection = self._database.get_collection(obj_type)

        return_obj = collection.find_one(uid_str)
        if return_obj is None:
            self._log.info(f"{uid_str}:Read attempted, but did not exist")
            return None
        
        del return_obj["_id"]
        return_obj = decode_json(return_obj)
        self._meta_add_db_action_item(uid, DBActionItem(DBActionType.READ, party=reader))

        self._log.info(f"{uid_str}:Read {obj_type}")
        return return_obj
    
    def retrieve_query_match_object(self, obj_type, archetype_id, query_dict, reader = None):
        # TODO: remove this warning once the code is written better...
        warn(UserWarning("retrieve_query_match_object for MongoDB is unoptimised and slow, and should be used with care"))
        
        self._log.info(f"QUERY:Running query for {obj_type} archetyped with {archetype_id.value} matching parameters: {json.dumps(query_dict, indent=1)}")

        collection = self._database.get_collection(obj_type)

        mongo_filter = {}
        if archetype_id is not None:
            mongo_filter = {
                "archetype_details.archetype_id.value" : archetype_id.value
            }

        candidates = collection.find(mongo_filter).to_list()

        # TODO: the code from here on out is rubbish and very slow (copied from the InMemoryDB), and should be replaced with dynamic building of a MongoDB query

        # step 3: for each item in this list, go through each item in the query dict, and keep those which match all query params
        returns = []
        for candidate in candidates:
            candidate_matched = True
            for (query_path, query_match_items) in query_dict.items():
                self._log.debug(f"[query] Finding value at path \'{str(query_path)}\'")
                
                # modified this as MongoDB already returns JSON like object
                candidate_dict = candidate

                val = self._nav_dict_path(candidate_dict, query_path)
                self._log.debug(f"[query] Value at path is \'{str(val)}\'")

                match_found = False
                for match_val in query_match_items:
                    self._log.debug(f"[query] Trying match against \'{str(match_val)}\'")
                    if val == match_val:
                        self._log.debug("[query] Matched!")
                        match_found = True

                candidate_matched = candidate_matched and match_found
                
            if candidate_matched:
                # decode here back to a pyehr object
                decodable_candidate = candidate_dict
                del decodable_candidate["_id"]
                returns.append(decode_json(candidate, target=obj_type))
        
        # step 4: log the reads in metadata
        for ret_item in returns:
            self._meta_add_db_action_item(get_uid_from_object_if_exists(ret_item), DBActionItem(DBActionType.READ, party=reader, query=query_dict))

        self._log.info(f"QUERY:Query returned {len(returns)} results")
        return returns    
    
    def create_versioned_object(self, vo, create_underlying_versions = False, creator = None):
        uid = get_uid_from_object_if_exists(vo)
        meta : DBMetadata = self.retrieve_db_metadata(uid, record_audit=False)

        if meta is not None and meta.obj_type is not None:
            raise ObjectAlreadyExistsError(f"Item with UID of {uid.value} already exists in database so could not be created.")
        
        type_str = get_openehr_type_str(vo)
        arch_id = self._get_archetype_node_id_from_object(vo)

        if meta is None:
            meta = DBMetadata(
                uid=uid,
                obj_type=type_str,
                is_deleted=False,
                action_history=[],
                obj_archetype_id=arch_id
            )
            self._meta.insert_one(meta.as_json())
        else:
            self._meta.update_one(
                filter={"_id": uid.value},
                update={
                    "$set": {
                        "type": type_str,
                        "is_deleted": False,
                        "archetype_id": arch_id
                    }
                }
            )

        vo_collection = self._database.get_collection(type_str)

        vo_json = vo.as_json(include_revision_history=True)
        vo_json["_id"] = uid.value

        vo_collection.insert_one(vo_json)
        self._meta_add_db_action_item(uid, DBActionItem(DBActionType.CREATE, party=creator))
        self._log.info(f"{uid.value}:Created new {type_str}")

        if create_underlying_versions:
            versions = vo.all_versions()
            for version in versions:
                self.create_uid_object(version)
        
    def retrieve_versioned_object(self, uid, reader = None, metadata_only_versioned_object = True):        
        vo_collection = self._database.get_collection("VERSIONED_OBJECT")

        combined_vo = vo_collection.find_one(uid.value)

        if combined_vo is None:
            self._log.info(f"{uid.value}:Read of VERSIONED_OBJECT attempted, but did not exist")
            return None
        
        rev_history_json = combined_vo["revision_history"]
        del combined_vo["revision_history"]
        del combined_vo["_id"]

        rev_history = decode_json(rev_history_json, target="REVISION_HISTORY")
        meta_only_vo = decode_json(combined_vo, target="VERSIONED_OBJECT")

        if metadata_only_versioned_object:
            self._log.info(f"{uid.value}:Retrieved VERSIONED_OBJECT (metadata and revision history only)")
            return (meta_only_vo, rev_history)
        else:
            versions = []
            for revision in rev_history.items:
                version_id = revision.version_id
                version_meta = self.retrieve_db_metadata(version_id, record_audit=False)
                if version_meta is None:
                    raise ObjectDoesNotExistError(f"Could not rebuild VERSIONED_OBJECT: version with ID \'{version_id.value}\' present in REVISION_HISTORY but not found in database.")
                version_type = version_meta.obj_type
                try:
                    versions.append(self.retrieve_uid_object(version_type, version_id, reader))
                except ValueError:
                    raise ObjectDoesNotExistError(f"Could not rebuild VERSIONED_OBJECT: version with ID \'{version_id.value}\' had valid metadata but could not be retrieved")
            full_vo = VersionedObject(
                uid=meta_only_vo.uid,
                owner_id=meta_only_vo.owner_id,
                time_created=meta_only_vo.time_created,
                revision_history_and_versions=(rev_history, versions)
            )
            self._log.info(f"{uid.value}:Retrieved VERSIONED_OBJECT (and all underlying VERSIONs)")
            return (full_vo, rev_history)
  
    def add_revision_history_item(self, uid, item, creator = None):
        vo_meta = self.retrieve_db_metadata(uid, record_audit=False)
        if vo_meta is None or vo_meta.obj_type is None:
            raise ObjectDoesNotExistError(f"Could not add new REVISION_HISTORY_ITEM as VERSIONED_OBJECT with uid \'{uid.value}\' not in database")
        
        collection = self._database.get_collection("VERSIONED_OBJECT")
        
        collection.update_one(
            filter={"_id": uid.value},
            update={
                "$push": {
                    "revision_history.items": item.as_json()
                }
            }
        )

        self._meta_add_db_action_item(uid, DBActionItem(DBActionType.UPDATE, party=creator))
        self._log.info(f"{uid.value}:Added REVISION_HISTORY_ITEM")
        

    def commit_contribution_set(self, contrib, versions, owner_id = None, committer = None):
        # ensure IDs are consistent within commit
        self._perform_pre_commit_checks(contrib, versions)

        # begin transcation to ensure whole contribution commits as a single DB transaction
        with self._client.start_session() as session:
            self._log.info(f"{contrib.uid.value}:Starting commit of CONTRIBUTION set with {len(versions)} VERSIONs")
            session.start_transaction()

            # this method is then basically identical to the reference version for InMemoryDB
            for version in versions:
                vo_uid = HierObjectID(version.owner_id().value)
                vo_meta = self.retrieve_db_metadata(vo_uid, record_audit=False)
                if vo_meta is None or vo_meta.obj_type is None:
                    if owner_id is None:
                        raise ValueError(f"Could not commit CONTRIBUTION: VERSIONED_OBJECT with UID \'{vo_uid}\' did not exist and no owner_id was provided so could not be created")
                    vo = VersionedObject(
                        uid=vo_uid,
                        owner_id=owner_id,
                        time_created=DVDateTime(Env.current_date_time())
                    )
                    self.create_versioned_object(vo, creator=committer)
            
                rhi = RevisionHistoryItem(
                    version_id=version.uid(),
                    audits=[version.commit_audit]
                )
                self.add_revision_history_item(vo_uid, rhi, creator=committer)

                # write actual version to the database
                self.create_uid_object(version, creator=committer)
            
            # then contribution!
            self.create_uid_object(contrib, creator=committer)
            session.commit_transaction()

        self._log.info(f"{contrib.uid.value}:Finished committing CONTRIBUTION set of {len(versions)} VERSIONs")

    
    def add_attestation(self, version_id, attestation, attester = None):
        # do this as a single database transaction
        with self._client.start_session() as session:
            self._log.info(f"{version_id.value}:Started adding ATTESTATION")
            session.start_transaction()
        
            # check versioned_object existence
            vo_uid = version_id.object_id()
            vo_meta = self.retrieve_db_metadata(vo_uid, record_audit=False)
            if vo_meta is None:
                raise ObjectDoesNotExistError(f"Could not add ATTESTATION as VERSIONED_OBJECT with uid \'{vo_uid.value}\' not in database")
            
            vo, rh = self.retrieve_versioned_object(vo_uid)
            rev_history_item_exists = False
            for rev_history_item in rh.items:
                if rev_history_item.version_id.value == version_id.value:
                    rev_history_item_exists = True
                    break
            
            if not rev_history_item_exists:
                raise ObjectDoesNotExistError(f"Could not add ATTESTATION as REVISION_HISTORY did not contain version with ID \'{version_id.value}\'")
            
            # check version is in the versioned_object
            vers_meta = self.retrieve_db_metadata(version_id, record_audit=False)
            if vers_meta is None:
                raise ObjectDoesNotExistError(f"Could not add ATTESTATION as VERSION with ID \'{version_id.value}\' not in database")
            
            ver = self.retrieve_uid_object(vers_meta.obj_type, version_id)
            if not isinstance(ver, OriginalVersion):
                raise IncorrectVersionTypeError(f"Could not add ATTESTATION as VERSION with ID \'{version_id.value}\' was not an ORIGINAL_VERSION")
            
            # add the ATTESTATION to the VERSION
            ver_collection = self._database.get_collection(vers_meta.obj_type)
            
            if ver.attestations is None:
                ver_collection.update_one(
                    filter={"_id": version_id.value},
                    update={
                        "$set": {
                            "attestations": [attestation.as_json()]
                        }
                    }
                )
            else:
                ver_collection.update_one(
                    filter={"_id": version_id.value},
                    update={
                        "$push": {
                            "attestations": attestation.as_json()
                        }
                    }
                )
            
            self._meta_add_db_action_item(version_id, DBActionItem(DBActionType.UPDATE_VERSION_ATTESTATIONS, party=attester))

            # add the ATTESTATION to the REVISION_HISTORY of the VERSIONED_OBJECT
            vo_collection = self._database.get_collection("VERSIONED_OBJECT")
            vo_collection.update_one(
                filter={
                    "_id": vo_uid.value,
                    "revision_history.items.version_id.value": version_id.value},
                update={
                    "$push": {
                        "revision_history.items.$.audits": attestation.as_json()
                    }
                }
            )
            self._meta_add_db_action_item(vo_uid, DBActionItem(DBActionType.UPDATE, party=attester))
            session.commit_transaction()
        self._log.info(f"{version_id.value}:Finished adding ATTESTATION")
            
    def add_to_ehr_lists(self, ehr_id, addition, adder = None):
        meta = self.retrieve_db_metadata(ehr_id, reader=adder, record_audit=False)
        if meta is None or meta.obj_type is None or meta.obj_type != "EHR":
            raise ValueError(f"Cannot add items to lists in EHR \'{ehr_id.value}\' as it did not exist")
        
        ehr_collection = self._database.get_collection("EHR")
        ehr : EHR = decode_json(ehr_collection.find_one(filter={"_id": ehr_id.value}), target="EHR")

        update_dict = None
        if addition.ref_type == "CONTRIBUTION":
            if ehr.contributions is None:
                update_dict = {
                    "$set" : {"contributions": [addition.as_json()]}
                }
            else:
                update_dict = {
                    "$push": {"contributions": addition.as_json()}
                }
        elif addition.ref_type == "VERSIONED_COMPOSITION":
            if ehr.compositions is None:
                update_dict = {
                    "$set": {"compositions": [addition.as_json()]}
                }
            else:
                update_dict = {
                    "$push": {"compositions": addition.as_json()}
                }
        elif addition.ref_type == "VERSIONED_FOLDER":
            if ehr.folders is None:
                update_dict = {
                    "$set": {"folders": [addition.as_json()]}
                }
            else:
                update_dict = {
                    "$push": {"folders": addition.as_json()}
                }
        else:
            raise ValueError("Could not add reference as it was not of type CONTRIBUTION, VERSIONED_FOLDER or VERSIONED_COMPOSITION")
        
        ehr_collection.update_one(
            filter = {"_id": ehr_id.value},
            update=update_dict
        )
        
        self._meta_add_db_action_item(ehr_id, DBActionItem(DBActionType.UPDATE, party=adder))
        self._log.info(f"{ehr_id.value}:Added reference to {addition.ref_type} to EHR.")

