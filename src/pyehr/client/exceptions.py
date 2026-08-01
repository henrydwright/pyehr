__all__ = ['OpenEHRRestClientError', 'OpenEHRRestOperationError', 'OpenEHRRestBadRequestError', 'OpenEHRRestObjectAlreadyExistsError', 'OpenEHRRestObjectNotFoundError', 'OpenEHRRestVersionMismatchError', 'OpenEHRRestConstraintError']


class OpenEHRRestClientError(RuntimeError):
    """Base class for any exception explicitly raised through use
    of any of the OpenEHRRestClients."""

    message: str

    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(*args)

class OpenEHRRestOperationError(OpenEHRRestClientError):
    """Base class for any error raised as a result of a server
    returning a 'non-successful' status code."""

    status_code : int
    response_body: str

    def __init__(self, message: str, status_code: int, response_body: str, *args):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message, *args)

class OpenEHRRestBadRequestError(OpenEHRRestOperationError):
    """Thrown when a status code is received showing that 
    an argument was likely invalid."""
    pass

class OpenEHRRestObjectAlreadyExistsError(OpenEHRRestOperationError):
    """Thrown when a status code is received showing that
    an object with one or more parameter matching the provided object
    already exists."""
    pass

class OpenEHRRestObjectNotFoundError(OpenEHRRestOperationError):
    """Thrown when a status code is received showing that
    the given object (or EHR to which the object will be attached) 
    does not exist"""
    pass

class OpenEHRRestVersionMismatchError(OpenEHRRestOperationError):
    """Thrown when a status code is received showing some
    issue relating to versioning (e.g. the preceding_version_uid
    not matching the latest version on the server)"""
    pass

class OpenEHRRestConstraintError(OpenEHRRestOperationError):
    """Thrown when a status code is received showing that
    either constraints could not be validated (e.g. unknown
    template or archetype_id) or were found not to be met
    (e.g. contents do not match template)"""
    pass
