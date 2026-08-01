from typing import Union

import numpy as np

from pyehr.core.base.foundation_types import AnyClass

container = Union[dict, list, set, np.ndarray]

__all__ = ['is_equal_value', 'list_is_equal', 'dict_is_equal', 'set_is_equal']

def is_equal_value(a, b) -> bool:
    """Utility function to test if two arbitrary pyehr classes are equal in value (rather than in reference)"""
    #print(f"?|{str(a)}:{str(b)}")
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
        if isinstance(a_item, AnyClass):
            # reference type, so can't use 'a_item in b'
            found = False
            for b_item in b:
                found = found or a_item.is_equal(b_item)
            if not found:
                return False
        else:
            if a_item not in b:
                return False
    return True