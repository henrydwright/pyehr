"""Assertions are expressed in archetypes in typed first-order predicate 
logic (FOL). They are used in two places: to express archetype slot constraints, 
and to express rules in complex object constraints. In both of these places, 
their role is to constrain something inside the archetype."""

from abc import abstractmethod
from enum import Enum
from typing import Optional, Union
import xml.etree.ElementTree as ET

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.xml import IXMLSupport, get_pyehr_type_from_element
from pyehr.core.its.xml_tools import from_arbitrary_xml

__all__ = ['ExprItem', 'ExprLeaf', 'OperatorKind', 'ExprOperator', 'ExprUnaryOperator', 'ExprBinaryOperator', 'AssertionVariable', 'Assertion']


class ExprItem(AnyClass, IXMLSupport):
    """Abstract parent of all expression tree items."""
    
    type_var: str
    """Type name of this item in the mathematical sense. For leaf nodes, must 
    be the name of a primitive type, or else a reference model type. The type 
    for any relational or boolean operator will be “Boolean”, while the type 
    for any arithmetic operator, will be “Real” or “Integer”."""

    @abstractmethod
    def __init__(self, type_var: str, **kwargs):
        self.type_var = type_var
        super().__init__(**kwargs)

    def is_equal(self, other: 'ExprItem'):
        return (type(self) == type(other) and
                self.type_var == other.type_var)
    
    @abstractmethod
    def as_json(self):
        return {
            "type": self.type_var
        }
    
    @abstractmethod
    def as_xml(self, root_tag = None):
        root = ET.Element("expr_item" if root_tag is None else root_tag)
        typ_el = ET.Element("type")
        typ_el.text = self.type_var
        root.append(typ_el)
        return root
    
    @staticmethod
    def extract_xml_elements(root: ET.Element, **kwargs) -> str:
        """Extract 'type' from EXPR_ITEM xml"""
        type_var = root.findtext("./type")
        return type_var
    
    def from_xml(root, **kwargs):
        typ = get_pyehr_type_from_element(root)
        if typ == "EXPR_LEAF":
            return ExprLeaf.from_xml(root, **kwargs)
        elif typ == "EXPR_UNARY_OPERATOR":
            return ExprUnaryOperator.from_xml(root, **kwargs)
        elif typ == "EXPR_BINARY_OPERATOR":
            return ExprBinaryOperator.from_xml(root, **kwargs)
        else:
            raise TypeError(f"Expected subtype of EXPR_ITEM but found \'{typ}\'.")

class ExprLeaf(ExprItem):
    """Expression tree leaf item representing one of:
        * a manifest constant of any primitive type;
        * a path referring to a value in the archetype;
        * a constraint;
        * a variable reference."""
    
    reference_type: str
    """Type of reference: “constant”, “attribute”, “function”, “constraint”. 
    The first three are used to indicate the referencing mechanism for an 
    operand. The last is used to indicate a constraint operand, as happens 
    in the case of the right-hand operand of the 'matches' operator."""

    item: Union[AnyClass, str, bool]
    """The value referred to; a manifest constant, an attribute path (in 
    the form of a String), or for the right-hand side of a 'matches' node, 
    a constraint, often a C_PRIMITIVE_OBJECT."""

    def __init__(self, type_var: str, reference_type: str, item: AnyClass, **kwargs):
        """Expression tree leaf item representing one of:
        * a manifest constant of any primitive type;
        * a path referring to a value in the archetype;
        * a constraint;
        * a variable reference.

        :param reference_type: Either 'constant', 'attribute', 'function' or 'constraint'"""
        self.reference_type = reference_type
        self.item = item
        super().__init__(type_var, **kwargs)

    def is_equal(self, other: 'ExprLeaf'):
        return (super().is_equal(other) and
                self.reference_type == other.reference_type and
                is_equal_value(self.item, other.item))
    
    def as_json(self):
        draft = super().as_json()
        draft["reference_type"] = self.reference_type
        if isinstance(self.item, AnyClass):
            draft["item"] = self.item.as_json()
        else:
            draft["item"] = str(self.item)
            
        draft["_type"] = "EXPR_LEAF"
        return draft
    
    def as_xml(self, root_tag=None):
        draft = super().as_xml("expr_leaf" if root_tag is None else root_tag)

        if isinstance(self.item, IXMLSupport):
            it_xml = self.item.as_xml("item")
            it_xml.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
            it_xml.attrib["xsi:type"] = self.item.as_json()["_type"]
            draft.append(it_xml)
        else:
            it_el = ET.Element("item")
            it_el.attrib["xmlns:xsd"] = "http://www.w3.org/2001/XMLSchema"
            it_el.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
            if isinstance(self.item, bool):
                it_el.attrib["xsi:type"] = "xsd:boolean"
                it_el.text = str(self.item).lower()
            else:
                it_el.attrib["xsi:type"] = "xsd:string"
                it_el.text = str(self.item)
            draft.append(it_el)

        ref_el = ET.Element("reference_type")
        ref_el.text = self.reference_type
        draft.append(ref_el)

        draft.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        draft.attrib["xsi:type"] = "EXPR_LEAF"

        return draft
    
    def from_xml(root: ET.Element, **kwargs):
        typ = ExprItem.extract_xml_elements(root)
        ref_typ = root.findtext("./reference_type")
        it = from_arbitrary_xml(root.find("./item"))
        return ExprLeaf(typ, ref_typ, it)    

