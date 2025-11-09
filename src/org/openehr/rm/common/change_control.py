"""Formal version control and change management are used in openEHR to support 
the construction of EHR and other repositories requiring the properties of consistency, 
indelibility, traceability and distributed sharing. The `change_control` package supplies 
the formal specification of these features in openEHR."""

from abc import abstractmethod
from typing import Optional, Union
import json

import numpy as np

from org.openehr.base.base_types.identification import HierObjectID, ObjectRef, ObjectVersionID, UID
from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.rm.common.generic import AuditDetails, Attestation, RevisionHistory
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_types.text import DVCodedText
from org.openehr.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

class Version[T: AnyClass](AnyClass):
    """Abstract model of one Version within a Version container, containing data, commit audit 
    trail, and the identifier of its Contribution."""

    contribution: ObjectRef
    """Contribution in which this version was added."""

    signature: Optional[str]
    """OpenPGP digital signature or digest of content committed in this Version."""

    commit_audit: AuditDetails
    """Audit trail corresponding to the committal of this version to the VERSIONED_OBJECT."""

    @abstractmethod
    def __init__(self, contribution: ObjectRef, commit_audit: AuditDetails, signature: Optional[str] = None, **kwargs):
        self.contribution = contribution
        self.signature = signature
        self.commit_audit = commit_audit
        super().__init__(**kwargs)

    @abstractmethod
    def uid(self) -> ObjectVersionID:
        """Unique identifier of this VERSION, in the form of an {object_id, a version_tree_id, 
        creating_system_id} triple, where the object_id has the same value as the containing 
        VERSIONED_OBJECT uid."""
        pass

    @abstractmethod
    def preceding_version_uid(self) -> Optional[ObjectVersionID]:
        """Unique identifier of the version of which this version is a modification; Void if 
        this is the first version."""
        pass

    @abstractmethod
    def data(self) -> T:
        """The data of this Version. Original content of this Version."""
        pass

    @abstractmethod
    def lifecycle_state(self) -> DVCodedText:
        """Lifecycle state of this version; coded by openEHR vocabulary `version lifecycle state`."""
        pass

    def canonical_form(self) -> str:
        """A canonical serial form of this Version, suitable for generating reliable hashes and
        signatures. Canonical form of Version object, created by serialising all attributes 
        except signature."""
        self_json = self.as_json()
        # remove signature from serialisation
        del self_json["signature"]
        return json.dumps(self_json)

    @abstractmethod
    def owner_id(self) -> HierObjectID:
        """Copy of the owning VERSIONED_OBJECT.uid value; extracted from the local uid 
        property's object_id."""
        pass

    @abstractmethod
    def is_branch(self) -> bool:
        """True if this Version represents a branch. Derived from uid attribute."""
        pass

    @abstractmethod
    def is_equal(self, other: 'Version'):
        return (
            type(self) == type(other) and
            is_equal_value(self.contribution, other.contribution) and
            is_equal_value(self.signature, other.signature) and
            is_equal_value(self.commit_audit, other.commit_audit)
        )
    
    def as_json(self):
        draft = {
            "contribution": self.contribution.as_json(),
            "commit_audit": self.commit_audit.as_json()
        }
        if self.signature is not None:
            draft["signature"] = self.signature
        return draft


