from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeInternalRef, CArchetypeRoot, CCodePhrase, CComplexObject, CMultipleAttribute, CPrimitiveObject, CSingleAttribute, add_rm_constraints, resolve_archetype_internal_refs
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CString
from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.interval import Cardinality, MultiplicityInterval
import pytest
import json

from numpy import int32

def test_resolve_archetype_internal_refs():
    before = CComplexObject(
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

    after = resolve_archetype_internal_refs(before)

    # check that the occurences in the ARCHETYPE_INTERNAL_REF overrides the target
    assert after.attributes[0].children[1].attributes[0].children[0].occurrences.is_equal(MultiplicityInterval(int32(1), int32(1)))
    # and that the other parts are the same
    assert after.attributes[0].children[1].attributes[0].children[0].attributes[0].rm_attribute_name == "defining_code"
    assert after.attributes[0].children[1].attributes[0].children[0].attributes[0].children[0].is_equal(CCodePhrase(
                                                                            "CODE_PHRASE",
                                                                            MultiplicityInterval(int32(1), int32(1)),
                                                                            "",
                                                                            code_list=["at0010", "at0011"]
                                                                        ))


def test_add_rm_constraints():
    before = CComplexObject(
        "ELEMENT",
        MultiplicityInterval(int32(1), int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "value",
                MultiplicityInterval(int32(1), int32(1)),
                children=[
                    CComplexObject(
                        "DV_TEXT",
                        MultiplicityInterval(int32(1), int32(1)),
                        ""
                    )
                ]
            )
        ]
    )

    after = CComplexObject(
        "ELEMENT",
        MultiplicityInterval(int32(1), int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "value",
                MultiplicityInterval(int32(1), int32(1)),
                children=[
                    CComplexObject(
                        "DV_TEXT",
                        MultiplicityInterval(int32(1), int32(1)),
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
                                        item=CString(pattern=".*")
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            CSingleAttribute(
                "name",
                MultiplicityInterval(int32(1), int32(1)),
                children=[
                    CComplexObject(
                        "DV_TEXT",
                        MultiplicityInterval(int32(1), int32(1)),
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
                                        item=CString(pattern=".*")
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            CSingleAttribute(
                "archetype_node_id",
                MultiplicityInterval(int32(1), int32(1)),
                children=[
                    CPrimitiveObject(
                        "STRING",
                        MultiplicityInterval(int32(1), int32(1)),
                        "",
                        item=CString(pattern=".*")
                    )
                ]
            )
        ]
    )

    assert add_rm_constraints(before).is_equal(after)