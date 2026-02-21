

from typing import Optional
from uuid import UUID

import numpy as np

from pyehr.core.am.aom14.archetype.assertion import Assertion
from pyehr.core.am.aom14.archetype.constraint_model import CComplexObject
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.base.resource import AuthoredResource, ResourceAnnotations


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
                uid: Optional[UUID] = None,
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

