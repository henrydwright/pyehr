import pytest

from org.openehr.rm.common.archetyped import Pathable

def test_pathable_is_abstract():
    with pytest.raises(TypeError):
        p = Pathable()