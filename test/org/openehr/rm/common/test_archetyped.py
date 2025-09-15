import pytest

from org.openehr.base.base_types.identification import ArchetypeID
from org.openehr.rm.common.archetyped import Pathable, Locatable, Link, Archetyped
from org.openehr.rm.data_types.text import DVText
from org.openehr.rm.data_types.uri import DVEHRUri

class _TstLocatableImpl(Locatable):
    def __init__(self, name, archetype_node_id, uid = None, links = None, archetype_details = None, feeder_audit = None, **kwargs):
        super().__init__(name, archetype_node_id, uid, links, archetype_details, feeder_audit, **kwargs)

    def concept(self):
        return super().concept()
    
    def is_archetype_root(self):
        return super().is_archetype_root()
    
    def is_equal(self, other):
        return super().is_equal(other)
    
    def item_at_path(a_path):
        return super().item_at_path()
    
    def items_at_path(a_path):
        return super().items_at_path()
    
    def parent(self):
        return super().parent()
    
    def path_exists(a_path):
        return super().path_exists()
    
    def path_of_item(a_loc):
        return super().path_of_item()
    
    def path_unique(a_path):
        return super().path_unique()

def test_pathable_is_abstract():
    with pytest.raises(TypeError):
        p = Pathable()

def test_locatable_links_valid():
    # OK (no links list)
    l = _TstLocatableImpl(DVText("Gender"), "openEHR-EHR-EVALUATION.gender.v1")
    # OK (links list not empty)
    l = _TstLocatableImpl(DVText("Blood pressure reading"), "openEHR-EHR-OBSERVATION.blood_pressure.v2", links=[Link(DVText("in response to"), DVText("order"), DVEHRUri("ehr:tasks/380daa09-028f-4beb-9803-4aef91644c2a"))])
    # not OK (links list empty)
    with pytest.raises(ValueError):
        l = _TstLocatableImpl(DVText("Gender"), "openEHR-EHR-EVALUATION.gender.v1", links=[])

def test_locatable_archetyped_valid():
    # is_archetype_root xor archetype_details = Void
    l = _TstLocatableImpl(DVText("Gender"), "openEHR-EHR-EVALUATION.gender.v1", archetype_details=Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.gender.v1"), "1.1.0"))
    assert l.is_archetype_root() == True
    l = _TstLocatableImpl(DVText("Administrative gender"), "at0022")
    assert l.is_archetype_root() == False

def test_locatable_archetype_node_id_valid():
    # OK (archetype ID not empty)
    l = _TstLocatableImpl(DVText("Gender"), "openEHR-EHR-EVALUATION.gender.v1")
    # not OK (archetype ID empty)
    with pytest.raises(ValueError):
        l = _TstLocatableImpl(DVText("Gender"), "")

def test_archetyped_rm_version_valid():
    a = Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.gender.v1"), "1.1.0")
    # not OK (rm_version empty)
    with pytest.raises(ValueError):
        a = Archetyped(ArchetypeID("openEHR-EHR-EVALUATION.gender.v1"), "")