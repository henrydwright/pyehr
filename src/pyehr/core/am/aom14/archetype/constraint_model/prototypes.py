"""This file contains base constraint models for RM types"""

from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CPrimitiveObject, CSingleAttribute
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CBoolean, CDate, CDateTime, CDuration, CInteger, CReal, CString, CTime
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.base.foundation_types.interval import MultiplicityInterval, Cardinality
from pyehr.core.rm.data_types.text import DVText

from numpy import int32
from copy import deepcopy

INT_ZERO_TO_MANY = MultiplicityInterval(int32(0))
INT_ONE_TO_MANY = MultiplicityInterval(int32(1))
INT_OPTIONAL = MultiplicityInterval(int32(0), int32(0))
INT_REQUIRED = MultiplicityInterval(int32(1), int32(1))

CARD_ZERO_TO_MANY_LIST = Cardinality(True, False, INT_ZERO_TO_MANY)
CARD_ONE_TO_MANY_LIST = Cardinality(True, False, INT_ONE_TO_MANY)

CPO_ANY_STRING = CPrimitiveObject(
                    "STRING",
                    MultiplicityInterval(int32(1), int32(1)),
                    "",
                    item=CString(pattern=r".*")
                )
optional_string = deepcopy(CPO_ANY_STRING)
optional_string.occurrences = INT_OPTIONAL

CPO_ANY_INTEGER = CPrimitiveObject(
    "INTEGER",
    INT_REQUIRED,
    "",
    item=CInteger()
)
optional_integer = deepcopy(CPO_ANY_INTEGER)
optional_integer.occurrences = INT_OPTIONAL

CPO_ANY_REAL = CPrimitiveObject(
    "REAL",
    INT_REQUIRED,
    "",
    item=CReal()
)
optional_real = deepcopy(CPO_ANY_REAL)
optional_real.occurrences = INT_OPTIONAL

CPO_ANY_TIME = CPrimitiveObject(
    "TIME",
    INT_REQUIRED,
    "",
    item=CTime()
)
optional_time = deepcopy(CPO_ANY_TIME)
optional_time.occurrences = INT_OPTIONAL

CPO_ANY_DATE = CPrimitiveObject(
    "DATE",
    INT_REQUIRED,
    "",
    item=CDate()
)
optional_date = deepcopy(CPO_ANY_DATE)
optional_date.occurrences = INT_OPTIONAL

CPO_ANY_DATE_TIME = CPrimitiveObject(
    "DATE_TIME",
    INT_REQUIRED,
    "",
    item=CDateTime()
)
optional_date_time = deepcopy(CPO_ANY_DATE_TIME)
optional_date_time.occurrences = INT_OPTIONAL

CPO_ANY_BOOLEAN = CPrimitiveObject(
    "BOOLEAN",
    INT_REQUIRED,
    "",
    item=CBoolean(True, True)
)
optional_boolean = deepcopy(CPO_ANY_BOOLEAN)
optional_boolean.occurrences = INT_OPTIONAL

CPO_ANY_DURATION = CPrimitiveObject(
    "DURATION",
    INT_REQUIRED,
    "",
    item=CDuration()
)
optional_duration = deepcopy(CPO_ANY_DURATION)
optional_duration.occurrences = INT_OPTIONAL

SUBCLASS_ORDERED = [optional_date, optional_date_time, optional_time, optional_real, optional_integer, optional_string]

# BASE

# BASE.FOUNDATION_TYPES

INTERVAL = CComplexObject(
    "INTERVAL",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "lower_unbounded",
            INT_REQUIRED,
            children=[CPO_ANY_BOOLEAN]
        ),
        CSingleAttribute(
            "upper_unbounded",
            INT_REQUIRED,
            children=[CPO_ANY_BOOLEAN]
        ),
        CSingleAttribute(
            "lower_included",
            INT_REQUIRED,
            children=[CPO_ANY_BOOLEAN]
        ),
        CSingleAttribute(
            "upper_included",
            INT_REQUIRED,
            children=[CPO_ANY_BOOLEAN]
        ),
        CSingleAttribute(
            "lower",
            INT_OPTIONAL,
            children=SUBCLASS_ORDERED
        ),
        CSingleAttribute(
            "upper",
            INT_OPTIONAL,
            children=SUBCLASS_ORDERED
        )
    ]
)

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

ABSTRACT_UID = CComplexObject(
    "UID",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        )
    ]
)

ISO_OID = deepcopy(ABSTRACT_UID)
ISO_OID.rm_type_name = "ISO_OID"
ISO_OID.attributes[0].children[0] = CPrimitiveObject(
    "STRING",
    INT_REQUIRED,
    "",
    item=CString(pattern="^([0-2])((\\.0)|(\\.[1-9][0-9]*))*$")
)

UUID = deepcopy(ABSTRACT_UID)
UUID.rm_type_name = "UUID"
UUID.attributes[0].children[0] = CPrimitiveObject(
    "STRING",
    INT_REQUIRED,
    "",
    item=CString(pattern="^(?:(?:[0-9a-fA-F]){8}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){12})$")
)

