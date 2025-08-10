from abc import ABC, abstractmethod

class MeasurementService(ABC):
    """Defines an object providing proxy access to a measurement information service."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def is_valid_units_string(self, units: str) -> bool:
        """True if the units string 'units' is a valid string according to the HL7 UCUM specification."""
        pass

    @abstractmethod
    def units_equivalent(self, units1: str, units2: str) -> bool:
        """True if two units strings correspond to the same measured property."""
        pass