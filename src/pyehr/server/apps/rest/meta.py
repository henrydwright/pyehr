from enum import StrEnum
from typing import Optional
from flask import Request

import logging

from pyehr.core.base.base_types.identification import ObjectID, ObjectVersionID, PartyRef
from pyehr.core.rm.common.generic import PartyIdentified
from pyehr.core.rm.data_types.text import DVText
from pyehr.server.change_control import AuditChangeType, VersionLifecycleState

IGNORE_CLIENT_VERSION_DETAILS_HEADERS = False
LOG_HEADERS = False

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

    version_lifecycle_state: Optional[VersionLifecycleState] = None
    """Contents of the `openehr-version` header for operations that can take audit information from the client"""

    version_audit_change_type: Optional[AuditChangeType] = None
    """Contents of the `openehr-audit-details` header (change_type.) operations that can take audit information from the client"""

    version_audit_description: Optional[DVText] = None
    """Contents of the `openehr-audit-details` header (description.) for operations that can take audit information from the client"""

    version_committer: Optional[PartyIdentified] = None
    """Contents of the `openehr-audit-details` header (committer.) for operations that can take audit information from the client"""

    def __init__(self, log: logging.Logger, request_content: Request):
        if LOG_HEADERS:
            for header in request_content.headers:
                log.debug(str(header))
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
        
        openehr_lifecycle_state = request_content.headers.get("openehr-version")
        if openehr_lifecycle_state is not None:
            code_string = openehr_lifecycle_state.split("\"")[1]
            self.version_lifecycle_state = VersionLifecycleState.from_code_string(code_string)

        audit_details = request_content.headers.get("openehr-audit-details")
        if audit_details is not None:
            audit_details = audit_details[:-1]
            audit_details_list = audit_details.split("\",")
            audit_details_map = dict()
            for item in audit_details_list:
                eq_split = item.split("=\"")
                audit_details_map[eq_split[0]] = eq_split[1]
            
            if "change_type.code_string" in audit_details_map:
                code_string = audit_details_map["change_type.code_string"]
                self.version_audit_change_type = AuditChangeType.from_code_string(code_string)

            if "description.value" in audit_details_map:
                self.version_audit_description = DVText(audit_details_map["description.value"])

            xref = None
            if "committer.external_ref.id" in audit_details_map:
                xref = PartyRef(audit_details_map["committer.external_ref.namespace"], audit_details_map["committer.external_ref.type"], ObjectID(audit_details_map["committer.external_ref.id"]))
            name = None
            if "committer.name" in audit_details_map:
                name = audit_details_map["committer.name"]
            if name is not None or xref is not None:
                self.version_committer = PartyIdentified(external_ref=xref, name=name)

