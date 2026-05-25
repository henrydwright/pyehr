

import datetime
import json
from logging import Logger
from typing import Optional, Union

from flask import Response, current_app, g, jsonify, make_response, request

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
from pyehr.server.security.auth import IPyehrAuthProvider
from pyehr.utils import PYTHON_TYPE_TO_STRING_TYPE_MAP, get_openehr_type_str

def commit_contribution_set(logged_in_user: PartyProxy, db: IDatabaseEngine, owner_id: ObjectRef, log: Logger):
    body_obj : UpdateContribution = _parse_request_body("UPDATE_CONTRIBUTION")
    if isinstance(body_obj, Response):
        return body_obj
    commit_time = DVDateTime(Env.current_date_time())

    contrib_audit = body_obj.audit._inner_audit_details
    contrib_audit.system_id = current_app.config["SYSTEM_ID_STR"]
    contrib_audit.time_committed = commit_time

    contrib_id = body_obj.uid if body_obj.uid is not None else db.generate_hier_object_id()

    orig_versions = []
    orefs = []
    for update_version in body_obj.versions:
        orig_ver_uid = None
        preceding_version_uid = update_version._inner_original_version.preceding_version_uid()
        if preceding_version_uid is not None:
            new_ver = str(int(preceding_version_uid.version_tree_id().trunk_version()) + 1)
            orig_ver_uid = ObjectVersionID(preceding_version_uid.object_id().value + "::" + current_app.config["SYSTEM_ID_STR"] + "::" + new_ver)
        else:
            orig_ver_uid = ObjectVersionID(db.generate_hier_object_id().value + "::" + current_app.config["SYSTEM_ID_STR"] + "::1")
        
        orefs.append(ObjectRef("local", get_openehr_type_str(update_version), orig_ver_uid))

        # add in the server generated details
        orig_ver = update_version._inner_original_version
        orig_ver.uid_var = orig_ver_uid

        orig_ver_audit = update_version.commit_audit._inner_audit_details
        orig_ver_audit.system_id = current_app.config["SYSTEM_ID_STR"]
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
        committer=_get_committer(log, logged_in_user).external_ref
    )

    resp = _create_object_response(contrib, 201)
    _add_headers_to_response(resp, contrib.uid, commit_time, f"{current_app.config["BASE_URL"]}/demographic/contribution/{contrib.uid.value}")
    return resp

def create_object(logged_in_user: PartyProxy, vs: VersionedStore, typ: str, owner_id: ObjectRef, log: Logger) -> tuple[Response, Optional[ObjectVersionID]]:
    body_obj = _parse_request_body(typ)
    # if you get a Response back rather than an instance of AnyClass, there was an error
    if isinstance(body_obj, Response):
        return (body_obj, None)
    d_ovid, d_contrib, d_vo = vs.create(
        obj=body_obj,
        owner_id=owner_id,
        committer=_get_committer(log, logged_in_user),
        lifecycle_state=_get_lifecycle_state(VersionLifecycleState.COMPLETE, log),
        description=_get_audit_description(log),
        user=_get_committer(log, logged_in_user).external_ref)
    new_obj = d_vo.all_versions()[0].data()
    resp = _create_object_response(new_obj, 201)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed)
    return (resp, d_ovid)

def get_object(logged_in_user: PartyProxy, vs: VersionedStore, uid_based_id: str, typ: str, log: Logger):
    object_version : Version = None
    if "::" in uid_based_id:
        object_version = vs.read_version(typ, ObjectVersionID(uid_based_id), _get_committer(log, logged_in_user).external_ref)
    else:
        version_at_time = request.args.get("version_at_time")
        version_at_time = DVDateTime(version_at_time) if version_at_time is not None else None
        object_version = vs.read(typ, HierObjectID(uid_based_id), version_at_time, _get_committer(log, logged_in_user).external_ref)
    
    if object_version is None:
        return (_create_not_found_response(typ, uid_based_id), None)
    else:
        if object_version.data() is None:
            # has been deleted
            empty = _create_empty_response()
            _add_headers_to_response(empty, object_version.uid(), object_version.commit_audit.time_committed)
            return (empty, object_version.uid())
        resp = _create_object_response(object_version.data(), 200)
        _add_headers_to_response(resp, object_version.uid(), object_version.commit_audit.time_committed)
        return (resp, object_version.uid())

