from typing import Optional

from pyehr.core.rm.support.terminology import TerminologyService, ICodeSetAccess, ITerminologyAccess, OpenEHRCodeSetIdentifiers, OpenEHRTerminologyGroupIdentifiers
from pyehr.core.rm.data_types.text import CodePhrase
from pyehr.core.base.base_types.identification import TerminologyID

class ListCodeSetAccess(ICodeSetAccess):
    """Provides a code set access for a given list of
    CodePhrases in a single language"""

    _id : str
    _language : str
    _code_dict : dict[str, CodePhrase]
    
    def __init__(self, id: str, lang: str, code_list: list[CodePhrase]):
        self._id = id
        self._language = lang
        self._code_dict = dict()
        for code in code_list:
            self._code_dict[code.code_string] = code
        super().__init__()

    def id(self):
        return self._id

    def all_codes(self):
        return list(self._code_dict.values())

    def has_lang(self, a_lang: str):
        return (a_lang == self._language)
    
    def has_code(self, a_code: str):
        return (a_code in self._code_dict)

class DictTerminologyAccess(ITerminologyAccess):
    """Provides a terminology access for groups of 
     lists of code phrases in a single language"""
    
    _id : str
    _name : str
    _language : str
    _groupid_code_dict : dict[str, dict[str, CodePhrase]]
    _groupname_code_dict : dict[str, dict[str, CodePhrase]]
    _all_code_dict: dict[str, CodePhrase]

    def __init__(self, id: str, lang: str, code_dict: dict[tuple[str, str], list[CodePhrase]]):
        self._id = id
        self._language = lang
        self._groupid_code_dict = dict()
        self._groupname_code_dict = dict()
        self._all_code_dict = dict()
        for (group_id, group_name) in code_dict.keys():
            group_list = code_dict[(group_id, group_name)]
            for code in group_list:
                if group_id not in self._groupid_code_dict:
                    self._groupid_code_dict[group_id] = dict()
                if group_name not in self._groupname_code_dict:
                    self._groupname_code_dict[group_name] = self._groupid_code_dict[group_id]
                # due to reference already in place this also adds to group_name
                self._groupid_code_dict[group_id][code.code_string] = code
                self._all_code_dict[code.code_string] = code
        super().__init__()

    def id(self):
        return self._id
    
    def all_codes(self):
        return list(self._all_code_dict.values())
    
    def codes_for_group_id(self, a_group_id):
        if a_group_id not in self._groupid_code_dict:
            raise ValueError(f"Group with ID \'{a_group_id}\' not found in this terminology service")
        
        return list(self._groupid_code_dict[a_group_id].values())
    
    def codes_for_group_name(self, a_lang, a_name):
        if a_lang != self._language:
            raise ValueError(f"This terminology does not support language '{a_lang}'. It only supports '{self._language}'")
        
        if a_name not in self._groupname_code_dict:
            raise ValueError(f"Group with name \'{a_name}\' in language \'{a_lang}\' not found in this terminology service")

        return list(self._groupname_code_dict[a_name].values())
    
    def has_code_for_group_id(self, a_code, group_id):
        if group_id not in self._groupid_code_dict:
            raise ValueError(f"Group with ID \'{group_id}\' not found in this terminology service")
        candidates = self.codes_for_group_id(group_id)
        for candidate_code in candidates:
            if candidate_code.code_string == a_code:
                return True
            
    def rubric_for_code(self, code, lang):
        if lang != self._language:
            raise ValueError(f"This terminology does not support language '{lang}'. It only supports '{self._language}'")
        
        if code not in self._all_code_dict:
            raise ValueError(f"Could not find code '{code}' in the terminology")
        
        return self._all_code_dict[code].preferred_term