INTERNET_ID = deepcopy(ABSTRACT_UID)
INTERNET_ID.rm_type_name = "INTERNET_ID"
INTERNET_ID.attributes[0].children[0] = CPrimitiveObject(
    "STRING",
    INT_REQUIRED,
    "",
    item=CString(pattern="^(?=.{1,253})(?!.*--.*)((?:(?!-)(?![0-9])[a-zA-Z0-9-]{1,63}(?<!-)\\.){1,}(?:(?!-)[a-zA-Z0-9-]{1,63}(?<!-)))")
)

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

many_dv_texts = deepcopy(DV_TEXT)
many_dv_texts.occurrences = INT_ZERO_TO_MANY

DV_PARAGRAPH = CComplexObject(
    "DV_PARAGRAPH",
    INT_OPTIONAL,
    "",
    attributes=[
        CMultipleAttribute(
            "items",
            INT_REQUIRED,
            CARD_ONE_TO_MANY_LIST,
            children=[
                many_dv_texts
            ]
        )
    ]
)

required_dv_coded_text = deepcopy(DV_CODED_TEXT)
required_dv_coded_text.occurrences = INT_REQUIRED
DV_STATE = CComplexObject(
    "DV_STATE",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[required_dv_coded_text]
        ),
        CSingleAttribute(
            "is_terminal",
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

# RM.DATA_TYPES.QUANTITY
DV_INTERVAL = deepcopy(INTERVAL)
DV_INTERVAL.rm_type_name = "DV_INTERVAL"

required_dv_text = deepcopy(DV_TEXT)
required_dv_text.occurrences = INT_REQUIRED

required_dv_interval = deepcopy(DV_INTERVAL)
required_dv_interval.occurrences = INT_REQUIRED

REFERENCE_RANGE = CComplexObject(
    "REFERENCE_RANGE",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "meaning",
            INT_REQUIRED,
            children=[required_dv_text]
        ),
        CSingleAttribute(
            "range",
            INT_REQUIRED,
            children=[required_dv_interval]
        )
    ]
)

many_reference_ranges = deepcopy(REFERENCE_RANGE)
many_reference_ranges.occurrences = INT_ZERO_TO_MANY

ABSTRACT_DV_ORDERED = CComplexObject(
    "DV_ORDERED",
    INT_OPTIONAL,
    "",
    attributes=[
        # removed from here as redefined in descendants
        # CSingleAttribute(
        #     "value",
        #     INT_REQUIRED,
        #     children=SUBCLASS_ORDERED
        # ),
        CSingleAttribute(
            "normal_status",
            INT_OPTIONAL,
            children=[CODE_PHRASE]
        ),
        CSingleAttribute(
            "normal_range",
            INT_OPTIONAL,
            children=[DV_INTERVAL]
        ),
        CMultipleAttribute(
            "other_reference_ranges",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST,
            children=[many_reference_ranges]
        )
    ]
)

DV_ORDINAL = deepcopy(ABSTRACT_DV_ORDERED)
DV_ORDINAL.rm_type_name = "DV_ORDINAL"
DV_ORDINAL.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[optional_integer, optional_real]
    )
)
DV_ORDINAL.attributes.append(
    CSingleAttribute(
        "symbol",
        INT_REQUIRED,
        children=[required_dv_coded_text]
    )
)

DV_SCALE = deepcopy(DV_ORDINAL) # not the inheritence path but a shortcut...
DV_SCALE.rm_type_name = "DV_SCALE"

ABSTRACT_DV_QUANTIFIED = deepcopy(ABSTRACT_DV_ORDERED)
ABSTRACT_DV_QUANTIFIED.attributes.append(
    CSingleAttribute(
        "magnitude_status",
        INT_OPTIONAL,
        children=[
            CPrimitiveObject(
                "STRING",
                INT_OPTIONAL,
                "",
                item=CString(list_open=False, list_var=["=", "<", ">", "<=", ">=", "~"])
            )
        ]
    ))

# accuracy re-defined in descendants


ABSTRACT_DV_AMOUNT = deepcopy(ABSTRACT_DV_QUANTIFIED)
ABSTRACT_DV_AMOUNT.rm_type_name = "DV_AMOUNT"
ABSTRACT_DV_AMOUNT.attributes.append(
    CSingleAttribute(
        "accuracy",
        INT_OPTIONAL,
        children=[
            optional_real
        ]
    )
)

ABSTRACT_DV_AMOUNT.attributes.append(
    CSingleAttribute(
        "accuracy_is_percent",
        INT_OPTIONAL,
        children=[
            optional_boolean
        ]
    )
)

