"""Methods and classes for handling Archetype Query Language (AQL)."""

from ast import literal_eval
from typing import Optional, Union

from antlr4 import CommonTokenStream, InputStream, ParserRuleContext
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNode

from pyehr.core.base.base_types.identification import ArchetypeID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISOTime
from pyehr.core.its.aql.query import (
    AQLArithmeticExprBinaryExpr,
    AQLArithmeticExprLeaf,
    AQLArithmeticOperator,
    AQLAggregateCountFunction,
    AQLAggregateFunctionCall,
    AQLAggregateMathFunction,
    AQLColumnSpec,
    AQLComparisonOperand,
    AQLComparisonOperator,
    AQLDataMatchPath,
    AQLDataMatchPathSegment,
    AQLFunctionCall,
    AQLFromClause,
    AQLLimitClause,
    AQLModelPath,
    AQLModelType,
    AQLModelTypeTreeBinaryExpr,
    AQLModelTypeTreeConstraint,
    AQLModelTypeTreeNotExpr,
    AQLOrderByClause,
    AQLOrderByExpr,
    AQLParameter,
    AQLPredicateTreeLeaf,
    AQLPredicateTreeNonLeaf,
    AQLPrimitiveLiteral,
    AQLQuery,
    AQLSelectClause,
    AQLWhereClause,
    AQLWhereTreeBinaryExpr,
    AQLWhereTreeComparisonLeaf,
    AQLWhereTreeExistsLeaf,
    AQLWhereTreeLikeLeaf,
    AQLWhereTreeMatchesLeaf,
    AQLWhereTreeNotExpr,
)
from pyehr.core.lang.AqlLexer import AqlLexer
from pyehr.core.lang.AqlParserPyehr import AqlParserPyehr


class AQLParseError(ValueError):
    """Raised when an AQL string is invalid or cannot be represented."""


class _ParseErrorListener(ErrorListener):
    def __init__(self):
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, exception):
        self.errors.append(f"line {line}:{column} {msg}")


def _rule_name(ctx: ParserRuleContext) -> str:
    return ctx.parser.ruleNames[ctx.getRuleIndex()]


def _children_of_rule(ctx: ParserRuleContext, name: str) -> list[ParserRuleContext]:
    return [
        child
        for child in ctx.children or []
        if isinstance(child, ParserRuleContext) and _rule_name(child) == name
    ]


def _first_child_of_rule(ctx: ParserRuleContext, name: str) -> Optional[ParserRuleContext]:
    children = _children_of_rule(ctx, name)
    return children[0] if children else None


def _source_text(ctx: ParserRuleContext) -> str:
    start = ctx.start
    stop = ctx.stop
    input_stream = start.getInputStream()
    return input_stream.strdata[start.start : stop.stop + 1]


def _quoted_value(text: str) -> str:
    try:
        value = literal_eval(text)
    except (SyntaxError, ValueError) as exc:
        raise AQLParseError(f"Invalid AQL string literal {text!r}") from exc
    if not isinstance(value, str):
        raise AQLParseError(f"Expected a string literal, got {text!r}")
    return value


def _numeric_value(text: str) -> Union[int, float]:
    if any(char in text for char in ".eE"):
        return float(text)
    return int(text)


def _literal_from_token(token) -> AQLPrimitiveLiteral:
    text = token.text
    token_type = token.type
    if token_type == AqlParserPyehr.STRING:
        value: Union[str, int, float, ISODate, ISOTime, ISODateTime, bool, None] = _quoted_value(text)
    elif token_type in (AqlParserPyehr.INTEGER, AqlParserPyehr.SCI_INTEGER,
                         AqlParserPyehr.REAL, AqlParserPyehr.SCI_REAL):
        value = _numeric_value(text)
    elif token_type == AqlParserPyehr.BOOLEAN:
        value = text.lower() == "true"
    elif token_type == AqlParserPyehr.SYM_NULL:
        value = None
    elif token_type in (AqlParserPyehr.DATE_STRING, AqlParserPyehr.TIME_STRING,
                         AqlParserPyehr.DATE_TIME_STRING):
        date_time_value = _quoted_value(text)
        if token_type == AqlParserPyehr.DATE_STRING:
            value = ISODate(date_time_value)
        elif token_type == AqlParserPyehr.TIME_STRING:
            value = ISOTime(date_time_value)
        else:
            value = ISODateTime(date_time_value)
    else:
        raise AQLParseError(f"Unsupported AQL literal {text!r}")
    return AQLPrimitiveLiteral(text, value)


