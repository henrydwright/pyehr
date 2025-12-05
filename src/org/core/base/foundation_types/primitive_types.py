from typing import Union
import re

from uritools import urisplit, uriencode, RESERVED, UNRESERVED
import numpy as np
from pydantic import BaseModel

from org.core.base.foundation_types.time import temporal

class Uri(str):
    """
    A string constrained to obey the syntax of RFC 3986
    """

    def __new__(cls, uri_string : str, allow_unencoded = False):
        parts = urisplit(uri_string)
        if not parts.isuri():
            raise ValueError("URI string not valid under RFC 3986")
        
        if not allow_unencoded:
            valid_chars = RESERVED + UNRESERVED + "%"
            for i in range(0, len(uri_string)):
                if valid_chars.find(uri_string[i]) < 0:
                    raise ValueError("URI string contains characters that have not been encoded as per RFC 3986")
        
        return str(uri_string)

# This section defines Types for other primitive types
integer_type = np.int32
ordered_numeric = Union[np.int32, np.int64, np.float32, np.float64]
"""Abstract notional parent class of ordered, numeric types, which are types with both the less_than() and arithmetic functions defined."""
numeric = ordered_numeric
"""Abstract parent class of numeric types, which are types which have various arithmetic and comparison operators defined."""
ordered = Union[ordered_numeric, np.uint8, np.int8, str, temporal]
"""Abstract parent class of ordered types i.e. types on which the '<' operator is defined."""
