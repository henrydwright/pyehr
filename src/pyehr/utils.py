from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, ObjectVersionID
from pyehr.core.its.rest.additions import UpdateAttestation, UpdateAudit, UpdateContribution, UpdateVersion
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, VersionedObject
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.demographic import Organisation, Party, Person
from pyehr.core.rm.ehr import EHR, EHRStatus
from pyehr.core.base.base_types.identification import HierObjectID, InternetID, ObjectRef, ObjectVersionID, GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, ImportedVersion, OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import Attestation, AuditDetails, PartyIdentified, PartySelf, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVIdentifier
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText, DVUri
from pyehr.core.rm.demographic import Address, Contact, Organisation, PartyIdentity, Person, VersionedParty
from pyehr.core.rm.ehr import EHR, EHRStatus, VersionedEHRStatus


PYTHON_TYPE_TO_STRING_TYPE_MAP : dict[type, str] = {
    Party: "PARTY",
    Person: "PERSON",
    VersionedObject: "VERSIONED_OBJECT",
    OriginalVersion: "VERSION",
    Contribution: "CONTRIBUTION",
    DVText: "DV_TEXT",
    EHRStatus: "EHR_STATUS",
    EHR: "EHR",
    Organisation: "ORGANISATION"
}
"""Mapping of pyehr type (Python type) to the openEHR type string (e.g. pyehr type
of Party maps to 'PARTY')"""

OPENEHR_TYPE_MAP = {
    "OBJECT_VERSION_ID": ObjectVersionID,
    "OBJECT_REF": ObjectRef,
    "HIER_OBJECT_ID" : HierObjectID,
    "DV_TEXT": DVText,
    "DV_URI": DVUri,
    "DV_DATE_TIME": DVDateTime,
    "PARTY_SELF": PartySelf,
    "EHR": EHR,
    "EHR_STATUS": EHRStatus,
    "ARCHETYPED": Archetyped,
    "ARCHETYPE_ID": ArchetypeID,
    "PARTY_REF": PartyRef,
    "GENERIC_ID": GenericID,
    "PERSON": Person,
    "PARTY_IDENTITY": PartyIdentity,
    "ITEM_TREE": ItemTree,
    "ELEMENT": Element,
    "DV_IDENTIFIER": DVIdentifier,
    "CLUSTER": Cluster,
    "DV_CODED_TEXT": DVCodedText,
    "CODE_PHRASE": CodePhrase,
    "TERMINOLOGY_ID": TerminologyID,
    "VERSIONED_EHR_STATUS": VersionedEHRStatus,
    "REVISION_HISTORY": RevisionHistory,
    "REVISION_HISTORY_ITEM": RevisionHistoryItem,
    "AUDIT_DETAILS": AuditDetails,
    "PARTY_IDENTIFIED": PartyIdentified,
    "ORIGINAL_VERSION": OriginalVersion,
    "IMPORTED_VERSION": ImportedVersion,
    "CONTRIBUTION": Contribution,
    "ITEM_SINGLE": ItemSingle,
    "VERSIONED_PARTY": VersionedParty,
    "VERSIONED_OBJECT": VersionedObject,
    "INTERNET_ID": InternetID,
    "ATTESTATION": Attestation,
    "UPDATE_CONTRIBUTION": UpdateContribution,
    "UPDATE_VERSION": UpdateVersion,
    "UPDATE_AUDIT": UpdateAudit,
    "UPDATE_ATTESTATION": UpdateAttestation,
    "ORGANISATION": Organisation,
    "CONTACT": Contact,
    "ADDRESS": Address,
    "DV_DATE": DVDate,
    "TEMPLATE": OperationalTemplate
}
"""Map of OpenEHR string type names (e.g. as found in '_type' JSON) to pyehr Python types"""

def get_openehr_type_str(obj: AnyClass) -> str:
    type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

    if type_str == "VERSION":
        type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

    return type_str