def _literal(ctx: ParserRuleContext) -> AQLPrimitiveLiteral:
    if _rule_name(ctx) == "primitiveLiteral":
        numeric = ctx.numericLiteral()
        if numeric is not None:
            text = numeric.getText()
            return AQLPrimitiveLiteral(text, _numeric_value(text))
        date_time = ctx.aqlDateTimeLiteral()
        if date_time is not None:
            return _literal(date_time)
        for child in ctx.children or []:
            if isinstance(child, TerminalNode):
                return _literal_from_token(child.symbol)
    elif _rule_name(ctx) == "numericLiteral":
        text = ctx.getText()
        return AQLPrimitiveLiteral(text, _numeric_value(text))
    elif _rule_name(ctx) == "aqlDateTimeLiteral":
        for child in ctx.children or []:
            if isinstance(child, TerminalNode):
                return _literal_from_token(child.symbol)
    elif _rule_name(ctx) in ("integerValue", "realValue"):
        text = ctx.getText()
        return AQLPrimitiveLiteral(text, _numeric_value(text))
    elif _rule_name(ctx) == "durationValue":
        text = ctx.getText()
        return AQLPrimitiveLiteral(text, text)
    raise AQLParseError(f"Unsupported AQL literal {ctx.getText()!r}")


def _data_match_path(ctx: ParserRuleContext) -> AQLDataMatchPath:
    segments = [_data_match_path_segment(segment) for segment in ctx.dataMatchPathSegment()]
    return AQLDataMatchPath(ctx.variableName.text, segments)


def _data_match_path_segment(ctx: ParserRuleContext) -> AQLDataMatchPathSegment:
    predicate = ctx.dataMatchPathPredicate()
    if predicate is None:
        return AQLDataMatchPathSegment(ctx.attributeId.text)
    predicate_tree = _data_match_path_predicate(predicate)
    return AQLDataMatchPathSegment(
        ctx.attributeId.text,
        _source_text(predicate),
        predicate_tree,
    )


def _model_path(ctx: ParserRuleContext) -> AQLModelPath:
    return AQLModelPath(ctx.getText())


def _comparison_operator(ctx: ParserRuleContext) -> AQLComparisonOperator:
    operators = {
        "=": AQLComparisonOperator.EQUAL,
        "!=": AQLComparisonOperator.NOT_EQUAL_TO,
        ">": AQLComparisonOperator.GREATER_THAN,
        ">=": AQLComparisonOperator.GREATER_THAN_OR_EQUAL_TO,
        "<": AQLComparisonOperator.SMALLER_THAN,
        "<=": AQLComparisonOperator.SMALLER_THAN_OR_EQUAL_TO,
    }
    operator = ctx.getText()
    try:
        return operators[operator]
    except KeyError as exc:
        raise AQLParseError(f"Unsupported AQL comparison operator {operator!r}") from exc


def _data_match_path_predicate(ctx: ParserRuleContext):
    base = ctx.adlPathPredicate()
    tree = None
    if base.archetypeIdPredicate() is not None:
        archetype_id = base.archetypeIdPredicate().getText()
        tree = AQLPredicateTreeLeaf(
            AQLModelPath("archetype_node_id"),
            AQLComparisonOperator.EQUAL,
            AQLPrimitiveLiteral(f"'{archetype_id}'", archetype_id),
        )
    elif base.idCode() is not None:
        code = base.idCode().getText()
        tree = AQLPredicateTreeLeaf.at_code_shortcut(code)

    value_predicate = ctx.dataMatchPathValuePredicate()
    if value_predicate is not None:
        value_tree = _data_match_path_value_predicate(value_predicate)
        tree = value_tree if tree is None else AQLPredicateTreeNonLeaf(tree, "AND", value_tree)
    return tree


