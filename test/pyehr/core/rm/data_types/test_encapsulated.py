import hashlib
import zlib

import pytest

from term import PythonTerminologyService, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, TERMINOLOGY_OPENEHR
from pyehr.core.base.base_types.identification import TerminologyID
from pyehr.core.rm.data_types.text import CodePhrase
from pyehr.core.rm.data_types.encapsulated import DVEncapsulated, DVMultimedia, DVParsable
from pyehr.core.rm.data_types.uri import DVUri

class _DVEncapsulatedImpl(DVEncapsulated):
    def __init__(self, charset = None, language = None, terminology_service = None):
        super().__init__(charset, language, terminology_service)

test_ts = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS], [TERMINOLOGY_OPENEHR])
test_ts_empty = PythonTerminologyService([], [])


def test_dv_encapsulated_language_valid():
    # should be OK
    dvei = _DVEncapsulatedImpl()
    dvei = _DVEncapsulatedImpl(language=CodePhrase(TerminologyID("ISO_639-1"), "fr", "French"), terminology_service=test_ts)

    # not OK (missing terminology service)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(language=CodePhrase(TerminologyID("ISO_639-1"), "fr", "French"))

    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(language=CodePhrase(TerminologyID("ISO_639-1"), "fr", "French"), terminology_service=test_ts_empty)

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(language=CodePhrase(TerminologyID("ISO_639-1"), "FRENCH", "French"), terminology_service=test_ts)

def test_dv_encapsulated_charset_valid():
    # should be OK
    dvei = _DVEncapsulatedImpl()
    dvei = _DVEncapsulatedImpl(charset=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"), terminology_service=test_ts)

    # not OK (missing terminology service)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(charset=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"))

    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(charset=CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8"), terminology_service=test_ts_empty)

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvei = _DVEncapsulatedImpl(charset=CodePhrase(TerminologyID("IANA_character-sets"), "INVALID-CHARSET"), terminology_service=test_ts)

def test_dv_multimedia_not_empty():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    # should be OK (inline)
    dvm_inline = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes)
    assert dvm_inline.is_inline() == True

    # should be OK (external)
    dvm_external = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/pdf"),
        size=549453,
        terminology_service=test_ts,
        uri=DVUri("https://ruh.nhs.uk/patients/patient_information/HTH024_Wrist_Exercises.pdf")
    )
    assert dvm_external.is_external() == True

    # not OK (neither inline nor external)
    with pytest.raises(ValueError):
        dvm_invalid = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"),
            size=1024,
            terminology_service=test_ts
        )

def test_dv_multimedia_size_valid():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    # should be OK
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes)
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=0,
        terminology_service=test_ts,
        data=bytes())
    
    # not OK (size < 0)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
            size=-20,
            terminology_service=test_ts,
            data=bytes())
    
    
def test_dv_multimedia_media_type_valid():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    # should be OK
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        )
    
    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
            size=len(test_json_bytes),
            terminology_service=test_ts_empty,
            data=test_json_bytes
        )

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "INVALID-MEDIA-TYPE"), 
            size=len(test_json_bytes),
            terminology_service=test_ts,
            data=test_json_bytes
        )

def test_dv_multimedia_compression_algorithm_validity():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    test_json_bytes_compressed = zlib.compress(test_json_bytes)
    # should be OK
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        )
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes_compressed),
        terminology_service=test_ts,
        data=test_json_bytes_compressed,
        compression_algorithm=CodePhrase(TerminologyID("openehr_compression_algorithms"), "zlib")
        )
    
    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"),
            size=len(test_json_bytes_compressed),
            terminology_service=test_ts_empty,
            data=test_json_bytes_compressed,
            compression_algorithm=CodePhrase(TerminologyID("openehr_compression_algorithms"), "zlib")
        )

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"),
            size=len(test_json_bytes_compressed),
            terminology_service=test_ts,
            data=test_json_bytes_compressed,
            compression_algorithm=CodePhrase(TerminologyID("openehr_compression_algorithms"), "INVALID-ALGO")
        )
    
def test_dv_multimedia_integrity_check_validity():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    test_json_sha1 = hashlib.sha1(string=test_json_bytes).digest()
    # should be OK
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes
        )
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        integrity_check=test_json_sha1,
        integrity_check_algorithm=CodePhrase(TerminologyID("openehr_integrity_check_algorithms"), "SHA-1")
        )
    
    # not OK (missing integrity_check)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        integrity_check=test_json_sha1
        )

    # not OK (missing integrity_check_algorithm)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        integrity_check_algorithm=CodePhrase(TerminologyID("openehr_integrity_check_algorithms"), "SHA-1")
        )

def test_dv_multimedia_integrity_check_algorithm_validity():
    test_json = "{\"key\":\"value\"}"
    test_json_bytes = test_json.encode()
    test_json_sha1 = hashlib.sha1(string=test_json_bytes).digest()
    # should be OK
    dvm = DVMultimedia(
        media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"), 
        size=len(test_json_bytes),
        terminology_service=test_ts,
        data=test_json_bytes,
        integrity_check=test_json_sha1,
        integrity_check_algorithm=CodePhrase(TerminologyID("openehr_integrity_check_algorithms"), "SHA-1")
        )
    
    # not OK (terminology service has no openehr)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"),
            size=len(test_json_bytes),
            terminology_service=test_ts_empty,
            data=test_json_bytes,
            integrity_check=test_json_sha1,
            integrity_check_algorithm=CodePhrase(TerminologyID("openehr_integrity_check_algorithms"), "SHA-1")
        )

    # not OK (invalid code)
    with pytest.raises(ValueError):
        dvm = DVMultimedia(
            media_type=CodePhrase(TerminologyID("IANA_media-types"), "application/json"),
            size=len(test_json_bytes),
            terminology_service=test_ts,
            data=test_json_bytes,
            integrity_check=test_json_sha1,
            integrity_check_algorithm=CodePhrase(TerminologyID("openehr_integrity_check_algorithms"), "INVALID-ALGO")
        )

def test_dv_parsable_formalism_valid():
    # should be OK
    dvp = DVParsable("print(\"Hello, world!\")", "Python 3")
    # not OK
    with pytest.raises(ValueError):
        dvp = DVParsable("print(\"Hello, world!\")", "")

def test_dv_parsable_size_valid():
    test_str = "print(\"Hello, world!\")"
    dvp = DVParsable(test_str, "Python 3")
    assert dvp.size() == len(test_str)
