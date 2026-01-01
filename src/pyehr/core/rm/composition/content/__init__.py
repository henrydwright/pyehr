"""The `content` package contains the CONTENT_ITEM class, ancestor class of 
all content types, and the navigation and entry packages, which contain 
SECTION, ENTRY and related types."""

from abc import abstractmethod
from typing import Optional

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.rm.common.archetyped import Archetyped, FeederAudit, Link, Locatable, Pathable
from pyehr.core.rm.data_types.text import DVText


class ContentItem(Locatable):
    """Abstract ancestor of all concrete content types."""

    @abstractmethod
    def __init__(self, 
                name: DVText, 
                archetype_node_id: str, 
                uid : Optional[UIDBasedID] = None, 
                links : Optional[list[Link]] = None,  
                archetype_details : Optional[Archetyped] = None,
                feeder_audit : Optional[FeederAudit] = None,
                parent: Optional[Pathable] = None,
                parent_container_attribute_name: Optional[str] = None,
                **kwargs):
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)