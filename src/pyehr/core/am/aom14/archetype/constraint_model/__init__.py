from abc import abstractmethod
from typing import Optional
import warnings
import xml.etree.ElementTree as ET

import numpy as np

from pyehr.core.am.aom14.archetype.assertion import Assertion
from pyehr.core.am.aom14.archetype.constraint_model.primitive import CPrimitive
from pyehr.core.am.aom14.archetype.ontology import ArchetypeTerm, TermBindingSet
from pyehr.core.base.base_types.identification import ArchetypeID, TemplateID, TerminologyID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Cardinality, Interval
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.json_path_utils import json_has_path
from pyehr.core.its.xml import IXMLSupport, get_pyehr_type_from_element
from pyehr.core.rm.data_types.quantity import DVQuantity
from pyehr.core.rm.data_types.text import CodePhrase

# TODO: implement tests for member methods

class ArchetypeConstraint(AnyClass, IXMLSupport):
    """Archetype equivalent to LOCATABLE class in openEHR Common reference model. 
    Defines common constraints for any inheritor of LOCATABLE in any reference 
    model."""

    _parent: Optional['ArchetypeConstraint']
    """Parent ARCHETYPE_CONSTRAINT object of this ARCHETYPE_CONSTRAINT or None if root-level"""

    _parent_container_attribute_name: Optional[str]
    """The attribute within which this ARCHETYPE_CONSTRAINT is stored in its parent (e.g. 'children' for a child of C_ATTRIBUTE)"""

    _list_index: Optional[int]
    """The index of this item within a parent list, if it is in one"""

    @abstractmethod
    def __init__(self,
                 parent: Optional['ArchetypeConstraint'] = None,
                 parent_container_attribute_name: Optional[str] = None,
                 list_index: Optional[int] = None,
                 **kwargs):
        # n.b this logic is implemented in the same way as in PATHABLE so try
        #      to remember to copy any code changes from there, into here...
        self._parent = parent
        self._parent_container_attribute_name = parent_container_attribute_name
        self._list_index = list_index
        super().__init__(**kwargs)

    @abstractmethod
    def is_subset_of(self, other: 'ArchetypeConstraint') -> bool:
        """True if constraints represented by this node, ignoring any sub-parts, 
        are narrower or the same as other. Typically used during validation of 
        special-ised archetype nodes."""
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    def path(self) -> str:
        """Path of this node relative to root of archetype."""
        if self._parent is None:
            return "/definition"
        else:
            parent_path = self._parent.path()
            plural = self._list_index is not None
            pred = f"[{self._list_index}]" if plural else ""
            if parent_path == "/":
                return parent_path + f"{self._parent_container_attribute_name}{pred}"
            else:
                return parent_path + f"/{self._parent_container_attribute_name}{pred}"

    def has_path(self, a_path: str) -> bool:
        """True if the relative path `a_path` exists at this node."""
        return json_has_path(self.as_json(), a_path)
    