DV_QUANTITY = deepcopy(ABSTRACT_DV_AMOUNT)
DV_QUANTITY.rm_type_name = "DV_QUANTITY"
DV_QUANTITY.attributes.append(
    CSingleAttribute(
        "magnitude",
        INT_REQUIRED,
        children=[CPO_ANY_REAL]
    )
)
DV_QUANTITY.attributes.append(
    CSingleAttribute(
        "precision",
        INT_OPTIONAL,
        children=[optional_integer]
    )
)
DV_QUANTITY.attributes.append(
    CSingleAttribute(
        "units",
        INT_REQUIRED,
        children=[CPO_ANY_STRING]
    )
)
DV_QUANTITY.attributes.append(
    CSingleAttribute(
        "units_system",
        INT_OPTIONAL,
        children=[optional_string]
    )
)
DV_QUANTITY.attributes.append(
    CSingleAttribute(
        "units_display_name",
        INT_OPTIONAL,
        children=[optional_string]
    )
)

DV_COUNT = deepcopy(ABSTRACT_DV_AMOUNT)
DV_COUNT.rm_type_name = "DV_COUNT"
DV_COUNT.attributes.append(
    CSingleAttribute(
        "magnitude",
        INT_REQUIRED,
        children=[CPO_ANY_INTEGER]
    )
)

DV_PROPORTION = deepcopy(ABSTRACT_DV_AMOUNT)
DV_PROPORTION.rm_type_name = "DV_PROPORTION"
DV_PROPORTION.attributes.append(
    CSingleAttribute(
        "numerator",
        INT_REQUIRED,
        children=[CPO_ANY_REAL]
    )
)
DV_PROPORTION.attributes.append(
    CSingleAttribute(
        "denominator",
        INT_REQUIRED,
        children=[CPO_ANY_REAL]
    )
)
DV_PROPORTION.attributes.append(
    CSingleAttribute(
        "type",
        INT_REQUIRED,
        children=[
            CPrimitiveObject(
                "INTEGER",
                INT_REQUIRED,
                "",
                item=CInteger(list_var=[0, 1, 2, 3, 4])
            )
        ]
    )
)
DV_PROPORTION.attributes.append(
    CSingleAttribute(
        "precision",
        INT_OPTIONAL,
        children=[optional_integer]
    )
)

DV_DURATION = deepcopy(ABSTRACT_DV_AMOUNT)
DV_DURATION.rm_type_name = "DV_DURATION"
DV_DURATION.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[
            CPO_ANY_DURATION
        ]
    )
)

SUBCLASS_DV_AMOUNT = [DV_QUANTITY, DV_COUNT, DV_PROPORTION, DV_DURATION]

ABSTRACT_DV_ABSOLUTE_QUANTITY = deepcopy(ABSTRACT_DV_QUANTIFIED)
ABSTRACT_DV_ABSOLUTE_QUANTITY.rm_type_name = "DV_ABSOLUTE_QUANTITY"
ABSTRACT_DV_ABSOLUTE_QUANTITY.attributes.append(
    CSingleAttribute(
        "accuracy",
        INT_OPTIONAL,
        children=SUBCLASS_DV_AMOUNT
    )
)

ABSTRACT_DV_TEMPORAL = deepcopy(ABSTRACT_DV_ABSOLUTE_QUANTITY)
ABSTRACT_DV_TEMPORAL.rm_type_name = "DV_TEMPORAL"
ABSTRACT_DV_TEMPORAL.attributes[-1] = CSingleAttribute(
    "accuracy",
    INT_OPTIONAL,
    children=[optional_duration]
)

DV_DATE = deepcopy(ABSTRACT_DV_TEMPORAL)
DV_DATE.rm_type_name = "DV_DATE"
DV_DATE.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[CPO_ANY_DATE]
    )
)

DV_TIME = deepcopy(ABSTRACT_DV_TEMPORAL)
DV_TIME.rm_type_name = "DV_TIME"
DV_TIME.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[CPO_ANY_TIME]
    )
)

DV_DATE_TIME = deepcopy(ABSTRACT_DV_TEMPORAL)
DV_DATE_TIME.rm_type_name = "DV_DATE_TIME"
DV_DATE_TIME.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[CPO_ANY_DATE_TIME]
    )
)

SUBCLASS_DV_ORDERED = [DV_ORDINAL, DV_SCALE, DV_QUANTITY, DV_COUNT, DV_PROPORTION, DV_DURATION, DV_DATE, DV_TIME, DV_DATE_TIME]

DV_INTERVAL.attributes[-1].children = SUBCLASS_DV_ORDERED
DV_INTERVAL.attributes[-2].children = SUBCLASS_DV_ORDERED

# RM.DATA_TYPES.ENCAPSULATED
ABSTRACT_DV_ENCAPSULATED = CComplexObject(
    "DV_ENCAPSULATED",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "charset",
            INT_OPTIONAL,
            children=[CODE_PHRASE]
        ),
        CSingleAttribute(
            "language",
            INT_OPTIONAL,
            children=[CODE_PHRASE]
        )
    ]
)

