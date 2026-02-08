"""Additional types not part of the core RM, but used by REST APIs by both client and server
and part of the REST API specification."""

from typing import Optional
from pyehr.core.base.base_types.identification import GenericID, HierObjectID, ObjectRef, ObjectVersionID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion
from pyehr.core.rm.common.generic import Attestation, AuditDetails, PartyProxy
from pyehr.core.rm.data_types.encapsulated import DVMultimedia
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVCodedText, DVText
from pyehr.core.rm.data_types.uri import DVEHRUri
from pyehr.core.rm.support.terminology import TerminologyService

class UpdateAudit(AnyClass):
    """Similar to AUDIT_DETAILS but with reduced fields, used for clients
    to commit new ORIGINAL_VERSIONs to remote host (i.e. without certain audit details
    that are set by the server)"""

    _inner_audit_details : AuditDetails

    def __init__(self, 
                 change_type: DVCodedText, 
                 committer: PartyProxy, 
                 terminology_service: TerminologyService,
                 description: Optional[DVText] = None, 
                 **kwargs):
        self._inner_audit_details = AuditDetails(
            system_id="NULL",
            time_committed=DVDateTime("1970-01-01T00:00:00Z"),
            change_type=change_type,
            committer=committer,
            terminology_service=terminology_service,
            description=description
        )

    def as_json(self):
        draft = self._inner_audit_details.as_json()
        del draft["system_id"]
        del draft["time_committed"]
        draft["_type"] = "UPDATE_AUDIT"
        return draft
    
    def is_equal(self, other: 'UpdateAudit'):
        return self._inner_audit_details.is_equal(other._inner_audit_details)
    
    def as_audit_details(self):
        return self._inner_audit_details
    
class UpdateAttestation(AnyClass):
    """Similar to ATTESTATION but with reduced fields, used for clients to 
    commit new ORIGINAL_VERSIONs to remote host (i.e. without certain audit details
    that are set by the server)"""

    _inner_attestation : Attestation

    def __init__(self, 
                 change_type: DVCodedText, 
                 committer: PartyProxy, 
                 reason: DVText,
                 is_pending: bool,
                 terminology_service: TerminologyService,
                 description: Optional[DVText] = None, 
                 attested_view: Optional[DVMultimedia] = None,
                 proof: Optional[str] = None,
                 items: Optional[list[DVEHRUri]] = None,
                 **kwargs):
        self._inner_attestation = Attestation(
            system_id="NULL",
            time_committed=DVDateTime("1970-01-01T00:00:00Z"),
            change_type=change_type,
            committer=committer,
            reason=reason,
            is_pending=is_pending,
            terminology_service=terminology_service,
            description=description,
            attested_view=attested_view,
            proof=proof,
            items=items
        )

    def as_json(self):
        draft = self._inner_attestation.as_json()
        del draft["system_id"]
        del draft["time_committed"]
        draft["_type"] = "UPDATE_ATTESTATION"

    def is_equal(self, other: 'UpdateAttestation'):
        return self._inner_attestation.is_equal(other._inner_attestation)
    
    def as_attestation(self):
        return self._inner_attestation


class UpdateVersion[T](AnyClass):
    """A type of VERSION with reduced fields, used for clients to commit new
    ORIGINAL_VERSIONs to remote host (i.e. without certain audit details)"""

    _inner_original_version: OriginalVersion

    attestations: Optional[list[UpdateAttestation]]

    commit_audit: UpdateAudit

    def __init__(self, 
                commit_audit: UpdateAudit, 
                lifecycle_state: DVCodedText,
                terminology_service: TerminologyService,
                data: Optional[T] = None,
                preceding_version_uid: Optional[ObjectVersionID] = None,
                attestations: Optional[list[UpdateAttestation]] = None,
                signature: Optional[str] = None, **kwargs):
        dummy_contribution = ObjectRef("null", "CONTRIBUTION", GenericID("None", "python"))

        self.commit_audit = commit_audit
        dummy_audit = commit_audit.as_audit_details()

        self.attestations = attestations
        dummy_attestations = None
        if self.attestations is not None:
            dummy_attestations = [attestation.as_attestation() for attestation in attestations]
        
        self._inner_original_version = OriginalVersion(
            contribution=dummy_contribution,
            commit_audit=dummy_audit,
            uid=ObjectVersionID("00000000-0000-0000-0000-000000000000::null.null.null::1"),
            lifecycle_state=lifecycle_state,
            terminology_service=terminology_service,
            data=data,
            preceding_version_uid=preceding_version_uid,
            other_input_version_uids=None,
            attestations=dummy_attestations,
            signature=signature
        )

    def as_json(self):
        draft = self._inner_original_version.as_json()
        del draft["contribution"]
        del draft["uid"]

        del draft["commit_audit"]
        draft["commit_audit"] = self.commit_audit.as_json()

        if "attestations" in draft:
            del draft["attestations"]
            draft["attestations"] = [attestation.as_json() for attestation in self.attestations]

        draft["_type"] = "UPDATE_VERSION"
        return draft

    def is_equal(self, other: 'UpdateVersion'):
        return self._inner_original_version.is_equal(other._inner_original_version)

class UpdateContribution(AnyClass):
    """Special type of CONTRIBUTION containing content rather than references, used
    to submit a whole set of versions to a server"""

    versions: list[UpdateVersion]
    """List of versions to update/create as part of the commit"""

    audit: UpdateAudit
    """Audit details associated with this contribution"""

    uid: Optional[HierObjectID]
    """Unique identifier for this contribution"""

    def __init__(self, versions: list[UpdateVersion], audit: UpdateAudit, uid: Optional[HierObjectID] = None, **kwargs):
        self.versions = versions
        self.audit = audit
        self.uid = uid
        super().__init__(**kwargs)

    def as_json(self):
        draft = {
            "versions": [version.as_json() for version in self.versions],
            "audit": self.audit.as_json()
        }
        if self.uid is not None:
                draft["uid"] = self.uid.as_json()
        draft["_type"] = "UPDATE_CONTRIBUTION"
        return draft
    
    def is_equal(self, other: 'UpdateContribution'):
        return (
            type(self) == type(other) and
            is_equal_value(self.versions, other.versions) and
            is_equal_value(self.audit, other.audit) and
            is_equal_value(self.uid, other.uid)
        )