class CObject(ArchetypeConstraint):
    """Abstract model of constraint on any kind of object node."""
    
    rm_type_name: str
    """Reference model type that this node corresponds to."""

    occurrences: Interval[np.int32]
    """Occurrences of this object node in the data, under the owning attribute. 
    Upper limit can only be greater than 1 if owning attribute has a cardinality 
    of more than 1)."""

    node_id: str
    """Semantic identifier of this node, used to dis-tinguish sibling nodes. All 
    nodes must have a node_id; for nodes under a container C_ATTRIBUTE, the id 
    must be an id-code must be defined in the archetype terminolo-gy. For valid 
    structures, all node ids are id-codes. For C_PRIMITIVE_OBJECTs, it will have 
    the special value Primitive_node_id."""

    @abstractmethod
    def __init__(self,
                 rm_type_name: str,
                 occurrences: Interval[np.int32],
                 node_id: str,
                parent: Optional['ArchetypeConstraint'] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                **kwargs):
        self.rm_type_name = rm_type_name
        self.occurrences = occurrences
        self.node_id = node_id
        super().__init__(parent, parent_container_attribute_name, list_index, **kwargs)

    @abstractmethod
    def is_equal(self, other: 'CObject'):
        return (type(self) == type(other) and
                self.rm_type_name == other.rm_type_name and
                self.node_id == other.node_id and
                is_equal_value(self.occurrences, other.occurrences))
    
    @abstractmethod
    def as_json(self):
        return {
            "rm_type_name": self.rm_type_name,
            "occurrences": self.occurrences.as_json(),
            "node_id": self.node_id
        }
    
    @abstractmethod
    def as_xml(self, root_tag = None):
        # https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/Archetype.xsd
        tag = "c_object" if root_tag is None else root_tag
        root = ET.Element(tag)
        rm_typ = ET.Element("rm_type_name")
        rm_typ.text = self.rm_type_name
        root.append(rm_typ)

        root.append(self.occurrences.as_xml("occurrences"))

        nod = ET.Element("node_id")
        nod.text = self.node_id
        root.append(nod)

        return root
    
    def from_xml(root: ET.Element, **kwargs):
        typ = get_pyehr_type_from_element(root)
        if typ is None:
            raise RuntimeError("Cannot parse C_OBJECT based element as type was ambiguous")
        elif typ == "C_COMPLEX_OBJECT":
            return CComplexObject.from_xml(root, **kwargs)
        elif typ == "C_CODE_PHRASE":
            return CCodePhrase.from_xml(root, **kwargs)
        elif typ == "ARCHETYPE_SLOT":
            return ArchetypeSlot.from_xml(root, **kwargs)
        elif typ == "C_ARCHETYPE_ROOT":
            return CArchetypeRoot.from_xml(root, **kwargs)
        elif typ == "C_PRIMITIVE_OBJECT":
            return CPrimitiveObject.from_xml(root, **kwargs)
        elif typ == "C_DV_QUANTITY":
            warnings.warn("C_DV_QUANTITY is unsupported, parsing as a placeholder class")
            return CDomainPlaceholder.from_xml(root, **kwargs)
        elif typ == "ARCHETYPE_INTERNAL_REF":
            return ArchetypeInternalRef.from_xml(root, **kwargs)
        else:
            raise RuntimeError(f"Cannot parse C_OBJECT based element as given type \'{typ}\' was not a sub-type of C_OBJECT")
    
    def extract_xml_elements(root: ET.Element, **kwargs) -> tuple[str, Interval[np.int32], str]:
        rm_typ = root.findtext("./rm_type_name")
        occ = Interval.from_xml(root.find("./occurrences"), np.int32)
        nod = root.findtext("./node_id")
        return (rm_typ, occ, nod)
    
    def is_subset_of(self, other):
        raise NotImplementedError()
    
    def is_valid(self):
        raise NotImplementedError()
    
class CDefinedObject(CObject):
    """Abstract parent type of C_OBJECT subtypes that are defined by value, i.e. 
    whose definitions are actually in the archetype rather than being by reference."""

    assumed_value: Optional[AnyClass]
    """Value to be assumed if none sent in data."""

    @abstractmethod
    def __init__(self,
                rm_type_name: str,
                occurrences: Interval[np.int32],
                node_id: str,
                assumed_value: Optional[AnyClass] = None,
                parent: Optional['ArchetypeConstraint'] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                **kwargs):
        self.assumed_value = assumed_value
        super().__init__(rm_type_name, occurrences, node_id, parent, parent_container_attribute_name, list_index, **kwargs)

    @abstractmethod
    def as_xml(self, root_tag=None):
        # https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/Archetype.xsd
        tag = "c_defined_object" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        return sup

    @abstractmethod
    def as_json(self):
        draft = super().as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value.as_json()
        return draft
    
    @abstractmethod
    def is_equal(self, other: 'CDefinedObject'):
        return (super().is_equal(other) and
                is_equal_value(self.assumed_value, other.assumed_value))

    @abstractmethod
    def valid_value(self, a_value: AnyClass) -> bool:
        """True if a_value is valid with respect to constraint expressed in concrete 
        instance of this type."""
        pass

    @abstractmethod
    def prototype_value(self) -> AnyClass:
        """Generate a prototype value from this constraint object."""
        pass

    def has_assumed_value(self) -> bool:
        """True if there is an assumed value."""
        return self.assumed_value is not None

    @abstractmethod
    def default_value(self) -> Optional[AnyClass]:
        """Generate a default value from this constraint object."""
        pass

    @abstractmethod
    def any_allowed(self) -> bool:
        """True if any value of the reference model type being constrained is 
        allowed. Redefine in descendants."""
        pass