DV_MULTIMEDIA = deepcopy(ABSTRACT_DV_ENCAPSULATED)
DV_MULTIMEDIA.rm_type_name = "DV_MULTIMEDIA"
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "alternate_text",
        INT_OPTIONAL,
        children=[CPO_ANY_STRING]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "uri",
        INT_OPTIONAL,
        children=[DV_URI]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "data",
        INT_OPTIONAL,
        children=[CPO_ANY_STRING]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "media_type",
        INT_REQUIRED,
        children=[required_code_phrase]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "compression_algorithm",
        INT_OPTIONAL,
        children=[CODE_PHRASE]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "integrity_check",
        INT_OPTIONAL,
        children=[CPO_ANY_STRING]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "integrity_check_algorithm",
        INT_OPTIONAL,
        children=[CODE_PHRASE]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "thumbnail",
        INT_OPTIONAL,
        children=[
            CComplexObject(
                "DV_MULTIMEDIA",
                INT_OPTIONAL,
                ""
            )
        ]
    )
)
DV_MULTIMEDIA.attributes.append(
    CSingleAttribute(
        "size",
        INT_REQUIRED,
        children=[CPO_ANY_INTEGER]
    )
)

DV_PARSABLE = deepcopy(ABSTRACT_DV_ENCAPSULATED)
DV_PARSABLE.rm_type_name = "DV_PARSABLE"
DV_PARSABLE.attributes.append(
    CSingleAttribute(
        "value",
        INT_REQUIRED,
        children=[CPO_ANY_STRING]
    )
)
DV_PARSABLE.attributes.append(
    CSingleAttribute(
        "formalism",
        INT_REQUIRED,
        children=[CPO_ANY_STRING]
    )
)

# RM.DATA_TYPES.TIME_SPECIFICATION
required_dv_parsable = deepcopy(DV_PARSABLE)
required_dv_parsable.occurrences = INT_REQUIRED

ABSTRACT_DV_TIME_SPECIFICATION = CComplexObject(
    "DV_TIME_SPECIFICATION",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "value",
            INT_REQUIRED,
            children=[required_dv_parsable]
        )
    ]
)

DV_PERIODIC_TIME_SPECIFICATION = deepcopy(ABSTRACT_DV_TIME_SPECIFICATION)
DV_PERIODIC_TIME_SPECIFICATION.rm_type_name = "DV_PERIODIC_TIME_SPECIFICATION"

DV_GENERAL_TIME_SPECIFICATION = deepcopy(ABSTRACT_DV_TIME_SPECIFICATION)
DV_GENERAL_TIME_SPECIFICATION.rm_type_name = "DV_GENERAL_TIME_SPECIFICATION"

SUBCLASS_DATA_VALUE = [DV_URI, DV_EHR_URI, DV_TEXT, DV_CODED_TEXT, DV_IDENTIFIER]

# RM.COMMON

# RM.COMMON.ARCHETYPED
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

PARTICIPATION = CComplexObject(
    "PARTICIPATION",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "function",
            INT_REQUIRED,
            children=[required_dv_text]
        ),
        CSingleAttribute(
            "mode",
            INT_OPTIONAL,
            children=[DV_CODED_TEXT]
        ),
        CSingleAttribute(
            "performer",
            INT_REQUIRED,
            children=SUBCLASS_PARTY_PROXY
        ),
        CSingleAttribute(
            "time",
            INT_OPTIONAL,
            children=[DV_INTERVAL]
        )
    ]
)
PARTICIPATION.attributes[-1].children[0].attributes[-1].children = [DV_DATE_TIME] # upper
PARTICIPATION.attributes[-1].children[0].attributes[-2].children = [DV_DATE_TIME] # lower

many_participations = deepcopy(PARTICIPATION)
many_participations.occurrences = INT_ZERO_TO_MANY

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

# RM.DATA_STRUCTURES.ITEM_STRUCTURE
required_element = deepcopy(ELEMENT)
required_element.occurrences = INT_REQUIRED
ITEM_SINGLE = deepcopy(LOCATABLE)
ITEM_SINGLE.attributes.append(
    CSingleAttribute(
        "item",
        INT_REQUIRED,
        children=[required_element]
    )
)

many_elements = deepcopy(ELEMENT)
many_elements.occurrences = INT_ZERO_TO_MANY
ITEM_LIST = deepcopy(LOCATABLE)
ITEM_LIST.attributes.append(
    CMultipleAttribute(
        "items",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_elements]
    )
)

many_clusters = deepcopy(CLUSTER)
many_clusters.occurrences = INT_ZERO_TO_MANY
ITEM_TABLE = deepcopy(LOCATABLE)
ITEM_TABLE.attributes.append(
    CMultipleAttribute(
        "rows",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_clusters]
    )
)

ITEM_TREE = deepcopy(LOCATABLE)
ITEM_TREE.attributes.append(
    CMultipleAttribute(
        "items",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_elements, many_clusters]
    )
)

SUBCLASS_ITEM_STRUCTURE = [ITEM_SINGLE, ITEM_LIST, ITEM_TABLE, ITEM_TREE]

# RM.DATA_STRUCTURES.HISTORY
required_dv_date_time = deepcopy(DV_DATE_TIME)
required_dv_date_time.occurrences = INT_REQUIRED

