import csv

from org.openehr.rm.support.terminology import TerminologyService, ICodeSetAccess, ITerminologyAccess
from org.openehr.rm.data_types.text import CodePhrase
from org.openehr.base.base_types.identification import TerminologyID

class _CSVTerminologyAccess(ITerminologyAccess):

    _terminology_id : TerminologyID
    _language: str
    _all_codes: dict[str, CodePhrase]
    _all_groups: dict[str, list[CodePhrase]]

    def _import_csv_file(self, csv_path: str):
        self._all_codes = dict()
        self._all_groups = dict()
        with open(csv_path, 'r') as csv_file:
            code_reader = csv.reader(csv_file, dialect='excel')
            for row in code_reader:
                # code_string, preferred_term, group
                code = CodePhrase(self._terminology_id, row[0], row[1])
                self._all_codes[row[0]] = code
                if row[2] in self._all_groups:
                    self._all_groups[row[2]].append(code)
                else:
                    self._all_groups[row[2]] = [code]

    def __init__(self, terminology_id: TerminologyID, csv_path: str, language: str):
        self._terminology_id = terminology_id
        self._language = language
        self._import_csv_file(csv_path)
        super().__init__()

    def id(self):
        return self._terminology_id.value
    
    def all_codes(self):
        return list(self._all_codes.values())
    
    def codes_for_group_id(self, a_group_id: str) -> list[CodePhrase]:
        if a_group_id in self._all_groups:
            return self._all_groups[a_group_id]
        else:
            return []
    
    def codes_for_group_name(self, a_group_id, a_lang, a_name) -> list[CodePhrase]:
        if a_group_id in self._all_groups and self._language == a_lang:
            matches = []
            for potential_match in self.codes_for_group_id(a_group_id):
                if potential_match.preferred_term == a_name:
                    matches.append(potential_match)
        else:
            return []
        
    def has_code_for_group_id(self, a_code, group_id):
        for potential_match in self.codes_for_group_id(group_id):
            if potential_match.code_string == a_code:
                return True
        return False
    
    def rubric_for_code(self, code, lang):
        if lang != self._language:
            raise ValueError(f"This terminology does not support language '{lang}'. It only supports '{self._language}'")
        elif code not in self._all_codes:
            raise ValueError(f"Could not find code '{code}' in the terminology")
        else:
            return self._all_codes[code].preferred_term


class CSVTerminologyService(TerminologyService):
    """Defines a basic terminology service which imports a single code set from a CSV file
    and provides it as an OpenEHR compliant TerminologyService. Does not provide ITerminologyAccess"""

    _terminology_id : TerminologyID
    
    _terminology_access: _CSVTerminologyAccess

    def __init__(self, terminology_id: str, csv_path: str, language: str):
        self._terminology_id = TerminologyID(terminology_id)
        self._terminology_access = _CSVTerminologyAccess(self._terminology_id, csv_path, language)
        super().__init__()

    def terminology(self, name) -> ITerminologyAccess:
        if name == self._terminology_id.value:
            return self._terminology_access
        else:
            raise ValueError(f"This service only implements '{self._terminology_id.value}' as a single terminology. No others are supported.")
        
    def code_set(self, name: str) -> ICodeSetAccess:
        raise NotImplementedError(f"No code sets are supported by this service")
    
    def code_set_for_id(self, name):
        raise NotImplementedError("No OpenEHR internal code sets are supported by this service")
    
    def has_terminology(self, name):
        return (name == self._terminology_id.value)
    
    def has_code_set(self, name):
        return False
    
    def terminology_identifiers(self):
        return [self._terminology_id.value]
    
    def openehr_code_sets(self):
        return {}
    
    def code_set_identifiers(self):
        return []
        

    