class CAttribute(ArchetypeConstraint):
    """Abstract model of constraint on any kind of attribute node."""

    rm_attribute_name: str
    """Reference model attribute within the enclosing type represented by a C_OBJECT."""

    existence: Interval[np.int32]
    """Constraint on every attribute, regardless of whether it is singular or of 
    a container type, which indicates whether its target object exists or not 
    (i.e. is mandatory or not)."""

    children: Optional[list[CObject]]
    """Child C_OBJECT nodes. Each such node represents a constraint on the type 
    of this attribute in its reference model. Multiples occur both for multiple 
    items in the case of container attributes, and alternatives in the case of 
    singular attributes."""

    @abstractmethod
    def __init__(self,
                 rm_attribute_name: str,
                 existence: Interval[np.int32],
                parent: Optional['ArchetypeConstraint'] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                children: Optional[list[CObject]] = None,
                **kwargs):
        if rm_attribute_name == "":
            raise ValueError("rm_attribute_name cannot be empty (invariant: rm_attribute_name_valid)")
        self.rm_attribute_name = rm_attribute_name
        if existence.lower < 0:
            raise ValueError("existence.lower must be >= 0 (invariant: existence_set)")
        if existence.upper > 1:
            raise ValueError("existence.upper must be <= 1 (invariant: existence_set)")
        self.existence = existence
        self.children = children
        super().__init__(parent, parent_container_attribute_name, list_index, **kwargs)

    def any_allowed(self) -> bool:
        """True if any value (i.e. instance) of the reference model attribute represented by this C_ATTIRBUTE is allowed."""
        return (self.children is None or len(self.children) == 0)
    
    @abstractmethod
    def is_equal(self, other: 'CAttribute'):
        return (
            is_equal_value(self.rm_attribute_name, other.rm_attribute_name) and
            is_equal_value(self.existence, other.existence) and
            is_equal_value(self.children, other.children)
        )
    
    @abstractmethod
    def as_json(self):
        draft = {
            "rm_attribute_name": self.rm_attribute_name,
            "existence": self.existence.as_json()
        }
        if self.children is not None:
            draft["children"] = [child.as_json() for child in self.children]
        return draft

    @abstractmethod
    def as_xml(self, root_tag = None):
        # https://specifications.openehr.org/releases/ITS-XML/Release-1.0.2/components/ALL/Archetype.xsd
        tag = "c_attribute" if root_tag is None else root_tag
        root = ET.Element(tag)

        rm_attr = ET.Element("rm_attribute_name")
        rm_attr.text = self.rm_attribute_name
        root.append(rm_attr)

        root.append(self.existence.as_xml("existence"))

        if self.children is not None:
            for child in self.children:
                root.append(child.as_xml("children"))

        return root
    
    def from_xml(root, **kwargs):
        typ = get_pyehr_type_from_element(root)
        if typ is None:
            ET.dump(root)
            raise RuntimeError("Cannot parse C_ATTRIBUTE based element as type was ambiguous")
        elif typ == "C_SINGLE_ATTRIBUTE":
            return CSingleAttribute.from_xml(root)
        elif typ == "C_MULTIPLE_ATTRIBUTE":
            return CMultipleAttribute.from_xml(root)
        else:
            raise RuntimeError(f"Cannot parse C_ATTRIBUTE based element as given type \'{typ}\' was not a sub-type of C_ATTRIBUTE")
    
    def extract_xml_elements(root: ET.Element, **kwargs) -> tuple[str, Interval, Optional[list[CObject]]]:
        rm_attr = root.findtext("./rm_attribute_name")
        existence = Interval.from_xml(root.find("./existence"), np.int32)
        children_els = root.findall("./children")
        children = None
        if len(children_els) > 0:
            children = []
            for i in range(len(children_els)):
                child_el = children_els[i]
                children.append(CObject.from_xml(child_el))
        
        return (rm_attr, existence, children)
    
    def is_subset_of(self, other):
        raise NotImplementedError()
    
    def is_valid(self):
        raise NotImplementedError()

class CSingleAttribute(CAttribute):
    """Concrete model of constraint on a single-valued attribute node. The 
    meaning of the inherited children attribute is that they are alternatives."""

    def __init__(self,
                rm_attribute_name: str,
                existence: Interval[np.int32],
            parent: Optional['ArchetypeConstraint'] = None,
            parent_container_attribute_name: Optional[str] = None,
            list_index: Optional[int] = None,
            children: Optional[list[CObject]] = None,
            **kwargs):
        if children is not None:
            for child in children:
                if child.occurrences.upper > 1:
                    raise ValueError("Every child in children must have child.occurences.upper <= 1 for C_SINGLE_ATTRIBUTE (invariant: members_valid)")
        super().__init__(rm_attribute_name, existence, parent, parent_container_attribute_name, list_index, children, **kwargs)

    def alternatives(self) -> Optional[list[CObject]]:
        """List of alternative constraints for the single child of this attribute 
        within the data."""
        return self.children
    
    def as_json(self):
        draft = super().as_json()
        draft["_type"] = "C_SINGLE_ATTRIBUTE"
        return draft
    
    def as_xml(self, root_tag=None):
        tag = "c_single_attribute" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_SINGLE_ATTRIBUTE"
        return sup
    
    def is_equal(self, other):
        return super().is_equal(other)
    
    def from_xml(root, **kwargs) -> 'CSingleAttribute':
        rm_attr, existence, children = CAttribute.extract_xml_elements(root)
        ret = CSingleAttribute(rm_attr, existence, children=children, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))
        
        if ret.children is not None:
            for i in range(len(ret.children)):
                child = ret.children[i]
                child._parent = ret
                child._parent_container_attribute_name = "children"
                child._list_index = i
        return ret

