"""The `navigation` Package defines a hierachical heading structure, in which all 
individual headings are considered to belong to a "tree of headings". 
Each heading is an instance of the class `SECTION`"""

from typing import Optional
from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Pathable
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.ehr.composition.content import ContentItem


class Section(ContentItem):
    """Represents a heading in a heading structure, or section tree. Created 
    according to archetyped structures for typical headings such as SOAP, 
    physical examination, but also pathology result heading structures. 
    Should not be used instead of ENTRY hierarchical structures."""

    items: Optional[list[ContentItem]]
    """Ordered list of content items under this section, which may include:

    * more SECTIONs;
    * ENTRYs."""

    def __init__(self, 
            name: DVText, 
            archetype_node_id: str, 
            items: Optional[list[ContentItem]] = None,
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        if items is not None:
            if len(items) == 0:
                raise ValueError("If provided, items cannot be an empty list (invariant: items_valid)")
        self.items = items
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_at_path(self, a_path):
        return super().item_at_path(a_path)
    
    def items_at_path(self, a_path):
        return super().items_at_path(a_path)
    
    def path_exists(self, a_path):
        return super().path_exists(a_path)
    
    def path_unique(self, a_path):
        return super().path_unique(a_path)