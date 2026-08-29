"""This file contains base constraint models for RM types"""

from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CPrimitiveObject, CSingleAttribute
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CBoolean, CString
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.interval import MultiplicityInterval, Cardinality
from pyehr.core.rm.data_types.text import DVText

from numpy import int32
from copy import deepcopy

INT_ZERO_TO_MANY = MultiplicityInterval(int32(0))
INT_OPTIONAL = MultiplicityInterval(int32(0), int32(0))
INT_REQUIRED = MultiplicityInterval(int32(1), int32(1))

CARD_ZERO_TO_MANY_LIST = Cardinality(True, False, INT_ZERO_TO_MANY)

CPO_ANY_STRING = CPrimitiveObject(
                    "STRING",
                    MultiplicityInterval(int32(1), int32(1)),
                    "",
                    item=CString(pattern=r".*")
                )

# BASE

# BASE.IDENTIFICATION
ABSTRACT_OBJECT_ID = CComplexObject(
    "OBJECT_ID",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            MultiplicityInterval(int32(1), int32(1)),
            children=[
                CPO_ANY_STRING
            ]
        )
    ]
)

ABSTRACT_UID_BASED_ID = deepcopy(ABSTRACT_OBJECT_ID)
ABSTRACT_UID_BASED_ID.rm_type_name = "UID_BASED_ID"

HIER_OBJECT_ID = deepcopy(ABSTRACT_UID_BASED_ID)
HIER_OBJECT_ID.rm_type_name = "HIER_OBJECT_ID"

VERSION_TREE_ID = deepcopy(ABSTRACT_OBJECT_ID) # this is not the inheritance but a shortcut
VERSION_TREE_ID.rm_type_name = "VERSION_TREE_ID"
VERSION_TREE_ID.attributes[0].children[0].item = CString(pattern=r"^([1-9][0-9]*)(\\.[1-9][0-9]*\\.[1-9][0-9]*)?$")

OBJECT_VERSION_ID = deepcopy(ABSTRACT_UID_BASED_ID)
OBJECT_VERSION_ID.rm_type_name = "OBJECT_VERSION_ID"

ARCHETYPE_ID = deepcopy(ABSTRACT_OBJECT_ID)
ARCHETYPE_ID.rm_type_name = "ARCHETYPE_ID"
ARCHETYPE_ID.attributes[0].children[0].item = CString(pattern=r"^(([a-zA-Z][a-zA-Z0-9_]*)-([a-zA-Z][a-zA-Z0-9_]*)-([a-zA-Z][a-zA-Z0-9_]*))\\.(([a-zA-Z][a-zA-Z0-9_]*)((?:-[a-zA-Z][a-zA-Z0-9_]*)*)?)\\.(v[0-9][0-9]*)$")

TEMPLATE_ID = deepcopy(ABSTRACT_OBJECT_ID)
TEMPLATE_ID.rm_type_name = "TEMPLATE_ID"

TERMINOLOGY_ID = deepcopy(ABSTRACT_OBJECT_ID)
TERMINOLOGY_ID.rm_type_name = "TERMINOLOGY_ID"
TERMINOLOGY_ID.attributes[0].children[0].item = CString(pattern=r"^([a-zA-Z][a-zA-Z0-9_\\-\\/+]*)(\\([a-zA-Z0-9_\\.\\-\\/+]*\\))?$")

GENERIC_ID = deepcopy(ABSTRACT_OBJECT_ID)
GENERIC_ID.rm_type_name = "GENERIC_ID"
GENERIC_ID.attributes.append(
    CSingleAttribute(
                "scheme",
                MultiplicityInterval(int32(1), int32(1)),
                children=[
                    CPO_ANY_STRING
                ]
            )
)

SUBCLASS_OBJECT_ID = [
    GENERIC_ID,
    TERMINOLOGY_ID,
    TEMPLATE_ID,
    ARCHETYPE_ID,
    OBJECT_VERSION_ID,
    HIER_OBJECT_ID
]

SUBCLASS_UID_BASED_ID = [
    OBJECT_VERSION_ID,
    HIER_OBJECT_ID
]

OBJECT_REF = CComplexObject(
    "OBJECT_REF",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "namespace",
            INT_REQUIRED,
            children=[
                CPO_ANY_STRING
            ]
        ),
        CSingleAttribute(
            "type",
            INT_REQUIRED,
            children=[
                CPO_ANY_STRING
            ]
        ),
        CSingleAttribute(
            "id",
            INT_REQUIRED,
            children=SUBCLASS_OBJECT_ID
        )
    ]
)