class CMultipleAttribute(CAttribute):
    """Concrete model of constraint on multiply-valued (ie. container) attribute 
    node."""

    cardinality: Cardinality
    """Cardinality of this attribute constraint, if it constraints a container 
    attribute."""

    def __init__(self,
                rm_attribute_name: str,
                existence: Interval[np.int32],
                cardinality: Cardinality,
                parent: Optional['ArchetypeConstraint'] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                children: Optional[list[CObject]] = None,
                **kwargs):
        self.cardinality = cardinality
        super().__init__(rm_attribute_name, existence, parent, parent_container_attribute_name, list_index, children, **kwargs)

    def members(self) -> Optional[list[CObject]]:
        """List of constraints representing members of the container value of 
        this attribute within the data. Semantics of the uniqueness and ordering 
        of items in the container are given by the cardinality."""
        return self.children
    
    def as_xml(self, root_tag=None):
        tag = "c_multiple_attribute" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        sup.append(self.cardinality.as_xml("cardinality"))
        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_MULTIPLE_ATTRIBUTE"
        return sup
    
    def as_json(self):
        draft = super().as_json()
        draft["cardinality"] = self.cardinality.as_json()
        draft["_type"] = "C_MULTIPLE_ATTRIBUTE"
        return draft

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.cardinality, other.cardinality))
    
    def from_xml(root: ET.Element, **kwargs) -> 'CMultipleAttribute':
        rm_attr, existence, children = CAttribute.extract_xml_elements(root)
        card = Cardinality.from_xml(root.find("./cardinality"))
        ret = CMultipleAttribute(rm_attr, existence, card, children=children, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))
        for i in range(len(ret.children)):
            child = ret.children[i]
            child._parent = ret
            child._parent_container_attribute_name = "children"
            child._list_index = i
        return ret
    
# CARDINALITY is implemented elsewhere in rm 1.1.0 so no need to re-implement here

class CComplexObject(CDefinedObject):
    """Constraint on complex objects, i.e. any object that consists of other 
    object constraints."""

    attributes: Optional[list[CAttribute]]
    """List of constraints on attributes of the reference model type represented by this object."""

    def __init__(self,
            rm_type_name: str,
            occurrences: Interval[np.int32],
            node_id: str,
            assumed_value: Optional[AnyClass] = None,
            attributes: Optional[list[CAttribute]] = None,
            parent: Optional['ArchetypeConstraint'] = None,
            parent_container_attribute_name: Optional[str] = None,
            list_index: Optional[int] = None,
            **kwargs):
        self.attributes = attributes
        super().__init__(rm_type_name, occurrences, node_id, assumed_value, parent, parent_container_attribute_name, list_index, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
            is_equal_value(self.attributes, other.attributes))
    
    def as_json(self):
        draft = super().as_json()
        if self.attributes is not None:
            draft["attributes"] = [attribute.as_json() for attribute in self.attributes]
        draft["_type"] = "C_COMPLEX_OBJECT"
        return draft

    def as_xml(self, root_tag=None):
        tag = "c_complex_object" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        if self.attributes is not None:
            for attr in self.attributes:
                sup.append(attr.as_xml("attributes"))
        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_COMPLEX_OBJECT"
        return sup

    def from_xml(root: ET.Element, **kwargs):
        rm_typ, occur, nod = CObject.extract_xml_elements(root)
        attr_els = root.findall("./attributes")
        attrs = None
        if len(attr_els) > 0:
            attrs = []
            for attr_el in attr_els:
                attrs.append(CAttribute.from_xml(attr_el))
        
        ret = CComplexObject(rm_typ, occur, nod, attributes=attrs, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))

        if ret.attributes is not None:
            for i in range(len(ret.attributes)):
                attr = ret.attributes[i]
                attr._parent = ret
                attr._parent_container_attribute_name = "attributes"
                attr._list_index = i
        
        return ret
    
    def any_allowed(self):
        raise NotImplementedError()
    
    def default_value(self):
        raise NotImplementedError()
    
    def prototype_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

