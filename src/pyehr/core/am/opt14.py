from typing import Optional, Union

import warnings
import xml.etree.ElementTree as ET

import numpy as np

from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeConstraint, CArchetypeRoot, CAttribute, CComplexObject
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology, ArchetypeTerm, CodeDefinitionSet, ConstraintBindingSet, TermBindingItem, TermBindingSet
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, TemplateID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.resource import ResourceDescription
from pyehr.core.its.xml import IXMLSupport, get_pyehr_type_from_element
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.core.rm.data_types import DataValue
from pyehr.core.rm.data_types.text import CodePhrase

__all__ = ['FlatArchetypeOntology', 'Annotation', 'TComplexObject', 'TAttribute', 'TConstraint', 'TViewConstraint', 'TView', 'OperationalTemplate']


class FlatArchetypeOntology(ArchetypeOntology):
    archetype_id: str

    def __init__(self, 
                term_definitions: list[CodeDefinitionSet],
                archetype_id: str,
                constraint_definitions: Optional[list[CodeDefinitionSet]] = None,
                term_bindings: Optional[list['TermBindingSet']] = None,
                constraint_bindings: Optional[list[ConstraintBindingSet]] = None,
                parent_archetype = None,
                specialisation_depth: Optional[np.int32] = None,
                term_attribute_names: Optional[list[str]] = None,
                **kwargs):
        self.archetype_id = archetype_id
        super().__init__(term_definitions, constraint_definitions, term_bindings, constraint_bindings, parent_archetype, specialisation_depth, term_attribute_names, **kwargs)

    def from_xml(root: ET.Element, **kwargs):
        term_defs, constraint_defs, term_binds, constraint_binds = ArchetypeOntology.extract_xml_elements(root)

        arch_id = root.attrib["archetype_id"]

        return FlatArchetypeOntology(term_defs, arch_id, constraint_defs, term_binds, constraint_binds)

    def as_xml(self, root_tag=None):
        draft = super().as_xml(root_tag)

        draft.attrib["archetype_id"] = self.archetype_id

        return draft

    def as_json(self):
        draft = super().as_json()
        draft["archetype_id"] = self.archetype_id
        draft["_type"] = "FLAT_ARCHETYPE_ONTOLOGY"

class Annotation(AnyClass, IXMLSupport):
    pass

class TComplexObject(AnyClass, IXMLSupport):
    """Class to represent an object within a template constraint tree as defined in Template.xsd
    
    Actual instances seem not to sub-class C_COMPLEX_OBJECT as per the .xsd, so neither does this."""

    default_value: Optional[DataValue]

    def __init__(self,
        default_value: Optional[DataValue] = None,
        **kwargs):
        self.default_value = default_value
        super().__init__()

    def from_xml(root: ET.Element, **kwargs):
        # sup : CComplexObject = CComplexObject.from_xml(root)
        dv = root.find("./default_value")
        if dv is not None:
            from pyehr.types import OPENEHR_TYPE_MAP
            typ = get_pyehr_type_from_element(dv)
            cls = OPENEHR_TYPE_MAP.get(typ)
            if cls is not None:
                if not hasattr(cls, "from_xml"):
                    warnings.warn(f"Default value found when parsing XML but skipped as \'{typ}\' does not yet have XML support in pyehr")
                else:
                    dv = cls.from_xml(dv)

        return TComplexObject(dv)

    def as_xml(self, root_tag=None):
        draft = ET.Element(root_tag if root_tag is not None else "tcomplexobject")
        if self.default_value is not None:
            if not hasattr(self.default_value, "as_xml"):
                warnings.warn(f"Default value found when writing to XML but skipped as \'{str(type(self.default_value))}\' does not yet have XML support in pyehr")
            else:
                draft.append(self.default_value.as_xml())

        return draft

    def as_json(self):
        draft = dict()
        if self.default_value is not None:
            draft["default_value"] = self.default_value.as_json()
        draft["_type"] = "T_COMPLEX_OBJECT"
        return draft

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.default_value, other.default_value))

