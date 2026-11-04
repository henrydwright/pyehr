"""Methods relating to processing of AQL queries"""

from pyehr.core.its.aql.query import AQLModelTypeTreeNode


_ITEM_STRUCTURE_TYPES = (
    "DATA_STRUCTURE",
    "ITEM_STRUCTURE",
    "ITEM_SINGLE",
    "ITEM_LIST",
    "ITEM_TABLE",
    "ITEM_TREE",
)


def _item_structure_containment(attribute_name: str):
    return {
        rm_type: (attribute_name, False, False, False)
        for rm_type in _ITEM_STRUCTURE_TYPES
    }


_PARTY_CONTAINMENT = {
    "PARTY_IDENTITY": ("identities", False, False, True),
    "CONTACT": ("contacts", False, False, True),
    **_item_structure_containment("details"),
    "PARTY_RELATIONSHIP": ("relationships", False, False, True),
}

_ACTOR_CONTAINMENT = {
    **_PARTY_CONTAINMENT,
    "ROLE": ("roles", True, True, True),
    "VERSIONED_PARTY": ("roles", True, False, True),
}

_CONTENT_ITEM_TYPES = (
    "CONTENT_ITEM",
    "SECTION",
    "ENTRY",
    "ADMIN_ENTRY",
    "CARE_ENTRY",
    "OBSERVATION",
    "EVALUATION",
    "INSTRUCTION",
    "ACTION",
)


def _content_item_containment(attribute_name: str, is_multiple: bool):
    return {
        rm_type: (attribute_name, False, False, is_multiple)
        for rm_type in _CONTENT_ITEM_TYPES
    }


CONTAINS_RM_MAP = {
    "COMPOSITION": _content_item_containment("content", True),
    "EHR": {
        "CONTRIBUTION": ("contributions", True, False, True),
        "COMPOSITION": ("compositions", True, True, True),
        "VERSIONED_COMPOSITION": ("compositions", True, False, True),
        "EHR_STATUS": ("ehr_status", True, True, False),
        "VERSIONED_EHR_STATUS": ("ehr_status", True, False, False),
        "EHR_ACCESS": ("ehr_access", True, True, False),
        "VERSIONED_EHR_ACCESS": ("ehr_access", True, False, False),
        "FOLDER": ("folders", True, True, True),
        "VERSIONED_FOLDER": ("folders", True, False, True),
    },
    "SECTION": _content_item_containment("items", True),
    "ADMIN_ENTRY": _item_structure_containment("data"),
    "CARE_ENTRY": _item_structure_containment("protocol"),
    "OBSERVATION": {
        "HISTORY": ("data", False, False, False),
        **_item_structure_containment("protocol"),
    },
    "EVALUATION": _item_structure_containment("data"),
    "INSTRUCTION": {
        "ACTIVITY": ("activities", False, False, True),
        **_item_structure_containment("protocol"),
    },
    "ACTION": _item_structure_containment("description"),
    "ACTIVITY": _item_structure_containment("description"),
    "EVENT": _item_structure_containment("data"),
    "POINT_EVENT": _item_structure_containment("data"),
    "INTERVAL_EVENT": _item_structure_containment("data"),
    "HISTORY": {
        **_item_structure_containment("summary"),
        "EVENT": ("events", False, False, True),
        "POINT_EVENT": ("events", False, False, True),
        "INTERVAL_EVENT": ("events", False, False, True),
    },
    "ITEM_SINGLE": {
        "ELEMENT": ("item", False, False, False),
    },
    "ITEM_LIST": {
        "ELEMENT": ("items", False, False, True),
    },
    "ITEM_TABLE": {
        "CLUSTER": ("rows", False, False, True),
    },
    "ITEM_TREE": {
        "ITEM": ("items", False, False, True),
        "CLUSTER": ("items", False, False, True),
        "ELEMENT": ("items", False, False, True),
    },
    "CLUSTER": {
        "ITEM": ("items", False, False, True),
        "CLUSTER": ("items", False, False, True),
        "ELEMENT": ("items", False, False, True),
    },
    "FOLDER": {
        "COMPOSITION": ("items", True, True, True),
        "VERSIONED_COMPOSITION": ("items", True, False, True),
        "FOLDER": ("folders", False, False, True),
        "VERSIONED_FOLDER": ("items", True, False, True),
        **_item_structure_containment("details"),
    },
    "CONTACT": {
        "ADDRESS": ("addresses", False, False, True),
    },
    "ADDRESS": _item_structure_containment("details"),
    "PARTY_RELATIONSHIP": _item_structure_containment("details"),
    "PARTY": _PARTY_CONTAINMENT.copy(),
    "ACTOR": _ACTOR_CONTAINMENT.copy(),
    "PERSON": _ACTOR_CONTAINMENT.copy(),
    "ORGANISATION": _ACTOR_CONTAINMENT.copy(),
    "GROUP": _ACTOR_CONTAINMENT.copy(),
    "AGENT": _ACTOR_CONTAINMENT.copy(),
    "ROLE": {
        **_PARTY_CONTAINMENT,
        "CAPABILITY": ("capabilities", False, False, True),
    },
    "CAPABILITY": _item_structure_containment("credentials"),
    "EHR_STATUS": _item_structure_containment("other_details"),
    "EVENT_CONTEXT": _item_structure_containment("other_context"),
    "INSTRUCTION_DETAILS": _item_structure_containment("wf_details"),
    "FEEDER_AUDIT_DETAILS": _item_structure_containment("other_details"),
}
"""Provides a mapping between a type A, some type B that can be 'contained' within A, and 

1) the attribute of A that can contain B; 
2) is_reference: if it is the object itself - False, or a reference to the object - True; 
3) is_versioned: if it is the type itself - False, or a VERSIONED_OBJECT of that type - True
4) is_multiple: if A can have at most 1 of B - False, or if A can contain more than 1 B - True"""
