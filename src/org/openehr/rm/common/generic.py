"""
The classes presented in this module are abstractions of concepts which are generic 
patterns in the domain of health (and most likely other domains), such as 
'participation' and 'attestation'
"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.resource import is_equal_value
from org.openehr.base.base_types.identification import PartyRef, ObjectVersionID
from org.openehr.rm.data_types.basic import DVIdentifier
from org.openehr.rm.data_types.encapsulated import DVMultimedia
from org.openehr.rm.data_types.quantity import DVInterval
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_types.text import DVCodedText, DVText
from org.openehr.rm.data_types.uri import DVEHRUri
from org.openehr.rm.support.terminology import TerminologyService, util_verify_code_in_openehr_terminology_group_or_error, OpenEHRTerminologyGroupIdentifiers

class PartyProxy(AnyClass):
    """Abstract concept of a proxy description of a party, including an optional link 
    to data for this party in a demographic or other identity management system. Sub-typed 
    into PARTY_IDENTIFIED and PARTY_SELF."""

    external_ref: Optional[PartyRef]
    """Optional reference to more detailed demographic or identification information for 
    this party, in an external system."""

    @abstractmethod
    def __init__(self, external_ref: Optional[PartyRef] = None, **kwargs):
        self.external_ref = external_ref
        super().__init__(**kwargs)

    @abstractmethod
    def is_equal(self, other: 'PartyProxy'):
        return (type(self) == type(other) and
                self.external_ref.is_equal(other.external_ref))

class PartySelf(PartyProxy):
    """Party proxy representing the subject of the record. Used to indicate that the 
    party is the owner of the record. May or may not have external_ref set."""

    def __init__(self, external_ref: Optional[PartyRef] = None, **kwargs):
        super().__init__(external_ref, **kwargs)

    def is_equal(self, other):
        return super().is_equal(other)

class PartyIdentified(PartyProxy):
    """Proxy data for an identified party other than the subject of the record, minimally 
    consisting of human-readable identifier(s), such as name, formal (and possibly computable) 
    identifiers such as NHS number, and an optional link to external data. There must be at 
    least one of name, identifier or external_ref present.

    Used to describe parties where only identifiers may be known, and there is no entry at all 
    in the demographic system (or even no demographic system). Typically for health care providers,
    e.g. name and provider number of an institution.

    Should not be used to include patient identifying information."""

    name: Optional[str]
    """Optional human-readable name (in String form)."""

    identifiers: Optional[list[DVIdentifier]]
    """One or more formal identifiers (possibly computable)."""

    def __init__(self, external_ref : Optional[PartyRef] = None, name : Optional[str] = None, identifiers : Optional[list[DVIdentifier]] = None, **kwargs):
        if (external_ref is None and name is None and identifiers is None):
            raise ValueError("Either an external_ref, a name or at least one identifier must be provided (invariant: basic_validity)")
        
        if (name is not None and name == ""):
            raise ValueError("If name is provided, it must not be empty (invariant: name_valid)")
        self.name = name

        if (identifiers is not None and len(identifiers) == 0):
            raise ValueError("If a list of identifiers is provided, it must not be emplty (invariant: identifiers_valid)")
        
        self.identifiers = identifiers
        super().__init__(external_ref, **kwargs)

    def is_equal(self, other: 'PartyIdentified'):
        return (
            super().is_equal(other) and
            self.name == other.name and
            is_equal_value(self.identifiers, other.identifiers)
        )

class PartyRelated(PartyIdentified):
    """Proxy type for identifying a party and its relationship to the subject of the record. 
    Use where the relationship between the party and the subject of the record must be known."""

    _terminology_service: TerminologyService

    relationship: DVCodedText
    """Relationship of subject of this ENTRY to the subject of the record. May be coded. 
    If it is the patient, coded as self."""

    def __init__(self,
                 relationship: DVCodedText,
                 terminology_service: TerminologyService, 
                 external_ref : Optional[PartyRef] = None, 
                 name : Optional[str] = None, 
                 identifiers : Optional[list[DVIdentifier]] = None, **kwargs):
        self._terminology_service = terminology_service

        util_verify_code_in_openehr_terminology_group_or_error(
            code=relationship.defining_code,
            terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_SUBJECT_RELATIONSHIP,
            terminology_service=terminology_service,
            invariant_name_for_error="relationship_valid"
        )
        self.relationship = relationship
        super().__init__(external_ref, name, identifiers, **kwargs)

class Participation(AnyClass):
    """Model of a participation of a Party (any Actor or Role) in an activity. Used to represent 
    any participation of a Party in some activity, which is not explicitly in the model, e.g. 
    assisting nurse. Can be used to record past or future participations.

    Should not be used in place of more permanent relationships between demographic entities."""

    function: DVText
    """The function of the Party in this participation (note that a given party might participate 
    in more than one way in a particular activity). This attribute should be coded, but cannot be 
    limited to the HL7v3:ParticipationFunction vocabulary, since it is too limited and 
    hospital-oriented."""

    mode: Optional[DVCodedText]
    """Optional field for recording the 'mode' of the performer / activity interaction, e.g. 
    present, by telephone, by email etc."""

    performer: PartyProxy
    """The id and possibly demographic system link of the party participating in the activity."""

    time: Optional[DVInterval[DVDateTime]]
    """The time interval during which the participation took place, if it is used in an 
    observational context (i.e. recording facts about the past); or the intended time interval 
    of the participation when used in future contexts, such as EHR Instructions."""

    def __init__(self, function: DVText, performer: PartyProxy, mode: Optional[DVCodedText] = None, time: DVInterval[DVDateTime] = None, terminology_service: Optional[TerminologyService] = None, **kwargs):
        if (isinstance(function, DVCodedText)):
            if terminology_service is None:
                raise ValueError("If provided function is DV_CODED_TEXT, then a terminology service must also be provided (invariant: function_valid)")
            util_verify_code_in_openehr_terminology_group_or_error(
                code=function.defining_code, 
                terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PARTICIPATION_FUNCTION, 
                terminology_service=terminology_service,
                invariant_name_for_error="function_valid")
        
        self.function = function
        self.performer = performer

        if (mode is not None):
            if terminology_service is None:
                raise ValueError("If mode is provided, then a terminology service must also be provided (invariant: mode_valid)")
            util_verify_code_in_openehr_terminology_group_or_error(
                code=mode.defining_code,
                terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PARTICIPATION_MODE,
                terminology_service=terminology_service,
                invariant_name_for_error="mode_valid"
            )
        self.mode = mode
        self.time = time 
        super().__init__(**kwargs)

    def is_equal(self, other: 'Participation'):
        return (type(self) == type(other) and
                is_equal_value(self.function, other.function) and
                is_equal_value(self.mode, other.mode) and
                is_equal_value(self.performer, other.performer) and
                is_equal_value(self.time, other.time))
    
class AuditDetails(AnyClass):
    """The set of attributes required to document the committal of an information item to a 
    repository."""

    system_id: str
    """Identifier of the logical EHR system where the change was committed. This is almost 
    always owned by the organisation legally responsible for the EHR, and is distinct from 
    any application, or any hosting infrastructure."""

    time_committed: DVDateTime
    """Time of committal of the item."""

    change_type: DVCodedText
    """Type of change. Coded using the openEHR Terminology audit change type group."""

    description: Optional[DVText]
    """Reason for committal. This may be used to qualify the value in the change_type 
    field. For example, if the change affects only the EHR directory, this field might 
    be used to indicate 'Folder "episode 2018-02-16" added' or similar."""

    committer: PartyProxy
    """Identity and optional reference into identity management service, of user who 
    committed the item."""

    def __init__(self, 
                 system_id: str, 
                 time_committed: DVDateTime, 
                 change_type: DVCodedText, 
                 committer: PartyProxy, 
                 terminology_service: TerminologyService,
                 description: Optional[DVText] = None, 
                 **kwargs):
        if len(system_id) == 0:
            raise ValueError("system_id cannot be empty (invariant: system_id_valid)")
        self.system_id = system_id
        self.time_committed = time_committed
        util_verify_code_in_openehr_terminology_group_or_error(
            code=change_type.defining_code,
            terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_AUDIT_CHANGE_TYPE,
            terminology_service=terminology_service,
            invariant_name_for_error="change_type_valid"
        )
        self.change_type = change_type
        self.committer = committer
        self.description = description
        super().__init__(**kwargs)

    def is_equal(self, other: 'AuditDetails'):
        return (
            type(self) == type(other) and
            self.system_id == other.system_id and
            is_equal_value(self.time_committed, other.time_committed) and
            is_equal_value(self.change_type, other.change_type) and
            is_equal_value(self.description, other.description) and
            is_equal_value(self.committer, other.committer)
        )
    
class Attestation(AuditDetails):
    """Record an attestation of a party (the committer) to item(s) of record content. An attestation 
    is an explicit signing by one healthcare agent of particular content for various particular purposes, 
    including:
      * for authorisation of a controlled substance or procedure (e.g. sectioning of patient under mental health act);
      * witnessing of content by senior clinical professional;
      * indicating acknowledgement of content by intended recipient, e.g. GP who ordered a test result."""
    
    attested_view: Optional[DVMultimedia]
    """Optional visual representation of content attested e.g. screen image."""

    proof: Optional[str]
    """Proof of attestation."""

    items: Optional[list[DVEHRUri]]
    """Items attested, expressed as fully qualified runtime paths to the items in question. Although not 
    recommended, these may include fine-grained items which have been attested in some other system. Otherwise 
    it is assumed to be for the entire VERSION with which it is associated."""

    reason: DVText
    """Reason of this attestation. Optionally coded by the openEHR Terminology group attestation reason; 
    includes values like authorisation, witness etc."""

    is_pending: bool
    """True if this attestation is outstanding; False means it has been completed."""

    def __init__(self, 
                 system_id: str, 
                 time_committed: DVDateTime, 
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
        if (isinstance(reason, DVCodedText)):
            util_verify_code_in_openehr_terminology_group_or_error(
                code=reason.defining_code,
                terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_ATTESTATION_REASON,
                terminology_service=terminology_service,
                invariant_name_for_error="reason_valid"
            )
        self.reason = reason
        self.is_pending = is_pending
        self.attested_view = attested_view
        self.proof = proof
        if (items is not None and len(items) == 0):
            raise ValueError("If items is provided it must not be an empty list (invariant: items_valid)")
        self.items = items
        super().__init__(system_id, time_committed, change_type, committer, terminology_service, description, **kwargs)

class RevisionHistoryItem(AnyClass):
    """An entry in a revision history, corresponding to a version from a versioned container. Consists of 
    AUDIT_DETAILS instances with revision identifier of the revision to which the AUDIT_DETAILS instance belongs."""

    version_id: ObjectVersionID
    """Version identifier for this revision."""

    audits: list[AuditDetails]
    """The audits for this revision; there will always be at least one commit audit (which may itself be an ATTESTATION),
    there may also be further attestations."""

    def __init__(self, version_id: ObjectVersionID, audits: list[AuditDetails], **kwargs):
        self.version_id = version_id
        self.audits = audits
        super().__init__(**kwargs)

    def is_equal(self, other: 'RevisionHistoryItem'):
        return (type(self) == type(other) and
                is_equal_value(self.version_id, other.version_id) and
                is_equal_value(self.audits, other.audits))

class RevisionHistory(AnyClass):
    """Defines the notion of a revision history of audit items, each associated with the version for which that 
    audit was committed. The list is in most-recent-first order."""

    # TODO: the specification has a class description and parameter description that are exact opposites (most-recent-first vs. most-recent-last)
    #        need to report this, but in meantime take parameter definition of most-recent-last...
    items: list[RevisionHistoryItem]
    """The items in this history in most-recent-last order."""

    def __init__(self, items: list[RevisionHistoryItem], **kwargs):
        self.items = items
        super().__init__(**kwargs)

    def most_recent_version(self) -> str:
        """The version id of the most recent item, as a String."""
        return self.items[-1].version_id.value

    def most_recent_version_time_committed(self) -> str:
        """The commit date/time of the most recent item, as a String."""
        return self.items[-1].audits[-1].time_committed.as_string()

    def is_equal(self, other: 'RevisionHistory'):
        return (
            type(self) == type(other) and
            is_equal_value(self.items, other.items))