class OriginalVersion[T: AnyClass](Version[T]):
    """A Version containing locally created content and optional attestations."""

    uid_var: ObjectVersionID
    """Stored version of inheritance precursor."""

    preceding_version_uid_var: Optional[ObjectVersionID]
    """Stored version of inheritance precursor."""

    other_input_version_uids: Optional[list[ObjectVersionID]]
    """Identifiers of other versions whose content was merged into this version, if any."""

    lifecycle_state_var: DVCodedText
    """Lifecycle state of the content item in this version; coded by openEHR vocabulary `version lifecycle state`."""

    attestations: Optional[list[Attestation]]
    """Set of attestations relating to this version."""

    data_var: Optional[T]
    """Data content of this Version."""

    def __init__(self, 
                 contribution: ObjectRef, 
                 commit_audit: AuditDetails, 
                 uid: ObjectVersionID,
                 lifecycle_state: DVCodedText,
                 terminology_service: TerminologyService,
                 data: Optional[T] = None,
                 preceding_version_uid: Optional[ObjectVersionID] = None,
                 other_input_version_uids: Optional[list[ObjectVersionID]] = None,
                 attestations: Optional[list[Attestation]] = None,
                 signature: Optional[str] = None, **kwargs):
        self.uid_var = uid

        util_verify_code_in_openehr_terminology_group_or_error(
            code=lifecycle_state.defining_code,
            terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_VERSION_LIFE_CYCLE_STATE,
            terminology_service=terminology_service,
            invariant_name_for_error="lifecycle_state_valid"
        )
        self.lifecycle_state_var = lifecycle_state
        self.data_var = data
        self.preceding_version_uid_var = preceding_version_uid

        if (other_input_version_uids is not None and len(other_input_version_uids) == 0):
            raise ValueError("If provided, other_input_version_uids cannot be an empty list (invariant: other_input_version_uids_valid)")
        self.other_input_version_uids = other_input_version_uids

        if (attestations is not None and len(attestations) == 0):
            raise ValueError("If provided, attestations cannot be an empty list (invariant: attestations_valid)")
        self.attestations = attestations
        super().__init__(contribution, commit_audit, signature, **kwargs)

    def is_merged(self) -> bool:
        """True if this Version was created from more than just the preceding (checked out) version."""
        return (self.other_input_version_uids is not None)

    def data(self):
        return self.data_var
    
    def is_equal(self, other: 'OriginalVersion'):
        return (
            super().is_equal(other) and
            is_equal_value(self.uid_var, other.uid_var) and
            is_equal_value(self.preceding_version_uid_var, other.preceding_version_uid_var) and
            is_equal_value(self.other_input_version_uids, other.other_input_version_uids) and
            is_equal_value(self.lifecycle_state_var, other.lifecycle_state_var) and
            is_equal_value(self.attestations, other.attestations) and
            is_equal_value(self.data_var, other.data_var)
            )

    def is_branch(self):
        return self.uid_var.version_tree_id().is_branch()

    def lifecycle_state(self):
        return self.lifecycle_state_var
    
    def owner_id(self):
        return self.uid_var.object_id()
    
    def preceding_version_uid(self):
        return self.preceding_version_uid_var
    
    def uid(self):
        return self.uid_var
    
    def as_json(self):
        draft = super().as_json()
        draft["uid"] = self.uid_var.as_json()
        draft["lifecycle_state"] = self.lifecycle_state_var.as_json()
        if self.preceding_version_uid_var is not None:
            draft["preceding_version_uid"] = self.preceding_version_uid_var.as_json()
        if self.other_input_version_uids is not None:
            draft["other_input_version_uids"] = [other_input_version_uid.as_json() for other_input_version_uid in self.other_input_version_uids]
        if self.attestations is not None:
            draft["attestations"] = [attestation.as_json() for attestation in self.attestations]
        if self.data_var is not None:
            draft["data"] = self.data_var.as_json()
        draft["_type"] = "ORIGINAL_VERSION"
        return draft

class ImportedVersion[T: AnyClass](Version[T]):
    """Versions whose content is an ORIGINAL_VERSION copied from another location; this 
    class inherits commit_audit and contribution from VERSION<T>, providing imported versions 
    with their own audit trail and Contribution, distinct from those of the imported ORIGINAL_VERSION."""

    item: OriginalVersion[T]
    """The ORIGINAL_VERSION object that was imported."""

    def __init__(self, 
                 contribution: ObjectRef, 
                 commit_audit: AuditDetails, 
                 item: OriginalVersion[T],
                 signature: Optional[str] = None, **kwargs):
        self.item = item
        super().__init__(contribution, commit_audit, signature, **kwargs)

    def uid(self) -> ObjectVersionID:
        """Computed version of inheritance precursor, derived as item.uid."""
        return self.item.uid()

    def preceding_version_uid(self):
        """Computed version of inheritance precursor, derived as item.preceding_version_uid."""
        return self.item.preceding_version_uid()

    def lifecycle_state(self):
        """Lifecycle state of the content item in wrapped ORIGINAL_VERSION, derived as 
        item.lifecycle_state; coded by openEHR vocabulary version lifecycle state."""
        return self.item.lifecycle_state()

    def data(self) -> T:
        """Original content of this Version."""
        return self.item.data()

    def is_branch(self):
        return self.item.is_branch()

    def is_equal(self, other):
        return (
            super().is_equal(other) and
            is_equal_value(self.item, other.item)
        )
    
    def owner_id(self):
        return self.item.owner_id()

    def as_json(self):
        draft = super().as_json()
        draft["item"] = self.item.as_json()
        draft["_type"] = "IMPORTED_VERSION"
        return draft

