# file dedicated to testing that the constraints_met method works in a range of circumstances

import numpy as np
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CPrimitiveObject, CSingleAttribute
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CBoolean, CInteger, CReal, CString
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID
from pyehr.core.base.foundation_types.interval import Cardinality, MultiplicityInterval, ProperInterval
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.rm.composition.content.entry import Evaluation, Instruction, Observation
from pyehr.core.rm.data_structures.history import History
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemStructure, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVBoolean
from pyehr.core.rm.data_types.quantity import DVCount
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime, DVDuration, DVTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
import pytest


@pytest.fixture()
def example_observation():
    return Observation(
        DVText("Test Observation"),
        archetype_node_id="at0000",
        language=CodePhrase("ISO_639-1", "en"),
        encoding=CodePhrase("IANA_character-sets", "UTF-8"),
        subject=PartySelf(),
        archetype_details=Archetyped(ArchetypeID("pyehr-EHR-OBSERVATION.test_example.v0"), "1.1.0"),
        data=History[ItemStructure](
            name=DVText("history"),
            archetype_node_id="at0001",
            origin=DVDateTime("2026-08-16T19:06:02Z")
        )
    )

@pytest.fixture()
def example_evaluation():
    return Evaluation(
        DVText("Test Evaluation"),
        archetype_node_id="at0000",
        language=CodePhrase("ISO_639-1", "en"),
        encoding=CodePhrase("IANA_character-sets", "UTF-8"),
        subject=PartySelf(),
        archetype_details=Archetyped(ArchetypeID("pyehr-EHR-EVALUATION.text_example.v0"), "1.1.0"),
        data=ItemTree(
            name=DVText("Thoughts and things"),
            archetype_node_id="at0001",
            items=[Element(
                name=DVText("First Thought"),
                archetype_node_id="at0002",
                value=DVText("I think, therefore, I am")
            ),
            Element(
                name=DVText("Second Thought"),
                archetype_node_id="at0002",
                value=DVText("Respice finem")
            ),
            Element(
                name=DVText("Third Thought"),
                archetype_node_id="at0002",
                value=DVText("Fides et amor")
            ),
            Element(
                name=DVText("Coded thing"),
                archetype_node_id="at0003",
                value=DVCodedText("Does not perform shopping activities (finding)", defining_code=CodePhrase("SNOMED-CT", "300722002"))
            )]
        )
    )

@pytest.fixture()
def example_instruction():
    return Instruction(
        name=DVText("Many data types to constrain"),
        archetype_node_id="at0000",
        language=CodePhrase("ISO_639-1", "en"),
        encoding=CodePhrase("IANA_character-sets", "UTF-8"),
        subject=PartySelf(),
        archetype_details=Archetyped(
            archetype_id=ArchetypeID("pyehr-EHR-INSTRUCTION.many_types.v0"),
            rm_version="1.1.0"
        ),
        narrative=DVText("Please perform an interprative dance based on the below instructions"),
        protocol=ItemTree(
            name=DVText("Inspiration"),
            archetype_node_id="at0001",
            items=[
                Cluster(
                    name=DVText("strings n' bools"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("string thing"),
                            archetype_node_id="at0003",
                            value=DVText("Bop it!")
                        ),
                        Element(
                            name=DVText("twist it?"),
                            archetype_node_id="at0004",
                            value=DVBoolean(True)
                        )
                    ]
                ),
                Element(
                    name=DVText("are we human?"),
                    archetype_node_id="at0005",
                    value=DVCodedText("Dancer (occupation)", CodePhrase("SNOMED-CT", "45050008"))
                ),
                Element(
                    name=DVText("how many hops this time?"),
                    archetype_node_id="at0006",
                    value=DVCount(np.int64(2), accuracy=np.float32(1.0), accuracy_is_percent=False)
                ),
                Element(
                    name=DVText("monster mash"),
                    archetype_node_id="at0007",
                    value=DVDate("1962-08", accuracy=DVDuration("P1M"))
                ),
                Element(
                    name=DVText("time to dance?"),
                    archetype_node_id="at0008",
                    value=DVTime("23:59:00+01:00")
                ),
                Element(
                    name=DVText("yadda"),
                    archetype_node_id="at0009",
                    value=DVDateTime("2026-08-17T21:57:23Z")
                )
            ]
        )
    )

def test_rm_type_name_check_functions(example_observation, example_evaluation):
    con = CComplexObject(
        "OBSERVATION",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "at0000"
    )
    assert con.valid_value(example_observation) == True
    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="at0000: expected rm_type_name of OBSERVATION but found EVALUATION"):
        con.valid_value(example_evaluation, raise_exceptions=True)

