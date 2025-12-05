from abc import abstractmethod

from org.core.base.foundation_types.any import AnyClass
from org.core.base.base_types.definitions import OpenEHRDefinitions

class DataValue(AnyClass, OpenEHRDefinitions):
    """Abstract parent of all DV_ data value types. Serves as a common ancestor of all data value types in openEHR models."""
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def is_equal(self, other):
        pass