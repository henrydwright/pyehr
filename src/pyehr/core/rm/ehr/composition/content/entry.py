"""All information which is created in the openEHR health record is expressed 
as an instance of a class in the `entry` package, containing the `ENTRY` class 
and a number of descendants."""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import ObjectRef, UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalProcessedPath
from pyehr.core.rm.common.generic import Participation, PartyProxy, PartySelf
from pyehr.core.rm.data_structures.history import History
from pyehr.core.rm.data_structures.item_structure import ItemStructure
from pyehr.core.rm.data_types.encapsulated import DVParsable
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
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
    
class CareEntry(Entry):
    """The abstract parent of all clinical ENTRY subtypes. A CARE_ENTRY defines 
    protocol and guideline attributes for all clinical Entry subtypes."""

    protocol: Optional[ItemStructure]
    """Description of the method (i.e. how) the information in this entry was 
    arrived at. For `OBSERVATIONs`, this is a description of the method or 
    instrument used. For `EVALUATIONs`, how the evaluation was arrived at. 
    For `INSTRUCTIONs`, how to execute the Instruction. This may take the 
    form of references to guidelines, including manually followed and executable;
    knowledge references such as a paper in Medline; clinical reasons within a 
    larger care process."""

    guideline_id: Optional[ObjectRef]
    """Optional external identifier of guideline creating this Entry if relevant."""

    @abstractmethod
    def __init__(self, 
        name: DVText, 
        archetype_node_id: str,
        language: CodePhrase,
        encoding: CodePhrase,
        subject: PartyProxy,
        archetype_details : Archetyped,
        terminology_service: TerminologyService,
        protocol: Optional[ItemStructure] = None,
        guideline_id: Optional[ObjectRef] = None,
        other_participations : Optional[list[Participation]] = None,
        workflow_id : Optional[ObjectRef] = None,
        provider: Optional[PartyProxy] = None, 
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        self.protocol = protocol
        self.guideline_id = guideline_id
        super().__init__(name, archetype_node_id, language, encoding, subject, archetype_details, terminology_service, other_participations, workflow_id, provider, uid, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    @abstractmethod
    def as_json(self):
        draft = super().as_json()
        if self.protocol is not None:
            draft["protocol"] = self.protocol.as_json()
        if self.guideline_id is not None:
            draft["guideline_id"] = self.guideline_id.as_json()
        return draft
    
    @abstractmethod
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.protocol, other.protocol) and
                is_equal_value(self.guideline_id, other.guideline_id))
    
