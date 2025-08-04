import pytest

from org.openehr.base.foundation_types.structure import dict_is_equal, list_is_equal, set_is_equal

def test_list_is_equal_different_lengths():
    a = [1, 2, 3, 4]
    b = [1, 2, 3]
    assert not list_is_equal(a, b)

def test_list_is_equal_identical_lists():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert list_is_equal(a, b)

def test_list_is_equal_different_values():
    a = [1, 2, 3]
    b = [1, 2, 4]
    assert not list_is_equal(a, b)

def test_list_is_equal_empty_lists():
    a = []
    b = []
    assert list_is_equal(a, b)

def test_list_is_equal_nested_reference_types():
    a = [[1, 2], [3, 4]]
    b = [[1, 2], [3, 4]]
    assert list_is_equal(a, b)

    c = [{"x": 2, "y": 3}, {"x": 3, "y": 4}]
    d = [{"x": 2, "y": 3}, {"x": 3, "y": 4}]
    assert list_is_equal(c, d)

def test_list_is_equal_nested_reference_types_different():
    a = [[1, 2], [3, 4]]
    b = [[1, 2], [4, 3]]
    assert not list_is_equal(a, b)

    c = [{"x": 2, "y": 3}, {"x": 3, "y": 4}]
    d = [{"x": 2, "y": 3}, {"x": 5, "y": 4}]
    assert not list_is_equal(c, d)

def test_list_is_equal_with_different_types():
    a = [1, "2", 3.0]
    b = [1, "2", 3.0]
    assert list_is_equal(a, b)

def test_list_is_equal_with_none():
    a = [None, 2, 3]
    b = [None, 2, 3]
    assert list_is_equal(a, b)

def test_list_is_equal_with_none_and_value():
    a = [None, 2, 3]
    b = [0, 2, 3]
    assert not list_is_equal(a, b)

def test_dict_is_equal_identical_dicts():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 2}
    assert dict_is_equal(a, b)

def test_dict_is_equal_different_keys():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "c": 2}
    assert not dict_is_equal(a, b)

def test_dict_is_equal_different_values():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 3}
    assert not dict_is_equal(a, b)

def test_dict_is_equal_missing_key():
    a = {"a": 1, "b": 2}
    b = {"a": 1}
    assert not dict_is_equal(a, b)

    a = {"a": 1, "b": 2}
    b = {"a": 1}
    assert not dict_is_equal(b, a)

def test_dict_is_equal_empty_dicts():
    a = {}
    b = {}
    assert dict_is_equal(a, b)

def test_dict_is_equal_nested_dicts():
    a = {"x": {"y": 1}, "z": 2}
    b = {"x": {"y": 1}, "z": 2}
    assert dict_is_equal(a, b)

def test_dict_is_equal_nested_dicts_different():
    a = {"x": {"y": 1}, "z": 2}
    b = {"x": {"y": 2}, "z": 2}
    assert not dict_is_equal(a, b)

def test_dict_is_equal_with_list_values():
    a = {"x": [1, 2], "y": [3, 4]}
    b = {"x": [1, 2], "y": [3, 4]}
    assert dict_is_equal(a, b)

def test_dict_is_equal_with_list_values_different():
    a = {"x": [1, 2], "y": [3, 4]}
    b = {"x": [1, 2], "y": [4, 3]}
    assert not dict_is_equal(a, b)

def test_dict_is_equal_with_none_values():
    a = {"x": None, "y": 2}
    b = {"x": None, "y": 2}
    assert dict_is_equal(a, b)

def test_dict_is_equal_with_none_and_value():
    a = {"x": None, "y": 2}
    b = {"x": 0, "y": 2}
    assert not dict_is_equal(a, b)

def test_set_is_equal_identical_sets():
    a = {1, 2, 3}
    b = {1, 2, 3}
    assert set_is_equal(a, b)

def test_set_is_equal_different_lengths():
    a = {1, 2, 3}
    b = {1, 2}
    assert not set_is_equal(a, b)

def test_set_is_equal_different_values():
    a = {1, 2, 3}
    b = {1, 2, 4}
    assert not set_is_equal(a, b)

def test_set_is_equal_empty_sets():
    a = set()
    b = set()
    assert set_is_equal(a, b)

def test_set_is_equal_with_none():
    a = {None, 2, 3}
    b = {None, 2, 3}
    assert set_is_equal(a, b)

def test_set_is_equal_with_none_and_value():
    a = {None, 2, 3}
    b = {0, 2, 3}
    assert not set_is_equal(a, b)

def test_set_is_equal_with_different_types():
    a = {1, "2", 3.0}
    b = {1, "2", 3.0}
    assert set_is_equal(a, b)