def test_node_id_check_functions(example_observation):
    con = CComplexObject(
            "OBSERVATION",
            MultiplicityInterval(np.int32(1), np.int32(1)),
            "at0000"
        )
    assert con.valid_value(example_observation) == True
    con.node_id = "at0001"
    assert con.valid_value(example_observation) == False
    with pytest.raises(ValueError, match="at0001: expected node_id of at0001 but found at0000"):
        con.valid_value(example_observation, raise_exceptions=True)

    # passes for a blank node_id in all cases
    con.node_id = ""
    assert con.valid_value(example_observation) == True
    con2 = CComplexObject(
        "DV_TEXT",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        ""
    )
    dvt = DVText("Hello, world!")
    assert con2.valid_value(dvt) == True

def test_occurences_constraint_applied(example_evaluation):
    con = CComplexObject(
        "EVALUATION",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "data",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "ITEM_TREE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "at0001",
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                Cardinality(True, True, MultiplicityInterval(np.int32(0))),
                                children=[
                                    CComplexObject(
                                        "ELEMENT",
                                        occurrences=MultiplicityInterval(np.int32(1), np.int32(2)),
                                        node_id="at0002"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # the above constrains something like example_evaluation but with 1 to 2 at0002s
    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/at0000/data/at0001/items/at0002: found 3 occurences of at0002 but expected \\[1\\.\\.2\\]"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[2]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[1]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/at0000/data/at0001/items/at0002: found 0 occurences of at0002 but expected \\[1\\.\\.2\\]"):
        con.valid_value(example_evaluation, raise_exceptions=True)

def test_existence_constraint_applied(example_observation):
    con = CComplexObject(
        "OBSERVATION",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "uid",
                existence=MultiplicityInterval(np.int32(1), np.int32(1))
            )
        ]
    )

    assert con.valid_value(example_observation) == False
    with pytest.raises(ValueError, match="/at0000: attribute 'uid' is mandatory \\(existence 1\\.\\.1\\) but WAS NOT provided"):
        con.valid_value(example_observation, raise_exceptions=True)

    example_observation.uid = HierObjectID("ec6b16be-7ae6-4b27-91da-710f6a458c61")
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(1))
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(0))
    assert con.valid_value(example_observation) == False

    with pytest.raises(ValueError, match="/at0000: attribute 'uid' is prohibited \\(existence 0\\.\\.0\\) but WAS provided"):
            con.valid_value(example_observation, raise_exceptions=True)

