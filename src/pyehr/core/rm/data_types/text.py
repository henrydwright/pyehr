"""The rm.data_types.text package contains classes for representing all textual values in the health record, 
including plain text, coded terms, and narrative text."""

from typing import Optional

from numpy import uint8

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.base_types.identification import TerminologyID

from pyehr.core.rm.data_types import DataValue
from pyehr.core.rm.data_types.uri import DVUri

class CodePhrase(AnyClass):
    """A fully coordinated (i.e. all coordination has been performed) term from a terminology service (as distinct from a particular terminology)."""
    
    terminology_id: TerminologyID
    """Identifier of the distinct terminology from which the code_string (or its elements) was extracted."""

    code_string: str
    """The key used by the terminology service to identify a concept or coordination of concepts. This string is most likely parsable inside the terminology service, but nothing can be assumed about its syntax outside that context."""

    preferred_term: Optional[str] = None
    """Optional attribute to carry preferred term corresponding to the code or expression in code_string. Typical use in integration situations which create mappings, and representing data for which both a (non-preferred) actual term and a preferred term are both required."""

    def __init__(self, terminology_id: TerminologyID, code_string: str, preferred_term: Optional[str] = None):
        self.terminology_id = terminology_id
        if code_string == "":
            raise ValueError("Code string cannot be empty (invariant: code_string_valid)")
        self.code_string = code_string
        self.preferred_term = preferred_term
        super().__init__()

    def __str__(self):
        return f"{self.code_string}|{self.preferred_term}"

    def is_equal(self, other: 'CodePhrase'):
        return (
            (type(self) == type(other)) and
            self.terminology_id.is_equal(other.terminology_id) and
            self.code_string == other.code_string and
            self.preferred_term == other.preferred_term
        )
    
    def as_json(self):
        j = {
            "_type": "CODE_PHRASE",
            "terminology_id": self.terminology_id.as_json(),
            "code_string": self.code_string
        }
        if self.preferred_term is not None:
            j["preferred_term"] = self.preferred_term
        return j
    
class TermMapping(AnyClass):
    """Represents a coded term mapped to a DV_TEXT, and the relative match of the target term with respect to the mapped item. Plain or coded text items may appear in the EHR for which one or mappings in alternative terminologies are required. Mappings are only used to enable computer processing, so they can only be instances of DV_CODED_TEXT.

    Used for adding classification terms (e.g. adding ICD classifiers to SNOMED descriptive terms), or mapping into equivalents in other terminologies (e.g. across nursing vocabularies)."""

    match: uint8
    """The relative match of the target term with respect to the mapped text item. Result meanings:

    * `'>'`: the mapping is to a broader term e.g. orginal text = arbovirus infection , target = viral infection
    * `'='`: the mapping is to a (supposedly) equivalent to the original item
    * `'<'`: the mapping is to a narrower term. e.g. original text = diabetes , mapping = diabetes mellitus .
    * `'?'`: the kind of mapping is unknown.

    The first three values are taken from the ISO standards 2788 ( Guide to Establishment and development of monolingual thesauri) and 5964 (Guide to Establishment and development of multilingual thesauri)."""

    purpose: Optional['DVCodedText']
    """Purpose of the mapping e.g. 'automated data mining', 'billing', 'interoperability'."""

    target: CodePhrase
    """The target term of the mapping."""

    def __init__(self, match : uint8, target: CodePhrase, purpose: Optional['DVCodedText'] = None, terminology_service = None):
        # import here to avoid circular reference
        from pyehr.core.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers, util_verify_code_in_openehr_terminology_group_or_error

        self.target = target

        # invariant: match_valid
        if not self.is_valid_match_code(match):
            raise ValueError(f"Match code must be one of '>', '=', '<' or '?', but \'{match}\' was given (invariant: match_valid)")
        self.match = match
        
        # invariant: purpose_valid
        if purpose is not None:
            if (terminology_service is None):
                raise ValueError("If purpose is provided, access to a TerminologyService with OpenEHR terminology must also be given to check validity (invariant: purpose_valid)")
            util_verify_code_in_openehr_terminology_group_or_error(purpose.defining_code, OpenEHRTerminologyGroupIdentifiers.GROUP_ID_TERM_MAPPING_PURPOSE, terminology_service, invariant_name_for_error="purpose_valid")   
        self.purpose = purpose         

    def is_equal(self, other: 'TermMapping'):
        return (
            type(self) == type(other) and
            self.match == other.match and
            is_equal_value(self.purpose, other.purpose) and
            is_equal_value(self.target, other.target)
        )

    def narrower(self) -> bool:
        """The mapping is to a narrower term."""
        return self.match == '<'

    def broader(self) -> bool:
        """The mapping is to a broader term."""
        return self.match == '>'

    def equivalent(self) -> bool:
        """The mapping is to an equivalent term."""
        return self.match == '='

    def unknown(self) -> bool:
        """The kind of mapping is unknown."""
        return self.match == '?'

    def is_valid_match_code(self, c: uint8):
        """True if match valid."""
        return (
            (c == '>') or
            (c == '=') or
            (c == '<') or
            (c == '?')
        )
    
    def as_json(self):
        draft = {
            "_type": "TERM_MAPPING",
            "match": str(self.match),
            "target": self.target.as_json()
        }
        if self.purpose is not None:
            draft["purpose"] = self.purpose.as_json()
        return draft

