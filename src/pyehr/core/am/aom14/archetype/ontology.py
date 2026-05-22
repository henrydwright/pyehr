from typing import Optional
import xml.etree.ElementTree as ET

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.primitive_types import Uri
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.xml import IXMLSupport
from pyehr.core.rm.data_types.text import CodePhrase

import numpy as np

class ConstraintBindingItem(AnyClass, IXMLSupport):
    """CONSTRAINT_BINDING_ITEM as defined in Archetype.xsd"""

    value: Uri

    code: str

    def __init__(self, value: Uri, code: str, **kwargs):
        self.value = value
        self.code = code
        super().__init__(**kwargs)

    def as_json(self):
        return {
            "value": str(self.value),
            "code": self.code,
            "_type": "CONSTRAINT_BINDING_ITEM"
        }

    def as_xml(self, root_tag=None):
        tag = "constraint_binding_item" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["code"] = self.code
        value_el = ET.Element("value")
        value_el.text = str(self.value)
        root.append(value_el)
        return root

    def from_xml(root: ET.Element, **kwargs):
        code = root.attrib["code"]
        value_el = root.find("value")
        if value_el is None or value_el.text is None:
            raise ValueError("ConstraintBindingItem XML missing value text")
        return ConstraintBindingItem(Uri(value_el.text), code)

class ConstraintBindingSet(AnyClass, IXMLSupport):
    """ConstraintBindingSet as defined in Archetype.xsd"""

    terminology: str

    _code_item_map: Optional[dict[str, ConstraintBindingItem]] = None
    """Mapping from a given code to the ConstraintBindingItem for that code"""

    def _get_items(self):
        if self._code_item_map is None:
            return None
        else:
            return list(self._code_item_map.values())

    items = property(fget=_get_items)
    """List of all CONSTRAINT_BINDING_ITEMs for this terminology"""

    def __init__(self, terminology: str, items: Optional[list[ConstraintBindingItem]] = None, **kwargs):
        self.terminology = terminology
        if items is not None:
            self._code_item_map = dict()
            for item in items:
                self._code_item_map[item.code] = item
        super().__init__(**kwargs)

    def item(self, a_code: str) -> Optional[ConstraintBindingItem]:
        """Returns the CONSTRAINT_BINDING_ITEM for a given code, or None if it doesn't exist"""
        if self._code_item_map is None:
            return None
        return self._code_item_map.get(a_code)

    def as_json(self):
        draft = {
            "terminology": self.terminology
        }
        if self.items is not None:
            draft["items"] = [item.as_json() for item in self.items]
        draft["_type"] = "CONSTRAINT_BINDING_SET"
        return draft

    def as_xml(self, root_tag=None):
        tag = "constraint_binding_set" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["terminology"] = self.terminology
        if self.items is not None:
            for item in self.items:
                root.append(item.as_xml("items"))
        return root

    def from_xml(root: ET.Element, **kwargs):
        terminology = root.attrib["terminology"]
        items = None
        item_els = root.findall("./items")
        if len(item_els) > 0:
            items = [ConstraintBindingItem.from_xml(item_el) for item_el in item_els]
        return ConstraintBindingSet(terminology, items)

class CodeDefinitionSet(AnyClass, IXMLSupport):
    """CodeDefinitionSet as defined in Archetype.xsd"""

    language: str

    _code_item_map: Optional[dict[str, 'ArchetypeTerm']] = None
    """Mapping from a given code to the ARCHETYPE_TERM for that code"""

    def _get_items(self):
        if self._code_item_map is None:
            return None
        else:
            return list(self._code_item_map.values())

    items = property(fget=_get_items)
    """List of all ARCHETYPE_TERMs for this language"""

    def __init__(self, language : str, items : Optional[list['ArchetypeTerm']], **kwargs):
        self.language = language
        if items is not None:
            self._code_item_map = dict()
            for arch_term in items:
                self._code_item_map[arch_term.code] = arch_term
        super().__init__(**kwargs)

    def item(self, a_code:str) -> Optional['ArchetypeTerm']:
        """Returns the ARCHETYPE_TERM for a given code, or None if it doesn't exist"""
        return self._code_item_map.get(a_code)

    def as_json(self):
        draft = {
            "language": self.language
        }
        if self.items is not None:
            draft["items"] = [item.as_json() for item in self.items]
        draft["_type"] = "CODE_DEFINITION_SET"
        return draft

    def as_xml(self, root_tag=None):
        tag = "code_definition_set" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["language"] = self.language
        if self.items is not None:
            for item in self.items:
                root.append(item.as_xml("items"))
        return root

    def from_xml(root: ET.Element, **kwargs):
        language = root.attrib["language"]
        items = None
        item_els = root.findall("./items")
        if len(item_els) > 0:
            items = [ArchetypeTerm.from_xml(item_el) for item_el in item_els]
        return CodeDefinitionSet(language, items)

    def is_equal(self, other: 'CodeDefinitionSet'):
        return (type(self) == type(other)
                and is_equal_value(self.language, other.language)
                and is_equal_value(self._code_item_map, other._code_item_map))

