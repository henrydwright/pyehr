import pytest

from src.org.openehr.rm.support.terminology import OpenEHRCodeSetIdentifiers, OpenEHRTerminologyGroupIdentifiers

def test_valid_code_set_id_returns_true_for_valid_ids():
    valid_ids = [
        "character sets",
        "compression algorithms",
        "countries",
        "integrity check algorithms",
        "languages",
        "media types",
        "normal statuses",
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
        "openehr",
        "audit_change_type",
        "attestation_reason",
        "composition_category",
        "event_math_function",
        "instruction_states",
        "instruction_transitions",
        "null_flavours",
        "property",
        "participation_function",
        "setting",
        "term_mapping_purpose",
        "subject_relationship",
        "version_lifecycle_state",
    ]
    for group_id in valid_ids:
        assert OpenEHRTerminologyGroupIdentifiers.valid_terminology_group_id(group_id) is True

def test_valid_terminology_group_id_returns_false_for_invalid_ids():
    invalid_ids = [
        "",
        "openehr terminology",
        "audit change type",
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