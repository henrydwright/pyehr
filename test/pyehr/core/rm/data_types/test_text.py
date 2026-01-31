import pytest

from pyehr.core.rm.data_types.text import CodePhrase, DVText, DVCodedText, TermMapping, DVParagraph
from pyehr.core.base.base_types.identification import TerminologyID

from term import CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, TERMINOLOGY_OPENEHR, PythonTerminologyService

test_ts = PythonTerminologyService([CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_LANGUAGES], [TERMINOLOGY_OPENEHR])
test_ts_empty = PythonTerminologyService([], [])

def test_code_phrase_code_string_valid():
    term_id = TerminologyID("ICD10_1998(2019)")
    
    # should be OK
    code = CodePhrase(term_id, "A15", "Respiratory tuberculosis, bacteriologically and histologically confirmed")

    # not OK
    with pytest.raises(ValueError):
        code = CodePhrase(term_id, "", "Respiratory tuberculosis, bacteriologically and histologically confirmed")

def test_code_phase_is_equal():
    term_id = TerminologyID("ICD10_1998(2019)")
    code1 = CodePhrase(term_id, "A15", "Respiratory tuberculosis, bacteriologically and histologically confirmed")
    code2 = CodePhrase(TerminologyID("ICD10_1998(2019)"), "A15", "Respiratory tuberculosis, bacteriologically and histologically confirmed")
    assert code1.is_equal(code2)

def test_term_mapping_purpose_valid():
    tmp = DVCodedText("research study", CodePhrase(TerminologyID("openehr"), "671", "research study"))
    invalid_tmp = DVCodedText("organisational policy", CodePhrase(TerminologyID("openehr"), "100000", "organisational policy"))

    # should be OK
    tm = TermMapping('>', CodePhrase(TerminologyID("SNOMED-CT"), "159412009", "Manager - supermarket (occupation)"))
    tm = TermMapping('>', CodePhrase(TerminologyID("SNOMED-CT"), "159412009", "Manager - supermarket (occupation)"), purpose=tmp, terminology_service=test_ts)

    # not OK (no terminology service provided)
    with pytest.raises(ValueError):
        tm = TermMapping('>', CodePhrase(TerminologyID("SNOMED-CT"), "159412009", "Manager - supermarket (occupation)"), purpose=tmp)

    # not OK (terminology service doesn't have OpenEHR)
    with pytest.raises(ValueError):
        tm = TermMapping('>', CodePhrase(TerminologyID("SNOMED-CT"), "159412009", "Manager - supermarket (occupation)"), purpose=tmp, terminology_service=test_ts_empty)

    # not OK (invalid purpose code provided)
    with pytest.raises(ValueError):
        tm = TermMapping('>', CodePhrase(TerminologyID("SNOMED-CT"), "159412009", "Manager - supermarket (occupation)"), purpose=invalid_tmp, terminology_service=test_ts)

def test_term_mapping_is_valid_code():
    tmp = TermMapping('?', CodePhrase("SNOMED-CT", "257256000", "Supermarket shopping cart (physical object)"))
    
    # valid codes
    assert tmp.is_valid_match_code('?') == True
    assert tmp.is_valid_match_code('=') == True
    assert tmp.is_valid_match_code('>') == True
    assert tmp.is_valid_match_code('<') == True

    # invalid codes
    assert tmp.is_valid_match_code('a') == False
    assert tmp.is_valid_match_code('M') == False
    assert tmp.is_valid_match_code('>>') == False

def test_term_mapping_match_valid():
    # OK
    tmp = TermMapping('?', CodePhrase("SNOMED-CT", "257256000", "Supermarket shopping cart (physical object)"))

    # not OK
    with pytest.raises(ValueError):
        tmp = TermMapping('A', CodePhrase("SNOMED-CT", "257256000", "Supermarket shopping cart (physical object)"))

def test_dv_text_language_valid():
    # should be OK
    txt = DVText("Er hat Krebs")
    txt = DVText("Er hat Krebs", language=CodePhrase(TerminologyID("ISO_639-1"), "de"), terminology_service=test_ts)

    # not OK (no terminology service provided)
    with pytest.raises(ValueError):
        txt = DVText("Er hat Krebs", language=CodePhrase(TerminologyID("ISO_639-1"), "de"))

    # not OK (terminology service doesn't have languages set)
    with pytest.raises(ValueError):
        txt = DVText("Er hat Krebs", language=CodePhrase(TerminologyID("ISO_639-1"), "de"), terminology_service=test_ts_empty)

    # not OK (code not in codeset)
    with pytest.raises(ValueError):
        txt = DVText("Er hat Krebs", language=CodePhrase(TerminologyID("ISO_639-1"), "german"), terminology_service=test_ts)

def test_dv_text_encoding_valid():
    # should be OK
    txt = DVText("o/e found lump 2cm diameter")
    txt = DVText("o/e found lump 2cm diameter", encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"), terminology_service=test_ts)

    # not OK (no terminology service provided)
    with pytest.raises(ValueError):
        txt = DVText("o/e found lump 2cm diameter", encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"))

    # not OK (terminology service doesn't have character sets set)
    with pytest.raises(ValueError):
        txt = DVText("o/e found lump 2cm diameter", encoding=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"), terminology_service=test_ts_empty)

    # not OK (code not in codeset)
    with pytest.raises(ValueError):
        txt = DVText("o/e found lump 2cm diameter", encoding=CodePhrase(TerminologyID("IANA_character-sets"), "python"), terminology_service=test_ts)


def test_dv_text_mappings_valid():
    tm = TermMapping('>', CodePhrase("SNOMED-CT", "159412009", "Manager - supermarket (occupation)"))

    # should be OK
    txt = DVText("Patient is a manager at the local Tesco", mappings=[tm])
    
    # not OK
    with pytest.raises(ValueError):
        txt = DVText("Patient is a manager at the local Tesco", mappings=[])

def test_dv_text_formatting_valid():

    # should be OK
    txt = DVText("**Paracetamol**: Twice a day", formatting="markdown")

    # should not be OK
    with pytest.raises(ValueError):
        txt = DVText("**Paracetamol**: Twice a day", formatting="")

def test_dv_paragraph_items_valid():
    txt = DVText("Hello world!")
    
    # should be OK
    p = DVParagraph([txt])

    # not OK (empty list of items)
    with pytest.raises(ValueError):
        p = DVParagraph([])
