"""Formal version control and change management are used in openEHR to support 
the construction of EHR and other repositories requiring the properties of consistency, 
indelibility, traceability and distributed sharing. The `change_control` package supplies 
the formal specification of these features in openEHR."""

from abc import abstractmethod
import base64
from typing import Optional, Union
import json
import warnings

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import numpy as np

from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, ObjectVersionID, UID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.generic import AuditDetails, Attestation, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVCodedText
from pyehr.core.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

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
        if "signature" in self_json:
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
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/ORIGINAL_VERSION.json
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
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/IMPORTED_VERSION.json
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

    _versions_id_lookup: dict[str, Version]
    """Dict of versions, mapped from object version ID (in str form) to version"""

    _versions_time_lookup: dict[str, Version]
    """Dict of versions, mapped from date time (in str form) to version"""

    _revision_history: RevisionHistory
    """Revision history for this versioned object"""

    def __init__(self, uid: HierObjectID, owner_id: ObjectRef, time_created: DVDateTime, revision_history_and_versions: Optional[tuple[RevisionHistory, list[Version]]] = None, **kwargs):
        if uid.has_extension():
            raise ValueError("UID of a versioned object cannot have an extension (invariant: uid_validity)")
        
        self.uid = uid
        self.owner_id = owner_id
        self.time_created = time_created
        self._version_ids = list()
        self._versions_id_lookup = dict()
        self._versions_time_lookup = dict()
        if revision_history_and_versions is None:
            self._revision_history = RevisionHistory([])
        else:
            self._revision_history = revision_history_and_versions[0]
            versions_list = revision_history_and_versions[1]
            for version in versions_list:
                self._version_ids.append(version.uid())
                self._versions_id_lookup[version.uid().value] = version
                self._versions_time_lookup[version.commit_audit.time_committed.as_string()] = version
                
        super().__init__(**kwargs)

    def version_count(self) -> np.int32:
        """Return the total number of versions in this object."""
        return len(self._version_ids)

    def all_version_ids(self) -> list[ObjectVersionID]:
        """Return a list of ids of all versions in this object in most-recent last order."""
        return self._version_ids

    def all_versions(self) -> list[Version[T]]:
        """Return a list of all versions in this object."""
        return list(self._versions_id_lookup.values())

    def has_version_at_time(self, a_time: DVDateTime) -> bool:
        """True if a version for time `a_time` exists."""
        # TODO: this is the stricter semantic (i.e. "at time X, was a version committed?")
        #        but a time machine (i.e. "at time X, was there a latest version?") may be preferable
        #        spec is unclear so leave this as a note to maybe come back to later
        return (a_time.as_string() in self._versions_time_lookup)

    def has_version_id(self, a_version_uid: ObjectVersionID) -> bool:
        """True if a version with `a_version_uid` exists."""
        return (a_version_uid.value in self._versions_id_lookup)

    def version_with_id(self, a_version_uid: ObjectVersionID) -> Version[T]:
        """Return the version with `uid` = `a_version_uid`."""
        if self.has_version_id(a_version_uid):
            return self._versions_id_lookup[a_version_uid.value]
        else:
            raise KeyError(f"Version with ID \'{a_version_uid.value}\' not in versioned object \'{self.uid.value}\'")

    def is_original_version(self, a_version_uid: ObjectVersionID) -> bool:
        """True if version with `a_version_uid` is an `ORIGINAL_VERSION`."""
        try:
            ver = self.version_with_id(a_version_uid)
            return isinstance(ver, OriginalVersion)
        except KeyError:
            raise ValueError(f"Version with ID \'{a_version_uid.value}\' could not be checked as not in versioned object \'{self.uid.value}\'")

    def version_at_time(self, a_time: DVDateTime) -> Version[T]:
        """Return the version for time `a_time`."""
        if self.has_version_at_time(a_time):
            return self._versions_time_lookup[a_time.as_string()]
        else:
            raise KeyError(f"No version committed at exact time \'{a_time.as_string()}\' exists in versioned object \'{self.uid.value}\'")

    def revision_history(self) -> RevisionHistory:
        """History of all audits and attestations in this versioned repository."""
        return self._revision_history

    def latest_version(self) -> Optional[Version[T]]:
        """Return the most recently added version (i.e. on trunk or any branch)."""
        if self.version_count() == 0:
            return None
        else:
            latest_id = self._version_ids[-1]
            return self._versions_id_lookup[latest_id.value]

    def latest_trunk_version(self) -> Optional[Version[T]]:
        """Return the most recently added trunk version."""
        if self.version_count() == 0:
            return None
        else:
            for ver_id in reversed(self._version_ids):
                if not ver_id.is_branch():
                    return self._versions_id_lookup[ver_id.value]

    def trunk_lifecycle_state(self) -> Optional[DVCodedText]:
        """Return the lifecycle state from the latest trunk version. Useful for 
        determining if the version container is logically deleted."""
        return self.latest_trunk_version().lifecycle_state() if self.version_count() > 0 else None

    def _pre_version_commit_checks(self, 
                                   new_version_uid: ObjectVersionID,
                                   preceding_version_uid: Optional[ObjectVersionID]):
        """Run some checks common to version commits"""
        # check new version UID matches this version container UID
        if not new_version_uid.root().is_equal(self.uid.root()):
            raise ValueError("New version UID does not match versioned object UID (did you add this version to the wrong versioned object?)")
        
        # check predecessor ID is in the versions_id_lookup (or first version)
        if preceding_version_uid is not None:
            if self.version_count() == 0:
                raise ValueError("First version must have preceding_version_uid set to None")
            elif not (preceding_version_uid.value in self._versions_id_lookup):
                raise ValueError("The provided preceding version UID does not exist in this versioned object (did you commit out of order?)")
        else:
            if self.version_count() != 0:
                raise ValueError("Subsequent versions cannot have preceding_version_uid set to None")
        
    def _revision_history_add(self, obj_uid: ObjectVersionID, new_audit: AuditDetails):
        # see if RHI already exists for this obj_uid
        for rhi in self._revision_history.items:
            if rhi.version_id.is_equal(obj_uid):
                # already exists
                rhi.audits.append(new_audit)
                return
        
        # doesn't already exist
        self._revision_history.items.append(RevisionHistoryItem(obj_uid, [new_audit]))


    def _commit_original_version_all(self,
                                    a_contribution: ObjectRef,
                                    a_new_version_uid: ObjectVersionID,
                                    a_preceding_version_id: Optional[ObjectVersionID],
                                    an_audit: AuditDetails,
                                    a_lifecycle_state: DVCodedText,
                                    a_data: T,
                                    terminology_service: TerminologyService,
                                    an_other_input_uids: Optional[list[ObjectVersionID]] = None,
                                    signing_key: Optional[str] = None) -> OriginalVersion:
        
        self._pre_version_commit_checks(a_new_version_uid, a_preceding_version_id)
        ov = OriginalVersion(
            contribution=a_contribution,
            commit_audit=an_audit,
            uid=a_new_version_uid,
            lifecycle_state=a_lifecycle_state,
            terminology_service=terminology_service,
            data=a_data,
            preceding_version_uid=a_preceding_version_id,
            other_input_version_uids=an_other_input_uids
        )
        if signing_key is not None:
            warnings.warn("Signing is not supported, signing key provided but ignored", RuntimeWarning)
        
        self._version_ids.append(ov.uid())
        self._versions_id_lookup[ov.uid().value] = ov
        self._versions_time_lookup[an_audit.time_committed.as_string()] = ov
        self._revision_history_add(ov.uid(), an_audit)

        return ov

    def commit_original_version(self,
                                a_contribution: ObjectRef,
                                a_new_version_uid: ObjectVersionID,
                                a_preceding_version_id: Optional[ObjectVersionID],
                                an_audit: AuditDetails,
                                a_lifecycle_state: DVCodedText,
                                a_data: T,
                                terminology_service: TerminologyService,
                                signing_key: Optional[str] = None) -> OriginalVersion:
        """Add a new original version."""
        return self._commit_original_version_all(a_contribution, a_new_version_uid, a_preceding_version_id, an_audit, a_lifecycle_state, a_data, terminology_service, signing_key=signing_key)

    def commit_original_merged_version(self,
                                a_contribution: ObjectRef,
                                a_new_version_uid: ObjectVersionID,
                                a_preceding_version_id: Optional[ObjectVersionID],
                                an_audit: AuditDetails,
                                a_lifecycle_state: DVCodedText,
                                a_data: Optional[T],
                                an_other_input_uids: list[ObjectVersionID],
                                terminology_service: TerminologyService,
                                signing_key: Optional[str] = None) -> OriginalVersion:
        """Add a new original merged version. This commit function adds a 
        parameter containing the ids of other versions merged into the current one."""
        return self._commit_original_version_all(a_contribution, a_new_version_uid, a_preceding_version_id, an_audit, a_lifecycle_state, a_data, terminology_service, an_other_input_uids=an_other_input_uids, signing_key=signing_key)

    def commit_imported_version(self,
                                a_contribution: ObjectRef,
                                an_audit: AuditDetails,
                                a_version: OriginalVersion[T]) -> ImportedVersion:
        """Add a new imported version. Details of version id etc come from the 
        ORIGINAL_VERSION being committed."""
        self._pre_version_commit_checks(a_version.uid(), a_version.preceding_version_uid())
        iv = ImportedVersion(
            contribution=a_contribution,
            commit_audit=an_audit,
            item=a_version
        )
        self._version_ids.append(iv.uid())
        self._versions_id_lookup[iv.uid().value] = iv
        self._versions_time_lookup[an_audit.time_committed.as_string()] = iv
        self._revision_history_add(iv.uid(), an_audit)

        return iv

    def commit_attestation(self,
                           an_attestation: Attestation,
                           a_ver_id: ObjectVersionID,
                           signing_key: Optional[str] = None):
        """Add a new attestation to a specified original version. Attestations 
        can only be added to Original versions."""
        if signing_key is not None:
            warnings.warn("Signing is not supported, signing key provided but ignored", RuntimeWarning)
        
        if self.has_version_id(a_ver_id):
            if self.is_original_version(a_ver_id):
                ov = self.version_with_id(a_ver_id)
                if ov.attestations is None:
                    ov.attestations = []
                ov.attestations.append(an_attestation)
                self._revision_history_add(ov.uid(), an_attestation)
            else:
                raise ValueError(f"Could not add attestation as version id \'{a_ver_id.value}\' is not an ORIGINAL_VERSION")
        else:
            raise ValueError(f"Could not add attestation as version id \'{a_ver_id.value}\' did not exist in versioned object \'{self.uid.value}\'")

    def is_equal(self, other):
        return (
            type(self) == type(other) and
            is_equal_value(self.uid, other.uid) and
            is_equal_value(self.owner_id, other.owner_id) and
            is_equal_value(self.time_created, other.time_created) and
            is_equal_value(self._versions_id_lookup, other._versions_id_lookup)
        )
    
    def as_json(self, include_revision_history=False, include_versions=False):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Common/VERSIONED_OBJECT.json
        draft = {
            "uid": self.uid.as_json(),
            "owner_id": self.owner_id.as_json(),
            "time_created": self.time_created.as_json()
        }
        if include_revision_history:
            draft["revision_history"] = self._revision_history.as_json()
        if include_versions:
            draft["versions"] = [v.as_json() for v in self._versions_id_lookup.values()]
        draft["_type"] = "VERSIONED_OBJECT"
        return draft

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

    def is_equal(self, other: 'Contribution'):
        return (
            type(self) == type(other) and
            is_equal_value(self.uid, other.uid) and
            is_equal_value(self.versions, other.versions) and
            is_equal_value(self.audit, other.audit)
        )
    
    def as_json(self):
        return {
            "uid": self.uid.as_json(),
            "audit": self.audit.as_json(),
            "versions": [version.as_json() for version in self.versions],
            "_type": "CONTRIBUTION"
        }