class ArchetypeOntology(AnyClass, IXMLSupport):
    """Local ontology of an archetype."""

    _term_def_dict: dict[str, CodeDefinitionSet]
    """Mapping of language to the term definitions for that language"""

    def _get_term_definitions(self):
        return list(self._term_def_dict.values())

    term_definitions = property(fget=_get_term_definitions)
    """List of sets of code definitions in different languages"""

    _constraint_def_dict: Optional[dict[str, CodeDefinitionSet]] = None
    """Mapping of language to the constraint definitions for that language"""

    def _get_constraint_definitions(self):
        if self._constraint_def_dict is None:
            return None
        else:
            return list(self._constraint_def_dict.values())

    constraint_definitions = property(fget=_get_constraint_definitions)
    """List of sets of terminology constraints in different languages"""

    _term_bind_dict: Optional[dict[str, 'TermBindingSet']] = None
    """Mapping of terminology (str) to term bindings for that terminology"""

    def _get_term_bindings(self):
        if self._term_bind_dict is None:
            return None
        else:
            return list(self._term_bind_dict.values())

    term_bindings = property(fget=_get_term_bindings)
    """List of sets of terminology bindings"""

    _constraint_bind_dict: Optional[dict[str, ConstraintBindingSet]] = None
    """Mapping of terminology (str) to constraint bindings for that terminology"""

    def _get_constraint_bindings(self):
        if self._constraint_bind_dict is None:
            return None
        else:
            return list(self._constraint_bind_dict.values())

    constraint_bindings = property(fget=_get_constraint_bindings)
    """List of sets of constraint bindings"""

    term_codes: list[str]
    """List of all term codes in the ontology. Most of these correspond to “at” 
    codes in an ADL archetype, which are the node_ids on C_OBJECT descendants. 
    There may be an extra one, if a different term is used as the overall 
    archetype concept from that used as the node_id of the outermost C_OBJECT 
    in the definition part."""

    constraint_codes: list[str]
    """List of all term codes in the ontology. These correspond to the “ac” codes
      in an ADL archetype, or equivalently, the CONSTRAINT_REF.reference values 
      in the archetype definition."""
    
    parent_archetype = None
    """Archetype which owns this terminology."""
    # this should be mandatory as per the spec, but makes decoding hard so made optional
    #  for now.

    terminologies_available: Optional[list[str]]
    """List of terminologies to which term or constraint bindings exist in this 
    terminology."""

    languages_available: set[str]
    """[Not in OpenEHR spec] List of languages in which term or constraint definitions are exist in this terminology"""

    specialisation_depth: Optional[np.int32]
    """Specialisation depth of this archetype. Unspecialised archetypes have depth
      0, with each additional level of specialisation adding 1 to the 
      specialisation_depth."""
    # this should be mandatory as per the spec, but makes decoding hard so made optional
    #  for now.
    
    term_attribute_names: Optional[list[str]]
    # This has no explaining in the spec, and doesn't feature in the XML spec so making it
    #  optional as no idea what it does.

    
    def __init__(self, 
                 term_definitions: list[CodeDefinitionSet],
                 constraint_definitions: Optional[list[CodeDefinitionSet]] = None,
                 term_bindings: Optional[list['TermBindingSet']] = None,
                 constraint_bindings: Optional[list[ConstraintBindingSet]] = None,
                 parent_archetype = None,
                 specialisation_depth: Optional[np.int32] = None,
                 term_attribute_names: Optional[list[str]] = None,
                 **kwargs):
        self.parent_archetype = parent_archetype
        self.specialisation_depth = specialisation_depth
        self.term_attribute_names = term_attribute_names

        terminologies_available = set()
        languages_available = set()

        # create term_codes and load term_definitions and term_bindings into
        #  their respective dicts
        term_codes = set()

        self._term_def_dict = dict()
        for term_def in term_definitions:
            self._term_def_dict[term_def.language] = term_def
            languages_available.add(term_def.language)
            for term_def_item in term_def.items:
                term_codes.add(term_def_item.code)

        if term_bindings is not None:
            self._term_bind_dict = dict()
            for term_bind in term_bindings:
                self._term_bind_dict[term_bind.terminology] = term_bind
                for term_bind_item in term_bind.items:
                    term_codes.add(term_bind_item.code)
                    terminologies_available.add(term_bind_item.value.terminology_id.value)

        self.term_codes = list(term_codes)

        # create constraint_codes and load constraint_definitions and constraint_bindings
        #  into their respective dicts
        constraint_codes = set()
        if constraint_definitions is not None:
            self._constraint_def_dict = dict()
            for constraint_def in constraint_definitions:
                self._constraint_def_dict[constraint_def.language] = constraint_def
                languages_available.add(constraint_def.language)
                for constraint_def_item in constraint_def.items:
                    constraint_codes.add(constraint_def_item.code)

        if constraint_bindings is not None:
            self._constraint_bind_dict = dict()
            for constraint_bind in constraint_bindings:
                self._constraint_bind_dict[constraint_bind.terminology] = constraint_bind
                terminologies_available.add(constraint_bind.terminology)
                for constraint_bind_item in constraint_bind.items:
                    constraint_codes.add(constraint_bind_item.code)

        self.constraint_codes = list(constraint_codes)

        self.terminologies_available = list(terminologies_available)
        self.languages_available = languages_available

        super().__init__(**kwargs)

    def has_language(self, a_lang:str) -> bool:
        """True if language 'a_lang' is present in archetype ontology."""
        # TODO: report typo in spec where has_terminology documentation is copied for has_language
        return a_lang in self.languages_available

    def has_terminology(self, a_terminology_id: str) -> bool:
        """True if terminology 'a_terminology' is present in archetype ontology."""
        if self.terminologies_available is None:
            return False
        else:
            return a_terminology_id in self.terminologies_available

    def has_term_code(self, a_code: str) -> bool:
        """True if term_codes has a_code."""
        return a_code in self.term_codes

    def has_constraint_code(self, a_code: str) -> bool:
        """True if constraint_codes has a_code."""
        return a_code in self.constraint_codes

    def term_definition(self, a_code: str, a_lang: str) -> 'ArchetypeTerm':
        """Term definition for a code, in a specified language."""
        if a_lang not in self._term_def_dict:
            raise ValueError(f"Term definitions for language \'{a_lang}\' do not exist in this ontology")
        
        term_defs = self._term_def_dict[a_lang]
        term = term_defs.item(a_code)

        if term is None:
            raise ValueError(f"Code \'{a_code}\' was not present in the term definitions for \'{a_lang}\'")
        
        return term

    def constraint_definition(self, a_code: str, a_lang: str) -> 'ArchetypeTerm':
        """Constraint definition for a code, in a specified language."""
        if self._constraint_def_dict is None:
            raise ValueError("No constraint definitions exist in this ontology")
        
        if a_lang not in self._constraint_def_dict:
            raise ValueError(f"Constraint definitions for language \'{a_lang}\' do not exist in this ontology")
        
        constraint_defs = self._constraint_def_dict[a_lang]
        constraint = constraint_defs.item(a_code)

        if constraint is None:
            raise ValueError(f"Code \'{a_code}\' was not present in the constraint definitions for \'{a_lang}\'")
        
        return constraint



    def term_binding(self, a_terminology: str, a_code: str) -> 'TermBindingItem':
        """Binding of term corresponding to a_code in target external 
        terminology a_terminology, as a TermBindingItem."""
        if self._term_bind_dict is None:
            raise ValueError("No term bindings exist in this ontology")
        
        if a_terminology not in self._term_bind_dict:
            raise ValueError(f"Term bindings for terminology '{a_terminology}' do not exist in this ontology")
        
        term_binds = self._term_bind_dict[a_terminology]
        term_bind = term_binds.item(a_code)

        if term_bind is None:
            raise ValueError(f"Code '{a_code}' was not present in the term bindings for '{a_terminology}'")
        
        return term_bind

    def constraint_binding(self, a_terminology_id: str, a_code: str) -> 'ConstraintBindingItem':
        """Binding of constraint corresponding to a_code in target external 
        terminology a_terminology_id, as a ConstraintBindingItem."""
        if self._constraint_bind_dict is None:
            raise ValueError("No constraint bindings exist in this ontology")
        
        if a_terminology_id not in self._constraint_bind_dict:
            raise ValueError(f"Constraint bindings for terminology '{a_terminology_id}' do not exist in this ontology")
        
        constraint_binds = self._constraint_bind_dict[a_terminology_id]
        constraint_bind = constraint_binds.item(a_code)

        if constraint_bind is None:
            raise ValueError(f"Code '{a_code}' was not present in the constraint bindings for '{a_terminology_id}'")
        
        return constraint_bind

    def from_xml(root: ET.ElementTree, **kwargs):
        tds_els = root.findall("./term_definitions")
        term_defs = []
        for tds_el in tds_els:
            term_defs.append(CodeDefinitionSet.from_xml(tds_el))
        
        constraint_defs = None
        cds_els = root.findall("./constraint_definitions")
        if len(cds_els) > 0:
            constraint_defs = []
            for cds_el in cds_els:
                constraint_defs.append(CodeDefinitionSet.from_xml(cds_el))

        term_binds = None
        tbs_els = root.findall("./term_bindings")
        if len(tbs_els) > 0:
            term_binds = []
            for tbs_el in tbs_els:
                term_binds.append(TermBindingSet.from_xml(tbs_el))
        
        constraint_binds = None
        cbs_els = root.findall("./constraint_bindings")
        if len(cbs_els) > 0:
            constraint_binds = []
            for cbs_el in cbs_els:
                constraint_binds.append(ConstraintBindingSet.from_xml(cbs_el))

        return ArchetypeOntology(term_defs, constraint_defs, term_binds, constraint_binds)

    def as_json(self):
        draft = {
            "term_definitions": [td.as_json() for td in self.term_definitions]
        }
        if self.constraint_definitions is not None:
            draft["constraint_definitions"] = [cd.as_json() for cd in self.constraint_definitions]
        if self.term_bindings is not None:
            draft["term_bindings"] = [tb.as_json() for tb in self.term_bindings]
        if self.constraint_bindings is not None:
            draft["constraint_bindings"] = [cb.as_json() for cb in self.constraint_bindings]
        draft["_type"] = "ARCHETYPE_ONTOLOGY"
        return draft

    def as_xml(self, root_tag=None):
        tag = "archetype_ontology" if root_tag is None else root_tag
        root = ET.Element(tag)
        for td in self.term_definitions:
            root.append(td.as_xml("term_definitions"))
        if self.constraint_definitions is not None:
            for cd in self.constraint_definitions:
                root.append(cd.as_xml("constraint_definitions"))
        if self.term_bindings is not None:
            for tb in self.term_bindings:
                root.append(tb.as_xml("term_bindings"))
        if self.constraint_bindings is not None:
            for cb in self.constraint_bindings:
                root.append(cb.as_xml("constraint_bindings"))
        return root
    
    def is_equal(self, other: 'ArchetypeOntology'):
        return (type(self) == type(other) and
                is_equal_value(self._term_def_dict, other._term_def_dict) and
                is_equal_value(self._constraint_def_dict, other._constraint_def_dict) and
                is_equal_value(self._term_bind_dict, other._term_bind_dict) and
                is_equal_value(self._constraint_bind_dict, other._constraint_bind_dict) and
                is_equal_value(self.parent_archetype, other.parent_archetype) and
                is_equal_value(self.specialisation_depth, other.specialisation_depth) and
                is_equal_value(self.term_attribute_names, other.term_attribute_names))

