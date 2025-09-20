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
