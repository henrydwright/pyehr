from typing import Union

from uritools import urisplit
import numpy as np
from pydantic import BaseModel

from org.openehr.base.foundation_types.time import temporal

class Uri(str):
    """
    A string constrained to obey the syntax of RFC 3986
    """

    def __new__(cls, uri_string : str):
        parts = urisplit(uri_string)
        if not parts.isuri():
            raise ValueError("URI string not valid under RFC 3986")
        return str(uri_string)

# This section defines Types for other primitive types
integer_type = np.int32
ordered_numeric = Union[np.int32, np.int64, np.float32, np.float64]
"""Abstract notional parent class of ordered, numeric types, which are types with both the less_than() and arithmetic functions defined."""
numeric = ordered_numeric
"""Abstract parent class of numeric types, which are types which have various arithmetic and comparison operators defined."""
ordered = Union[ordered_numeric, np.uint8, np.int8, str, temporal]
"""Abstract parent class of ordered types i.e. types on which the '<' operator is defined."""