class VersionedObject[T: AnyClass](AnyClass):
    """Version control abstraction, defining semantics for versioning one complex object."""

    uid: HierObjectID
    """Unique identifier of this version container in the form of a UID with no extension. 
    This id will be the same in all instances of the same container in a distributed 
    environment, meaning that it can be understood as the uid of the virtual version tree."""

    owner_id: ObjectRef
    """Reference to object to which this version container belongs, e.g. the id of the 
    containing EHR or other relevant owning entity."""

    time_created: DVDateTime
    """Time of initial creation of this versioned object."""
    
    _version_ids: list[ObjectVersionID]
    """List of object version IDs kept in most-recent last order"""

    _version_dict: dict[UID, dict[str, Union[dict[str, Version[T], Version[T]]]]]
    """Creating system ID -> (Trunk version -> (Version[T] OR branch number.branch version -> Version[T]))"""

    def __init__(self, uid: HierObjectID, owner_id: ObjectRef, time_created: DVDateTime, **kwargs):
        self.uid = uid
        self.owner_id = owner_id
        self.time_created = time_created
        super().__init__(**kwargs)

    def version_count(self) -> np.int32:
        """Return the total number of versions in this object."""
        pass

    def all_version_ids(self) -> list[ObjectVersionID]:
        """Return a list of ids of all versions in this object."""
        pass

    def all_versions(self) -> list[Version[T]]:
        """Return a list of all versions in this object."""
        pass

    def has_version_at_time(self, a_time: DVDateTime) -> bool:
        """True if a version for time `a_time` exists."""
        pass

    def version_with_id(self, a_version_uid: ObjectVersionID) -> Version[T]:
        """Return the version with `uid` = `a_version_uid`."""
        pass

    def is_original_version(self, a_version_uid: ObjectVersionID) -> bool:
        """True if version with `a_version_uid` is an `ORIGINAL_VERSION`."""
        pass

    def version_at_time(self, a_time: DVDateTime) -> Version[T]:
        """Return the version for time `a_time`."""
        pass

    def revision_history(self) -> RevisionHistory:
        """History of all audits and attestations in this versioned repository."""
        pass

    def latest_version(self) -> Version[T]:
        """Return the most recently added version (i.e. on trunk or any branch)."""
        pass

    def latest_trunk_version(self) -> Version[T]:
        """Return the most recently added trunk version."""
        pass

    def trunk_lifecycle_state(self) -> DVCodedText:
        """Return the lifecycle state from the latest trunk version. Useful for 
        determining if the version container is logically deleted."""
        pass

    def commit_original_version(self,
                                a_contribution: ObjectRef,
                                a_new_version_uid: ObjectVersionID,
                                a_preceding_version_id: ObjectVersionID,
                                an_audit: AuditDetails,
                                a_lifecycle_state: DVCodedText,
                                a_data: T,
                                signing_key: str):
        """Add a new original version."""
        pass

    def commit_original_merged_version(self,
                                a_contribution: ObjectRef,
                                a_new_version_uid: ObjectVersionID,
                                a_preceding_version_id: ObjectVersionID,
                                an_audit: AuditDetails,
                                a_lifecycle_state: DVCodedText,
                                a_data: T,
                                an_other_input_uids: list[ObjectVersionID],
                                signing_key: str):
        """Add a new original merged version. This commit function adds a 
        parameter containing the ids of other versions merged into the current one."""
        pass

    def commit_imported_version(self,
                                a_contribution: ObjectRef,
                                an_audit: AuditDetails,
                                a_version: OriginalVersion[T]):
        """Add a new imported version. Details of version id etc come from the 
        ORIGINAL_VERSION being committed."""
        pass

    def commit_attestation(self,
                           an_attestation: Attestation,
                           a_ver_id: ObjectVersionID,
                           signing_key: str):
        """Add a new attestation to a specified original version. Attestations 
        can only be added to Original versions."""
        pass

class Contribution(AnyClass):
    """Documents a Contribution (change set) of one or more versions added to a 
    change-controlled repository."""

    uid: HierObjectID
    """Unique identifier for this Contribution."""

    versions: list[ObjectRef]
    """Set of references to Versions causing changes to this EHR. Each contribution 
    contains a list of versions, which may include paths pointing to any number of 
    versionable items, i.e. items of types such as COMPOSITION and FOLDER."""

    audit: AuditDetails
    """Audit trail corresponding to the committal of this Contribution."""

    def __init__(self, uid: HierObjectID, versions: list[ObjectRef], audit: AuditDetails, **kwargs):
        self.uid = uid
        self.versions = versions
        self.audit = audit
        super().__init__(**kwargs)

