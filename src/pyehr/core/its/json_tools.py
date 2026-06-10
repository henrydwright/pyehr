"""Functions and classes for creating and reading OpenEHR JSON files"""

import base64
from json import JSONEncoder
import json
from typing import Union, Optional

import numpy as np
from pyehr.core.base.foundation_types.interval import PointInterval, ProperInterval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.rest.additions import UpdateAttestation, UpdateAudit, UpdateContribution, UpdateVersion
from pyehr.core.rm.common.change_control import Contribution, ImportedVersion, OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import Attestation, AuditDetails, PartyIdentified, PartySelf, RevisionHistory, RevisionHistoryItem
from pyehr.server.security.access_control import PyehrAccessPolicyEndpoint, PyehrAccessPolicyEndpointAction
from pyehr.types import OPENEHR_TYPE_MAP
from pyehr.core.base.base_types.identification import HierObjectID, InternetID, ObjectID, ObjectRef, ObjectVersionID, GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText, DVUri
from pyehr.core.rm.demographic import Address, Agent, Contact, Organisation, PartyIdentity, Person, VersionedParty
from pyehr.core.rm.ehr import EHR, EHRStatus, VersionedEHRStatus
from pyehr.core.rm.support.terminology import TerminologyService

from pyehr.term import PyehrGlobalTerminologyService

_possible_object_refs = {
    "EHR": {
        "contributions": "CONTRIBUTION",
        "ehr_status": "VERSIONED_EHR_STATUS",
        "ehr_access": "VERSIONED_EHR_ACCESS",
        "compositions": "VERSIONED_COMPOSITION",
        "folders": "VERSIONED_FOLDER"
        }
}
"""Map of OpenEHR types to a map of attribute name (of a possible OBJECT_REF) to if the attribute is a list or not"""

class OpenEHREncoder(JSONEncoder):
    """Implementation of `json.JSONEncoder` that can be used with json.dumps() to produce
    OpenEHR ITS JSON encodings of all base and rm classes. e.g. `json.dumps(my_openehr_object, cls=OpenEHREncoder)`"""
    
    def default(self, o):
        try:
            return o.as_json()
        except:
            return super().default(o)

def _obj_uid_or_none(obj: AnyClass) -> Optional[ObjectID]:
        if isinstance(obj, EHR):
            return obj.ehr_id
        if not hasattr(obj, "uid"):
            return None
        uid = obj.uid
        if callable(uid):
            uid = obj.uid()
        return uid

