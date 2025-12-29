import pytest

from common import CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_LANGUAGES, TERMINOLOGY_OPENEHR, PythonTerminologyService
from pyehr.core.base.base_types.identification import ArchetypeID, TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import Participation, PartyIdentified, PartyProxy
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.ehr.composition import Composition, EventContext
from pyehr.core.rm.ehr.composition.content import ContentItem
from pyehr.core.rm.ehr.composition.content.navigation import Section

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES], [TERMINOLOGY_OPENEHR])

s0 = Section(
    name=DVText("subjective"),
    archetype_node_id="at0011"
)

s1 = Section(
    name=DVText("objective"),
    archetype_node_id="at0012"
)

s2 = Section(
    name=DVText("assessment"),
    archetype_node_id="at0013"
)

c = Composition(
    name=DVText("GP appointment - 29th Dec 2025"),
    archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
    language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
    territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
    category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
    composer=PartyIdentified(name="Dr Test General-Practitioner"),
    archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
    content=[s0, s1, s2],
    terminology_service=test_ts
)

def test_composition_category_validity():
    # OK tested above
    # category not in group
    with pytest.raises(ValueError):
        Composition(
            name=DVText("GP appointment - 29th Dec 2025"),
            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
            territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
            category=DVCodedText("area", CodePhrase(TerminologyID("openehr"), "335")),
            composer=PartyIdentified(name="Dr Test General-Practitioner"),
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
            terminology_service=test_ts
        )

def test_composition_territory_valid():
    # OK tested above
    # territory not in codeset
    with pytest.raises(ValueError):
        Composition(
            name=DVText("GP appointment - 29th Dec 2025"),
            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
            territory=CodePhrase(TerminologyID("ISO_3166-1"), "ZZ"),
            category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
            composer=PartyIdentified(name="Dr Test General-Practitioner"),
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
            terminology_service=test_ts
        )

def test_composition_language_valid():
    # OK tested above
    # language not in codeset
    with pytest.raises(ValueError):
        Composition(
            name=DVText("GP appointment - 29th Dec 2025"),
            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
            language=CodePhrase(TerminologyID("openehr"), "en-GB"),
            territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
            category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
            composer=PartyIdentified(name="Dr Test General-Practitioner"),
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
            terminology_service=test_ts
        )

def test_composition_content_valid():
    # OK tested above (no content)
    # empty list provided for content
    with pytest.raises(ValueError):
        Composition(
            name=DVText("GP appointment - 29th Dec 2025"),
            archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
            language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
            territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
            category=DVCodedText("episodic", CodePhrase(TerminologyID("openehr"), "451")),
            composer=PartyIdentified(name="Dr Test General-Practitioner"),
            content=[],
            archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
            terminology_service=test_ts
        )

def test_composition_is_persistent():
    assert c.is_persistent() == False
    c_pers = Composition(
        name=DVText("GP appointment - 29th Dec 2025"),
        archetype_node_id="openEHR-EHR-COMPOSITION.gp_appointment.v0",
        language=CodePhrase(TerminologyID("ISO_639-1"), "en-gb"),
        territory=CodePhrase(TerminologyID("ISO_3166-1"), "GB"),
        category=DVCodedText("persistent", CodePhrase(TerminologyID("openehr"), "431")),
        composer=PartyIdentified(name="Dr Test General-Practitioner"),
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.gp_appointment.v0"), "1.1.0"),
        content=[s0, s1, s2],
        terminology_service=test_ts
    )
    assert c_pers.is_persistent() == True

def test_composition_item_at_path():
    assert is_equal_value(c.item_at_path("content[at0011]"), s0)
    assert is_equal_value(c.item_at_path("content[1]"), s1)
    with pytest.raises(ValueError):
        c.item_at_path("rows[0]")
    with pytest.raises(ValueError):
        c.item_at_path("content")
    with pytest.raises(IndexError):
        c.item_at_path("content[3]")

def test_composition_items_at_path():
    assert is_equal_value(c.items_at_path("content"), [s0, s1, s2])
    with pytest.raises(ValueError):
        c.items_at_path("rows")
    with pytest.raises(ValueError):
        c.items_at_path("content[2]")

ec = EventContext(
    start_time=DVDateTime("2025-12-29"),
    setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
    terminology_service=test_ts
)

def test_event_context_setting_valid():
    with pytest.raises(ValueError):
        EventContext(
            start_time=DVDateTime("2025-12-29"),
            setting=DVCodedText("mobilehome", CodePhrase(TerminologyID("openehr"), "225a")),
            terminology_service=test_ts
        )

def test_event_context_participations_validity():
    # OK - participation list
    ec = EventContext(
        start_time=DVDateTime("2025-12-29"),
        setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
        terminology_service=test_ts,
        participations=[Participation(DVText("observer"), PartyIdentified(name="Miss M Student"))]
    )
    # NOT OK - empty list
    with pytest.raises(ValueError):
        ec = EventContext(
            start_time=DVDateTime("2025-12-29"),
            setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
            terminology_service=test_ts,
            participations=[]
        )

def test_event_context_location_valid():
    # OK - location present but filled
    ec = EventContext(
        start_time=DVDateTime("2025-12-29"),
        setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
        terminology_service=test_ts,
        location="45 Example Street, Somewhereville, RG99 2BA"
    )
    # NOT OK - location empty
    with pytest.raises(ValueError):
        ec = EventContext(
            start_time=DVDateTime("2025-12-29"),
            setting=DVCodedText("home", CodePhrase(TerminologyID("openehr"), "225")),
            terminology_service=test_ts,
            location=""
        )