def _data_match_path_value_predicate(ctx: ParserRuleContext):
    operands = _children_of_rule(ctx, "dataMatchPathValuePredicate")
    if len(operands) == 2:
        operator = next(
            child.getText()
            for child in ctx.children or []
            if isinstance(child, TerminalNode) and child.getText().upper() in ("AND", "OR")
        )
        return AQLPredicateTreeNonLeaf(
            _data_match_path_value_predicate(operands[0]),
            operator.upper(),
            _data_match_path_value_predicate(operands[1]),
        )

    nested = _first_child_of_rule(ctx, "dataMatchPathValuePredicate")
    if nested is not None:
        return _data_match_path_value_predicate(nested)

    model_path = ctx.modelPath()
    comparator_ctx = ctx.modelPathComparatorValue()
    if comparator_ctx.primitiveLiteral() is not None:
        comparator = _literal(comparator_ctx.primitiveLiteral())
    elif comparator_ctx.modelPath() is not None:
        comparator = _model_path(comparator_ctx.modelPath())
    else:
        comparator = AQLParameter(comparator_ctx.PARAMETER().getText()[1:])
    return AQLPredicateTreeLeaf(
        _model_path(model_path),
        _comparison_operator(ctx.comparisonOperator()),
        comparator,
    )


def _value(ctx: ParserRuleContext):
    path = ctx.dataMatchPath()
    if path is not None:
        return _data_match_path(path)
    primitive = ctx.primitiveLiteral()
    if primitive is not None:
        return _literal(primitive)
    function = ctx.functionCall()
    if function is not None:
        return _function_call(function)
    parameter = ctx.PARAMETER()
    if parameter is not None:
        return AQLParameter(parameter.getText()[1:])
    raise AQLParseError(f"Unsupported AQL value {ctx.getText()!r}")


def _function_call(ctx: ParserRuleContext) -> AQLFunctionCall:
    terminology = ctx.terminologyFunctionCall()
    if terminology is not None:
        return _terminology_function_call(terminology)

    arguments = ctx.functionArgs()
    args = [] if arguments is None else [_value(value) for value in arguments.value()]
    built_in = ctx.builtInFunction()
    if built_in is not None:
        name = built_in.getText()
    else:
        name = ctx.LC_ID().getText()
    return AQLFunctionCall(name.upper(), args)


def _terminology_function_call(ctx: ParserRuleContext) -> AQLFunctionCall:
    strings = ctx.STRING()
    args = [
        _literal_from_token(strings[0].symbol),
        _literal_from_token(strings[1].symbol),
    ]
    string_function = ctx.stringFunction()
    if string_function is None:
        args.append(_literal_from_token(strings[2].symbol))
    else:
        args.append(AQLFunctionCall(
            string_function.getText().upper(),
            [_value(value) for value in ctx.functionArgs().value()],
        ))
    return AQLFunctionCall("TERMINOLOGY", args)


def _comparison_operand(ctx: ParserRuleContext) -> AQLComparisonOperand:
    value = ctx.value()
    if value is not None:
        return AQLComparisonOperand(_value(value))
    return AQLComparisonOperand(_arithmetic_expr(ctx.arithmeticExpr()))


def _arithmetic_expr(ctx: ParserRuleContext):
    operands = _children_of_rule(ctx, "arithmeticExpr")
    if len(operands) == 2:
        operator_text = next(
            child.getText()
            for child in ctx.children or []
            if isinstance(child, TerminalNode)
            and child.getText() in ("^", "/", "*", "%", "+", "-")
        )
        return AQLArithmeticExprBinaryExpr(
            _arithmetic_expr(operands[0]),
            AQLArithmeticOperator(operator_text),
            _arithmetic_expr(operands[1]),
        )

    leaf = ctx.arithmeticLeaf()
    return _arithmetic_leaf(leaf)


