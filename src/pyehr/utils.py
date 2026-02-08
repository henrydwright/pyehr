from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, VersionedObject
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.demographic import Organisation, Party, Person
from pyehr.core.rm.ehr import EHR, EHRStatus


PYTHON_TYPE_TO_STRING_TYPE_MAP : dict[type, str] = {
    Party: "PARTY",
    Person: "PERSON",
    VersionedObject: "VERSIONED_OBJECT",
    OriginalVersion: "VERSION",
    Contribution: "CONTRIBUTION",
    DVText: "DV_TEXT",
    EHRStatus: "EHR_STATUS",
    EHR: "EHR",
    Organisation: "ORGANISATION"
}
"""Mapping of pyehr type (Python type) to the openEHR type string (e.g. pyehr type
of Party maps to 'PARTY')"""

def get_openehr_type_str(obj: AnyClass) -> str:
    type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

    if type_str == "VERSION":
        type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

    return type_str