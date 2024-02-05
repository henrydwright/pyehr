from enum import Enum

import numpy as np

class BaseDefinitions:
    """Defines globally used constant values."""

    CR : np.uint8 = np.array('\015', 'c')
    """Carriage return character."""
    LF : np.uint8 = np.array('\012', 'c')
    """Line feed character."""
    ANY_TYPE_NAME = "Any"
    REGEX_ANY_PATTERN = "*"
    DEFAULT_ENCODING = "UTF-8"
    NONE_TYPE_NAME = "None"

class OpenEHRDefinitions(BaseDefinitions):
    """Inheritance class to provide access to constants defined in other packages."""

    local_terminology_id : str = "local"
    """Predefined terminology identifier to indicate it is local to the knowledge 
    resource in which it occurs, e.g. an archetype"""

class ValidityKind(Enum):
    """An enumeration of three values that may commonly occur in constraint models.
    
    Use as the type of any attribute within this model, which expresses constraint 
    on some attribute in a class in a reference model. For example to indicate 
    validity of Date/Time fields."""

    MANDATORY = "mandatory"
    """Constant to indicate mandatory presence of something."""
    
    OPTIONAL = "optional"
    """Constant to indicate optional presence of something."""
    
    PROHIBITED = "prohibited"
    """Constant to indicate disallowed presence of something."""

class VersionStatus(Enum):
    """Status of a versioned artefact, as one of a number of possible values: 
    uncontrolled, prerelease, release, build."""

    ALPHA = "alpha"
    """Value representing a version which is 'unstable', i.e. contains 
    an unknown size of change with respect to its base version. 
    Rendered with the build number as a string in the form N.M.P-alpha.B 
    e.g. 2.0.1-alpha.154."""

    BETA = "beta"
    """Value representing a version which is 'beta', i.e. contains 
    an unknown but reducing size of change with respect to its base version. 
    Rendered with the build number as a string in the form N.M.P-beta.B 
    e.g. 2.0.1-beta.154."""

    RELEASE_CANDIDATE = "release_candidate"
    """Value representing a version which is 'release candidate', 
    i.e. contains only patch-level changes on the base version. 
    Rendered as a string as N.M.P-rc.B e.g. 2.0.1-rc.27."""

    RELEASED = "released"
    """Value representing a version which is 'released', i.e. is the 
    definitive base version. N.M.P e.g. 2.0.1."""

    BUILD = "build"
    """Value representing a version which is a build of the 
    current base release. Rendered with the build number as a string 
    in the form N.M.P+B e.g. 2.0.1+33."""