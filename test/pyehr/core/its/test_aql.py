import pytest

from pyehr.core.base.foundation_types.time import ISODate
from pyehr.core.its.aql import AQLParseError, parse_aql
from pyehr.core.its.aql.process import CONTAINS_RM_MAP
from pyehr.core.its.aql.query import (
    AQLAggregateCountFunction,
    AQLAggregateMathFunction,
    AQLFunctionCall,
    AQLModelTypeTreeBinaryExpr,
    AQLModelTypeTreeConstraint,
    AQLWhereTreeComparisonLeaf,
    AQLWhereTreeMatchesLeaf,
)


def test_contains_rm_map_uses_json_attributes():
    assert CONTAINS_RM_MAP["COMPOSITION"] == {
        "CONTENT_ITEM": ("content", False, False),
        "SECTION": ("content", False, False),
        "ENTRY": ("content", False, False),
        "ADMIN_ENTRY": ("content", False, False),
        "CARE_ENTRY": ("content", False, False),
        "OBSERVATION": ("content", False, False),
        "EVALUATION": ("content", False, False),
        "INSTRUCTION": ("content", False, False),
        "ACTION": ("content", False, False),
    }
    assert CONTAINS_RM_MAP["EHR"]["CONTRIBUTION"] == ("contributions", True, False)
    assert CONTAINS_RM_MAP["EHR"]["VERSIONED_EHR_STATUS"] == ("ehr_status", True, False)
    assert CONTAINS_RM_MAP["EHR"]["VERSIONED_EHR_ACCESS"] == ("ehr_access", True, False)
    assert CONTAINS_RM_MAP["EHR"]["VERSIONED_FOLDER"] == ("folders", True, False)
    assert CONTAINS_RM_MAP["SECTION"]["SECTION"] == ("items", False, False)
    assert CONTAINS_RM_MAP["INSTRUCTION"]["ACTIVITY"] == ("activities", False, False)

    party_children = {
        "PARTY_IDENTITY": ("identities", False, False),
        "CONTACT": ("contacts", False, False),
        "ITEM_STRUCTURE": ("details", False, False),
        "PARTY_RELATIONSHIP": ("relationships", False, False),
    }
    for actor_type in ("ACTOR", "PERSON", "ORGANISATION", "GROUP", "AGENT"):
        assert all(
            CONTAINS_RM_MAP[actor_type][child_type] == containment
            for child_type, containment in party_children.items()
        )
        assert CONTAINS_RM_MAP[actor_type]["ROLE"] == ("roles", True, True)
        assert CONTAINS_RM_MAP[actor_type]["VERSIONED_PARTY"] == ("roles", True, False)
    assert CONTAINS_RM_MAP["ROLE"]["CAPABILITY"] == ("capabilities", False, False)


def test_contains_rm_map_covers_nested_locatables():
    containment_edges = (
        ("ADMIN_ENTRY", "ITEM_TREE", "data"),
        ("OBSERVATION", "HISTORY", "data"),
        ("HISTORY", "POINT_EVENT", "events"),
        ("EVENT", "ITEM_TREE", "data"),
        ("ITEM_TABLE", "CLUSTER", "rows"),
        ("CLUSTER", "ELEMENT", "items"),
        ("FOLDER", "FOLDER", "folders"),
        ("CONTACT", "ADDRESS", "addresses"),
        ("CAPABILITY", "ITEM_TREE", "credentials"),
        ("EHR_STATUS", "ITEM_TREE", "other_details"),
    )
    for parent_type, child_type, attribute in containment_edges:
        assert CONTAINS_RM_MAP[parent_type][child_type] == (
            attribute,
            False,
            False,
        )


def test_parse_aql_clauses_and_round_trip():
    query = parse_aql(
        "SELECT DISTINCT c/name/value AS value "
        "FROM COMPOSITION c "
        "WHERE c/name/value = 'example' "
        "ORDER BY c/name/value DESC "
        "LIMIT 10 OFFSET 2"
    )

    assert query.select_clause.distinct
    assert query.select_clause.result_columns[0].alias == "value"
    assert query.from_clause.model_type_constraint.model_type.type_name == "COMPOSITION"
    assert isinstance(query.where_clause.where_expression_tree, AQLWhereTreeComparisonLeaf)
    assert query.orderby_clause.order_by_expressions[0].ascending_order is False
    assert query.limit_clause.limit == 10
    assert query.limit_clause.offset == 2
    assert "LIMIT 10 OFFSET 2" in query.as_aql()
    assert parse_aql(query.as_aql()).limit_clause.offset == 2