class CPrimitiveObject(CDefinedObject):
    """Constraint on a primitive type."""

    item: Optional[CPrimitive]
    """Object actually defining the constraint."""

    def __init__(self,
        rm_type_name: str,
        occurrences: Interval[np.int32],
        node_id: str,
        item: Optional[CPrimitive] = None,
        assumed_value: Optional[AnyClass] = None,
        parent: Optional['ArchetypeConstraint'] = None,
        parent_container_attribute_name: Optional[str] = None,
        list_index: Optional[int] = None,
        **kwargs):
        self.item = item
        super().__init__(rm_type_name, occurrences, node_id, assumed_value, parent, parent_container_attribute_name, list_index, **kwargs)

    def any_allowed(self):
        return self.item is None
    
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.item, other.item))
    
    def as_json(self):
        draft = super().as_json()
        if self.item is not None:
            draft["item"] = self.item.as_json()
        draft["_type"] = "C_PRIMITIVE_OBJECT"
        return draft
    
    def as_xml(self, root_tag=None):
        tag = "c_primitive_object" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        if self.item is not None:
            sup.append(self.item.as_xml("item"))
        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_PRIMITIVE_OBJECT"
        return sup
    
    def default_value(self):
        raise NotImplementedError()
    
    def prototype_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()
    
    def from_xml(root: ET.Element, **kwargs):
        warnings.warn("C_PRIMITIVE_OBJECT from_xml not fully implemented so will not be fully parsed")
        rm_typ, occur, nod = CObject.extract_xml_elements(root)
        return CPrimitiveObject(rm_typ, occur, nod, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))
    
class CDomainType(CDefinedObject):
    """Abstract parent type of domain-specific constrainer types, to be defined in external packages."""

    @abstractmethod
    def standard_equivalent(self) -> CComplexObject:
        """Standard (i.e. C_OBJECT) form of constraint."""
        pass

