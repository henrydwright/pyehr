import datetime
from enum import StrEnum
import json
from typing import Optional, Union
from flask import Flask, Request, g, request, jsonify, make_response, Response

import logging
from uuid import uuid4

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, ObjectVersionID, PartyRef
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.change_control import Version
from pyehr.core.rm.common.generic import PartyIdentified, PartySelf
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.demographic import Person
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState, VersionedStore
from pyehr.server.database.local import InMemoryDB

class OpenEHRPreferredResponseDetailLevel(StrEnum):
    """Different types of API response that OpenEHR clients can request"""
    REPRESENTATION = "return=representation"
    MINIMAL = "return=minimal"
    IDENTIFIER = "return=identifier"

class OpenEHRFormat(StrEnum):
    """Different formats that OpenEHR objects can be serialised to"""
    JSON = "application/json"
    XML = "application/xml"
    FLAT = "application/openehr.wt.flat+json"
    STRUCTURED = "application/openehr.wt.structured+json"
    NONSTANDARD_HTML = "text/html"

class OpenEHRRequestHeaders():
    """Pythonic representation of the header values in OpenEHR REST API requests"""

    preferred_response_detail_level: Optional[OpenEHRPreferredResponseDetailLevel] = None
    """Contents of the `Prefer` header saying the level of detail the client would prefer in the response"""

    preferred_response_formats: Optional[set[OpenEHRFormat]] = None
    """Contents of the `Accept` header saying what serialisation format(s) the client will accept"""

    provided_content_format: Optional[OpenEHRFormat] = None
    """Contents of the `Content-Type` header saying what serialisation format has been provided in the body"""

    preceding_version_uid: Optional[ObjectVersionID] = None
    """Contents of the `If-Match` header for operations that must only be performed when the latest version matches this version ID"""

    def __init__(self, request_content: Request):
        prefer = request_content.headers.get("Prefer")
        if prefer is not None:
            self.preferred_response_detail_level = OpenEHRPreferredResponseDetailLevel(prefer)
        accept = request_content.headers.get("Accept")
        if accept is not None:
            accepted_formats = set()
            accept_list = accept.split(",")
            for accept_format in accept_list:
                if accept_format == "*/*":
                    # wildcard for all formats, so allow all OpenEHR types
                    accepted_formats = {OpenEHRFormat.JSON, OpenEHRFormat.XML, OpenEHRFormat.FLAT, OpenEHRFormat.STRUCTURED}
                    break
                if accept_format in OpenEHRFormat:
                    accepted_formats.add(accept_format)
            if len(accepted_formats) == 0:
                raise ValueError(f"\'{accept}\' did not contain a valid OpenEHR format type")
            self.preferred_response_formats = accepted_formats
        content_type = request_content.headers.get("Content-Type")
        if content_type is not None:
            self.provided_content_format = OpenEHRFormat(content_type)
        if_match = request_content.headers.get("If-Match")
        if if_match is not None:
            self.preceding_version_uid = ObjectVersionID(if_match)

logging.basicConfig(level=logging.DEBUG)

SYSTEM_ID_HID = str(uuid4())
SYSTEM_ID_STR = "com.eldonhealth.ehr1"
LOCATION_BASE_URL = "http://localhost:5000"

log = logging.getLogger("RestAPIServer")
log.info("pyehr REST API server starting...")

log.info("Initialising: database")
db = InMemoryDB()

log.info("Initialising: versioned store")
vs = VersionedStore(
    db_engine=db,
    system_id=SYSTEM_ID_STR
)

logged_in_user_uuid = str(uuid4())

logged_in_user = PartyIdentified(
    external_ref=PartyRef("local", "PERSON", HierObjectID(logged_in_user_uuid)),
    name="DR ABBEY EXAMPLE"
)

app = Flask(__name__)

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

@app.before_request
def process_headers():
    if not (request.path == "/" or request.path == "/favicon.ico"):
        try:
            g.processed_headers = OpenEHRRequestHeaders(request)
        except ValueError as ve:
            log.error("Invalid headers provided: " + str(ve))
            return jsonify({"error":f"Invalid headers provided: {str(ve)}"}), 400

@app.route("/", methods=['GET'])
def web_home():
    return "<h1>pyehr REST API Server</h1><p>You have reached an OpenEHR server running on pyehr.</p>"

