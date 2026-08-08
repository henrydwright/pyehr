import json

from antlr4 import CommonTokenStream, InputStream
from pyehr.core.am.aom14.archetype import Archetype
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject, CDVOrdinal
from pyehr.core.base.base_types.identification import UUID, ArchetypeID, HierObjectID
from pyehr.core.its.adl14.grammar.Adl14Lexer import Adl14Lexer
from pyehr.core.its.adl14.grammar.Adl14Parser import Adl14Parser
from pyehr.core.its.adl14 import decode_adl14, _decode_header, _decode_concept, _decode_specialise, _odin_to_raw_json, _odin_to_dict, _decode_description, _decode_terminology, _cadl_to_cobject
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
    arch_id, adl_ver, uid, is_cont = _decode_header(adl_test_file_parsed.header())

    assert arch_id.is_equal(ArchetypeID("openEHR-EHR-OBSERVATION.blood_pressure.v2"))
    assert adl_ver == "1.4"
    assert uid.is_equal(HierObjectID("1811b084-29c0-4bec-bde3-c70b7a5bc28e"))
    assert is_cont == False

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
    cobj : CComplexObject = _cadl_to_cobject(archetype_definition_parsed)

    assert cobj.rm_type_name == "OBSERVATION"
    assert cobj.node_id == "at0000"
    assert cobj.attributes[0].rm_attribute_name == "data"
    assert cobj.attributes[0].children[0].rm_type_name == "HISTORY"
    assert cobj.attributes[0].children[0].node_id == "at0001"

def test_adl14_decode_no_errors(adl_test_file):
    arch : Archetype = decode_adl14(adl_test_file)
    # if there are no errors we're good to go!

def test_adl14_with_no_translations_decodes():
    # regression for bug where file with no translations would not load
    with open("test/pyehr/core/its/noTranslation.adl14") as f:
        arch = decode_adl14(f.read())

def test_adl14_odin_with_empty_object_value_decodes():
    # regression for bug where valid appearance of "<>" in ODIN caused "ODIN object value block had no valid children" error
    with open("test/pyehr/core/its/odinEmptyObjectValue.adl14") as f:
        arch = decode_adl14(f.read())

def test_adl14_cordinal_decodes():
    with open("test/pyehr/core/its/cOrdinalUse.adl14") as f:
        arch = decode_adl14(f.read())
        #                       data         HISTORY     events     POINT_EVENT      data       ITEM_TREE     items       ELEMENT       value      C_DV_ORDINAL
        ord = arch.definition.attributes[0].children[0].attributes[0].children[0].attributes[0].children[0].attributes[0].children[0].attributes[0].children[0]
        assert isinstance(ord, CDVOrdinal)
        assert ord.list_var[0].value == 1
        assert ord.list_var[0].symbol.defining_code.code_string == "at0028"

def test_adl14_cordinal_with_float_values_decodes():
    # regression for bug where cOrdinal using float value rather than integer doesn't decode
    with open("test/pyehr/core/its/cOrdinalFloatUse.adl14") as f:
        arch = decode_adl14(f.read())
        #                        data        HISTORY      events      POINT_EVENT     data       ITEM_TREE    items         CLUSTER       items       [at0299]     value      C_DV_ORDINAL
        ord = arch.definition.attributes[0].children[0].attributes[0].children[0].attributes[0].children[0].attributes[0].children[1].attributes[0].children[6].attributes[0].children[0]

        assert isinstance(ord, CDVOrdinal)
        assert ord.list_var[1].value == 1.5
        assert ord.list_var[1].symbol.defining_code.code_string == "at0519"

def test_adl14_empty_c_dv_quantity():
    # regression for bug where valid empty CDVQuantity caused "ODIN object value block had no valid children error"
    with open("test/pyehr/core/its/emptyCDVQuantity.adl14") as f:
        arch = decode_adl14(f.read())