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
from pyehr.server.apps.rest.blueprints.shared import _add_headers_to_response, _add_location_headers_to_response, _create_empty_response, _create_error_response, _create_not_found_response, _create_object_response, _get_archetype_id_from_request_body, _get_audit_change_type, _get_audit_description, _get_committer, _get_lifecycle_state, _parse_request_body, _process_headers, commit_contribution_set, create_object, delete_object, get_contribution_by_id, get_object, get_versioned_object, get_versioned_object_version_at_time, get_versioned_object_version_by_id, update_object 
from pyehr.server.apps.rest.meta import OpenEHRFormat, OpenEHRRequestHeaders
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState, VersionedStore
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyEndpoint, PyehrAccessPolicyEndpointAction, PyehrAccessPolicyItem
from pyehr.server.security.auth import IPyehrAuthProvider
from pyehr.utils import get_openehr_type_str

def create_demographic_blueprint(auth: IPyehrAuthProvider, db: IDatabaseEngine, vs: VersionedStore):
    demo_bp = Blueprint("demographic", __name__, url_prefix="/demographic")

    log = logging.getLogger("apps.rest.demographic")

    default_access_policy = db.retrieve_uid_object("PYEHR_ACCESS_CONTROL_SETTINGS", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000"))
    auth_policy = default_access_policy if default_access_policy is not None else PyehrAccessControlSettings(policies=[PyehrAccessPolicyItem(True)])

    @demo_bp.before_request
    def process_headers():
        _process_headers(log)

    @demo_bp.before_request
    def authenticate_user():
        auth.authenticated_actor()

    def _is_demographic_type(typ : str):
        return (typ in {"AGENT", "GROUP", "ORGANISATION", "PERSON", "ROLE"})

    @demo_bp.route("/contribution", methods=['POST'])
    def commit_demographic_contribution_set():
        owner_id = ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000"))
        
        return commit_contribution_set(auth, db, owner_id, log, (auth_policy, PyehrAccessPolicyEndpoint.DEMOGRAPHIC_CONTRIBUTION))

    @demo_bp.route("/<demographic_type>", methods=['GET', 'POST'])
    def create_demographic_object(demographic_type: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        ep_map = {
            "AGENT": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_AGENT,
            "GROUP": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_GROUP,
            "ORGANISATION": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ORGANISATION,
            "PERSON": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_PERSON,
            "ROLE": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ROLE
        }
        ep = ep_map[typ]
        
        owner_id = ObjectRef("null", "NULL", HierObjectID("00000000-0000-0000-0000-000000000000"))

        resp, ovid = create_object(auth, vs, typ, owner_id, log, (auth_policy, ep))
        if resp.status_code == 201:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.object_id().value}")

        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version/<object_version_id>", methods=['GET'])
    def get_versioned_party_version_by_id(hier_object_id: str, object_version_id: str):
        ovid = ObjectVersionID(object_version_id)
        hid = HierObjectID(hier_object_id)

        resp = get_versioned_object_version_by_id(auth, db, vs, "PARTY", hid, ovid, (auth_policy, PyehrAccessPolicyEndpoint.DEMOGRAPHIC_VERSIONED_PARTY))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp,  f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/version/{object_version_id}")
        return resp

    @demo_bp.route("/versioned_party/<hier_object_id>/version", methods=['GET'])
    def get_versioned_party_version_at_time(hier_object_id: str):
        resp, ovid = get_versioned_object_version_at_time(auth, db, vs, HierObjectID(hier_object_id), "PARTY", (auth_policy, PyehrAccessPolicyEndpoint.DEMOGRAPHIC_VERSIONED_PARTY))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/version/{ovid.value}")
        return resp
        
    @demo_bp.route("/versioned_party/<hier_object_id>", methods=['GET'])
    def get_versioned_party(hier_object_id: str):
        resp = get_versioned_object(auth, vs, HierObjectID(hier_object_id), "VERSIONED_PARTY", (auth_policy, PyehrAccessPolicyEndpoint.DEMOGRAPHIC_VERSIONED_PARTY))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}")
        return resp
        
    @demo_bp.route("/versioned_party/<hier_object_id>/revision_history", methods=['GET'])
    def get_versioned_party_revision_history(hier_object_id: str):
        if not auth.action_authorised_for_authenticated_actor(auth_policy,
                                        {PyehrAccessPolicyEndpointAction.GET},
                                        PyehrAccessPolicyEndpoint.DEMOGRAPHIC_VERSIONED_PARTY):
            return _create_error_response("403 Forbidden: Access denied under auth policy", 403)
        
        versioned_party, revhis = vs.retrieve_versioned_object(HierObjectID(hier_object_id), auth.authenticated_actor()[0].external_ref)

        if revhis is None:
            return _create_not_found_response("REVISION_HISTORY", hier_object_id)
        else:
            resp = _create_object_response(revhis, 200)
            _add_headers_to_response(resp, HierObjectID(hier_object_id), versioned_party.time_created, f"{current_app.config["BASE_URL"]}/demographic/versioned_party/{hier_object_id}/revision_history")
            return resp
        
    @demo_bp.route("/contribution/<hier_object_id>", methods=['GET'])
    def get_demographic_contribution_by_id(hier_object_id: str):
        resp = get_contribution_by_id(auth, db, HierObjectID(hier_object_id), (auth_policy, PyehrAccessPolicyEndpoint.DEMOGRAPHIC_CONTRIBUTION))
        if resp.status_code == 200:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/contribution/{hier_object_id}")
        return resp

    @demo_bp.route("/<demographic_type>/<uid_based_id>", methods=['GET'])
    def get_demographic_object(demographic_type: str, uid_based_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        ep_map = {
            "AGENT": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_AGENT,
            "GROUP": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_GROUP,
            "ORGANISATION": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ORGANISATION,
            "PERSON": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_PERSON,
            "ROLE": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ROLE
        }
        ep = ep_map[typ]

        resp, ovid = get_object(auth, vs, uid_based_id, typ, log, (auth_policy, ep))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.value}")

        return resp
        
    @demo_bp.route("/<demographic_type>/<hier_object_id>", methods=['PUT'])
    def update_demographic_object(demographic_type: str, hier_object_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        ep_map = {
            "AGENT": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_AGENT,
            "GROUP": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_GROUP,
            "ORGANISATION": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ORGANISATION,
            "PERSON": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_PERSON,
            "ROLE": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ROLE
        }
        ep = ep_map[typ]
        
        resp, ovid = update_object(auth, vs, typ, hier_object_id, log, (auth_policy, ep))

        if ovid is not None:
            _add_location_headers_to_response(resp, f"{current_app.config["BASE_URL"]}/demographic/{typ.lower()}/{ovid.value}", f"demographic://{ovid.value}")

        return resp

    @demo_bp.route("/<demographic_type>/<object_version_id>", methods=['DELETE'])
    def delete_demographic_object(demographic_type: str, object_version_id: str):
        typ = demographic_type.upper()
        if not _is_demographic_type(typ):
            return _create_error_response("", 404)
        
        ep_map = {
            "AGENT": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_AGENT,
            "GROUP": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_GROUP,
            "ORGANISATION": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ORGANISATION,
            "PERSON": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_PERSON,
            "ROLE": PyehrAccessPolicyEndpoint.DEMOGRAPHIC_ROLE
        }
        ep = ep_map[typ]
        
        return delete_object(auth, vs, typ, object_version_id, log, (auth_policy, ep))
    
    return demo_bp
