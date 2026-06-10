

import logging

from flask import Blueprint, g, jsonify, make_response, request

import xml.etree.ElementTree as ET

from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import HierObjectID
from pyehr.core.its.rest.additions import ADL14TemplateList, ADL14TemplateListItem
from pyehr.core.its.xml_tools import decode_xml
from pyehr.server.apps.rest.blueprints.shared import _create_empty_response, _create_error_response, _create_not_found_response, _create_object_response, _process_headers
from pyehr.server.apps.rest.meta import OpenEHRFormat
from pyehr.server.change_control import VersionedStore
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyItem
from pyehr.server.security.auth import IPyehrAuthProvider
from pyehr.utils import get_uid_from_object_if_exists


def create_definition_blueprint(auth: IPyehrAuthProvider, db: IDatabaseEngine, vs: VersionedStore):
    def_bp = Blueprint("definition", __name__, url_prefix="/definition")

    log = logging.getLogger("apps.rest.definition")

    default_access_policy = db.retrieve_uid_object("PYEHR_ACCESS_CONTROL_SETTINGS", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000"))
    auth_policy = default_access_policy if default_access_policy is not None else PyehrAccessControlSettings(policies=[PyehrAccessPolicyItem(True)])

    # create template list if it doesn't exist yet in database
    log.info("Checking template list exists")
    meta = db.retrieve_db_metadata(HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1e39"))
    if meta is None or meta.obj_type is None:
        log.info("Template list did not exist in database, creating...")
        new_template_list = ADL14TemplateList([])
        db.create_uid_object(new_template_list)

    def _get_template_list() -> ADL14TemplateList:
        return db.retrieve_uid_object("ADL14_TEMPLATE_LIST", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1e39"))

    def _add_template_to_template_list(item: ADL14TemplateListItem) -> None:
        current_list = _get_template_list()
        current_list.items.append(item)
        db.update_uid_object(current_list)

    @def_bp.before_request
    def process_headers():
        _process_headers(log)

    @def_bp.before_request
    def authenticate_user():
        auth.authenticated_actor()

    @def_bp.route("/template/adl1.4", methods=['GET'])
    def list_templates():
        temp_list = _get_template_list()

        success_resp = make_response(jsonify(temp_list.as_json()["items"]))
        success_resp.status_code = 200
        success_resp.headers["Content-Type"] = "application/json"
        return success_resp
    
    @def_bp.route("/template/adl1.4/<template_id>")
    def get_template(template_id: str):
        obj = db.retrieve_uid_object("TEMPLATE", template_id)

        if obj is None:
            return _create_not_found_response("TEMPLATE", template_id)
        
        success_resp = make_response()
        success_resp.data = ET.tostring(obj.as_xml("template"))
        success_resp.status_code = 200
        success_resp.headers["Content-Type"] = "application/xml"
        return success_resp
        

    @def_bp.route("/template/adl1.4", methods=['POST'])
    def upload_template():
        parse_format = g.processed_headers.provided_content_format
        if parse_format != OpenEHRFormat.XML:
            return _create_error_response("415 Unsupported Media Type: pyehr /definition endpoints support XML only.", 415)
        
        xml_str = bytes.decode(request.data) 

        try:
            templ : OperationalTemplate = decode_xml(xml_str, "TEMPLATE")
        except Exception as ex:
            return _create_error_response(f"400 Bad Request: Error when attempting to parse request body. {str(ex)}", 400)

        meta = db.retrieve_db_metadata(templ.template_id.value)
        if meta is not None and meta.obj_type is not None:
            return _create_error_response(f"409 Conflict: Template with ID \'{templ.template_id.value}\' already exists", 409)
        
            
        db.create_uid_object(templ, uid_override=templ.template_id.value)
        _add_template_to_template_list(ADL14TemplateListItem(templ.template_id.value, templ.concept, templ.definition.archetype_id.value, Env.current_date_time().as_string()))

        success_resp = make_response()
        success_resp.data = ET.tostring(templ.as_xml("template"))
        success_resp.status_code = 201
        success_resp.headers["Content-Type"] = "application/xml"
        return success_resp
        
        
    return def_bp
            


    