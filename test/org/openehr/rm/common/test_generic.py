import pytest

from org.openehr.base.base_types.identification import PartyRef, ObjectID
from org.openehr.rm.common.generic import PartyIdentified
from org.openehr.rm.data_types.basic import DVIdentifier

def test_party_identified_basic_validity():
    # OK (one of three not void)
    pi = PartyIdentified(external_ref=PartyRef("gmc_number", "PERSON", ObjectID("9999999")))
    pi = PartyIdentified(name="Dr. Test Example")
    pi = PartyIdentified(identifiers=[DVIdentifier("9999999", issuer="General Medical Council")])

    # not OK (all void)
    with pytest.raises(ValueError):
        pi = PartyIdentified()

def test_party_identified_name_valid():
    # OK (name not empty)
    pi = PartyIdentified(name="Dr. Test Example")

    # not OK (name empty)
    with pytest.raises(ValueError):
        pi = PartyIdentified(name="")

def test_party_identified_identifiers_valid():
    # OK (list of identifiers not empty)
    pi = PartyIdentified(identifiers=[DVIdentifier("9999999", issuer="General Medical Council")])

    # not OK (identifiers empty)
    with pytest.raises(ValueError):
        pi = PartyIdentified(identifiers=[])
