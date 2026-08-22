from pyehr.types import get_python_attribute_name
import pytest

def test_get_python_attribute_name_returns_default_otherwise():
    assert get_python_attribute_name("C_COMPLEX_OBJECT", "rm_type_name") == "rm_type_name"

def test_get_python_attribute_name_covers_all_exceptions():
    assert get_python_attribute_name("OBJECT_REF", "type") == "ref_type"
    assert get_python_attribute_name("DV_IDENTIFIER", "type") == "id_type"
    assert get_python_attribute_name("DV_PROPORTION", "type") == "proportion_type"
    assert get_python_attribute_name("LINK", "type") == "link_type"
    assert get_python_attribute_name("EXPR_LEAF", "type") == "type_var"
    assert get_python_attribute_name("EXPR_BINARY_OPERATOR", "type") == "type_var"
    assert get_python_attribute_name("EXPR_UNARY_OPERATOR", "type") == "type_var"
    assert get_python_attribute_name("C_DV_QUANTITY", "property") == "property_var"
    assert get_python_attribute_name("C_DV_QUANTITY", "list") == "list_var"
    assert get_python_attribute_name("C_STRING", "list") == "list_var"
    assert get_python_attribute_name("C_INTEGER", "list") == "list_var"
    assert get_python_attribute_name("C_REAL", "list") == "list_var"
    assert get_python_attribute_name("C_DV_ORDINAL", "list") == "list_var"

