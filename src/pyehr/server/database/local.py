from logging import getLogger, Logger
import json

from pyehr.core.rm.common.archetyped import PyehrInternalPathPredicateType, PyehrInternalProcessedPath
from pyehr.core.rm.common.change_control import OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.ehr import EHR
from pyehr.utils import PYTHON_TYPE_TO_STRING_TYPE_MAP

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef
from pyehr.server.database import DBActionItem, DBActionType, IDatabaseEngine, DBMetadata

from uuid import uuid4


class InMemoryDB(IDatabaseEngine):
    """In memory 'database' designed for exploration and testing use. Does NOT persist data."""

    _log : Logger

    _meta : dict[str, DBMetadata]
    # dict between uid (as string) -> metadata

    _obj : dict[str, dict[str, IDatabaseEngine.UID_OBJECT_TYPE]]
    # dict between object_type -> uid (as string) -> object

    def __init__(self):
        self._log = getLogger("InMemoryDB")
        self._meta = dict()
        self._obj = dict()
        self._obj["REVISION_HISTORY"] = dict()
        self._log.info("Started new InMemoryDB, note data is NOT persisted.")
        super().__init__()

    def generate_hier_object_id(self, generator=None):
        gen = str(uuid4())
        # ensure uniqueness within database
        while (gen in self._meta):
            gen = str(uuid4())
        ret_id = HierObjectID(gen)
        self._meta[gen] = DBMetadata(
            uid=ret_id,
            obj_type=None,
            is_deleted=None,
            action_history=[
                DBActionItem(DBActionType.GENERATE_HID, party=generator)
            ]
        )
        self._log.info(f"{gen}:Generated")
        return ret_id
        
    def add_revision_history_item(self, uid, item, creator = None):
        if uid.value not in self._meta:
            raise ValueError(f"Could not add new REVISION_HISTORY_ITEM as VERSIONED_OBJECT with uid \'{uid.value}\' not in database")
        
        if uid.value not in self._obj["REVISION_HISTORY"]:
            self._obj["REVISION_HISTORY"] = RevisionHistory(
                items=[]
            )
        
        rh = self._obj["REVISION_HISTORY"][uid.value]
        rh.items.append(item)

        vo_meta = self._meta[uid.value]
        vo_meta.action_history.append(DBActionItem(DBActionType.UPDATE, party=creator))
        self._log.info(f"{uid.value}:Added REVISION_HISTORY_ITEM")

    def add_attestation(self, version_id, attestation, attester = None):
        # check versioned_object existance
        vo_uid = version_id.object_id()
        if vo_uid.value not in self._meta:
            raise ValueError(f"Could not add ATTESTATION as VERSIONED_OBJECT with uid \'{vo_uid.value}\' not in database")
        
        if vo_uid.value not in self._obj["REVISION_HISTORY"]:
            raise ValueError(f"Could not add ATTESTATION as no REVISION_HISTORY existed for VERSIONED_OBJECT with uid \'{vo_uid.value}\'")
        
        vo_meta = self._meta[vo_uid.value]
        rev_his = self._obj["REVISION_HISTORY"][vo_uid.value]

        # check version is in the versioned_object
        rh_item_to_update = None
        for rh_item in rev_his.items:
            if rh_item.version_id.value == version_id.value:
                rh_item_to_update = rh_item

        if rh_item is None:
            raise ValueError(f"Could not add ATTESTATION as REVISION_HISTORY did not contain version with ID \'{version_id.value}\'")
        
        # check version is in the database
        if version_id.value not in self._meta:
            raise ValueError(f"Could not add ATTESTATION as VERSION with ID \'{version_id.value}\' not in database")
        
        # add the attestation
        ver_meta = self._meta[version_id.value]
        ver = self._obj[ver_meta.obj_type][version_id.value]
        if not isinstance(ver, OriginalVersion):
            raise ValueError(f"Could not add ATTESTATION as VERSION with ID \'{version_id.value}\' was not an ORIGINAL_VERSION")
        
        if ver.attestations is None:
            ver.attestations = []
        ver.attestations.append(attestation)
        ver_meta.action_history.append(DBActionItem(DBActionType.UPDATE_VERSION_ATTESTATIONS, party=attester))

        rh_item_to_update.audits.append(attestation)
        vo_meta.action_history.append(DBActionItem(DBActionType.UPDATE, party=attester))
        self._log.info(f"{version_id.value}:Added ATTESTATION")

    
    def _get_uid_from_uid_object_type(self, obj):
        if isinstance(obj, EHR):
            return obj.ehr_id
        uid = obj.uid
        if callable(uid):
            uid = obj.uid()
        return uid

    def create_uid_object(self, obj, creator = None):
        met = None
        uid = self._get_uid_from_uid_object_type(obj)
        if uid.value in self._meta:
            met = self._meta[uid.value]
            if met.obj_type is not None:
                raise ValueError(f"Item with UID of {uid.value} already exists in database so could not be created.")

        type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

        if type_str == "VERSION":
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

        if uid.value not in self._meta:
            met = DBMetadata(
                uid=uid,
                obj_type=type_str,
                is_deleted=False,
                action_history=[]
            )
            self._meta[uid.value] = met
        else:
            met.obj_type = type_str
            met.is_deleted = False

        if type_str not in self._obj:
            self._obj[type_str] = dict()

        self._obj[type_str][uid.value] = obj

        met.action_history.append(DBActionItem(DBActionType.CREATE, party=creator))
        self._log.info(f"{uid.value}:Created new {type_str}")
    
    def update_uid_object(self, obj, updater = None):
        uid = self._get_uid_from_uid_object_type(obj)
        met = None
        if uid.value in self._meta:
            met = self._meta[uid.value]
            if met.obj_type is None:
                raise ValueError(f"Item with UID of {uid.value} did not exist in database so could not be updated")
        else:
            raise ValueError(f"Item with UID of {uid.value} did not exist in database so could not be updated")
        
        type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

        if type_str == "VERSION":
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

        self._obj[type_str][uid.value] = obj
        met.action_history.append(DBActionItem(DBActionType.UPDATE, party=updater))
        self._log.info(f"Updated {type_str} with UID {uid.value}")
    
    def retrieve_db_metadata(self, uid, reader = None):
        if uid.value not in self._meta:
            return None
        met = self._meta[uid.value]
        met.action_history.append(DBActionItem(DBActionType.READ_METADATA, party=reader))
        self._log.info(f"{uid.value}:Retrieved metadata")
        return met
    
    def _nav_dict_path(self, js_dict, path):
        """Navigate to a pyehr path within an as_json() dict output"""
        if path is None:
            return js_dict
        proc = PyehrInternalProcessedPath(path)
        if proc.is_self_path():
            return js_dict
        
        next_el = js_dict[proc.current_node_attribute]

        if isinstance(next_el, list):
            if proc.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
                next_el = next_el[int(proc.current_node_predicate)]
            elif proc.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
                found_match = False
                for el in next_el:
                    if el["archetype_node_id"] == proc.current_node_predicate:
                        found_match = True
                        next_el = el
                if not found_match:
                    raise ValueError(f"Could not find node matching `{proc.current_node_predicate}` in list")
            
        return self._nav_dict_path(next_el, proc.remaining_path)

    
    def retrieve_query_match_object(self, obj_type, archetype_id, query_dict, reader = None):
        # this method would be horrificly slow, but given lack of persistence it doesn't matter!
        self._log.info(f"QUERY:Running query for {obj_type} archetyped with {archetype_id.value} matching parameters: {json.dumps(query_dict, indent=1)}")
        # step 1: check any objects of this type exist
        if obj_type not in self._obj:
            return []
        
        # step 2: if they do, then find ones which match the given archetype ID
        candidates = []
        for obj in self._obj[obj_type].values():
            if obj.archetype_node_id == archetype_id.value:
                candidates.append(obj)

        # step 3: for each item in this list, go through each item in the query dict, and keep those which match all query params
        returns = []
        for candidate in candidates:
            candidate_matched = True
            for (query_path, query_match_items) in query_dict.items():
                self._log.debug(f"[query] Finding value at path \'{str(query_path)}\'")
                candidate_dict = candidate.as_json()

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
                returns.append(candidate)

        # step 4: for those we are returning, log that a read has happened
        for ret_item in returns:
            ret_meta = self._meta[ret_item.uid.value]
            ret_meta.action_history.append(DBActionItem(DBActionType.READ, party=reader, query=query_dict))

        self._log.info(f"QUERY:Query returned {len(returns)} results")
        return returns
    
    def retrieve_uid_object(self, obj_type, uid, reader = None):
        if uid.value not in self._meta:
            # object with given uid does not exist in database
            self._log.info(f"{uid.value}:Read attempted, but did not exist")
            return None
        
        met = self._meta[uid.value]
        met.action_history.append(DBActionItem(DBActionType.READ, party=reader))

        self._log.info(f"{uid.value}:Read {obj_type}")
        return self._obj[obj_type][uid.value]
        
    def create_versioned_object(self, vo, create_underlying_versions=False, creator = None):
        vo_meta_only = VersionedObject(
            uid=vo.uid,
            owner_id=vo.owner_id,
            time_created=vo.time_created
        )
        self.create_uid_object(vo_meta_only, creator)

        self._obj["REVISION_HISTORY"][vo.uid.value] = vo.revision_history()
        if create_underlying_versions:
            vers = vo.all_versions()
            for ver in vers:
                self.create_uid_object(ver)
    
    def retrieve_versioned_object(self, uid, reader = None, metadata_only_versioned_object = True):
        if uid.value not in self._meta:
            raise ValueError("VERSIONED_OBJECT with given UID does not exist in database")
        
        met = self._meta[uid.value]
        met.action_history.append(DBActionItem(DBActionType.READ, party=reader))

        meta_only_vo = self._obj["VERSIONED_OBJECT"][uid.value]
        rev_history = self._obj["REVISION_HISTORY"][uid.value]

        if metadata_only_versioned_object:
            self._log.info(f"{uid.value}: Retrieved VERSIONED_OBJECT (metadata and revision history only)")
            return (meta_only_vo, rev_history)
        else:
            versions = []
            for revision in rev_history.items:
                version_id = revision.version_id
                if version_id.value not in self._meta:
                    raise ValueError(f"Could not rebuild VERSIONED_OBJECT: version with ID \'{version_id.value}\' present in REVISION_HISTORY but not found in database.")
                version_meta = self._meta[version_id.value]
                version_type = version_meta.obj_type
                try:
                    versions.append(self.retrieve_uid_object(version_type, version_id, reader))
                except ValueError:
                    raise ValueError(f"Could not rebuild VERSIONED_OBJECT: version with ID \'{version_id.value}\' had valid metadata but could not be retrieved")
            full_vo = VersionedObject(
                uid=meta_only_vo.uid,
                owner_id=meta_only_vo.owner_id,
                time_created=meta_only_vo.time_created,
                revision_history_and_versions=(rev_history, versions)
            )
            self._log.info(f"{uid.value}:Retrieved VERSIONED_OBJECT (and all underlying VERSIONs)")
            return (full_vo, rev_history)

    
    def commit_contribution_set(self, contrib, versions, owner_id = None, committer = None):
        # check the various IDs refer to each other correctly
        contrib_id = contrib.uid.value
        version_ids = set()
        for version in versions:
            version_ids.add(version.uid().value)
            if version.contribution.id.value != contrib_id:
                raise ValueError(f"Could not commit CONTRIBUTION: version with ID \'{version.uid().value}\' did not reference the provided contribution")
        for version_ref in contrib.versions:
            if version_ref.id.value not in version_ids:
                raise ValueError(f"Could not commit CONTRIBUTION: contribution contained reference to version with ID \'{version_ref.id.value}\' but this was not found in the provided list of versions")
        
        # write each version to the DB
        for version in versions:
            # check if a VERSIONED_OBJECT already exists for this version, and if not create one
            vo_uid = version.owner_id()
            if vo_uid.value not in self._meta:
                if owner_id is None:
                    raise ValueError(f"Could not commit CONTRIBUTION: VERSIONED_OBJECT with UID \'{vo_uid}\' did not exist and no owner_id was provided so could not be created")
                vo = VersionedObject(
                    uid=vo_uid,
                    owner_id=owner_id,
                    time_created=DVDateTime(Env.current_date_time())
                )
                self.create_versioned_object(vo, creator=committer)

            # now add a revision history item for this version
            rhi = RevisionHistoryItem(
                version_id=version.uid(),
                audits=[version.commit_audit]
            )
            self.add_revision_history_item(vo_uid, rhi, creator=committer)

            # finally, write the actual version to the database
            self.create_uid_object(version, creator=committer)

        # then write the contribution itself
        self.create_uid_object(contrib, creator=committer)
        self._log.info(f"Committed CONTRIBUTION (uid={contrib.uid.value}) set of {len(versions)} VERSIONs")