class Observation(CareEntry):
    """Entry subtype for all clinical data in the past or present, i.e. which 
    (by the time it is recorded) has already occurred. OBSERVATION data is 
    expressed using the class HISTORY<T>, which guarantees that it is situated 
    in time. OBSERVATION is used for all notionally objective (i.e. measured 
    in some way) observations of phenomena, and patient-reported phenomena, 
    e.g. pain.

    Not to be used for recording opinion or future statements of any kind, 
    including instructions, intentions, plans etc."""

    data: History[ItemStructure]
    """The data of this observation, in the form of a history of values which may 
    be of any complexity."""

    state: Optional[History[ItemStructure]]
    """Optional recording of the state of subject of this observation during the 
    observation process, in the form of a separate history of values which may be 
    of any complexity. State may also be recorded within the History of the data 
    attribute."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str,
        language: CodePhrase,
        encoding: CodePhrase,
        subject: PartyProxy,
        archetype_details : Archetyped,
        data: History[ItemStructure],
        terminology_service: TerminologyService,
        state: Optional[History[ItemStructure]] = None,
        protocol: Optional[ItemStructure] = None,
        guideline_id: Optional[ObjectRef] = None,
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
        self.state = state
        super().__init__(name, archetype_node_id, language, encoding, subject, archetype_details, terminology_service, protocol, guideline_id, other_participations, workflow_id, provider, uid, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (OBSERVATION)")

        if path.current_node_attribute == "data":
            return self._path_resolve_single(path, self.data, single_item, check_only)
        elif path.current_node_attribute == "protocol":
            return self._path_resolve_single(path, self.protocol, single_item, check_only)
        elif path.current_node_attribute == "state":
            return self._path_resolve_single(path, self.state, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'data', 'protocol' or 'state' at OBSERVATION but found \'{path.current_node_attribute}\'")
         
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
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition/OBSERVATION.json
        draft = super().as_json()
        draft["data"] = self.data.as_json()
        if self.state is not None:
            draft["state"] = self.state.as_json()
        draft["_type"] = "OBSERVATION"
        return draft
    
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.data, other.data) and
                is_equal_value(self.state, other.state))
    
class Evaluation(CareEntry):
    """Entry type for evaluation statements. Used for all kinds of statements 
    which evaluate other information, such as interpretations of observations, 
    diagnoses, differential diagnoses, hypotheses, risk assessments, goals and 
    plans.

    Should not be used for actionable statements such as medication orders - 
    these are represented using the INSTRUCTION type."""

    data: ItemStructure
    """The data of this evaluation, in the form of a spatial data structure."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str,
        language: CodePhrase,
        encoding: CodePhrase,
        subject: PartyProxy,
        archetype_details : Archetyped,
        data: ItemStructure,
        terminology_service: TerminologyService,
        protocol: Optional[ItemStructure] = None,
        guideline_id: Optional[ObjectRef] = None,
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
        super().__init__(name, archetype_node_id, language, encoding, subject, archetype_details, terminology_service, protocol, guideline_id, other_participations, workflow_id, provider, uid, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.data, other.data))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition/EVALUATION.json
        draft = super().as_json()
        draft["data"] = self.data.as_json()
        draft["_type"] = "EVALUATION"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (EVALUATION)")

        if path.current_node_attribute == "data":
            return self._path_resolve_single(path, self.data, single_item, check_only)
        elif path.current_node_attribute == "protocol":
            return self._path_resolve_single(path, self.protocol, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'data' or 'protocol' at EVALUATION but found \'{path.current_node_attribute}\'")
         
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
        
class Activity(Locatable):
    """Defines a single activity within an Instruction, such as a medication 
    administration."""
    
    timing: Optional[DVParsable]
    """Timing of the activity, in the form of a parsable string. If used, the 
    preferred syntax is ISO8601 'R' format, but other formats may be used 
    including HL7 GTS.

    May be omitted if:
    * timing is represented structurally in the description attribute (e.g. via archetyped elements), or
    * unavailable, e.g. imported legacy data; in such cases, the INSTRUCTION.narrative should carry text that indicates the timing of its activities."""

    action_archetype_id: str
    """Perl-compliant regular expression pattern, enclosed in '//' delimiters, 
    indicating the valid identifiers of archetypes for Actions corresponding to 
    this Activity specification.

    Defaults to /.*/, meaning any archetype."""

    description: ItemStructure
    """Description of the activity, in the form of an archetyped structure."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                description: ItemStructure,
                action_archetype_id: str = "/.*/",
                timing: Optional[DVParsable] = None,
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        self.description = description
        if action_archetype_id == "":
            raise ValueError("action_archetype_id cannot be empty (invariant: action_archetype_id_valid)")
        self.action_archetype_id = action_archetype_id
        self.timing = timing
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ACTIVITY)")

        if path.current_node_attribute == "description":
            return self._path_resolve_single(path, self.description, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'description' at ACTIVITY but found \'{path.current_node_attribute}\'")
         
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
        
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.timing, other.timing) and
                is_equal_value(self.action_archetype_id, other.action_archetype_id) and
                is_equal_value(self.description, other.description))
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition/ACTIVITY.json
        draft = super().as_json()
        draft["action_archetype_id"] = self.action_archetype_id
        draft["description"] = self.description.as_json()
        if self.timing is not None:
            draft["timing"] = self.timing.as_json()
        draft["_type"] = "ACTIVITY"
        return draft
    
class Instruction(CareEntry):
    """Used to specify actions in the future. Enables simple and complex 
    specifications to be expressed, including in a fully-computable workflow 
    form. Used for any actionable statement such as medication and therapeutic 
    orders, monitoring, recall and review. Enough details must be provided for 
    the specification to be directly executed by an actor, either human or machine.

    Not to be used for plan items which are only specified in general terms."""

    narrative: DVText
    """Mandatory human-readable version of what the Instruction is about."""

    expiry_time: Optional[DVDateTime]
    """Optional expiry date/time to assist determination of when an Instruction 
    can be assumed to have expired. This helps prevent false listing of 
    Instructions as Active when they clearly must have been terminated in some 
    way or other."""

    wf_definition: Optional[DVParsable]
    """Optional workflow engine executable expression of the Instruction."""

    activities: Optional[list[Activity]]
    """List of all activities in Instruction."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str,
        language: CodePhrase,
        encoding: CodePhrase,
        subject: PartyProxy,
        archetype_details : Archetyped,
        narrative: DVText,
        terminology_service: TerminologyService,
        expiry_time: Optional[DVDateTime] = None,
        wf_definition: Optional[DVParsable] = None,
        activities: Optional[list[Activity]] = None,
        protocol: Optional[ItemStructure] = None,
        guideline_id: Optional[ObjectRef] = None,
        other_participations : Optional[list[Participation]] = None,
        workflow_id : Optional[ObjectRef] = None,
        provider: Optional[PartyProxy] = None, 
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        self.narrative = narrative
        self.expiry_time = expiry_time
        self.wf_definition = wf_definition
        self.activities = activities
        super().__init__(name, archetype_node_id, language, encoding, subject, archetype_details, terminology_service, protocol, guideline_id, other_participations, workflow_id, provider, uid, links, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (INSTRUCTION)")

        if path.current_node_attribute == "activities":
            return self._path_resolve_item_list(path, self.activities, single_item, check_only)
        elif path.current_node_attribute == "protocol":
            return self._path_resolve_single(path, self.protocol, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'description' at ACTIVITY but found \'{path.current_node_attribute}\'")
         
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
        
    def is_equal(self, other):
        return (
            super().is_equal(other)
            and is_equal_value(self.narrative, other.narrative)
            and is_equal_value(self.expiry_time, other.expiry_time)
            and is_equal_value(self.wf_definition, other.wf_definition)
            and is_equal_value(self.activities, other.activities)
        )
    
    def as_json(self):
        draft = super().as_json()
        draft["narrative"] = self.narrative.as_json()
        if self.expiry_time is not None:
            draft["expiry_time"] = self.expiry_time.as_json()
        if self.wf_definition is not None:
            draft["wf_definition"] = self.wf_definition.as_json()
        if self.activities is not None:
            draft["activities"] = [a.as_json() for a in self.activities]
        draft["_type"] = "INSTRUCTION"
        return draft