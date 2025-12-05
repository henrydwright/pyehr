"""`ehr` contains the top level structure, the EHR, which consists of an 
EHR_ACCESS object, an EHR_STATUS object, versioned data containers in the form 
of VERSIONED_COMPOSITIONs, optionally indexed by one or more hierarchical FOLDER 
structures. A collection of CONTRIBUTIONs which document the changes to the EHR 
over time is also included."""

from typing import Optional

from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime

class EHR(AnyClass):
    """The EHR object is the root object and access point of an EHR for a subject 
    of care."""

    system_id: HierObjectID
    """The identifier of the logical EHR management system in which this EHR was 
    created."""

    ehr_id: HierObjectID
    """The unique identifier of this EHR.
    
    Note: it is strongly recommended that a UUID always be used for this field."""

    contributions: Optional[list[ObjectRef]]
    """List of contributions causing changes to this EHR. Each contribution 
    contains a list of versions, which may include references to any number 
    of VERSION instances, i.e. items of type VERSIONED_COMPOSITION and 
    VERSIONED_FOLDER."""

    ehr_status: ObjectRef
    """Reference to EHR_STATUS object for this EHR."""

    ehr_access: ObjectRef
    """Reference to EHR_ACCESS object for this EHR."""

    compositions: Optional[list[ObjectRef]]
    """Master list of all Versioned Composition references in this EHR."""

    time_created: DVDateTime
    """Time of creation of the EHR."""

    folders: Optional[list[ObjectRef]]
    """Optional additional Folder structures for this EHR. If set, the _directory_ 
    attribute refers to the first member."""

    def _get_directory(self):
        if self.folders is None:
            return None
        else:
            return self.folders[0]

    directory = property(fget=_get_directory)
    """Optional directory structure for this EHR. If present, this is 
    a reference to the first member of _folders_."""

    def __init__(self,
                 system_id: HierObjectID,
                 ehr_id: HierObjectID,
                 ehr_status: ObjectRef,
                 ehr_access: ObjectRef,
                 time_created: DVDateTime,
                 contributions: Optional[list[ObjectRef]] = None,
                 compositions: Optional[list[ObjectRef]] = None,
                 folders: Optional[list[ObjectRef]] = None,
                    **kwargs):
        self.system_id = system_id
        self.ehr_id = ehr_id
        if ehr_status.ref_type != "VERSIONED_EHR_STATUS":
            raise ValueError("ehr_status must reference type VERSIONED_EHR_STATUS (invariant: ehr_status_valid)")
        self.ehr_status = ehr_status
        if ehr_access.ref_type != "VERSIONED_EHR_ACCESS":
            raise ValueError("ehr_access must reference type VERSIONED_EHR_ACCESS (invariant: ehr_access_valid)")
        self.ehr_access = ehr_access
        self.time_created = time_created
        if contributions is not None:
            if len(contributions) == 0:
                raise ValueError("If contributions is provided it cannot be an empty list (invariant: contributions_valid)")
            else:
                for oref in contributions:
                    if oref.ref_type != "CONTRIBUTION":
                        raise ValueError("All references in contributions must be to type CONTRIBUTION (invariant: contributions_valid)")
        self.contributions = contributions
        if compositions is not None:
            if len(compositions) == 0:
                raise ValueError("If compositions is provided it cannot be an empty list (invariant: compositions_valid)")
            else:
                for oref in compositions:
                    if oref.ref_type != "VERSIONED_COMPOSITION":
                        raise ValueError("All references in compositions must be to type VERSIONED_COMPOSITION (invariant: compositions_valid)")
        self.compositions = compositions
        if folders is not None:
            if len(folders) == 0:
                raise ValueError("If folders is provided it cannot be an empty list (invariant: directory_in_folders)")
            else:
                for oref in folders:
                    if oref.ref_type != "VERSIONED_FOLDER":
                        raise ValueError("All references in folders must be to type VERSIONED_FOLDER (invariant: folders_valid)")
        self.folders = folders
        super().__init__(**kwargs)

    def is_equal(self, other: 'EHR'):
        return (
            type(self) == type(other) and
            is_equal_value(self.system_id, other.system_id) and
            is_equal_value(self.ehr_id, other.ehr_id) and
            is_equal_value(self.contributions, other.contributions) and
            is_equal_value(self.ehr_status, other.ehr_status) and
            is_equal_value(self.ehr_access, other.ehr_access) and
            is_equal_value(self.compositions, other.compositions) and
            is_equal_value(self.time_created, other.time_created) and
            is_equal_value(self.folders, other.folders)
        )
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Ehr/EHR.json
        # TODO: mismatch between JSON spec and RM spec as to whether contributions required or not, taking RM
        draft = {
            "system_id": self.system_id.as_json(),
            "ehr_id": self.ehr_id.as_json(),
            "time_created": self.time_created.as_json(),
            "ehr_access": self.ehr_access.as_json(),
            "ehr_status": self.ehr_status.as_json()
        }
        if self.contributions is not None:
            draft["contributions"] = [c.as_json() for c in self.contributions]
        if self.compositions is not None:
            draft["compositions"] = [c.as_json() for c in self.compositions]
        if self.folders is not None:
            draft["folders"] = [f.as_json() for f in self.folders]
            draft["directory"] = self.directory.as_json()
        draft["_type"] = "EHR"
        return draft