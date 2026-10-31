"""Classes for working with AQL queries (both parsing and generating)"""

from abc import ABC, abstractmethod
from enum import StrEnum
from types import NoneType
from typing import Literal, Optional, Union

from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISOTime

class IAQLQueryNode(ABC):
    """Abstract notion of some node within an AQL query tree"""

    @abstractmethod
    def as_aql(self) -> str:
        """Returns the contents of this node as a valid AQL string"""

class AQLPrimitiveLiteral(IAQLQueryNode):
    """A primitive literal within an AQL query."""

    string_representation: str
    """String representation of the literal value, as written in the query"""

    value: Union[str, int, float, ISODate, ISOTime, ISODateTime, bool, NoneType]
    """Parsed python representation of the representation"""

    def __init__(self, string_representation: str, value: Union[str, int, float, ISODate, ISOTime, ISODateTime, bool, NoneType]):
        self.string_representation = string_representation
        self.value = value

    def as_aql(self):
        return self.string_representation

class AQLParameter(IAQLQueryNode):
    """Named parameter in an AQL query (e.g. $THRESHOLD)"""

    name: str
    """Name of the parameter before the $ sign"""

    def __init__(self, name: str):
        self.name = name

    def as_aql(self):
        return "$" + self.name

class AQLComparisonOperator(StrEnum):
    """Basic AQL comparison operators."""
    EQUAL = "="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL_TO = ">="
    SMALLER_THAN = "<"
    SMALLER_THAN_OR_EQUAL_TO = "<="
    NOT_EQUAL_TO = "!="

class AQLModelPath(IAQLQueryNode):
    """A simple path within a model without any predicates.
    
    e.g. `name/defining_code/code_string`"""

    path: str

    def __init__(self, path: str):
        self.path = path

    def split(self):
        return self.path.split("/")

    def as_aql(self):
        return self.path

class AQLPredicateTreeNode(IAQLQueryNode):
    """(Abstract) Node within an AQL predicate tree"""

    @abstractmethod
    def __init__(self):
        super().__init__()

class AQLPredicateTreeLeaf(AQLPredicateTreeNode):
    """Combination of a model path, an operator and a comparator value.
    
    e.g. `name/defining_code/code_string='313267000'`"""

    model_path: AQLModelPath
    """Path within the model referred to"""

    operator: AQLComparisonOperator
    """Operator within the expression"""

    comparator_value: Union[AQLPrimitiveLiteral, AQLModelPath, AQLParameter]
    """Value to compare the item at the model path to"""

    def __init__(self, model_path: AQLModelPath, operator: AQLComparisonOperator, comparator_value: Union[AQLPrimitiveLiteral, AQLModelPath, AQLParameter]):
        self.model_path = model_path
        self.operator = operator
        self.comparator_value = comparator_value

    def as_aql(self):
        return self.model_path.as_aql() + self.operator.value + self.comparator_value.as_aql()

class AQLPredicateTreeNonLeaf(AQLPredicateTreeNode):
    """Combination of two AQL predicate tree nodes combined with either AND or OR.
    
    e.g. `name/defining_code/code_string='at0003' and name/defining_code/terminology_id/value='local'`"""

    op1: AQLPredicateTreeNode
    """First operand"""

    operator: Union[Literal['AND'], Literal['OR']]
    """Operator between the two operands"""

    op2: AQLPredicateTreeNode
    """Second operand"""

    def __init__(self, op1: AQLPredicateTreeNode, operator: Union[Literal['AND'], Literal['OR']], op2: AQLPredicateTreeNode):
        if not (operator == "AND" or operator == "OR"):
            raise ValueError("Operator between two AQL predicate tree branches must be either AND, or OR")
        self.op1 = op1
        self.operator = operator
        self.op2 = op2

    def as_aql(self):
        return "(" + self.op1.as_aql() + ") " + self.operator + " (" + self.op2.as_aql() + ")"

class AQLModelType(IAQLQueryNode):
    """Represents a single model type.
    
    e.g. `COMPOSITION c [openEHR-EHR-COMPOSITION.referral.v1]`"""

    type_name: str
    """Type referred to by the model type, always in upper case (e.g. `COMPOSITION`)"""

    variable_name: Optional[str]
    """If provided, the variable name associated with the type in the match"""

    archetype_id_predicate: Optional[ArchetypeID]
    """If provided, the archetype ID that must be matched within the given type"""

    def __init__(self, type_name: str, variable_name: Optional[str] = None, archetype_id_predicate: Optional[ArchetypeID] = None):
        self.type_name = type_name
        self.variable_name = variable_name
        self.archetype_id_predicate = archetype_id_predicate

    def as_aql(self):
        ret = self.type_name
        if self.variable_name is not None:
            ret += " " + self.variable_name
        if self.archetype_id_predicate is not None:
            ret += " [" + self.archetype_id_predicate.value + "]"
        return ret

class AQLModelTypeTreeNode(IAQLQueryNode):
    """(Abstract) Represents a node in an AQL model type expression tree"""

    @abstractmethod
    def __init__(self):
        super().__init__()