def update_object(logged_in_user: PartyProxy, vs: VersionedStore, typ: str, hier_object_id: str, log: Logger):
    body_object = _parse_request_body(typ)
    if isinstance(body_object, Response):
        return body_object
    
    preceding_uid : ObjectVersionID = g.processed_headers.preceding_version_uid
    if preceding_uid is None:
        return (_create_error_response("400 Bad Request: No 'If-Match' header was provided.", 400), None)
    elif preceding_uid.object_id().value != hier_object_id:
        return (_create_error_response(f"400 Bad Request: 'If-Match' hier object ID ({preceding_uid.object_id().value}) and URL hier object ID ({hier_object_id}) do not match.", 400), None)
    
    obj_type = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(body_object)] if body_object is not None else None
    latest_ver = vs.read(obj_type, HierObjectID(preceding_uid.object_id().value), user=_get_committer(log, logged_in_user).external_ref)
    if latest_ver.uid().value != preceding_uid.value:
        resp = _create_error_response(f"412 Precondition Failed: Provided 'If-Match' of \'{preceding_uid.value}\' did not match latest version uid of \'{latest_ver.uid().value}\'", 412)
        _add_headers_to_response(resp, latest_ver.uid())
        return (resp, None)
    
    d_ovid, d_contrib, _ = vs.update(
        obj=body_object,
        committer=_get_committer(log, logged_in_user),
        lifecycle_state=_get_lifecycle_state(VersionLifecycleState.COMPLETE, log),
        change_type=_get_audit_change_type(AuditChangeType.MODIFICATION, log),
        preceding_version_uid=preceding_uid,
        description=_get_audit_description(log),
        user=_get_committer(log, logged_in_user).external_ref
    )

    resp = _create_object_response(body_object, 200)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed)
    return (resp, d_ovid)

def delete_object(logged_in_user: PartyProxy, vs: VersionedStore, typ: str, object_version_id: str, log: Logger):
    try:
        preceding_uid = ObjectVersionID(object_version_id)
    except ValueError as ve:
        return _create_error_response(f"400 Bad Request: {object_version_id} is not a valid Object Version ID. Inner error: {str(ve)}", 400)
    
    d_ovid, d_contrib, _ = vs.delete(
        obj_type=typ,
        deleter=_get_committer(log, logged_in_user),
        preceding_version_uid=preceding_uid,
        description=_get_audit_description(log),
        user=_get_committer(log, logged_in_user).external_ref
    )

    resp = make_response("", 204)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed)
    return resp


def get_versioned_object_version_by_id(logged_in_user: PartyProxy, db:IDatabaseEngine, vs: VersionedStore, typ: str, hier_object_id: HierObjectID, object_version_id: ObjectVersionID):
    ovid = object_version_id
    hid = hier_object_id
    
    if ovid.object_id().value != hid.value:
        return _create_error_response("400 Bad Request: Hier Object ID and Object Version ID -> Object ID did not match.")
    meta = db.retrieve_db_metadata(ovid, logged_in_user.external_ref)

    if meta is None:
        return _create_not_found_response(f"VERSION<{typ}>", object_version_id)

    obj_type = meta.obj_type
    obj_type = obj_type.replace(">", "")
    obj_type = obj_type.split("<")[1]

    obj = vs.read_version(obj_type, ovid, logged_in_user.external_ref)
    if obj is None:
        return _create_not_found_response(obj_type, object_version_id)
    
    resp = _create_object_response(obj, 200)
    _add_headers_to_response(resp, obj.uid(), obj.commit_audit.time_committed)

    return resp

def get_versioned_object_version_at_time(logged_in_user: PartyProxy, db:IDatabaseEngine, vs: VersionedStore, hier_object_id: HierObjectID, typ: str):
    vo, revision_history = vs.retrieve_versioned_object(hier_object_id, logged_in_user.external_ref)
    if vo is None:
        return (_create_not_found_response(f"VERSION<{typ}>", hier_object_id.value), None)
    most_recent_version_id = revision_history.items[0].version_id
    meta = db.retrieve_db_metadata(most_recent_version_id, reader=logged_in_user.external_ref)
    obj_type = meta.obj_type
    obj_type = obj_type.replace(">", "")
    obj_type = obj_type.split("<")[1]

    version_at_time_arg = request.args.get("version_at_time")
    version_at_time = None if version_at_time_arg is None else DVDateTime(version_at_time_arg)
    obj = vs.read(obj_type, hier_object_id, version_at_time, user=logged_in_user.external_ref)

    if obj is not None:
        resp = _create_object_response(obj, 200)
        _add_headers_to_response(resp, obj.uid(), obj.commit_audit.time_committed)
        return (resp, obj.uid())
    else:
        return (_create_not_found_response(obj_type, hier_object_id), None)

