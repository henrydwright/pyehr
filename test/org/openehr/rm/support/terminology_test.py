import pytest

from src.org.openehr.rm.support.terminology import OpenEHRCodeSetIdentifiers

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