class PythonTerminologyService(TerminologyService):
    """Terminology service providing some set code sets and
    terminologies to provide testing"""

    _code_sets : dict[str, ListCodeSetAccess]
    _terminologies: dict[str, DictTerminologyAccess]

    _OPENEHR_CODE_SET_MAP : dict[str, str] = {
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_COUNTRIES : "ISO_3166-1",
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_CHARACTER_SETS: "IANA_character-sets",
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_LANGUAGES : "ISO_639-1",
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_MEDIA_TYPES: "IANA_media-types",
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_COMPRESSION_ALGORITHMS: "openehr_compression_algorithms",
        OpenEHRCodeSetIdentifiers.CODE_SET_INTEGRITY_CHECK_ALGORITHMS: "openehr_integrity_check_algorithms",
        OpenEHRCodeSetIdentifiers.CODE_SET_ID_NORMAL_STATUSES: "openehr_normal_statuses"
    }

    def __init__(self, code_sets: Optional[list[ListCodeSetAccess]], terminologies: Optional[list[DictTerminologyAccess]]):
        self._code_sets = dict()
        self._terminologies = dict()
        self._openehr_supported_codesets = dict()

        if code_sets is not None:
            for code_set in code_sets:
                self._code_sets[code_set.id()] = code_set
        
        if terminologies is not None:
            for terminology in terminologies:
                self._terminologies[terminology.id()] = terminology

        super().__init__()
    
    def terminology(self, name):
        if name not in self._terminologies:
            raise ValueError(f"Terminology \'{name}\' not found in terminology service")
        return self._terminologies[name]
    
    def code_set(self, name):
        if name not in self._code_sets:
            raise ValueError(f"Code set \'{name}\' not found in terminology service")
        return self._code_sets[name]
    
    def code_set_for_id(self, name):
        if not OpenEHRCodeSetIdentifiers.valid_code_set_id(name):
            raise ValueError(f"Code set name \'{name}\' is not a valid openehr internal ID")
        else:
            return self.code_set(self._OPENEHR_CODE_SET_MAP[name])
        
    def has_terminology(self, name):
        return (name in self._terminologies)
    
    def has_code_set(self, name):
        if not OpenEHRCodeSetIdentifiers.valid_code_set_id(name):
            raise ValueError(f"Code set name \'{name}\' is not a valid openehr internal ID")
        
        return (self._OPENEHR_CODE_SET_MAP[name]) in self._code_sets
        
    def terminology_identifiers(self):
        return list(self._terminologies.keys())
    
    def openehr_code_sets(self):
        return_value = dict()
        for openehr_internal_name in self._OPENEHR_CODE_SET_MAP:
            print("Checking", openehr_internal_name, "=", self._OPENEHR_CODE_SET_MAP[openehr_internal_name])
            if self.has_code_set(openehr_internal_name):
                print("Found")
                return_value[openehr_internal_name] = self._OPENEHR_CODE_SET_MAP[openehr_internal_name]
        return return_value
    
    def code_set_identifiers(self):
        return list(self._code_sets.keys())
    

TERMINOLOGYID_OPENEHR_CHARACTER_SETS = TerminologyID("IANA_character-sets")
TERMINOLOGYID_OPENEHR_COUNTRIES = TerminologyID("ISO_3166-1")
TERMINOLOGYID_OPENEHR_LANGUAGES = TerminologyID("ISO_639-1")
TERMINOLOGYID_OPENEHR_MEDIA_TYPES = TerminologyID("IANA_media-types")
TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS = TerminologyID("openehr_compression_algorithms")
TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS = TerminologyID("openehr_integrity_check_algorithms")
TERMINOLOGYID_OPENEHR_NORMAL_STATUSES = TerminologyID("openehr_normal_statuses")
TERMINOLOGYID_OPENEHR = TerminologyID(OpenEHRTerminologyGroupIdentifiers.TERMINOLOGY_ID_OPENEHR)