def test_parse_aql_model_type_contains_expression():
    query = parse_aql(
        "SELECT c FROM EHR e CONTAINS COMPOSITION c "
        "CONTAINS (OBSERVATION o OR EVALUATION x)"
    )

    root = query.from_clause.model_type_constraint
    assert isinstance(root, AQLModelTypeTreeConstraint)
    assert root.model_type.type_name == "EHR"
    composition = root.contains
    assert isinstance(composition, AQLModelTypeTreeConstraint)
    assert composition.model_type.variable_name == "c"
    assert isinstance(composition.contains, AQLModelTypeTreeBinaryExpr)
    assert composition.contains.operator == "OR"


def test_parse_aql_path_predicates_and_typed_literals():
    query = parse_aql(
        "SELECT c FROM COMPOSITION c "
        "WHERE c/data[at0001 AND name/value = 'x']/value = '2020-01-01'"
    )

    comparison = query.where_clause.where_expression_tree
    assert isinstance(comparison, AQLWhereTreeComparisonLeaf)
    path_segment = comparison.op1.path_segments[0]
    assert path_segment.predicate_string == "at0001 AND name/value = 'x'"
    assert path_segment.predicate_tree is not None
    assert isinstance(comparison.op2.value.value, ISODate)


def test_parse_aql_matches_lists_and_uris():
    list_query = parse_aql(
        "SELECT c FROM COMPOSITION c WHERE c/name/value matches {'one', 'two'}"
    )
    list_leaf = list_query.where_clause.where_expression_tree
    assert isinstance(list_leaf, AQLWhereTreeMatchesLeaf)
    assert list_leaf.matches == ["one", "two"]
    assert isinstance(parse_aql(list_query.as_aql()), type(list_query))

    uri_query = parse_aql(
        "SELECT c FROM COMPOSITION c WHERE c/name/value matches {https://example.org/terms}"
    )
    uri_leaf = uri_query.where_clause.where_expression_tree
    assert uri_leaf.matches == "https://example.org/terms"
    assert parse_aql(uri_query.as_aql()).where_clause is not None

    numeric_query = parse_aql(
        "SELECT c FROM COMPOSITION c WHERE c/name/value matches {1, 2}"
    )
    assert numeric_query.where_clause.where_expression_tree.matches == [1, 2]

    date_query = parse_aql(
        "SELECT c FROM COMPOSITION c WHERE c/name/value matches {'2020-01-01'}"
    )
    date_values = date_query.where_clause.where_expression_tree.matches
    assert len(date_values) == 1
    assert isinstance(date_values[0], ISODate)


def test_parse_aql_functions_aggregates_and_top():
    query = parse_aql(
        "SELECT TOP 5 BACKWARD COUNT(DISTINCT c/data) AS total, "
        "SUM(c/data[at0001]/value), LENGTH(c/name/value) FROM COMPOSITION c"
    )

    assert query.select_clause.top == (5, False)
    aggregate = query.select_clause.result_columns[0].value
    assert isinstance(aggregate, AQLAggregateCountFunction)
    assert aggregate.distinct
    math_aggregate = query.select_clause.result_columns[1].value
    assert isinstance(math_aggregate, AQLAggregateMathFunction)
    assert math_aggregate.data_path.path_segments[0].predicate_string == "at0001"
    assert isinstance(query.select_clause.result_columns[2].value, AQLFunctionCall)
    assert "COUNT(DISTINCT c/data)" in query.as_aql()
    assert "SUM(c/data[at0001]/value)" in query.as_aql()

    count_all = parse_aql("SELECT COUNT(*) FROM COMPOSITION c")
    count_all_function = count_all.select_clause.result_columns[0].value
    assert isinstance(count_all_function, AQLAggregateCountFunction)
    assert count_all_function.match_path is None


def test_parse_aql_rejects_malformed_input():
    with pytest.raises(AQLParseError, match="Invalid AQL string"):
        parse_aql("SELECT FROM COMPOSITION c")

