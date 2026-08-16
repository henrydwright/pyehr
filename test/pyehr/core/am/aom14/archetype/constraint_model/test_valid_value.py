# file dedicated to testing that the constraints_met method works in a range of circumstances

import numpy as np
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CMultipleAttribute, CSingleAttribute
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID
from pyehr.core.base.foundation_types.interval import Cardinality, MultiplicityInterval
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.rm.composition.content.entry import Evaluation, Observation
from pyehr.core.rm.data_structures.history import History
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemStructure, ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
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
    with pytest.raises(ValueError, match="at0002: found 3 occurences but expected \\[1\\.\\.2\\]"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[2]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[1]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="at0002: found 0 occurences but expected \\[1\\.\\.2\\]"):
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
    with pytest.raises(ValueError, match="at0000: attribute 'uid' is mandatory \\(existence 1\\.\\.1\\) but WAS NOT provided"):
        con.valid_value(example_observation, raise_exceptions=True)

    example_observation.uid = HierObjectID("ec6b16be-7ae6-4b27-91da-710f6a458c61")
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(1))
    assert con.valid_value(example_observation) == True

    con.attributes[0].existence = MultiplicityInterval(np.int32(0), np.int32(0))
    assert con.valid_value(example_observation) == False

    with pytest.raises(ValueError, match="at0000: attribute 'uid' is prohibited \\(existence 0\\.\\.0\\) but WAS provided"):
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
    with pytest.raises(ValueError, match="at0001: found 4 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
        con.valid_value(example_evaluation, raise_exceptions=True)

    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == True

    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]
    del example_evaluation.data.items[0]

    assert con.valid_value(example_evaluation) == False
    with pytest.raises(ValueError, match="at0001: found 0 items in attribute 'items' but expected \\[1\\.\\.3\\] \\(cardinality\\)"):
        con.valid_value(example_evaluation, raise_exceptions=True)