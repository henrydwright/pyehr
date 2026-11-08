import json
from logging import getLogger, Logger
from typing import Optional, Union
from uuid import uuid4
from warnings import warn

from pyehr.core.its.aql import AQLResultSet, AQLResultSetMetadata
from pyehr.core.its.aql.process import CONTAINS_RM_MAP
from pyehr.core.its.aql.query import AQLComparisonOperator, AQLDataMatchPath, AQLFromClause, AQLModelTypeTreeConstraint, AQLModelTypeTreeNode, AQLPrimitiveLiteral, AQLQuery, AQLSelectClause, AQLWhereClause, AQLWhereTreeBinaryExpr, AQLWhereTreeComparisonLeaf, AQLWhereTreeNode
from pyehr.core.rm.ehr import EHR
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import UUID, HierObjectID, PartyRef, UIDBasedID
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.archetyped import Locatable, PyehrInternalProcessedPath
from pyehr.core.rm.common.change_control import OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import RevisionHistoryItem
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.server.database import AQLExecuteFailure, AQLNotSupportedError, DBActionItem, DBActionType, DBMetadata, IDatabaseEngine, IncorrectVersionTypeError, ObjectAlreadyExistsError, ObjectDoesNotExistError
from pyehr.types import get_openehr_type_str
from pyehr.utils import get_uid_from_object_if_exists

