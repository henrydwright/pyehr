
from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, PartyRef
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartyIdentified, PartySelf
from pyehr.core.rm.composition import Composition
from pyehr.core.rm.composition.content.entry import Action, Evaluation, ISMTransition
from pyehr.core.rm.data_structures.item_structure import ItemTree
from pyehr.core.rm.data_structures.representation import Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.demographic import PartyIdentity, Person
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus
from pyehr.server.database import IDatabaseEngine
from pyehr.server.database.mongodb import MongoDBDatabaseEngine

from pyehr.server.change_control import VersionLifecycleState, VersionedStore
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyItem


def create_test_data(db: IDatabaseEngine):
    vs = VersionedStore(db, "local.aql")

    creator = PartyIdentified(name="SMITH, Joe")

    system_id = HierObjectID("8addce0e-2289-420e-adf8-3400907c0d3e")

    person_ids = [
        HierObjectID("0c4823c7-15f0-4310-991d-ab4a7a35d11e"),
        HierObjectID("01302448-0377-4dcd-be5f-9f16bad3812b"),
        HierObjectID("f6f094c5-b21b-4dd6-8b53-d99437fa25e6"),
        HierObjectID("b9036171-440f-4287-8219-1581d82ffb70"),
        HierObjectID("901d459c-615e-4078-bddc-61eee3f3a3cd")
    ]

    ehr_ids = [
        HierObjectID("8d7f36c1-c2d0-4332-895c-4a3cab3446b6"),
        HierObjectID("209ff927-3777-4360-b09c-f8e50ae5b1e7"),
        HierObjectID("a2906af1-cc9f-4ef2-879b-9a3c22737b23"),
        HierObjectID("726f23bb-5b8d-4b24-bb7e-545fc698b068"),
        HierObjectID("def83fa8-3c37-4fd4-89ec-143de9401563")
    ]
    ehr_subjects = [
        PartyIdentified(external_ref=PartyRef("local", "PERSON", person_ids[0]), name="AINDOW, Comfort Zula"),
        PartyIdentified(external_ref=PartyRef("local", "PERSON", person_ids[1]), name="CHISLETT, Octavia"),
        PartyIdentified(external_ref=PartyRef("local", "PERSON", person_ids[2]), name="SHIPPERBOTTOM, Beryl"),
        PartyIdentified(external_ref=PartyRef("local", "PERSON", person_ids[3]), name="ANDERTON, Briar Chadwick"),
        PartyIdentified(external_ref=PartyRef("local", "PERSON", person_ids[4]), name="GILMAN, Percy")
    ]
    acs_ids = [db.generate_hier_object_id() for i in range(5)]

    versioned_ehr_status_ids = []
    versioned_ehr_access_ids = []

    default_acs = PyehrAccessControlSettings(
        policies=[PyehrAccessPolicyItem(True)],
        uid=HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000"))

    db.create_uid_object(default_acs)

    for i in range(5):
        owner_ehr_id = ehr_ids[i]
        acs_id = acs_ids[i]

        ea_ovid, ea_contrib, ea_vo = vs.create(
            obj=EHRAccess(
                name=DVText("EHR access"),
                archetype_node_id="openEHR-EHR-EHR_ACCESS.generic.v1",
                archetype_details=Archetyped(
                    archetype_id=ArchetypeID("openEHR-EHR-EHR_ACCESS.generic.v1"),
                    rm_version="1.1.0"
                ),
                settings=PyehrAccessControlSettings(
                    base_upon=ObjectRef("local", "PYEHR_ACCESS_CONTROL_SETTINGS", HierObjectID("e0000000-0000-0000-FF00-FFFFFFFF1000")),
                    uid=acs_id
                )
            ),
            owner_id=ObjectRef("local", "EHR", owner_ehr_id),
            committer=creator,
            lifecycle_state=VersionLifecycleState.COMPLETE
        )
        versioned_ehr_access_ids.append(HierObjectID(ea_ovid.object_id().value))

        ehr_subject = ehr_subjects[i]

        status_obj = EHRStatus(
                        name=DVText("EHR status"),
                        archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
                        subject=ehr_subject,
                        is_queryable=True,
                        is_modifiable=True,
                        archetype_details=Archetyped(
                            archetype_id=ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"),
                            rm_version="1.1.0"
                        )
                    )
        
        es_ovid, es_contrib, es_vo = vs.create(
            obj=status_obj,
            owner_id=ObjectRef("local", "EHR", owner_ehr_id),
            committer=creator,
            lifecycle_state=VersionLifecycleState.COMPLETE
        )
        versioned_ehr_status_ids.append(HierObjectID(es_ovid.object_id().value))

        ehr_obj = EHR(
            system_id=system_id,
            ehr_id=ehr_ids[i],
            ehr_status=ObjectRef("local", "VERSIONED_EHR_STATUS", versioned_ehr_status_ids[i]),
            ehr_access=ObjectRef("local", "VERSIONED_EHR_ACCESS", versioned_ehr_access_ids[i]),
            time_created=DVDateTime(Env.current_date_time())
        )
        db.create_uid_object(ehr_obj)

    arch_id_version = ["0", "0", "0", "1", "1"]
    dobs = ["19430519","20080920","20110509","20090215","20110128"]
    nhs_nos = ["9449304424","9449305552","9449306621","9449306613","9449306605"]
    family_names = ["AINDOW","CHISLETT","SHIPPERBOTTOM","ANDERTON","GILMAN"]
    given_names = ["COMFORT","OCTAVIA","BERYL","BRIAR","PERCY"]

    for i in range(5):
        p = Person(
            actor_type=DVText("patient"),
            archetype_node_id="pyehr-DEMOGRAPHIC-PERSON.nhs_patient.v" + str(arch_id_version[i]),
            archetype_details=Archetyped(ArchetypeID("pyehr-DEMOGRAPHIC-PERSON.nhs_patient.v" + str(arch_id_version[i])), "1.1.0"),
            uid=person_ids[i],
            identities=[PartyIdentity(
                purpose=DVText("nhs"),
                archetype_node_id="at0004",
                details=ItemTree(
                    name=DVText("pds_demographics"),
                    archetype_node_id="at0005",
                    items=[
                        Element(
                            name=DVText("nhs_number"),
                            archetype_node_id="at0006",
                            value=DVIdentifier(nhs_nos[i], "nhs_england", "nhs_england", "nhs_number")
                        ),
                        Element(
                            name=DVText("family_name"),
                            archetype_node_id="at0007",
                            value=DVText(family_names[i])
                        ),
                        Element(
                            name=DVText("given_name"),
                            archetype_node_id="at0008",
                            value=DVText(given_names[i])
                        )
                    ]
                )
            )],
            details=ItemTree(
                name=DVText("details"),
                archetype_node_id="at0002",
                items=[
                    Element(
                        name=DVText("DOB"),
                        archetype_node_id="at0003",
                        value=DVDate(dobs[i])
                    )
                ]
            )
        )
        db.create_uid_object(p)


    def problem_list(problem_content_list: list[Evaluation]):
        return Composition(
            DVText("problem list"),
            "openEHR-EHR-COMPOSITION.problem_list.v2",
            CodePhrase("ISO_639-1", "en-gb"),
            CodePhrase("ISO_3166-1", "GB"),
            DVCodedText("event", CodePhrase("openehr", "433")),
            creator,
            Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.problem_list.v2"), "1.1.0"),
            content=problem_content_list
        )

    def diagnosis(diag: DVCodedText, severity: DVCodedText):
        return Evaluation(
            DVText(f"diagnosis: {diag.value}"),
            "openEHR-EHR-EVALUATION.problem_diagnosis.v1",
            CodePhrase("ISO_639-1", "en-gb"),
            CodePhrase("IANA_character-sets", "UTF-8"),
            PartySelf(),
            Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.problem_diagnosis.v1"), "1.1.0"),
            data=ItemTree(
                DVText("structure"),
                "at0001",
                items=[
                    Element(
                        DVText("Problem/Diagnosis name"),
                        "at0002",
                        diag
                    ),
                    Element(
                        DVText("Severity"),
                        "at0005",
                        severity
                    )
                ]
            )
        )

    problem_lists = [
        problem_list([diagnosis(DVCodedText("Allergic asthma", CodePhrase("SNOMED-CT", "389145006")), DVCodedText("Severe", CodePhrase("local", "at0049")))]),
        None,
        problem_list([
            diagnosis(DVCodedText("Chronic obstructive pulmonary disease", CodePhrase("SNOMED-CT", "13645005")), DVCodedText("Mild", CodePhrase("local", "at0047"))),
            diagnosis(DVCodedText("Arthritis of finger of left hand", CodePhrase("SNOMED-CT", "12236561000119100")),  DVCodedText("Mild", CodePhrase("local", "at0047")))]),
        problem_list([diagnosis(DVCodedText("Cocaine dependence", CodePhrase("SNOMED-CT", "31956009")), DVCodedText("Moderate", CodePhrase("local", "at0048")))]),
        problem_list([diagnosis(DVCodedText("Heart failure", CodePhrase("SNOMED-CT", "84114007")), DVCodedText("Mild", CodePhrase("local", "at0047")))])
    ]

    for i in range(5):
        if problem_lists[i] is not None:
            d_ovid, _, _ = vs.create(
                obj=problem_lists[i],
                owner_id=ObjectRef("local", "EHR", ehr_ids[i]),
                committer=creator,
                lifecycle_state=VersionLifecycleState.COMPLETE
            )
            db.add_to_ehr_lists(ehr_ids[i], ObjectRef("local", "VERSIONED_COMPOSITION", HierObjectID(d_ovid.object_id().value)))

    asthma_meds = Composition(
        DVText("medication list"),
        "openEHR-EHR-COMPOSITION.medication_list.v1",
        CodePhrase("ISO_639-1", "en-gb"),
        CodePhrase("ISO_3166-1", "GB"),
        DVCodedText("event", CodePhrase("openehr", "433")),
        creator,
        Archetyped(ArchetypeID("openEHR-EHR-COMPOSITION.medication_list.v1"), "1.1.0"),
        content=[
            Action(
                DVText("prescription: DuoResp Spiromax 160micrograms/dose / 4.5micrograms/dose dry powder inhaler (Teva UK Ltd)"),
                "openEHR-EHR-ACTION.medication.v1",
                CodePhrase("ISO_639-1", "en-gb"),
                CodePhrase("IANA_character-sets", "UTF-8"),
                PartySelf(),
                Archetyped(ArchetypeID("openEHR-EHR-ACTION.medication.v1"), "1.1.0"),
                Env.current_date_time(),
                ISMTransition(
                    DVCodedText("active", CodePhrase("openehr", "245")),
                    careflow_step=DVCodedText("Prescription issued", CodePhrase("local", "at0002"))
                ),
                ItemTree(
                    DVText("Tree"),
                    "at0017",
                    items=[
                        Element(
                            DVText("Medication item"),
                            "at0020",
                            DVCodedText("DuoResp Spiromax 160micrograms/dose / 4.5micrograms/dose dry powder inhaler (Teva UK Ltd)", CodePhrase("SNOMED-CT", "25254111000001105"))
                        )
                    ]
                )
            )
        ]
    )

    med_ovid, _, _ = vs.create(
        asthma_meds,
        ObjectRef("local", "EHR", ehr_ids[0]),
        creator,
        VersionLifecycleState.COMPLETE
    )
    db.add_to_ehr_lists(ehr_ids[0], ObjectRef("local", "VERSIONED_COMPOSITION", HierObjectID(med_ovid.object_id().value)))