def decode_json(json_obj: dict, 
                python_params: Optional[dict] = None,
                target: Optional[str] = None,
                terminology_service: Optional[TerminologyService] = None,
                flag_allow_resolved_references: bool = True,
                flag_ignore_missing_ehr_access_on_ehr: bool = True,
                flag_ignore_missing_archetype_details_on_ehr_status: bool = True,
                flag_infer_missing_type_details: bool = True,
                flag_replace_empty_dv_text_with_null: bool = True) -> Union[AnyClass, list[AnyClass]]:
    """Decodes Python objects (from JSON) to pyehr.core objects.
    
    :param python_params: (Optional) Dict of Python parameters to provide at class creation (e.g. for references to parents)
    :param target_type: (Optional) Set the target type to decode to explicitly. Overrides the '_type' parameter, if present.
    :param terminology_service: (Optional) Provide a terminology service, if not provided, uses the inbuilt pyehr terminology service.
    :param flag_allow_resolved_references: (Optional, default=True) Some APIs do not return OBJECT_REF as per the OpenEHR
                                           RM specification, instead returning the target type. This flag allows the method
                                           to return a list of items with `OBJECT_REF` with GENERIC_IDs set to indicies within
                                           the list and namespace of 'pyehr_decode_list' (e.g. if type is `EHR` and `ehr_status` is
                                           of type `EHR_STATUS` rather than `OBJECT_REF`, a list will be returned with the EHR.ehr_status set
                                           to an OBJECT_REF with namespace 'pyehr_decode_list' and ID of list index for the EHR_STATUS object).
    :param flag_ignore_missing_ehr_access_on_ehr: (Optional, default=True) The EHR_ACCESS object is implementation specific 
                                                  so some APIs do not provide it at all (e.g. EHRBase). This flag replaces a 
                                                  missing instance with an ObjectRef to null.
    :param flag_take_archetype_node_id_as_details_on_ehr_status: (Optional, default=True) The EHR_STATUS object should have archetype details
                                                                 attached as it is an archetype root (per specification invariances) but some
                                                                 implementations (e.g. EHRBase) just include archetype_node_id. This flag creates
                                                                 a new ARCHETYPED with the contents of archetype_node_id
    :param flag_infer_missing_type_details: (Optional, default=True) If a '_type' parameter is missing, still try to decode using a target type
                                                                     based on the JSON ITS schema.
    :param flag_replace_empty_dv_text_with_null: (Optional, default=True) If an empty DV_TEXT (i.e. DV_TEXT without value) is encountered, ignore this
                                                                          and replace it with `None` in any relevant object. Sometimes EHRBase does this."""

    if terminology_service is None:
        terminology_service = PyehrGlobalTerminologyService.get_global_terminology_service()

    if target is not None:
        target_type = target
    else:
        if '_type' not in json_obj:
            print(str(json_obj))
            raise ValueError("Could not decode object: '_type' attribute not present")
        target_type = json_obj['_type']
    
    if target_type not in OPENEHR_TYPE_MAP:
        raise NotImplementedError(f"Could not decode object: '_type' of \'{target_type}\' is either not yet supported or is not a valid openEHR type")

    target_cls = OPENEHR_TYPE_MAP[target_type]
    
    if '_type' in json_obj:
        # not a valid argument
        del json_obj['_type']

    create_parent_first_params = dict()

    arg_dict = dict()
    for (param_name, param) in json_obj.items():
        if type(param) == str or type(param) == bool:
            arg_dict[param_name] = param
        elif type(param) == int:
            arg_dict[param_name] = np.int32(param)
            if target_type == "DV_COUNT":
                arg_dict[param_name] = np.int64(param)
        elif type(param) == float:
            arg_dict[param_name] = np.float32(param)
        elif type(param) == dict:
            if target_type == "TRANSLATION_DETAILS" and param_name == "author":
                arg_dict[param_name] = param
                continue
            elif target_type == "RESOURCE_DESCRIPTION" and param_name in ["original_author", "ip_acknowledgements", "references", "conversion_details", "other_details"]:
                arg_dict[param_name] = param
                continue
            elif (target_type == "POINT_EVENT" or target_type == "INTERVAL_EVENT") and (python_params is None):
                raise ValueError("Cannot decode 'POINT_EVENT' or 'INTERVAL_EVENT' unless they are part of 'events' in a HISTORY.")
            
            type_hint = None
            
            # TODO: replace this with proper hinting and lookups from the schema
            if flag_infer_missing_type_details and target_type == "EHR_STATUS" and param_name == "archetype_details":
                type_hint = "ARCHETYPED"
            elif flag_infer_missing_type_details and target_type == "ARCHETYPED" and param_name == "archetype_id":
                type_hint = "ARCHETYPE_ID"
            arg_dict[param_name] = decode_json(param, target=type_hint, terminology_service=terminology_service)
        elif type(param) == list:
            if len(param) > 0:
                item = param[0]
                if isinstance(item, str):
                    arg_dict[param_name] = param
                    continue
            if target_type == "PYEHR_ACCESS_POLICY_ITEM":
                if param_name == "actions":
                    arg_dict["actions"] = [PyehrAccessPolicyEndpointAction(action) for action in param]
                    continue
                elif param_name == "endpoints":
                    arg_dict["endpoints"] = [PyehrAccessPolicyEndpoint(endpoint) for endpoint in param]
                    continue
                elif param_name == "archetype_ids":
                    arg_dict["archetype_ids"] = param
                    continue
            elif target_type == "HISTORY":
                if param_name == "events":
                    create_parent_first_params["events"] = param
                    continue
            elif target_type == "ADL14_TEMPLATE_LIST":
                # type hint as schema doesn't use _type for the inner items
                arg_dict[param_name] = [decode_json(list_item, target="ADL14_TEMPLATE_LIST_ITEM", terminology_service=terminology_service) for list_item in param]
                continue
            arg_dict[param_name] = [decode_json(list_item, terminology_service=terminology_service) for list_item in param]
        else:
            raise RuntimeError(f"Could not decode object: unknown type of parameter \'{type(param)}\' encountered during parsing")
        
    # change the target type here if needed
    if target_type == "INTERVAL":
        if arg_dict["lower_included"] == arg_dict["upper_included"] and "lower" in arg_dict and "upper" in arg_dict and is_equal_value(arg_dict["lower"], arg_dict["upper"]):
            target_type = "POINT_INTERVAL"
            target_cls = PointInterval
        else:
            target_type = "PROPER_INTERVAL"
            target_cls = ProperInterval

    # perform any modifications to the arg_dict here depending on the target type
    if target_type == "OBJECT_REF":
        if "type" in arg_dict:
            # pyehr uses 'ref_type' to avoid collision with Python 'type'
            arg_dict["ref_type"] = arg_dict["type"]
            del arg_dict["type"]
    elif target_type == "POINT_INTERVAL":
        arg_dict["point_value"] = arg_dict["lower"]
    elif target_type == "PROPER_INTERVAL":
        del arg_dict["lower_unbounded"]
        del arg_dict["upper_unbounded"]
    elif target_type == "EHR_STATUS":
        if flag_ignore_missing_archetype_details_on_ehr_status and not "archetype_details" in json_obj:
            arg_dict["archetype_details"] = Archetyped(ArchetypeID(json_obj["archetype_node_id"]), "1.1.0")
    elif target_type == "EHR":
        if flag_ignore_missing_ehr_access_on_ehr and not "ehr_access" in json_obj:
            arg_dict["ehr_access"] = ObjectRef("null", "VERSIONED_EHR_ACCESS", HierObjectID("00000000-0000-0000-0000-000000000000"))
    elif target_type == "DV_IDENTIFIER":
        # pyehr uses 'id_type' to avoid collision with Python 'type'
        if "type" in arg_dict:
            arg_dict["id_type"] = arg_dict["type"]
            del arg_dict["type"]
    elif target_type == "PARTY_IDENTITY":
        # pyehr library uses 'purpose' to clarify meaning of the inherited 'name' field
        arg_dict["purpose"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "PERSON" or target_type == "ORGANISATION" or target_type == "AGENT":
        # pyehr library uses 'actor_type' to clarify meaning of inherited 'name' field
        arg_dict["actor_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "ADDRESS":
        # pyehr library used 'addr_type' to clarify meaning of inherited 'name' field
        arg_dict["addr_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "GROUP":
        # pyehr library used 'actor_type' to clarify meaning of inherited 'name' field
        arg_dict["actor_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "PARTY_RELATIONSHIP":
        # pyehr library used 'rel_type' to clarify meaning of inherited 'name' field
        arg_dict["rel_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "CONTACT":
        # pyehr library used 'purpose' to clarify meaning of inherited 'name' field
        arg_dict["purpose"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "ROLE":
        # pyehr library used 'role_type' to clarify meaning of inherited 'name' field
        arg_dict["role_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "DV_TEXT":
        if flag_replace_empty_dv_text_with_null and not "value" in json_obj:
            return None
    elif target_type == "AUDIT_DETAILS":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "ORIGINAL_VERSION":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "ATTESTATION":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "UPDATE_AUDIT":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "UPDATE_VERSION":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "COMPOSITION":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "DV_MULTIMEDIA":
        if "data" in arg_dict:
            arg_dict["data"] = base64.decodebytes(arg_dict["data"].encode())
    elif target_type == "DV_INTERVAL":
        del arg_dict["lower_unbounded"]
        del arg_dict["upper_unbounded"]
    elif target_type == "DV_PROPORTION":
        # uses 'proportion_type' to avoid collision with python keyword type
        arg_dict["proportion_type"] = arg_dict["type"]
        del arg_dict["type"]
    elif target_type == "LINK":
        # uses 'link_type' to avoid collision with python keyword type
        arg_dict["link_type"] = arg_dict["type"]
        del arg_dict["type"]
    elif target_type == "PYEHR_ACCESS_POLICY_ITEM":
        # read lists of strs as sets of enums
        if "actions" in arg_dict:
            action_str_list = arg_dict["actions"]
            action_enum_set = set()
            for action in action_str_list:
                action_enum_set.add(PyehrAccessPolicyEndpointAction(action))
            arg_dict["actions"] = action_enum_set
        if "endpoints" in arg_dict:
            endpoint_str_list = arg_dict["endpoints"]
            endpoint_enum_set = set()
            for endpoint in endpoint_str_list:
                endpoint_enum_set.add(PyehrAccessPolicyEndpoint(endpoint))
            arg_dict["endpoints"] = endpoint_enum_set
        # turn lists into sets
        if "roles" in arg_dict:
            arg_dict["roles"] = set(arg_dict["roles"])
        if "archetype_ids" in arg_dict:
            arg_dict["archetype_ids"] = set(arg_dict["archetype_ids"])
        if "organisations" in arg_dict:
            arg_dict["organisations"] = set(arg_dict["organisations"])

    instance_list = []
    if flag_allow_resolved_references:
        i = 0
        if target_type in _possible_object_refs:
            for (oref_param, oref_type) in _possible_object_refs[target_type].items():
                if oref_param in arg_dict:
                    potential_oref_obj = arg_dict[oref_param]
                    if isinstance(potential_oref_obj, list):
                        oref_lst = potential_oref_obj
                        for j in range(len(oref_lst)):
                            if not isinstance(oref_lst[j], ObjectRef):
                                # need to swap for OBJECT_REF
                                instance_list.append(oref_lst[j])
                                target_uid = _obj_uid_or_none(oref_lst[j])
                                if target_uid is not None:
                                    if isinstance(target_uid, ObjectVersionID) and oref_type == "VERSIONED_EHR_STATUS":
                                        target_uid = HierObjectID(target_uid.object_id().value)
                                    oref_lst[j] = ObjectRef("local", oref_type, target_uid)
                                else:
                                    oref_lst[j] = ObjectRef("pyehr_decode_json", oref_type, GenericID(str(i), "list_index"))
                                i = i + 1
                    else:
                        if not isinstance(potential_oref_obj, ObjectRef):
                            # need to swap for OBJECT_REF
                            instance_list.append(potential_oref_obj)
                            target_uid = _obj_uid_or_none(potential_oref_obj)
                            if target_uid is not None:
                                if isinstance(target_uid, ObjectVersionID) and oref_type == "VERSIONED_EHR_STATUS":
                                    target_uid = HierObjectID(target_uid.object_id().value)
                                arg_dict[oref_param] = ObjectRef("local", oref_type, target_uid)
                            else:
                                arg_dict[oref_param] = ObjectRef("pyehr_decode_json", oref_type, GenericID(str(i), "list_index"))

    if python_params is not None:
        for (param_name, param) in python_params.items():
            arg_dict[param_name] = param

    result = target_cls(**arg_dict)

    if create_parent_first_params is not None:
        for (param_name, param) in create_parent_first_params.items():
            decoded = None
            if isinstance(param, list):
                decoded = [decode_json(list_item, python_params={"parent": result}, terminology_service=terminology_service) for list_item in param]
            else:
                decoded = decode_json(param, python_params={"parent": result}, terminology_service=terminology_service)

            setattr(result, param_name, decoded)


    if len(instance_list) > 0:
        instance_list.append(result)
        return instance_list
    else:
        return result