class OperatorKind(Enum):

    EQUALS = "op_eq"
    """Equals operator (= or ==)"""

    NOT_EQUAL = "op_ne"
    """Not equals operator (!= or /=)"""

    LESS_THAN_OR_EQUAL = "op_le"
    """Less-than or equals operator (<=)"""

    LESS_THAN = "op_lt"
    """Less-than operator (<=)"""

    GREATER_THAN_OR_EQUAL = "op_ge"
    """Greater-than or equals operator (>=)"""

    GREATER_THAN = "op_gt"
    """Greater-than operator (>)"""

    MATCHES = "op_matches"
    """Matches operator (matches or is_in)"""

    NOT = "op_not"
    """Not logical operator"""

    AND = "op_and"
    """And logical operator"""

    OR = "op_or"
    """Or logical operator"""

    XOR = "op_xor"
    """Xor logical operator"""

    IMPLIES = "op_implies"
    """Implies logical operator"""

    FOR_ALL = "op_for_all"
    """For-all (universal) quantifier"""

    EXISTS = "op_exists"
    """Exists quantifier"""

    PLUS = "op_plus"
    """Arithmetic plus operator (+)"""

    MINUS = "op_minus"
    """Arithmetic minus operator (-)"""

    MULTIPLY = "op_multiply"
    """Arithmetic multiplication operator (*)"""

    DIVIDE = "op_divide"
    """Arithmetic division operator (/)"""

    EXPONENT = "op_exponent"
    """Arithmetic exponentiation operator (^)"""

    def as_xml(self, root_tag = None):
        root = ET.Element("operator_kind" if root_tag is None else root_tag)
        map_dict = {
            OperatorKind.EQUALS: "2001",
            OperatorKind.NOT_EQUAL: "2002",
            OperatorKind.LESS_THAN_OR_EQUAL: "2003",
            OperatorKind.LESS_THAN: "2004",
            OperatorKind.GREATER_THAN_OR_EQUAL: "2005",
            OperatorKind.GREATER_THAN: "2006",
            OperatorKind.MATCHES: "2007",
            OperatorKind.NOT: "2010",
            OperatorKind.AND: "2011",
            OperatorKind.OR: "2012",
            OperatorKind.XOR: "2013",
            OperatorKind.IMPLIES: "2014",
            OperatorKind.FOR_ALL: "2015",
            OperatorKind.EXISTS: "2016",
            OperatorKind.PLUS: "2020",
            OperatorKind.MINUS: "2021",
            OperatorKind.MULTIPLY: "2022",
            OperatorKind.DIVIDE: "2023",
            OperatorKind.EXPONENT: "2024"
        }
        root.text = map_dict[self]
        return root
    
    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        map_dict = {
            "2001": OperatorKind.EQUALS,
            "2002": OperatorKind.NOT_EQUAL,
            "2003": OperatorKind.LESS_THAN_OR_EQUAL,
            "2004": OperatorKind.LESS_THAN,
            "2005": OperatorKind.GREATER_THAN_OR_EQUAL,
            "2006": OperatorKind.GREATER_THAN,
            "2007": OperatorKind.MATCHES,
            "2010": OperatorKind.NOT,
            "2011": OperatorKind.AND,
            "2012": OperatorKind.OR,
            "2013": OperatorKind.XOR,
            "2014": OperatorKind.IMPLIES,
            "2015": OperatorKind.FOR_ALL,
            "2016": OperatorKind.EXISTS,
            "2020": OperatorKind.PLUS,
            "2021": OperatorKind.MINUS,
            "2022": OperatorKind.MULTIPLY,
            "2023": OperatorKind.DIVIDE,
            "2024": OperatorKind.EXPONENT
        }
        return map_dict[root.text]

