# file dedicated to testing that the constraints_met method works in a range of circumstances

import numpy as np
from pyehr.core.am.aom14.archetype.constraint_model import CCodePhrase, CComplexObject, CDVOrdinal, CDVQuantity, CMultipleAttribute, CPrimitiveObject, CQuantityItem, CSingleAttribute, ConstraintRef
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CBoolean, CDate, CDateTime, CDuration, CInteger, CReal, CString, CTime
from pyehr.core.base.base_types.definitions import ValidityKind
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, TerminologyID
from pyehr.core.base.foundation_types.interval import Cardinality, ISODateTime, MultiplicityInterval, PointInterval, ProperInterval
from pyehr.core.base.foundation_types.time import ISODate, ISODuration, ISOTime
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.rm.composition.content.entry import Evaluation, Instruction, Observation
from pyehr.core.rm.data_structures.history import History
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemStructure, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVBoolean
from pyehr.core.rm.data_types.quantity import DVCount, DVInterval, DVOrdinal, DVQuantity
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
                    value=DVTime("22:59:00+01:00")
                ),
                Element(
                    name=DVText("yadda"),
                    archetype_node_id="at0009",
                    value=DVDateTime("2026-08-17T21:57:23Z")
                ),
                Element(
                    name=DVText("ordinal"),
                    archetype_node_id="at0010",
                    value=DVOrdinal(np.int32(12), DVCodedText("Glasgow coma scale, 12", defining_code=CodePhrase("SNOMED-CT", "91234001")))
                ),
                Element(
                     name=DVText("my quant"),
                     archetype_node_id="at0011",
                     value=DVQuantity(np.float32(45.7), "cm", precision=3)
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
    with pytest.raises(ValueError, match="/data\\[at0001\\]/items\\[at0002\\]: found 3 occurences of at0002 but expected \\[1\\.\\.2\\]"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[2]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[1]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/data\\[at0001\\]/items\\[at0002\\]: found 0 occurences of at0002 but expected \\[1\\.\\.2\\]"):
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
    with pytest.raises(ValueError, match="/: attribute 'uid' is mandatory \\(existence 1\\.\\.1\\) but WAS NOT provided"):
        con.valid_value(example_observation, raise_exceptions=True)

    example_observation.uid = HierObjectID("ec6b16be-7ae6-4b27-91da-710f6a458c61")
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(1))
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(0))
    assert con.valid_value(example_observation) == False

    with pytest.raises(ValueError, match="/: attribute 'uid' is prohibited \\(existence 0\\.\\.0\\) but WAS provided"):
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
    with pytest.raises(ValueError, match="/data\\[at0001\\]: found 4 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="/data\\[at0001\\]: found 0 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
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
    with pytest.raises(ValueError, match="/name/value: value of 'Invalid Value' was not in the permitted list of strings"):
        con.valid_value(example_observation, raise_exceptions=True)

    con.attributes[0].children[0].attributes[0].children[0].item.list_open = True
    assert con.valid_value(example_observation) == True

    con.attributes[0].children[0].attributes[0].children[0].item = CString(pattern=r"^(abacus|wall)$")
    assert con.valid_value(example_observation) == False
    with pytest.raises(ValueError, match="/name/value: value of 'Invalid Value' did not match the regex pattern '\\^\\(abacus\\|wall\\)\\$'"):
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
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0002\\]/items\\[at0004\\]/value/value: is set to True but only \\[False\\] is valid"):
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
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0006\\]/value/magnitude: value of 2 was not in interval range \\[0, 2\\)"):
        con.valid_value(example_instruction, raise_exceptions=True)

    example_instruction.protocol.items[2].value.value = np.int64(1)
    assert con.valid_value(example_instruction) == True

    prim.range = None
    prim.list_var = [np.int32(7)]
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0006\\]/value/magnitude: value of 1 was not in list of acceptable values"):
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
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0006\\]/value/accuracy: value of 1\\.0 was not in interval range \\[0\\.0, 0\\.5\\]"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.range = ProperInterval[np.float32](np.float32(0.0), np.float32(5.5), True, False)
    assert con.valid_value(example_instruction) == True

    prim.range = None
    prim.list_var = [np.float32(16.5)]
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0006\\]/value/accuracy: value of 1\\.0 was not in list of acceptable values"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.list_var = [np.float32(1.0)]
    assert con.valid_value(example_instruction) == True

