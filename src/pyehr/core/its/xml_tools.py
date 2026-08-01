import re
from typing import Optional, Union

import xml.etree.ElementTree as ET

from pyehr.core.its.xml import IXMLSupport, get_pyehr_type_from_element
from pyehr.term import PyehrGlobalTerminologyService

__all__ = ['from_arbitrary_xml', 'decode_xml', 'make_xml_text_element']


def from_arbitrary_xml(root: ET.Element,
                       target: Optional[str] = None,
                       terminology_service = None) -> Union[IXMLSupport, str]:
    """Deserialise an arbitrary element from XML.
    
    :param root: XML element at root of tree to decode.
    :param target: (Optional) Target type to decode the root element to (e.g. 'CODE_PHRASE')
    :param terminology_service: (Optional) Provide a terminology service, if not provided, uses the inbuilt pyehr terminology service.
    :type terminology_service: TerminologyService"""
    from pyehr.types import OPENEHR_TYPE_MAP

    if target is None:
        # attempt to extract the target type from underlying
        target = get_pyehr_type_from_element(root)
        if target is None:
            target = root.tag.upper()

    if ":string" in target:
        return root.text
    elif ":boolean" in target:
        return (root.text == "true")

    if target not in OPENEHR_TYPE_MAP:
        raise NotImplementedError(f"Could not decode object with type of \'{target}\' as it is either not yet supported or is not a valid openEHR type")
    
    py_cls : IXMLSupport = OPENEHR_TYPE_MAP[target]
    
    return py_cls.from_xml(root, term_svc=terminology_service)


def decode_xml(xml_str: str, 
               target: Optional[str] = None, 
               terminology_service = None) -> IXMLSupport:
    """Read an OpenEHR ITS XML string

    :param xml_str: OpenEHR ITS XML as a string
    :param target: (Optional) Target type to decode the root element to (e.g. 'CODE_PHRASE')
    :param terminology_service: (Optional) Provide a terminology service, if not provided, uses the inbuilt pyehr terminology service.
    :type terminology_service: TerminologyService"""

    if terminology_service is None:
        terminology_service = PyehrGlobalTerminologyService.get_global_terminology_service()

    # remove namespace to avoid a world of pain...
    xmlstring = re.sub(' xmlns="[^"]+"', '', xml_str, count=1)

    el = ET.fromstring(xmlstring)

    return from_arbitrary_xml(el, target, terminology_service)

def make_xml_text_element(element_name: str, value: str):
    el = ET.Element(element_name)
    el.text = value
    return el
    