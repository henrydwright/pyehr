import pytest

from common import CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_LANGUAGES, TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.identification import ArchetypeID, TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import Participation, PartyIdentified, PartyRelated, PartySelf
from pyehr.core.rm.data_structures.history import History, PointEvent
from pyehr.core.rm.data_structures.item_structure import ItemList, ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity import DVQuantity
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.ehr.composition.content.entry import AdminEntry, Evaluation, Observation
from pyehr.core.rm.support.terminology import OpenEHRCodeSetIdentifiers

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_CHARACTER_SETS], [TERMINOLOGY_OPENEHR])

it0 = Element(
                name=DVText("hospital provider spell identifier"),
                archetype_node_id="at0011",
                value=DVIdentifier("AA-000-000-000")
            )

it_lst = ItemList(
        name=DVText("admission characteristics"),
        archetype_node_id="at0001",
        items=[
            it0,
            Element(
                name=DVText("administrative category code (on admission)"),
                archetype_node_id="at0012",
                value=DVCodedText("NHS PATIENT, including Overseas Visitors charged under the National Health Service (Overseas Visitors Hospital Charging Regulations)", CodePhrase(TerminologyID("NHS_NATIONAL_ADMINISTRATIVE_CATEGORY_CODE"), "01"))
            ),
            Element(
                name=DVText("patient classification code"),
                archetype_node_id="at0013",
                value=DVCodedText("Ordinary admission", CodePhrase(TerminologyID("NHS_NATIONAL_PATIENT_CLASSIFICATION_CODE"), "1"))
            )
        ]
    )

ae = AdminEntry(
    name=DVText("Admission 30/12/2025"),
    archetype_node_id="openEHR-EHR-ADMIN_ENTRY.cds_admission.v0",
    archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.cds_admission.v0"), "1.1.0"),
    language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb", "English (United Kingdom)"),
    encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
    subject=PartySelf(),
    data=it_lst,
    terminology_service=test_ts,
    other_participations=[
        Participation(DVText("observer"), PartyIdentified(name="Miss M Student"))
    ]
)

def test_entry_language_valid():
    # OK above
    # not OK - language not in set
    with pytest.raises(ValueError):
        bad_e = AdminEntry(
            name=DVText("Test admin entry"),
            archetype_node_id="openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0"), "1.1.0"),
            language=CodePhrase(TerminologyID("ISO_639-1"), "zz-zz"),
            encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
            subject=PartySelf(),
            data=ItemSingle(
                name=DVText("single item"),
                archetype_node_id="at0001",
                item=Element(
                    name=DVText("test item"),
                    archetype_node_id="at0011",
                    value=DVText("test")
                )
            ),
            terminology_service=test_ts
        )

def test_entry_encoding_valid():
    # not OK character set not in code set
    with pytest.raises(ValueError):
        bad_e = AdminEntry(
            name=DVText("Test admin entry"),
            archetype_node_id="openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0"), "1.1.0"),
            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
            encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-88888"),
            subject=PartySelf(),
            data=ItemSingle(
                name=DVText("single item"),
                archetype_node_id="at0001",
                item=Element(
                    name=DVText("test item"),
                    archetype_node_id="at0011",
                    value=DVText("test")
                )
            ),
            terminology_service=test_ts
        )

def test_entry_subject_validity():
    assert ae.subject_is_self() == True
    other_sub = AdminEntry(
            name=DVText("Test admin entry"),
            archetype_node_id="openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0"), "1.1.0"),
            language=CodePhrase(TerminologyID("openehr"), "en-gb"),
            encoding=CodePhrase(TerminologyID("openehr"), "UTF-8"),
            subject=PartyRelated(DVCodedText("parent", CodePhrase(TerminologyID("openehr"), "254")), test_ts, name="Mrs T Test"),
            data=ItemSingle(
                name=DVText("single item"),
                archetype_node_id="at0001",
                item=Element(
                    name=DVText("test item"),
                    archetype_node_id="at0011",
                    value=DVText("test")
                )
            ),
            terminology_service=test_ts
        )
    assert other_sub.subject_is_self() == False

def test_entry_other_participations():
    # OK - see above
    # NOT OK - empty list
    with pytest.raises(ValueError):
        other_sub = AdminEntry(
            name=DVText("Test admin entry"),
            archetype_node_id="openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-ADMIN_ENTRY.test_admin_entry.v0"), "1.1.0"),
            language=CodePhrase(TerminologyID("openehr"), "en-gb"),
            encoding=CodePhrase(TerminologyID("openehr"), "UTF-8"),
            subject=PartyRelated(DVCodedText("parent", CodePhrase(TerminologyID("openehr"), "254")), test_ts, name="Mrs T Test"),
            data=ItemSingle(
                name=DVText("single item"),
                archetype_node_id="at0001",
                item=Element(
                    name=DVText("test item"),
                    archetype_node_id="at0011",
                    value=DVText("test")
                )
            ),
            terminology_service=test_ts,
            other_participations=[]
        )

def test_admin_entry_item_at_path():
    assert is_equal_value(ae.item_at_path(""), ae)
    assert is_equal_value(ae.item_at_path("data"), it_lst)
    assert is_equal_value(ae.item_at_path("data/items[0]"), it0)

def test_admin_entry_items_at_path():
    assert is_equal_value(ae.items_at_path("data/items"), it_lst.items)

his = History[ItemTree](
        name=DVText("history"),
        archetype_node_id="at0002",
        origin=DVDateTime("2026-01-01T12:28:00Z")
    )
his.events = [
            PointEvent[ItemTree](
                name=DVText("weight at 12:28"),
                archetype_node_id="at0003",
                time=DVDateTime("2026-01-01T12:28:00Z"),
                data=ItemTree(
                    name=DVText("weight observation"),
                    archetype_node_id="at0001",
                    items=[
                        Element(
                            name=DVText("weight"),
                            archetype_node_id="at0004",
                            value=DVQuantity(82.0, "kg")
                        )
                    ]
                ),
                parent=his
            )
        ]
obs = Observation(
    name=DVText("Body weight"),
    archetype_node_id="openEHR-EHR-OBSERVATION.body_weight.v2",
    language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
    encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
    subject=PartySelf(),
    archetype_details=Archetyped(ArchetypeID("openEHR-EHR-OBSERVATION.body_weight.v2"), "1.1.0"),
    data=his,
    state=his,
    terminology_service=test_ts
)

def test_observation_item_at_path():
    assert is_equal_value(obs.item_at_path(""), obs)
    assert is_equal_value(obs.item_at_path("data"), his)
    assert is_equal_value(obs.item_at_path("state"), his)

dat = ItemTree(
            DVText("Tree"),
            archetype_node_id="at0001",
            items=[
                Element(
                    name=DVText("Overall status"),
                    archetype_node_id="at0089",
                    value=DVCodedText("Never smoked", CodePhrase(TerminologyID("local"), "at0006"))
                )
            ]
        )

ev = Evaluation(
        name=DVText("Tobacco smoking summary"),
        archetype_node_id="openEHR-EHR-EVALUATION.tobacco_smoking_summary.v1",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.tobacco_smoking_summary.v1"), "1.1.0"),
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"),
        subject=PartySelf(),
        data=dat,
        terminology_service=test_ts
    )

def test_evaluation_item_at_path():
    assert is_equal_value(ev.item_at_path(""), ev)
    assert is_equal_value(ev.item_at_path("data"), dat)