CODELIST_OPENEHR_CHARACTER_SETS = [
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "ISO-10646-UTF-1"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "ISO_8859-1:1987"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "ISO-8859-2"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "ISO_8859-3:1988"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "ISO-8859-15"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "US-ASCII"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-7"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-8"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-16"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-16BE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-16LE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-32"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-32BE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_CHARACTER_SETS, "UTF-32LE")
]
CODELIST_OPENEHR_COUNTRIES = [
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AF", "AFGHANISTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AX", "ÅLAND ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AL", "ALBANIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DZ", "ALGERIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AS", "AMERICAN SAMOA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AD", "ANDORRA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AO", "ANGOLA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AI", "ANGUILLA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AQ", "ANTARCTICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AG", "ANTIGUA AND BARBUDA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AR", "ARGENTINA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AM", "ARMENIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AW", "ARUBA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AU", "AUSTRALIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AT", "AUSTRIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AZ", "AZERBAIJAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BS", "BAHAMAS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BH", "BAHRAIN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BD", "BANGLADESH"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BB", "BARBADOS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BY", "BELARUS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BE", "BELGIUM"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BZ", "BELIZE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BJ", "BENIN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BM", "BERMUDA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BT", "BHUTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BO", "BOLIVIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BQ", "BONAIRE, SINT EUSTATIUS AND SABA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BA", "BOSNIA AND HERZEGOVINA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BW", "BOTSWANA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BV", "BOUVET ISLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BR", "BRAZIL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IO", "BRITISH INDIAN OCEAN TERRITORY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BN", "BRUNEI DARUSSALAM"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BG", "BULGARIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BF", "BURKINA FASO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BI", "BURUNDI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KH", "CAMBODIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CM", "CAMEROON"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CA", "CANADA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CV", "CAPE VERDE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KY", "CAYMAN ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CF", "CENTRAL AFRICAN REPUBLIC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TD", "CHAD"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CL", "CHILE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CN", "CHINA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CX", "CHRISTMAS ISLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CC", "COCOS (KEELING) ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CO", "COLOMBIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KM", "COMOROS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CG", "CONGO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CD", "CONGO, THE DEMOCRATIC REPUBLIC OF THE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CK", "COOK ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CR", "COSTA RICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CI", "CÔTE D’IVOIRE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HR", "CROATIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CU", "CUBA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CW", "CURAÇAO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CY", "CYPRUS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CZ", "CZECH REPUBLIC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DK", "DENMARK"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DJ", "DJIBOUTI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DM", "DOMINICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DO", "DOMINICAN REPUBLIC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "EC", "ECUADOR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "EG", "EGYPT"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SV", "EL SALVADOR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GQ", "EQUATORIAL GUINEA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ER", "ERITREA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "EE", "ESTONIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SZ", "ESWATINI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ET", "ETHIOPIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FK", "FALKLAND ISLANDS (MALVINAS)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FO", "FAROE ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FJ", "FIJI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FI", "FINLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FR", "FRANCE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GF", "FRENCH GUIANA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PF", "FRENCH POLYNESIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TF", "FRENCH SOUTHERN TERRITORIES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GA", "GABON"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GM", "GAMBIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GE", "GEORGIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "DE", "GERMANY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GH", "GHANA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GI", "GIBRALTAR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GR", "GREECE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GL", "GREENLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GD", "GRENADA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GP", "GUADELOUPE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GU", "GUAM"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GT", "GUATEMALA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GG", "GUERNSEY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GN", "GUINEA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GW", "GUINEA-BISSAU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GY", "GUYANA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HT", "HAITI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HM", "HEARD ISLAND AND MCDONALD ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VA", "HOLY SEE (VATICAN CITY STATE)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HN", "HONDURAS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HK", "HONG KONG"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "HU", "HUNGARY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IS", "ICELAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IN", "INDIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ID", "INDONESIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IR", "IRAN, ISLAMIC REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IQ", "IRAQ"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IE", "IRELAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IM", "ISLE OF MAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IL", "ISRAEL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "IT", "ITALY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "JM", "JAMAICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "JP", "JAPAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "JE", "JERSEY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "JO", "JORDAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KZ", "KAZAKHSTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KE", "KENYA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KI", "KIRIBATI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KP", "KOREA, DEMOCRATIC PEOPLE’S REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KR", "KOREA, REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KW", "KUWAIT"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KG", "KYRGYZSTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LA", "LAO PEOPLE’S DEMOCRATIC REPUBLIC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LV", "LATVIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LB", "LEBANON"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LS", "LESOTHO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LR", "LIBERIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LY", "LIBYA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LI", "LIECHTENSTEIN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LT", "LITHUANIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LU", "LUXEMBOURG"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MO", "MACAO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MG", "MADAGASCAR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MW", "MALAWI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MY", "MALAYSIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MV", "MALDIVES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ML", "MALI"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MT", "MALTA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MH", "MARSHALL ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MQ", "MARTINIQUE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MR", "MAURITANIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MU", "MAURITIUS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "YT", "MAYOTTE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MX", "MEXICO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "FM", "MICRONESIA, FEDERATED STATES OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MD", "MOLDOVA, REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MC", "MONACO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MN", "MONGOLIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ME", "MONTENEGRO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MS", "MONTSERRAT"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MA", "MOROCCO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MZ", "MOZAMBIQUE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MM", "MYANMAR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NA", "NAMIBIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NR", "NAURU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NP", "NEPAL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NL", "NETHERLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AN", "NETHERLANDS ANTILLES - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NC", "NEW CALEDONIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NZ", "NEW ZEALAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NI", "NICARAGUA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NE", "NIGER"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NG", "NIGERIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NU", "NIUE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NF", "NORFOLK ISLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MK", "NORTH MACEDONIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MP", "NORTHERN MARIANA ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "NO", "NORWAY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "OM", "OMAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PK", "PAKISTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PW", "PALAU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PS", "PALESTINIAN, STATE OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PA", "PANAMA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PG", "PAPUA NEW GUINEA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PY", "PARAGUAY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PE", "PERU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PH", "PHILIPPINES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PN", "PITCAIRN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PL", "POLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PT", "PORTUGAL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PR", "PUERTO RICO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "QA", "QATAR"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "RE", "RÉUNION"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "RO", "ROMANIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "RU", "RUSSIAN FEDERATION"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "RW", "RWANDA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "BL", "SAINT BARTHÉLEMY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SH", "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "KN", "SAINT KITTS AND NEVIS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LC", "SAINT LUCIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "MF", "SAINT MARTIN (FRENCH PART)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "PM", "SAINT PIERRE AND MIQUELON"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VC", "SAINT VINCENT AND THE GRENADINES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "WS", "SAMOA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SM", "SAN MARINO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ST", "SAO TOME AND PRINCIPE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SA", "SAUDI ARABIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SN", "SENEGAL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "RS", "SERBIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SC", "SEYCHELLES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SL", "SIERRA LEONE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SG", "SINGAPORE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SX", "SINT MAARTEN (DUTCH PART)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SK", "SLOVAKIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SI", "SLOVENIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SB", "SOLOMON ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SO", "SOMALIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ZA", "SOUTH AFRICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GS", "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SS", "SOUTH SUDAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ES", "SPAIN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "LK", "SRI LANKA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SD", "SUDAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SR", "SURINAME"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SJ", "SVALBARD AND JAN MAYEN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SE", "SWEDEN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "CH", "SWITZERLAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "SY", "SYRIAN ARAB REPUBLIC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TW", "TAIWAN, PROVINCE OF CHINA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TJ", "TAJIKISTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TZ", "TANZANIA, UNITED REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TH", "THAILAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TL", "TIMOR-LESTE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TG", "TOGO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TK", "TOKELAU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TO", "TONGA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TT", "TRINIDAD AND TOBAGO"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TN", "TUNISIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TR", "TÜRKIYE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TM", "TURKMENISTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TC", "TURKS AND CAICOS ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "TV", "TUVALU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "UG", "UGANDA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "UA", "UKRAINE"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "AE", "UNITED ARAB EMIRATES"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "GB", "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "US", "UNITED STATES OF AMERICA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "UM", "UNITED STATES MINOR OUTLYING ISLANDS"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "UY", "URUGUAY"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "UZ", "UZBEKISTAN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VU", "VANUATU"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VE", "VENEZUELA, BOLIVARIAN REPUBLIC OF"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VN", "VIET NAM"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VG", "VIRGIN ISLANDS, BRITISH"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "VI", "VIRGIN ISLANDS, U.S."),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "WF", "WALLIS AND FUTUNA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "EH", "WESTERN SAHARA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "YE", "YEMEN"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ZM", "ZAMBIA"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COUNTRIES, "ZW", "ZIMBABWE")
]
CODELIST_OPENEHR_LANGUAGES = [
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "aa", "Afar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "af", "Afrikaans"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ak", "Akan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sq", "Albanian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "am", "Amharic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar", "Arabic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-sa", "Arabic (Saudi Arabia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-iq", "Arabic (Iraq)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-eg", "Arabic (Egypt)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-ly", "Arabic (Libya)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-dz", "Arabic (Algeria)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-ma", "Arabic (Morocco)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-tn", "Arabic (Tunisia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-om", "Arabic (Oman)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-ye", "Arabic (Yemen)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-sy", "Arabic (Syria)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-jo", "Arabic (Jordan)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-lb", "Arabic (Lebanon)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-kw", "Arabic (Kuwait)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-ae", "Arabic (U.A.E.)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-bh", "Arabic (Bahrain)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ar-qa", "Arabic (Qatar)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "an", "Aragonese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hy", "Armenian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "as", "Assamese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "av", "Avaric, Avar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ay", "Aymara"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "az", "Azerbaijani, Azeri"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bm", "Bambara"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ba", "Bashkir"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "eu", "Basque"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "be", "Belarusian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bn", "Bengali, Bangla"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bi", "Bislama"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bs", "Bosnian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "br", "Breton"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bg", "Bulgarian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "my", "Burmese, Myanmar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ca", "Catalan, Valencian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ch", "Chamorro"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ce", "Chechen"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ny", "Chichewa, Chewa, Nyanja"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh", "Chinese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh-tw", "Chinese (Taiwan)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh-cn", "Chinese (PRC)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh-hk", "Chinese (Hong Kong SAR)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh-sg", "Chinese (Singapore)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zh-mo", "Chinese (Macau)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cv", "Chuvash"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kw", "Cornish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "co", "Corsican"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cr", "Cree"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hr", "Croatian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hr-ba", "Croatian (Bosnia and Herzegovina)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cs", "Czech"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "da", "Danish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "dv", "Divehi, Dhivehi, Maldivian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nl", "Dutch"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nl-be", "Dutch (Belgium)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "dz", "Dzongkha"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en", "English"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-us", "English (United States)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-gb", "English (United Kingdom)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-au", "English (Australia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-ca", "English (Canada)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-nz", "English (New Zealand)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-ie", "English (Ireland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-za", "English (South Africa)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-jm", "English (Jamaica)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-cb", "English (Caribbean)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-bz", "English (Belize)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-tt", "English (Trinidad and Tobago)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-ph", "English (Republic of the Philippines)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "en-zw", "English (Zimbabwe)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "eo", "Esperanto"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "et", "Estonian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ee", "Ewe"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fo", "Faroese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fj", "Fijian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fi", "Finnish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr", "French"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr-be", "French (Belgium)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr-ca", "French (Canada)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr-ch", "French (Switzerland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr-lu", "French (Luxembourg)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fr-mc", "French (Principality of Monaco)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fy", "Frisian, Western Frisian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ff", "Fulah, Fulani"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gd", "Gaelic, Scottish Gaelic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gd-ie", "Gaelic (Ireland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gl", "Galician"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lg", "Ganda"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ka", "Georgian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "de", "German"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "de-ch", "German (Switzerland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "de-at", "German (Austria)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "de-lu", "German (Luxembourg)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "de-li", "German (Liechtenstein)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "el", "Greek"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kl", "Kalaallisut, Greenlandic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gn", "Guarani"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gu", "Gujarati"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ht", "Haitian, Haitian Creole"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ha", "Hausa"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "he", "Hebrew"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hz", "Herero"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hi", "Hindi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ho", "Hiri Motu, Pidgin Motu"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "hu", "Hungarian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "is", "Icelandic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ig", "Igbo"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "id", "Indonesian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "iu", "Inuktitut"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ik", "Inupiaq"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ga", "Irish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "it", "Italian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "it-ch", "Italian (Switzerland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ja", "Japanese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "jv", "Javanese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kn", "Kannada"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kr", "Kanuri"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ks", "Kashmiri"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kk", "Kazakh"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "km", "Central Khmer, Cambodian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ki", "Kikuyu, Gikuyu"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "rw", "Kinyarwanda"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ky", "Kirghiz, Kyrgyz"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kv", "Komi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kg", "Kongo"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ko", "Korean"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "kj", "Kuanyama, Kwanyama"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ku", "Kurdish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lo", "Lao"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "la", "Latin"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lv", "Latvian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "li", "Limburgan, Limburger, Limburgish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ln", "Lingala"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lt", "Lithuanian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lu", "Luba-Katanga, Luba-Shaba"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "lb", "Luxembourgish, Letzeburgesch"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mk", "Macedonian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mg", "Malagasy"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ms", "Malay"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ml", "Malayalam"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mt", "Maltese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "gv", "Manx"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mi", "Maori"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mr", "Marathi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mh", "Marshallese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "mn", "Mongolian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "na", "Nauru, Nauruan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nv", "Navajo, Navaho"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nd", "North Ndebele"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nr", "South Ndebele"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ng", "Ndonga"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ne", "Nepali"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nb", "Norwegian Bokmal"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "nn", "Norwegian Nynorsk"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ii", "Sichuan Yi, Nuosu, Northern Yi, Liangshan Yi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "oc", "Occitan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "oj", "Ojibwa, Ojibwe"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "or", "Oriya, Odia"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "om", "Oromo"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "os", "Ossetian, Ossetic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ps", "Pashto, Pushto"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "fa", "Persian, Farsi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "pl", "Polish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "pt", "Portuguese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "pt-br", "Portuguese (Brazil)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "pt-pt", "Portuguese (Portugal) - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "pa", "Punjabi, Panjabi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "qu", "Quechua"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "qu-bo", "Quechua (Bolivia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "qu-ec", "Quechua (Ecuador)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "qu-pe", "Quechua (Peru)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ro", "Romanian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ro-mo", "Romanian (Moldavia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "rm", "Romansh, Rhaeto-Romanic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "rn", "Rundi, Kirundi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ru", "Russian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ru-mo", "Russian (Moldavia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "se", "Northern Sami"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sz", "Sami (Lappish) - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sm", "Samoan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sg", "Sango"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sc", "Sardinian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sr", "Serbian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sr-ba", "Serbian (Bosnia and Herzegovina)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sb", "Serbian - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sn", "Shona"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sd", "Sindhi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "si", "Sinhala, Sinhalese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sk", "Slovak"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sl", "Slovenian, Slovene"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "so", "Somali"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "st", "Southern Sotho, Sesotho, Sutu"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es", "Spanish, Castilian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-mx", "Spanish (Mexico)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-gt", "Spanish (Guatemala)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-cr", "Spanish (Costa Rica)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-pa", "Spanish (Panama)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-do", "Spanish (Dominican Republic)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-ve", "Spanish (Venezuela)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-co", "Spanish (Colombia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-pe", "Spanish (Peru)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-ar", "Spanish (Argentina)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-ec", "Spanish (Ecuador)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-cl", "Spanish (Chile)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-uy", "Spanish (Uruguay)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-py", "Spanish (Paraguay)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-bo", "Spanish (Bolivia)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-sv", "Spanish (El Salvador)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-hn", "Spanish (Honduras)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-ni", "Spanish (Nicaragua)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "es-pr", "Spanish (Puerto Rico)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "su", "Sundanese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sx", "Sutu - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sw", "Swahili"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ss", "Swati, Swazi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sv", "Swedish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "sv-fi", "Swedish (Finland)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tl", "Tagalog"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ty", "Tahitian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tg", "Tajik"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ta", "Tamil"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tt", "Tatar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "te", "Telugu"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "th", "Thai"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "bo", "Tibetan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ti", "Tigrinya"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "to", "Tonga, Tongan"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ts", "Tsonga"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tn", "Tswana"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tr", "Turkish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tk", "Turkmen"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "tw", "Twi"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ug", "Uighur, Uyghur"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "uk", "Ukrainian"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ur", "Urdu"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "uz", "Uzbek"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ve", "Venda"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "vi", "Vietnamese"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "wa", "Walloon"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cy", "Welsh"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cy-gb", "Welsh (United Kingdom)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "cy-ar", "Welsh (Argentina)"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "wo", "Wolof"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "xh", "Xhosa"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "yi", "Yiddish"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "ji", "Yiddish - DEPRECATED"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "yo", "Yoruba"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "za", "Zhuang, Chuang"),
    CodePhrase(TERMINOLOGYID_OPENEHR_LANGUAGES, "zu", "Zulu")
]
CODELIST_OPENEHR_MEDIA_TYPES = [
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/DVI4"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G722"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G723"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G726-16"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G726-24"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G726-32"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G726-40"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G728"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/L8"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/L16"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/LPC"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G729"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G729D"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/G729E"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/BT656"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/CelB"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/JPEG"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/H261"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/H263"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/H263-1998"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/H263-2000"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/H264"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/MPV"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/mp4"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/ogg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/mpeg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/basic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/mpeg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/mpeg3"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/mpeg4-generic"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/mp4"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/L20"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/L24"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/telephone-event"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/ogg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "audio/vorbis"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "video/quicktime"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/calendar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/directory"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/html"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/plain"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/richtext"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/rtf"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/rfc822-headers"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/sgml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/tab-separated-values"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/uri-list"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "text/xml-external-parsed-entity"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/avif"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/bmp"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/cgm"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/gif"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/png"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/tiff"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/jpeg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/jp2"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "image/svg+xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/cda+xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/EDIFACT"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/fhir+json"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/fhir+xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/hl7v2+xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/gzip"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/json"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/msword"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/pdf"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/rtf"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/dicom"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/dicom+json"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/dicom+xml"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/octet-stream"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/ogg"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.base"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.chart"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.chart-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.formula"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.formula-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.graphics"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.graphics-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.image"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.image-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.presentation"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.presentation-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.spreadsheet"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.spreadsheet-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.text"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.text-master"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.text-template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.oasis.opendocument.text-web"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-word.document.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-word.template.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.openxmlformats-officedocument.wordprocessingml.template"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-powerpoint.slideshow.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.openxmlformats-officedocument.presentationml.slideshow"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-powerpoint.presentation.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-excel.sheet.binary.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-excel.sheet.macroEnabled.12"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-xpsdocument"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-excel"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-outlook"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.ms-powerpoint"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/vnd.rar"),
    CodePhrase(TERMINOLOGYID_OPENEHR_MEDIA_TYPES, "application/zip")
]
CODELIST_OPENEHR_COMPRESSION_ALGORITHMS = [
    CodePhrase(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS, "compress"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS, "deflate"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS, "gzip"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS, "zlib"),
    CodePhrase(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS, "other")
]
CODELIST_OPENEHR_INTEGRITY_CHECK_ALGORITHMS = [
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-1"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-224"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-256"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-384"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-512"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-512/224"),
    CodePhrase(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS, "SHA-512/256")
]
CODELIST_OPENEHR_NORMAL_STATUSES = [
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "HHH"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "HH"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "H"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "N"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "L"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "LL"),
    CodePhrase(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES, "LLL")
]

GROUPLIST_OPENEHR_TERM_MAPPING_PURPOSES = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "669", "public health"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "670", "reimbursement"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "671", "research study")
]
GROUPLIST_OPENEHR_SUBJECT_RELATIONSHIP = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "0", "self"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "3", "foetus"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "10", "mother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "9", "father"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "6", "donor"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "253", "unknown"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "261", "adopted daughter"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "260", "adopted son"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "259", "adoptive father"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "258", "adoptive mother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "256", "biological father"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "255", "biological mother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "23", "brother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "28", "child"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "265", "cohabitee"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "257", "cousin"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "29", "daughter"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "264", "guardian"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "39", "maternal aunt"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "8", "maternal grandfather"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "7", "maternal grandmother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "38", "maternal uncle"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "189", "neonate"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "254", "parent"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "22", "partner/spouse"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "41", "paternal aunt"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "36", "paternal grandfather"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "37", "paternal grandmother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "40", "paternal uncle"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "27", "sibling"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "24", "sister"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "31", "son"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "263", "step father"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "262", "step mother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "25", "step or half brother"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "26", "step or half sister")
]
GROUPLIST_OPENEHR_PARTICIPATION_FUNCTION = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "253", "unknown")
]
GROUPLIST_OPENEHR_PARTICIPATION_MODE = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "193", "not specified"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "216", "face-to-face communication"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "223", "interpreted face-to-face communication"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "217", "signing (face-to-face)"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "195", "live audiovisual; videoconference; videophone"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "198", "videoconferencing"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "197", "videophone"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "218", "signing over video"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "224", "interpreted video communication"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "194", "asynchronous audiovisual; recorded video"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "196", "recorded video"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "202", "live audio-only; telephone; internet phone; teleconference"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "204", "telephone"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "203", "teleconference"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "205", "internet telephone"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "222", "interpreted audio-only"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "199", "asynchronous audio-only; dictated; voice mail"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "200", "dictated"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "201", "voice-mail"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "212", "live text-only; internet chat; SMS chat; interactive written note"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "213", "internet chat"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "214", "SMS chat"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "215", "interactive written note"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "206", "asynchronous text; email; fax; letter; handwritten note; SMS message"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "211", "handwritten note"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "210", "printed/typed letter"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "207", "email"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "208", "facsimile/telefax"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "221", "translated text"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "209", "SMS message"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "219", "physically present"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "220", "physically remote")
]
GROUPLIST_OPENEHR_AUDIT_CHANGE_TYPE = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "249", "creation"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "250", "amendment"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "251", "modification"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "252", "synthesis"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "523", "deleted"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "666", "attestation"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "816", "restoration"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "817", "format conversion"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "253", "unknown")
]
GROUPLIST_OPENEHR_ATTESTATION_REASON = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "240", "signed"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "648", "witnessed")
]
GROUPLIST_OPENEHR_VERSION_LIFECYCLE_STATE = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "532", "complete"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "553", "incomplete"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "523", "deleted"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "800", "inactive"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "801", "abandoned")
]
GROUPLIST_OPENEHR_NULL_FLAVOURS = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "271", "no information"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "253", "unknown"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "272", "masked"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "273", "not applicable")
]
GROUPLIST_OPENEHR_EVENT_MATH_FUNCTION = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "145", "minimum"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "144", "maximum"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "267", "mode"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "268", "median"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "146", "mean"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "147", "change"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "148", "total"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "149", "variation"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "521", "decrease"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "522", "increase"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "640", "actual")
]
GROUPLIST_OPENEHR_COMPOSITION_CATEGORY = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "431", "persistent"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "451", "episodic"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "433", "event"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "815", "report"),
]
GROUPLIST_OPENEHR_SETTING = [
    CodePhrase(TERMINOLOGYID_OPENEHR, "225", "home"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "227", "emergency care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "228", "primary medical care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "229", "primary nursing care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "230", "primary allied health care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "231", "midwifery care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "232", "secondary medical care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "233", "secondary nursing care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "234", "secondary allied health care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "235", "complementary health care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "236", "dental care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "237", "nursing home care"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "802", "mental healthcare"),
    CodePhrase(TERMINOLOGYID_OPENEHR, "238", "other care"),
]

