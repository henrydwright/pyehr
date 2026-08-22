"""Contains interfaces and methods relied upon for validating references outside of
an archetype or a template"""

from abc import ABC, abstractmethod
from typing import Optional

from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology, ConstraintBindingItem
from pyehr.core.base.base_types.identification import ArchetypeID, TerminologyID

__all__ = ['IArchetypeRetriever']

class IArchetypeRetriever(ABC):
    """(NON-RM CLASS) Defines an interface for retrieving archetypes"""

    @abstractmethod
    def get_archetype_by_id(self, arch_id : ArchetypeID) -> Optional['Archetype']: # pyright: ignore[reportUndefinedVariable]
        """Retrieve a single ARCHETYPE by its ID, or None if it doesn't exist"""
        pass

class TerminologyUnsupportedError(NotImplementedError):
    """Error raised when a constraint resolver cannot resolve a given constraint
    as it does not support that terminology"""
    pass

class IConstraintResolver(ABC):
    """(NON-RM CLASS) Defines an interface for resolving whether a given
    terminological constraint has been met"""

    @abstractmethod
    def supports_terminology(self, terminology_id: TerminologyID) -> bool:
        """Returns whether this resolver supports the given terminology ID"""
        pass

    @abstractmethod
    def valid_value(self, terminology_id: TerminologyID, constraint: ConstraintBindingItem, concrete_value: str) -> bool:
        """Returns whether a concrete value is valid under a given constraint.
        
        :raises TerminologyUnsupportedError: If the terminology in terminology_id is not supported by this resolver"""
        pass

class PythonArchetypeRetriever(IArchetypeRetriever):

    _archetype_dict: dict[str, 'Archetype'] # pyright: ignore[reportUndefinedVariable]

    def __init__(self, archetypes : Optional[list['Archetype']] = None): # pyright: ignore[reportUndefinedVariable]
        from pyehr.core.am.aom14.archetype import Archetype
        self._archetype_dict = dict()
        for archetype in archetypes:
            self._archetype_dict[archetype.archetype_id.value] = archetype
        super().__init__()

    def get_archetype_by_id(self, arch_id: ArchetypeID):
        return self._archetype_dict.get(arch_id.value)
