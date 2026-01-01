"""All information which is created in the openEHR health record is expressed 
as an instance of a class in the `entry` package, containing the `ENTRY` class 
and a number of descendants."""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import ObjectRef, UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Pathable, PyehrInternalProcessedPath
from pyehr.core.rm.common.generic import Participation, PartyProxy, PartySelf
from pyehr.core.rm.data_structures.item_structure import ItemStructure
from pyehr.core.rm.data_types.text import CodePhrase, DVText
from pyehr.core.rm.ehr.composition.content import ContentItem
from pyehr.core.rm.support.terminology import OpenEHRCodeSetIdentifiers, TerminologyService, util_verify_code_in_openehr_codeset_or_error


class Entry(ContentItem):
    """The abstract parent of all ENTRY subtypes. An ENTRY is the root of a 
    logical item of hard clinical information created in the clinical statement 
    context, within a clinical session. There can be numerous such contexts in 
    a clinical session. Observations and other Entry types only ever document 
    information captured/created in the event documented by the enclosing 
    Composition.

    An ENTRY is also the minimal unit of information any query should return, 
    since a whole ENTRY (including subparts) records spatial structure, timing 
    information, and contextual information, as well as the subject and generator 
    of the information."""

    language: CodePhrase
    """Mandatory indicator of the localised language in which this Entry is 
    written. Coded from openEHR Code Set languages."""

    encoding: CodePhrase
    """Name of character set in which text values in this Entry are encoded. 
    Coded from openEHR Code Set character sets."""

    other_participations: Optional[list[Participation]]
    """Other participations at `ENTRY` level."""

    workflow_id: Optional[ObjectRef]
    """Identifier of externally held workflow engine data for this workflow 
    execution, for this subject of care."""

    subject: PartyProxy
    """Id of human subject of this ENTRY, e.g.:
    
    * patient
    * organ donor
    * foetus
    * a family member
    * another clinically relevant person."""

    provider: Optional[PartyProxy]
    """Optional identification of provider of the information in this ENTRY, 
    which might be:

    * the patient
    * a patient agent, e.g. parent, guardian
    * the clinician
    * a device or software

    Generally only used when the recorder needs to make it explicit. Otherwise, 
    Composition composer and other participants are assumed."""

    @abstractmethod
    def __init__(self, 
            name: DVText, 
            archetype_node_id: str,
            language: CodePhrase,
            encoding: CodePhrase,
            subject: PartyProxy,
            archetype_details : Archetyped,
            terminology_service: TerminologyService,
            other_participations : Optional[list[Participation]] = None,
            workflow_id : Optional[ObjectRef] = None,
            provider: Optional[PartyProxy] = None, 
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        util_verify_code_in_openehr_codeset_or_error(
            code=language,
            codeset_name=OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES,
            terminology_service=terminology_service,
            invariant_name_for_error="language_valid"
        )
        self.language = language
        util_verify_code_in_openehr_codeset_or_error(
            code=encoding,
            codeset_name=OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS,
            terminology_service=terminology_service,
            invariant_name_for_error="encoding_valid"
        )
        self.encoding = encoding
        self.subject = subject
        if other_participations is not None and len(other_participations) == 0:
            raise ValueError("If provided, other_participations cannot be an empty list (invariant: other_participations_valid)")
        self.other_participations = other_participations
        self.workflow_id = workflow_id
        self.provider = provider
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def subject_is_self(self):
        """Returns True if this Entry is about the subject of the EHR, in which 
        case the subject attribute is of type PARTY_SELF."""
        return isinstance(self.subject, PartySelf)
    
    def is_equal(self, other: 'Entry'):
        return (super().is_equal(other) and
                is_equal_value(self.language, other.language) and
                is_equal_value(self.encoding, other.encoding) and 
                is_equal_value(self.subject, other.subject) and
                is_equal_value(self.provider, other.provider) and
                is_equal_value(self.other_participations, other.other_participations) and
                is_equal_value(self.workflow_id, other.workflow_id))
    
    @abstractmethod
    def as_json(self):
        # implement these in a similar way to descendants (e.g. ADMIN_ENTRY)
        draft = super().as_json()
        draft["language"] = self.language.as_json()
        draft["encoding"] = self.encoding.as_json()
        draft["subject"] = self.subject.as_json()
        if self.provider is not None:
            draft["provider"] = self.provider.as_json()
        if self.other_participations is not None:
            draft["other_participations"] = [p.as_json() for p in self.other_participations]
        if self.workflow_id is not None:
            draft["workflow_id"] = self.workflow_id.as_json()
        return draft
    
class AdminEntry(Entry):
    """Entry subtype for administrative information, i.e. information about 
    setting up the clinical process, but not itself clinically relevant. 
    Archetypes will define contained information.

    Used for administrative details of admission, episode, ward location, 
    discharge, appointment (if not stored in a practice management or 
    appointments system).

    Not to be used for any clinically significant information."""

    data: ItemStructure
    """Content of the Admin Entry. The data of the Entry; modelled in 
    archetypes."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str,
        language: CodePhrase,
        encoding: CodePhrase,
        subject: PartyProxy,
        archetype_details : Archetyped,
        terminology_service: TerminologyService,
        data: ItemStructure,
        other_participations : Optional[list[Participation]] = None,
        workflow_id : Optional[ObjectRef] = None,
        provider: Optional[PartyProxy] = None, 
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        self.data = data
        super().__init__(name, archetype_node_id, language, encoding, subject, archetype_details, terminology_service, other_participations, workflow_id, provider, uid, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ADMIN_ENTRY)")

        if path.current_node_attribute == "data":
            return self._path_resolve_single(path, self.data, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'data' at ADMIN_ENTRY but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
        
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition/ADMIN_ENTRY.json
        draft = super().as_json()
        draft["data"] = self.data.as_json()
        draft["_type"] = "ADMIN_ENTRY"
        return draft
    
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.data, other.data))