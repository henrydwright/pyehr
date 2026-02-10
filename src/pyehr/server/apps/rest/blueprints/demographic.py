import datetime
import json
from typing import Optional, Union
import logging
from uuid import uuid4

from flask import Blueprint, g, request, jsonify, make_response, Response

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.json_tools import decode_json
from pyehr.core.its.rest.additions import UpdateContribution
from pyehr.core.rm.common.change_control import Contribution, Version
from pyehr.core.rm.common.generic import PartyIdentified, PartyProxy
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.server.apps.rest.meta import OpenEHRFormat, OpenEHRRequestHeaders
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState, VersionedStore
from pyehr.server.database import IDatabaseEngine

def create_demographic_blueprint(system_id: str, base_url: str, logged_in_user: PartyProxy, db: IDatabaseEngine, vs: VersionedStore):
    LOCATION_BASE_URL = base_url
    SYSTEM_ID_STR = system_id

    demo_bp = Blueprint("demographic", __name__, url_prefix="/demographic")

    log = logging.getLogger("apps.rest.demographic")

    def _add_headers_to_response(response_to_add_to: Response, obj_id: Union[HierObjectID, ObjectVersionID], last_modified: Optional[DVDateTime] = None, location: Optional[str] = None, ehr_uri: Optional[str] = None):
        response_to_add_to.headers.add("ETag", f"W/\"{obj_id.value}\"")
        if last_modified is not None:
            dt = datetime.datetime.fromisoformat(last_modified.value)
            response_to_add_to.headers.add("Last-Modified", dt.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        if location is not None:
            response_to_add_to.headers.add("Location", location)
        if ehr_uri is not None:
            response_to_add_to.headers.add("openEHR-uri", ehr_uri)

    def _create_error_response(error_text: str, status_code: int):
        err_response = make_response(jsonify({"error": error_text}))
        err_response.status_code = status_code
        err_response.headers["Content-Type"] = "application/json"
        return err_response

    def _create_object_response(obj: AnyClass, status_code: int):
        accepted_formats = g.processed_headers.preferred_response_formats
        if accepted_formats is None:
            accepted_formats = {OpenEHRFormat.JSON}
        if OpenEHRFormat.JSON in accepted_formats or OpenEHRFormat.NONSTANDARD_HTML in accepted_formats:
            success_resp = make_response(jsonify(obj.as_json()))
            success_resp.status_code = status_code
            success_resp.headers["Content-Type"] = "application/json"
            return success_resp
        else:
            return _create_error_response(f"412 Precondition Failed: Server does not support any OpenEHR format that the client accepts ({str(accepted_formats)})", 412)
        
    def _create_empty_response():
        empty_resp = make_response("")
        empty_resp.status_code = 204
        return empty_resp

    def _create_not_found_response(obj_type: str, uid_based_id: str):
        return _create_error_response(f"404 Not Found: Could not find {obj_type} with uid of \'{uid_based_id}\'", 404)

    def _parse_request_body(target_type: str):
        parse_format = g.processed_headers.provided_content_format
        if parse_format is None:
            parse_format = OpenEHRFormat.JSON
        
        if parse_format != OpenEHRFormat.JSON:
            return _create_error_response(f"415 Unsupported Media Type: Server cannot parse the OpenEHR \'{str(parse_format)}\' format", 415)
        else:
            return decode_json(request.get_json(), target_type)

    def _get_lifecycle_state(fallback_value: VersionLifecycleState):
        header_state : VersionLifecycleState = g.processed_headers.version_lifecycle_state
        if header_state is not None:
            log.debug(f"Using lifecycle state from header: {header_state.value.value}")
            return header_state
        else:
            return fallback_value

    def _get_committer():
        header_state : PartyIdentified = g.processed_headers.version_committer
        if header_state is not None:
            log.debug(f"Using committer from header: {json.dumps(header_state.as_json())}")
            return header_state
        else:
            return logged_in_user

    def _get_audit_change_type(fallback_value: AuditChangeType):
        header_state : AuditChangeType = g.processed_headers.version_audit_change_type
        if header_state is not None:
            log.debug(f"Using audit change type from header: {header_state.value.value}")
            return header_state
        else:
            return fallback_value

    def _get_audit_description(fallback_value: Optional[DVText] = None):
        header_state : DVText = g.processed_headers.version_audit_description
        if header_state is not None:
            log.debug(f"Using audit description from header: {header_state.value}")
        else:
            return fallback_value

    @demo_bp.before_request
    def process_headers():
        if not (request.path == "/" or request.path == "/favicon.ico"):
            try:
                g.processed_headers = OpenEHRRequestHeaders(log, request)
            except ValueError as ve:
                log.error("Invalid headers provided: " + str(ve))
                return jsonify({"error":f"Invalid headers provided: {str(ve)}"}), 400

    def _is_demographic_type(typ : str):
        return (typ in {"AGENT", "GROUP", "ORGANISATION", "PERSON", "ROLE"})

    @demo_bp.route("/contribution", methods=['POST'])
    def commit_contribution_set():
        body_obj : UpdateContribution = _parse_request_body("UPDATE_CONTRIBUTION")
        if isinstance(body_obj, Response):
            return body_obj
        
        owner_id = ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000"))
        
        commit_time = DVDateTime(Env.current_date_time())

        contrib_audit = body_obj.audit._inner_audit_details
        contrib_audit.system_id = SYSTEM_ID_STR
        contrib_audit.time_committed = commit_time

        contrib_id = body_obj.uid if body_obj.uid is not None else db.generate_hier_object_id()

        orig_versions = []
        orefs = []
        for update_version in body_obj.versions:
            orig_ver_uid = None
            preceding_version_uid = update_version._inner_original_version.preceding_version_uid()
            if preceding_version_uid is not None:
                new_ver = str(int(preceding_version_uid.version_tree_id().trunk_version()) + 1)
                orig_ver_uid = ObjectVersionID(preceding_version_uid.object_id().value + "::" + SYSTEM_ID_STR + "::" + new_ver)
            else:
                orig_ver_uid = ObjectVersionID(db.generate_hier_object_id().value + "::" + SYSTEM_ID_STR + "::1")
            
            orefs.append(ObjectRef("local", "VERSION", orig_ver_uid))

            # add in the server generated details
            orig_ver = update_version._inner_original_version
            orig_ver.uid_var = orig_ver_uid

            orig_ver_audit = update_version.commit_audit._inner_audit_details
            orig_ver_audit.system_id = SYSTEM_ID_STR
            orig_ver_audit.time_committed = commit_time
            orig_ver.commit_audit = orig_ver_audit

            orig_ver.contribution = ObjectRef("local", "CONTRIBUTION", contrib_id)

            orig_versions.append(orig_ver)

        contrib = Contribution(
            uid=contrib_id,
            versions=orefs,
            audit=contrib_audit
        )

        db.commit_contribution_set(
            contrib=contrib,
            versions=orig_versions,
            owner_id=owner_id,
            committer=_get_committer().external_ref
        )

        resp = _create_object_response(contrib, 201)
        _add_headers_to_response(resp, contrib.uid, commit_time, f"{LOCATION_BASE_URL}/demographic/contribution/{contrib.uid.value}")
        return resp

    @demo_bp.route("/<demographic_type>", methods=['GET', 'POST'])
    def create_demographic_object(demographic_type: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        body_obj = _parse_request_body(typ)
        # if you get a Response back rather than an instance of AnyClass, there was an error
        if isinstance(body_obj, Response):
            return body_obj
        d_ovid, d_contrib, d_vo = vs.create(
            obj=body_obj,
            owner_id=ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000")),
            committer=_get_committer(),
            lifecycle_state=_get_lifecycle_state(VersionLifecycleState.COMPLETE),
            description=_get_audit_description(),
            user=_get_committer().external_ref)
        new_obj = d_vo.all_versions()[0].data()
        resp = _create_object_response(new_obj, 201)
        _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{d_ovid.value}", f"demographic://{d_ovid.object_id().value}")
        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version/<object_version_id>", methods=['GET'])
    def get_versioned_party_version_by_id(hier_object_id: str, object_version_id: str):
        ovid = ObjectVersionID(object_version_id)
        hid = HierObjectID(hier_object_id)
        if ovid.object_id().value != hid.value:
            return _create_error_response("400 Bad Request: Hier Object ID and Object Version ID -> Object ID did not match.")
        meta = db.retrieve_db_metadata(ovid, logged_in_user.external_ref)

        if meta is None:
            return _create_not_found_response("VERSION<PARTY>", object_version_id)

        obj_type = meta.obj_type
        obj_type = obj_type.replace(">", "")
        obj_type = obj_type.split("<")[1]

        obj = vs.read_version(obj_type, ovid, logged_in_user.external_ref)
        if obj is None:
            return _create_not_found_response(obj_type, object_version_id)
        
        resp = _create_object_response(obj, 200)
        _add_headers_to_response(resp, obj.uid(), obj.commit_audit.time_committed, f"{LOCATION_BASE_URL}/demographic/versioned_party/{hier_object_id}/version/{obj.uid().value}")
        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version", methods=['GET'])
    def get_versioned_party_version_at_time(hier_object_id: str):
        vo, revision_history = vs.retrieve_versioned_object(HierObjectID(hier_object_id), logged_in_user.external_ref)
        if vo is None:
            return _create_not_found_response("VERSION<PARTY>", hier_object_id)
        most_recent_version_id = revision_history.items[0].version_id
        meta = db.retrieve_db_metadata(most_recent_version_id, reader=logged_in_user.external_ref)
        obj_type = meta.obj_type
        obj_type = obj_type.replace(">", "")
        obj_type = obj_type.split("<")[1]

        version_at_time = request.args.get("version_at_time")
        obj = vs.read(obj_type, HierObjectID(hier_object_id), version_at_time, user=logged_in_user.external_ref)

        resp = _create_object_response(obj, 200)
        _add_headers_to_response(resp, obj.uid(), obj.commit_audit.time_committed, f"{LOCATION_BASE_URL}/demographic/versioned_party/{hier_object_id}/version/{obj.uid().value}")
        return resp
        
    @demo_bp.route("/versioned_party/<hier_object_id>", methods=['GET'])
    def get_versioned_party(hier_object_id: str):
        versioned_party, _ = vs.retrieve_versioned_object(HierObjectID(hier_object_id), logged_in_user.external_ref)

        if versioned_party is None:
            return _create_not_found_response("VERSIONED_PARTY", hier_object_id)
        else:
            resp = _create_object_response(versioned_party, 200)
            _add_headers_to_response(resp, HierObjectID(hier_object_id), versioned_party.time_created, f"{LOCATION_BASE_URL}/demographic/versioned_party/{hier_object_id}")
            return resp
        
    @demo_bp.route("/contribution/<hier_object_id>", methods=['GET'])
    def get_contribution_by_id(hier_object_id: str):
        contrib : Contribution = db.retrieve_uid_object("CONTRIBUTION", HierObjectID(hier_object_id), logged_in_user.external_ref)

        if contrib is None:
            return _create_not_found_response("CONTRIBUTION", hier_object_id)
        else:
            resp = _create_object_response(contrib, 200)
            _add_headers_to_response(resp, HierObjectID(hier_object_id), contrib.audit.time_committed, f"{LOCATION_BASE_URL}/demographic/contribution/{hier_object_id}")
            return resp

    @demo_bp.route("/<demographic_type>/<uid_based_id>", methods=['GET'])
    def get_demographic_object(demographic_type: str, uid_based_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)

        object_version : Version = None
        if "::" in uid_based_id:
            object_version = vs.read_version(typ, ObjectVersionID(uid_based_id), _get_committer().external_ref)
        else:
            version_at_time = request.args.get("version_at_time")
            object_version = vs.read(typ, HierObjectID(uid_based_id), version_at_time, _get_committer().external_ref)
        
        if object_version is None:
            return _create_not_found_response(typ, uid_based_id)
        else:
            if object_version.data() is None:
                # has been deleted
                empty = _create_empty_response()
                _add_headers_to_response(empty, object_version.uid(), object_version.commit_audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{object_version.uid().value}", f"demographic://{object_version.uid().value}")
                return empty
            resp = _create_object_response(object_version.data(), 200)
            _add_headers_to_response(resp, object_version.uid(), object_version.commit_audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{object_version.uid().value}", f"demographic://{object_version.uid().value}")
            return resp
        
    @demo_bp.route("/<demographic_type>/<hier_object_id>", methods=['PUT'])
    def update_demographic_object(demographic_type: str, hier_object_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        body_object = _parse_request_body(typ)
        if isinstance(body_object, Response):
            return body_object
        
        preceding_uid = g.processed_headers.preceding_version_uid
        if preceding_uid is None:
            return _create_error_response("400 Bad Request: No 'If-Match' header was provided.", 400)
        elif preceding_uid.object_id().value != hier_object_id:
            return _create_error_response("400 Bad Request: 'If-Match' hier object ID and URL hier object ID do not match.", 400)
        
        d_ovid, d_contrib, _ = vs.update(
            obj=body_object,
            committer=_get_committer(),
            lifecycle_state=_get_lifecycle_state(VersionLifecycleState.COMPLETE),
            change_type=_get_audit_change_type(AuditChangeType.MODIFICATION),
            preceding_version_uid=preceding_uid,
            description=_get_audit_description(),
            user=_get_committer().external_ref
        )

        resp = _create_object_response(body_object, 200)
        _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{d_ovid.value}", f"demographic://{d_ovid.value}")
        return resp

    @demo_bp.route("/<demographic_type>/<object_version_id>", methods=['DELETE'])
    def delete_demographic_object(demographic_type: str, object_version_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        try:
            preceding_uid = ObjectVersionID(object_version_id)
        except ValueError as ve:
            return _create_error_response(f"400 Bad Request: {object_version_id} is not a valid Object Version ID. Inner error: {str(ve)}", 400)
        
        d_ovid, d_contrib, _ = vs.delete(
            obj_type=typ,
            deleter=_get_committer(),
            preceding_version_uid=preceding_uid,
            description=_get_audit_description(),
            user=_get_committer().external_ref
        )

        resp = make_response("", 204)
        _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed)
        return resp
    
    return demo_bp