class ArchetypeTerm(AnyClass, IXMLSupport):
    """Representation of any coded entity (term or constraint) in the archetype 
    ontology."""

    code: str
    """Code of this term."""

    items: Optional[dict[str, str]]
    """Hash of keys (“text”, “description” etc) and corresponding values. Hash of 
    keys ("text", "description" etc) and corresponding values."""

    def __init__(self, code: str, items: Optional[dict[str, str]] = None, **kwargs):
        if code == "":
            raise ValueError("code cannot be an empty string (invariant: code_valid)")
        self.code = code
        self.items = items
        super().__init__(**kwargs)

    def as_json(self):
        draft = {
            "code": self.code
        }
        if self.items is not None:
            draft["items"] = self.items
        draft["_type"] = "ARCHETYPE_TERM"
        return draft
                
    def as_xml(self, root_tag = None):
        tag = "archetype_term" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["code"] = self.code
        if self.items is not None:
            for (key, val) in self.items.items():
                item = ET.Element("items")
                item.attrib["id"] = key
                item.text = val
                root.append(item)
        return root
    
    def from_xml(root: ET.Element, **kwargs) -> 'ArchetypeTerm':
        cod = root.attrib["code"]
        it_dict = None
        items = root.findall("./items")
        if len(items) > 0:
            it_dict = dict()
            for it_el in items:
                it_dict[it_el.attrib["id"]] = it_el.text
        
        return ArchetypeTerm(cod, it_dict)
        
    def is_equal(self, other: 'ArchetypeTerm'):
        return (type(self) == type(other) and
                is_equal_value(self.code, other.code) and
                is_equal_value(self.items, other.items))
    
    def keys(self) -> Optional[list[str]]:
        """List of all keys used in this term."""
        if self.items is None:
            return None
        else:
            return list(self.items.keys())

