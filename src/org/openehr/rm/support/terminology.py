

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