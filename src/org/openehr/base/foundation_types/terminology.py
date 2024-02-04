from org.openehr.base.foundation_types import AnyClass
from org.openehr.base.foundation_types.primitive_types import Uri
from typing import Optional

class TerminologyCode(AnyClass):
    """Primitive type representing a standalone reference to a terminology concept, 
    in the form of a terminology identifier, optional version, and a code or code string 
    from the terminology.
    """
    terminology_id : str
    """The archetype environment namespace identifier used to identify a terminology. 
    Typically a value like "snomed_ct" that is mapped elsewhere to the full URI 
    identifying the terminology."""
    terminology_version : Optional[str]
    """Optional string value representing terminology version, typically a date or 
    dotted numeric."""
    code_string : str
    """A terminology code or post-coordinated code expression, if supported by the terminology. 
    The code may refer to a single term, a value set consisting of multiple terms, or some other 
    entity representable within the terminology."""
    uri : Optional[Uri]
    """The URI reference that may be used as a concrete key into a notional terminology service
    for queries that can obtain the term text, definition, and other associated elements."""

    def is_equal(self, other) -> bool:
        return ((type(self) == type(other)) and
               (self.terminology_id == other.terminology_id) and
               (self.terminology_version == other.terminology_version) and
               (self.code_string == other.code_string) and
               (self.uri == other.uri))


class TerminologyTerm(AnyClass):
    """Leaf type representing a standalone term from a terminology, which consists 
    of the term text and the code, i.e. a concept reference.
    """
    text : str
    """Text of term"""
    concept : TerminologyCode
    """Reference to the terminology concept formally representing this term"""

    def is_equal(self, other) -> bool:
        return ((type(self == type(other))) and
                self.concept.is_equal(other.concept))
