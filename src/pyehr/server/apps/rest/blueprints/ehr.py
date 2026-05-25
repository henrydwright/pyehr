
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
from pyehr.server.apps.rest.blueprints.shared import _add_headers_to_response, _add_location_headers_to_response, _create_error_response, _create_object_response, _create_unauthorised_response, _get_committer, _parse_request_body, _process_headers, commit_contribution_set, create_object, delete_object, get_contribution_by_id, get_object, get_versioned_object, get_versioned_object_revision_history, get_versioned_object_version_at_time, get_versioned_object_version_by_id, update_object
from pyehr.server.apps.rest.meta import OpenEHRRequestHeaders
from pyehr.server.change_control import VersionLifecycleState, VersionedStore
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyEndpoint, PyehrAccessPolicyEndpointAction
from pyehr.server.security.auth import IPyehrAuthProvider


def create_ehr_blueprint(auth: IPyehrAuthProvider, db: IDatabaseEngine, vs: VersionedStore):
    ehr_bp = Blueprint("ehr", __name__, url_prefix="/ehr")

    log = logging.getLogger("apps.rest.ehr")
    
    default_access_policy = db.retrieve_uid_object("PYEHR_ACCESS_CONTROL_SETTINGS", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000"))

    @ehr_bp.before_request
    def process_headers():
        _process_headers(log)

    def _get_ehr_access(ehr_id: HierObjectID) -> Optional[EHRAccess]:
        meta = db.retrieve_db_metadata(ehr_id)
        if meta is None or meta.obj_type is None or meta.obj_type != "EHR":
            return None
        ehr : EHR = db.retrieve_uid_object("EHR", ehr_id)
        ehr_access : EHRAccess = vs.read("EHR_ACCESS", HierObjectID(ehr.ehr_access.id.value)).data()
        return ehr_access
    
    def _get_access_control_settings(ehr_id: HierObjectID) -> Optional[PyehrAccessControlSettings]:
        ea = _get_ehr_access(ehr_id)
        if isinstance(ea.settings, PyehrAccessControlSettings):
            return ea.settings
        else:
            return None

    @ehr_bp.route("/<string:ehr_id>/ehr_status/<string:version_uid>", methods=["GET"])
    def get_ehr_status_by_version_id(ehr_id: str, version_uid:str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        ovid = ObjectVersionID(version_uid)
        hid = HierObjectID(ovid.object_id().value)

        resp, ovid = get_object(auth, vs, version_uid, "EHR_STATUS", log, (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))
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
            committer=_get_committer(log, auth),
            lifecycle_state=VersionLifecycleState.COMPLETE,
            user=_get_committer(log, auth).external_ref
        )

        return ObjectRef("local", "VERSIONED_EHR_STATUS", HierObjectID(es_ovid.object_id().value))

    def _create_ehr_access(owner_ehr_id: ObjectRef) -> ObjectRef:
        acs_id = db.generate_hier_object_id()
        ea_ovid, ea_contrib, ea_vo = vs.create(
            obj=EHRAccess(
                name=DVText("EHR access"),
                archetype_node_id="openEHR-EHR-EHR_ACCESS.generic.v1",
                archetype_details=Archetyped(
                    archetype_id=ArchetypeID("openEHR-EHR-EHR_ACCESS.generic.v1"),
                    rm_version="1.1.0"
                ),
                settings=PyehrAccessControlSettings(
                    base_upon=ObjectRef("local", "PYEHR_ACCESS_CONTROL_SETTINGS", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000")),
                    uid=acs_id
                )
            ),
            owner_id=owner_ehr_id,
            committer=_get_committer(log, auth),
            lifecycle_state=VersionLifecycleState.COMPLETE,
            user=_get_committer(log, auth).external_ref
        )
        return ObjectRef("local", "VERSIONED_EHR_ACCESS", HierObjectID(ea_ovid.object_id().value))

    @ehr_bp.route("", methods=['POST'])
    @ehr_bp.route("/<param_ehr_id>", methods=['PUT'])
    def create_ehr(param_ehr_id: Optional[str] = None):
        if default_access_policy is not None:
            if not auth.action_authorised_for_authenticated_actor(default_access_policy, PyehrAccessPolicyEndpointAction.CREATE, PyehrAccessPolicyEndpoint.EHR):
                return _create_unauthorised_response()
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
            ehr_id = db.generate_hier_object_id(auth.authenticated_actor()[0].external_ref) 

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

        db.create_uid_object(ehr_obj, _get_committer(log, auth).external_ref)

        resp = _create_object_response(ehr_obj, 201)
        _add_headers_to_response(resp, ehr_id, create_time, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id.value}", f"ehr://{ehr_id.value}")
        
        return resp
    
    def _get_ehr_from_id(hid: HierObjectID) -> Union[EHR, Response]:
        auth_party = auth.authenticated_actor()[0]
        met = db.retrieve_db_metadata(hid, auth_party.external_ref)

        if met is None or met.obj_type != "EHR":
            return _create_error_response(f"404 Not Found: No EHR exists with id \'{hid.value}\'")
        
        ehr : EHR = db.retrieve_uid_object("EHR", hid, auth_party.external_ref)

        return ehr
    
    @ehr_bp.route("/<ehr_id>/ehr_status", methods=['PUT'])
    def update_ehr_status(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(hid)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = ehr.ehr_status.id.value
        log.info(f"EHR_STATUS has ID of \'{es_hid}\'")

        resp, ovid = update_object(auth, vs, "EHR_STATUS", es_hid, log, (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/ehr_status/{ovid.value}", f"ehr://{ehr_id}/ehr_status/{ovid.value}")
        return resp

    @ehr_bp.route("/<string:ehr_id>/ehr_status", methods=['GET'])
    def get_ehr_status_at_time(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(hid)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = ehr.ehr_status.id.value
        log.info(f"EHR_STATUS has ID of \'{es_hid}\'")

        resp, ovid = get_object(auth, vs, es_hid, "EHR_STATUS", log, (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/ehr_status/{ovid.value}", f"ehr://{ehr_id}/ehr_status/{ovid.value}")
        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<uid_based_id>", methods=['GET'])
    def get_composition(ehr_id: str, uid_based_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp, ovid = get_object(auth, vs, uid_based_id, "COMPOSITION", log, (policy, PyehrAccessPolicyEndpoint.EHR_CONTRIBUTION))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")
        
        return resp

    @ehr_bp.route("/<ehr_id>/composition", methods=['POST'])
    def create_composition(ehr_id: str):
        ehid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(ehid)
        emeta = db.retrieve_db_metadata(ehid)
        if emeta is None or emeta.obj_type is None or emeta.obj_type != "EHR":
            return _create_error_response(f"404 Not Found: No EHR with ID \'{ehr_id}\' was found")

        resp, ovid = create_object(auth, vs, "COMPOSITION", ObjectRef("local", "EHR", ehid), log, (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))
        db.add_to_ehr_lists(ehid, ObjectRef("local", "VERSIONED_COMPOSITION", HierObjectID(ovid.object_id().value)))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")

        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<uid_based_id>", methods=['PUT'])
    def update_composition(ehr_id: str, uid_based_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp, ovid = update_object(auth, vs, "COMPOSITION", uid_based_id, log, (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/composition/{ovid.value}", f"ehr://{ehr_id}/composition/{ovid.value}")

        return resp
    
    @ehr_bp.route("/<ehr_id>/composition/<obj_ver_id>", methods=['DELETE'])
    def delete_composition(ehr_id: str, obj_ver_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        return delete_object(auth, vs, "COMPOSITION", obj_ver_id, log, (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>/revision_history")
    def get_versioned_composition_revision_history(ehr_id: str, versioned_object_uid: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp = get_versioned_object_revision_history(auth, vs, HierObjectID(versioned_object_uid), "COMPOSITION", (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}/revision_history", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}/revision_history")
        return resp
    
    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_composition_uid>/version/<versioned_composition_version_id>")
    def get_versioned_composition_version_by_id(ehr_id: str, versioned_composition_uid: str, versioned_composition_version_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp = get_versioned_object_version_by_id(auth, db, vs, "COMPOSITION", HierObjectID(versioned_composition_uid), ObjectVersionID(versioned_composition_version_id), (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_composition_uid}/version/{versioned_composition_version_id}", f"ehr://{ehr_id}/versioned_composition/{versioned_composition_uid}/version/{versioned_composition_version_id}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>/version")
    def get_versioned_composition_version_at_time(ehr_id: str, versioned_object_uid: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp, ovid = get_versioned_object_version_at_time(auth, db, vs, HierObjectID(versioned_object_uid), "COMPOSITION", (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))
        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}/version/{ovid.value}", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}/version/{ovid.value}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_composition/<versioned_object_uid>")
    def get_versioned_composition(ehr_id: str, versioned_object_uid: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp = get_versioned_object(auth, vs, HierObjectID(versioned_object_uid), "COMPOSITION", (policy, PyehrAccessPolicyEndpoint.EHR_COMPOSITION))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_composition/{versioned_object_uid}", f"ehr://{ehr_id}/versioned_composition/{versioned_object_uid}")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/version/<version_uid>", methods=['GET'])
    def get_versioned_ehr_status_version_by_id(ehr_id: str, version_uid: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        ovid = ObjectVersionID(version_uid)

        resp = get_versioned_object_version_by_id(auth, db, vs, "EHR_STATUS", HierObjectID(ovid.object_id().value), ovid, (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))

        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/version/{ovid.value}", f"ehr://{ehr_id}/versioned_ehr_status/version/{ovid.value}")

        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/version", methods=['GET'])
    def get_versioned_ehr_status_version_at_time(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(hid)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp, ovid = get_versioned_object_version_at_time(auth, db, vs, es_hid, "EHR_STATUS", (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/version/{ovid.value}", f"ehr://{ehr_id}/versioned_ehr_status/version/{ovid.value}")

        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status/revision_history", methods=['GET'])
    def get_versioned_ehr_status_revision_history(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(hid)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp = get_versioned_object_revision_history(auth, vs, es_hid, "EHR_STATUS", (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))

        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status/revision_history", f"ehr://{ehr_id}/versioned_ehr_status/revision_history")
        return resp

    @ehr_bp.route("/<ehr_id>/versioned_ehr_status", methods=['GET'])
    def get_versioned_ehr_status(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(hid)

        ehr : EHR = _get_ehr_from_id(hid)
        if isinstance(ehr, Response):
            return ehr
        
        es_hid = HierObjectID(ehr.ehr_status.id.value)
        log.info(f"EHR_STATUS has ID of \'{es_hid.value}\'")

        resp = get_versioned_object(auth, vs, es_hid, "EHR_STATUS", (policy, PyehrAccessPolicyEndpoint.EHR_STATUS))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/versioned_ehr_status", f"ehr://{ehr_id}/versioned_ehr_status")
        return resp

    @ehr_bp.route("/<ehr_id>/contribution/<contribution_id>", methods=['GET'])
    def get_ehr_contribution_by_id(ehr_id: str, contribution_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        resp = get_contribution_by_id(auth, db, HierObjectID(contribution_id), (policy, PyehrAccessPolicyEndpoint.EHR_CONTRIBUTION))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/ehr/{ehr_id}/contribution/{contribution_id}")
        return resp

    @ehr_bp.route("/<ehr_id>/contribution", methods=['POST'])
    def commit_ehr_contribution_set(ehr_id: str):
        policy = _get_access_control_settings(HierObjectID(ehr_id))
        owner_id = ObjectRef("local", "EHR", HierObjectID(ehr_id))

        return commit_contribution_set(auth, db, owner_id, log, (policy, PyehrAccessPolicyEndpoint.EHR_CONTRIBUTION))

    @ehr_bp.route("/<ehr_id>", methods=['GET'])
    def get_ehr_by_id(ehr_id: str):
        hid = HierObjectID(ehr_id)
        policy = _get_access_control_settings(HierObjectID(ehr_id))

        if not auth.action_authorised_for_authenticated_actor(policy, {PyehrAccessPolicyEndpointAction.GET}, PyehrAccessPolicyEndpoint.EHR):
            return _create_unauthorised_response()

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
        auth_actor = auth.authenticated_actor()[0]

        if subject_id is None or subject_namespace is None:
            return _create_error_response("400 Bad Request: Either subject_id or subject_namespace was missing", 400)
        
        ehr_status_results = db.retrieve_query_match_object("VERSION<EHR_STATUS>", 
                                       None, 
                                       {
                                           "data/subject/external_ref/id/value": [subject_id],
                                           "data/subject/external_ref/namespace": [subject_namespace]
                                       })

        if len(ehr_status_results) < 1:
            return _create_error_response("404 Not Found: EHR with supplied subject parameters could not be found", 404)
        
        ehr_status_version : Version[EHRStatus] = ehr_status_results[0]
        esid = ehr_status_version.uid().object_id().value

        ehr_results = db.retrieve_query_match_object("EHR", None, {"ehr_status/id/value" : [esid]})

        if len(ehr_results) != 1:
            return _create_error_response("404 Not Found: EHR with supplied subject parameters could not be found", 404)
        
        ehr : EHR = ehr_results[0]

        policy = _get_access_control_settings(ehr.ehr_id)
        if not auth.action_authorised_for_authenticated_actor(policy, {PyehrAccessPolicyEndpointAction.GET}, PyehrAccessPolicyEndpoint.EHR):
            return _create_unauthorised_response()

        resp = _create_object_response(ehr, 200)
        _add_headers_to_response(resp, ehr.ehr_id, ehr.time_created, f"{current_app.config["BASE_URL"]}/ehr/{ehr.ehr_id.value}", f"ehr://{ehr.ehr_id.value}")
        return resp

    return ehr_bp