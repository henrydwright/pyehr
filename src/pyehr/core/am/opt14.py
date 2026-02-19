from typing import Optional

import xml.etree.ElementTree as ET

from pyehr.core.base.base_types.identification import HierObjectID, TemplateID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.resource import ResourceDescription
from pyehr.core.its.xml import IXMLSupport
from pyehr.core.rm.common.generic import RevisionHistory
from pyehr.core.rm.data_types.text import CodePhrase


class OperationalTemplate(IXMLSupport):
    """pyehr representation of the OPT 1.4 XML template represented in XML
    schemas in Template.xsd"""

    language: CodePhrase

    is_controlled: Optional[bool]

    description: Optional[ResourceDescription]

    revision_history: Optional[RevisionHistory]

    uid: Optional[HierObjectID]

    template_id: TemplateID

    concept: str

    definition = None #C_ARCHETYPE_ROOT

    ontology = None #FLAT_ARCHETYPE_ONTOLOGY

    component_ontologies = None #FLAT_ARCHETYPE_ONTOLOGY

    annotations = None #ANNOTATION

    constraints = None #T_CONSTRAINT

    view = None #T_VIEW

    def __init__(self, 
                 language:CodePhrase, 
                 template_id: TemplateID, 
                 concept: str, 
                 is_controlled: Optional[bool] = None, 
                 description: Optional[ResourceDescription] = None, 
                 revision_history: Optional[RevisionHistory] = None, 
                 uid: Optional[HierObjectID] = None):
        self.language = language
        self.template_id = template_id
        self.concept = concept
        self.is_controlled = is_controlled
        self.description = description
        self.revision_history = revision_history
        self.uid = uid

    def as_xml(self, root_tag = None):
        return super().as_xml(root_tag)
    
    def from_xml(root: ET.Element, **kwargs) -> 'OperationalTemplate':
        lang = CodePhrase.from_xml(root.find("./language"))
        tid = TemplateID.from_xml(root.find("./template_id"))
        concept = root.findtext("./concept")
        return OperationalTemplate(lang, tid, concept)