class DVText(DataValue):
    """A text item, which may contain any amount of legal characters arranged as e.g. words, sentences etc (i.e. one DV_TEXT may be more than one word). Visual formatting and hyperlinks may be included via markdown.

    If the formatting field is set, the value field is affected as follows:

    * `formatting = "plain"`: plain text, may contain newlines;
    * `formatting = "plain_no_newlines"`: plain text with no newlines;
    * `formatting = "markdown"`: text in markdown format; use of CommonMark strongly recommended.

    A DV_TEXT can be coded by adding mappings to it."""

    value: str
    """Displayable rendition of the item, regardless of its underlying structure. For DV_CODED_TEXT, this is the rubric of the complete term as provided by the terminology service."""

    hyperlink: Optional[DVUri]
    """DEPRECATED: this field is deprecated; use markdown link/text in the value attribute, and "markdown" as the value of the formatting field.

    Original usage, prior to RM Release 1.0.4: Optional link sitting behind a section of plain text or coded term item."""

    formatting: Optional[str]
    """If set, contains one of the following values:

    * `"plain"`: use for plain text, possibly containing newlines, but otherwise unformatted (same as Void);
    * `"plain_no_newlines"`: use for text containing no newlines or other formatting;
    * `"markdown"`: use for markdown formatted text, strongly recommended in the format of the CommonMark specification.

    DEPRECATED usage: contains a string of the form `"name:value; name:value..."` , e.g. `"font-weight : bold; font-family : Arial; font-size : 12pt;"`. Values taken from W3C CSS2 properties lists for background and font."""

    mappings: Optional[list[TermMapping]]
    """Terms from other terminologies most closely matching this term, typically used where the originator (e.g. pathology lab) of information uses a local terminology but also supplies one or more equivalents from well known terminologies (e.g. LOINC)."""

    language: Optional[CodePhrase]
    """Optional indicator of the localised language in which the value is written. Coded from openEHR Code Set languages . Only used when either the text object is in a different language from the enclosing ENTRY, or else the text object is being used outside of an ENTRY or other enclosing structure which indicates the language."""

    encoding: Optional[CodePhrase]
    """Name of character encoding scheme in which this value is encoded. Coded from openEHR Code Set character sets . Unicode is the default assumption in openEHR, with UTF-8 being the assumed encoding. This attribute allows for variations from these assumptions."""

    def __init__(self, value: str, hyperlink: Optional[DVUri] = None, formatting: Optional[str] = None, mappings: Optional[list[TermMapping]] = None, language : Optional[CodePhrase] = None, encoding: Optional[CodePhrase] = None, terminology_service = None):
        # import here to avoid circular reference
        from pyehr.core.rm.support.terminology import TerminologyService, OpenEHRCodeSetIdentifiers, OpenEHRTerminologyGroupIdentifiers
        ts : TerminologyService = terminology_service

        self.value = value
        self.hyperlink = hyperlink

        # invariant: formatting_valid
        if (formatting is not None) and (formatting == ""):
            raise ValueError("If provided, formatting cannot be an empty string (invariant: formatting_valid)")
        self.formatting = formatting

        # invariant: mappings_valid
        if (mappings is not None) and (len(mappings) == 0):
            raise ValueError("If provided, mappings cannot be an empty list (invariant: mappings_valid)")
        self.mappings = mappings

        if ((language is not None) or (encoding is not None)) and (ts is None):
            raise ValueError("If language or encoding is provided, access to a TerminologyService with OpenEHR terminology must also be given to check validity (invariant: language_valid, encoding_valid)")

        # invariant: language_valid
        if (language is not None) and (not ts.has_code_set(OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES)):
            raise ValueError("If language is provided, access to a TerminologyService with OpenEHR terminology, specifically the languages code set, must also be given to check validity (invariant: language_valid)")
        elif (language is not None) and (ts.has_code_set(OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES)):
            language_code_set = ts.code_set_for_id(OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES)
            if not language_code_set.has_code(language.code_string):
                raise ValueError(f"Provided language code {language.code_string} was not in the OpenEHR languages code set (invariant: language_valid)")
        self.language = language
            
        # invariant: encoding_valid
        if (encoding is not None) and (not ts.has_code_set(OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS)):
            raise ValueError("If encoding is provided, access to a TerminologyService with OpenEHR terminology, specifically the character sets code set, must also be given to check validity (invariant: encoding_valid)")
        elif (encoding is not None) and (ts.has_code_set(OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS)):
            encoding_code_set = ts.code_set_for_id(OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS)
            if not encoding_code_set.has_code(encoding.code_string):
                raise ValueError(f"Provided encoding code {encoding.code_string} was not in the OpenEHR character set code set (invariant: encoding_valid)")
        self.encoding = encoding
            
    def is_equal(self, other: 'DVText'):
        return (
            type(self) == type(other) and
            is_equal_value(self.value, other.value) and
            is_equal_value(self.hyperlink, other.hyperlink) and
            is_equal_value(self.formatting, other.formatting) and
            is_equal_value(self.mappings, other.mappings) and
            is_equal_value(self.language, other.language) and
            is_equal_value(self.encoding, other.encoding)
        )

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_TEXT.json
        draft = {
            "_type": "DV_TEXT",
            "value": self.value
        }
        if self.hyperlink is not None:
            draft["hyperlink"] = self.hyperlink.as_json()
        if self.language is not None:
            draft["language"] = self.language.as_json()
        if self.encoding is not None:
            draft["encoding"] = self.encoding.as_json()
        if self.formatting is not None:
            draft["formatting"] = self.formatting
        if self.mappings is not None:
            mappings = []
            for mapping in self.mappings:
                mappings.append(mapping.as_json())
            draft["mappings"] = mappings
        return draft

