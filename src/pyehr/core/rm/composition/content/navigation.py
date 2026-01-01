"""The `navigation` Package defines a hierachical heading structure, in which all 
individual headings are considered to belong to a "tree of headings". 
Each heading is an instance of the class `SECTION`"""

from typing import Optional
from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Pathable, PyehrInternalProcessedPath
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.composition.content import ContentItem


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

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if check_only:
                return True
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (SECTION)")

        if path.current_node_attribute == "items":
            return self._path_resolve_item_list(path, self.items, single_item, check_only)
        else:
            if check_only:
                return False
            raise ValueError(f"Path invalid: expected 'items' at SECTION but found \'{path.current_node_attribute}\'")
         
    def item_at_path(self, a_path):
        return self._path_eval(a_path, True, False)
    
    def items_at_path(self, a_path):
        return self._path_eval(a_path, False, False)
    
    def path_exists(self, a_path):
        return self._path_eval(a_path, None, True)
    
    def path_unique(self, a_path):
        try:
            self.item_at_path(a_path)
            return True
        except (ValueError):
            return False
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Composition/SECTION.json
        draft = super().as_json()
        if self.items is not None:
            draft["items"] = [item.as_json() for item in self.items]
        draft["_type"] = "SECTION"
        return draft
