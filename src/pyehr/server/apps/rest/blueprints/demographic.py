import datetime
import json
from typing import Optional, Union
import logging
from uuid import uuid4

from flask import Blueprint, g, request, jsonify, make_response, Response, current_app

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.json_tools import decode_json
from pyehr.core.its.rest.additions import UpdateContribution
from pyehr.core.rm.common.change_control import Contribution, Version
from pyehr.core.rm.common.generic import PartyIdentified, PartyProxy
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.server.apps.rest.blueprints.shared import _add_headers_to_response, _add_location_headers_to_response, _create_empty_response, _create_error_response, _create_not_found_response, _create_object_response, _get_audit_change_type, _get_audit_description, _get_committer, _get_lifecycle_state, _parse_request_body, _process_headers, commit_contribution_set, create_object, delete_object, get_contribution_by_id, get_object, get_versioned_object, get_versioned_object_version_at_time, get_versioned_object_version_by_id, update_object 
from pyehr.server.apps.rest.meta import OpenEHRFormat, OpenEHRRequestHeaders
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState, VersionedStore
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.auth import IPyehrAuthProvider
from pyehr.utils import get_openehr_type_str

def create_demographic_blueprint(auth: IPyehrAuthProvider, db: IDatabaseEngine, vs: VersionedStore):
    demo_bp = Blueprint("demographic", __name__, url_prefix="/demographic")

    logged_in_user, _ = auth.authenticated_actor()

    log = logging.getLogger("apps.rest.demographic")

    @demo_bp.before_request
    def process_headers():
        _process_headers(log)

    def _is_demographic_type(typ : str):
        return (typ in {"AGENT", "GROUP", "ORGANISATION", "PERSON", "ROLE"})

    @demo_bp.route("/contribution", methods=['POST'])
    def commit_demographic_contribution_set():
        owner_id = ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000"))
        
        return commit_contribution_set(logged_in_user, db, owner_id, log)

    @demo_bp.route("/<demographic_type>", methods=['GET', 'POST'])
    def create_demographic_object(demographic_type: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        owner_id = ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000"))

        resp, ovid = create_object(logged_in_user, vs, typ, owner_id, log)
        if resp.status_code == 201:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.object_id().value}")

        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version/<object_version_id>", methods=['GET'])
    def get_versioned_party_version_by_id(hier_object_id: str, object_version_id: str):
        ovid = ObjectVersionID(object_version_id)
        hid = HierObjectID(hier_object_id)

        resp = get_versioned_object_version_by_id(logged_in_user, db, vs, "PARTY", hid, ovid)
        if resp.status_code == 200:
            _add_location_headers_to_response(resp,  f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/version/{object_version_id}")
        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version", methods=['GET'])
    def get_versioned_party_version_at_time(hier_object_id: str):
        resp, ovid = get_versioned_object_version_at_time(logged_in_user, db, vs, HierObjectID(hier_object_id), "PARTY")
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/version/{ovid.value}")
        return resp
        
    @demo_bp.route("/versioned_party/<hier_object_id>", methods=['GET'])
    def get_versioned_party(hier_object_id: str):
        resp = get_versioned_object(logged_in_user, vs, HierObjectID(hier_object_id), "VERSIONED_PARTY")
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}")
        return resp
        
    @demo_bp.route("/versioned_party/<hier_object_id>/revision_history", methods=['GET'])
    def get_versioned_party_revision_history(hier_object_id: str):
        versioned_party, revhis = vs.retrieve_versioned_object(HierObjectID(hier_object_id), logged_in_user.external_ref)

        if revhis is None:
            return _create_not_found_response("REVISION_HISTORY", hier_object_id)
        else:
            resp = _create_object_response(revhis, 200)
            _add_headers_to_response(resp, HierObjectID(hier_object_id), versioned_party.time_created, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/revision_history")
            return resp
        
    @demo_bp.route("/contribution/<hier_object_id>", methods=['GET'])
    def get_demographic_contribution_by_id(hier_object_id: str):
        resp = get_contribution_by_id(logged_in_user, db, HierObjectID(hier_object_id))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/contribution/{hier_object_id}")
        return resp

    @demo_bp.route("/<demographic_type>/<uid_based_id>", methods=['GET'])
    def get_demographic_object(demographic_type: str, uid_based_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)

        resp, ovid = get_object(logged_in_user, vs, uid_based_id, typ, log)

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.value}")

        return resp
        
    @demo_bp.route("/<demographic_type>/<hier_object_id>", methods=['PUT'])
    def update_demographic_object(demographic_type: str, hier_object_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        resp, ovid = update_object(logged_in_user, vs, typ, hier_object_id, log)

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.value}")

        return resp

    @demo_bp.route("/<demographic_type>/<object_version_id>", methods=['DELETE'])
    def delete_demographic_object(demographic_type: str, object_version_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        return delete_object(logged_in_user, vs, typ, object_version_id, log)
    
    return demo_bp
