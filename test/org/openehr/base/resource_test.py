import pytest
import numpy as np

from org.openehr.base.resource import AuthoredResource, TranslationDetails, ResourceDescriptionItem, ResourceDescription
from org.openehr.base.foundation_types.terminology import TerminologyCode

class TestAuthoredResourceImplementation(AuthoredResource):

    __test__ = False

    def __init__(self, original_lanugage : TerminologyCode):
        super().__init__(original_lanugage)

    def current_revision(self) -> str:
        return "(uncontrolled)"
    
def test_languages_available_valid():
    # invariant - Languages_available_valid: languages_available.has (original_language)
    lang = TerminologyCode("ISO639-1", "en")
    res = TestAuthoredResourceImplementation(lang)

    assert "en" in res.languages_available()

def test_translations_valid():
    # invariant - Translations_valid: translations /= Void implies (not translations.is_empty and not translations.has (orginal_language.code_string))
    lang = TerminologyCode("ISO639-1", "en")
    lang_de =  TerminologyCode("ISO639-1", "de")

    res = TestAuthoredResourceImplementation(lang)

    # cannot create a translation for a resource with no description
    with pytest.raises(Exception):
        res.add_translation(TranslationDetails(lang_de, {"name": "Herr Beispiel Urheber"}), ResourceDescriptionItem(lang_de, "Testressource zum Testen von Invarianten auf Sprachen"))

    lifecycle = TerminologyCode("lifecycle", "DRAFT")
    meta = ResourceDescription({"name", "Mr Test Author"}, lifecycle, res)
    res.set_description(meta)

    # cannot create a translation for a resource with no description details
    with pytest.raises(Exception):
        res.add_translation(TranslationDetails(lang, {"name": "Mr Test Author"}), ResourceDescriptionItem(lang, "Test resource to test invariant on languages"))

    res.description.details = {"en": ResourceDescriptionItem(lang, "Test resource to test invariant on languages")}

    # cannot create a translation with same language as original
    with pytest.raises(ValueError):
        res.add_translation(TranslationDetails(lang, {"name": "Mr Test Author"}), ResourceDescriptionItem(lang, "Test resource to test invariant on languages"))

    # cannot create a translation with a mismatch of languages
    with pytest.raises(ValueError):
        res.add_translation(TranslationDetails(lang, {"name": "Mr Test Author"}), ResourceDescriptionItem(lang_de, "Testressource zum Testen von Invarianten auf Sprachen"))

    # once a translation is added the list is not void and is not empty
    res.add_translation(TranslationDetails(lang_de, {"name": "Herr Beispiel Urheber"}), ResourceDescriptionItem(lang_de, "Testressource zum Testen von Invarianten auf Sprachen"))
    assert len(res.translations) > 0

def test_description_valid():
    # invariant - Description_valid: translations /= Void implies (description.details.for_all (d | translations.has_key (d.language.code_string)))

    lang = TerminologyCode("ISO639-1", "en")
    lang_de =  TerminologyCode("ISO639-1", "de")

    res = TestAuthoredResourceImplementation(lang)

    lifecycle = TerminologyCode("lifecycle", "DRAFT")

    meta = ResourceDescription({"name", "Mr Test Author"}, lifecycle, res)
    
    # setting description on an object which doesn't have one yet should work fine
    res.set_description(meta)
    assert res.description == meta

    meta2 = ResourceDescription({"name", "Mr Test Author"}, lifecycle, res)
    meta2.details = {"de": ResourceDescriptionItem(lang_de, "Testressource zum Testen von Invarianten auf Sprachen")}
    # setting description on an object that already has one without no details, should NOT work if the new one has details without original_language
    with pytest.raises(ValueError):
        res.set_description(meta2)

    # setting description on an object that already has one without no details, should work if the new one has a set of details for the original_language
    meta3 = ResourceDescription({"name", "Mr Test Author"}, lifecycle, res)
    meta3.details = {"en": ResourceDescriptionItem(lang, "Test resource to test invariant on languages")}
    res.set_description(meta3)
    assert res.description == meta3

    res.add_translation(TranslationDetails(lang_de, {"name": "Herr Beispiel Urheber"}), ResourceDescriptionItem(lang_de, "Testressource zum Testen von Invarianten auf Sprachen"))

    # setting details on an object which has a translation (and thus existing details) should fail when the new description doesn't have details
    with pytest.raises(ValueError):
        res.set_description(meta)

    # ...or does not contain all the same language codes
    with pytest.raises(ValueError):
        res.set_description(meta2)