def get_versioned_object_revision_history(logged_in_user: PartyProxy, vs: VersionedStore, hier_object_id: HierObjectID, typ: str):
    _, rev_history = vs.retrieve_versioned_object(hier_object_id, logged_in_user.external_ref)

    if rev_history is None:
        return _create_not_found_response(typ, hier_object_id.value)
    else:
        resp = _create_object_response(rev_history, 200)
        _add_headers_to_response(resp, hier_object_id, DVDateTime(rev_history.most_recent_version_time_committed()))
        return resp

def get_versioned_object(logged_in_user: PartyProxy, vs: VersionedStore, hier_object_id: HierObjectID, typ: str):
    versioned_object, _ = vs.retrieve_versioned_object(hier_object_id, logged_in_user.external_ref)

    if versioned_object is None:
        return _create_not_found_response(typ, hier_object_id.value)
    else:
        resp = _create_object_response(versioned_object, 200)
        _add_headers_to_response(resp, hier_object_id, versioned_object.time_created)
        return resp
    
def get_contribution_by_id(logged_in_user: PartyProxy, db: IDatabaseEngine, hier_object_id: HierObjectID):
    contrib : Contribution = db.retrieve_uid_object("CONTRIBUTION", hier_object_id, logged_in_user.external_ref)

    if contrib is None:
        return _create_not_found_response("CONTRIBUTION", hier_object_id.value)
    else:
        resp = _create_object_response(contrib, 200)
        _add_headers_to_response(resp, hier_object_id, contrib.audit.time_committed)
        return resp

# private shared methods
def _process_headers(log: Logger):
    if not (request.path == "/" or request.path == "/favicon.ico"):
        try:
            g.processed_headers = OpenEHRRequestHeaders(log, request)
        except ValueError as ve:
            log.error("Invalid headers provided: " + str(ve))
            return jsonify({"error":f"Invalid headers provided: {str(ve)}"}), 400

def _add_headers_to_response(response_to_add_to: Response, obj_id: Union[HierObjectID, ObjectVersionID], last_modified: Optional[DVDateTime] = None, location: Optional[str] = None, ehr_uri: Optional[str] = None):
    response_to_add_to.headers.add("ETag", f"W/\"{obj_id.value}\"")
    if last_modified is not None:
        dt = datetime.datetime.fromisoformat(last_modified.value).astimezone(datetime.timezone.utc)
        response_to_add_to.headers.add("Last-Modified", dt.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    if location is not None:
        response_to_add_to.headers.add("Location", location)
    if ehr_uri is not None:
        response_to_add_to.headers.add("openEHR-uri", ehr_uri)

def _add_location_headers_to_response(response_to_add_to: Response, location: Optional[str] = None, ehr_uri: Optional[str] = None):
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

def _get_lifecycle_state(fallback_value: VersionLifecycleState, log: Logger):
    header_state : VersionLifecycleState = g.processed_headers.version_lifecycle_state
    if header_state is not None:
        log.debug(f"Using lifecycle state from header: {header_state.value.value}")
        return header_state
    else:
        return fallback_value

def _get_committer(log: Logger, logged_in_user: PartyProxy):
    header_state : PartyIdentified = g.processed_headers.version_committer
    if header_state is not None:
        log.debug(f"Using committer from header: {json.dumps(header_state.as_json())}")
        return header_state
    else:
        return logged_in_user

def _get_audit_change_type(fallback_value: AuditChangeType, log: Logger):
    header_state : AuditChangeType = g.processed_headers.version_audit_change_type
    if header_state is not None:
        log.debug(f"Using audit change type from header: {header_state.value.value}")
        return header_state
    else:
        return fallback_value

def _get_audit_description(log: Logger, fallback_value: Optional[DVText] = None):
    header_state : DVText = g.processed_headers.version_audit_description
    if header_state is not None:
        log.debug(f"Using audit description from header: {header_state.value}")
    else:
        return fallback_value