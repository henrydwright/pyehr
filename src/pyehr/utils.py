"""A set of utility functions useful for interacting with pyehr classes (descendents of AnyClass)."""

from typing import Optional

from pyehr.core.base.base_types.identification import ObjectID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.ehr import EHR

def get_uid_from_object_if_exists(obj: Optional[AnyClass]) -> Optional[ObjectID]:
    """Extract the UID from a UID object type"""
    if isinstance(obj, EHR):
        return obj.ehr_id
    uid = obj.uid
    if callable(uid):
        uid = obj.uid()
    return uid