PARTY_REF = deepcopy(OBJECT_REF)
PARTY_REF.rm_type_name = "PARTY_REF"
PARTY_REF.attributes[1].children[0].item = CString(list_open=False, list_var=["PERSON", "ORGANISATION", "GROUP", "AGENT", "ROLE", "PARTY", "ACTOR"])

LOCATABLE_REF = deepcopy(OBJECT_REF)
LOCATABLE_REF.rm_type_name = "LOCATABLE_REF"
LOCATABLE_REF.attributes[2].children = SUBCLASS_UID_BASED_ID
LOCATABLE_REF.attributes.append(
    CSingleAttribute(
        "path",
        INT_OPTIONAL,
        children=[
            CPO_ANY_STRING
        ]
    )
)

# RM

# RM.DATA_TYPES

# RM.DATA_TYPES.BASIC
DV_IDENTIFIER = CComplexObject(
    "DV_IDENTIFIER",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "id",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "issuer",
            INT_OPTIONAL,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "assigner",
            INT_OPTIONAL,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "type",
            INT_OPTIONAL,
            children=[CPO_ANY_STRING]
        )
    ]
)

DV_BOOLEAN = CComplexObject(
    "DV_BOOLEAN",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[
                CPrimitiveObject(
                    "BOOLEAN",
                    INT_REQUIRED,
                    "",
                    item=CBoolean(True, True)
                )
            ]
        )
    ]
)

# RM.DATA_TYPES.URI
DV_URI = CComplexObject(
    "DV_URI",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[
                CPO_ANY_STRING
            ]
        )
    ]
)

DV_EHR_URI = deepcopy(DV_URI)
DV_EHR_URI.rm_type_name = "DV_EHR_URI"

# RM.DATA_TYPES.TEXT
CODE_PHRASE = CComplexObject(
    "CODE_PHRASE",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "terminology_id",
            INT_REQUIRED,
            children=[
                TERMINOLOGY_ID
            ]
        ),
        CSingleAttribute(
            "code_string",
            INT_REQUIRED,
            children=[
                CPO_ANY_STRING
            ]
        ),
        CSingleAttribute(
            "preferred_term",
            INT_OPTIONAL,
            children=[
                CPO_ANY_STRING
            ]
        )
    ]
)

required_code_phrase = deepcopy(CODE_PHRASE)
required_code_phrase.occurrences = INT_REQUIRED
TERM_MAPPING = CComplexObject(
    "TERM_MAPPING",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "match",
            INT_REQUIRED,
            children=[
                CPrimitiveObject(
                    "STRING",
                    INT_REQUIRED,
                    "",
                    item=CString(list_open=False, list_var=['>', '=', '<', '?'])
                )
            ]
        ),
        CSingleAttribute(
            "purpose",
            INT_OPTIONAL
        ),
        CSingleAttribute(
            "target",
            INT_REQUIRED,
            children=[
                required_code_phrase
            ]
        )
    ]
)

DV_TEXT = CComplexObject(
    "DV_TEXT",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "hyperlink",
            INT_OPTIONAL,
            children=[
                DV_URI
            ]
        ),
        CSingleAttribute(
            "formatting",
            INT_OPTIONAL,
            children=[CPO_ANY_STRING]
        ),
        CMultipleAttribute(
            "mappings",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST
        ),
        CSingleAttribute(
            "language",
            INT_OPTIONAL,
            children=[CODE_PHRASE]
        ),
        CSingleAttribute(
            "encoding",
            INT_OPTIONAL,
            children=[CODE_PHRASE]
        )

    ]
)

DV_CODED_TEXT = deepcopy(DV_TEXT)
DV_CODED_TEXT.attributes.append(
    CSingleAttribute(
        "defining_code",
        INT_REQUIRED,
        children=[required_code_phrase]
    )
)

# fool around here because TERM_MAPPING is in DV_CODED_TEXT and also depends on it
TERM_MAPPING.attributes[1].children = [DV_CODED_TEXT]
many_term_mappings = deepcopy(TERM_MAPPING)
many_term_mappings.occurrences = INT_ZERO_TO_MANY
DV_TEXT.attributes[3].children = [many_term_mappings]
DV_CODED_TEXT.attributes[3].children = [many_term_mappings]

SUBCLASS_DATA_VALUE = [DV_URI, DV_EHR_URI, DV_TEXT, DV_CODED_TEXT, DV_IDENTIFIER]

# RM.COMMON