def test_c_primitive_object_c_date(example_instruction):
    prim = CDate(
        ValidityKind.MANDATORY,
        ValidityKind.MANDATORY)
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
                                        "at0007",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_DATE",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "value",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "DATE",
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
    # an object like example_instruction but the date needs to have months AND days
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0007\\]/value/value: date of '1962\\-08' did not fit constraint pattern of YYYY\\-MM\\-DD"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.day_validity = ValidityKind.OPTIONAL
    assert con.valid_value(example_instruction) == True

    prim.day_validity = ValidityKind.PROHIBITED
    prim.month_validity = ValidityKind.PROHIBITED
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0007\\]/value/value: date of '1962\\-08' did not fit constraint pattern of YYYY\\-XX\\-XX"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.month_validity = ValidityKind.OPTIONAL
    assert con.valid_value(example_instruction) == True

    prim.day_validity = None
    prim.month_validity = None

    prim.range = ProperInterval[ISODate](ISODate("2020-01"), ISODate("2024-02"), True, True)
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0007\\]/value/value: provided date '1962\\-08' was not in range \\[2020\\-01, 2024\\-02\\]"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.range = ProperInterval[ISODate](ISODate("1952-02-06"), ISODate("2022-09-08"), True, False)
    assert con.valid_value(example_instruction) == True


def test_c_primitive_object_c_time(example_instruction):
    prim = CTime(
        ValidityKind.OPTIONAL,
        ValidityKind.OPTIONAL,
        ValidityKind.PROHIBITED
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
                                        "at0008",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_TIME",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "value",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "TIME",
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

    # an object like example_instruction but time zone is not allowed
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0008\\]/value/value: time of '22:59:00\\+01:00' has a timezone, which is not permitted"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.timezone_validity = None
    assert con.valid_value(example_instruction) == True

    prim.second_validity = ValidityKind.PROHIBITED
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0008\\]/value/value: time of '22:59:00\\+01:00' did not fit constraint pattern of HH:\\?\\?:XX"):
            con.valid_value(example_instruction, raise_exceptions=True)

    prim.second_validity = None
    prim.minute_validity = None
    prim.range = ProperInterval[ISOTime](ISOTime("21"), ISOTime("23"), True, True)
    assert con.valid_value(example_instruction) == True

    prim.range = ProperInterval[ISOTime](ISOTime("10:00"), ISOTime("13:22:22+02:00"))
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0008\\]/value/value: provided time of '22:59:00\\+01:00' was not in range \\(10:00:00, 13:22:22\\+02:00\\)"):
            con.valid_value(example_instruction, raise_exceptions=True)
    

    
def test_c_primitive_object_c_date_time(example_instruction):
    prim = CDateTime(
        month_validity=ValidityKind.MANDATORY,
        day_validity=ValidityKind.PROHIBITED,
        hour_validity=ValidityKind.PROHIBITED,
        minute_validity=ValidityKind.PROHIBITED,
        second_validity=ValidityKind.PROHIBITED
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
                                        "at0009",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_DATE_TIME",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "value",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CPrimitiveObject(
                                                                        "DATE_TIME",
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

    # an object like example_instruction but date_time only in years and months

    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0009\\]/value/value: datetime of '2026-08-17T21:57:23Z' did not fit constraint pattern of YYYY\\-MM\\-XXTXX:XX:XX"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.day_validity=ValidityKind.MANDATORY
    prim.hour_validity=ValidityKind.MANDATORY
    prim.minute_validity=ValidityKind.MANDATORY
    prim.second_validity=ValidityKind.MANDATORY
    assert con.valid_value(example_instruction) == True

    prim.range = ProperInterval[ISODateTime](ISODateTime("2020"), ISODateTime("2023-02-01T13:00"), True, True)
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0009\\]/value/value: provided datetime of '2026-08-17T21:57:23Z' was not in range \\[2020, 2023-02-01T13:00:00\\]"):
            con.valid_value(example_instruction, raise_exceptions=True)

    prim.range = ProperInterval[ISODateTime](ISODateTime("2020"), ISODateTime("2029-02-01T13:00"), True, True)
    assert con.valid_value(example_instruction) == True



