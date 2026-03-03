import xml.etree.ElementTree as ET

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.xml import IXMLSupport


class Assertion(AnyClass, IXMLSupport):
    """Structural model of a typed first order predicate logic assertion, in the 
    form of an expression tree, including optional variable definitions."""

    def as_xml(self, root_tag = None):
        return ET.Element("assertion")
    
    def from_xml(root, **kwargs):
        return Assertion()
    
    def as_json(self):
        return {"_type": "ASSERTION"}
    
    def is_equal(self, other):
        return True