ABSTRACT_EVENT = deepcopy(LOCATABLE)
ABSTRACT_EVENT.rm_type_name = "EVENT"
ABSTRACT_EVENT.attributes.append(
    CSingleAttribute(
        "time",
        INT_REQUIRED,
        children=[required_dv_date_time]
    ))
ABSTRACT_EVENT.attributes.append(
    CSingleAttribute(
        "state",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    ))
ABSTRACT_EVENT.attributes.append(
    CSingleAttribute(
        "data",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

POINT_EVENT = deepcopy(ABSTRACT_EVENT)
POINT_EVENT.rm_type_name = "POINT_EVENT"


required_dv_duration = deepcopy(DV_DURATION)
required_dv_duration.occurrences = INT_REQUIRED

INTERVAL_EVENT = deepcopy(ABSTRACT_EVENT)
INTERVAL_EVENT.rm_type_name = "INTERVAL_EVENT"
INTERVAL_EVENT.attributes.append(
    CSingleAttribute(
        "width",
        INT_REQUIRED,
        children=[required_dv_duration]
    ))
INTERVAL_EVENT.attributes.append(
    CSingleAttribute(
        "sample_count",
        INT_OPTIONAL,
        children=[optional_integer]
    ))
INTERVAL_EVENT.attributes.append(
    CSingleAttribute(
        "math_function",
        INT_REQUIRED,
        children=[required_dv_coded_text]
    )
)

SUBCLASS_EVENT = [POINT_EVENT, INTERVAL_EVENT]

HISTORY = deepcopy(LOCATABLE)
HISTORY.rm_type_name = "HISTORY"
HISTORY.attributes.append(
    CSingleAttribute(
        "origin",
        INT_REQUIRED,
        children=[required_dv_date_time]
    ))
HISTORY.attributes.append(
    CSingleAttribute(
        "period",
        INT_OPTIONAL,
        children=[DV_DURATION]
    ))
HISTORY.attributes.append(
    CSingleAttribute(
        "duration",
        INT_OPTIONAL,
        children=[DV_DURATION]
    ))
HISTORY.attributes.append(
    CSingleAttribute(
        "summary",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    ))
HISTORY.attributes.append(
    CMultipleAttribute(
        "events",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=SUBCLASS_EVENT
    )
)

# RM.COMPOSITION.CONTENT.ENTRY

ABSTRACT_CONTENT_ITEM = deepcopy(LOCATABLE)
ABSTRACT_CONTENT_ITEM.rm_type_name = "CONTENT_ITEM"

ABSTRACT_ENTRY = deepcopy(ABSTRACT_CONTENT_ITEM)
ABSTRACT_ENTRY.rm_type_name = "ENTRY"
ABSTRACT_ENTRY.attributes.append(
    CSingleAttribute(
        "language",
        INT_REQUIRED,
        children=[required_code_phrase]
    ))
ABSTRACT_ENTRY.attributes.append(
    CSingleAttribute(
        "encoding",
        INT_REQUIRED,
        children=[required_code_phrase]
    ))
ABSTRACT_ENTRY.attributes.append(
    CMultipleAttribute(
        "other_participations",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST
    ))
ABSTRACT_ENTRY.attributes.append(
    CSingleAttribute(
        "workflow_id",
        INT_OPTIONAL,
        children=[OBJECT_REF]
    ))
ABSTRACT_ENTRY.attributes.append(
    CSingleAttribute(
        "subject",
        INT_REQUIRED,
        children=SUBCLASS_PARTY_PROXY
    ))
ABSTRACT_ENTRY.attributes.append(
    CSingleAttribute(
        "provider",
        INT_OPTIONAL,
        children=SUBCLASS_PARTY_PROXY
    )
)

ADMIN_ENTRY = deepcopy(ABSTRACT_ENTRY)
ADMIN_ENTRY.rm_type_name = "ADMIN_ENTRY"
ADMIN_ENTRY.attributes.append(
    CSingleAttribute(
        "data",
        INT_REQUIRED,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

ABSTRACT_CARE_ENTRY = deepcopy(ABSTRACT_ENTRY)
ABSTRACT_CARE_ENTRY.rm_type_name = "CARE_ENTRY"
ABSTRACT_CARE_ENTRY.attributes.append(
    CSingleAttribute(
        "protocol",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    ))
ABSTRACT_CARE_ENTRY.attributes.append(
    CSingleAttribute(
        "guideline_id",
        INT_OPTIONAL,
        children=[OBJECT_REF]
    )
)

required_history = deepcopy(HISTORY)
required_history.occurrences = INT_REQUIRED

OBSERVATION = deepcopy(ABSTRACT_CARE_ENTRY)
OBSERVATION.rm_type_name = "OBSERVATION"
OBSERVATION.attributes.append(
    CSingleAttribute(
        "data",
        INT_REQUIRED,
        children=[required_history]
    )
)
OBSERVATION.attributes.append(
    CSingleAttribute(
        "state",
        INT_OPTIONAL,
        children=[HISTORY]
    )
)

EVALUATION = deepcopy(ABSTRACT_CARE_ENTRY)
EVALUATION.rm_type_name = "EVALUATION"
EVALUATION.attributes.append(
    CSingleAttribute(
        "data",
        INT_REQUIRED,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

ACTIVITY = deepcopy(LOCATABLE)
ACTIVITY.rm_type_name = "ACTIVITY"
ACTIVITY.attributes.append(
    CSingleAttribute(
        "timing",
        INT_OPTIONAL,
        children=[DV_PARSABLE]
    )
)
ACTIVITY.attributes.append(
    CSingleAttribute(
        "action_archetype_id",
        INT_REQUIRED,
        children=[CPO_ANY_STRING]
    )
)
ACTIVITY.attributes.append(
    CSingleAttribute(
        "description",
        INT_REQUIRED,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

many_activities = deepcopy(ACTIVITY)
many_activities.occurrences = INT_ZERO_TO_MANY

INSTRUCTION = deepcopy(ABSTRACT_CARE_ENTRY)
INSTRUCTION.rm_type_name = "INSTRUCTION"
INSTRUCTION.attributes.append(
    CSingleAttribute(
        "narrative",
        INT_REQUIRED,
        children=[required_dv_text]
    )
)
INSTRUCTION.attributes.append(
    CSingleAttribute(
        "expiry_time",
        INT_OPTIONAL,
        children=[DV_DATE_TIME]
    )
)
INSTRUCTION.attributes.append(
    CSingleAttribute(
        "wf_definition",
        INT_OPTIONAL,
        children=[DV_PARSABLE]
    )
)
INSTRUCTION.attributes.append(
    CMultipleAttribute(
        "activities",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_activities]
    )
)

required_locatable_ref = deepcopy(LOCATABLE_REF)
required_locatable_ref.occurrences = INT_REQUIRED

INSTRUCTION_DETAILS = CComplexObject(
    "INSTRUCTION_DETAILS",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "instruction_id",
            INT_REQUIRED,
            children=[required_locatable_ref]
        ),
        CSingleAttribute(
            "activity_id",
            INT_REQUIRED,
            children=[CPO_ANY_STRING]
        ),
        CSingleAttribute(
            "wf_details",
            INT_OPTIONAL,
            children=SUBCLASS_ITEM_STRUCTURE
        )
    ]
)

ISM_TRANSITION = CComplexObject(
    "ISM_TRANSITION",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "current_state",
            INT_REQUIRED,
            children=[required_dv_coded_text]
        ),
        CSingleAttribute(
            "transition",
            INT_OPTIONAL,
            children=[DV_CODED_TEXT]
        ),
        CSingleAttribute(
            "careflow_step",
            INT_OPTIONAL,
            children=[DV_CODED_TEXT]
        ),
        CMultipleAttribute(
            "reason",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST,
            children=[many_dv_texts]
        )
    ]
)

required_ism_transition = deepcopy(ISM_TRANSITION)
required_ism_transition.occurrences = INT_REQUIRED

ACTION = deepcopy(ABSTRACT_CARE_ENTRY)
ACTION.rm_type_name = "ACTION"
ACTION.attributes.append(
    CSingleAttribute(
        "time",
        INT_REQUIRED,
        children=[required_dv_date_time]
    ))
ACTION.attributes.append(
    CSingleAttribute(
        "ism_transition",
        INT_REQUIRED,
        children=[required_ism_transition]
    ))
ACTION.attributes.append(
    CSingleAttribute(
        "instruction_details",
        INT_OPTIONAL,
        children=[INSTRUCTION_DETAILS]
    ))
ACTION.attributes.append(
    CSingleAttribute(
        "description",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

SUBCLASS_CONTENT_ITEM = [ADMIN_ENTRY, OBSERVATION, EVALUATION, INSTRUCTION, ACTION]

SECTION = deepcopy(LOCATABLE)
SECTION.rm_type_name = "SECTION"
SECTION.attributes.append(
    CMultipleAttribute(
        "items",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=SUBCLASS_CONTENT_ITEM
    )
)

SUBCLASS_CONTENT_ITEM.append(SECTION)



# RM.COMPOSITION

EVENT_CONTEXT = CComplexObject(
    "EVENT_CONTEXT",
    INT_OPTIONAL,
    "",
    attributes=[
        CSingleAttribute(
            "start_time",
            INT_REQUIRED,
            children=[required_dv_date_time]
        ),
        CSingleAttribute(
            "end_time",
            INT_REQUIRED,
            children=[required_dv_date_time]
        ),
        CSingleAttribute(
            "location",
            INT_OPTIONAL,
            children=[optional_string]
        ),
        CSingleAttribute(
            "setting",
            INT_REQUIRED,
            children=[required_dv_coded_text]
        ),
        CSingleAttribute(
            "other_context",
            INT_OPTIONAL,
            children=SUBCLASS_ITEM_STRUCTURE
        ),
        CSingleAttribute(
            "health_care_facility",
            INT_OPTIONAL,
            children=[PARTY_IDENTIFIED]
        ),
        CMultipleAttribute(
            "participations",
            INT_OPTIONAL,
            CARD_ZERO_TO_MANY_LIST,
            children=[many_participations]
        )
    ]
)

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
            children=[EVENT_CONTEXT]
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

# DEMOGRAPHIC

PARTY_IDENTITY = deepcopy(LOCATABLE)
PARTY_IDENTITY.attributes.append(
    CSingleAttribute(
        "details",
        INT_REQUIRED,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)

ADDRESS = deepcopy(PARTY_IDENTITY) # not inheritence, but shortcut
ADDRESS.rm_type_name = "ADDRESS"

many_addresses = deepcopy(ADDRESS)
many_addresses.occurrences = INT_ZERO_TO_MANY

typebind_dv_interval_dv_date = deepcopy(DV_INTERVAL)
typebind_dv_interval_dv_date.attributes[-1].children = [DV_DATE]
typebind_dv_interval_dv_date.attributes[-2].children = [DV_DATE]

CONTACT = deepcopy(LOCATABLE)
CONTACT.attributes.append(
    CMultipleAttribute(
        "addresses",
        INT_REQUIRED,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_addresses]
    ))
CONTACT.attributes.append(
    CSingleAttribute(
        "time_validity",
        INT_OPTIONAL,
        children=[DV_INTERVAL]
    )
)

required_party_ref = deepcopy(PARTY_REF)
required_party_ref.occurrences = INT_REQUIRED

PARTY_RELATIONSHIP = deepcopy(LOCATABLE)
PARTY_RELATIONSHIP.rm_type_name = "PARTY_RELATIONSHIP"
PARTY_RELATIONSHIP.attributes.append(
    CSingleAttribute(
        "details",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    ))
PARTY_RELATIONSHIP.attributes.append(
    CSingleAttribute(
        "target",
        INT_REQUIRED,
        children=[required_party_ref]
    ))
PARTY_RELATIONSHIP.attributes.append(
    CSingleAttribute(
        "time_validity",
        INT_OPTIONAL,
        children=[typebind_dv_interval_dv_date]
    ))
PARTY_RELATIONSHIP.attributes.append(
    CSingleAttribute(
        "source",
        INT_REQUIRED,
        children=[required_party_ref]
    )
)

many_party_identities = deepcopy(PARTY_IDENTITY)
many_party_identities.occurrences = INT_ZERO_TO_MANY

many_contacts = deepcopy(CONTACT)
many_contacts.occurrences = INT_ZERO_TO_MANY

many_locatable_refs = deepcopy(LOCATABLE_REF)
many_locatable_refs.occurrences = INT_ZERO_TO_MANY

many_party_relationships = deepcopy(PARTY_RELATIONSHIP)
many_party_relationships.occurrences = INT_ZERO_TO_MANY

ABSTRACT_PARTY = deepcopy(LOCATABLE)
ABSTRACT_PARTY.rm_type_name = "PARTY"
ABSTRACT_PARTY.attributes.append(
    CMultipleAttribute(
        "identities",
        INT_REQUIRED,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_party_identities]
    )
)
ABSTRACT_PARTY.attributes.append(
    CMultipleAttribute(
        "contacts",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_contacts]
    )
)
ABSTRACT_PARTY.attributes.append(
    CSingleAttribute(
        "details",
        INT_OPTIONAL,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)
ABSTRACT_PARTY.attributes.append(
    CMultipleAttribute(
        "reverse_relationships",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_locatable_refs]
    )
)
ABSTRACT_PARTY.attributes.append(
    CMultipleAttribute(
        "relationships",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_party_relationships]
    )
)

many_party_refs = deepcopy(PARTY_REF)
many_party_refs.occurrences = INT_ZERO_TO_MANY

ABSTRACT_ACTOR = deepcopy(ABSTRACT_PARTY)
ABSTRACT_ACTOR.rm_type_name = "ACTOR"
ABSTRACT_ACTOR.attributes.append(
    CMultipleAttribute(
        "languages",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_dv_texts]
    )
)
ABSTRACT_ACTOR.attributes.append(
    CMultipleAttribute(
        "roles",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_party_refs]
    )
)