class AQLModelTypeTreeBinaryExpr(AQLModelTypeTreeNode):
    """A binary operator within an AQL model type expression tree (either AND or OR)
    
    e.g. `(...) AND (...)`"""

    expr1: AQLModelTypeTreeNode
    """First operand"""

    operator: Union[Literal['AND'], Literal['OR']]
    """Either the value 'AND' or 'OR'"""

    expr2: AQLModelTypeTreeNode
    """Second operand"""

    def __init__(self, expr1: AQLModelTypeTreeNode, operator: Union[Literal['AND'], Literal['OR']], expr2: AQLModelTypeTreeNode):
        self.expr1 = expr1
        self.operator = operator
        self.expr2 = expr2

    def as_aql(self):
        return "(" + self.expr1.as_aql() + " " + self.operator + " " + self.expr2.as_aql() + ")"

class AQLModelTypeTreeNotExpr(AQLModelTypeTreeNode):
    """Represents NOT of an AQL model type tree expression
    
    e.g. `NOT (...)`"""

    expr: AQLModelTypeTreeNode
    """Expression being negated"""

    def __init__(self, expr: AQLModelTypeTreeNode):
        self.expr = expr

    def as_aql(self):
        return "(NOT " + self.expr.as_aql() + ")"

class AQLModelTypeTreeConstraint(AQLModelTypeTreeNode):
    """Represents the leaf of an expression constraint tree (either a model type or chain thereof)
    
    e.g. `EHR e CONTAINS (...)`"""

    model_type: AQLModelType
    """The model type (at the start of the chain, if this is a chain)"""

    negate_contains: bool
    """If there is a contains clause, is it negated"""

    contains: Optional[AQLModelTypeTreeNode]
    """The contained model type (expression) that must be matched"""

    def __init__(self, model_type: AQLModelType, negate_contains: bool = False, contains: Optional[AQLModelTypeTreeNode] = None):
        self.model_type = model_type
        self.negate_contains = negate_contains
        self.contains = contains

    def as_aql(self):
        ret = self.model_type.as_aql()
        if self.negate_contains:
            ret += " NOT"
        if self.contains is not None:
            ret += " CONTAINS " + self.contains.as_aql()
        return ret

class AQLDataMatchPathSegment(IAQLQueryNode):
    """Single segment within a data match path
    
    e.g. `/data[archetype_node_id=at0002 and name/defining_code/code_string='at0003' and name/defining_code/terminology_id/value='local']`"""

    attribute_id: str
    """Attribute within the path segment (e.g. /data[at0002] this would be 'data')"""

    predicate_string: Optional[str]
    """Original string representation of the predicate (e.g. \"at0001, 'some name value'\").
    
    This exists because on parsing, all predicates are converted to a standard non-shortcut form."""

    predicate_tree: Optional[AQLPredicateTreeNode]
    """Parsed representation of the predicate for this segment of the path"""

    def __init__(self, attribute_id: str, predicate_string: Optional[str] = None, predicate_tree: Optional[AQLPredicateTreeNode] = None):
        self.attribute_id = attribute_id
        self.predicate_string = predicate_string
        self.predicate_tree = predicate_tree

    def as_aql(self):
        ret = "/" + self.attribute_id
        if self.predicate_string is not None:
            ret += "[" + self.predicate_string + "]"
        return ret

class AQLDataMatchPath(IAQLQueryNode):
    """Identifies part of an archetyped object (from the FROM clause) to return
    which may need to match certain inline predicates.
    
    e.g. `o/data[at0001, 'some name value']/.../data[at0003]/items[at0004]/value/value`"""

    variable_name: str
    """The name of the variable to which the path pertains"""

    path_segments: Optional[list[AQLDataMatchPathSegment]]
    """Path within a the variable referred to, if provided"""

    def __init__(self, variable_name: str, path_segments: Optional[list[AQLDataMatchPathSegment]] = None):
        self.variable_name = variable_name
        self.path_segments = path_segments

    def as_aql(self):
        ret = self.variable_name
        if self.path_segments is not None:
            ret += "".join([path_segment.as_aql() for path_segment in self.path_segments])
        return ret


class AQLFunctionCall(IAQLQueryNode):
    """Abstract parent of all AQL function calls"""

    name: str
    """The name of the function (part before arguments) in upper-case.
    
    e.g. for CURRRENT_DATE_TIME() this would be 'CURRENT_DATE_TIME'"""

    args: list[Union[AQLDataMatchPath, AQLPrimitiveLiteral, 'AQLFunctionCall', AQLParameter]]
    """Arguments contained within the function call"""

    def __init__(self, function_name: str, function_args: list[Union[AQLDataMatchPath, AQLPrimitiveLiteral, 'AQLFunctionCall', AQLParameter]]):
        self.name = function_name
        self.args = function_args

    @abstractmethod
    def evaluate(self) -> AQLPrimitiveLiteral:
        """Evaluate the function with name and arguments."""
        pass

    def as_aql(self):
        return self.name + "(" + ",".join([arg.as_aql() for arg in self.args]) + ")"