def test_c_primitive_object_c_duration(example_instruction):
    prim = CDuration(
         years_allowed=False,
         months_allowed=False,
         weeks_allowed=False,
         days_allowed=False,
         minutes_allowed=False,
         seconds_allowed=True
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
                                        "at0007",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                    CComplexObject(
                                                        "DV_DATE",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        "",
                                                        attributes=[
                                                            CSingleAttribute(
                                                                "accuracy",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                    CComplexObject(
                                                                        "DV_DURATION",
                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        "",
                                                                        attributes=[
                                                                            CSingleAttribute(
                                                                                "value",
                                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                                children=[
                                                                                     CPrimitiveObject(
                                                                                        "DURATION",
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

    # an object like example_instruction but the accuracy measurement can only be in seconds
    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0007\\]/value/accuracy/value: duration of 'P1M' did not fit constraint pattern of PTS"):
        con.valid_value(example_instruction, raise_exceptions=True)

    prim.seconds_allowed = False
    prim.months_allowed = True
    assert con.valid_value(example_instruction) == True

    prim.years_allowed=None
    prim.months_allowed=None
    prim.weeks_allowed=None
    prim.days_allowed=None
    prim.minutes_allowed=None
    prim.seconds_allowed=None
    prim.range = ProperInterval[ISODuration](ISODuration("P2M"), ISODuration("P40W"), True)

    assert con.valid_value(example_instruction) == False
    with pytest.raises(ValueError, match="/protocol\\[at0001\\]/items\\[at0007\\]/value/accuracy/value: provided duration of 'P1M' was not in range \\[P2M, P40W\\)"):
            con.valid_value(example_instruction, raise_exceptions=True)

    prim.range = ProperInterval[ISODuration](ISODuration("PT30S"), ISODuration("P1Y"))
    assert con.valid_value(example_instruction) == True
    

def test_c_code_phrase_standard_equivalent():
    domain1 = CCodePhrase(
         "CODE_PHRASE",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         assumed_value=CodePhrase("SNOMED-CT", "257266008"),
         terminology_id=TerminologyID("SNOMED-CT"),
         code_list=["257266008", "284485005", "262176006"]
    )

    standard1 = CComplexObject(
         "CODE_PHRASE",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         assumed_value=CodePhrase("SNOMED-CT", "257266008"),
         attributes=[
              CSingleAttribute(
                        "terminology_id",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        children=[
                            CComplexObject(
                                "TERMINOLOGY_ID",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                "",
                                attributes=[
                                    CSingleAttribute(
                                            "value",
                                            MultiplicityInterval(np.int32(1), np.int32(1)),
                                            children=[
                                                CPrimitiveObject(
                                                    "STRING",
                                                    MultiplicityInterval(np.int32(1), np.int32(1)),
                                                    "",
                                                    item=CString(list_open=False, list_var=["SNOMED-CT"])
                                                )
                                            ]
                                    )
                                ]
                            )
                        ]
                ),
              CSingleAttribute(
                   "code_string",
                   MultiplicityInterval(np.int32(1), np.int32(1)),
                   children=[
                        CPrimitiveObject(
                             "STRING",
                             MultiplicityInterval(np.int32(1), np.int32(1)),
                             "",
                             item=CString(
                                  list_open=False,
                                  list_var=["257266008", "284485005", "262176006"]
                             )
                        )
                   ]
              )
        ]
    )

    assert domain1.standard_equivalent().is_equal(standard1)

    domain2 = CCodePhrase(
         "CODE_PHRASE",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         code_list=["at0010", "at1100", "at0001"]
    )

    standard2 = CComplexObject(
         "CODE_PHRASE",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         attributes=[
              CSingleAttribute(
                   "code_string",
                   MultiplicityInterval(np.int32(1), np.int32(1)),
                   children=[
                        CPrimitiveObject(
                             "STRING",
                             MultiplicityInterval(np.int32(1), np.int32(1)),
                             "",
                             item=CString(
                                  list_open=False,
                                  list_var=["at0010", "at1100", "at0001"]
                             )
                        )
                   ]
              )
        ]
    )

    assert domain2.standard_equivalent().is_equal(standard2)

def test_c_code_phrase_constraint_applied(example_evaluation):
     ccp = CCodePhrase(
                "CODE_PHRASE",
                MultiplicityInterval(np.int32(1), np.int32(1)),
                "",
                terminology_id=TerminologyID("ICD10"),
                code_list=["Z00.1", "K35.2"]
            )
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
                                        Cardinality(True, False, MultiplicityInterval(np.int32(0))),
                                        children=[
                                             CComplexObject(
                                                  "ELEMENT",
                                                  MultiplicityInterval(np.int32(1), np.int32(1)),
                                                  "at0003",
                                                  attributes=[
                                                       CSingleAttribute(
                                                            "value",
                                                            MultiplicityInterval(np.int32(1), np.int32(1)),
                                                            children=[
                                                                 CComplexObject(
                                                                      "DV_CODED_TEXT",
                                                                      MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                      "",
                                                                      attributes=[
                                                                           CSingleAttribute(
                                                                                "defining_code",
                                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                                children=[
                                                                                     ccp
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
     
     # coded thing has different codes and terminology
     assert con.valid_value(example_evaluation) == False

     ccp.code_list = None
     ccp.terminology_id = TerminologyID("SNOMED-CT")
     assert con.valid_value(example_evaluation) == True

     ccp.code_list = ["262176006"]
     assert con.valid_value(example_evaluation) == False

     ccp.terminology_id = None
     ccp.code_list = ["300722002"]
     assert con.valid_value(example_evaluation) == True

def test_c_dv_ordinal_standard_equivalent():
    domain = CDVOrdinal(
         "DV_ORDINAL",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         list_var=[
              DVOrdinal(
                   np.int32(5),
                   DVCodedText("Glasgow coma scale, 5", CodePhrase("SNOMED-CT", "74957005")),
                   normal_status=CodePhrase("openehr_normal_statuses", "LLL"),
                   normal_range=DVInterval[DVOrdinal](
                        value=PointInterval(DVOrdinal(15, DVCodedText("Glasgow coma scale, 15", CodePhrase("SNOMED-CT", "70040003"))))
                   )
              ),
              DVOrdinal(
                   np.int32(8),
                   DVCodedText("Glasgow coma scale, 8", CodePhrase("local", "at0010")),
                   normal_status=CodePhrase("openehr_normal_statuses", "LL")
              )
         ]
    )

    standard = CComplexObject(
         "DV_ORDINAL",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         attributes=[
              CSingleAttribute(
                   "value",
                   MultiplicityInterval(np.int32(1), np.int32(1)),
                   children=[
                        CPrimitiveObject(
                             "INTEGER",
                             MultiplicityInterval(np.int32(1), np.int32(1)),
                             "",
                             CInteger(
                                  list_var=[np.int32(5), np.int32(8)]
                             )
                        )
                   ]
              ),
              CSingleAttribute(
                   "symbol",
                   MultiplicityInterval(np.int32(1), np.int32(1)),
                   children=[
                        CComplexObject(
                             "DV_CODED_TEXT",
                             MultiplicityInterval(np.int32(1), np.int32(1)),
                             "",
                             attributes=[
                                  CSingleAttribute(
                                       "value",
                                       MultiplicityInterval(np.int32(1), np.int32(1)),
                                       children=[
                                        CPrimitiveObject(
                                             "STRING",
                                             MultiplicityInterval(np.int32(1), np.int32(1)),
                                             "",
                                             CString(list_open=False, list_var=["Glasgow coma scale, 5", "Glasgow coma scale, 8"])
                                        )
                                       ]
                                  ),
                                  CSingleAttribute(
                                       "defining_code",
                                       MultiplicityInterval(np.int32(1), np.int32(1)),
                                       children=[
                                            CComplexObject(
                                                 "CODE_PHRASE",
                                                 MultiplicityInterval(np.int32(1), np.int32(1)),
                                                 "",
                                                 attributes=[
                                                      CSingleAttribute(
                                                           "terminology_id",
                                                           MultiplicityInterval(np.int32(1), np.int32(1)),
                                                           children=[
                                                            CComplexObject(
                                                                 "TERMINOLOGY_ID",
                                                                 MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                 "",
                                                                 attributes=[
                                                                      CSingleAttribute(
                                                                           "value",
                                                                           MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                           children=[
                                                                                CPrimitiveObject(
                                                                                     "STRING",
                                                                                     MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                                     "",
                                                                                     CString(list_open=False, list_var=["SNOMED-CT", "local"])
                                                                                )
                                                                           ]
                                                                      )
                                                                 ]
                                                            )
                                                           ]
                                                      ),
                                                      CSingleAttribute(
                                                        "code_string",
                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                        children=[
                                                             CPrimitiveObject(
                                                                "STRING",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                "",
                                                                CString(
                                                                     list_open=False,
                                                                     list_var=["74957005", "at0010"]
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
                   ]
              ),
              CSingleAttribute(
                "normal_status",
                MultiplicityInterval(np.int32(0), np.int32(1)),
                children=[
                     CCodePhrase(
                        "CODE_PHRASE",
                        MultiplicityInterval(np.int32(1), np.int32(1)),
                        "",
                        terminology_id=TerminologyID("openehr_normal_statuses"),
                        code_list=["LLL", "LL"]
                     ).standard_equivalent()
                ]
              ),
              CSingleAttribute(
                "normal_range",
                MultiplicityInterval(np.int32(0), np.int32(1)),
                children=[
                     CComplexObject(
                          "DV_INTERVAL",
                          MultiplicityInterval(np.int32(1), np.int32(1)),
                          "",
                          attributes=[
                               CSingleAttribute(
                                "lower",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                children=[
                                     CComplexObject(
                                        "DV_ORDINAL",
                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                        "",
                                        attributes=[
                                             CSingleAttribute(
                                                  "value",
                                                  MultiplicityInterval(np.int32(1), np.int32(1)),
                                                  children=[
                                                    CPrimitiveObject(
                                                         "INTEGER",
                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                         "",
                                                         CInteger([15])
                                                    )
                                                  ]
                                             ),
                                             CSingleAttribute(
                                                  "symbol",
                                                  MultiplicityInterval(np.int32(1), np.int32(1)),
                                                  children=[
                                                    CComplexObject(
                                                         "DV_CODED_TEXT",
                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                         "",
                                                         attributes=[
                                                              CSingleAttribute(
                                                                   "value",
                                                                   MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                   children=[
                                                                    CPrimitiveObject(
                                                                         "STRING",
                                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                         "",
                                                                         CString(list_open=False, list_var=["Glasgow coma scale, 15"])
                                                                    )
                                                                   ]
                                                              ),
                                                              CSingleAttribute(
                                                                "defining_code",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                     CCodePhrase(
                                                                        "CODE_PHRASE",
                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        "",
                                                                        terminology_id=TerminologyID("SNOMED-CT"),
                                                                        code_list=["70040003"]
                                                                     ).standard_equivalent()
                                                                ]
                                                              )
                                                         ]
                                                    )
                                                  ]
                                             )
                                        ]
                                     )
                                ]
                               ),
                               CSingleAttribute(
                                "upper",
                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                children=[
                                     CComplexObject(
                                        "DV_ORDINAL",
                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                        "",
                                        attributes=[
                                             CSingleAttribute(
                                                  "value",
                                                  MultiplicityInterval(np.int32(1), np.int32(1)),
                                                  children=[
                                                    CPrimitiveObject(
                                                         "INTEGER",
                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                         "",
                                                         CInteger([15])
                                                    )
                                                  ]
                                             ),
                                             CSingleAttribute(
                                                  "symbol",
                                                  MultiplicityInterval(np.int32(1), np.int32(1)),
                                                  children=[
                                                    CComplexObject(
                                                         "DV_CODED_TEXT",
                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                         "",
                                                         attributes=[
                                                              CSingleAttribute(
                                                                   "value",
                                                                   MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                   children=[
                                                                    CPrimitiveObject(
                                                                         "STRING",
                                                                         MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                         "",
                                                                         CString(list_open=False, list_var=["Glasgow coma scale, 15"])
                                                                    )
                                                                   ]
                                                              ),
                                                              CSingleAttribute(
                                                                "defining_code",
                                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                children=[
                                                                     CCodePhrase(
                                                                        "CODE_PHRASE",
                                                                        MultiplicityInterval(np.int32(1), np.int32(1)),
                                                                        "",
                                                                        terminology_id=TerminologyID("SNOMED-CT"),
                                                                        code_list=["70040003"]
                                                                     ).standard_equivalent()
                                                                ]
                                                              )
                                                         ]
                                                    )
                                                  ]
                                             )
                                        ]
                                     )
                                ]
                               ),
                               CSingleAttribute(
                                    "lower_included",
                                    MultiplicityInterval(np.int32(1), np.int32(1)),
                                    children=[
                                        CPrimitiveObject(
                                             "BOOLEAN",
                                             MultiplicityInterval(np.int32(1), np.int32(1)),
                                             "",
                                             CBoolean(True, False)
                                        )
                                    ]
                                ),
                                CSingleAttribute(
                                    "upper_included",
                                    MultiplicityInterval(np.int32(1), np.int32(1)),
                                    children=[
                                        CPrimitiveObject(
                                                "BOOLEAN",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                "",
                                                CBoolean(True, False)
                                        )
                                    ]
                                )
                          ]
                     )
                ]
              )
         ]
    )

    assert domain.standard_equivalent().is_equal(standard)

def test_c_dv_ordinal_constraint_applied(example_instruction):
    cdvo = CDVOrdinal(
        "DV_ORDINAL",
        MultiplicityInterval(np.int32(1), np.int32(1)),
        "",
        list_var=[
            DVOrdinal(np.int32(15), DVCodedText("Glasgow coma scale, 15 (finding)", CodePhrase("SNOMED-CT", "70040003")))
        ]
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
                                        "at0010",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                     cdvo
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

    assert con.valid_value(example_instruction) == False

    cdvo.list_var.append(DVOrdinal(np.int32(12), DVCodedText("Glasgow coma scale, 12", defining_code=CodePhrase("SNOMED-CT", "91234001"))))
    assert con.valid_value(example_instruction) == True


def test_c_dv_quantity_standard_equivalent():
     domain = CDVQuantity(
          "DV_QUANTITY",
          MultiplicityInterval(np.int32(1), np.int32(1)),
          "",
          assumed_value=DVQuantity(9.5, "kg", units_display_name="kilograms"),
          list_var=[
               CQuantityItem(
                    units="g",
                    magnitude=ProperInterval[np.float32](np.float32(0), np.float32(10000)),
                    precision=PointInterval[np.int32](np.int32(0))
               ),
               CQuantityItem(
                    units="kg",
                    magnitude=ProperInterval[np.float32](np.float32(0), np.float32(10)),
                    precision=ProperInterval[np.int32](np.int32(0), np.int32(3), True, True)
               )
          ]
     )

     standard = CComplexObject(
          "DV_QUANTITY",
          MultiplicityInterval(np.int32(1), np.int32(1)),
          "",
          assumed_value=DVQuantity(9.5, "kg", units_display_name="kilograms"),
          attributes=[
               CSingleAttribute(
                    "magnitude",
                    MultiplicityInterval(np.int32(1), np.int32(1)),
                    children=[
                         CPrimitiveObject(
                              "REAL",
                              MultiplicityInterval(np.int32(1), np.int32(1)),
                              "",
                              CReal(range=ProperInterval[np.float32](np.float32(0), np.float32(10000)))
                         )
                    ]
               ),
               CSingleAttribute(
                    "units",
                    MultiplicityInterval(np.int32(1), np.int32(1)),
                    children=[
                         CPrimitiveObject(
                              "STRING",
                              MultiplicityInterval(np.int32(1), np.int32(1)),
                              "",
                              CString(list_open=False, list_var=["g", "kg"])
                         )
                    ]
               ),
               CSingleAttribute(
                    "precision",
                    MultiplicityInterval(np.int32(0), np.int32(1)),
                    children=[
                         CPrimitiveObject(
                              "INTEGER",
                              MultiplicityInterval(np.int32(1), np.int32(1)),
                              "",
                              CReal(range=ProperInterval[np.int32](np.int32(0), np.int32(3), True, True))
                         )
                    ]
               )
          ]
     )

     assert domain.standard_equivalent().is_equal(standard)



def test_c_dv_quantity_constraint_applied(example_instruction):
    cdvi = CDVQuantity(
         "DV_QUANTITY",
         MultiplicityInterval(np.int32(1), np.int32(1)),
         "",
         list_var=[
              CQuantityItem("m", magnitude=ProperInterval[np.float32](np.float32(0), np.float32(0.5)))
         ]
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
                                        "at0011",
                                        attributes=[
                                            CSingleAttribute(
                                                "value",
                                                MultiplicityInterval(np.int32(1), np.int32(1)),
                                                children=[
                                                     cdvi
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

    assert con.valid_value(example_instruction) == False

    cdvi.list_var = [CQuantityItem("cm", ProperInterval[np.float32](np.float32(0), np.float32(50), True, True))]
    assert con.valid_value(example_instruction) == True

# test_archetype_slot_constraint_applied

# test_archetype_internal_ref_constraint_applied

def test_constraint_ref_throws_unsupported_error():
     con = CComplexObject(
          "CODE_PHRASE",
          MultiplicityInterval(np.int32(1), np.int32(1)),
          "",
          attributes=[
               CSingleAttribute(
                    "code_string",
                    MultiplicityInterval(np.int32(1), np.int32(1)),
                    children=[
                        ConstraintRef("STRING", occurrences=MultiplicityInterval(np.int32(1), np.int32(1)), node_id="", reference="ac0015")
                    ]
               )
          ]
     )
     val = CodePhrase("SNOMED-CT", "286572006")

     with pytest.raises(NotImplementedError):
          con.valid_value(val)

     