def test_cardinality_constraint_applied(example_evaluation):
    con = CComplexObject(
        "EVALUATION",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "data",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "ITEM_TREE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "at0001",
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                Cardinality(True, True, MultiplicityInterval(np.int32(1), np.int32(3)))
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # the above constrains something like example_evaluation but with 1 to 3 items in items
    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/at0000/data/at0001: found 4 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/at0000/data/at0001: found 0 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
        con.valid_value(example_evaluation, raise_exceptions=True)

def test_c_primitive_object_c_string(example_observation):
    con = CComplexObject(
        "OBSERVATION",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "at0000",
        attributes=[
            CSingleAttribute(
                "name",
                existence=MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "DV_TEXT",
                        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
                        node_id="",
                        attributes=[
                            CSingleAttribute(
                                "value",
                                existence=MultiplicityInterval(np.int32(1), np.int32(1)),
                                children=[
                                    CPrimitiveObject(
                                        rm_type_name="STRING",
                                        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
                                        node_id="",
                                        item=CString(
                                            list_var=["Test Observation"]
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert con.valid_value(example_observation) == True

    example_observation.name.value = "Invalid Value"
    assert con.valid_value(example_observation) == False
    with pytest.raises(ValueError, match="/at0000/name/value: value of 'Invalid Value' was not in the permitted list of strings"):
        con.valid_value(example_observation, raise_exceptions=True)

    con.attributes[0].children[0].attributes[0].children[0].item.list_open = True
    assert con.valid_value(example_observation) == True

    con.attributes[0].children[0].attributes[0].children[0].item = CString(pattern=r"^(abacus|wall)$")
    assert con.valid_value(example_observation) == False
    with pytest.raises(ValueError, match="/at0000/name/value: value of 'Invalid Value' did not match the regex pattern '\\^\\(abacus\\|wall\\)\\$'"):
        con.valid_value(example_observation, raise_exceptions=True)

    example_observation.name.value = "abacus"
    assert con.valid_value(example_observation) == True

def test_c_primitive_object_c_boolean(example_instruction):
    prim = CBoolean(False, True, assumed_value=True)
    con = CComplexObject(
        "INSTRUCTION",
        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
        node_id="at0000",
        attributes=[
            CSingleAttribute(
                "protocol",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "ITEM_TREE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "at0001",
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                cardinality=Cardinality(True, False, MultiplicityInterval(np.int32(1))),
                                children=[
                                    CComplexObject(
                                        "CLUSTER",
                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                        "at0002",
                                        attributes=[
                                            CMultipleAttribute(
                                                "items",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                cardinality=Cardinality(True, False, MultiplicityInterval(np.int32(0))),
                                                children=[
                                                    CComplexObject(
                                                        "ELEMENT",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "at0004",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "value",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CComplexObject(
                                                                        "DV_BOOLEAN",
                                                                        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        node_id="",
                                                                        attributes=[
                                                                            CSingleAttribute(
                                                                                "value",
                                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                                children=[
                                                                                    CPrimitiveObject(
                                                                                        "BOOLEAN",
                                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                                        "",
                                                                                        item=prim
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # the above constrains something like example_instruction but the boolean value
    #  can only be set to False
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/at0000/protocol/at0001/items/at0002/items/at0004/value/value: is set to True but only \\[False\\] is valid"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.true_valid = True
    assert con.valid_value(example_instruction) == True

    prim.false_valid = False
    example_instruction.protocol.items[0].items[1].value = DVBoolean(False)
    assert con.valid_value(example_instruction) == False

def test_c_primitive_object_c_integer(example_instruction):
    prim = CInteger(
        range=ProperInterval[np.int32](np.int32(0), np.int32(2), True, False)
    )
    con = CComplexObject(
        "INSTRUCTION",
        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
        node_id="at0000",
        attributes=[
            CSingleAttribute(
                "protocol",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "ITEM_TREE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "at0001",
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                cardinality=Cardinality(True, False, MultiplicityInterval(np.int32(1))),
                                children=[
                                    CComplexObject(
                                        "ELEMENT",
                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                        "at0006",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_COUNT",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "magnitude",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "INTEGER64",
                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        "",
                                                                        item=prim
                                                                    )
                                                                ]
                                                                
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                    ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # the above constrains something like example_instruction but the number of hops
    #  can only between 0 and 1
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/at0000/protocol/at0001/items/at0006/value/magnitude: value of 2 was not in interval range \\[0, 2\\)"):
        con.valid_value(example_instruction, raise_exceptions=True)

    example_instruction.protocol.items[2].value.value = np.int64(1)
    assert con.valid_value(example_instruction) == True

    prim.range = None
    prim.list_var = [np.int32(7)]
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/at0000/protocol/at0001/items/at0006/value/magnitude: value of 1 was not in list of acceptable values"):
            con.valid_value(example_instruction, raise_exceptions=True)

    example_instruction.protocol.items[2].value.value = np.int64(7)
    assert con.valid_value(example_instruction) == True

def test_c_primitive_object_c_real(example_instruction):
    prim = CReal(
        range=ProperInterval[np.float32](np.float32(0.0), np.float32(0.5), True, True)
    )
    con = CComplexObject(
        "INSTRUCTION",
        occurrences=MultiplicityInterval(np.int32(1), np.int32(1)),
        node_id="at0000",
        attributes=[
            CSingleAttribute(
                "protocol",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                children=[
                    CComplexObject(
                        "ITEM_TREE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "at0001",
                        attributes=[
                            CMultipleAttribute(
                                "items",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                cardinality=Cardinality(True, False, MultiplicityInterval(np.int32(1))),
                                children=[
                                    CComplexObject(
                                        "ELEMENT",
                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                        "at0006",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_COUNT",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "accuracy",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "REAL",
                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        "",
                                                                        item=prim
                                                                    )
                                                                ]
                                                                
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                    ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # an object like example_instruction but the float accuracy must be between 0 and 0.5 inclusive

    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/at0000/protocol/at0001/items/at0006/value/accuracy: value of 1\\.0 was not in interval range \\[0\\.0, 0\\.5\\]"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.range = ProperInterval[np.float32](np.float32(0.0), np.float32(5.5), True, False)
    assert con.valid_value(example_instruction) == True

    prim.range = None
    prim.list_var = [np.float32(16.5)]
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/at0000/protocol/at0001/items/at0006/value/accuracy: value of 1\\.0 was not in list of acceptable values"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.list_var = [np.float32(1.0)]
    assert con.valid_value(example_instruction) == True

# test_c_primitive_object_c_date

# test_c_primitive_object_c_time

# test_c_primitive_object_c_date_time

# test_c_primitive_object_c_duration

# test_c_code_phrase_standard_equivalent

# test_c_code_phrase_constraint_applied

# test_archetype_slot_constraint_applied

# test_archetype_internal_ref_constraint_applied

# test_constraint_ref_throws_unsupported_error

# test_c_dv_ordinal_standard_equivalent

# test_c_dv_ordinal_constraint_applied

# test_c_dv_quantity_standard_equivalent

# test_c_dv_quantity_constraint_applied