from typing import Optional, Union

import warnings
import xml.etree.ElementTree as ET

import numpy as np

from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeConstraint, CArchetypeRoot, CAttribute, CComplexObject
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology, ArchetypeTerm, TermBindingItem, TermBindingSet
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, TemplateID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Interval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.resource import ResourceDescription
from pyehr.core.its.xml import IXMLSupport, get_pyehr_type_from_element
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.core.rm.data_types.text import CodePhrase

class FlatArchetypeOntology(ArchetypeOntology):
    pass

class Annotation(AnyClass, IXMLSupport):
    pass

class TComplexObject(CComplexObject):
    pass

class TAttribute(AnyClass, IXMLSupport):
    pass

class TConstraint(AnyClass, IXMLSupport):
    pass

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
            "items": self.items
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

    component_ontologies : Optional[FlatArchetypeOntology] = None

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
        
        root.append(self.definition.as_xml("definition"))

        # ontology
        # component_ontologies
        # annotations
        # constraints

        root.append(self.view.as_xml("view"))
        return root
    
    def from_xml(root: ET.Element, **kwargs) -> 'OperationalTemplate':
        lang = CodePhrase.from_xml(root.find("./language"))
        is_cont = (root.findtext("./is_controlled") == "true")
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
        comp_onto = root.find("./component_ontologies")
        anno = root.find("./annotations")
        cons = root.find("./constraints")
        if onto is not None or comp_onto is not None or anno is not None or cons is not None:
            warnings.warn("OPERATIONAL_TEMPLATE parsing does not support parsing top-level elements ontology, component_ontologies, annotations or constraints so these will be skipped.")
        # TODO : ontology
        # TODO : component_ontologies

        # TODO : annotation

        # TODO : constraints
        view = root.find("./view")
        view = TView.from_xml(view) if view is not None else None
        
        return OperationalTemplate(lang, tid, concept, is_controlled=is_cont, description=desc, uid=uid, definition=definition, view=view)
    
    def as_json(self):
        draft = {
            "language": self.language.as_json(),
            "is_controlled": self.is_controlled,
            "template_id": self.template_id.as_json(),
            "concept": self.concept
        }
        if self.revision_history is not None:
            draft["revision_history"] = self.revision_history.as_json()
        if self.definition is not None:
            draft["definition"] = self.definition.as_json()
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