class ExprOperator(ExprItem):
    """Abstract parent of operator types."""

    precedence_overridden: bool
    """True if the natural precedence of operators is overridden in the 
    expression represented by this node of the expression tree. If True, 
    parentheses should be introduced around the totality of the syntax 
    expression corresponding to this operator node and its operands."""
    # in spec this is cardinality 0..1 but here it is 1..1 to match xml spec

    operator: OperatorKind
    """Code of operator"""

    @abstractmethod
    def __init__(self, type_var: str, operator: OperatorKind, precedence_overridden: bool = False, **kwargs):
        self.operator = operator
        self.precedence_overridden = precedence_overridden
        super().__init__(type_var, **kwargs)

    def is_equal(self, other: 'ExprOperator'):
        return (super().is_equal(other) and
                is_equal_value(self.precedence_overridden, other.precedence_overridden) and
                is_equal_value(self.operator, other.operator))
    
    @abstractmethod
    def as_json(self):
        draft = super().as_json()
        draft["operator"] = str(self.operator.value)
        draft["precedence_overridden"] = self.precedence_overridden
        return draft
    
    @abstractmethod
    def as_xml(self, root_tag=None):
        draft = super().as_xml("expr_operator" if root_tag is None else root_tag)
        draft.append(self.operator.as_xml("operator"))
        prec_el = ET.Element("precedence_overridden")
        prec_el.text = str(self.precedence_overridden).lower()
        draft.append(prec_el)
        return draft
    
    @staticmethod
    def extract_xml_elements(root, **kwargs) -> tuple[str, OperatorKind, Optional[bool]]:
        """Extract (type, operator and precedence_overridden) from xml"""
        typ = ExprItem.extract_xml_elements(root, **kwargs)
        ok = OperatorKind.from_xml(root.find("./operator"))
        po = (root.findtext("./precedence_overridden") == "true")
        return (typ, ok, po)
                
class ExprUnaryOperator(ExprOperator):
    """Unary operator expression node."""

    operand: ExprItem
    """Operand node."""

    def __init__(self, type_var: str, operator: OperatorKind, operand: ExprItem, precedence_overridden: bool = False, **kwargs):
        self.operand = operand
        super().__init__(type_var, operator, precedence_overridden, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.operand, other.operand))
    
    def as_json(self):
        draft = super().as_json()
        draft["operand"] = self.operand.as_json()
        draft["_type"] = "EXPR_UNARY_OPERATOR"
        return draft

    def as_xml(self, root_tag=None):
        draft = super().as_xml("expr_unary_operator" if root_tag is None else root_tag)
        draft.append(self.operand.as_xml("operand"))

        draft.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        draft.attrib["xsi:type"] = "EXPR_UNARY_OPERATOR"

        return draft
    
    def from_xml(root, **kwargs):
        typ, ok, po = ExprOperator.extract_xml_elements(root)
        op = ExprItem.from_xml(root.find("./operand"))
        return ExprUnaryOperator(typ, ok, op, po)
    
class ExprBinaryOperator(ExprOperator):
    """Binary operator expression node."""

    left_operand: ExprItem
    """Left operand node."""

    right_operand: ExprItem
    """Right operand node."""

    def __init__(self, type_var: str, left_operand: ExprItem, operator: OperatorKind, right_operand: ExprItem, precedence_overridden: bool = False, **kwargs):
        self.left_operand = left_operand
        self.right_operand = right_operand
        super().__init__(type_var, operator, precedence_overridden, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.left_operand, other.left_operand) and
                is_equal_value(self.right_operand, other.right_operand))
    
    def as_json(self):
        draft = super().as_json()
        draft["left_operand"] = self.left_operand.as_json()
        draft["right_operand"] = self.right_operand.as_json()
        draft["_type"] = "EXPR_BINARY_OPERATOR"
        return draft

    def as_xml(self, root_tag=None):
        draft = super().as_xml("expr_binary_operator" if root_tag is None else root_tag)
        draft.append(self.left_operand.as_xml("left_operand"))
        draft.append(self.right_operand.as_xml("right_operand"))

        draft.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        draft.attrib["xsi:type"] = "EXPR_BINARY_OPERATOR"
        return draft

    def from_xml(root, **kwargs):
        typ, ok, po = ExprOperator.extract_xml_elements(root)
        l_op = ExprItem.from_xml(root.find("./left_operand"))
        r_op = ExprItem.from_xml(root.find("./right_operand"))
        return ExprBinaryOperator(typ, l_op, ok, r_op, po)

