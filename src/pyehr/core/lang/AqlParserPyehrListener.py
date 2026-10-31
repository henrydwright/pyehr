# Generated from AqlParserPyehr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AqlParserPyehr import AqlParserPyehr
else:
    from AqlParserPyehr import AqlParserPyehr

# This class defines a complete listener for a parse tree produced by AqlParserPyehr.
class AqlParserPyehrListener(ParseTreeListener):

    # Enter a parse tree produced by AqlParserPyehr#aqlQuery.
    def enterAqlQuery(self, ctx:AqlParserPyehr.AqlQueryContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#aqlQuery.
    def exitAqlQuery(self, ctx:AqlParserPyehr.AqlQueryContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#selectClause.
    def enterSelectClause(self, ctx:AqlParserPyehr.SelectClauseContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#selectClause.
    def exitSelectClause(self, ctx:AqlParserPyehr.SelectClauseContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#fromClause.
    def enterFromClause(self, ctx:AqlParserPyehr.FromClauseContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#fromClause.
    def exitFromClause(self, ctx:AqlParserPyehr.FromClauseContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#whereClause.
    def enterWhereClause(self, ctx:AqlParserPyehr.WhereClauseContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#whereClause.
    def exitWhereClause(self, ctx:AqlParserPyehr.WhereClauseContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#orderByClause.
    def enterOrderByClause(self, ctx:AqlParserPyehr.OrderByClauseContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#orderByClause.
    def exitOrderByClause(self, ctx:AqlParserPyehr.OrderByClauseContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#limitClause.
    def enterLimitClause(self, ctx:AqlParserPyehr.LimitClauseContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#limitClause.
    def exitLimitClause(self, ctx:AqlParserPyehr.LimitClauseContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#resultTable.
    def enterResultTable(self, ctx:AqlParserPyehr.ResultTableContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#resultTable.
    def exitResultTable(self, ctx:AqlParserPyehr.ResultTableContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#columnSpec.
    def enterColumnSpec(self, ctx:AqlParserPyehr.ColumnSpecContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#columnSpec.
    def exitColumnSpec(self, ctx:AqlParserPyehr.ColumnSpecContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#columnAlias.
    def enterColumnAlias(self, ctx:AqlParserPyehr.ColumnAliasContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#columnAlias.
    def exitColumnAlias(self, ctx:AqlParserPyehr.ColumnAliasContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#columnValue.
    def enterColumnValue(self, ctx:AqlParserPyehr.ColumnValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#columnValue.
    def exitColumnValue(self, ctx:AqlParserPyehr.ColumnValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#orderByExpr.
    def enterOrderByExpr(self, ctx:AqlParserPyehr.OrderByExprContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#orderByExpr.
    def exitOrderByExpr(self, ctx:AqlParserPyehr.OrderByExprContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelTypeConstraint.
    def enterModelTypeConstraint(self, ctx:AqlParserPyehr.ModelTypeConstraintContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelTypeConstraint.
    def exitModelTypeConstraint(self, ctx:AqlParserPyehr.ModelTypeConstraintContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelTypeChain.
    def enterModelTypeChain(self, ctx:AqlParserPyehr.ModelTypeChainContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelTypeChain.
    def exitModelTypeChain(self, ctx:AqlParserPyehr.ModelTypeChainContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelTypeSubChain.
    def enterModelTypeSubChain(self, ctx:AqlParserPyehr.ModelTypeSubChainContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelTypeSubChain.
    def exitModelTypeSubChain(self, ctx:AqlParserPyehr.ModelTypeSubChainContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelTypeExpr.
    def enterModelTypeExpr(self, ctx:AqlParserPyehr.ModelTypeExprContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelTypeExpr.
    def exitModelTypeExpr(self, ctx:AqlParserPyehr.ModelTypeExprContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelType.
    def enterModelType(self, ctx:AqlParserPyehr.ModelTypeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelType.
    def exitModelType(self, ctx:AqlParserPyehr.ModelTypeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#whereExpr.
    def enterWhereExpr(self, ctx:AqlParserPyehr.WhereExprContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#whereExpr.
    def exitWhereExpr(self, ctx:AqlParserPyehr.WhereExprContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#whereBooleanLeaf.
    def enterWhereBooleanLeaf(self, ctx:AqlParserPyehr.WhereBooleanLeafContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#whereBooleanLeaf.
    def exitWhereBooleanLeaf(self, ctx:AqlParserPyehr.WhereBooleanLeafContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#comparisonOperand.
    def enterComparisonOperand(self, ctx:AqlParserPyehr.ComparisonOperandContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#comparisonOperand.
    def exitComparisonOperand(self, ctx:AqlParserPyehr.ComparisonOperandContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#value.
    def enterValue(self, ctx:AqlParserPyehr.ValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#value.
    def exitValue(self, ctx:AqlParserPyehr.ValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#likeOperand.
    def enterLikeOperand(self, ctx:AqlParserPyehr.LikeOperandContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#likeOperand.
    def exitLikeOperand(self, ctx:AqlParserPyehr.LikeOperandContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#matchesOperand.
    def enterMatchesOperand(self, ctx:AqlParserPyehr.MatchesOperandContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#matchesOperand.
    def exitMatchesOperand(self, ctx:AqlParserPyehr.MatchesOperandContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#matchesConstraint.
    def enterMatchesConstraint(self, ctx:AqlParserPyehr.MatchesConstraintContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#matchesConstraint.
    def exitMatchesConstraint(self, ctx:AqlParserPyehr.MatchesConstraintContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#arithmeticExpr.
    def enterArithmeticExpr(self, ctx:AqlParserPyehr.ArithmeticExprContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#arithmeticExpr.
    def exitArithmeticExpr(self, ctx:AqlParserPyehr.ArithmeticExprContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#arithmeticLeaf.
    def enterArithmeticLeaf(self, ctx:AqlParserPyehr.ArithmeticLeafContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#arithmeticLeaf.
    def exitArithmeticLeaf(self, ctx:AqlParserPyehr.ArithmeticLeafContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#arithmeticLiteral.
    def enterArithmeticLiteral(self, ctx:AqlParserPyehr.ArithmeticLiteralContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#arithmeticLiteral.
    def exitArithmeticLiteral(self, ctx:AqlParserPyehr.ArithmeticLiteralContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dataMatchPath.
    def enterDataMatchPath(self, ctx:AqlParserPyehr.DataMatchPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dataMatchPath.
    def exitDataMatchPath(self, ctx:AqlParserPyehr.DataMatchPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dataMatchPathSegment.
    def enterDataMatchPathSegment(self, ctx:AqlParserPyehr.DataMatchPathSegmentContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dataMatchPathSegment.
    def exitDataMatchPathSegment(self, ctx:AqlParserPyehr.DataMatchPathSegmentContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dataMatchPathPredicate.
    def enterDataMatchPathPredicate(self, ctx:AqlParserPyehr.DataMatchPathPredicateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dataMatchPathPredicate.
    def exitDataMatchPathPredicate(self, ctx:AqlParserPyehr.DataMatchPathPredicateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dataMatchPathValuePredicate.
    def enterDataMatchPathValuePredicate(self, ctx:AqlParserPyehr.DataMatchPathValuePredicateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dataMatchPathValuePredicate.
    def exitDataMatchPathValuePredicate(self, ctx:AqlParserPyehr.DataMatchPathValuePredicateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelPathComparatorValue.
    def enterModelPathComparatorValue(self, ctx:AqlParserPyehr.ModelPathComparatorValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelPathComparatorValue.
    def exitModelPathComparatorValue(self, ctx:AqlParserPyehr.ModelPathComparatorValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#versionPredicate.
    def enterVersionPredicate(self, ctx:AqlParserPyehr.VersionPredicateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#versionPredicate.
    def exitVersionPredicate(self, ctx:AqlParserPyehr.VersionPredicateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#functionCall.
    def enterFunctionCall(self, ctx:AqlParserPyehr.FunctionCallContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#functionCall.
    def exitFunctionCall(self, ctx:AqlParserPyehr.FunctionCallContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#functionArgs.
    def enterFunctionArgs(self, ctx:AqlParserPyehr.FunctionArgsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#functionArgs.
    def exitFunctionArgs(self, ctx:AqlParserPyehr.FunctionArgsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#aggregateFunctionCall.
    def enterAggregateFunctionCall(self, ctx:AqlParserPyehr.AggregateFunctionCallContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#aggregateFunctionCall.
    def exitAggregateFunctionCall(self, ctx:AqlParserPyehr.AggregateFunctionCallContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#aggregateMathFunction.
    def enterAggregateMathFunction(self, ctx:AqlParserPyehr.AggregateMathFunctionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#aggregateMathFunction.
    def exitAggregateMathFunction(self, ctx:AqlParserPyehr.AggregateMathFunctionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#terminologyFunctionCall.
    def enterTerminologyFunctionCall(self, ctx:AqlParserPyehr.TerminologyFunctionCallContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#terminologyFunctionCall.
    def exitTerminologyFunctionCall(self, ctx:AqlParserPyehr.TerminologyFunctionCallContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#builtInFunction.
    def enterBuiltInFunction(self, ctx:AqlParserPyehr.BuiltInFunctionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#builtInFunction.
    def exitBuiltInFunction(self, ctx:AqlParserPyehr.BuiltInFunctionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#stringFunction.
    def enterStringFunction(self, ctx:AqlParserPyehr.StringFunctionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#stringFunction.
    def exitStringFunction(self, ctx:AqlParserPyehr.StringFunctionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#numericFunction.
    def enterNumericFunction(self, ctx:AqlParserPyehr.NumericFunctionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#numericFunction.
    def exitNumericFunction(self, ctx:AqlParserPyehr.NumericFunctionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeFunction.
    def enterDateTimeFunction(self, ctx:AqlParserPyehr.DateTimeFunctionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeFunction.
    def exitDateTimeFunction(self, ctx:AqlParserPyehr.DateTimeFunctionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#comparisonOperator.
    def enterComparisonOperator(self, ctx:AqlParserPyehr.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#comparisonOperator.
    def exitComparisonOperator(self, ctx:AqlParserPyehr.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveLiteral.
    def enterPrimitiveLiteral(self, ctx:AqlParserPyehr.PrimitiveLiteralContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveLiteral.
    def exitPrimitiveLiteral(self, ctx:AqlParserPyehr.PrimitiveLiteralContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#numericLiteral.
    def enterNumericLiteral(self, ctx:AqlParserPyehr.NumericLiteralContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#numericLiteral.
    def exitNumericLiteral(self, ctx:AqlParserPyehr.NumericLiteralContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerLiteralList.
    def enterIntegerLiteralList(self, ctx:AqlParserPyehr.IntegerLiteralListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerLiteralList.
    def exitIntegerLiteralList(self, ctx:AqlParserPyehr.IntegerLiteralListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realLiteralList.
    def enterRealLiteralList(self, ctx:AqlParserPyehr.RealLiteralListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realLiteralList.
    def exitRealLiteralList(self, ctx:AqlParserPyehr.RealLiteralListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#stringLiteralList.
    def enterStringLiteralList(self, ctx:AqlParserPyehr.StringLiteralListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#stringLiteralList.
    def exitStringLiteralList(self, ctx:AqlParserPyehr.StringLiteralListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeLiteralList.
    def enterDateTimeLiteralList(self, ctx:AqlParserPyehr.DateTimeLiteralListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeLiteralList.
    def exitDateTimeLiteralList(self, ctx:AqlParserPyehr.DateTimeLiteralListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#literalList.
    def enterLiteralList(self, ctx:AqlParserPyehr.LiteralListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#literalList.
    def exitLiteralList(self, ctx:AqlParserPyehr.LiteralListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#aqlDateTimeLiteral.
    def enterAqlDateTimeLiteral(self, ctx:AqlParserPyehr.AqlDateTimeLiteralContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#aqlDateTimeLiteral.
    def exitAqlDateTimeLiteral(self, ctx:AqlParserPyehr.AqlDateTimeLiteralContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelSpecificPredicateShortcut.
    def enterModelSpecificPredicateShortcut(self, ctx:AqlParserPyehr.ModelSpecificPredicateShortcutContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelSpecificPredicateShortcut.
    def exitModelSpecificPredicateShortcut(self, ctx:AqlParserPyehr.ModelSpecificPredicateShortcutContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#top.
    def enterTop(self, ctx:AqlParserPyehr.TopContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#top.
    def exitTop(self, ctx:AqlParserPyehr.TopContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cComplexObject.
    def enterCComplexObject(self, ctx:AqlParserPyehr.CComplexObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cComplexObject.
    def exitCComplexObject(self, ctx:AqlParserPyehr.CComplexObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cComplexObjectDef.
    def enterCComplexObjectDef(self, ctx:AqlParserPyehr.CComplexObjectDefContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cComplexObjectDef.
    def exitCComplexObjectDef(self, ctx:AqlParserPyehr.CComplexObjectDefContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#nodeId.
    def enterNodeId(self, ctx:AqlParserPyehr.NodeIdContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#nodeId.
    def exitNodeId(self, ctx:AqlParserPyehr.NodeIdContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cAttribute.
    def enterCAttribute(self, ctx:AqlParserPyehr.CAttributeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cAttribute.
    def exitCAttribute(self, ctx:AqlParserPyehr.CAttributeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cAttributeDef.
    def enterCAttributeDef(self, ctx:AqlParserPyehr.CAttributeDefContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cAttributeDef.
    def exitCAttributeDef(self, ctx:AqlParserPyehr.CAttributeDefContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cRegularObject.
    def enterCRegularObject(self, ctx:AqlParserPyehr.CRegularObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cRegularObject.
    def exitCRegularObject(self, ctx:AqlParserPyehr.CRegularObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cArchetypeRoot.
    def enterCArchetypeRoot(self, ctx:AqlParserPyehr.CArchetypeRootContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cArchetypeRoot.
    def exitCArchetypeRoot(self, ctx:AqlParserPyehr.CArchetypeRootContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cComplexObjectProxy.
    def enterCComplexObjectProxy(self, ctx:AqlParserPyehr.CComplexObjectProxyContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cComplexObjectProxy.
    def exitCComplexObjectProxy(self, ctx:AqlParserPyehr.CComplexObjectProxyContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cRegularPrimitiveObject.
    def enterCRegularPrimitiveObject(self, ctx:AqlParserPyehr.CRegularPrimitiveObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cRegularPrimitiveObject.
    def exitCRegularPrimitiveObject(self, ctx:AqlParserPyehr.CRegularPrimitiveObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#archetypeSlot.
    def enterArchetypeSlot(self, ctx:AqlParserPyehr.ArchetypeSlotContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#archetypeSlot.
    def exitArchetypeSlot(self, ctx:AqlParserPyehr.ArchetypeSlotContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cIncludes.
    def enterCIncludes(self, ctx:AqlParserPyehr.CIncludesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cIncludes.
    def exitCIncludes(self, ctx:AqlParserPyehr.CIncludesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cExcludes.
    def enterCExcludes(self, ctx:AqlParserPyehr.CExcludesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cExcludes.
    def exitCExcludes(self, ctx:AqlParserPyehr.CExcludesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#archetypeIdConstraint.
    def enterArchetypeIdConstraint(self, ctx:AqlParserPyehr.ArchetypeIdConstraintContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#archetypeIdConstraint.
    def exitArchetypeIdConstraint(self, ctx:AqlParserPyehr.ArchetypeIdConstraintContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#archetypeIdPath.
    def enterArchetypeIdPath(self, ctx:AqlParserPyehr.ArchetypeIdPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#archetypeIdPath.
    def exitArchetypeIdPath(self, ctx:AqlParserPyehr.ArchetypeIdPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cExistence.
    def enterCExistence(self, ctx:AqlParserPyehr.CExistenceContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cExistence.
    def exitCExistence(self, ctx:AqlParserPyehr.CExistenceContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#existence.
    def enterExistence(self, ctx:AqlParserPyehr.ExistenceContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#existence.
    def exitExistence(self, ctx:AqlParserPyehr.ExistenceContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cCardinality.
    def enterCCardinality(self, ctx:AqlParserPyehr.CCardinalityContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cCardinality.
    def exitCCardinality(self, ctx:AqlParserPyehr.CCardinalityContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cardinality.
    def enterCardinality(self, ctx:AqlParserPyehr.CardinalityContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cardinality.
    def exitCardinality(self, ctx:AqlParserPyehr.CardinalityContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cOccurrences.
    def enterCOccurrences(self, ctx:AqlParserPyehr.COccurrencesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cOccurrences.
    def exitCOccurrences(self, ctx:AqlParserPyehr.COccurrencesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#multiplicity.
    def enterMultiplicity(self, ctx:AqlParserPyehr.MultiplicityContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#multiplicity.
    def exitMultiplicity(self, ctx:AqlParserPyehr.MultiplicityContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#multiplicityMod.
    def enterMultiplicityMod(self, ctx:AqlParserPyehr.MultiplicityModContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#multiplicityMod.
    def exitMultiplicityMod(self, ctx:AqlParserPyehr.MultiplicityModContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#orderingMod.
    def enterOrderingMod(self, ctx:AqlParserPyehr.OrderingModContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#orderingMod.
    def exitOrderingMod(self, ctx:AqlParserPyehr.OrderingModContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#uniqueMod.
    def enterUniqueMod(self, ctx:AqlParserPyehr.UniqueModContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#uniqueMod.
    def exitUniqueMod(self, ctx:AqlParserPyehr.UniqueModContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cOrdinal.
    def enterCOrdinal(self, ctx:AqlParserPyehr.COrdinalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cOrdinal.
    def exitCOrdinal(self, ctx:AqlParserPyehr.COrdinalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#ordinalValue.
    def enterOrdinalValue(self, ctx:AqlParserPyehr.OrdinalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#ordinalValue.
    def exitOrdinalValue(self, ctx:AqlParserPyehr.OrdinalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#ordinalTerm.
    def enterOrdinalTerm(self, ctx:AqlParserPyehr.OrdinalTermContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#ordinalTerm.
    def exitOrdinalTerm(self, ctx:AqlParserPyehr.OrdinalTermContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#domainSpecificExtension.
    def enterDomainSpecificExtension(self, ctx:AqlParserPyehr.DomainSpecificExtensionContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#domainSpecificExtension.
    def exitDomainSpecificExtension(self, ctx:AqlParserPyehr.DomainSpecificExtensionContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#rmTypeId.
    def enterRmTypeId(self, ctx:AqlParserPyehr.RmTypeIdContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#rmTypeId.
    def exitRmTypeId(self, ctx:AqlParserPyehr.RmTypeIdContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#rmAttributeId.
    def enterRmAttributeId(self, ctx:AqlParserPyehr.RmAttributeIdContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#rmAttributeId.
    def exitRmAttributeId(self, ctx:AqlParserPyehr.RmAttributeIdContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cObjectMatcher.
    def enterCObjectMatcher(self, ctx:AqlParserPyehr.CObjectMatcherContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cObjectMatcher.
    def exitCObjectMatcher(self, ctx:AqlParserPyehr.CObjectMatcherContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cComplexObjectMatcher.
    def enterCComplexObjectMatcher(self, ctx:AqlParserPyehr.CComplexObjectMatcherContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cComplexObjectMatcher.
    def exitCComplexObjectMatcher(self, ctx:AqlParserPyehr.CComplexObjectMatcherContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cComplexObjectMatcherDef.
    def enterCComplexObjectMatcherDef(self, ctx:AqlParserPyehr.CComplexObjectMatcherDefContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cComplexObjectMatcherDef.
    def exitCComplexObjectMatcherDef(self, ctx:AqlParserPyehr.CComplexObjectMatcherDefContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cAttributeMatcher.
    def enterCAttributeMatcher(self, ctx:AqlParserPyehr.CAttributeMatcherContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cAttributeMatcher.
    def exitCAttributeMatcher(self, ctx:AqlParserPyehr.CAttributeMatcherContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cAttributeMatcherDef.
    def enterCAttributeMatcherDef(self, ctx:AqlParserPyehr.CAttributeMatcherDefContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cAttributeMatcherDef.
    def exitCAttributeMatcherDef(self, ctx:AqlParserPyehr.CAttributeMatcherDefContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cRegularObjectMatcher.
    def enterCRegularObjectMatcher(self, ctx:AqlParserPyehr.CRegularObjectMatcherContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cRegularObjectMatcher.
    def exitCRegularObjectMatcher(self, ctx:AqlParserPyehr.CRegularObjectMatcherContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cTerminologyCode.
    def enterCTerminologyCode(self, ctx:AqlParserPyehr.CTerminologyCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cTerminologyCode.
    def exitCTerminologyCode(self, ctx:AqlParserPyehr.CTerminologyCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#terminologyLocalCode.
    def enterTerminologyLocalCode(self, ctx:AqlParserPyehr.TerminologyLocalCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#terminologyLocalCode.
    def exitTerminologyLocalCode(self, ctx:AqlParserPyehr.TerminologyLocalCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#valueSetCode.
    def enterValueSetCode(self, ctx:AqlParserPyehr.ValueSetCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#valueSetCode.
    def exitValueSetCode(self, ctx:AqlParserPyehr.ValueSetCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#termCodeDefault.
    def enterTermCodeDefault(self, ctx:AqlParserPyehr.TermCodeDefaultContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#termCodeDefault.
    def exitTermCodeDefault(self, ctx:AqlParserPyehr.TermCodeDefaultContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cLocalTermCode.
    def enterCLocalTermCode(self, ctx:AqlParserPyehr.CLocalTermCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cLocalTermCode.
    def exitCLocalTermCode(self, ctx:AqlParserPyehr.CLocalTermCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#localCodesList.
    def enterLocalCodesList(self, ctx:AqlParserPyehr.LocalCodesListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#localCodesList.
    def exitLocalCodesList(self, ctx:AqlParserPyehr.LocalCodesListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#termCodeItem.
    def enterTermCodeItem(self, ctx:AqlParserPyehr.TermCodeItemContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#termCodeItem.
    def exitTermCodeItem(self, ctx:AqlParserPyehr.TermCodeItemContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cExternalTermCode.
    def enterCExternalTermCode(self, ctx:AqlParserPyehr.CExternalTermCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cExternalTermCode.
    def exitCExternalTermCode(self, ctx:AqlParserPyehr.CExternalTermCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#externalCodesList.
    def enterExternalCodesList(self, ctx:AqlParserPyehr.ExternalCodesListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#externalCodesList.
    def exitExternalCodesList(self, ctx:AqlParserPyehr.ExternalCodesListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#externalTermCodeItem.
    def enterExternalTermCodeItem(self, ctx:AqlParserPyehr.ExternalTermCodeItemContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#externalTermCodeItem.
    def exitExternalTermCodeItem(self, ctx:AqlParserPyehr.ExternalTermCodeItemContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#externalTermCodeDefault.
    def enterExternalTermCodeDefault(self, ctx:AqlParserPyehr.ExternalTermCodeDefaultContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#externalTermCodeDefault.
    def exitExternalTermCodeDefault(self, ctx:AqlParserPyehr.ExternalTermCodeDefaultContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#adl14_at_code.
    def enterAdl14_at_code(self, ctx:AqlParserPyehr.Adl14_at_codeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#adl14_at_code.
    def exitAdl14_at_code(self, ctx:AqlParserPyehr.Adl14_at_codeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#adl14_ac_code.
    def enterAdl14_ac_code(self, ctx:AqlParserPyehr.Adl14_ac_codeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#adl14_ac_code.
    def exitAdl14_ac_code(self, ctx:AqlParserPyehr.Adl14_ac_codeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cInlinePrimitiveObject.
    def enterCInlinePrimitiveObject(self, ctx:AqlParserPyehr.CInlinePrimitiveObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cInlinePrimitiveObject.
    def exitCInlinePrimitiveObject(self, ctx:AqlParserPyehr.CInlinePrimitiveObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cInlineOrderedObject.
    def enterCInlineOrderedObject(self, ctx:AqlParserPyehr.CInlineOrderedObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cInlineOrderedObject.
    def exitCInlineOrderedObject(self, ctx:AqlParserPyehr.CInlineOrderedObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cInlineDTemporalObject.
    def enterCInlineDTemporalObject(self, ctx:AqlParserPyehr.CInlineDTemporalObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cInlineDTemporalObject.
    def exitCInlineDTemporalObject(self, ctx:AqlParserPyehr.CInlineDTemporalObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cBoolean.
    def enterCBoolean(self, ctx:AqlParserPyehr.CBooleanContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cBoolean.
    def exitCBoolean(self, ctx:AqlParserPyehr.CBooleanContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedBooleanValue.
    def enterAssumedBooleanValue(self, ctx:AqlParserPyehr.AssumedBooleanValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedBooleanValue.
    def exitAssumedBooleanValue(self, ctx:AqlParserPyehr.AssumedBooleanValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cInteger.
    def enterCInteger(self, ctx:AqlParserPyehr.CIntegerContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cInteger.
    def exitCInteger(self, ctx:AqlParserPyehr.CIntegerContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedIntegerValue.
    def enterAssumedIntegerValue(self, ctx:AqlParserPyehr.AssumedIntegerValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedIntegerValue.
    def exitAssumedIntegerValue(self, ctx:AqlParserPyehr.AssumedIntegerValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cReal.
    def enterCReal(self, ctx:AqlParserPyehr.CRealContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cReal.
    def exitCReal(self, ctx:AqlParserPyehr.CRealContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedRealValue.
    def enterAssumedRealValue(self, ctx:AqlParserPyehr.AssumedRealValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedRealValue.
    def exitAssumedRealValue(self, ctx:AqlParserPyehr.AssumedRealValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cDateTime.
    def enterCDateTime(self, ctx:AqlParserPyehr.CDateTimeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cDateTime.
    def exitCDateTime(self, ctx:AqlParserPyehr.CDateTimeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedDateTimeValue.
    def enterAssumedDateTimeValue(self, ctx:AqlParserPyehr.AssumedDateTimeValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedDateTimeValue.
    def exitAssumedDateTimeValue(self, ctx:AqlParserPyehr.AssumedDateTimeValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cDate.
    def enterCDate(self, ctx:AqlParserPyehr.CDateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cDate.
    def exitCDate(self, ctx:AqlParserPyehr.CDateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedDateValue.
    def enterAssumedDateValue(self, ctx:AqlParserPyehr.AssumedDateValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedDateValue.
    def exitAssumedDateValue(self, ctx:AqlParserPyehr.AssumedDateValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cTime.
    def enterCTime(self, ctx:AqlParserPyehr.CTimeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cTime.
    def exitCTime(self, ctx:AqlParserPyehr.CTimeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedTimeValue.
    def enterAssumedTimeValue(self, ctx:AqlParserPyehr.AssumedTimeValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedTimeValue.
    def exitAssumedTimeValue(self, ctx:AqlParserPyehr.AssumedTimeValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cDuration.
    def enterCDuration(self, ctx:AqlParserPyehr.CDurationContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cDuration.
    def exitCDuration(self, ctx:AqlParserPyehr.CDurationContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedDurationValue.
    def enterAssumedDurationValue(self, ctx:AqlParserPyehr.AssumedDurationValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedDurationValue.
    def exitAssumedDurationValue(self, ctx:AqlParserPyehr.AssumedDurationValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#cString.
    def enterCString(self, ctx:AqlParserPyehr.CStringContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#cString.
    def exitCString(self, ctx:AqlParserPyehr.CStringContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#assumedStringValue.
    def enterAssumedStringValue(self, ctx:AqlParserPyehr.AssumedStringValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#assumedStringValue.
    def exitAssumedStringValue(self, ctx:AqlParserPyehr.AssumedStringValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveObject.
    def enterPrimitiveObject(self, ctx:AqlParserPyehr.PrimitiveObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveObject.
    def exitPrimitiveObject(self, ctx:AqlParserPyehr.PrimitiveObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveValue.
    def enterPrimitiveValue(self, ctx:AqlParserPyehr.PrimitiveValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveValue.
    def exitPrimitiveValue(self, ctx:AqlParserPyehr.PrimitiveValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveList.
    def enterPrimitiveList(self, ctx:AqlParserPyehr.PrimitiveListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveList.
    def exitPrimitiveList(self, ctx:AqlParserPyehr.PrimitiveListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveArray.
    def enterPrimitiveArray(self, ctx:AqlParserPyehr.PrimitiveArrayContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveArray.
    def exitPrimitiveArray(self, ctx:AqlParserPyehr.PrimitiveArrayContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveSet.
    def enterPrimitiveSet(self, ctx:AqlParserPyehr.PrimitiveSetContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveSet.
    def exitPrimitiveSet(self, ctx:AqlParserPyehr.PrimitiveSetContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveValues.
    def enterPrimitiveValues(self, ctx:AqlParserPyehr.PrimitiveValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveValues.
    def exitPrimitiveValues(self, ctx:AqlParserPyehr.PrimitiveValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveInterval.
    def enterPrimitiveInterval(self, ctx:AqlParserPyehr.PrimitiveIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveInterval.
    def exitPrimitiveInterval(self, ctx:AqlParserPyehr.PrimitiveIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#stringValue.
    def enterStringValue(self, ctx:AqlParserPyehr.StringValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#stringValue.
    def exitStringValue(self, ctx:AqlParserPyehr.StringValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#stringValues.
    def enterStringValues(self, ctx:AqlParserPyehr.StringValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#stringValues.
    def exitStringValues(self, ctx:AqlParserPyehr.StringValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerValue.
    def enterIntegerValue(self, ctx:AqlParserPyehr.IntegerValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerValue.
    def exitIntegerValue(self, ctx:AqlParserPyehr.IntegerValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerValues.
    def enterIntegerValues(self, ctx:AqlParserPyehr.IntegerValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerValues.
    def exitIntegerValues(self, ctx:AqlParserPyehr.IntegerValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerInterval.
    def enterIntegerInterval(self, ctx:AqlParserPyehr.IntegerIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerInterval.
    def exitIntegerInterval(self, ctx:AqlParserPyehr.IntegerIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerIntervalRange.
    def enterIntegerIntervalRange(self, ctx:AqlParserPyehr.IntegerIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerIntervalRange.
    def exitIntegerIntervalRange(self, ctx:AqlParserPyehr.IntegerIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerIntervals.
    def enterIntegerIntervals(self, ctx:AqlParserPyehr.IntegerIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerIntervals.
    def exitIntegerIntervals(self, ctx:AqlParserPyehr.IntegerIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realValue.
    def enterRealValue(self, ctx:AqlParserPyehr.RealValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realValue.
    def exitRealValue(self, ctx:AqlParserPyehr.RealValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realValues.
    def enterRealValues(self, ctx:AqlParserPyehr.RealValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realValues.
    def exitRealValues(self, ctx:AqlParserPyehr.RealValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realInterval.
    def enterRealInterval(self, ctx:AqlParserPyehr.RealIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realInterval.
    def exitRealInterval(self, ctx:AqlParserPyehr.RealIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realIntervalRange.
    def enterRealIntervalRange(self, ctx:AqlParserPyehr.RealIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realIntervalRange.
    def exitRealIntervalRange(self, ctx:AqlParserPyehr.RealIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realIntervals.
    def enterRealIntervals(self, ctx:AqlParserPyehr.RealIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realIntervals.
    def exitRealIntervals(self, ctx:AqlParserPyehr.RealIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#booleanValue.
    def enterBooleanValue(self, ctx:AqlParserPyehr.BooleanValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#booleanValue.
    def exitBooleanValue(self, ctx:AqlParserPyehr.BooleanValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#booleanValues.
    def enterBooleanValues(self, ctx:AqlParserPyehr.BooleanValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#booleanValues.
    def exitBooleanValues(self, ctx:AqlParserPyehr.BooleanValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#characterValue.
    def enterCharacterValue(self, ctx:AqlParserPyehr.CharacterValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#characterValue.
    def exitCharacterValue(self, ctx:AqlParserPyehr.CharacterValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#characterValues.
    def enterCharacterValues(self, ctx:AqlParserPyehr.CharacterValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#characterValues.
    def exitCharacterValues(self, ctx:AqlParserPyehr.CharacterValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateValue.
    def enterDateValue(self, ctx:AqlParserPyehr.DateValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateValue.
    def exitDateValue(self, ctx:AqlParserPyehr.DateValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateValues.
    def enterDateValues(self, ctx:AqlParserPyehr.DateValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateValues.
    def exitDateValues(self, ctx:AqlParserPyehr.DateValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateInterval.
    def enterDateInterval(self, ctx:AqlParserPyehr.DateIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateInterval.
    def exitDateInterval(self, ctx:AqlParserPyehr.DateIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateIntervalRange.
    def enterDateIntervalRange(self, ctx:AqlParserPyehr.DateIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateIntervalRange.
    def exitDateIntervalRange(self, ctx:AqlParserPyehr.DateIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateIntervals.
    def enterDateIntervals(self, ctx:AqlParserPyehr.DateIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateIntervals.
    def exitDateIntervals(self, ctx:AqlParserPyehr.DateIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeValue.
    def enterTimeValue(self, ctx:AqlParserPyehr.TimeValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeValue.
    def exitTimeValue(self, ctx:AqlParserPyehr.TimeValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeValues.
    def enterTimeValues(self, ctx:AqlParserPyehr.TimeValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeValues.
    def exitTimeValues(self, ctx:AqlParserPyehr.TimeValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeInterval.
    def enterTimeInterval(self, ctx:AqlParserPyehr.TimeIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeInterval.
    def exitTimeInterval(self, ctx:AqlParserPyehr.TimeIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeIntervalRange.
    def enterTimeIntervalRange(self, ctx:AqlParserPyehr.TimeIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeIntervalRange.
    def exitTimeIntervalRange(self, ctx:AqlParserPyehr.TimeIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeIntervals.
    def enterTimeIntervals(self, ctx:AqlParserPyehr.TimeIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeIntervals.
    def exitTimeIntervals(self, ctx:AqlParserPyehr.TimeIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeValue.
    def enterDateTimeValue(self, ctx:AqlParserPyehr.DateTimeValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeValue.
    def exitDateTimeValue(self, ctx:AqlParserPyehr.DateTimeValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeValues.
    def enterDateTimeValues(self, ctx:AqlParserPyehr.DateTimeValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeValues.
    def exitDateTimeValues(self, ctx:AqlParserPyehr.DateTimeValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeInterval.
    def enterDateTimeInterval(self, ctx:AqlParserPyehr.DateTimeIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeInterval.
    def exitDateTimeInterval(self, ctx:AqlParserPyehr.DateTimeIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeIntervalRange.
    def enterDateTimeIntervalRange(self, ctx:AqlParserPyehr.DateTimeIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeIntervalRange.
    def exitDateTimeIntervalRange(self, ctx:AqlParserPyehr.DateTimeIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeIntervals.
    def enterDateTimeIntervals(self, ctx:AqlParserPyehr.DateTimeIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeIntervals.
    def exitDateTimeIntervals(self, ctx:AqlParserPyehr.DateTimeIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationValue.
    def enterDurationValue(self, ctx:AqlParserPyehr.DurationValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationValue.
    def exitDurationValue(self, ctx:AqlParserPyehr.DurationValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationValues.
    def enterDurationValues(self, ctx:AqlParserPyehr.DurationValuesContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationValues.
    def exitDurationValues(self, ctx:AqlParserPyehr.DurationValuesContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationInterval.
    def enterDurationInterval(self, ctx:AqlParserPyehr.DurationIntervalContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationInterval.
    def exitDurationInterval(self, ctx:AqlParserPyehr.DurationIntervalContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationIntervalRange.
    def enterDurationIntervalRange(self, ctx:AqlParserPyehr.DurationIntervalRangeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationIntervalRange.
    def exitDurationIntervalRange(self, ctx:AqlParserPyehr.DurationIntervalRangeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationIntervals.
    def enterDurationIntervals(self, ctx:AqlParserPyehr.DurationIntervalsContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationIntervals.
    def exitDurationIntervals(self, ctx:AqlParserPyehr.DurationIntervalsContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#termCodeValue.
    def enterTermCodeValue(self, ctx:AqlParserPyehr.TermCodeValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#termCodeValue.
    def exitTermCodeValue(self, ctx:AqlParserPyehr.TermCodeValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#termCodeListValue.
    def enterTermCodeListValue(self, ctx:AqlParserPyehr.TermCodeListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#termCodeListValue.
    def exitTermCodeListValue(self, ctx:AqlParserPyehr.TermCodeListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#relop.
    def enterRelop(self, ctx:AqlParserPyehr.RelopContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#relop.
    def exitRelop(self, ctx:AqlParserPyehr.RelopContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#adlPath.
    def enterAdlPath(self, ctx:AqlParserPyehr.AdlPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#adlPath.
    def exitAdlPath(self, ctx:AqlParserPyehr.AdlPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#adlPathSegment.
    def enterAdlPathSegment(self, ctx:AqlParserPyehr.AdlPathSegmentContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#adlPathSegment.
    def exitAdlPathSegment(self, ctx:AqlParserPyehr.AdlPathSegmentContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#adlPathPredicate.
    def enterAdlPathPredicate(self, ctx:AqlParserPyehr.AdlPathPredicateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#adlPathPredicate.
    def exitAdlPathPredicate(self, ctx:AqlParserPyehr.AdlPathPredicateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#archetypeIdPredicate.
    def enterArchetypeIdPredicate(self, ctx:AqlParserPyehr.ArchetypeIdPredicateContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#archetypeIdPredicate.
    def exitArchetypeIdPredicate(self, ctx:AqlParserPyehr.ArchetypeIdPredicateContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#idCode.
    def enterIdCode(self, ctx:AqlParserPyehr.IdCodeContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#idCode.
    def exitIdCode(self, ctx:AqlParserPyehr.IdCodeContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#augmentedAdlPath.
    def enterAugmentedAdlPath(self, ctx:AqlParserPyehr.AugmentedAdlPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#augmentedAdlPath.
    def exitAugmentedAdlPath(self, ctx:AqlParserPyehr.AugmentedAdlPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelPath.
    def enterModelPath(self, ctx:AqlParserPyehr.ModelPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelPath.
    def exitModelPath(self, ctx:AqlParserPyehr.ModelPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelSubPath.
    def enterModelSubPath(self, ctx:AqlParserPyehr.ModelSubPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelSubPath.
    def exitModelSubPath(self, ctx:AqlParserPyehr.ModelSubPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#modelPathSegment.
    def enterModelPathSegment(self, ctx:AqlParserPyehr.ModelPathSegmentContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#modelPathSegment.
    def exitModelPathSegment(self, ctx:AqlParserPyehr.ModelPathSegmentContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinObject.
    def enterOdinObject(self, ctx:AqlParserPyehr.OdinObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinObject.
    def exitOdinObject(self, ctx:AqlParserPyehr.OdinObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinAttrVal.
    def enterOdinAttrVal(self, ctx:AqlParserPyehr.OdinAttrValContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinAttrVal.
    def exitOdinAttrVal(self, ctx:AqlParserPyehr.OdinAttrValContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinAttrName.
    def enterOdinAttrName(self, ctx:AqlParserPyehr.OdinAttrNameContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinAttrName.
    def exitOdinAttrName(self, ctx:AqlParserPyehr.OdinAttrNameContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinObjectBlock.
    def enterOdinObjectBlock(self, ctx:AqlParserPyehr.OdinObjectBlockContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinObjectBlock.
    def exitOdinObjectBlock(self, ctx:AqlParserPyehr.OdinObjectBlockContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinObjectValueBlock.
    def enterOdinObjectValueBlock(self, ctx:AqlParserPyehr.OdinObjectValueBlockContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinObjectValueBlock.
    def exitOdinObjectValueBlock(self, ctx:AqlParserPyehr.OdinObjectValueBlockContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#rmTypeSpec.
    def enterRmTypeSpec(self, ctx:AqlParserPyehr.RmTypeSpecContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#rmTypeSpec.
    def exitRmTypeSpec(self, ctx:AqlParserPyehr.RmTypeSpecContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinKeyedObject.
    def enterOdinKeyedObject(self, ctx:AqlParserPyehr.OdinKeyedObjectContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinKeyedObject.
    def exitOdinKeyedObject(self, ctx:AqlParserPyehr.OdinKeyedObjectContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinKeySpec.
    def enterOdinKeySpec(self, ctx:AqlParserPyehr.OdinKeySpecContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinKeySpec.
    def exitOdinKeySpec(self, ctx:AqlParserPyehr.OdinKeySpecContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinObjectReferenceBlock.
    def enterOdinObjectReferenceBlock(self, ctx:AqlParserPyehr.OdinObjectReferenceBlockContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinObjectReferenceBlock.
    def exitOdinObjectReferenceBlock(self, ctx:AqlParserPyehr.OdinObjectReferenceBlockContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinPathList.
    def enterOdinPathList(self, ctx:AqlParserPyehr.OdinPathListContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinPathList.
    def exitOdinPathList(self, ctx:AqlParserPyehr.OdinPathListContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinPath.
    def enterOdinPath(self, ctx:AqlParserPyehr.OdinPathContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinPath.
    def exitOdinPath(self, ctx:AqlParserPyehr.OdinPathContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#odinPathSegment.
    def enterOdinPathSegment(self, ctx:AqlParserPyehr.OdinPathSegmentContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#odinPathSegment.
    def exitOdinPathSegment(self, ctx:AqlParserPyehr.OdinPathSegmentContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveListValue.
    def enterPrimitiveListValue(self, ctx:AqlParserPyehr.PrimitiveListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveListValue.
    def exitPrimitiveListValue(self, ctx:AqlParserPyehr.PrimitiveListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#primitiveIntervalValue.
    def enterPrimitiveIntervalValue(self, ctx:AqlParserPyehr.PrimitiveIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#primitiveIntervalValue.
    def exitPrimitiveIntervalValue(self, ctx:AqlParserPyehr.PrimitiveIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#stringListValue.
    def enterStringListValue(self, ctx:AqlParserPyehr.StringListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#stringListValue.
    def exitStringListValue(self, ctx:AqlParserPyehr.StringListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerListValue.
    def enterIntegerListValue(self, ctx:AqlParserPyehr.IntegerListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerListValue.
    def exitIntegerListValue(self, ctx:AqlParserPyehr.IntegerListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerIntervalValue.
    def enterIntegerIntervalValue(self, ctx:AqlParserPyehr.IntegerIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerIntervalValue.
    def exitIntegerIntervalValue(self, ctx:AqlParserPyehr.IntegerIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#integerIntervalListValue.
    def enterIntegerIntervalListValue(self, ctx:AqlParserPyehr.IntegerIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#integerIntervalListValue.
    def exitIntegerIntervalListValue(self, ctx:AqlParserPyehr.IntegerIntervalListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realListValue.
    def enterRealListValue(self, ctx:AqlParserPyehr.RealListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realListValue.
    def exitRealListValue(self, ctx:AqlParserPyehr.RealListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realIntervalValue.
    def enterRealIntervalValue(self, ctx:AqlParserPyehr.RealIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realIntervalValue.
    def exitRealIntervalValue(self, ctx:AqlParserPyehr.RealIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#realIntervalListValue.
    def enterRealIntervalListValue(self, ctx:AqlParserPyehr.RealIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#realIntervalListValue.
    def exitRealIntervalListValue(self, ctx:AqlParserPyehr.RealIntervalListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#booleanListValue.
    def enterBooleanListValue(self, ctx:AqlParserPyehr.BooleanListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#booleanListValue.
    def exitBooleanListValue(self, ctx:AqlParserPyehr.BooleanListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#characterListValue.
    def enterCharacterListValue(self, ctx:AqlParserPyehr.CharacterListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#characterListValue.
    def exitCharacterListValue(self, ctx:AqlParserPyehr.CharacterListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateListValue.
    def enterDateListValue(self, ctx:AqlParserPyehr.DateListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateListValue.
    def exitDateListValue(self, ctx:AqlParserPyehr.DateListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateIntervalValue.
    def enterDateIntervalValue(self, ctx:AqlParserPyehr.DateIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateIntervalValue.
    def exitDateIntervalValue(self, ctx:AqlParserPyehr.DateIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateIntervalListValue.
    def enterDateIntervalListValue(self, ctx:AqlParserPyehr.DateIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateIntervalListValue.
    def exitDateIntervalListValue(self, ctx:AqlParserPyehr.DateIntervalListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeListValue.
    def enterTimeListValue(self, ctx:AqlParserPyehr.TimeListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeListValue.
    def exitTimeListValue(self, ctx:AqlParserPyehr.TimeListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeIntervalValue.
    def enterTimeIntervalValue(self, ctx:AqlParserPyehr.TimeIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeIntervalValue.
    def exitTimeIntervalValue(self, ctx:AqlParserPyehr.TimeIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#timeIntervalListValue.
    def enterTimeIntervalListValue(self, ctx:AqlParserPyehr.TimeIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#timeIntervalListValue.
    def exitTimeIntervalListValue(self, ctx:AqlParserPyehr.TimeIntervalListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeListValue.
    def enterDateTimeListValue(self, ctx:AqlParserPyehr.DateTimeListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeListValue.
    def exitDateTimeListValue(self, ctx:AqlParserPyehr.DateTimeListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeIntervalValue.
    def enterDateTimeIntervalValue(self, ctx:AqlParserPyehr.DateTimeIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeIntervalValue.
    def exitDateTimeIntervalValue(self, ctx:AqlParserPyehr.DateTimeIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#dateTimeIntervalListValue.
    def enterDateTimeIntervalListValue(self, ctx:AqlParserPyehr.DateTimeIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#dateTimeIntervalListValue.
    def exitDateTimeIntervalListValue(self, ctx:AqlParserPyehr.DateTimeIntervalListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationListValue.
    def enterDurationListValue(self, ctx:AqlParserPyehr.DurationListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationListValue.
    def exitDurationListValue(self, ctx:AqlParserPyehr.DurationListValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationIntervalValue.
    def enterDurationIntervalValue(self, ctx:AqlParserPyehr.DurationIntervalValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationIntervalValue.
    def exitDurationIntervalValue(self, ctx:AqlParserPyehr.DurationIntervalValueContext):
        pass


    # Enter a parse tree produced by AqlParserPyehr#durationIntervalListValue.
    def enterDurationIntervalListValue(self, ctx:AqlParserPyehr.DurationIntervalListValueContext):
        pass

    # Exit a parse tree produced by AqlParserPyehr#durationIntervalListValue.
    def exitDurationIntervalListValue(self, ctx:AqlParserPyehr.DurationIntervalListValueContext):
        pass



del AqlParserPyehr