def _arithmetic_leaf(ctx: ParserRuleContext):
    arithmetic_literal = ctx.arithmeticLiteral()
    if arithmetic_literal is not None:
        literal_ctx = next(
            child for child in arithmetic_literal.children
            if isinstance(child, ParserRuleContext)
        )
        return AQLArithmeticExprLeaf(_literal(literal_ctx))

    value = ctx.value()
    if value is not None:
        decoded = _value(value)
        if isinstance(decoded, AQLParameter):
            return AQLArithmeticExprLeaf(decoded)
        return AQLArithmeticExprLeaf(decoded)

    return _arithmetic_expr(ctx.arithmeticExpr())


def _where_boolean_leaf(ctx: ParserRuleContext):
    if ctx.SYM_EXISTS() is not None:
        return AQLWhereTreeExistsLeaf(_data_match_path(ctx.dataMatchPath()))

    if ctx.matchesOperand() is not None:
        comparison = _comparison_operand(ctx.comparisonOperand())
        matches_ctx = ctx.matchesOperand()
        terminology = matches_ctx.terminologyFunctionCall()
        if terminology is not None:
            matches = _terminology_function_call(terminology)
        else:
            constraint = matches_ctx.matchesConstraint()
            if constraint.literalList() is not None:
                literal_token_types = {
                    AqlParserPyehr.INTEGER,
                    AqlParserPyehr.SCI_INTEGER,
                    AqlParserPyehr.REAL,
                    AqlParserPyehr.SCI_REAL,
                    AqlParserPyehr.STRING,
                    AqlParserPyehr.DATE_STRING,
                    AqlParserPyehr.TIME_STRING,
                    AqlParserPyehr.DATE_TIME_STRING,
                }
                matches = [
                    _literal_from_token(child.symbol).value
                    for child in _terminal_nodes(constraint.literalList())
                    if child.symbol.type in literal_token_types
                ]
            elif constraint.AQL_URI() is not None:
                uri = constraint.AQL_URI().getText().strip("<>")
                matches = Uri(uri)
            else:
                matches = AQLParameter(constraint.PARAMETER().getText()[1:])
        return AQLWhereTreeMatchesLeaf(comparison, matches)

    if ctx.SYM_LIKE() is not None:
        operand = ctx.likeOperand()
        like = (
            AQLParameter(operand.PARAMETER().getText()[1:])
            if operand.PARAMETER() is not None
            else _quoted_value(operand.STRING().getText())
        )
        return AQLWhereTreeLikeLeaf(
            AQLComparisonOperand(_data_match_path(ctx.dataMatchPath())),
            like,
        )

    operator = _comparison_operator(ctx.comparisonOperator())
    right = _comparison_operand(ctx.comparisonOperand())
    left_path = ctx.dataMatchPath()
    left = _data_match_path(left_path) if left_path is not None else _function_call(ctx.functionCall())
    return AQLWhereTreeComparisonLeaf(left, operator, right)


def _terminal_nodes(ctx: ParserRuleContext) -> list[TerminalNode]:
    result: list[TerminalNode] = []
    for child in ctx.children or []:
        if isinstance(child, TerminalNode):
            result.append(child)
        elif isinstance(child, ParserRuleContext):
            result.extend(_terminal_nodes(child))
    return result


def _where_expr(ctx: ParserRuleContext):
    operands = _children_of_rule(ctx, "whereExpr")
    if len(operands) == 2:
        operator = next(
            child.getText()
            for child in ctx.children or []
            if isinstance(child, TerminalNode) and child.getText().upper() in ("AND", "OR")
        )
        return AQLWhereTreeBinaryExpr(
            _where_expr(operands[0]),
            operator.upper(),
            _where_expr(operands[1]),
        )
    if len(operands) == 1:
        if any(isinstance(child, TerminalNode) and child.getText().upper() == "NOT"
               for child in ctx.children or []):
            return AQLWhereTreeNotExpr(_where_expr(operands[0]))
        return _where_expr(operands[0])
    return _where_boolean_leaf(ctx.whereBooleanLeaf())


