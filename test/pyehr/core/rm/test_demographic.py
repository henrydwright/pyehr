import pytest

from pyehr.core.base.base_types.identification import GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.quantity.date_time import DVDate
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.demographic import Address, Contact, PartyIdentity, PartyRelationship

def test_party_identity_purpose_valid():
    pur = DVCodedText(
            value="Official",
            defining_code=CodePhrase(
                terminology_id=TerminologyID("FHIR-R4-name-use"),
                code_string="official"
            )
        )
    pi = PartyIdentity(
        purpose=pur,
        archetype_node_id="at0002",
        details=ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0003",
            items=[]
        )
    )
    assert pi.purpose().is_equal(pur)

def test_party_identity_item_at_path():
    pur = DVCodedText(
        value="Official",
        defining_code=CodePhrase(
            terminology_id=TerminologyID("FHIR-R4-name-use"),
            code_string="official"
        )
    )
    det = ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0003",
            items=[]
        )
    pi = PartyIdentity(
        purpose=pur,
        archetype_node_id="at0002",
        details=det
    )
    assert is_equal_value(pi.item_at_path("details"), det)
    assert is_equal_value(pi.item_at_path(""), pi)

def test_address_type_valid():
    addr = Address(
        addr_type=DVCodedText("Home", CodePhrase("FHIR-R4-address-use", "home")),
        archetype_node_id="at0011",
        details=ItemSingle(
            name=DVText("item"),
            archetype_node_id="at0012",
            item=Element(
                name=DVText("postal address"),
                archetype_node_id="at0013",
                value=DVText("12 Example Way, Anytown, AT1 4BA")
            )
        )
    )
    assert addr.address_type().is_equal(DVCodedText("Home", CodePhrase("FHIR-R4-address-use", "home")))

def test_address_item_at_path():
    det = ItemSingle(
            name=DVText("item"),
            archetype_node_id="at0012",
            item=Element(
                name=DVText("postal address"),
                archetype_node_id="at0013",
                value=DVText("12 Example Way, Anytown, AT1 4BA")
            )
        )
    addr = Address(
        addr_type=DVCodedText("Home", CodePhrase("FHIR-R4-address-use", "home")),
        archetype_node_id="at0011",
        details=det
    )
    assert is_equal_value(addr.item_at_path(""), addr)
    assert is_equal_value(addr.item_at_path("details"), det)

def test_contact_purpose_valid():
    cont = Contact(
        purpose=DVText("address"),
        archetype_node_id="at0001",
        addresses=[
            Address(
                addr_type=DVCodedText("Home", CodePhrase("FHIR-R4-address-use", "home")),
                archetype_node_id="at0011",
                details=ItemSingle(
                    name=DVText("item"),
                    archetype_node_id="at0012",
                    item=Element(
                        name=DVText("postal address"),
                        archetype_node_id="at0013",
                        value=DVText("12 Example Way, Anytown, AT1 4BA")
                    )
                )
            )
        ]
    )
    assert cont.purpose().is_equal(DVText("address"))

def test_contact_item_at_path():
    det = ItemSingle(
                    name=DVText("item"),
                    archetype_node_id="at0012",
                    item=Element(
                        name=DVText("postal address"),
                        archetype_node_id="at0013",
                        value=DVText("12 Example Way, Anytown, AT1 4BA")
                    )
                )
    addr = Address(
                addr_type=DVCodedText("Home", CodePhrase("FHIR-R4-address-use", "home")),
                archetype_node_id="at0011",
                details=det
            )
    cont = Contact(
        purpose=DVText("address"),
        archetype_node_id="at0001",
        addresses=[
            addr
        ]
    )
    assert is_equal_value(cont.item_at_path(""), cont)
    assert is_equal_value(cont.item_at_path("addresses[at0011]"), addr)
    assert is_equal_value(cont.item_at_path("addresses[0]/details"), det)

def test_party_relationship_type_validity():
    pr = PartyRelationship(
        rel_type=DVText("NHS employee of"),
        archetype_node_id="at0001",
        source=PartyRef("nhs_pds", "PERSON", GenericID("9449306583", "nhs_number")),
        target=PartyRef("nhs_ods", "ORGANISATION", GenericID("X24", "ods_code")),
        details=ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0010",
            items=[
                Element(
                    name=DVText("employment start date"),
                    archetype_node_id="at0012",
                    value=DVDate("2020-11-13")
                )
            ]
        )
    )
    assert pr.relationship_type().is_equal(DVText("NHS employee of"))

def test_party_relationship_item_at_path():
    det = ItemTree(
            name=DVText("tree"),
            archetype_node_id="at0010",
            items=[
                Element(
                    name=DVText("employment start date"),
                    archetype_node_id="at0012",
                    value=DVDate("2020-11-13")
                )
            ]
        )
    pr = PartyRelationship(
        rel_type=DVText("NHS employee of"),
        archetype_node_id="at0001",
        source=PartyRef("nhs_pds", "PERSON", GenericID("9449306583", "nhs_number")),
        target=PartyRef("nhs_ods", "ORGANISATION", GenericID("X24", "ods_code")),
        details=det
    )
    assert is_equal_value(pr.item_at_path(""), pr)
    assert is_equal_value(pr.item_at_path("details"), det)