class AQLColumnSpec(IAQLQueryNode):
    """Specification for a single column to be returned from a SELECT clause"""

    value: Union[AQLDataMatchPath, AQLFunctionCall, AQLPrimitiveLiteral]
    """Value selected out of the data to form each row of this column."""

    alias: Optional[str]
    """Optional, human friendly name for the column"""

    def __init__(self, value: Union[AQLDataMatchPath, AQLFunctionCall, AQLPrimitiveLiteral], alias: Optional[str] = None):
        self.value = value
        self.alias = alias

    def as_aql(self):
        ret = self.value.as_aql()
        if self.alias is not None:
            ret += " AS " + self.alias
        return ret

class AQLSelectClause(IAQLQueryNode):
    """A SELECT clause specifies what data is to be retrieved by the AQL query. The data can 
    be any types from RM or any built-in data types (see Section 3.12)."""

    distinct: bool
    """Specifies whether duplicate rows should be filtered out from result set.

    By default, an AQL query returns all data items selected by the FROM and WHERE clauses 
    as rows in the result set. A row is considered to be duplicated in the result set if there 
    is at least one other row with the same value for each corresponding column expression.
    DISTINCT specifies removal of all such duplicate rows from the result set."""

    top: Optional[tuple[int, bool]]
    """DEPRECATED: The TOP syntax was borrowed from SQL language for representing the number 
    of result sets that should be returned by the AQL query. It uses BACKWARD and FORWARD to 
    indicate the direction where to start to get the number of results to be returned.
    
    In this representation, the boolean part is True for FORWARD and False for BACKWARD."""

    result_columns: list[AQLColumnSpec]
    """List of columns to be returned by the query selected out of the data gathered in the FROM
    and WHERE stages.
    
    A column expression is formed by an identified path, a function, a literal value or 
    plain variable name defined in the FROM clause. Where a variable name is specified, 
    the full object of the type associated with the variable is retrieved, such as a 
    COMPOSITION, OBSERVATION etc. Where a function is specified, the call has to be done 
    using the specified arguments, and the results are returned. Where an identified path 
    is specified, the data item(s) having that archetype path are returned.

    Each column expression may have a name alias renaming the associated data. When the SELECT 
    clause contains multiple column expressions, they are separated using a comma."""

    def __init__(self, result_columns: list[AQLColumnSpec], distinct: bool = False, top: Optional[tuple[int, bool]] = None):
        self.result_columns = result_columns
        self.distinct = distinct
        self.top = top

    def as_aql(self):
        ret = "SELECT "
        if self.distinct:
            ret += "DISTINCT "
        if self.top is not None:
            ret += str(self.top[0]) + (" FORWARD " if self.top[1] else " BACKWARD ")
        ret += ", ".join([result_column.as_aql() for result_column in self.result_columns])
        return ret


class AQLFromClause(IAQLQueryNode):
    """The FROM clause is used to specify the subset of all the data available in a repository, 
    that will be available for the rest of the clauses to filter and return specific data (WHERE, 
    SELECT, etc)."""

    model_type_constraint: AQLModelTypeTreeConstraint
    """The constraint on model type, including variable bindings, to be applied."""

    def __init__(self, model_type_constraint: AQLModelTypeTreeConstraint):
        self.model_type_constraint = model_type_constraint

    def as_aql(self):
        return "FROM " + self.model_type_constraint.as_aql()

class AQLWhereClause(IAQLQueryNode):
    pass

class AQLOrderByClause(IAQLQueryNode):
    pass

class AQLLimitClause(IAQLQueryNode):
    pass

class AQLQuery(IAQLQueryNode):
    """A valid AQL query that can be executed"""

    select_clause: AQLSelectClause

    from_clause: AQLFromClause

    where_clause: Optional[AQLWhereClause]

    orderby_clause: Optional[AQLOrderByClause]

    limit_clause: Optional[AQLLimitClause]

    def __init__(self, 
                 select_clause: AQLSelectClause, 
                 from_clause: AQLFromClause, 
                 where_clause: Optional[AQLWhereClause] = None,
                 orderby_clause: Optional[AQLOrderByClause] = None,
                 limit_clause: Optional[AQLLimitClause] = None):
        self.select_clause = select_clause
        self.from_clause = from_clause
        self.where_clause = where_clause
        self.orderby_clause = orderby_clause
        self.limit_clause = limit_clause

    def as_aql(self):
        ret = self.select_clause.as_aql() + "\n" + self.from_clause.as_aql()
        if self.where_clause is not None:
            ret += "\n" + self.where_clause.as_aql()
        if self.orderby_clause is not None:
            ret += "\n" + self.orderby_clause.as_aql()
        if self.limit_clause is not None:
            ret += "\n" + self.limit_clause.as_aql()
        return ret

def select() -> AQLSelectClause:
    pass