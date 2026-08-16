# file dedicated to testing that the constraints_met method works in a range of circumstances

import numpy as np
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject
from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.interval import MultiplicityInterval
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.rm.composition.content.entry import Evaluation, Observation
from pyehr.core.rm.data_structures.history import History
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemStructure
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVText
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
        data=ItemSingle(
            name=DVText("Thoughts"),
            archetype_node_id="at0001",
            item=Element(
                name=DVText("Text"),
                archetype_node_id="at0002",
                value=DVText("I think, therefore, I am")
            )
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