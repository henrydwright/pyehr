import pytest

from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeConstraint

# test what can be tested from base abstract class
class _ImplArchetypeConstraint(ArchetypeConstraint):
    def __init__(self, parent = None, parent_container_attribute_name = None, list_index = None, **kwargs):
        super().__init__(parent, parent_container_attribute_name, list_index, **kwargs)
    
    def as_json(self):
        return {}
    
    def is_equal(self, other):
        return False
    
    def is_subset_of(self, other):
        return False
    
    def is_valid(self):
        return False

def test_archetype_constraint_path():
    iac1 = _ImplArchetypeConstraint(
        parent=None,
    )
    assert iac1.path() == "/definition"
    iac2 = _ImplArchetypeConstraint(
        parent=iac1,
        parent_container_attribute_name="attributes",
        list_index=0
    )
    assert iac2.path() == "/definition/attributes[0]"
    iac3 = _ImplArchetypeConstraint(
        parent=iac1,
        parent_container_attribute_name="attributes",
        list_index=1
    )
    assert iac3.path() == "/definition/attributes[1]"
    iac4 = _ImplArchetypeConstraint(
        parent=iac3,
        parent_container_attribute_name="children",
        list_index=0
    )
    assert iac4.path() == "/definition/attributes[1]/children[0]"
    