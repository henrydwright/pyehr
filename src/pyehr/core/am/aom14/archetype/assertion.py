
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.xml import IXMLSupport


class Assertion(AnyClass, IXMLSupport):
    """Structural model of a typed first order predicate logic assertion, in the form of an expression tree, including optional variable definitions."""