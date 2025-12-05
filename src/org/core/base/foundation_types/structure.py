from typing import Union

import numpy as np

from org.core.base.foundation_types import AnyClass

container = Union[dict, list, set, np.ndarray]

def is_equal_value(a, b) -> bool:
    """Utility function to test if two arbitrary pyehr classes are equal in value (rather than in reference)"""
    if type(a) != type(b):
        return False
    elif isinstance(a, AnyClass):
        return a.is_equal(b)
    elif isinstance(a, list):
        return list_is_equal(a, b)
    elif isinstance(a, dict):
        return dict_is_equal(a, b)
    elif isinstance(a, set):
        return set_is_equal(a, b)
    else:
        return (a == b)

def list_is_equal(a : list, b: list) -> bool:
    """Utility function to test if two lists are equal in value (i.e for every item in a, the item in the same position in b is equal in value)"""
    if len(a) != len(b):
        return False
    for i in range(0, len(a)):
        if not is_equal_value(a[i], b[i]):
            return False
    return True

def dict_is_equal(a: dict, b: dict) -> bool:
    """Utility function to test if two dictionaries are equal in value (i.e for every (k, v) in a, the same (k, v) exists in b and vice versa)"""
    if len(a) != len(b):
        return False
    for a_key in a.keys():
        if a_key not in b:
            return False
        elif not is_equal_value(a[a_key], b[a_key]):
            return False
    return True

def set_is_equal(a: set, b: set) -> bool:
    """Utility function to test if two sets are equal in value (i.e every item in a is also in b)"""
    if len(a) != len(b):
        return False
    for a_item in a:
        if a_item not in b:
            return False
    return True