class DVCodedText(DVText):
    """A text item whose value must be the rubric from a controlled terminology, the key (i.e. the 'code') of which is the _defining_code_ attribute. In other words: a `DV_CODED_TEXT` is a combination of a `CODE_PHRASE` (effectively a code) and the rubric of that term, from a terminology service, in the language in which the data were authored.

    Since `DV_CODED_TEXT` is a subtype of `DV_TEXT`, it can be used in place of it, effectively allowing the type `DV_TEXT` to mean a text item, which may optionally be coded.

    Misuse: If the intention is to represent a term code attached in some way to a fragment of plain text, `DV_CODED_TEXT` should not be used; instead use a `DV_TEXT` and a `TERM_MAPPING` to a `CODE_PHRASE`."""
    
    defining_code : CodePhrase

    def __init__(self, value: str, defining_code: CodePhrase, hyperlink: Optional[DVUri] = None, formatting: Optional[str] = None, mappings: Optional[list[TermMapping]] = None, language : Optional[CodePhrase] = None, encoding: Optional[CodePhrase] = None, terminology_service = None):
        self.defining_code = defining_code
        super().__init__(value, hyperlink, formatting, mappings, language, encoding, terminology_service)

    def is_equal(self, other: 'DVCodedText'):
        return (
            self.defining_code.is_equal(other.defining_code) and
            super().is_equal(other)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_CODED_TEXT.json
        draft = super().as_json()
        draft["_type"] = "DV_CODED_TEXT"
        draft["defining_code"] = self.defining_code.as_json()
        return draft

class DVParagraph(DataValue):
    """DEPRECATED: use markdown formatted DV_TEXT instead.

    Original definition:

    A logical composite text value consisting of a series of DV_TEXTs, i.e. plain text (optionally coded) potentially with simple formatting, to form a larger tract of prose, which may be interpreted for display purposes as a paragraph.

    DV_PARAGRAPH is the standard way for constructing longer text items in summaries, reports and so on.
    """

    items : list[DVText]
    """Items making up the paragraph, each of which is a text item (which may have its own formatting, and/or have hyperlinks)."""

    def __init__(self, items: list[DVText]):
        if len(items) == 0:
            raise ValueError("List of items cannot be an empty list (invariant: items_valid)")
        self.items = items
        
    def is_equal(self, other: 'DVParagraph'):
        return (
            type(self) == type(other) and
            is_equal_value(self.items, other.items)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_PARAGRAPH.json
        json_items = []
        for item in self.items:
            json_items.append(item.as_json())
        return {
            "_type": "DV_PARAGRAPH",
            "items": json_items
        }