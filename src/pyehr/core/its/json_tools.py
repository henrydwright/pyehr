"""Functions and classes for creating and reading OpenEHR JSON files"""

from json import JSONEncoder, dumps
from typing import Union, Optional

from term import CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.identification import HierObjectID, ObjectID, ObjectRef, ObjectVersionID, GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, ImportedVersion, OriginalVersion
from pyehr.core.rm.common.generic import AuditDetails, PartyIdentified, PartySelf, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText, DVUri
from pyehr.core.rm.demographic import PartyIdentity, Person, VersionedParty
from pyehr.core.rm.ehr import EHR, EHRStatus, VersionedEHRStatus
from pyehr.core.rm.support.terminology import TerminologyService

_type_map = {
    "OBJECT_VERSION_ID": ObjectVersionID,
    "OBJECT_REF": ObjectRef,
    "HIER_OBJECT_ID" : HierObjectID,
    "DV_TEXT": DVText,
    "DV_URI": DVUri,
    "DV_DATE_TIME": DVDateTime,
    "PARTY_SELF": PartySelf,
    "EHR": EHR,
    "EHR_STATUS": EHRStatus,
    "ARCHETYPED": Archetyped,
    "ARCHETYPE_ID": ArchetypeID,
    "PARTY_REF": PartyRef,
    "GENERIC_ID": GenericID,
    "PERSON": Person,
    "PARTY_IDENTITY": PartyIdentity,
    "ITEM_TREE": ItemTree,
    "ELEMENT": Element,
    "DV_IDENTIFIER": DVIdentifier,
    "CLUSTER": Cluster,
    "DV_CODED_TEXT": DVCodedText,
    "CODE_PHRASE": CodePhrase,
    "TERMINOLOGY_ID": TerminologyID,
    "VERSIONED_EHR_STATUS": VersionedEHRStatus,
    "REVISION_HISTORY": RevisionHistory,
    "REVISION_HISTORY_ITEM": RevisionHistoryItem,
    "AUDIT_DETAILS": AuditDetails,
    "PARTY_IDENTIFIED": PartyIdentified,
    "ORIGINAL_VERSION": OriginalVersion,
    "IMPORTED_VERSION": ImportedVersion,
    "CONTRIBUTION": Contribution,
    "ITEM_SINGLE": ItemSingle,
    "VERSIONED_PARTY": VersionedParty
}
"""Map of OpenEHR JSON '_type' attributes to pyehr.core types"""

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
                target: Optional[str] = None,
                terminology_service: Optional[TerminologyService] = None,
                flag_allow_resolved_references: bool = True,
                flag_ignore_missing_ehr_access_on_ehr: bool = True,
                flag_ignore_missing_archetype_details_on_ehr_status: bool = True,
                flag_infer_missing_type_details: bool = True,
                flag_replace_empty_dv_text_with_null: bool = True) -> Union[AnyClass, list[AnyClass]]:
    """Decodes Python objects (from JSON) to pyehr.core objects.
    
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
        terminology_service = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

    #print(dumps(json_obj, indent=1))

    if target is not None:
        target_type = target
    else:
        if '_type' not in json_obj:
            raise ValueError("Could not decode object: '_type' attribute not present")
        target_type = json_obj['_type']
    
    if target_type not in _type_map:
        raise NotImplementedError(f"Could not decode object: '_type' of \'{target_type}\' is either not yet supported or is not a valid openEHR type")

    target_cls = _type_map[target_type]
    
    if '_type' in json_obj:
        # not a valid argument
        del json_obj['_type']

    arg_dict = dict()
    for (param_name, param) in json_obj.items():
        if type(param) == str or type(param) == bool:
            arg_dict[param_name] = param
        elif type(param) == dict:
            type_hint = None
            # TODO: replace this with proper hinting and lookups from the schema
            if flag_infer_missing_type_details and target_type == "EHR_STATUS" and param_name == "archetype_details":
                type_hint = "ARCHETYPED"
            elif flag_infer_missing_type_details and target_type == "ARCHETYPED" and param_name == "archetype_id":
                type_hint = "ARCHETYPE_ID"
            arg_dict[param_name] = decode_json(param, target=type_hint, terminology_service=terminology_service)
        elif type(param) == list:
            arg_dict[param_name] = [decode_json(list_item, terminology_service=terminology_service) for list_item in param]
        else:
            raise RuntimeError(f"Could not decode object: unknown type of parameter \'{type(param)}\' encountered during parsing")
        
    if target_type == "OBJECT_REF":
        if "type" in arg_dict:
            # pyehr uses 'ref_type' to avoid collision with Python 'type'
            arg_dict["ref_type"] = arg_dict["type"]
            del arg_dict["type"]
    elif target_type == "EHR_STATUS":
        if flag_ignore_missing_archetype_details_on_ehr_status and not "archetype_details" in json_obj:
            arg_dict["archetype_details"] = Archetyped(ArchetypeID(json_obj["archetype_node_id"]), "1.1.0")
    elif target_type == "EHR":
        if flag_ignore_missing_ehr_access_on_ehr and not "ehr_access" in json_obj:
            arg_dict["ehr_access"] = ObjectRef("null", "VERSIONED_EHR_ACCESS", HierObjectID("00000000-0000-0000-0000-000000000000"))
    elif target_type == "DV_IDENTIFIER":
        # pyehr uses 'id_type' to avoid collision with Python 'type'
        arg_dict["id_type"] = arg_dict["type"]
        del arg_dict["type"]
    elif target_type == "PARTY_IDENTITY":
        # pyehr library uses 'purpose' to clarify meaning of the inherited 'name' field
        arg_dict["purpose"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "PERSON":
        # pyehr library uses 'actor_type' to clarify meaning of inherited 'name' field
        arg_dict["actor_type"] = arg_dict["name"]
        del arg_dict["name"]
    elif target_type == "DV_TEXT":
        if flag_replace_empty_dv_text_with_null and not "value" in json_obj:
            return None
    elif target_type == "AUDIT_DETAILS":
        arg_dict["terminology_service"] = terminology_service
    elif target_type == "ORIGINAL_VERSION":
        arg_dict["terminology_service"] = terminology_service

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

    result = target_cls(**arg_dict)

    if len(instance_list) > 0:
        instance_list.append(result)
        return instance_list
    else:
        return result

        