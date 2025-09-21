"""
The classes presented in this module are abstractions of concepts which are generic 
patterns in the domain of health (and most likely other domains), such as 
'participation' and 'attestation'
"""

from abc import abstractmethod
from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.resource import is_equal_value
from org.openehr.base.base_types.identification import PartyRef
from org.openehr.rm.data_types.basic import DVIdentifier
from org.openehr.rm.data_types.quantity import DVInterval
from org.openehr.rm.data_types.quantity.date_time import DVDateTime
from org.openehr.rm.data_types.text import DVCodedText, DVText
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