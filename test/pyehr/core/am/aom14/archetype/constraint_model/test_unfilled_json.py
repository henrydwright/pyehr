from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeInternalRef, CArchetypeRoot, CCodePhrase, CComplexObject, CMultipleAttribute, CPrimitiveObject, CSingleAttribute, resolve_archetype_internal_refs
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CString
from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.interval import Cardinality, MultiplicityInterval

import pytest

from numpy import int32

from pyehr.core.am.aom14.archetype.constraint_model.prototypes import CODE_PHRASE

def test_unfilled_json():
    output = {
        '_type': 'CODE_PHRASE',
        'code_string': '',
        'preferred_term': '',
        'terminology_id': {
            '_type': 'TERMINOLOGY_ID',
            'value': ''
        }
    }
    assert is_equal_value(output, CODE_PHRASE.unfilled_json())

def test_unfilled_json_optional_flag_works():
    output = {
        '_type': 'CODE_PHRASE',
        'code_string': '',
        'terminology_id': {
            '_type': 'TERMINOLOGY_ID',
            'value': ''
        }
    }
    assert is_equal_value(output, CODE_PHRASE.unfilled_json(include_optional_elements=False))

def test_unfilled_json_archetype_internal_ref_resolved():
    ref_ex = CComplexObject(
        "ITEM_TREE",
        MultiplicityInterval(int32(1), int32(1)),
        "at0000",
        attributes=[
            CMultipleAttribute(
                "items",
                MultiplicityInterval(int32(1), int32(1)),
                Cardinality(True, False, MultiplicityInterval(int32(0), int32(10))),
                children=[
                    CArchetypeRoot(
                        "CLUSTER",
                        MultiplicityInterval(int32(0)),
                        "at0000",
                        ArchetypeID("openEHR-EHR-CLUSTER.example.v0"),
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(int32(1), int32(1)),
                                Cardinality(True, False, MultiplicityInterval(int32(0))),
                                children=[
                                    CComplexObject(
                                        "ELEMENT",
                                        MultiplicityInterval(int32(0)),
                                        "at0001",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(int32(1), int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_TEXT",
                                                        MultiplicityInterval(int32(0), int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "value",
                                                                MultiplicityInterval(int32(1), int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "STRING",
                                                                        MultiplicityInterval(int32(1), int32(1)),
                                                                        "",
                                                                        item=CString(pattern="hello")
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    CComplexObject(
                                                        "DV_CODED_TEXT",
                                                        MultiplicityInterval(int32(0), int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "defining_code",
                                                                MultiplicityInterval(int32(1), int32(1)),
                                                                children=[
                                                                    CCodePhrase(
                                                                        "CODE_PHRASE",
                                                                        MultiplicityInterval(int32(1), int32(1)),
                                                                        "",
                                                                        code_list=["at0010", "at0011"]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ])
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    CComplexObject(
                        "ELEMENT",
                        MultiplicityInterval(int32(0)),
                        "at0001",
                        attributes=[
                            CSingleAttribute(
                                "value",
                                MultiplicityInterval(int32(1), int32(1)),
                                children=[
                                    ArchetypeInternalRef(
                                        "DV_CODED_TEXT",
                                        MultiplicityInterval(int32(1), int32(1)),
                                        "",
                                        target_path="items[openEHR-EHR-CLUSTER.example.v0]/items[at0001]/value[1]"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    ujson = ref_ex.unfilled_json()

    assert ujson["items"][1]["value"]["defining_code"]["code_string"] == "at0010"

    