class TAttribute(AnyClass, IXMLSupport):
    """Class to represent an attribute within a template constraint tree as defined in Template.xsd"""

    rm_attribute_name: str

    children: Optional[list[TComplexObject]]

    differential_path: str

    def __init__(self, rm_attribute_name: str, differential_path: str, children: Optional[list[TComplexObject]] = None):
        self.rm_attribute_name = rm_attribute_name
        self.differential_path = differential_path
        self.children = children
        super().__init__()

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.rm_attribute_name, other.rm_attribute_name) and
                is_equal_value(self.differential_path, other.differential_path) and
                is_equal_value(self.children, other.children))

    def as_json(self):
        draft = dict()
        draft["rm_attribute_name"] = self.rm_attribute_name
        draft["differential_path"] = self.differential_path
        if self.children is not None:
            draft["children"] = [child.as_json() for child in self.children]
        draft["_type"] = "T_ATTRIBUTE"
        return draft

    def as_xml(self, root_tag=None):
        root = ET.Element("tattribute" if root_tag is None else root_tag)
        root.attrib["rm_attribute_name"] = self.rm_attribute_name
        root.attrib["differential_path"] = self.differential_path
        if self.children is not None:
            for child in self.children:
                root.append(child.as_xml("children"))

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        rm_attribute_name = root.findtext("./rm_attribute_name")
        differential_path = root.findtext("./differential_path")
        child_els = root.findall("./children")
        children = None
        if len(child_els) > 0:
            children = []
            for child_el in child_els:
                children.append(TComplexObject.from_xml(child_el))

        return TAttribute(rm_attribute_name, differential_path, children)


class TConstraint(AnyClass, IXMLSupport):
    """Class to represent a template constraint as defined in T_CONSTRAINT in Template.xsd"""

    attributes : Optional[list[TAttribute]]

    def __init__(self, attributes: Optional[list[TAttribute]] = None):
        self.attributes = attributes
        super().__init__()

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.attributes, other.attributes))

    def as_json(self):
        draft = dict()
        if self.attributes is not None:
            draft["attributes"] = [attr.as_json() for attr in self.attributes]
        draft["_type"] = "T_CONSTRAINT"
        return draft

    def as_xml(self, root_tag = None):
        root = ET.Element("tconstraint" if root_tag is None else root_tag)
        if self.attributes is not None:
            for attr in self.attributes:
                root.append(attr.as_xml("attributes"))

        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        attr_els = root.findall("./attributes")
        attrs = None
        if len(attr_els) > 0:
            attrs = []
            for attr_el in attr_els:
                attrs.append(TAttribute.from_xml(attr_el))

        return TConstraint(attrs)


class TViewConstraint(AnyClass, IXMLSupport):
    """Class to represent items within constraints in T_VIEW"""

    path: str

    items: dict[str, Union[bool, int, float, str]]
    """Map of id -> value"""

    def __init__(self, path: str, items: dict[str, Union[bool, int, float, str]]):
        self.path = path
        self.items = items
        super().__init__()

    def is_equal(self, other):
        return (type(self) == type(other) and 
                is_equal_value(self.path, other.path) and
                is_equal_value(self.items, other.items))
    
    def as_json(self):
        return {
            "path": self.path,
            "items": self.items,
            "_type": "T_VIEW_CONSTRAINT"
        }
    
    def as_xml(self, root_tag = None):
        root = ET.Element("tviewconstraint" if root_tag is None else root_tag)
        root.attrib["path"] = self.path
        for (id, value) in self.items.items():
            items_el = ET.Element("items")
            items_el.attrib["id"] = id
            val_el = ET.Element("value")
            if isinstance(value, bool):
                val_el.text = str(value).lower()
                val_el.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
                val_el.attrib["xmlns:xs"] = "http://www.w3.org/2001/XMLSchema"
                val_el.attrib["xsi:type"] = "xs:boolean"
            elif isinstance(value, str):
                val_el.text = value
                val_el.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
                val_el.attrib["xmlns:xs"] = "http://www.w3.org/2001/XMLSchema"
                val_el.attrib["xsi:type"] = "xs:string"
            elif isinstance(value, int):
                val_el.text = str(value)
                val_el.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
                val_el.attrib["xmlns:xs"] = "http://www.w3.org/2001/XMLSchema"
                val_el.attrib["xsi:type"] = "xs:integer"
            elif isinstance(value, float):
                val_el.text = str(value)
                val_el.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
                val_el.attrib["xmlns:xs"] = "http://www.w3.org/2001/XMLSchema"
                val_el.attrib["xsi:type"] = "xs:float"
            else:
                val_el.text = str(value)
            items_el.append(val_el)
            root.append(items_el)
        return root
    
    @staticmethod
    def from_xml(root: ET.Element, **kwargs):
        path = root.attrib["path"]

        items_els = root.findall("./items")
        items = dict()
        for item_el in items_els:
            id = item_el.attrib["id"]
            val_el = item_el.find("./value")
            txt = val_el.text
            typ = get_pyehr_type_from_element(val_el)
            if typ is None:
                if txt == "true" or txt == "false":
                    items[id] = (txt == "true")
                else:
                    items[id] = txt
            elif typ == "xs:boolean":
                items[id] = (txt == "true")
            elif typ == "xs:string":
                items[id] = txt
            elif typ == "xs:integer":
                items[id] = int(txt)
            elif typ == "xs:float":
                items[id] = float(txt)
            else:
                raise ValueError(f"Could not parse T_VIEW constraint item with value of type \'{typ}\' as it was not supported.")
        
        return TViewConstraint(path, items)
            