__all__ = ['MongoDBDatabaseEngine']


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
        if isinstance(uid, str):
            uid_str = uid
        else:
            uid_str = uid.value

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
        if isinstance(uid, str):
            uid_str = uid
        else:
            uid_str = uid.value
        
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

    def _process_from_clause_recurse(self, parent_type: str, parent_var: str, node: AQLModelTypeTreeNode, pipeline: list, path_dict: dict[str, str]):
        if node is None:
            return
        elif isinstance(node, AQLModelTypeTreeConstraint):
            parent_map = CONTAINS_RM_MAP.get(parent_type)
            if parent_map is None:
                raise AQLExecuteFailure(f"No possible CONTAINS relationship exists for type \'{parent_type}\'")
            container = parent_map.get(node.model_type.type_name)
            if container is None:
                raise AQLExecuteFailure(f"No CONTAINS relationship possible between \'{parent_type}\' and \'{node.model_type}\'")

            parent_path = path_dict[parent_var]
            attr_name = container[0]
            is_ref = container[1]
            is_versioned_obj = container[2]
            is_multiple = container[3]

            # lookup/join relevant data
            if is_ref:
                if is_versioned_obj:
                    self._log.info(f"pipeline: add REF/VO at {parent_path}.{attr_name}.id.value AS {node.model_type.variable_name}")
                    pipeline.append({
                        "$lookup": {
                            "from": "VERSIONED_OBJECT",
                            "localField": f"{parent_path}.{attr_name}.id.value",
                            "foreignField": "uid.value",
                            "as": f"{node.model_type.variable_name}_vo",
                            "pipeline": [
                                {
                                    "$project": {
                                        "_id": 0,
                                        "latest_revision_history_item": {
                                            "$last": "$revision_history.items"
                                        }
                                    }
                                },
                                {
                                    "$project": {
                                        "latest_version_id": "$latest_revision_history_item.version_id.value"
                                    }
                                }
                            ]
                        }
                    })
                    pipeline.append({
                        "$unwind": f"${node.model_type.variable_name}_vo"
                    })
                    pipeline.append({
                        "$lookup": {
                            "from": f"VERSION<{node.model_type.type_name}>",
                            "localField": f"{node.model_type.variable_name}_vo.latest_version_id",
                            "foreignField": "_id",
                            "as": node.model_type.variable_name,
                            "pipeline": [
                                {
                                    "$project": {
                                        "_id": 0,
                                        "data": 1
                                    }
                                },
                                {
                                    "$replaceRoot": {
                                        "newRoot": "$data"
                                    }
                                }
                            ]
                        }
                    })
                    pipeline.append({
                        "$unwind": f"${node.model_type.variable_name}"
                    })
                    path_dict[node.model_type.variable_name] = node.model_type.variable_name
                else:
                    self._log.info(f"pipeline: add REF at {parent_path}.{attr_name}.id.value AS {node.model_type.variable_name}")
                    pipeline.append({
                        "$lookup": {
                            "from": f"{node.model_type}",
                            "localField": f"{parent_path}.{attr_name}.id.value",
                            "foreignField": "_id",
                            "as": node.model_type.variable_name
                        }
                    })
                    pipeline.append({
                        "$unwind": {
                            "path": f"${node.model_type.variable_name}"
                        }
                    })
                    path_dict[node.model_type.variable_name] = node.model_type.variable_name
            else:
                if is_multiple:
                    self._log.info(f"pipeline: add MULTPATH at {parent_path}.{attr_name} AS {node.model_type.variable_name}")
                    pipeline.append({
                        "$set": {
                            node.model_type.variable_name: f"${parent_path}.{attr_name}"
                        }
                    })
                    pipeline.append({
                        "$unwind": {
                            "path": ("$" + node.model_type.variable_name)
                        }
                    })
                else:
                    self._log.info(f"pipeline: add SINGPATH at {parent_path}.{attr_name} AS {node.model_type.variable_name}")
                
                # match on type
                # TODO: this will fail for inherited types and will need fixing later on
                pipeline.append({
                    "$match": {
                        f"{node.model_type.variable_name}._type": node.model_type.type_name
                    }
                })
                path_dict[node.model_type.variable_name] = node.model_type.variable_name
                

            if node.model_type.archetype_id_predicate is not None:
                pipeline.append({
                    "$match": {
                        f"{path_dict[node.model_type.variable_name]}.archetype_details.archetype_id.value" : {
                            "$eq": node.model_type.archetype_id_predicate.value
                        }
                    }
                })

            self._process_from_clause_recurse(node.model_type.type_name, node.model_type.variable_name, node.contains, pipeline, path_dict)
        else:
            raise AQLNotSupportedError("MongoDB/AQL/FROM: engine does not support OR, AND or NOT in FROM clause")

    
    def _process_from_clause(self, from_clause: AQLFromClause) -> tuple[str, list[object], dict[str, str]]:
        """Takes contents of a FROM clause and produces aggregation pipeline stages plus a mapping
        between named FROM clause variables and their path within the object created by the pipeline
        stage.
        
        :returns: Tuple with 0: collection to selection from, 1: aggergation pipeline, 2: mapping from
                  variable name to path within the object at the end of the pipeline.
        :raises AQLExecuteFailure: If an invalid CONTAINS is given.
        :raises AQLNotSupportedError: If an archetype predicate, AND, OR or NOT is found."""
        t = from_clause.model_type_constraint

        root_type = t.model_type.type_name
        root_var = t.model_type.variable_name

        path_dict = {
            root_var: root_var
        }
        pipeline = []

        if t.model_type.archetype_id_predicate is not None:
            pipeline.append({
                "$match" : {
                    "archetype_details.archetype_id.value": {
                        "$eq": t.model_type.archetype_id_predicate.value
                    }
                }
            })

        pipeline.append({
            "$project" : {
                "_id": 0,
                root_var: "$$ROOT"
            }
        })

        self._process_from_clause_recurse(root_type, root_var, t.contains, pipeline, path_dict)

        return (root_type, pipeline, path_dict)

    def _aql_data_match_path_to_mdb_expression(self, dmp: AQLDataMatchPath) -> object:
        project_obj = {}
        current_project_obj = project_obj
        last_project_obj = {}
        for path_seg in reversed(dmp.path_segments):
            if path_seg.predicate_string is not None and path_seg.predicate_string[:2] == "at" and len(path_seg.predicate_string) == 6:
                current_project_obj["$arrayElemAt"] = [
                            {"$map": 
                                {"input": {
                                    "$filter": {
                                        "input": {
                                            "$getField": {
                                                "field": path_seg.attribute_id,
                                                "input": {}
                                            }
                                        },
                                        "as": "map_field",
                                        "cond": {"$eq": ["$$map_field.archetype_node_id", path_seg.predicate_string]}
                                    }
                                }, 
                                "as": "map_field",
                                "in": "$$map_field"}},0]
                last_project_obj = current_project_obj["$arrayElemAt"][0]["$map"]["input"]["$filter"]["input"]["$getField"]
                current_project_obj = current_project_obj["$arrayElemAt"][0]["$map"]["input"]["$filter"]["input"]["$getField"]["input"]
            elif path_seg.predicate_tree is not None:
                raise AQLNotSupportedError("MongoDB/AQL/SELECT: Only [atXXXX] predicates are supported in SELECT paths, not more complex predicates")
            else:
                current_project_obj["$getField"] = {"field": path_seg.attribute_id, "input": {}}
                last_project_obj = current_project_obj["$getField"]
                current_project_obj = current_project_obj["$getField"]["input"]
        last_project_obj["input"] = f"${dmp.variable_name}"
        return project_obj


    def _process_select_clause(self, select_clause: AQLSelectClause) -> tuple[object, list[tuple[str, str]]]:
        """Takes the contents of a SELECT clause and produces the contents of a $project operation
        plus the required column specifications for the return of an AQL RESULT_SET
        :returns: Tuple with 0: contents of $project operation, 1: list of columns in RESULT_SET format"""
        top_projects = {"_id": 0}
        result_cols = []
        for i in range(len(select_clause.result_columns)):
            col = select_clause.result_columns[i]
            col_val = col.value
            col_nm = col.alias if col.alias is not None else f"#{str(i)}"
            if isinstance(col_val, AQLDataMatchPath):
                project_obj = self._aql_data_match_path_to_mdb_expression(col_val)
                result_path = "".join([ps.as_aql() for ps in col_val.path_segments])
                self._log.info(f"Will set {col_nm} to {str(project_obj)}")
                top_projects[col_nm] = {"$ifNull": [project_obj, None]} # project_obj
                result_cols.append((col_nm, result_path))
            else:
                raise AQLNotSupportedError("MongoDB/AQL/SELECT: Only data match column specifications are supported (not parameters nor function calls)")

        return (top_projects, result_cols)

    _AQL_COMPARISON_TO_MDB = {
        AQLComparisonOperator.EQUAL : "$eq",
        AQLComparisonOperator.GREATER_THAN : "$gt",
        AQLComparisonOperator.GREATER_THAN_OR_EQUAL_TO: "$gte",
        AQLComparisonOperator.NOT_EQUAL_TO: "$ne",
        AQLComparisonOperator.SMALLER_THAN: "$lt",
        AQLComparisonOperator.SMALLER_THAN_OR_EQUAL_TO: "$lte"
    }

    def _process_where_clause_recurse(self, node: AQLWhereTreeNode, add_field_dict: object, add_field_map: dict[str, str]) -> object:
        """Recurses down a where node tree and returns the contents of the $match expression for this
        part of the tree. Adds to the add_field_dict as it goes, using add_field_map to lookup the temporary
        field name for a given path needed in the WHERE clause"""
        t = node
        if isinstance(t, AQLWhereTreeComparisonLeaf):
            if isinstance(t.op1, AQLDataMatchPath):
                if isinstance(t.op2.value, AQLPrimitiveLiteral):
                    if t.op1.as_aql() not in add_field_map:
                        new_field_name = f"pyehr-where-{str(uuid4())}"
                        add_field_map[t.op1.as_aql()] = new_field_name
                        add_field_dict[new_field_name] = self._aql_data_match_path_to_mdb_expression(t.op1)
                    
                    where_field_name = add_field_map[t.op1.as_aql()]
                    
                    self._log.info(f"Will set {where_field_name} to path {t.op1.as_aql()} and match with {str(t.op2.value.value)}")
                    return {
                        where_field_name: {self._AQL_COMPARISON_TO_MDB[t.operand]: str(t.op2.value.value)}
                    }
                else:
                    raise AQLNotSupportedError("MongoDB/AQL/WHERE: Only literal values are supported as right operand for comparison expression in WHERE clause.")
            else:
                raise AQLNotSupportedError("MongoDB/AQL/WHERE: Only data match paths are supported as left operand for comparison expression in WHERE clause.")
        elif isinstance(t, AQLWhereTreeBinaryExpr):
            if t.operand == "OR":
                return {
                    "$or": [
                        self._process_where_clause_recurse(t.op1, add_field_dict, add_field_map),
                        self._process_where_clause_recurse(t.op2, add_field_dict, add_field_map)
                    ]
                }
            else:
                return {
                    "$and": [
                        self._process_where_clause_recurse(t.op1, add_field_dict, add_field_map),
                        self._process_where_clause_recurse(t.op2, add_field_dict, add_field_map)
                    ]
                }
        else:
            raise AQLNotSupportedError("MongoDB/AQL/WHERE: Only singular comparison is supported.")



    def _process_where_clause(self, where_clause: Optional[AQLWhereClause], pipeline: list):
        """Takes the contents of a WHERE clause plus a pipeline produced by the FROM clause and adds
        relevant pipeline stages to meet the filters of the where clause. Does not return a value."""
        if where_clause is None:
            return
        t = where_clause.where_expression_tree
        add_field_dict = {}
        field_map = {}
        match_obj = {
            "$match": self._process_where_clause_recurse(t, add_field_dict, field_map)
        }
        pipeline.append({
            "$addFields": add_field_dict
        })
        pipeline.append(match_obj)

    def execute_aql_query(self, aql_query: AQLQuery, _mongomock_compatibility_fixes=False) -> AQLResultSet:
        self._log.info("Executing AQL query: " + aql_query.as_aql())

        # build the base lookup model from the FROM clause before refining
        top_type, pipeline, path_dict = self._process_from_clause(aql_query.from_clause)

        top_collect = self._database.get_collection(top_type)

        self._process_where_clause(aql_query.where_clause, pipeline)

        # project out paths from the SELECT clause
        top_projects, result_cols = self._process_select_clause(aql_query.select_clause)

        pipeline.append(
            {
                "$project": top_projects
            }
        )
        self._log.info("Will run pipeline: " + str(pipeline) + "\n\n")
        if _mongomock_compatibility_fixes:
            r = list(top_collect.aggregate(pipeline))
        else:
            r = top_collect.aggregate(pipeline).to_list()

        self._log.info(f"Result has {len(r)} rows")

        # process the list of objects that MongoDB returns into a list of lists
        result_rows = []
        for doc in r:
            result_rows.append(list(doc.values()))

        r = AQLResultSet(
            q=aql_query,
            meta=AQLResultSetMetadata(created=Env.current_date_time(), generator="pyehr.server.database.mongodb", executed_aql=aql_query.as_aql()),
            columns=result_cols,
            rows=result_rows)

        return r

