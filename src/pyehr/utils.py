from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, VersionedObject
from pyehr.core.rm.demographic import Party, Person


PYTHON_TYPE_TO_STRING_TYPE_MAP : dict[type, str] = {
    Party: "PARTY",
    Person: "PERSON",
    VersionedObject: "VERSIONED_OBJECT",
    OriginalVersion: "VERSION",
    Contribution: "CONTRIBUTION"
}
"""Mapping of pyehr type (Python type) to the openEHR type string (e.g. pyehr type
of Party maps to 'PARTY')"""