class CCodePhrase(CDomainType):
    """C_CODE_PHRASE as defined in OpenehrProfile.xsd"""

    assumed_value: Optional[CodePhrase]

    terminology_id: Optional[TerminologyID]

    code_list: Optional[list[str]]

    def __init__(self,
            rm_type_name: str,
            occurrences: Interval[np.int32],
            node_id: str,
            assumed_value: Optional[CodePhrase] = None,
            terminology_id: Optional[TerminologyID] = None,
            code_list: Optional[list[str]] = None,
            parent: Optional['ArchetypeConstraint'] = None,
            parent_container_attribute_name: Optional[str] = None,
            list_index: Optional[int] = None,
            **kwargs):
        self.terminology_id = terminology_id
        self.code_list = code_list
        super().__init__(rm_type_name, occurrences, node_id, assumed_value, parent, parent_container_attribute_name, list_index, **kwargs)

    def as_xml(self, root_tag=None):
        tag = "c_code_phrase" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        if self.assumed_value is not None:
            sup.append(self.assumed_value.as_xml("assumed_value"))
        if self.terminology_id is not None:
            sup.append(self.terminology_id.as_xml("terminology_id"))
        if self.code_list is not None:
            for code in self.code_list:
                code_el = ET.Element("code_list")
                code_el.text = code
                sup.append(code_el)

        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_CODE_PHRASE"
        return sup
        
    def from_xml(root: ET.Element, **kwargs):
        rm_typ, occur, nod = CObject.extract_xml_elements(root)
        assumed_val = root.find("./assumed_value")
        if assumed_val is not None:
            assumed_val = CodePhrase.from_xml(assumed_val)
        term_id = root.find("./terminology_id")
        if term_id is not None:
            term_id = TerminologyID.from_xml(term_id)
        code_list_els = root.findall("./code_list")
        code_list = None
        if code_list_els is not None:
            code_list = []
            for code_list_el in code_list_els:
                code_list.append(code_list_el.text)
        return CCodePhrase(rm_typ, occur, nod, assumed_val, term_id, code_list, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))
    
    def as_json(self):
        draft = super().as_json()
        if self.assumed_value is not None:
            draft["assumed_value"] = self.assumed_value.as_json()
        if self.terminology_id is not None:
            draft["terminology_id"] = self.terminology_id.as_json()
        if self.code_list is not None:
            draft["code_list"] = self.code_list
        
        draft["_type"] = "C_CODE_PHRASE"
        return draft
    
    def is_equal(self, other: 'CCodePhrase'):
        return (super().is_equal(other) and
                is_equal_value(self.assumed_value, other.assumed_value) and
                is_equal_value(self.terminology_id, other.terminology_id) and 
                is_equal_value(self.code_list, other.code_list))

    def any_allowed(self):
        raise NotImplementedError()
    
    def default_value(self):
        raise NotImplementedError()
    
    def prototype_value(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

    def standard_equivalent(self):
        raise NotImplementedError()

class CReferenceObject(CObject):
    """Abstract parent type of C_OBJECT subtypes that are defined by reference."""
    pass

class ArchetypeSlot(CReferenceObject):
    """Constraint describing a slot' where another archetype can occur."""

    includes: Optional[list[Assertion]]
    """List of constraints defining other archetypes that could be included at this point."""

    excludes: Optional[list[Assertion]]
    """List of constraints defining other archetypes that cannot be included at this point."""

    def __init__(self,
                rm_type_name: str,
                occurrences: Interval[np.int32],
                node_id: str,
                includes: Optional[list[Assertion]] = None,
                excludes: Optional[list[Assertion]] = None,
                parent: Optional['ArchetypeConstraint'] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                **kwargs):
        if includes is not None and len(includes) == 0:
            raise ValueError("If provided, includes cannot be an empty list (invariant: includes_valid)")
        self.includes = includes
        if excludes is not None and len(excludes) == 0:
            raise ValueError("If provided, excludes cannot be an empty list (invariant: excludes_valid)")
        self.excludes = excludes
        super().__init__(rm_type_name, occurrences, node_id, parent, parent_container_attribute_name, list_index, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.includes, other.includes) and
                is_equal_value(self.excludes, other.excludes))
    
    def as_json(self):
        draft = super().as_json()
        if self.includes is not None:
            draft["includes"] = [assertion.as_json() for assertion in self.includes]
        if self.excludes is not None:
            draft["excludes"] = [assertion.as_json() for assertion in self.excludes]
        draft["_type"] = "ARCHETYPE_SLOT"
        return draft
    
    def as_xml(self, root_tag=None):
        tag = "archetype_slot" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        if self.includes is not None:
            for incl in self.includes:
                sup.append(incl.as_xml("includes"))
        if self.excludes is not None:
            for excl in self.excludes:
                sup.append(excl.as_xml("excludes"))
        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "ARCHETYPE_SLOT"
        return sup
    
    def from_xml(root: ET.Element, **kwargs):
        rm_typ, occur, nod = CObject.extract_xml_elements(root)
        incl_els = root.findall("./includes")
        incls = None
        if len(incl_els) > 0:
            incls = []
            for incl_el in incl_els:
                incls.append(Assertion.from_xml(incl_el))
        excls = None
        excl_els = root.findall("./excludes")
        if len(excl_els) > 0:
            excls = []
            for excl_el in excl_els:
                excls.append(Assertion.from_xml(excl_el))
        
        return ArchetypeSlot(rm_typ, occur, nod, incls, excls, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))

class ArchetypeInternalRef(CReferenceObject):
    """A constraint defined by proxy, using a reference to an object constraint 
    defined elsewhere in the same archetype.

    Note that since this object refers to another node, there are two objects 
    with available occurrences values. The local occurrences value on an 
    ARCHETYPE_INTERNAL_REF should always be used; when setting this from a 
    serialised form, if no occurrences is mentioned, the target occurrences 
    should be used (not the standard default of {1..1}); otherwise the locally 
    specified occurrences should be used as normal. When serialising out, 
    if the occurrences is the same as that of the target, it can be left out."""

    target_path: str
    """Reference to an object node using archetype path notation."""

    def __init__(self,
                rm_type_name: str,
                occurrences: Interval[np.int32],
                node_id: str,
                target_path: str,
                parent: Optional[ArchetypeConstraint] = None,
                parent_container_attribute_name: Optional[str] = None,
                list_index: Optional[int] = None,
                **kwargs):
        if target_path == "":
            raise ValueError("target_path cannot be empty (invariant: target_path_valid)")
        self.target_path = target_path
        super().__init__(rm_type_name, occurrences, node_id, parent, parent_container_attribute_name, list_index, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                self.target_path == other.target_path)
    
    def as_json(self):
        draft = super().as_json()
        draft["target_path"] = self.target_path
        draft["_type"] = "ARCHETYPE_INTERNAL_REF"
        return draft
    
    def as_xml(self, root_tag=None):
        tag = "archetype_internal_ref" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        tgt = ET.Element("target_path")
        tgt.text = self.target_path
        sup.append(tgt)
        return sup
    
    def from_xml(root: ET.Element, **kwargs) -> 'ArchetypeInternalRef':
        rm_typ, occ, nod = CObject.extract_xml_elements(root)
        tgt = root.findtext("./target_path")
        return ArchetypeInternalRef(rm_typ, occ, nod, tgt, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))
    