def _model_type(ctx: ParserRuleContext) -> AQLModelType:
    archetype_id_ctx = ctx.archetypeIdPredicate()
    archetype_id = ArchetypeID(archetype_id_ctx.getText()) if archetype_id_ctx else None
    variable = ctx.variableName.text if ctx.variableName is not None else None
    return AQLModelType(ctx.typeName.text, variable, archetype_id)


def _model_type_constraint(ctx: ParserRuleContext):
    chain = ctx.modelTypeChain()
    if chain is None:
        return AQLModelTypeTreeConstraint(_model_type(ctx.modelType()))

    subchain = chain.modelTypeSubChain()
    nested_constraint = subchain.modelTypeConstraint()
    nested_expr = subchain.modelTypeExpr()
    contains = (
        _model_type_constraint(nested_constraint)
        if nested_constraint is not None
        else _model_type_expr(nested_expr)
    )
    return AQLModelTypeTreeConstraint(
        _model_type(chain.modelType()),
        chain.SYM_NOT() is not None,
        contains,
    )


def _model_type_expr(ctx: ParserRuleContext):
    operands = _children_of_rule(ctx, "modelTypeExpr")
    if len(operands) == 2:
        operator = next(
            child.getText()
            for child in ctx.children or []
            if isinstance(child, TerminalNode) and child.getText().upper() in ("AND", "OR")
        )
        return AQLModelTypeTreeBinaryExpr(
            _model_type_expr(operands[0]),
            operator.upper(),
            _model_type_expr(operands[1]),
        )
    if len(operands) == 1:
        if any(isinstance(child, TerminalNode) and child.getText().upper() == "NOT"
               for child in ctx.children or []):
            return AQLModelTypeTreeNotExpr(_model_type_expr(operands[0]))
        return _model_type_expr(operands[0])
    return _model_type_constraint(ctx.modelTypeConstraint())


def _aggregate_function_call(ctx: ParserRuleContext) -> AQLAggregateFunctionCall:
    if ctx.SYM_COUNT() is not None:
        path_ctx = ctx.dataMatchPath()
        return AQLAggregateCountFunction(
            match_path=_data_match_path(path_ctx) if path_ctx is not None else None,
            distinct=ctx.SYM_DISTINCT() is not None,
        )

    data_path_ctx = ctx.dataMatchPath()
    if data_path_ctx is None:
        raise AQLParseError(f"Aggregate function is missing a data path: {ctx.getText()!r}")
    data_path = _data_match_path(data_path_ctx)
    return AQLAggregateMathFunction(
        ctx.aggregateMathFunction().getText().upper(),
        data_path,
    )