@app.route("/ehr", methods=['POST', 'GET'])
def create_ehr():
    new_ehr_uid = db.generate_hier_object_id()
    new_ehr_status = EHRStatus(
        name=DVText("EHR Status"),
        archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"), rm_version="1.1.0"),
        subject=PartySelf(),
        is_queryable=True,
        is_modifiable=True
    )
    new_ehr_status_vid, nes_contrib, nes_vo = vs.create(
        obj=new_ehr_status,
        owner_id=ObjectRef("local", "EHR", new_ehr_uid),
        committer=logged_in_user,
        lifecycle_state=VersionLifecycleState.COMPLETE,
        user=logged_in_user.external_ref
    )
    new_ehr = EHR(
        system_id=HierObjectID(SYSTEM_ID_HID),
        ehr_id=new_ehr_uid,
        ehr_status=ObjectRef("local", "VERSIONED_EHR_STATUS", nes_vo.uid),
        ehr_access=ObjectRef("local", "VERSIONED_EHR_ACCESS", db.generate_hier_object_id()),
        time_created=DVDateTime(Env.current_date_time())
    )
    db.create_uid_object(
        obj=new_ehr,
        creator=logged_in_user.external_ref
    )
    return _create_object_response(new_ehr, 201)

@app.route("/ehr/<uuid:ehr_id>", methods=['GET'])
def get_ehr_by_id(ehr_id):
    ehr = db.retrieve_uid_object(
        obj_type="EHR",
        uid=HierObjectID(str(ehr_id)),
        reader=logged_in_user.external_ref
    )
    return ehr.as_json()

def _is_demographic_type(typ : str):
    return typ in {"AGENT", "GROUP", "ORGANISATION", "PERSON", "ROLE"}

@app.route("/demographic/<demographic_type>", methods=['GET', 'POST'])
def create_demographic_object(demographic_type: str):
    typ = demographic_type.upper()
    if not _is_demographic_type(typ):
        _create_error_response("", 404)
    
    body_obj = _parse_request_body(typ)
    if isinstance(body_obj, Response):
        return body_obj
    d_ovid, d_contrib, d_vo = vs.create(
        obj=body_obj,
        owner_id=ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000")),
        committer=logged_in_user,
        lifecycle_state=VersionLifecycleState.COMPLETE,
        user=logged_in_user.external_ref)
    new_obj = d_vo.all_versions()[0].data()
    resp = _create_object_response(new_obj, 201)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{d_ovid.value}", f"demographic://{d_ovid.object_id().value}")
    return resp

@app.route("/demographic/<demographic_type>/<uid_based_id>", methods=['GET'])
def get_demographic_object(demographic_type: str, uid_based_id: str):
    typ = demographic_type.upper()
    if not _is_demographic_type(typ):
        _create_error_response("", 404)

    object_version : Version = None
    if "::" in uid_based_id:
        object_version = vs.read_version(typ, ObjectVersionID(uid_based_id), logged_in_user.external_ref)
    else:
        version_at_time = request.args.get("version_at_time")
        object_version = vs.read(typ, HierObjectID(uid_based_id), version_at_time, logged_in_user.external_ref)
    
    if object_version is None:
        return _create_not_found_response(typ, uid_based_id)
    else:
        resp = _create_object_response(object_version.data(), 200)
        _add_headers_to_response(resp, object_version.uid(), object_version.commit_audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{object_version.uid().value}", f"demographic://{object_version.uid().value}")
        return resp
    
@app.route("/demographic/<demographic_type>/<hier_object_id>", methods=['PUT'])
def update_demographic_object(demographic_type: str, hier_object_id: str):
    typ = demographic_type.upper()
    if not _is_demographic_type(typ):
        _create_error_response("", 404)
    
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
        committer=logged_in_user,
        lifecycle_state=VersionLifecycleState.COMPLETE,
        change_type=AuditChangeType.MODIFICATION,
        preceding_version_uid=preceding_uid,
        user=logged_in_user.external_ref
    )

    resp = _create_object_response(body_object, 200)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed, f"{LOCATION_BASE_URL}/demographic/{typ.lower()}/{d_ovid.value}", f"demographic://{d_ovid.value}")
    return resp

@app.route("/demographic/<demographic_type>/<object_version_id>", methods=['DELETE'])
def delete_demographic_object(demographic_type: str, object_version_id: str):
    typ = demographic_type.upper()
    if not _is_demographic_type(typ):
        _create_error_response("", 404)
    
    try:
        preceding_uid = ObjectVersionID(object_version_id)
    except ValueError as ve:
        return _create_error_response(f"400 Bad Request: {object_version_id} is not a valid Object Version ID. Inner error: {str(ve)}", 400)
    
    d_ovid, d_contrib, _ = vs.delete(
        obj_type=typ,
        deleter=logged_in_user,
        preceding_version_uid=preceding_uid,
        user=logged_in_user.external_ref
    )

    resp = make_response("", 204)
    _add_headers_to_response(resp, d_ovid, d_contrib.audit.time_committed)
    return resp

# TODO: Add VERSIONED_PARTY methods