class ConstraintRef(CReferenceObject):
    """Reference to a constraint described in the same archetype, but outside the 
    main constraint structure. This is used to refer to constraints expressed in 
    terms of external resources, such as constraints on terminology value sets."""

    reference: str
    """Reference to a constraint in the archetype local ontology."""

    def __init__(self,
            rm_type_name: str,
            occurrences: Interval[np.int32],
            node_id: str,
            reference: str,
            parent: Optional[ArchetypeConstraint] = None,
            parent_container_attribute_name: Optional[str] = None,
            list_index: Optional[int] = None,
            **kwargs):
        self.reference = reference
        super().__init__(rm_type_name, occurrences, node_id, parent, parent_container_attribute_name, list_index, **kwargs)

    def is_equal(self, other):
        return (super().is_equal(other) and
                self.reference == other.reference)
    
    def as_json(self):
        draft = super().as_json()
        draft["reference"] = self.reference
        draft["_type"] = "CONSTRAINT_REF"
        return draft
    
    def as_xml(self, root_tag=None):
        tag = "constraint_ref" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        tgt = ET.Element("reference")
        tgt.text = self.reference
        sup.append(tgt)
        return sup
    
    def from_xml(root: ET.Element, **kwargs) -> 'ArchetypeInternalRef':
        rm_typ, occ, nod = CObject.extract_xml_elements(root)
        ref = root.findtext("./reference")
        return ArchetypeInternalRef(rm_typ, occ, nod, ref, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))


class CArchetypeRoot(CComplexObject):
    """C_ARCHETYPE_ROOT as defined in Template.xsd"""
    
    archetype_id: ArchetypeID

    template_id: Optional[TemplateID]

    term_definitions: Optional[list[ArchetypeTerm]]

    term_bindings: Optional[list[TermBindingSet]]

    def __init__(self,
        rm_type_name: str,
        occurrences: Interval[np.int32],
        node_id: str,
        archetype_id: ArchetypeID,
        template_id: Optional[TemplateID] = None,
        term_definitions: Optional[list[ArchetypeTerm]] = None,
        term_bindings: Optional[list[TermBindingSet]] = None,
        assumed_value: Optional[AnyClass] = None,
        attributes: Optional[list[CAttribute]] = None,
        parent: Optional[ArchetypeConstraint] = None,
        parent_container_attribute_name: Optional[str] = None,
        list_index: Optional[int] = None,
        **kwargs):
        self.archetype_id = archetype_id
        self.template_id = template_id
        self.term_definitions = term_definitions
        self.term_bindings = term_bindings
        super().__init__(rm_type_name, occurrences, node_id, assumed_value, attributes, parent, parent_container_attribute_name, list_index, **kwargs)

    def from_xml(root: ET.Element, **kwargs):
        warnings.warn("C_ARCHETYPE_ROOT from_xml not fully implemented, elements will be missed when parsing.", UserWarning)
        cco : CComplexObject = CComplexObject.from_xml(root, **kwargs)
        aid = ArchetypeID.from_xml(root.find("./archetype_id"))
        tid = root.find("./template_id")
        if tid is not None:
            tid = TemplateID.from_xml(tid)

        tds = root.findall("./term_definitions")
        term_defs = None
        if len(tds) > 0:
            term_defs = []
            for td_el in tds:
                term_defs.append(ArchetypeTerm.from_xml(td_el))

        # TODO: TermBindings
        
        return CArchetypeRoot(cco.rm_type_name, cco.occurrences, cco.node_id, aid, tid, term_defs, None, cco.assumed_value, cco.attributes, cco._parent, cco._parent_container_attribute_name, cco._list_index)
    
    def as_xml(self, root_tag=None):
        warnings.warn("C_ARCHETYPE_ROOT as_xml not fully implemented, elements will be missed when serialising.", UserWarning)
        tag = "c_archetype_root" if root_tag is None else root_tag
        sup = super().as_xml(tag)
        sup.append(self.archetype_id.as_xml("archetype_id"))
        if self.template_id is not None:
            sup.append(self.template_id.as_xml("template_id"))

        sup.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        sup.attrib["xsi:type"] = "C_ARCHETYPE_ROOT"
        
        if self.term_definitions is not None:
            for term_def in self.term_definitions:
                sup.append(term_def.as_xml("term_definitions"))

        # TODO: TermBindings

        return sup
    
    def as_json(self):
        draft = super().as_json()
        draft["archetype_id"] = self.archetype_id.as_json()
        if self.template_id is not None:
            draft["template_id"] = self.template_id.as_json()
        
        if self.term_bindings is not None:
            draft["term_bindings"] = [tb.as_json() for tb in self.term_bindings]

        if self.term_definitions is not None:
            draft["term_definitions"] = [td.as_json() for td in self.term_definitions]

        draft["_type"] = "C_ARCHETYPE_ROOT"
        return draft
        
    def is_equal(self, other):
        return (super().is_equal(other) and
                is_equal_value(self.archetype_id, other.archetype_id) and
                is_equal_value(self.template_id, other.template_id) and
                is_equal_value(self.term_definitions, other.term_definitions) and
                is_equal_value(self.term_bindings, other.term_bindings))
    
