import json

from antlr4 import CommonTokenStream, InputStream
from pyehr.core.base.base_types.identification import UUID, ArchetypeID
from pyehr.core.its.adl14.grammar.Adl14Lexer import Adl14Lexer
from pyehr.core.its.adl14.grammar.Adl14Parser import Adl14Parser
from pyehr.core.its.adl14 import _decode_header, _decode_concept, _decode_specialise, _odin_to_raw_json, _odin_to_dict, _decode_description, _decode_terminology, _cadl_to_cobject
from pyehr.core.its.adl14.grammar.Cadl14Lexer import Cadl14Lexer
from pyehr.core.its.adl14.grammar.Cadl14Parser import Cadl14Parser
from pyehr.core.its.adl14.grammar.OdinLexer import OdinLexer
from pyehr.core.its.adl14.grammar.OdinParser import OdinParser
import pytest

@pytest.fixture(scope="module")
def adl_test_file() -> str:
    ret = None
    with open("test/pyehr/core/its/bloodPressure.adl14") as f:
        ret = f.read()
    return ret

@pytest.fixture(scope="module")
def adl_test_file_parsed(adl_test_file) -> Adl14Parser.AuthoredArchetypeContext:
    lex_adl = Adl14Lexer(InputStream(adl_test_file))
    par_adl = Adl14Parser(CommonTokenStream(lex_adl))

    return par_adl.authoredArchetype()

@pytest.fixture(scope="module")
def archetype_description_parsed(adl_test_file_parsed : Adl14Parser.AuthoredArchetypeContext) -> OdinParser.OdinObjectContext:
    lex_odin = OdinLexer(InputStream(adl_test_file_parsed.descriptionSection().odinText().getText()))
    par_odin = OdinParser(CommonTokenStream(lex_odin))

    return par_odin.odinObject()

@pytest.fixture(scope="module")
def archetype_terminology_parsed(adl_test_file_parsed) -> OdinParser.OdinObjectContext:
    lex_odin = OdinLexer(InputStream(adl_test_file_parsed.terminologySection().odinText().getText()))
    par_odin = OdinParser(CommonTokenStream(lex_odin))

    return par_odin.odinObject()

@pytest.fixture(scope="module")
def archetype_definition_parsed(adl_test_file_parsed) -> Cadl14Parser.CComplexObjectContext:
    lex_cadl = Cadl14Lexer(InputStream(adl_test_file_parsed.definitionSection().cadlText().getText()))
    par_cadl = Cadl14Parser(CommonTokenStream(lex_cadl))

    return par_cadl.cComplexObject()

def test_header_decode(adl_test_file_parsed : Adl14Parser.AuthoredArchetypeContext):
    arch_id, adl_ver, uid = _decode_header(adl_test_file_parsed.header())

    assert arch_id.is_equal(ArchetypeID("openEHR-EHR-OBSERVATION.blood_pressure.v2"))
    assert adl_ver == "1.4"
    assert uid.is_equal(UUID("1811b084-29c0-4bec-bde3-c70b7a5bc28e"))

def test_concept_decode(adl_test_file_parsed : Adl14Parser.AuthoredArchetypeContext):
    concept = _decode_concept(adl_test_file_parsed.conceptSection())

    assert concept == "at0000"

def test_specialise_decode(adl_test_file_parsed: Adl14Parser.AuthoredArchetypeContext):
    parent_id = _decode_specialise(adl_test_file_parsed.specializeSection())

    assert parent_id is None

def test_odin_to_dict_description(archetype_description_parsed: OdinParser.OdinObjectContext):
    dct = _odin_to_dict(archetype_description_parsed)
    raw = _odin_to_raw_json(dct)
    
    assert raw["original_author"]["name"] == "Sam Heard"
    assert raw["details"]["de"]["language"]["_type"] == "CODE_PHRASE"
    assert raw["other_details"]["original_namespace"] == "org.openehr"

def test_odin_to_dict_terminology(archetype_terminology_parsed : OdinParser.OdinObjectContext):
    dct = _odin_to_dict(archetype_terminology_parsed)
    raw = _odin_to_raw_json(dct)

    assert raw["term_definitions"]["en"]["items"]["at0000"]["text"] == "Blood pressure"
    assert raw["term_definitions"]["ca"]["items"]["at0001"]["text"] == "Antecedents"
    assert raw["term_bindings"]["SNOMED-CT"]["items"]["at0000"]["code_string"] == "364090009"

def test_description_decode(archetype_description_parsed: OdinParser.OdinObjectContext):
    desc = _decode_description(archetype_description_parsed)

    assert desc.original_author["name"] == "Sam Heard"
    assert len(desc.details) == 17
    assert desc.lifecycle_state == "published"
    assert desc.custodian_namespace is None
    assert desc.other_details.get("revision") == "2.0.16"

def test_terminology_decode(archetype_terminology_parsed: OdinParser.OdinObjectContext):
    term = _decode_terminology(archetype_terminology_parsed)

    assert term.has_language("de")
    assert term.term_definition("at1040", "en").items["text"] == "Invasive"
    assert term.term_definition("at0025", "es").items["text"] == "Brazo derecho"
    assert term.term_binding("SNOMED-CT", "at0000").value.code_string == "364090009"

def test_cadl_object_decode(archetype_definition_parsed: Cadl14Parser.CComplexObjectContext):
    # comp = _cadl_to_cobject(archetype_definition_parsed)

    # print(json.dumps(comp.as_json(), indent=1))

    # assert True == False
    pass
