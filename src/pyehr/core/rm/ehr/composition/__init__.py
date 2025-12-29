"""The Composition is the primary 'data container' in the openEHR EHR and is the 
root point of clinical content. Instances of the COMPOSITION class can be 
considered as self-standing data aggregations, or documents in a 
document-oriented system. """

from typing import Optional
from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable, PyehrInternalPathPredicateType, PyehrInternalProcessedPath
from pyehr.core.rm.common.generic import PartyProxy
from pyehr.core.rm.data_types.text import CodePhrase, DVCodedText, DVText
from pyehr.core.rm.ehr.composition.content import ContentItem
from pyehr.core.rm.support.terminology import OpenEHRCodeSetIdentifiers, OpenEHRTerminologyGroupIdentifiers, TerminologyService, util_verify_code_in_openehr_codeset_or_error, util_verify_code_in_openehr_terminology_group_or_error

class EventContext(Pathable):
    pass

class Composition(Locatable):
    """Content of one version in a VERSIONED_COMPOSITION. A Composition is 
    considered the unit of modification of the record, the unit of transmission 
    in record Extracts, and the unit of attestation by authorising clinicians. 
    In this latter sense, it may be considered equivalent to a signed document.

    Note: It is strongly recommended that the inherited attribute uid be populated
    in Compositions, using the UID copied from the object_id() of the uid field of
    the enclosing VERSION object.
    For example, the ORIGINAL_VERSION.uid 
    `87284370-2D4B-4e3d-A3F3-F303D2F4F34B::uk.nhs.ehr1::2` would be copied to the 
    uid field of the Composition."""

    language: CodePhrase
    """Mandatory indicator of the localised language in which this Composition 
    is written. Coded from openEHR Code Set languages. The language of an Entry 
    if different from the Composition is indicated in `ENTRY.language`."""

    territory: CodePhrase
    """Name of territory in which this Composition was written. Coded from 
    openEHR countries code set, which is an expression of the ISO 3166 standard."""
    
    category: DVCodedText
    """Temporal category of this Composition, i.e.

    * `431|persistent|` - of potential life-time validity;
    * `451|episodic|` - valid over the life of a care episode;
    * `433|event|` - valid at the time of recording (long-term validity requires subsequent clinical assessment).

    or any other code defined in the openEHR terminology group 'category'."""

    context: Optional[EventContext]
    """The clinical session context of this Composition, i.e. the contextual 
    attributes of the clinical session."""

    composer: PartyProxy
    """The person primarily responsible for the content of the Composition 
    (but not necessarily its committal into the EHR system). This is the 
    identifier which should appear on the screen. It may or may not be the 
    person who entered the data. When it is the patient, the special self 
    instance of PARTY_PROXY will be used."""

    content: Optional[list[ContentItem]]
    """The content of this Composition."""

    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                language: CodePhrase,
                territory: CodePhrase,
                category: DVCodedText,
                composer: PartyProxy,
                archetype_details : Archetyped,
                terminology_service: TerminologyService,
                context: Optional[EventContext] = None,
                content: Optional[list[ContentItem]] = None,
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
            code=territory,
            codeset_name=OpenEHRCodeSetIdentifiers.CODE_SET_ID_COUNTRIES,
            terminology_service=terminology_service,
            invariant_name_for_error="territory_valid"
        )
        self.territory = territory
        util_verify_code_in_openehr_terminology_group_or_error(
            code=category.defining_code,
            terminology_group_id=OpenEHRTerminologyGroupIdentifiers.GROUP_ID_COMPOSITION_CATEGORY,
            terminology_service=terminology_service,
            invariant_name_for_error="category_validity"
        )
        self.category = category
        self.composer = composer
        self.context = context
        if content is not None and len(content) == 0:
            raise ValueError("If content is provided it cannot be an empty list (invariant: content_valid)")
        self.content = content
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def is_persistent(self) -> bool:
        """True if category is 431|persistent|, False otherwise. Useful for 
        finding Compositions in an EHR which are guaranteed to be of interest 
        to most users."""
        return (self.category.defining_code.code_string == "431")

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ITEM_TREE)")

        if path.current_node_attribute == "content":
           return self._path_resolve_item_list(path, self.content, single_item, check_only)
        elif path.current_node_attribute == "context":
            return self._path_resolve_single(path, self.context, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'content' or 'context' at COMPOSITION but found \'{path.current_node_attribute}\'")
         
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