PERSON = deepcopy(ABSTRACT_ACTOR)
PERSON.rm_type_name = "PERSON"

ORGANISATION = deepcopy(ABSTRACT_ACTOR)
ORGANISATION.rm_type_name = "ORGANISATION"

GROUP = deepcopy(ABSTRACT_ACTOR)
GROUP.rm_type_name = "GROUP"

AGENT = deepcopy(ABSTRACT_ACTOR)
AGENT.rm_type_name = "AGENT"

CAPABILITY = deepcopy(LOCATABLE)
CAPABILITY.rm_type_name = "CAPABILITY"
CAPABILITY.attributes.append(
    CSingleAttribute(
        "credentials",
        INT_REQUIRED,
        children=SUBCLASS_ITEM_STRUCTURE
    )
)
CAPABILITY.attributes.append(
    CSingleAttribute(
        "time_validity",
        INT_OPTIONAL,
        children=[typebind_dv_interval_dv_date]
    )
)

many_capabilities = deepcopy(CAPABILITY)
many_capabilities.occurrences = INT_ZERO_TO_MANY

ROLE = deepcopy(ABSTRACT_PARTY)
ROLE.rm_type_name = "ROLE"
ROLE.attributes.append(
    CSingleAttribute(
        "time_validity",
        INT_OPTIONAL,
        children=[typebind_dv_interval_dv_date]
    )
)
ROLE.attributes.append(
    CSingleAttribute(
        "performer",
        INT_REQUIRED,
        children=[required_party_ref]
    )
)
ROLE.attributes.append(
    CMultipleAttribute(
        "capabilities",
        INT_OPTIONAL,
        CARD_ZERO_TO_MANY_LIST,
        children=[many_capabilities]
    )
)

