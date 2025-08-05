

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
