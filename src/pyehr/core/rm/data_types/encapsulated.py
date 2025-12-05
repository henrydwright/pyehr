"""The data_types.encapsulated package contains classes representing data values whose internal 
structure is defined outside the EHR model, such as multimedia and parsable data."""

from abc import ABC, abstractmethod
import base64
from typing import Optional

import numpy as np

from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types import DataValue
from pyehr.core.rm.data_types.text import CodePhrase
from pyehr.core.rm.data_types.uri import DVUri
from pyehr.core.rm.support.terminology import TerminologyService, OpenEHRCodeSetIdentifiers, util_verify_code_in_openehr_codeset_or_error

class DVEncapsulated(DataValue):
    """Abstract class defining the common meta-data of all types of encapsulated data."""

    charset : Optional[CodePhrase]
    """Name of character encoding scheme in which this value is encoded. Coded from 
    openEHR Code Set `character sets`. Unicode is the default assumption in openEHR, 
    with UTF-8 being the assumed encoding. This attribute allows for variations from 
    these assumptions."""

    language : Optional[CodePhrase]
    """Optional indicator of the localised language in which the data is written, 
    if relevant. Coded from openEHR Code Set `languages`."""

    @abstractmethod
    def __init__(self, charset : Optional[CodePhrase] = None, language : Optional[CodePhrase] = None, terminology_service: Optional[TerminologyService] = None):
        if ((charset is not None) or (language is not None)) and terminology_service is None:
            raise ValueError("If language or charset provided, a terminology service must be provided to check their validity (invariant: language_valid, charset_valid)")

        if (charset is not None):
            util_verify_code_in_openehr_codeset_or_error(charset, OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS, terminology_service, invariant_name_for_error="charset_valid")
        
        self.charset = charset
        
        if (language is not None):
            util_verify_code_in_openehr_codeset_or_error(language, OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES, terminology_service, invariant_name_for_error="language_valid")
                
        self.language = language
        super().__init__()

    def is_equal(self, other):
        return (
            type(self) == type(other) and
            is_equal_value(self.charset, other.charset) and
            is_equal_value(self.language, other.language)
        )
    
    def as_json(self):
        # relevant parts of https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_PARSABLE.json
        draft = {}
        if self.charset is not None:
            draft["charset"] = self.charset.as_json()
        if self.language is not None:
            draft["language"] = self.charset.as_json()
        return draft

