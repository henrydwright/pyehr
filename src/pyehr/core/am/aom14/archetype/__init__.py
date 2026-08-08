

from typing import Optional
from uuid import UUID
import warnings
import xml.etree.ElementTree as ET

import numpy as np

from pyehr.core.am.aom14.archetype.assertion import Assertion
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.base.resource import AuthoredResource, ResourceAnnotations

__all__ = ['Archetype']

class Archetype(AuthoredResource):
    """Archetype equivalent to ARCHETYPED class in Common reference model. Defines 
    semantics of identfication, lifecycle, versioning, composition and 
    specialisation."""

    definition : CComplexObject
    """Root node of the definition of this archetype."""

    ontology: ArchetypeOntology
    """The ontology of the archetype."""

    adl_version: Optional[str]
    """ADL version if archetype was read in from an ADL sharable archetype."""

    archetype_id: ArchetypeID
    """Multi-axial identifier of this archetype in archetype space."""

    concept: str
    """The normative meaning of the archetype as a whole, expressed as a local 
    archetype code, typically “at0000”."""

    parent_archetype_id: Optional[ArchetypeID]
    """Identifier of the specialisation parent of this archetype."""

    invariants: Optional[list[Assertion]]
    """Invariant statements about this object. Statements are expressed in first 
    order predicate logic, and usually refer to at least two attributes."""

    uid: Optional[HierObjectID]
    """OID identifier of this archetype."""

    def __init__(self, 
                original_language: TerminologyCode, 
                definition: CComplexObject,
                ontology: ArchetypeOntology,
                archetype_id: ArchetypeID,
                concept: str,
                adl_version: Optional[str] = None,
                parent_archetype_id: Optional[ArchetypeID] = None,
                invariants: Optional[list[Assertion]] = None,
                uid: Optional[HierObjectID] = None,
                is_controlled: Optional[bool] = None,
                annotations: Optional[ResourceAnnotations] = None):
        self.definition = definition
        self.ontology = ontology
        self.archetype_id = archetype_id
        self.concept = concept
        self.adl_version = adl_version
        self.parent_archetype_id = parent_archetype_id
        self.invariants = invariants
        super().__init__(original_language, uid, is_controlled, annotations)

    def concept_name(self, a_lang: str) -> str:
        """The concept name of the archetype in language a_lang; corresponds to 
        the term definition of the concept attribute in the archetype ontology."""
        raise NotImplementedError()
    
    def physical_paths(self) -> list[str]:
        """Set of language-independent paths extracted from archetype. Paths obey 
        Xpath-like syntax and are formed from alternations of C_OBJECT.node_id 
        and C_ATTRIBUTE.rm_attribute_name values."""
        raise NotImplementedError()
    
    def logical_paths(self, lang: str) -> list[str]:
        """Set of language-dependent paths extracted from archetype. Paths obey 
        the same syntax as physical_paths, but with node_ids replaced by their 
        meanings from the ontology."""
        raise NotImplementedError()
    
    def specialisation_depth(self) -> np.int32:
        """Specialisation depth of this archetype; larger than 0 if this archetype
        has a parent. Derived from terminology.specialisation_depth"""
        raise NotImplementedError()
    
    def is_specialised(self) -> bool:
        """True if this archetype is a specialisation of another."""
        raise NotImplementedError()
    
    def is_valid(self) -> bool:
        """True if the archetype is valid overall; various tests should be used, 
        including checks on node_ids, internal references, and constraint 
        references."""
        raise NotImplementedError()
    
    def node_ids_valid(self) -> bool:
        """True if every node_id found on a C_OBJECT node is found in 
        ontology.term_codes."""
        raise NotImplementedError()
    
    def previous_version(self) -> str:
        """Version of predecessor archetype of this archetype, if any."""
        raise NotImplementedError()
    
    def internal_references_valid(self) -> bool:
        """True if every ARCHETYPE_INTERNAL_REF.target_path refers to a 
        legitimate node in the archetype definition."""
        raise NotImplementedError()
    
    def constraint_references_valid(self) -> bool:
        """True if every CONSTRAINT_REF.reference found on a C_OBJECT node 
        in the archetype definition is found in ontology.constraint_codes."""
        raise NotImplementedError()
    
    def short_concept_name(self) -> str:
        """The short concept name of the archetype extracted from the archetype_id."""
        raise NotImplementedError()
    
    def version(self) -> str:
        raise NotImplementedError()
    
    def as_xml(self, root_tag=None):
        tag = "archetype" if root_tag is None else root_tag
        super_xml = super().as_xml(tag)
        super_xml.append(self.definition.as_xml("definition"))
        super_xml.append(self.ontology.as_xml("ontology"))
        super_xml.append(self.archetype_id.as_xml("archetype_id"))

        conc_el = ET.Element("concept")
        conc_el.text = self.concept
        super_xml.append(conc_el)

        if self.adl_version is not None:
            adl_ver_el = ET.Element("adl_version")
            adl_ver_el.text = self.adl_version
            super_xml.append(adl_ver_el)

        if self.parent_archetype_id is not None:
            super_xml.append(self.parent_archetype_id.as_xml())

        if self.invariants is not None:
            for invariant in self.invariants:
                super_xml.append(invariant.as_xml())

        if self.uid is not None:
            super_xml.append(self.uid.as_xml())

        return super_xml
    
    def from_xml(root: ET.Element, **kwargs):
        (ar_orig_lang, ar_is_cont, ar_description, ar_translations) = AuthoredResource.extract_xml_elements(root)

        arch_id_el = root.find("./archetype_id")
        arch_id = ArchetypeID.from_xml(arch_id_el)

        conc_el = root.find("./concept")
        conc = conc_el.text

        def_el = root.find("./definition")
        definition = CComplexObject.from_xml(def_el)

        ont_el = root.find("./ontology")
        ontology = ArchetypeOntology.from_xml(ont_el)

        adl_ver = root.findtext("./adl_version")

        invs = root.findall("./invariants")
        invariants = None
        if len(invs) > 0:
            invariants = [Assertion.from_xml(inv) for inv in invs]

        uid_el = root.find("./uid")
        uid = None
        if uid_el is not None:
            uid = HierObjectID.from_xml(uid_el)

        paid_el = root.find("./parent_archetype_id")
        paid = None
        if paid_el is not None:
            paid = ArchetypeID.from_xml(paid_el)

        # annotations exists in the RM for this class but not in XML so ignored

        arch = Archetype(
            ar_orig_lang,
            definition,
            ontology,
            arch_id,
            conc,
            adl_version=adl_ver,
            parent_archetype_id=paid,
            invariants=invariants,
            uid=uid,
            is_controlled=ar_is_cont,
            annotations=None
        )

        arch.set_description(ar_description)

        return arch
    
    def as_json(self):
        draft = {
            "original_language": self.original_language.as_json(),
            "archetype_id": self.archetype_id.as_json(),
            "concept": self.concept,
            "definition": self.definition.as_json(),
            "ontology": self.ontology.as_json() 
        }
        if self.is_controlled is not None:
            draft["is_controlled"] = self.is_controlled
        if self.description is not None:
            draft["description"] = self.description.as_json()
        if self._translations is not None:
            draft["translations"] = [tr.as_json() for tr in self._translations.values()]
        if self.uid is not None:
            draft["uid"] = self.uid.as_json()
        if self.adl_version is not None:
            draft["adl_version"] = self.adl_version
        if self.parent_archetype_id is not None:
            draft["parent_archetype_id"] = self.parent_archetype_id.as_json()
        if self.invariants is not None:
            draft["invariants"] = [inv.as_json() for inv in self.invariants]
        draft["_type"] = "ARCHETYPE"
        return draft

    def current_revision(self):
        raise NotImplementedError()
