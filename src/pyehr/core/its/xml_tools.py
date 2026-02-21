import re
from typing import Optional

import xml.etree.ElementTree as ET

from pyehr.core.its.xml import IXMLSupport
from pyehr.utils import OPENEHR_TYPE_MAP
from term import CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_NORMAL_STATUSES, TERMINOLOGY_OPENEHR, PythonTerminologyService


def decode_xml(xml_str: str, 
               target: Optional[str] = None, 
               terminology_service = None) -> IXMLSupport:
    """Read an OpenEHR ITS XML string

    :param xml_str: OpenEHR ITS XML as a string
    :param target: (Optional) Target type to decode the root element to (e.g. 'CODE_PHRASE')
    :param terminology_service: (Optional) Provide a terminology service, if not provided, uses the inbuilt pyehr terminology service.
    :type terminology_service: TerminologyService"""

    if terminology_service is None:
        terminology_service = PythonTerminologyService([CODESET_OPENEHR_LANGUAGES, CODESET_OPENEHR_COUNTRIES, CODESET_OPENEHR_CHARACTER_SETS, CODESET_OPENEHR_MEDIA_TYPES, CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, CODESET_OPENEHR_COMPRESSION_ALGORITHMS, CODESET_OPENEHR_NORMAL_STATUSES], [TERMINOLOGY_OPENEHR])

    # remove namespace to avoid a world of pain...
    xmlstring = re.sub(' xmlns="[^"]+"', '', xml_str, count=1)

    el = ET.fromstring(xmlstring)

    target_type = el.tag.upper() if target is None else target

    if target_type not in OPENEHR_TYPE_MAP:
        raise NotImplementedError(f"Could not decode object with type of \'{target_type}\' as it is either not yet supported or is not a valid openEHR type")
    
    py_cls : IXMLSupport = OPENEHR_TYPE_MAP[target_type]
    
    return py_cls.from_xml(el, terminology_service=terminology_service)
    