CODESET_OPENEHR_CHARACTER_SETS = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_CHARACTER_SETS.name(), "en", CODELIST_OPENEHR_CHARACTER_SETS)
CODESET_OPENEHR_COUNTRIES = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_COUNTRIES.name(), "en", CODELIST_OPENEHR_COUNTRIES)
CODESET_OPENEHR_LANGUAGES = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_LANGUAGES.name(), "en", CODELIST_OPENEHR_LANGUAGES)
CODESET_OPENEHR_MEDIA_TYPES = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_MEDIA_TYPES.name(), "en", CODELIST_OPENEHR_MEDIA_TYPES)
CODESET_OPENEHR_COMPRESSION_ALGORITHMS = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_COMPRESSION_ALGORITHMS.name(), "en", CODELIST_OPENEHR_COMPRESSION_ALGORITHMS)
CODESET_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_INTEGRITY_CEHCK_ALGORITHMS.name(), "en", CODELIST_OPENEHR_INTEGRITY_CHECK_ALGORITHMS)
CODESET_OPENEHR_NORMAL_STATUSES = ListCodeSetAccess(TERMINOLOGYID_OPENEHR_NORMAL_STATUSES.name(), "en", CODELIST_OPENEHR_NORMAL_STATUSES)

TERMINOLOGY_OPENEHR = DictTerminologyAccess("openehr", "en", {
    ("term_mapping_purpose", "term mapping purpose"): GROUPLIST_OPENEHR_TERM_MAPPING_PURPOSES,
    ("subject_relationship", "subject relationship"): GROUPLIST_OPENEHR_SUBJECT_RELATIONSHIP,
    ("participation_function", "participation function"): GROUPLIST_OPENEHR_PARTICIPATION_FUNCTION,
    ("participation_mode", "participation mode"): GROUPLIST_OPENEHR_PARTICIPATION_MODE,
    ("audit_change_type", "audit change type"): GROUPLIST_OPENEHR_AUDIT_CHANGE_TYPE,
    ("attestation_reason", "attestation reason"): GROUPLIST_OPENEHR_ATTESTATION_REASON,
    ("version_lifecycle_state", "version lifecycle state"): GROUPLIST_OPENEHR_VERSION_LIFECYCLE_STATE,
    ("null_flavours", "null flavours"): GROUPLIST_OPENEHR_NULL_FLAVOURS,
    ("event_math_function", "event math function"): GROUPLIST_OPENEHR_EVENT_MATH_FUNCTION,
    ("composition_category", "composition category"): GROUPLIST_OPENEHR_COMPOSITION_CATEGORY,
    ("setting", "setting"): GROUPLIST_OPENEHR_SETTING
})