from org.core.base.foundation_types import AnyClass
from org.core.base.foundation_types.primitive_types import Uri
from typing import Optional

class TerminologyTerm(AnyClass):
    """Leaf type representing a standalone term from a terminology, which consists 
    of the term text and the code, i.e. a concept reference.
    """

    concept : 'TerminologyCode'
    """Reference to the terminology concept formally representing this term"""
    
    text : str
    """Text of term"""

    def is_equal(self, other) -> bool:
        return ((type(self == type(other))) and
                self.concept.is_equal(other.concept))
    
    def __init__(self, concept: 'TerminologyCode', text: str):
        self.concept = concept
        self.text = text

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Foundation_types/Terminology_term.json
        return {
            "_type": "TERMINOLOGY_TERM",
            "text": self.text,
            "concept": self.concept.as_json()
        }

class TerminologyCode(AnyClass):
    """Primitive type representing a standalone reference to a terminology concept, 
    in the form of a terminology identifier, optional version, and a code or code string 
    from the terminology.
    """

    terminology_id : str
    """The archetype environment namespace identifier used to identify a terminology. 
    Typically a value like "snomed_ct" that is mapped elsewhere to the full URI 
    identifying the terminology."""

    terminology_version : Optional[str] = None
    """Optional string value representing terminology version, typically a date or 
    dotted numeric."""

    code_string : str
    """A terminology code or post-coordinated code expression, if supported by the terminology. 
    The code may refer to a single term, a value set consisting of multiple terms, or some other 
    entity representable within the terminology."""

    uri : Optional[Uri] = None
    """The URI reference that may be used as a concrete key into a notional terminology service
    for queries that can obtain the term text, definition, and other associated elements."""

    def is_equal(self, other) -> bool:
        return ((type(self) == type(other)) and
               (self.terminology_id == other.terminology_id) and
               (self.terminology_version == other.terminology_version) and
               (self.code_string == other.code_string) and
               (self.uri == other.uri))
    
    def __str__(self) -> str:
        return self.terminology_id + ": " + self.code_string
    
    def __init__(self, terminology_id: str, code_string: str, terminology_version: Optional[str] = None, uri: Optional[Uri] = None):
        self.terminology_id = terminology_id
        self.code_string = code_string
        self.terminology_version = terminology_version
        self.uri = uri

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Foundation_types/Terminology_code.json
        draft = {
            "_type": "TERMINOLOGY_CODE",
            "terminology_id": self.terminology_id,
            "code_string": self.code_string
        }
        if self.terminology_version is not None:
            draft["terminology_version"] = self.terminology_version
        if self.uri is not None:
            draft["uri"] = {
                "_type": "URI",
                "value": self.uri
            }
        return draft