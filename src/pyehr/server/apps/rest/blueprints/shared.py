

import datetime
import json
from logging import Logger
from typing import Optional, Union

from flask import Response, g, jsonify, make_response, request

from pyehr.core.base.base_types.identification import HierObjectID, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.generic import PartyIdentified, PartyProxy
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.server.apps.rest.meta import OpenEHRFormat
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState


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