# RM.COMMON.ARCHETYPED
required_dv_text = deepcopy(DV_TEXT)
required_dv_text.occurrences = INT_REQUIRED

required_dv_ehr_uri = deepcopy(DV_EHR_URI)
required_dv_ehr_uri.occurrences = INT_REQUIRED

LINK = CComplexObject(
    "LINK",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "meaning",
            INT_REQUIRED,
            children=[required_dv_text]
        ),
        CSingleAttribute(
            "link_type",
            INT_REQUIRED,
            children=[required_dv_text]
        ),
        CSingleAttribute(
            "target",
            INT_REQUIRED,
            children=[required_dv_ehr_uri]
        )
    ]
)

required_archetype_id = deepcopy(ARCHETYPE_ID)
required_archetype_id.occurrences = INT_REQUIRED
ARCHETYPED = CComplexObject(
    "ARCHETYPED",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "archetype_id",
            INT_REQUIRED,
            children=[required_archetype_id]
        ),
        CSingleAttribute(
            "template_id",
            INT_OPTIONAL,
            children=[TEMPLATE_ID]
        ),
        CSingleAttribute(
            "rm_version",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        )
    ]
)

many_links = deepcopy(LINK)
many_links.occurrences = INT_ZERO_TO_MANY
LOCATABLE = CComplexObject(
    "LOCATABLE",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "name",
            INT_REQUIRED,
            children=[required_dv_text]
        ),
        CSingleAttribute(
            "archetype_node_id",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "uid",
            INT_OPTIONAL,
            children=SUBCLASS_UID_BASED_ID
        ),
        CMultipleAttribute(
            "links",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST,
            children=[many_links]
        ),
        CSingleAttribute(
            "archetype_details",
            INT_OPTIONAL,
            children=[ARCHETYPED]
        ),
        CSingleAttribute(
            "feeder_audit",
            INT_OPTIONAL,
            # TODO: implement FEEDER_AUDIT and pals
            children=[CComplexObject("FEEDER_AUDIT", INT_OPTIONAL, "")]
        )
    ]
)

# RM.COMMON.GENERIC
ABSTRACT_PARTY_PROXY = CComplexObject(
    "PARTY_PROXY",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "external_ref",
            INT_OPTIONAL,
            children=[PARTY_REF]
        )
    ]
)

PARTY_SELF = deepcopy(ABSTRACT_PARTY_PROXY)
PARTY_SELF.rm_type_name = "PARTY_SELF"

many_dv_identifiers = deepcopy(DV_IDENTIFIER)
many_dv_identifiers.occurrences = INT_ZERO_TO_MANY
PARTY_IDENTIFIED = deepcopy(ABSTRACT_PARTY_PROXY)
PARTY_IDENTIFIED.rm_type_name = "PARTY_IDENTIFIED"
PARTY_IDENTIFIED.attributes.append(
    CSingleAttribute(
        "name",
        INT_OPTIONAL,
        children=[CPO_ANY_STRING]
    ))
PARTY_IDENTIFIED.attributes.append(
    CMultipleAttribute(
        "identifiers",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_dv_identifiers]
    )
)

required_dv_coded_text = deepcopy(DV_CODED_TEXT)
required_dv_coded_text.occurrences = INT_REQUIRED
PARTY_RELATED = deepcopy(PARTY_IDENTIFIED)
PARTY_RELATED.rm_type_name = "PARTY_IDENTIFIED"
PARTY_RELATED.attributes.append(
    CSingleAttribute(
        "relationship",
        INT_REQUIRED,
        children=[required_dv_coded_text]
    )
)

SUBCLASS_PARTY_PROXY = [PARTY_SELF, PARTY_IDENTIFIED, PARTY_RELATED]

# RM.DATA_STRUCTURES

# RM.DATA_STRUCTURES.REPRESENTATION
ELEMENT = deepcopy(LOCATABLE)
ELEMENT.attributes.append(
    CSingleAttribute(
        "value",
        INT_OPTIONAL,
        children=SUBCLASS_DATA_VALUE
    )
)
ELEMENT.attributes.append(
    CSingleAttribute(
        "null_flavour",
        INT_OPTIONAL,
        children=[DV_CODED_TEXT]
    )
)
ELEMENT.attributes.append(
    CSingleAttribute(
        "null_reason",
        INT_OPTIONAL,
        children=[DV_TEXT]
    )
)

