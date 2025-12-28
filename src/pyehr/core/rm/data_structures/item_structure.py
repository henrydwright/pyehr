"""The `item_structure` package classes are a formalisation of the need for 
generic, archetypable data structures, and are used by all openEHR 
reference models."""

from abc import abstractmethod
from typing import Optional

import numpy as np

from pyehr.core.base.base_types.identification import UIDBasedID
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.archetyped import Link, Archetyped, Pathable, FeederAudit, PyehrInternalProcessedPath, PyehrInternalPathPredicateType
from pyehr.core.rm.data_structures import DataStructure
from pyehr.core.rm.data_structures.representation import Element, Cluster
from pyehr.core.rm.data_types.text import DVText

class ItemStructure(DataStructure):
    """Abstract parent class of all spatial data types."""

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

class ItemSingle(ItemStructure):
    """Logical single value data structure. Used to represent any data which is 
    logically a single value, such as a person's height or weight."""

    item: Element

    def __init__(self, 
            name: DVText, 
            archetype_node_id: str, 
            item: Element,
            uid : Optional[UIDBasedID] = None, 
            links : Optional[list[Link]] = None,  
            archetype_details : Optional[Archetyped] = None,
            feeder_audit : Optional[FeederAudit] = None,
            parent: Optional[Pathable] = None,
            parent_container_attribute_name: Optional[str] = None,
            **kwargs):
        item._parent = self
        item._parent_container_attribute_name = "item"
        self.item = item
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return self
        
        if path.current_node_attribute == "item":
            return self.item.item_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Item not found: expected 'item' at ItemSingle but got \'{path.current_node_attribute}\'")
            
    def items_at_path(self, a_path):
        raise ValueError("Items not found: path would always result in single item, not multiple items")

    def path_exists(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "item":
            return self.item.path_exists(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
               
    def path_unique(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "item":
            return self.item.path_unique(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
            
    def as_hierarchy(self):
        return self.item
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/ITEM_SINGLE.json
        draft = super().as_json()
        draft["item"] = self.item.as_json()
        draft["_type"] = "ITEM_SINGLE"
        return draft
    
class ItemList(ItemStructure):
    """Logical list data structure, where each item has a value and can be 
    referred to by a name and a positional index in the list. The list may be empty.

    ITEM_LIST is used to represent any data which is logically a list of values, 
    such as blood pressure, most protocols, many blood tests etc.

    Not to be used for time-based lists, which should be represented with the 
    proper temporal class, i.e. HISTORY."""

    _items_name_dict : Optional[dict[str, Element]]
    """Internal map of name to elements"""

    _items_archid_dict: Optional[dict[str, Element]]
    """Internal map of archetype_node_id to elements"""

    def _get_items(self):
        return list(self._items_name_dict.values())

    items = property(
        fget=_get_items
    )
    """Physical representation of the list."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str, 
        items: Optional[list[Element]],
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        archetype_details : Optional[Archetyped] = None,
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
            if items is not None:
                self._items_name_dict = dict()
                self._items_archid_dict = dict()
                for item in items:
                    item._parent = self
                    item._parent_container_attribute_name = "items"
                    self._items_name_dict[item.name.value] = item
                    self._items_archid_dict[item.archetype_node_id] = item
            else:
                self._items_name_dict = None
            super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def item_count(self) -> np.int32:
        """Count of all items."""
        return np.int32(len(self.items))
    
    def names(self) -> Optional[list[DVText]]:
        """Retrieve the names of all items."""
        if self._items_name_dict is None:
            return None
        else:
            return [item.name for item in self.items]
        
    def named_item(self, a_name : str) -> Element:
        """Retrieve the item with name `a_name`."""
        if self._items_name_dict is None:
            raise ValueError("Cannot retrieve item from empty ITEM_LIST")
        elif a_name in self._items_name_dict:
            return self._items_name_dict[a_name]
        else:
            raise ValueError(f"Item not found: Named item \'{a_name}\' not found in this item list")
        
    def _archid_item(self, a_id : str) -> Element:
        if self._items_archid_dict is None:
            raise ValueError("Cannot retrieve item from empty ITEM_LIST")
        elif a_id in self._items_archid_dict:
            return self._items_archid_dict[a_id]
        else:
            raise ValueError(f"Item not found: Item with archetype node ID \'{a_id}\' not found in this item list")

    def _pred_item(self, pred, pred_type: PyehrInternalPathPredicateType):
        if pred_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
            return self._archid_item(pred)
        elif pred_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
            return self.ith_item(int(pred))
        else:
            raise ValueError(f"Cannot process path with predicate of type \'{str(pred_type)}\'")
            
    def ith_item(self, i: np.int32) -> Element:
        """Retrieve the i-th item with name."""
        if self._items_name_dict is None:
            raise ValueError("Item not found: Cannot retrieve item from empty ITEM_LIST")
        else:
            return self.items[i]
        
    def as_hierarchy(self):
        """Generate a CEN EN13606-compatible hierarchy consisting of a single 
        CLUSTER containing the ELEMENTs of this list."""
        return Cluster(
            name=self.name,
            archetype_node_id=self.archetype_node_id,
            items=self.items,
            uid=self.uid,
            links=self.links,
            archetype_details=self.archetype_details,
            feeder_audit=self.feeder_audit
        )
    
    def item_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return self
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None:
                raise ValueError(f"Item not found: path led to potentially multiple items")            
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).item_at_path(path.remaining_path if path.remaining_path is not None else "")
        else:
            raise ValueError(f"Item not found: expected 'items' at ItemList but got \'{path.current_node_attribute}\'")
    
    def items_at_path(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            raise ValueError("Items not found: path led to a single ITEM_LIST")
        
        if path.current_node_attribute == "items":
            if path.remaining_path is None:
                # leaf
                if path.current_node_predicate is not None:
                    raise ValueError(f"Items not found: path led to single item")
                return self.items
            else:
                # intermediate
                if path.current_node_predicate is None:
                    raise ValueError("Invalid path: ambiguous path provided - item in list not specified")
                return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).items_at_path(path.remaining_path)
        else:
            raise ValueError(f"Items not found: expected 'items' at ItemList but got \'{path.current_node_attribute}\'")
        
    def path_exists(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None and path.remaining_path is None:
                return True           
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).path_exists(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
    
    def path_unique(self, a_path):
        path = PyehrInternalProcessedPath(a_path)

        if path.is_self_path():
            return True
        
        if path.current_node_attribute == "items":
            if path.current_node_predicate is None and path.remaining_path is None:
                return False      
            return self._pred_item(path.current_node_predicate, path.current_node_predicate_type).path_unique(path.remaining_path if path.remaining_path is not None else "")
        else:
            return False
            
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/ITEM_LIST.json
        draft = super().as_json()
        if self.items is not None:
            draft["items"] = [e.as_json() for e in self.items]
        draft["_type"] = "ITEM_LIST"
        return draft
    
class ItemTable(ItemStructure):
    """Logical relational database style table data structure, in which columns 
    are named and ordered with respect to each other. Implemented using 
    Cluster-per-row encoding. Each row Cluster must have an identical number 
    of Elements, each of which in turn must have identical names and value 
    types in the corresponding positions in each row.
    
    Some columns may be designated key' columns, containing key data for each 
    row, in the manner of relational tables. This allows row-naming, where each 
    row represents a body site, a blood antigen etc. All values in a column have 
    the same data type.
    
    Used for representing any data which is logically a table of values, such as 
    blood pressure, most protocols, many blood tests etc.
    
    Misuse: Not to be used for time-based data, which should be represented with 
    the temporal class HISTORY. The table may be empty."""
    
    _column_name_list: Optional[list[DVText]]
    """List of column names, generated from first row on initialisation"""

    _plain_column_name_set: Optional[set[str]]
    """Set of columns names as plain strs, generated from first row on intialisation"""

    _row_name_list: Optional[list[DVText]]
    """List of row names"""

    _rowname_row_dict: Optional[dict[str, Cluster]]
    """Mapping of row names (in plain strs) to row clusters"""

    def _get_rows(self):
        return list(self._rowname_row_dict.values())
    
    rows = property(
        fget=_get_rows
    )
    """Physical representation of the table as a list of CLUSTERs, each containing
     the data of one row of the table."""

    def __init__(self, 
        name: DVText, 
        archetype_node_id: str, 
        rows: Optional[list[Cluster]],
        uid : Optional[UIDBasedID] = None, 
        links : Optional[list[Link]] = None,  
        archetype_details : Optional[Archetyped] = None,
        feeder_audit : Optional[FeederAudit] = None,
        parent: Optional[Pathable] = None,
        parent_container_attribute_name: Optional[str] = None,
        **kwargs):
        if rows is not None:
            self._column_name_list = list()
            self._row_name_list = list()
            self._rowname_row_dict = dict()
            column_count = 0
            self._plain_column_name_set = set()
        for i in range(len(rows)):
            row = rows[i]
            if i == 0:
                for item in row.items:
                    if not isinstance(item, Element):
                        raise ValueError("Each CLUSTER representing a row must have only ELEMENTs as members")
                    self._column_name_list.append(item.name)
                    self._plain_column_name_set.add(item.name.value)
                column_count = len(self._column_name_list)
            else:
                cols = len(row.items)
                if cols != column_count:
                    raise ValueError(f"Every row must have the same number of items. First row had \'{column_count}\' but row #{i} had \'{cols}\'")
                for j in range(cols):
                    item = row.items[j]
                    if not isinstance(item, Element):
                        raise ValueError("Each CLUSTER representing a row must have only ELEMENTs as members")
                    if item.name.value not in self._plain_column_name_set:
                        raise ValueError(f"Each row must have columns with the same names. Column named \'{item.name.value}\' not in the first row.")
            self._row_name_list.append(row.name)
            self._rowname_row_dict[row.name.value] = row        

        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, parent, parent_container_attribute_name, **kwargs)

    def row_count(self) -> np.int32:
        """Number of rows in the table"""
        return len(self._rowname_row_dict.values())

    def column_count(self) -> np.int32:
        """Return number of columns in the table."""
        return len(self._column_name_list)

    def row_names(self) -> Optional[list[DVText]]:
        """Return set of row names."""
        return self._row_name_list

    def column_names(self) -> Optional[list[DVText]]:
        """Return set of column names."""
        return self._column_name_list

    def ith_row(self, i: np.int32) -> Cluster:
        """Return i-th row"""
        if i < 0:
            raise IndexError("Row number cannot be negative.")
        return self.rows[i]

    def has_row_with_name(self, a_key: str) -> bool:
        """Return True if there is a row with name = a_key."""
        # TODO: report typo in the class listing on the spec website (says "column")
        return a_key in self._rowname_row_dict

    def has_column_with_name(self, a_key: str) -> bool:
        """Return True if there is a column with name = a_key."""
        return a_key in self._plain_column_name_set

    def named_row(self, a_key: str) -> Cluster:
        """Return row with name = a_key."""
        return self._rowname_row_dict[a_key]

    def has_row_with_key(self, keys: list[str]) -> bool:
        """Return True if there is a row with key keys."""
        # The specification declares some rows may be marked as "keys" but does not provide
        #  any mechanism for this to be specified, nor stored so any key would be transient
        #  and not passable between client and server, hence this method *should* go unused
        #  in any case, we won't support it.
        raise NotImplementedError("Marking columns as keys is not supported, so cannot retrieve rows based on keys.")

    def row_with_key(self, keys: list[str]) -> Cluster:
        """Return rows with particular keys."""
        raise NotImplementedError("Marking columns as keys is not supported, so cannot retrieve rows based on keys.")

    def element_at_cell_ij(self, i: np.int32, j: np.int32):
        """Return cell at a particular location."""
        return self.rows[i].items[j]

    def as_hierarchy(self):
        """Generate a CEN EN13606-compatible hierarchy consisting of a single 
        CLUSTER containing the CLUSTERs representing the rows of this table."""
        # TODO: the original definition says "CLUSTERs representing the *columns*"" but I think this is a typo
        return Cluster(
            name=self.name,
            archetype_node_id=self.archetype_node_id,
            items=self.rows
        )

    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/RM/Release-1.1.0/Data_structures/ITEM_TABLE.json
        draft = super().as_json()
        if self.rows is not None:
            draft["rows"] = [row.as_json() for row in self.rows]
        draft["_type"] = "ITEM_TABLE"
        return draft

    def _path_eval(self, a_path: str, single_item: bool, check_only: bool):
        path = PyehrInternalProcessedPath(a_path)
        if path.is_self_path():
            if single_item:
                return self
            else:
                raise ValueError("Items not found: reached single item (ITEM_TABLE)")
        
        ret_item = None

        if path.current_node_attribute == "rows":
            if path.current_node_predicate_type is None:
                ret_item = self.rows
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
                ret_item = self.rows[int(path.current_node_predicate)]
            elif path.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
                matches = []
                for row in self.rows:
                    if row.archetype_node_id == path.current_node_predicate:
                        matches.append(row)
                if len(matches) == 1:
                    ret_item = matches[0]
                else:
                    ret_item = matches

            if path.remaining_path is None:
                if check_only:
                    return True
                if single_item:
                    if not isinstance(ret_item, list):
                        return ret_item
                    else:
                        raise ValueError("Item not found: multiple items returned by query.")
                else:
                    if isinstance(ret_item, list):
                        return ret_item
                    else:
                        raise ValueError("Items not found: single item returned by query")
            else:
                if isinstance(ret_item, list):
                    raise ValueError("Path invalid: ambiguous intermediate path step containing multiple items")
                else:
                    if check_only:
                        return ret_item.path_exists(path.remaining_path)
                    if single_item:
                        return ret_item.item_at_path(path.remaining_path)
                    else:
                        return ret_item.items_at_path(path.remaining_path)
        else:
            raise ValueError(f"Path invalid: expected 'rows' at ITEM_TABLE but found \'{path.current_node_attribute}\'")


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
    
    def is_equal(self, other):
        return (super().is_equal(other) and 
                is_equal_value(self.rows, other.rows))

    