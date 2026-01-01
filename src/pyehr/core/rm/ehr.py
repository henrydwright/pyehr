"""`ehr` contains the top level structure, the EHR, which consists of an 
EHR_ACCESS object, an EHR_STATUS object, versioned data containers in the form 
of VERSIONED_COMPOSITIONs, optionally indexed by one or more hierarchical FOLDER 
structures. A collection of CONTRIBUTIONs which document the changes to the EHR 
over time is also included."""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, UIDBasedID
from pyehr.core.rm.common.generic import PartySelf
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.data_structures.item_structure import ItemStructure
from pyehr.core.rm.common.archetyped import Locatable, Archetyped, Link, FeederAudit, Pathable
from pyehr.core.rm.common.change_control import VersionedObject
from pyehr.core.rm.composition import Composition

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
    
class EHRStatus(Locatable):
    """Single object per EHR containing various EHR-wide status flags and settings,
    including whether this EHR can be queried, modified etc. This object is always
    modifiable, in order to change the status of the EHR as a whole.

    Note: It is strongly recommended that the inherited attribute uid be populated
    in EHR_STATUS objects, using the UID copied from the object_id() of the uid 
    field of the enclosing VERSION object.
    
    For example, the ORIGINAL_VERSION.uid 
    87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2 would be copied to the 
    uid field of the EHR_STATUS object."""

    subject: PartySelf
    """The subject of this EHR. The external_ref attribute can be used to contain 
    a direct reference to the subject in a demographic or identity service. 
    Alternatively, the association between patients and their records may be done 
    elsewhere for security reasons."""

    is_queryable: bool
    """True if this EHR should be included in population queries, i.e. if this 
    EHR is considered active in the population."""

    is_modifiable: bool
    """True if the EHR, other than the EHR_STATUS object, is allowed to be written
    to. The EHR_STATUS object itself can always be written to."""

    other_details: Optional[ItemStructure]
    """Any other details of the EHR summary object, in the form of an archetyped 
    ITEM_STRUCTURE."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                subject: PartySelf,
                is_queryable: bool,
                is_modifiable: bool,
                archetype_details : Archetyped,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                feeder_audit : Optional[FeederAudit] = None,
                other_details: Optional[ItemStructure] = None,
                **kwargs):
        self.subject = subject
        self.is_queryable = is_queryable
        self.is_modifiable = is_modifiable
        self.other_details = other_details
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, None, None, **kwargs)

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Ehr/EHR_STATUS.json
        draft = super().as_json()
        draft["subject"] = self.subject.as_json()
        draft["is_queryable"] = self.is_queryable
        draft["is_modifiable"] = self.is_modifiable
        if self.other_details is not None:
            draft["other_details"] = self.other_details.as_json()
        draft["_type"] = "EHR_STATUS"
        return draft
    
    def is_equal(self, other: 'EHRStatus'):
        return (super().is_equal(other) and
                self.subject.is_equal(other.subject) and
                self.is_queryable == other.is_queryable and
                self.is_modifiable == other.is_modifiable and
                self.other_details == other.other_details)
    
    def item_at_path(self, a_path):
        if a_path == "":
            return self
        elif a_path == "subject":
            return self.subject
        elif a_path == "is_queryable":
            return self.is_queryable
        elif a_path == "is_modifiable":
            return self.is_modifiable
        elif a_path == "other_details":
            return self.other_details
        else:
            raise ValueError("Item not found: \'{a_path}\' not an attribute of EHR_STATUS")
        
    def items_at_path(self, a_path):
        raise ValueError("Items not found: EHR_STATUS only has individual items")
    
    def path_unique(self, a_path):
        return a_path in ["", "subject", "is_queryable", "is_modifiable", "other_details"]
    
    def path_exists(self, a_path):
        return self.path_unique(a_path)
    
class AccessControlSettings(AnyClass):
    """Access Control Settings for the EHR and components. Intended to support 
    multiple access control schemes. Currently implementation dependent."""

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def is_equal(self, other):
        pass

class EHRAccess(Locatable):
    """EHR-wide access control object. All access decisions to data in the EHR must
    be made in accordance with the policies and rules in this object.

    Note: It is strongly recommended that the inherited attribute uid be populated
    in EHR_ACCESS objects, using the UID copied from the object_id() of the uid 
    field of the enclosing VERSION object.
    
    For example, the ORIGINAL_VERSION.uid 
    87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2 would be copied to the uid 
    field of the EHR_ACCESS object."""

    settings: Optional[AccessControlSettings]
    """Access control settings for the EHR. Instance is a subtype of the type 
    `ACCESS_CONTROL_SETTINGS`, allowing for the use of different access control 
    schemes."""

    def __init__(self, 
                 name: DVText, 
                 archetype_node_id: str, 
                 archetype_details : Archetyped,
                 uid : Optional[UIDBasedID] = None, 
                 links : Optional[list[Link]] = None,  
                 feeder_audit : Optional[FeederAudit] = None,
                 **kwargs):
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, None, None, **kwargs)

    def scheme(self):
        """The name of the access control scheme in use; corresponds to the 
        concrete instance of the settings attribute."""
        return "pyehr"
    
    def is_equal(self, other: 'EHRAccess'):
        return (super().is_equal(other) and
                self.settings.is_equal(other.settings))
    
    def as_json(self):
        draft = super().as_json()
        if self.settings is not None:
            draft["settings"] = self.settings.as_json()
        draft["_type"] = "EHR_ACCESS"

class VersionedEHRAccess(VersionedObject[EHRAccess]):
    """Version container for EHR_ACCESS instance."""
    pass

class VersionedEHRStatus(VersionedObject[EHRStatus]):
    """Version container for EHR_STATUS instance."""
    pass

class VersionedComposition(VersionedObject[Composition]):
    """Version-controlled composition abstraction, defined by inheriting VERSIONED_OBJECT<COMPOSITION>."""

    def is_persistent(self) -> bool:
        """Indicates whether this composition set is persistent; derived from first version."""
        first_version_id = self.all_version_ids[0]
        first_version = self.version_with_id(first_version_id)
        return first_version.data().is_persistent()