class DVMultimedia(DVEncapsulated):
    """A specialisation of `DV_ENCAPSULATED` for audiovisual and bio-signal types. Includes further metadata relating to multimedia types which are not applicable
    to other subtypes of `DV_ENCAPSULATED`."""

    alternate_text : Optional[str]
    """Text to display in lieu of multimedia display/replay."""

    uri : Optional[DVUri]
    """URI reference to electronic information stored outside the record as a file, database entry etc, if supplied as a reference."""

    data : Optional[bytes]
    """The actual data found at uri, if supplied inline."""

    media_type : CodePhrase
    """Data media type coded from openEHR code set media types (interface for the IANA MIME types code set)."""

    compression_algorithm: Optional[CodePhrase]
    """Compression type, a coded value from the openEHR Integrity check code set. Void means no compression."""

    integrity_check : Optional[bytes]
    """Binary cryptographic integrity checksum."""

    integrity_check_algorithm : Optional[CodePhrase]
    """Type of integrity check, a coded value from the openEHR Integrity check code set."""

    thumbnail: Optional['DVMultimedia']
    """The thumbnail for this item, if one exists; mainly for graphics formats."""

    size: np.int32
    """Original size in bytes of unencoded encapsulated data. I.e. encodings such as base64, hexadecimal etc do not change the value of this attribute."""


    def __init__(self, 
                 media_type : CodePhrase, 
                 size : np.int32, 
                 terminology_service : TerminologyService,
                 data : Optional[bytes] = None,
                 uri : Optional[DVUri] = None,
                 charset : Optional[CodePhrase] = None, 
                 language : Optional[CodePhrase] = None, 
                 alternate_text: Optional[str] = None,
                 compression_algorithm: Optional[CodePhrase] = None,
                 integrity_check: Optional[bytes] = None,
                 integrity_check_algorithm: Optional[CodePhrase] = None,
                 thumbnail: Optional['DVMultimedia'] = None
                 ):

        if (data is None and uri is None):
            raise ValueError("Either data should be provided (inline) or uri (external) (invariant: not_empty)")

        if ((integrity_check is not None) and (integrity_check_algorithm is None)) or ((integrity_check is None) and (integrity_check_algorithm is not None)):
            raise ValueError("Either integrity_check and integrity_check_algorithm should be provided or neither should be provided (invariant: integrity_check_validity)")

        if size < 0:
            raise ValueError("Size must be >= 0 (invariant: size_valid)")

        util_verify_code_in_openehr_codeset_or_error(
            media_type, OpenEHRCodeSetIdentifiers.CODE_SET_ID_MEDIA_TYPES, terminology_service, invariant_name_for_error="media_type_valid"
        )
        self.media_type = media_type

        if compression_algorithm is not None:
            util_verify_code_in_openehr_codeset_or_error(
                compression_algorithm, OpenEHRCodeSetIdentifiers.CODE_SET_ID_COMPRESSION_ALGORITHMS, terminology_service, invariant_name_for_error="compression_algorithm_validity"
            )
        self.compression_algorithm = compression_algorithm

        if integrity_check_algorithm is not None:
            util_verify_code_in_openehr_codeset_or_error(
                integrity_check_algorithm, OpenEHRCodeSetIdentifiers.CODE_SET_INTEGRITY_CHECK_ALGORITHMS, terminology_service, invariant_name_for_error="integrity_check_algorithm_validity"
            )
        self.integrity_check_algorithm = integrity_check_algorithm

        self.size = size
        self.data = data
        self.uri = uri
        self.alternate_text = alternate_text
        self.integrity_check = integrity_check
        self.thumbnail = thumbnail
        super().__init__(charset, language, terminology_service)

    def is_external(self) -> bool:
        """Computed from the value of the _uri_ attribute: True if the data is stored externally to the record, as indicated by _uri_. A copy may also be stored internally, in which case _is_expanded_ is also true."""
        return (self.uri is not None)

    def is_inline(self) -> bool:
        """Computed from the value of the data attribute. True if the data is stored in expanded form, ie within the EHR itself."""
        return (self.data is not None)

    def is_compressed(self) -> bool:
        """Computed from the value of the _compression_algorithm_ attribute: True if the data is stored in compressed form."""
        return (self.compression_algorithm is not None)

    def has_integrity_check(self) -> bool:
        """Computed from the value of the _integrity_check_algorithm_ attribute: True if an integrity check has been computed."""
        return (self.integrity_check_algorithm is not None)
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_MULTIMEDIA.json
        draft = super().as_json()
        draft["_type"] = "DV_MULTIMEDIA"
        draft["media_type"] = self.media_type.as_json()
        draft["size"] = int(self.size)
        if self.alternate_text is not None:
            draft["alternate_text"] = self.alternate_text
        if self.uri is not None:
            draft["uri"] = self.uri.as_json()
        if self.data is not None:
            draft["data"] = base64.b64encode(self.data).decode()
        if self.compression_algorithm is not None:
            draft["compression_algorithm"] = self.compression_algorithm.as_json()
        if self.integrity_check is not None:
            draft["integrity_check"] = base64.b64encode(self.integrity_check).decode()
        if self.integrity_check_algorithm is not None:
            draft["integrity_check_algorithm"] = self.integrity_check_algorithm.as_json()
        if self.thumbnail is not None:
            draft["thumbnail"] = self.thumbnail.as_json()
        return draft
        



class DVParsable(DVEncapsulated):
    """Encapsulated data expressed as a parsable String. The internal model of the data item 
    is not described in the openEHR model in common with other encapsulated types, but in this 
    case, the form of the data is assumed to be plaintext, rather than compressed or other types 
    of large binary data."""

    value : str
    """The string, which may validly be empty in some syntaxes."""

    formalism : str
    """Name of the formalism, e.g. GLIF 1.0 , Proforma etc."""

    def __init__(self, value: str, formalism : str, charset = None, language = None, terminology_service = None):
        self.value = value
        if formalism == "":
            raise ValueError("Formalism cannot be empty (invariant: formalism_valid)")
        self.formalism = formalism
        super().__init__(charset, language, terminology_service)

    def size(self) -> np.int32:
        """Size in bytes of value."""
        b = self.value.encode()
        return len(b)
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_PARSABLE.json
        draft = super().as_json()
        draft["_type"] = "DV_PARSABLE"
        draft["value"] = self.value
        draft["formalism"] = self.formalism
        return draft