class AssertionVariable(AnyClass, IXMLSupport):
    """Definition of a named variable used in an assertion expression."""
    
    name: str
    """Name of variable"""

    definition: str
    """Formal definition of the variable."""

    def __init__(self, name: str, definition: str, **kwargs):
        self.name = name
        self.definition = definition
        super().__init__(**kwargs)

    def is_equal(self, other: 'AssertionVariable'):
        return (type(self) == type(other) and
                self.name == other.name and
                self.definition == other.definition)
    
    def as_json(self):
        return {
            "name": self.name,
            "definition": self.definition,
            "_type": "ASSERTION_VARIABLE"
        }
    
    def as_xml(self, root_tag = None):
        root = ET.Element("assertion_variable" if root_tag is None else root_tag)
        name_el = ET.Element("name")
        name_el.text = self.name
        root.append(name_el)
        def_el = ET.Element("definition")
        def_el.text = self.definition
        root.append(def_el)
        return root
    
    def from_xml(root: ET.Element, **kwargs):
        name = root.findtext("./name")
        definition = root.findtext("./definition")
        return AssertionVariable(name, definition)
    

class Assertion(AnyClass, IXMLSupport):
    """Structural model of a typed first order predicate logic assertion, in the 
    form of an expression tree, including optional variable definitions."""

    tag: Optional[str]
    """Expression tag, used for differentiating multiple assertions."""

    string_expression: Optional[str]
    """String form of expression, in case an expression evaluator taking String 
    expressions is used for evaluation."""

    expression: ExprItem
    """Root of expression tree."""

    variables: Optional[list[AssertionVariable]]
    """Definitions of variables used in the assertion expression."""

    def __init__(self, expression: ExprItem, tag: Optional[str] = None, string_expression: Optional[str] = None, variables: Optional[list[AssertionVariable]] = None, **kwargs):
        self.expression = expression
        if tag is not None and tag == "":
            raise ValueError("If provided, tag cannot be empty (invariant: tag_valid)")
        self.tag = tag
        self.string_expression = string_expression
        self.variables = variables
        super().__init__(**kwargs)

    def as_xml(self, root_tag = None):
        root = ET.Element("assertion" if root_tag is None else root_tag)
        if self.tag is not None:
            tag_el = ET.Element("tag")
            tag_el.text = self.tag
            root.append(tag_el)
        if self.string_expression is not None:
            se_el = ET.Element("string_expression")
            se_el.text = self.string_expression
            root.append(se_el)
        root.append(self.expression.as_xml("expression"))
        if self.variables is not None:
            (root.append(var.as_xml("variables")) for var in self.variables)
        return root
    
    def from_xml(root: ET.Element, **kwargs):
        tag = root.findtext("./tag")
        string_expression = root.findtext("./string_expression")
        exp = ExprItem.from_xml(root.find("./expression"))
        var_els = root.findall("./variables")
        vars = None
        if len(var_els) > 0:
            vars = [AssertionVariable.from_xml(var_el) for var_el in var_els]
        return Assertion(exp, tag, string_expression, vars)

    def as_json(self):
        draft = {
            "expression": self.expression.as_json()
        }
        if self.tag is not None:
            draft["tag"] = self.tag
        if self.string_expression is not None:
            draft["string_expression"] = self.string_expression
        if self.variables is not None:
            draft["variables"] = [var.as_json() for var in self.variables]
        draft["_type"] = "ASSERTION"
        return draft
    
    def is_equal(self, other: 'Assertion'):
        return (type(self) == type(other) and
                is_equal_value(self.tag, other.tag) and
                is_equal_value(self.string_expression, other.string_expression) and
                is_equal_value(self.expression, other.expression) and
                is_equal_value(self.variables, other.variables))