# C_DOMAIN_TYPEs that are defined in OpenehrProfile.xsd. Would be in a separate class
#  however they are here to avoid headache of circular import errors

class CDomainPlaceholder(CDomainType):
    """Generic C_DOMAIN_TYPE used as placeholder for unsupported classes.
    assumed_value will always be set to None but may not be in practice"""

    def __init__(self,
            rm_type_name: str,
            occurrences: Interval[np.int32],
            node_id: str,
            assumed_value: Optional[AnyClass] = None,
            parent: Optional['ArchetypeConstraint'] = None,
            parent_container_attribute_name: Optional[str] = None,
            list_index: Optional[int] = None,
            **kwargs):
        super().__init__(rm_type_name, occurrences, node_id, assumed_value, parent, parent_container_attribute_name, list_index, **kwargs)

    def as_json(self):
        warnings.warn("C_DOMAIN_PLACEHOLDER as_xml() used, produced json will be missing elements")
        return super().as_json()
    
    def as_xml(self, root_tag=None):
        warnings.warn("C_DOMAIN_PLACEHOLDER as_xml() used, produced xml will be missing elements")
        return super().as_xml(root_tag)
    
    def from_xml(root, **kwargs):
        warnings.warn("C_DOMAIN_PLACEHOLDER from_xml() used, produced class structure will not match imported XML")
        rm_typ, occ, nod = CObject.extract_xml_elements(root)
        return CDomainPlaceholder(rm_typ, occ, nod, assumed_value=None, parent=kwargs.get("parent"), parent_container_attribute_name=kwargs.get("parent_container_attribute_name"), list_index=kwargs.get("list_index"))

    def is_equal(self, other):
        return super().is_equal(other)
    
    def any_allowed(self):
        raise NotImplementedError()
    
    def default_value(self):
        raise NotImplementedError()
    
    def prototype_value(self):
        raise NotImplementedError()
    
    def standard_equivalent(self):
        raise NotImplementedError()
    
    def valid_value(self, a_value):
        raise NotImplementedError()

# class CQuantityItem(AnyClass, IXMLSupport):
#     """C_QUANTITY_ITEM as defined in Archetype.xsd"""
#     pass

# class CDVQuantity(CDomainType):
#     """C_DV_QUANTITY as defined in Archetype.xsd"""
    
#     property_var : Optional[CodePhrase]

#     list_var : Optional[list[CQuantityItem]]

#     def __init__(self,
#             rm_type_name: str,
#             occurrences: Interval[np.int32],
#             node_id: str,
#             assumed_value: Optional[DVQuantity] = None,
#             property_var: Optional[CodePhrase] = None,
#             list_var: Optional[CodePhrase] = None,
#             parent: Optional['ArchetypeConstraint'] = None,
#             parent_container_attribute_name: Optional[str] = None,
#             list_index: Optional[int] = None,
#             **kwargs):
#         self.property_var = property_var
#         self.list_var = list_var
#         super().__init__(rm_type_name, occurrences, node_id, assumed_value, parent, parent_container_attribute_name, list_index, **kwargs)

#     def as_xml(self, root_tag=None):
#         tag = "cdvquantity" if root_tag is None else root_tag
#         sup = super().as_xml(tag)
#         if self.property_var is not None:
#             sup.append(self.property_var.as_xml("property"))
#         if self.list_var is not None:
#             for quant_item in self.list_var:
#                 sup.append(quant_item.as_xml("list"))
#         return sup

#     def from_xml(root: ET.Element, **kwargs):
#         rm_typ, occ, nod = CObject.extract_xml_elements(root)
