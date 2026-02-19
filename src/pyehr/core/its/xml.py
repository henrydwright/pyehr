from abc import ABC, abstractmethod

from typing import Optional
import xml.etree.ElementTree as ET

class IXMLSupport(ABC):
    """Interface denoting that this pyehr class supports being serialised to,
    and de-serialised from, the XML (1.0.2) defined in OpenEHR ITS."""

    @abstractmethod
    def as_xml(self, root_tag: Optional[str] = None) -> ET.Element:
        """Output this class as an XML element (with children) compliant with XML v1.0.2 schema
        
        :param root_tag: Optionally, override the default root tag name (e.g. when
        a CODE_PHRASE is called 'language' use that rather than default)"""
        pass

    @abstractmethod
    def from_xml(root: ET.Element, **kwargs) -> 'IXMLSupport':
        """Deserialise a copy of this class from XML (ElementTree.Element).

        :param root: Root element of this class to deserialise. Root element name will be ignored.
        :param term_svc: Must pass a TerminologyService for those classes which require one on init"""
        pass