class TermBindingItem(AnyClass, IXMLSupport):
    """TermBindingItem as defined Archetype.xsd"""

    code: str

    value: CodePhrase

    def __init__(self, code: str, value: CodePhrase, **kwargs):
        self.code = code
        self.value = value
        super().__init__(**kwargs)

    def is_equal(self, other: 'TermBindingItem'):
        return (type(self) == type(other) and
                self.code == other.code and
                is_equal_value(self.value, other.value))
    
    def as_json(self):
        return {
            "code": self.code,
            "value": self.value.as_json(),
            "_type": "TERM_BINDING_ITEM"
        }
    
    def as_xml(self, root_tag = None):
        tag = "term_binding_item" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["code"] = self.code
        root.append(self.value.as_xml("value"))
        return root
    
    def from_xml(root: ET.Element, **kwargs):
        code = root.attrib["code"]
        val = CodePhrase.from_xml(root.find("value"))
        return TermBindingItem(code, val)

class TermBindingSet(AnyClass, IXMLSupport):
    """TermBindingSet as defined Archetype.xsd"""
    
    terminology: str

    _code_item_map: Optional[dict[str, 'TermBindingItem']] = None
    """Mapping from a given code to the TERM_BINDING_ITEM for that code"""

    def _get_items(self):
        if self._code_item_map is None:
            return None
        else:
            return list(self._code_item_map.values())

    items = property(fget=_get_items)
    """List of all TERM_BINDING_ITEMs for this terminology"""

    def __init__(self, terminology: str, items: Optional[list[TermBindingItem]] = None, **kwargs):
        self.terminology = terminology
        if items is not None:
            self._code_item_map = dict()
            for term_item in items:
                self._code_item_map[term_item.code] = term_item
        super().__init__(**kwargs)

    def item(self, a_code: str) -> Optional['TermBindingItem']:
        """Returns the TERM_BINDING_ITEM for a given code, or None if it doesn't exist"""
        if self._code_item_map is None:
            return None
        return self._code_item_map.get(a_code)

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.items, other.items) and
                is_equal_value(self.terminology, other.terminology))

    def as_json(self):
        draft = {
            "terminology": self.terminology
        }
        if self.items is not None:
            draft["items"] = [item.as_json() for item in self.items]
        draft["_type"] = "TermBindingSet"
        return draft
    
    def as_xml(self, root_tag = None):
        tag = "termbindingset" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.attrib["terminology"] = self.terminology
        if self.items is not None:
            for item in self.items:
                root.append(item.as_xml("items"))
        return root
    
    def from_xml(root: ET.Element, **kwargs):
        termi = root.attrib["terminology"]
        tbi_els = root.findall("./items")
        tbis = []
        for tbi_el in tbi_els:
            tbis.append(TermBindingItem.from_xml(tbi_el))
        return TermBindingSet(termi, tbis)