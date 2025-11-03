"""The data_types.uri package includes two types used for referring to information resources."""

from org.openehr.rm.data_types import DataValue
from org.openehr.base.foundation_types.primitive_types import Uri

from uritools import urisplit

class DVUri(DataValue):
    """
    A reference to an object which structurally conforms to the Universal Resource Identifier (URI) RFC-3986 standard. The reference is contained in the value attribute, which is a `String`. So-called 'plain-text URIs' that contain RFC-3986 forbidden characters such as spaces etc, are allowed on the basis that they need to be RFC-3986 encoded prior to use in e.g. REST APIs or other contexts relying on machine-level conformance.
    """

    value : str
    """Value of URI as a String. 'Plain-text' URIs are allowed, enabling better readability, but must be RFC-3986 encoded in use."""

    def __init__(self, value: str):
        if value == "":
            raise ValueError("Uri cannot be empty string (invariant: value_valid)")
        
        self.value = Uri(value, allow_unencoded=True)
        super().__init__()

    def __str__(self):
        return self.value
    
    def is_equal(self, other):
        return (
            type(self) == type(other) and
            self.value == other.value
        )

    def scheme(self) -> str:
        """A distributed information 'space' in which information objects exist. The scheme simultaneously specifies an information space and a mechanism for accessing objects in that space. For example if scheme = "ftp", it identifies the information space in which all ftp-able objects exist, and also the application - ftp - which can be used to access them. Values may include: "ftp", "telnet", "mailto", etc. Refer to RFC-3986 for a full list."""
        return urisplit(self.value).scheme or ""

    def path(self) -> str:
        """A string whose format is a function of the scheme. Identifies the location in <scheme>-space of an information entity. Typical values include hierarchical directory paths for any machine. For example, with scheme = "ftp", path might be `"/pub/images/image_01"`. The strings "." and ".." are reserved for use in the path. Paths may include internet/intranet location identifiers of the form: `sub_domain...domain`, e.g. `"info.cern.ch"`."""
        return urisplit(self.value).path or ""

    def fragment_id(self) -> str:
        """A part of, a fragment or a sub-function within an object. Allows references to sub-parts of objects, such as a certain line and character position in a text object. The syntax and semantics are defined by the application responsible for the object."""
        return urisplit(self.value).fragment or ""

    def query(self) -> str:
        """Query string to send to application implied by scheme and path. Enables queries to applications, including databases to be included in the URI. Supports any query meaningful to the server, including SQL."""
        return urisplit(self.value).query or ""
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_URI.json
        return {
            "_type": "DV_URI",
            "value": self.value
        }
    
class DVEHRUri(DVUri):
    """A DV_EHR_URI is a DV_URI which has the scheme name 'ehr', and which can only reference items in EHRs.

    Used to reference items in an EHR, which may be the same as the current EHR (containing this link), or another."""

    EHR_SCHEME = "ehr"

    def __init__(self, value):
        super().__init__(value)
        if self.scheme() != self.EHR_SCHEME:
            raise ValueError(f"An EHR URI must have the scheme 'ehr' but the given scheme was \'{self.scheme()}\' (invariant: scheme_valid)")
        
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_types/DV_EHR_URI.json
        draft = super().as_json()
        draft["_type"] = "DV_EHR_URI"
        return draft