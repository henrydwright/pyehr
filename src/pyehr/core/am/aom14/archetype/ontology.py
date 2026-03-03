
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.xml import IXMLSupport


class ArchetypeOntology(AnyClass, IXMLSupport):
    pass

class ArchetypeTerm(AnyClass, IXMLSupport):
    pass

class TermBindingSet(AnyClass, IXMLSupport):
    # defined in Archetype.xsd
    pass

class TermBindingItem(AnyClass, IXMLSupport):
    # defined in Archetype.xsd
    pass