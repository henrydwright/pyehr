
from enum import Enum
import logging
from typing import Optional, Union

from flask import Blueprint, Response, current_app, jsonify, request

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, ObjectVersionID
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.change_control import Version
from pyehr.core.rm.common.generic import PartyProxy, PartySelf
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus
from pyehr.server.apps.rest.blueprints.shared import _add_headers_to_response, _add_location_headers_to_response, _create_error_response, _create_object_response, _get_committer, _parse_request_body, _process_headers, commit_contribution_set, create_object, delete_object, get_contribution_by_id, get_object, get_versioned_object, get_versioned_object_revision_history, get_versioned_object_version_at_time, get_versioned_object_version_by_id, update_object
from pyehr.server.apps.rest.meta import OpenEHRRequestHeaders
from pyehr.server.change_control import VersionLifecycleState, VersionedStore
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.auth import IPyehrAuthProvider


def create_ehr_blueprint(auth: IPyehrAuthProvider, db: IDatabaseEngine, vs: VersionedStore):
    ehr_bp = Blueprint("ehr", __name__, url_prefix="/ehr")

    logged_in_user, _ = auth.authenticated_actor()

    log = logging.getLogger("apps.rest.ehr")

    @ehr_bp.before_request
    def process_headers():
        _process_headers(log)

    @ehr_bp.route("/<string:ehr_id>/ehr_status/<string:version_uid>", methods=["GET"])
    def get_ehr_status_by_version_id(ehr_id: str, version_uid:str):
        ovid = ObjectVersionID(version_uid)
        hid = HierObjectID(ovid.object_id().value)

        resp, ovid = get_object(logged_in_user, vs, version_uid, "EHR_STATUS", log)
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/ehr_status/{version_uid}", f"ehr://{ehr_id}/ehr_status/{version_uid}")
        return resp

    def _create_ehr_status(owner_ehr_id: ObjectRef, status_obj: Optional[EHRStatus] = None) -> ObjectRef:
        if status_obj is None:
            status_obj = EHRStatus(
                name=DVText("EHR status"),
                archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
                subject=PartySelf(),
                is_queryable=True,
                is_modifiable=True,
                archetype_details=Archetyped(
                    archetype_id=ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"),
                    rm_version="1.1.0"
                )
            )

        es_ovid, es_contrib, es_vo = vs.create(
            obj=status_obj,
            owner_id=owner_ehr_id,
            committer=_get_committer(log, logged_in_user),
            lifecycle_state=VersionLifecycleState.COMPLETE,
            user=_get_committer(log, logged_in_user).external_ref
        )

        return ObjectRef("local", "VERSIONED_EHR_STATUS", HierObjectID(es_ovid.object_id().value))

    def _create_ehr_access(owner_ehr_id: ObjectRef) -> ObjectRef:
        ea_ovid, ea_contrib, ea_vo = vs.create(
            obj=EHRAccess(
                name=DVText("EHR access"),
                archetype_node_id="openEHR-EHR-EHR_ACCESS.generic.v1",
                archetype_details=Archetyped(
                    archetype_id=ArchetypeID("openEHR-EHR-EHR_ACCESS.generic.v1"),
                    rm_version="1.1.0"
                )
            ),
            owner_id=owner_ehr_id,
            committer=_get_committer(log, logged_in_user),
            lifecycle_state=VersionLifecycleState.COMPLETE,
            user=_get_committer(log, logged_in_user).external_ref
        )
        return ObjectRef("local", "VERSIONED_EHR_ACCESS", HierObjectID(ea_ovid.object_id().value))

    @ehr_bp.route("", methods=['POST'])
    @ehr_bp.route("/<param_ehr_id>", methods=['PUT'])
    def create_ehr(param_ehr_id: Optional[str] = None):
        body_obj = request.get_json(silent=True)
        if body_obj is not None:
            body_obj = _parse_request_body("EHR_STATUS")
        
            # if you get a Response back rather than an instance of AnyClass, there was an error
            if isinstance(body_obj, Response):
                return body_obj
        
        ehr_id = None
        if param_ehr_id is not None:
            ehr_id = HierObjectID(param_ehr_id)
            id_meta = db.retrieve_db_metadata(ehr_id)
            if id_meta is not None and id_meta.obj_type is not None:
                return _create_error_response(f"409 Conflict: Cannot create an EHR with id \'{ehr_id.value}\' as an object with that ID exists already in the database", 409)
        else:
            ehr_id = db.generate_hier_object_id(logged_in_user) 

        try:
            ehr_status_ref = _create_ehr_status(ObjectRef("local", "EHR", ehr_id), body_obj)
        except ValueError:
            return _create_error_response(f"409 Conflict: uid in provided EHR_STATUS already exists so cannot be created", 409)
        
        ehr_access_ref = _create_ehr_access(ObjectRef("local", "EHR", ehr_id))

        create_time = DVDateTime(Env.current_date_time())
        ehr_obj = EHR(
            system_id=HierObjectID(current_app.config["SYSTEM_ID_HID"]),
            ehr_id=ehr_id,
            ehr_status=ehr_status_ref,
            ehr_access=ehr_access_ref,
            time_created=create_time
        )

        db.create_uid_object(ehr_obj, _get_committer(log, logged_in_user).external_ref)

        resp = _create_object_response(ehr_obj, 201)
        _add_headers_to_response(resp, ehr_id, create_time, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id.value}", f"ehr://{ehr_id.value}")
        
        return resp
    
    def _get_ehr_from_id(hid: HierObjectID) -> Union[EHR, Response]:
        met = db.retrieve_db_metadata(hid, logged_in_user.external_ref)

        if met is None or met.obj_type != "EHR":
            return _create_error_response(f"404 Not Found: No EHR exists with id \'{hid.value}\'")
        
        ehr : EHR = db.retrieve_uid_object("EHR", hid, logged_in_user.external_ref)#

        return ehr
    
    @ehr_bp.route("/<ehr_id>/ehr_status", methods=['PUT'])
    def update_ehr_status(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = ehr.ehr_status.id.value
        log.info(f"EHR_STATUS has ID of \'{es_hid}\'")

        resp, ovid = update_object(logged_in_user, vs, "EHR_STATUS", es_hid, log)
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/ehr_status/{ovid.value}", f"ehr://{ehr_id}/ehr_status/{ovid.value}")
        return resp

    @ehr_bp.route("/<string:ehr_id>/ehr_status", methods=['GET'])
    def get_ehr_status_at_time(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = ehr.ehr_status.id.value
        log.info(f"EHR_STATUS has ID of \'{es_hid}\'")

        resp, ovid = get_object(logged_in_user, vs, es_hid, "EHR_STATUS", log)
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/ehr_status/{ovid.value}", f"ehr://{ehr_id}/ehr_status/{ovid.value}")
        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<uid_based_id>", methods=['GET'])
    def get_composition(ehr_id: str, uid_based_id: str):
        resp, ovid = get_object(logged_in_user, vs, uid_based_id, "COMPOSITION", log)

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")
        
        return resp

    @ehr_bp.route("/<ehr_id>/composition", methods=['POST'])
    def create_composition(ehr_id: str):
        ehid = HierObjectID(ehr_id)
        emeta = db.retrieve_db_metadata(ehid)
        if emeta is None or emeta.obj_type is None or emeta.obj_type != "EHR":
            return _create_error_response(f"404 Not Found: No EHR with ID \'{ehr_id}\' was found")

        resp, ovid = create_object(logged_in_user, vs, "COMPOSITION", ObjectRef("local", "EHR", ehid), log)
        db.add_to_ehr_lists(ehid, ObjectRef("local", "VERSIONED_COMPOSITION", HierObjectID(ovid.object_id().value)))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")

        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<uid_based_id>", methods=['PUT'])
    def update_composition(ehr_id: str, uid_based_id: str):
        resp, ovid = update_object(logged_in_user, vs, "COMPOSITION", uid_based_id, log)

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")

        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<obj_ver_id>", methods=['DELETE'])
    def delete_composition(ehr_id: str, obj_ver_id: str):
        return delete_object(logged_in_user, vs, "COMPOSITION", obj_ver_id, log)

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>/revision_history")
    def get_versioned_composition_revision_history(ehr_id: str, versioned_object_uid: str):
        resp = get_versioned_object_revision_history(logged_in_user, vs, HierObjectID(versioned_object_uid), "COMPOSITION")
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}/revision_history", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}/revision_history")
        return resp
    
    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_composition_uid>/version/<versioned_composition_version_id>")
    def get_versioned_composition_version_by_id(ehr_id: str, versioned_composition_uid: str, versioned_composition_version_id: str):
        resp = get_versioned_object_version_by_id(logged_in_user, db, vs, "COMPOSITION", HierObjectID(versioned_composition_uid), ObjectVersionID(versioned_composition_version_id))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_composition_uid}/version/{versioned_composition_version_id}", f"ehr://{ehr_id}/versioned_composition/{versioned_composition_uid}/version/{versioned_composition_version_id}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>/version")
    def get_versioned_composition_version_at_time(ehr_id: str, versioned_object_uid: str):
        resp, ovid = get_versioned_object_version_at_time(logged_in_user, db, vs, HierObjectID(versioned_object_uid), "COMPOSITION")
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}/version/{ovid.value}", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}/version/{ovid.value}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>")
    def get_versioned_composition(ehr_id: str, versioned_object_uid: str):
        resp = get_versioned_object(logged_in_user, vs, HierObjectID(versioned_object_uid), "COMPOSITION")
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/version/<version_uid>", methods=['GET'])
    def get_versioned_ehr_status_version_by_id(ehr_id: str, version_uid: str):
        ovid = ObjectVersionID(version_uid)

        resp = get_versioned_object_version_by_id(logged_in_user, db, vs, "EHR_STATUS", HierObjectID(ovid.object_id().value), ovid)

        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/version/{ovid.value}", f"ehr://{ehr_id}/versioned_ehr_status/version/{ovid.value}")

        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/version", methods=['GET'])
    def get_versioned_ehr_status_version_at_time(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp, ovid = get_versioned_object_version_at_time(logged_in_user, db, vs, es_hid, "EHR_STATUS")

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/version/{ovid.value}", f"ehr://{ehr_id}/versioned_ehr_status/version/{ovid.value}")

        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/revision_history", methods=['GET'])
    def get_versioned_ehr_status_revision_history(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp = get_versioned_object_revision_history(logged_in_user, vs, es_hid, "EHR_STATUS")

        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/revision_history", f"ehr://{ehr_id}/versioned_ehr_status/revision_history")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status", methods=['GET'])
    def get_versioned_ehr_status(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp = get_versioned_object(logged_in_user, vs, es_hid, "EHR_STATUS")
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status", f"ehr://{ehr_id}/versioned_ehr_status")
        return resp

    @ehr_bp.route("/<ehr_id>/contribution/<contribution_id>", methods=['GET'])
    def get_ehr_contribution_by_id(ehr_id: str, contribution_id: str):
        resp = get_contribution_by_id(logged_in_user, db, HierObjectID(contribution_id))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/contribution/{contribution_id}")
        return resp

    @ehr_bp.route("/<ehr_id>/contribution", methods=['POST'])
    def commit_ehr_contribution_set(ehr_id: str):
        owner_id = ObjectRef("local", "EHR", HierObjectID(ehr_id))

        return commit_contribution_set(logged_in_user, db, owner_id, log)

    @ehr_bp.route("/<ehr_id>", methods=['GET'])
    def get_ehr_by_id(ehr_id: str):
        hid = HierObjectID(ehr_id)

        ehr = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr

        resp = _create_object_response(ehr, 200)
        _add_headers_to_response(resp, hid, ehr.time_created, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}", f"ehr://{ehr_id}")
        return resp
            
    @ehr_bp.route("", methods=['GET'])
    def get_ehr_by_subject_id():
        subject_id = request.args.get("subject_id")
        subject_namespace = request.args.get("subject_namespace")

        if subject_id is None or subject_namespace is None:
            return _create_error_response("400 Bad Request: Either subject_id or subject_namespace was missing", 400)
        
        ehr_status_results = db.retrieve_query_match_object("VERSION<EHR_STATUS>", 
                                       None, 
                                       {
                                           "data/subject/external_ref/id/value": [subject_id],
                                           "data/subject/external_ref/namespace": [subject_namespace]
                                       },
                                       logged_in_user.external_ref)

        if len(ehr_status_results) < 1:
            return _create_error_response("404 Not Found: EHR with supplied subject parameters could not be found", 404)
        
        ehr_status_version : Version[EHRStatus] = ehr_status_results[0]
        esid = ehr_status_version.uid().object_id().value

        ehr_results = db.retrieve_query_match_object("EHR", None, {"ehr_status/id/value" : [esid]}, logged_in_user.external_ref)

        if len(ehr_results) != 1:
            return _create_error_response("404 Not Found: EHR with supplied subject parameters could not be found", 404)
        
        ehr : EHR = ehr_results[0]
        resp = _create_object_response(ehr, 200)
        _add_headers_to_response(resp, ehr.ehr_id, ehr.time_created, f"{current_app.config["BASE_URL"]}/ehr/{ehr.ehr_id.value}", f"ehr://{ehr.ehr_id.value}")
        return resp

    return ehr_bp