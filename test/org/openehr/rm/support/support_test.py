import pytest

from org.openehr.rm.support import ExternalEnvironmentAccess

def test_external_environment_access_is_abstract():
    with pytest.raises(TypeError):
        a = ExternalEnvironmentAccess()