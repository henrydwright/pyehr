import pytest

from common import PythonTerminologyService, TERMINOLOGY_OPENEHR
from org.openehr.base.base_types.identification import PartyRef, ObjectID, TerminologyID
from org.openehr.rm.common.generic import PartyIdentified, PartyRelated, Participation
from org.openehr.rm.data_types.basic import DVIdentifier
from org.openehr.rm.data_types.text import DVCodedText, CodePhrase, DVText
from org.openehr.rm.support.terminology import OpenEHRTerminologyGroupIdentifiers

ts_ok = PythonTerminologyService(code_sets=[], terminologies=[TERMINOLOGY_OPENEHR])
ts_empty = PythonTerminologyService(code_sets=[], terminologies=[])

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

def test_party_related_relationship_valid():
    PartyRelated(
        relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "10", "mother")),
        terminology_service=ts_ok,
        name="Ms. A Example"
        )
    # not OK (term svc without openehr)
    with pytest.raises(ValueError):
        PartyRelated(
            relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "10", "mother")),
            terminology_service=ts_empty,
            name="Ms. A Example"
            )
    # not OK (code not in terminology group)
    with pytest.raises(ValueError):
        PartyRelated(
            relationship=DVCodedText("mum", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "1000", "mum")),
            terminology_service=ts_ok,
            name="Ms. A Example"
            )

def test_participation_function_valid():
    # OK (text, not coded)
    Participation(DVText("observer"), PartyIdentified(name="Ms. A Student"))
    # OK (coded text, uses right coding, provides TS)
    Participation(
        function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
        performer=PartyIdentified(name="MRS J TEST"),
        terminology_service=ts_ok)
    # not OK (coded text, uses wrong coding)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("anesthesia nurse", CodePhrase(TerminologyID("HL7v3"), "ANRS")),
            performer=PartyIdentified(name="MRS J TEST"),
            terminology_service=ts_ok)
    # not OK (terminology service empty)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
            performer=PartyIdentified(name="MRS J TEST"),
            terminology_service=ts_empty)
    # not OK (no term svc)
    with pytest.raises(ValueError):
        Participation(
            function=DVCodedText("unknown", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "253", "unknown")),
            performer=PartyIdentified(name="MRS J TEST"))
        
def test_participation_mode_valid():
    # OK (coded text, uses right coding, provides ts)
    Participation(
        function=DVText("observer"), 
        performer=PartyIdentified(name="Ms. A Student"),
        mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")),
        terminology_service=ts_ok)
    # not OK (uses invalid code)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "524", "initial")),
            terminology_service=ts_ok)
    # not OK (empty ts)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")),
            terminology_service=ts_empty)
    # not OK (no termsvc)
    with pytest.raises(ValueError):
        Participation(
            function=DVText("observer"), 
            performer=PartyIdentified(name="Ms. A Student"),
            mode=DVCodedText("physically present", CodePhrase(TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR), "219", "physically present")))