class TView(AnyClass, IXMLSupport):
    """T_VIEW as defined in Template.xsd"""

    constraints = Optional[list[TViewConstraint]]

    def __init__(self, constraints: Optional[list[TViewConstraint]] = None):
        self.constraints = constraints
        super().__init__()

    def is_equal(self, other):
        return (type(self) == type(other) and
                is_equal_value(self.constraints, other.constraints))
    
    def as_json(self):
        draft = dict()
        if self.constraints is not None:
            draft["constraints"] = [constraint.as_json() for constraint in self.constraints]
        draft["_type"] = "T_VIEW"
        return draft
    
    def as_xml(self, root_tag = None):
        root = ET.Element("T_VIEW" if root_tag is None else root_tag)
        if self.constraints is not None:
            for constraint in self.constraints:
                root.append(constraint.as_xml("constraints"))
        return root
    
    @staticmethod
    def from_xml(root, **kwargs):
        cons_els = root.findall("./constraints")
        cons = None
        if len(cons_els) > 0:
            cons = []
            for con_el in cons_els:
                cons.append(TViewConstraint.from_xml(con_el))
        return TView(cons)


class OperationalTemplate(AnyClass, IXMLSupport):
    """pyehr representation of the OPT 1.4 XML template represented in XML
    schemas in Template.xsd"""

    language: CodePhrase

    is_controlled: Optional[bool]

    description: Optional[ResourceDescription]

    revision_history: Optional[RevisionHistory]

    uid: Optional[HierObjectID]

    template_id: TemplateID

    concept: str

    definition : Optional[CArchetypeRoot] = None

    ontology : Optional[FlatArchetypeOntology] = None

    component_ontologies : Optional[list[FlatArchetypeOntology]] = None

    annotations : Optional[list[Annotation]] = None

    constraints : Optional[TConstraint] = None

    view : Optional[TView] = None

    def __init__(self, 
                 language:CodePhrase, 
                 template_id: TemplateID, 
                 concept: str, 
                 is_controlled: Optional[bool] = None, 
                 description: Optional[ResourceDescription] = None, 
                 revision_history: Optional[RevisionHistory] = None, 
                 uid: Optional[HierObjectID] = None,
                 definition: Optional[CArchetypeRoot] = None,
                 ontology: Optional[FlatArchetypeOntology] = None,
                 component_ontologies: Optional[FlatArchetypeOntology] = None,
                 annotations: Optional[list[Annotation]] = None,
                 constraints: Optional[TConstraint] = None,
                 view: Optional[TView] = None
                 ):
        self.language = language
        self.template_id = template_id
        self.concept = concept
        self.is_controlled = is_controlled
        self.description = description
        self.revision_history = revision_history
        self.uid = uid
        self.definition = definition
        self.ontology = ontology
        self.component_ontologies = component_ontologies
        self.annotations = annotations
        self.constraints = constraints
        self.view = view

    def as_xml(self, root_tag = None):
        tag = "template" if root_tag is None else root_tag
        root = ET.Element(tag)
        root.append(self.language.as_xml("language"))

        if self.is_controlled is not None:
            is_cont = ET.Element("is_controlled")
            is_cont.text = str(self.is_controlled).lower()
            root.append(is_cont)

        if self.description is not None:
            root.append(self.description.as_xml("description"))

        if self.revision_history is not None:
            root.append(self.revision_history.as_xml("revision_history"))

        if self.uid is not None:
            root.append(self.uid.as_xml("uid"))
        
        root.append(self.template_id.as_xml("template_id"))
        
        conc = ET.Element("concept")
        conc.text = self.concept
        root.append(conc)
        
        if self.definition is not None:
            root.append(self.definition.as_xml("definition"))

        if self.ontology is not None:
            root.append(self.ontology.as_xml("ontology"))

        if self.component_ontologies is not None:
            for comp_onto in self.component_ontologies:
                root.append(comp_onto.as_xml("component_ontologies"))

        # annotations
        
        if self.constraints is not None:
            root.append(self.constraints.as_xml("constraints"))

        if self.view is not None:
            root.append(self.view.as_xml("view"))
        return root

    @staticmethod
    def from_xml(root: ET.Element, **kwargs) -> 'OperationalTemplate':
        lang = CodePhrase.from_xml(root.find("./language"))

        is_cont_str = root.findtext("./is_controlled")
        is_cont = None if is_cont_str is None else (is_cont_str == "true")

        desc = root.find("./description")
        if desc is not None:
            desc = ResourceDescription.from_xml(desc)

        rh = root.find("./revision_history")
        rh = RevisionHistory.from_xml(rh) if rh is not None else None

        uid = root.find("./uid")
        if uid is not None:
            uid = HierObjectID.from_xml(uid)
        tid = TemplateID.from_xml(root.find("./template_id"))
        concept = root.findtext("./concept")
        definition = CArchetypeRoot.from_xml(root.find("./definition"))

        onto = root.find("./ontology")
        comp_onto_els = root.findall("./component_ontologies")

        onto = FlatArchetypeOntology.from_xml(onto) if onto is not None else None
        comp_onto = None
        if len(comp_onto_els) > 0:
            comp_onto = []
            for comp_onto_el in comp_onto_els:
                comp_onto.append(FlatArchetypeOntology.from_xml(comp_onto_el))

        cons = root.find("./constraints")
        if cons is not None:
            cons = TConstraint.from_xml(cons)

        anno = root.find("./annotations")
        if anno is not None:
            warnings.warn("OPERATIONAL_TEMPLATE parsing does not support parsing top-level element annotations so this will be skipped.")

        view = root.find("./view")
        view = TView.from_xml(view) if view is not None else None
        
        return OperationalTemplate(lang, tid, concept, is_controlled=is_cont, description=desc, uid=uid, definition=definition, view=view, ontology=onto, constraints=cons)

    def as_json(self):
        draft = {
            "language": self.language.as_json(),
            "template_id": self.template_id.as_json(),
            "concept": self.concept
        }
        if self.is_controlled is not None:
            draft["is_controlled"] = self.is_controlled
        if self.description is not None:
            draft["description"] = self.description.as_json()
        if self.revision_history is not None:
            draft["revision_history"] = self.revision_history.as_json()
        if self.uid is not None:
            draft["uid"] = self.uid.as_json()
        if self.definition is not None:
            draft["definition"] = self.definition.as_json()
        if self.ontology is not None:
            draft["ontology"] = self.ontology.as_json()
        if self.component_ontologies is not None:
            draft["component_ontologies"] = [comp_onto.as_json() for comp_onto in self.component_ontologies]
        if self.annotations is not None:
            draft["annotations"] = [annotation.as_json() for annotation in self.annotations]
        if self.constraints is not None:
            draft["constraints"] = self.constraints.as_json() 
        if self.view is not None:
            draft["view"] = self.view.as_json()
        draft["_type"] = "TEMPLATE"
        return draft

    def is_equal(self, other: 'OperationalTemplate'):
        return (type(self) == type(other) and
                is_equal_value(self.language, other.language) and
                is_equal_value(self.is_controlled, other.is_controlled) and
                is_equal_value(self.description, other.description) and
                is_equal_value(self.revision_history, other.revision_history) and
                is_equal_value(self.uid, other.uid) and
                is_equal_value(self.template_id, other.template_id) and
                is_equal_value(self.concept, other.concept) and
                is_equal_value(self.definition, other.definition) and
                is_equal_value(self.ontology, other.ontology) and
                is_equal_value(self.component_ontologies, other.component_ontologies) and
                is_equal_value(self.annotations, other.annotations) and
                is_equal_value(self.constraints, other.constraints) and
                is_equal_value(self.view, other.view))
