import pytest

from pyehr.core.base.base_types.identification import ArchetypeID, GenericID, HierObjectID, LocatableRef, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDate
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.demographic import Address, Capability, Contact, Party, PartyIdentity, PartyRelationship, Person, Role

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

def _generate_test_person():
    return Person(
        actor_type=DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")),
        archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0",
        archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0"), "1.1.0"),
        uid=HierObjectID("8e94a778-989e-4682-8c36-76f8c18dda20"),
        identities=[
            PartyIdentity(
                purpose=DVText("Identity"),
                archetype_node_id="at0001",
                details=ItemTree(
                    name=DVText("tree"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("Name"),
                            archetype_node_id="at0011",
                            value=DVText("Dr Example General-Practitioner")
                        ),
                        Element(
                            name=DVText("GMC number"),
                            archetype_node_id="at0012",
                            value=DVIdentifier("9999999")
                        )
                    ]
                )
            )
        ],
        relationships=[
            PartyRelationship(
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
        ],
        reverse_relationships=[
            LocatableRef("local", "PARTY_RELATIONSHIP", HierObjectID("a8fa099f-5c0b-4d50-90e4-825af230f795"), path="relationships[at0001]")
        ]
    )

def test_party_type_valid():
    p = _generate_test_person()
    assert is_equal_value(p.type_party(), DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")))

def test_party_contacts_valid():
    # OK - list with content
    p = Person(
        actor_type=DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")),
        archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0",
        archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0"), "1.1.0"),
        uid=HierObjectID("8e94a778-989e-4682-8c36-76f8c18dda20"),
        identities=[
            PartyIdentity(
                purpose=DVText("Identity"),
                archetype_node_id="at0001",
                details=ItemTree(
                    name=DVText("tree"),
                    archetype_node_id="at0002",
                    items=[
                        Element(
                            name=DVText("Name"),
                            archetype_node_id="at0011",
                            value=DVText("Dr Example General-Practitioner")
                        ),
                        Element(
                            name=DVText("GMC number"),
                            archetype_node_id="at0012",
                            value=DVIdentifier("9999999")
                        )
                    ]
                )
            )
        ],
        contacts=[
            Contact(
                purpose=DVText("address"),
                archetype_node_id="at0001",
                addresses=[
                    Address(
                        addr_type=DVCodedText("Work", CodePhrase("FHIR-R4-address-use", "work")),
                        archetype_node_id="at0011",
                        details=ItemSingle(
                            name=DVText("item"),
                            archetype_node_id="at0012",
                            item=Element(
                                name=DVText("postal address"),
                                archetype_node_id="at0013",
                                value=DVText("Anytown Family Practice, 4 Example Street, Anytown, AT1 2GP")
                            )
                        )
                    )
                ]
            )
        ]
    )
    # not OK - empty list
    with pytest.raises(ValueError):
        p = Person(
            actor_type=DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")),
            archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0"), "1.1.0"),
            uid=HierObjectID("8e94a778-989e-4682-8c36-76f8c18dda20"),
            identities=[
                PartyIdentity(
                    purpose=DVText("Identity"),
                    archetype_node_id="at0001",
                    details=ItemTree(
                        name=DVText("tree"),
                        archetype_node_id="at0002",
                        items=[
                            Element(
                                name=DVText("Name"),
                                archetype_node_id="at0011",
                                value=DVText("Dr Example General-Practitioner")
                            ),
                            Element(
                                name=DVText("GMC number"),
                                archetype_node_id="at0012",
                                value=DVIdentifier("9999999")
                            )
                        ]
                    )
                )
            ],
            contacts=[]
        )

def test_party_relationships_validity():
    # OK - test person
    _generate_test_person()
    # not OK - empty list
    with pytest.raises(ValueError):
        Person(
            actor_type=DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")),
            archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0"), "1.1.0"),
            uid=HierObjectID("8e94a778-989e-4682-8c36-76f8c18dda20"),
            identities=[
                PartyIdentity(
                    purpose=DVText("Identity"),
                    archetype_node_id="at0001",
                    details=ItemTree(
                        name=DVText("tree"),
                        archetype_node_id="at0002",
                        items=[
                            Element(
                                name=DVText("Name"),
                                archetype_node_id="at0011",
                                value=DVText("Dr Example General-Practitioner")
                            ),
                            Element(
                                name=DVText("GMC number"),
                                archetype_node_id="at0012",
                                value=DVIdentifier("9999999")
                            )
                        ]
                    )
                )
            ],
            relationships=[]
        )

def test_party_reverse_relationships_validity():
    # OK - test person
    _generate_test_person()
    # not OK - empty list
    with pytest.raises(ValueError):
        Person(
            actor_type=DVCodedText("General practitioner", CodePhrase("SNOMED-CT", "62247001", "Family medicine specialist (occupation)")),
            archetype_node_id="openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0",
            archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-PERSON.nhs_clinician.v0"), "1.1.0"),
            uid=HierObjectID("8e94a778-989e-4682-8c36-76f8c18dda20"),
            identities=[
                PartyIdentity(
                    purpose=DVText("Identity"),
                    archetype_node_id="at0001",
                    details=ItemTree(
                        name=DVText("tree"),
                        archetype_node_id="at0002",
                        items=[
                            Element(
                                name=DVText("Name"),
                                archetype_node_id="at0011",
                                value=DVText("Dr Example General-Practitioner")
                            ),
                            Element(
                                name=DVText("GMC number"),
                                archetype_node_id="at0012",
                                value=DVIdentifier("9999999")
                            )
                        ]
                    )
                )
            ],
            reverse_relationships=[]
        )

def test_party_is_archetype_root():
    p = _generate_test_person()
    assert p.is_archetype_root() == True

def test_party_uid_mandatory():
    p = _generate_test_person()
    assert p.uid != None

def test_role_capabilities_valid():
    # OK - list filled
    Role(
        role_type=DVText("HC consumer"),
        archetype_node_id="openEHR-DEMOGRAPHIC-ROLE.person_role.v0",
        archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-ROLE.person_role.v0"), "1.1.0"),
        uid=HierObjectID("00da28fe-b7fa-4186-bb01-6f4c591e5bfc"),
        performer=PartyRef("local", "PERSON", HierObjectID("3196a11a-bc7f-4dd1-b52a-16394391a634")),
        identities=[
            PartyIdentity(
                purpose=DVText("internal consumer"),
                archetype_node_id="at0001",
                details=ItemSingle(
                    name=DVText("item"),
                    archetype_node_id="at0002",
                    item=Element(
                        name=DVText("internal consumer identifier"),
                        archetype_node_id="at0003",
                        value=DVIdentifier("999-999-999-999", "Local Healthcare System", "Local Hospital")
                    )
                )

            )
        ],
        capabilities=[
            Capability(
                name=DVText("pay for care using medicare"),
                archetype_node_id="at1001",
                credentials=ItemSingle(
                    name=DVText("item"),
                    archetype_node_id="at1002",
                    item=Element(
                        name=DVText("medicare identifier"),
                        archetype_node_id="at1004",
                        value=DVIdentifier("999", "Medicare")
                    )
                )
            )
        ]
    )
    # not OK - list empty
    with pytest.raises(ValueError):
            Role(
                role_type=DVText("HC consumer"),
                archetype_node_id="openEHR-DEMOGRAPHIC-ROLE.person_role.v0",
                archetype_details=Archetyped(ArchetypeID("openEHR-DEMOGRAPHIC-ROLE.person_role.v0"), "1.1.0"),
                uid=HierObjectID("00da28fe-b7fa-4186-bb01-6f4c591e5bfc"),
                performer=PartyRef("local", "PERSON", HierObjectID("3196a11a-bc7f-4dd1-b52a-16394391a634")),
                identities=[
                    PartyIdentity(
                        purpose=DVText("internal consumer"),
                        archetype_node_id="at0001",
                        details=ItemSingle(
                            name=DVText("item"),
                            archetype_node_id="at0002",
                            item=Element(
                                name=DVText("internal consumer identifier"),
                                archetype_node_id="at0003",
                                value=DVIdentifier("999-999-999-999", "Local Healthcare System", "Local Hospital")
                            )
                        )

                    )
                ],
                capabilities=[]
            )