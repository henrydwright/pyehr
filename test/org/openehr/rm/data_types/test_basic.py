import pytest

from org.openehr.rm.data_types import DataValue

def test_data_value_abstract():
    with pytest.raises(TypeError):
        d = DataValue()
        
    

    