OPENEHR_TYPE_TO_PROTOTYPE_MAP = {
    # BASE
    "INTERNET_ID": INTERNET_ID,
    "OBJECT_REF": OBJECT_REF,
    "PARTY_REF": PARTY_REF,
    "TEMPLATE_ID": TEMPLATE_ID,
    "OBJECT_VERSION_ID": OBJECT_VERSION_ID,
    "VERSION_TREE_ID": VERSION_TREE_ID,
    "LOCATABLE_REF": LOCATABLE_REF,
    "GENERIC_ID": GENERIC_ID,
    "ARCHETYPE_ID": ARCHETYPE_ID,
    "HIER_OBJECT_ID": HIER_OBJECT_ID,
    "UUID": UUID,
    "ISO_OID": ISO_OID,
    "TERMINOLOGY_ID": TERMINOLOGY_ID,
    # RM : Data Types
    "DV_TEXT": DV_TEXT,
    "DV_IDENTIFIER": DV_IDENTIFIER,
    "DV_DATE": DV_DATE,
    "DV_CODED_TEXT": DV_CODED_TEXT,
    "DV_TIME": DV_TIME,
    "DV_BOOLEAN": DV_BOOLEAN,
    "CODE_PHRASE": CODE_PHRASE,
    "DV_PARSABLE": DV_PARSABLE,
    "TERM_MAPPING": TERM_MAPPING,
    "DV_EHR_URI": DV_EHR_URI,
    "DV_URI": DV_URI,
    "DV_COUNT": DV_COUNT,
    "DV_GENERAL_TIME_SPECIFICATION": DV_GENERAL_TIME_SPECIFICATION,
    "DV_MULTIMEDIA": DV_MULTIMEDIA,
    "DV_DATE_TIME": DV_DATE_TIME,
    "DV_QUANTITY": DV_QUANTITY,
    "DV_DURATION": DV_DURATION,
    "DV_INTERVAL": DV_INTERVAL,
    "DV_ORDINAL": DV_ORDINAL,
    "DV_PARAGRAPH": DV_PARAGRAPH,
    "DV_STATE": DV_STATE,
    "DV_PERIODIC_TIME_SPECIFICATION": DV_PERIODIC_TIME_SPECIFICATION,
    "DV_PROPORTION": DV_PROPORTION,
    "DV_SCALE": DV_SCALE,
    "REFERENCE_RANGE": REFERENCE_RANGE,
    # RM : Common
    "LINK": LINK,
    "ARCHETYPED": ARCHETYPED,
    "PARTY_RELATED": PARTY_RELATED,
    "LOCATABLE": LOCATABLE,
    "PARTICIPATION": PARTICIPATION,
    "PARTY_SELF": PARTY_SELF,
    "PARTY_IDENTIFIED": PARTY_IDENTIFIED,
    # RM : Data Structures
    "INTERVAL_EVENT": INTERVAL_EVENT,
    "ITEM_TABLE": ITEM_TABLE,
    "CLUSTER": CLUSTER,
    "ITEM_LIST": ITEM_LIST,
    "ITEM_TREE": ITEM_TREE,
    "HISTORY": HISTORY,
    "POINT_EVENT": POINT_EVENT,
    "ELEMENT": ELEMENT,
    "ITEM_SINGLE": ITEM_SINGLE,
    # RM : Composition
    "ISM_TRANSITION": ISM_TRANSITION,
    "INSTRUCTION": INSTRUCTION,
    "ADMIN_ENTRY": ADMIN_ENTRY,
    "ACTIVITY": ACTIVITY,
    "COMPOSITION": COMPOSITION,
    "INSTRUCTION_DETAILS": INSTRUCTION_DETAILS,
    "EVALUATION": EVALUATION,
    "EVENT_CONTEXT": EVENT_CONTEXT,
    "SECTION": SECTION,
    "OBSERVATION": OBSERVATION,
    "ACTION": ACTION,
    # RM : Demographic
    "GROUP": GROUP,
    "PARTY_IDENTITY": PARTY_IDENTITY,
    "PERSON": PERSON,
    "AGENT": AGENT,
    "ROLE": ROLE,
    "CONTACT": CONTACT,
    "ORGANISATION": ORGANISATION,
    "PARTY_RELATIONSHIP": PARTY_RELATIONSHIP,
    "ADDRESS": ADDRESS,
    "CAPABILITY": CAPABILITY
}