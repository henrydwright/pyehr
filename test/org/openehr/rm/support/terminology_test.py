import pytest

from src.org.openehr.rm.support.terminology import OpenEHRCodeSetIdentifiers, OpenEHRTerminologyGroupIdentifiers

def test_valid_code_set_id_returns_true_for_valid_ids():
    valid_ids = [
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS,
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_COMPRESSION_ALGORITHMS,
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_COUNTRIES,
        OpenEHRCodeSetIdentifiers.CODE_SET_INTEGRITY_CHECK_ALGORITHMS,
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES,
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_MEDIA_TYPES,
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_NORMAL_STATUSES,
    ]
    for code_set_id in valid_ids:
        assert OpenEHRCodeSetIdentifiers.valid_code_set_id(code_set_id) is True

def test_valid_code_set_id_returns_false_for_invalid_ids():
    invalid_ids = [
        "",
        "unknown",
        "CHARACTER SETS",
        "compression_algorithms",
        "countries ",
        "integrity check algorithm",
        "languages-1",
        "media type",
        "normal status",
        None,
        123,
    ]
    for code_set_id in invalid_ids:
        assert OpenEHRCodeSetIdentifiers.valid_code_set_id(code_set_id) is False
        
def test_valid_terminology_group_id_returns_true_for_valid_ids():
    valid_ids = [
        OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_AUDIT_CHANGE_TYPE,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_ATTESTATION_REASON,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_COMPOSITION_CATEGORY,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_EVENT_MATH_FUNCTION,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_INSTRUCTION_STATES,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_INSTRUCTION_TRANSITIONS,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_NULL_FLAVOURS,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PROPERTY,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PARTICIPATION_FUNCTION,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_SETTING,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_TERM_MAPPING_PURPOSE,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_SUBJECT_RELATIONSHIP,
        OpenEHRTerminologyGroupIdentifiers.GROUP_ID_VERSION_LIFE_CYCLE_STATE,
    ]
    for group_id in valid_ids:
        assert OpenEHRTerminologyGroupIdentifiers.valid_terminology_group_id(group_id) is True

def test_valid_terminology_group_id_returns_false_for_invalid_ids():
    invalid_ids = [
        "",
        "openehr terminology",
        "audit_change_type",
        "attestation reason ",
        "composition-category",
        "event math",
        "instruction state",
        "null flavour",
        "property ",
        "participation function1",
        "setting_type",
        "term mapping",
        "subject relationship ",
        "version lifecycle",
        None,
        456,
    ]
    for group_id in invalid_ids:
        assert OpenEHRTerminologyGroupIdentifiers.valid_terminology_group_id(group_id) is False