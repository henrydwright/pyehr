from pyehr.core.am.aom14.archetype import Archetype
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CString
from pyehr.core.am.opt14 import OperationalTemplate
from pyehr.core.base.base_types.identification import ISOOID, UUID, ArchetypeID, HierObjectID, LocatableRef, ObjectRef, ObjectVersionID, TemplateID, VersionTreeID
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.terminology import TerminologyCode, TerminologyTerm
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
from pyehr.core.base.resource import ResourceDescription, ResourceDescriptionItem, TranslationDetails
from pyehr.core.its.rest.additions import ADL14TemplateList, ADL14TemplateListItem, UpdateAttestation, UpdateAudit, UpdateContribution, UpdateVersion
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.its.rest.additions import UpdateVersion
from pyehr.core.rm.common.change_control import Contribution, OriginalVersion, VersionedObject
from pyehr.core.rm.common.directory import Folder, VersionedFolder
from pyehr.core.rm.composition import Composition, EventContext
from pyehr.core.rm.composition.content.entry import Action, Activity, AdminEntry, Evaluation, ISMTransition, Instruction, InstructionDetails, Observation
from pyehr.core.rm.composition.content.navigation import Section
from pyehr.core.rm.data_structures.history import History, IntervalEvent, PointEvent
from pyehr.core.rm.data_types.encapsulated import DVMultimedia, DVParsable
from pyehr.core.rm.data_types.quantity import DVCount, DVInterval, DVOrdinal, DVProportion, DVQuantity, DVScale, ReferenceRange
from pyehr.core.rm.data_types.text import DVParagraph, DVText, TermMapping
from pyehr.core.rm.data_types.time_specification import DVGeneralTimeSpecification, DVPeriodicTimeSpecification
from pyehr.core.rm.data_types.uri import DVEHRUri
from pyehr.core.rm.demographic import Agent, Capability, Group, Organisation, Party, PartyRelationship, Person, Role
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus, VersionedComposition
from pyehr.core.base.base_types.identification import HierObjectID, InternetID, ObjectRef, ObjectVersionID, GenericID, PartyRef, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.rm.common.change_control import Contribution, ImportedVersion, OriginalVersion, VersionedObject
from pyehr.core.rm.common.generic import Attestation, AuditDetails, Participation, PartyIdentified, PartyRelated, PartySelf, RevisionHistory, RevisionHistoryItem
from pyehr.core.rm.common.archetyped import Archetyped, ArchetypeID, FeederAudit, FeederAuditDetails, Link
from pyehr.core.rm.data_structures.item_structure import ItemList, ItemSingle, ItemTable, ItemTree
from pyehr.core.rm.data_structures.representation import Cluster, Element
from pyehr.core.rm.data_types.basic import DVBoolean, DVIdentifier, DVState
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDateTime, DVDuration, DVTime
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText, DVUri
from pyehr.core.rm.demographic import Address, Contact, Organisation, PartyIdentity, Person, VersionedParty
from pyehr.core.rm.ehr import EHR, EHRStatus, VersionedEHRStatus
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyItem


def _reverse_type_map(mp: dict[str, type]) -> dict[type, str]:
    ret = dict()
    for (str_type, py_type) in mp.items():
        ret[py_type] = str_type
    return ret

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
    # RM : Data Types
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
    "ATTESTATION": Attestation,
    "CONTRIBUTION": Contribution,
    "FEEDER_AUDIT": FeederAudit,
    "LINK": Link,
    "ORIGINAL_VERSION": OriginalVersion,
    "VERSIONED_OBJECT": VersionedObject,
    "ARCHETYPED": Archetyped,
    "PARTY_RELATED": PartyRelated,
    "REVISION_HISTORY_ITEM": RevisionHistoryItem,
    "FOLDER": Folder,
    "VERSIONED_FOLDER": VersionedFolder,
    "FEEDER_AUDIT_DETAILS": FeederAuditDetails,
    "PARTICIPATION": Participation,
    "IMPORTED_VERSION": ImportedVersion,
    "PARTY_SELF": PartySelf,
    "REVISION_HISTORY": RevisionHistory,
    "AUDIT_DETAILS": AuditDetails,
    "PARTY_IDENTIFIED": PartyIdentified,
    # RM : Data Structures
    "INTERVAL_EVENT": IntervalEvent,
    "ITEM_TABLE": ItemTable,
    "CLUSTER": Cluster,
    "ITEM_LIST": ItemList,
    "ITEM_TREE": ItemTree,
    "HISTORY": History,
    "POINT_EVENT": PointEvent,
    "ELEMENT": Element,
    "ITEM_SINGLE": ItemSingle,
    # RM : EHR
    "EHR": EHR,
    "EHR_STATUS": EHRStatus,
    "EHR_ACCESS": EHRAccess,
    "VERSIONED_EHR_STATUS": VersionedEHRStatus,
    "VERSIONED_PARTY": VersionedParty,
    # RM : Composition
    "ISM_TRANSITION": ISMTransition,
    "INSTRUCTION": Instruction,
    "ADMIN_ENTRY": AdminEntry,
    "ACTIVITY": Activity,
    "COMPOSITION": Composition,
    "VERSIONED_COMPOSITION": VersionedComposition,
    "INSTRUCTION_DETAILS": InstructionDetails,
    "EVALUATION": Evaluation,
    "EVENT_CONTEXT": EventContext,
    "SECTION": Section,
    "OBSERVATION": Observation,
    "ACTION": Action,
    # RM : Demographic
    "GROUP": Group,
    "PARTY_IDENTITY": PartyIdentity,
    "PERSON": Person,
    "AGENT": Agent,
    "ROLE": Role,
    "CONTACT": Contact,
    "ORGANISATION": Organisation,
    "PARTY_RELATIONSHIP": PartyRelationship,
    "ADDRESS": Address,
    "CAPABILITY": Capability,
    # REST API classes
    "UPDATE_CONTRIBUTION": UpdateContribution,
    "UPDATE_VERSION": UpdateVersion,
    "UPDATE_AUDIT": UpdateAudit,
    "UPDATE_ATTESTATION": UpdateAttestation,
    "ADL14_TEMPLATE_LIST": ADL14TemplateList,
    "ADL14_TEMPLATE_LIST_ITEM": ADL14TemplateListItem,
    # AM
    "TEMPLATE": OperationalTemplate,
    "ARCHETYPE": Archetype,
    "C_STRING": CString,
    # PYEHR CLASSES
    "PYEHR_ACCESS_CONTROL_SETTINGS": PyehrAccessControlSettings,
    "PYEHR_ACCESS_POLICY_ITEM": PyehrAccessPolicyItem,
}
"""Map of OpenEHR string type names (e.g. as found in '_type' JSON) to pyehr Python types"""

PYTHON_TYPE_TO_STRING_TYPE_MAP : dict[type, str] = _reverse_type_map(OPENEHR_TYPE_MAP)
"""Mapping of pyehr type (Python type) to the openEHR type string (e.g. pyehr type
of Party maps to 'PARTY')"""

def get_openehr_type_str(obj: AnyClass) -> str:
    type_str = PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj)]

    if type_str == "VERSION":
        if isinstance(obj, UpdateVersion):
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj._inner_original_version.data())]}>"
        else:
            type_str += f"<{PYTHON_TYPE_TO_STRING_TYPE_MAP[type(obj.data())]}>"

    return type_str