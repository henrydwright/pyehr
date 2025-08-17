from abc import ABC, abstractmethod

from org.openehr.rm.data_types.text import CodePhrase

class OpenEHRCodeSetIdentifiers:
    """List of identifiers for code sets in the openEHR terminology."""

    CODE_SET_ID_CHARACTER_SETS = "character sets"
    CODE_SET_ID_COMPRESSION_ALGORITHMS = "compression algorithms"
    CODE_SET_ID_COUNTRIES = "countries"
    CODE_SET_INTEGRITY_CHECK_ALGORITHMS = "integrity check algorithms"
    CODE_SET_ID_LANGUAGES = "languages"
    CODE_SET_ID_MEDIA_TYPES = "media types"
    CODE_SET_ID_NORMAL_STATUSES = "normal statuses"

    def valid_code_set_id(an_id: str) -> bool:
        """Validity function to test if an identifier is in the set defined by this class."""
        return (
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_COMPRESSION_ALGORITHMS) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_COUNTRIES) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_INTEGRITY_CHECK_ALGORITHMS) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_MEDIA_TYPES) or
            (an_id == OpenEHRCodeSetIdentifiers.CODE_SET_ID_NORMAL_STATUSES)
        )
    
class OpenEHRTerminologyGroupIdentifiers:
    """List of identifiers for groups in the openEHR terminology."""

    TERMINOLOGY_ID_OPENEHR = "openehr"
    """Name of openEHR's own terminology."""

    GROUP_ID_AUDIT_CHANGE_TYPE = "audit change type"
    GROUP_ID_ATTESTATION_REASON = "attestation reason"
    GROUP_ID_COMPOSITION_CATEGORY = "composition category"
    GROUP_ID_EVENT_MATH_FUNCTION = "event math function"
    GROUP_ID_INSTRUCTION_STATES = "instruction states"
    GROUP_ID_INSTRUCTION_TRANSITIONS = "instruction transitions"
    GROUP_ID_NULL_FLAVOURS = "null flavours"
    GROUP_ID_PROPERTY = "property"
    GROUP_ID_PARTICIPATION_FUNCTION = "participation function"
    GROUP_ID_SETTING = "setting"
    GROUP_ID_TERM_MAPPING_PURPOSE = "term mapping purpose"
    GROUP_ID_SUBJECT_RELATIONSHIP = "subject relationship"
    GROUP_ID_VERSION_LIFE_CYCLE_STATE = "version lifecycle state"

    # TODO: report typo in spec where an_id is a boolean - https://specifications.openehr.org/releases/RM/Release-1.1.0/support.html#_openehr_code_set_identifiers_class
    def valid_terminology_group_id(an_id : str) -> bool:
        """Validity function to test if an identifier is in the set defined by this class."""
        return (
            (an_id == OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_AUDIT_CHANGE_TYPE) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_ATTESTATION_REASON) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_COMPOSITION_CATEGORY) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_EVENT_MATH_FUNCTION) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_INSTRUCTION_STATES) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_INSTRUCTION_TRANSITIONS) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_NULL_FLAVOURS) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PROPERTY) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_PARTICIPATION_FUNCTION) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_SETTING) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_TERM_MAPPING_PURPOSE) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_SUBJECT_RELATIONSHIP) or
            (an_id == OpenEHRTerminologyGroupIdentifiers.GROUP_ID_VERSION_LIFE_CYCLE_STATE)
        )

class ICodeSetAccess(ABC):
    """Defines an object providing proxy access to a code_set."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def id(self) -> str:
        """External identifier of this code set."""
        pass

    @abstractmethod
    def all_codes(self) -> list[CodePhrase]:
        """Return all codes known in this code set."""
        pass

    @abstractmethod
    def has_lang(self, a_lang: str) -> bool:
        """True if code set knows about 'a_lang'."""
        pass

    @abstractmethod
    def has_code(self, a_code: str) -> bool:
        """True if code set knows about 'a_code'."""
        pass

class ITerminologyAccess(ABC):
    """Defines an object providing proxy access to a terminology."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def id(self) -> str:
        """Identification of this Terminology."""
        pass

    # TODO: specification says single CodePhrase but should be a list clearly - https://specifications.openehr.org/releases/RM/Release-1.1.0/support.html#_terminology_package
    @abstractmethod
    def all_codes(self) -> list[CodePhrase]:
        """Return all codes known in this terminology."""
        pass

    @abstractmethod
    def codes_for_group_id(self, a_group_id : str) -> list[CodePhrase]:
        """Return all codes under grouper 'a_group_id' from this terminology."""
        pass

    @abstractmethod
    def codes_for_group_name(self, a_lang: str, a_name: str) -> list[CodePhrase]:
        """Return all codes under grouper whose name in 'a_lang' is 'a_name' from this terminology."""
        pass

    # TODO: This looks like it's an error in definition so assuming it should have an a_code and group_id argument. Report to fix https://specifications.openehr.org/releases/RM/Release-1.1.0/support.html#_openehr_code_set_identifiers_class
    @abstractmethod
    def has_code_for_group_id(self, a_code : str, group_id: str) -> bool:
        """True if a_code' is known in group group_id' in the openEHR terminology."""
        pass

    # TODO: Looks like another error in definition and should have lang as an argument...
    @abstractmethod
    def rubric_for_code(self, code : str, lang: str) -> str:
        """Return all rubric of code code' in language lang'."""
        pass

# chose not to inherit from OPENEHR_TERMINOLOGY_GROUP_IDENTIFIERS, OPENEHR_CODE_SET_IDENTIFIERS as
#  static classes whose constants will always be available

# chose to make this an abstract class which implementations can inherit
class TerminologyService(ABC):
    """Defines an object providing proxy access to a terminology service."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def terminology(self, name: str) -> ITerminologyAccess:
        """Return an interface to the terminology named name. Allowable names include:
        - openehr,
        - centc251,
        - any name from the US NLM UMLS meta-data list at http://www.nlm.nih.gov/research/umls/metaa1.html"""
        pass
    
    @abstractmethod
    def code_set(self, name: str) -> ICodeSetAccess:
        """Return an interface to the code_set identified by the external identifier name (e.g. ISO_639-1)."""
        pass
    
    @abstractmethod
    def code_set_for_id(self, name: str) -> ICodeSetAccess:
        """Return an interface to the code_set identified internally in openEHR by id."""
        pass
    
    @abstractmethod
    def has_terminology(self, name: str) -> bool:
        """True if terminology named name known by this service. Allowable names include:
        - openehr
        - centc251
        - any name from the US NLM UMLS meta-data list at http://www.nlm.nih.gov/research/umls/metaa1.html"""
        pass

    @abstractmethod
    def has_code_set(self, name: str) -> bool:
        """True if code_set linked to internal name (e.g. languages) is available."""
        pass

    @abstractmethod
    def terminology_identifiers(self) -> list[str]:
        """Set of all terminology identifiers known in the terminology service. Values from the US NLM UMLS meta-data list at: http://www.nlm.nih.gov/research/umls/metaa1.html"""
        pass

    @abstractmethod
    def openehr_code_sets(self) -> dict[str, str]:
        """Set of all code sets identifiers for which there is an internal openEHR name; returned as a Map of ids keyed by internal name."""
        pass

    # TODO: Think the description of the methods 'openehr_code_sets' and 'code_set_identifiers' has been reversed in https://specifications.openehr.org/releases/RM/Release-1.1.0/support.html#_terminology_service_class
    @abstractmethod
    def code_set_identifiers(self) -> list[str]:
        """Set of all code set identifiers known in the terminology service."""
        pass
    