def parse_aql(aql_string: str) -> AQLQuery:
    """Parse an AQL string into its structured query representation."""
    errors = _ParseErrorListener()
    lexer = AqlLexer(InputStream(aql_string))
    lexer.removeErrorListeners()
    lexer.addErrorListener(errors)
    parser = AqlParserPyehr(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(errors)
    tree = parser.aqlQuery()
    if errors.errors:
        raise AQLParseError("Invalid AQL string: " + "; ".join(errors.errors))

    try:
        select_ctx = tree.selectClause()
        top_ctx = select_ctx.top()
        top = None
        if top_ctx is not None:
            forward = top_ctx.direction is None or top_ctx.direction.text.upper() != "BACKWARD"
            top = (int(top_ctx.INTEGER().getText()), forward)

        columns: list[AQLColumnSpec] = []
        for column_ctx in select_ctx.resultTable().columnSpec():
            value_ctx = column_ctx.columnValue()
            if value_ctx.dataMatchPath() is not None:
                value = _data_match_path(value_ctx.dataMatchPath())
            elif value_ctx.aggregateFunctionCall() is not None:
                value = _aggregate_function_call(value_ctx.aggregateFunctionCall())
            elif value_ctx.functionCall() is not None:
                value = _function_call(value_ctx.functionCall())
            else:
                value = _literal(value_ctx.primitiveLiteral())
            alias_ctx = column_ctx.columnAlias()
            columns.append(AQLColumnSpec(value, alias_ctx.getText() if alias_ctx else None))

        from_clause = AQLFromClause(
            _model_type_constraint(tree.fromClause().modelTypeConstraint())
        )

        where_ctx = tree.whereClause()
        where_clause = (
            AQLWhereClause(_where_expr(where_ctx.whereExpr()))
            if where_ctx is not None else None
        )

        order_ctx = tree.orderByClause()
        orderby_clause = None
        if order_ctx is not None:
            order_exprs = []
            for expression in order_ctx.orderByExpr():
                order = expression.order
                ascending = order is None or order.text.upper() in ("ASC", "ASCENDING")
                order_exprs.append(
                    AQLOrderByExpr(_data_match_path(expression.dataMatchPath()), ascending)
                )
            orderby_clause = AQLOrderByClause(order_exprs)

        limit_ctx = tree.limitClause()
        limit_clause = None
        if limit_ctx is not None:
            limit_clause = AQLLimitClause(
                int(limit_ctx.limit.text),
                int(limit_ctx.offset.text) if limit_ctx.offset is not None else None,
            )

        return AQLQuery(
            AQLSelectClause(
                columns,
                distinct=select_ctx.SYM_DISTINCT() is not None,
                top=top,
            ),
            from_clause,
            where_clause,
            orderby_clause,
            limit_clause,
        )
    except AQLParseError:
        raise
    except ValueError as exc:
        raise AQLParseError(f"Invalid AQL string: {exc}") from exc

class AQLResultSetMetadata(AnyClass):
    """Metadata contained within a RESULT_SET"""

    href: Optional[str]
    """URL of the executed query (only for GET endpoint)."""

    created: ISODateTime
    """Result creation time (in the extended ISO 8601 format)."""

    generator: str
    """Some identifier of the application that generated the result, useful for 
    debugging."""

    executed_aql: Optional[str]
    """The actual AQL query that was executed by the server, after replacing the 
    query parameters. This attribute is not mandatory, but is useful for 
    debugging."""

    def __init__(self, created: ISODateTime, generator: str, href: Optional[str] = None, executed_aql: Optional[str] = None):
        self.href = href
        self.created = created
        self.generator = generator
        self.executed_aql = executed_aql

    def as_json(self):
        draft = {
            "_schema_version": "1.1.0",
            "_type": "RESULT_SET",
            "_created": self.created.value,
            "_generator": self.generator,
        }
        if self.href is not None:
            draft["_href"] = self.href
        if self.executed_aql is not None:
            draft["_executed_aql"] = self.executed_aql
        return draft

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.href, other.href) and
                is_equal_value(self.created, other.created) and
                is_equal_value(self.generator, other.generator) and
                is_equal_value(self.executed_aql, other.executed_aql))
        

class AQLResultSet(AnyClass):
    """Represents the result of running an AQL query. Defined in the REST Query API."""

    meta: AQLResultSetMetadata
    """RESULT_SET metadata"""

    q: AQLQuery
    """The given AQL query"""

    name: Optional[str]
    """The (fully qualified) name of the query (when is registered as a stored
      query), in a format of [{namespace}::]{query-name}."""

    columns: list[tuple[str, str]]
    """List of column definitions as a name, path pair"""

    rows: list[list[Union[str, int, object]]]
    """List of individual rows, as lists of values (in same order as the column definitions)"""

    def __init__(self, q: AQLQuery, meta: AQLResultSetMetadata, columns: list[tuple[str, str]], rows: list[list[Union[str, int, object]]], name: Optional[str] = None):
        self.meta = meta
        self.q = q
        self.name = name
        self.columns = columns
        self.rows = rows

    def is_equal(self, other):
        return (type(self) == type(other) and
                self.meta.is_equal(other.meta) and
                is_equal_value(self.q.as_aql(), other.q.as_aql()) and
                is_equal_value(self.name, other.name) and
                is_equal_value(self.columns, other.columns) and
                is_equal_value(self.rows, other.rows))

    def as_json(self):
        draft = {
            "meta": self.meta.as_json(),
            "q": self.q.as_aql(),
            "columns": [{"name": p[0], "path":p[1]} for p in self.columns],
            "rows": self.rows
        }
        if self.name is not None:
            draft["name"] = self.name
        return draft

