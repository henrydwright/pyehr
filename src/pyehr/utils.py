from pyehr.core.am.aom14.archetype import Archetype
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CString
from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.base.base_types.identification import ISOOID, UUID, ArchetypeID, HierObjectID, LocatableRef, ObjectRef, ObjectVersionID, TemplateID, VersionTreeID
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.terminology import TerminologyCode, TerminologyTerm
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
from pyehr.core.base.resource import ResourceDescription, ResourceDescriptionItem, TranslationDetails
from pyehr.core.its.rest.additions import UpdateAttestation, UpdateAudit, UpdateContribution, UpdateVersion
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.rest.additions import UpdateVersion
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, VersionedObject
from pyehr.core.rm.common.directory import Folder
from pyehr.core.rm.composition import Composition
from pyehr.core.rm.data_types.encapsulated import DVMultimedia, DVParsable
from pyehr.core.rm.data_types.quantity import DVCount, DVInterval, DVOrdinal, DVProportion, DVQuantity, DVScale, ReferenceRange
from pyehr.core.rm.data_types.text import DVParagraph, DVText, TermMapping
from pyehr.core.rm.data_types.time_specification import DVGeneralTimeSpecification, DVPeriodicTimeSpecification
from pyehr.core.rm.data_types.uri import DVEHRUri
from pyehr.core.rm.demographic import Agent, Organisation, Party, Person, Role
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus, VersionedComposition
from pyehr.core.base.base_types.identification import HierObjectID, InternetID, ObjectRef, ObjectVersionID, GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, ImportedVersion, OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import Attestation, AuditDetails, PartyIdentified, PartySelf, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID
from pyehr.core.rm.data_structures.item_structure import ItemSingle, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVBoolean, DVIdentifier, DVState
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime, DVDuration, DVTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText, DVUri
from pyehr.core.rm.demographic import Address, Contact, Organisation, PartyIdentity, Person, VersionedParty
from pyehr.core.rm.ehr import EHR, EHRStatus, VersionedEHRStatus
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyItem


PYTHON_TYPE_TO_STRING_TYPE_MAP : dict[type, str] = {
    Party: "PARTY",
    Person: "PERSON",
    VersionedObject: "VERSIONED_OBJECT",
    OriginalVersion: "VERSION",
    UpdateVersion: "VERSION",
    Contribution: "CONTRIBUTION",
    DVText: "DV_TEXT",
    EHRStatus: "EHR_STATUS",
    EHR: "EHR",
    Organisation: "ORGANISATION",
    Agent: "AGENT",
    EHRAccess: "EHR_ACCESS",
    Composition: "COMPOSITION",
    Folder: "FOLDER",
    Role: "ROLE",
    PyehrAccessControlSettings: "PYEHR_ACCESS_CONTROL_SETTINGS",
    PyehrAccessPolicyItem: "PYEHR_ACCESS_POLICY_ITEM",
    Folder: "FOLDER"
}
"""Mapping of pyehr type (Python type) to the openEHR type string (e.g. pyehr type
of Party maps to 'PARTY')"""

OPENEHR_TYPE_MAP = {
    # FOUNDATION
    "DATE": ISODate,
    "DATE_TIME": ISODateTime,
    "DURATION": ISODuration,
    "INTERVAL": Interval,
    "TERMINOLOGY_CODE": TerminologyCode,
    "TERMINOLOGY_TERM": TerminologyTerm,
    "TIME": ISOTime,
    # BASE
    "INTERNET_ID": InternetID,
    "OBJECT_REF": ObjectRef,
    "PARTY_REF": PartyRef,
    "TEMPLATE_ID": TemplateID,
    "OBJECT_VERSION_ID": ObjectVersionID,
    "VERSION_TREE_ID": VersionTreeID,
    "LOCATABLE_REF": LocatableRef,
    "GENERIC_ID": GenericID,
    "ARCHETYPE_ID": ArchetypeID,
    "HIER_OBJECT_ID" : HierObjectID,
    "UUID": UUID,
    "ISO_OID": ISOOID,
    "TERMINOLOGY_ID": TerminologyID,
    "TRANSLATION_DETAILS": TranslationDetails,
    "RESOURCE_DESCRIPTION_ITEM": ResourceDescriptionItem,
    "RESOURCE_DESCRIPTION": ResourceDescription,
    # RM : datatypes
    "DV_TEXT": DVText,
    "DV_IDENTIFIER": DVIdentifier,
    "DV_DATE": DVDate,
    "DV_CODED_TEXT": DVCodedText,
    "DV_TIME": DVTime,
    "DV_BOOLEAN": DVBoolean,
    "CODE_PHRASE": CodePhrase,
    "DV_PARSABLE": DVParsable,
    "TERM_MAPPING": TermMapping,
    "DV_EHR_URI": DVEHRUri,
    "DV_URI": DVUri,
    "DV_COUNT": DVCount,
    "DV_GENERAL_TIME_SPECIFICATION": DVGeneralTimeSpecification,
    "DV_MULTIMEDIA": DVMultimedia,
    "DV_DATE_TIME": DVDateTime,
    "DV_QUANTITY": DVQuantity,
    "DV_DURATION": DVDuration,
    "DV_INTERVAL": DVInterval,
    "DV_ORDINAL": DVOrdinal,
    "DV_PARAGRAPH": DVParagraph,
    "DV_STATE": DVState,
    "DV_PERIODIC_TIME_SPECIFICATION": DVPeriodicTimeSpecification,
    "DV_PROPORTION": DVProportion,
    "DV_SCALE": DVScale,
    "REFERENCE_RANGE": ReferenceRange,
    # RM : Common
    "PARTY_SELF": PartySelf,
    "EHR": EHR,
    "EHR_STATUS": EHRStatus,
    "ARCHETYPED": Archetyped,
    "PERSON": Person,
    "PARTY_IDENTITY": PartyIdentity,
    "ITEM_TREE": ItemTree,
    "ELEMENT": Element,
    "CLUSTER": Cluster,
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
    "ATTESTATION": Attestation,
    "UPDATE_CONTRIBUTION": UpdateContribution,
    "UPDATE_VERSION": UpdateVersion,
    "UPDATE_AUDIT": UpdateAudit,
    "UPDATE_ATTESTATION": UpdateAttestation,
    "ORGANISATION": Organisation,
    "CONTACT": Contact,
    "ADDRESS": Address,
    "TEMPLATE": OperationalTemplate,
    "ARCHETYPE": Archetype,
    "C_STRING": CString,
    "AGENT": Agent,
    "COMPOSITION": Composition,
    "VERSIONED_COMPOSITION": VersionedComposition,
    "ROLE": Role,
    "PYEHR_ACCESS_CONTROL_SETTINGS": PyehrAccessControlSettings,
    "PYEHR_ACCESS_POLICY_ITEM": PyehrAccessPolicyItem,
    "FOLDER": Folder
}
"""Map of OpenEHR string type names (e.g. as found in '_type' JSON) to pyehr Python types"""

def get_openehr_type_str(obj: AnyClass) -> str:
    type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

    if type_str == "VERSION":
        if isinstance(obj, UpdateVersion):
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj._inner_original_version.data())]}>"
        else:
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

    return type_str