from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.base_types.identification import TerminologyID

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

    def is_equal(self, other: 'CodePhrase'):
        return (
            (type(self) == type(other)) and
            self.terminology_id.is_equal(other.terminology_id) and
            self.code_string == other.code_string and
            self.preferred_term == other.preferred_term
        )