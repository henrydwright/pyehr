from pyehr.core.rm.support.measurement import MeasurementService
from pyehr.core.rm.support.terminology import TerminologyService

__all__ = ['ExternalEnvironmentAccess']

class ExternalEnvironmentAccess(TerminologyService, MeasurementService):
    """A mixin class providing access to services in the external environment."""

    def __init__(self):
        super(MeasurementService).__init__()
        super(TerminologyService).__init__()