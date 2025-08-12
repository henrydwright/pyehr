from abc import ABC, abstractmethod

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.base_types.definitions import OpenEHRDefinitions

class DataValue(ABC, OpenEHRDefinitions):
    """Abstract parent of all DV_ data value types. Serves as a common ancestor of all data value types in openEHR models."""
    
    @abstractmethod
    def __init__(self):
        pass

    