many_elements = deepcopy(ELEMENT)
many_elements.occurrences = INT_ZERO_TO_MANY
CLUSTER = deepcopy(LOCATABLE)
CLUSTER.attributes.append(
    CMultipleAttribute(
        "items",
        INT_REQUIRED,
        CARD_ZERO_TO_MANY_LIST,
        children=[
            many_elements,
            CComplexObject(
                "CLUSTER",
                INT_ZERO_TO_MANY,
                ""
            )
        ]
    )
)

SUBCLASS_ITEM = [CLUSTER, ELEMENT]

ABSTRACT_CONTENT_ITEM = deepcopy(LOCATABLE)
ABSTRACT_CONTENT_ITEM.rm_type_name = "LOCATABLE"

# TODO: finish these (currently just basic as can be)
ABSTRACT_ENTRY = deepcopy(ABSTRACT_CONTENT_ITEM)
ABSTRACT_ENTRY.rm_type_name = "ENTRY"

ADMIN_ENTRY = deepcopy(ABSTRACT_ENTRY)
ADMIN_ENTRY.rm_type_name = "ADMIN_ENTRY"

ABSTRACT_CARE_ENTRY = deepcopy(ABSTRACT_ENTRY)
ABSTRACT_CARE_ENTRY.rm_type_name = "CARE_ENTRY"

OBSERVATION = deepcopy(ABSTRACT_CARE_ENTRY)
OBSERVATION.rm_type_name = "OBSERVATION"

EVALUATION = deepcopy(ABSTRACT_CARE_ENTRY)
EVALUATION.rm_type_name = "EVALUATION"

INSTRUCTION = deepcopy(ABSTRACT_CARE_ENTRY)
INSTRUCTION.rm_type_name = "INSTRUCTION"

ACTION = deepcopy(ABSTRACT_CARE_ENTRY)
ACTION.rm_type_name = "ACTION"

SUBCLASS_CONTENT_ITEM = [ADMIN_ENTRY, OBSERVATION, EVALUATION, INSTRUCTION, ACTION]


# RM.COMPOSITION
COMPOSITION = CComplexObject(
    "COMPOSITION",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "language",
            INT_REQUIRED,
            children=[required_code_phrase]
        ),
        CSingleAttribute(
            "territory",
            INT_REQUIRED,
            children=[required_code_phrase]
        ),
        CSingleAttribute(
            "category",
            INT_REQUIRED,
            children=[required_dv_coded_text]
        ),
        CSingleAttribute(
            "context",
            INT_OPTIONAL,
            # TODO: implement CONTEXT
            children=[CComplexObject("EVENT_CONTEXT", INT_OPTIONAL, "")]
        ),
        CSingleAttribute(
            "composer",
            INT_REQUIRED,
            children=SUBCLASS_PARTY_PROXY
        ),
        CMultipleAttribute(
            "content",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST,
            children=SUBCLASS_CONTENT_ITEM
        )
    ]
)


OPENEHR_TYPE_TO_PROTOTYPE_MAP = {
    # BASE
    "HIER_OBJECT_ID": HIER_OBJECT_ID,
    "VERSION_TREE_ID": VERSION_TREE_ID,
    "OBJECT_VERSION_ID": OBJECT_VERSION_ID,
    "ARCHETYPE_ID": ARCHETYPE_ID,
    "TEMPLATE_ID": TEMPLATE_ID,
    "TERMINOLOGY_ID": TERMINOLOGY_ID,
    "GENERIC_ID": GENERIC_ID,
    "OBJECT_REF": OBJECT_REF,
    "PARTY_REF": PARTY_REF,
    "LOCATABLE_REF": LOCATABLE_REF,
    # DATA_TYPES
    "DV_BOOLEAN": DV_BOOLEAN,
    "DV_IDENTIFIER": DV_IDENTIFIER,
    "DV_URI": DV_URI,
    "CODE_PHRASE": CODE_PHRASE,
    "TERM_MAPPING": TERM_MAPPING,
    "DV_TEXT": DV_TEXT,
    "DV_CODED_TEXT": DV_CODED_TEXT,
    # COMMON
    "LINK": LINK,
    "ARCHETYPED": ARCHETYPED,
    "LOCATABLE": LOCATABLE,
    "PARTY_SELF": PARTY_SELF,
    "PARTY_IDENTIFIED": PARTY_IDENTIFIED,
    "PARTY_RELATED": PARTY_RELATED,
    # DATA_STRUCTURES
    "ELEMENT": ELEMENT,
    "CLUSTER": CLUSTER,
    # COMPOSITION
    "COMPOSITION": COMPOSITION
}