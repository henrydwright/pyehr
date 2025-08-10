from org.openehr.rm.support.measurement import MeasurementService
from org.openehr.rm.support.terminology import TerminologyService

class ExternalEnvironmentAccess(TerminologyService, MeasurementService):
    """A mixin class providing access to services in the external environment."""

    def __init__(self):
        super(MeasurementService).__init__()
        super(TerminologyService).__init__()