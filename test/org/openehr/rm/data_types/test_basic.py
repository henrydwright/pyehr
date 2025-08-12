import pytest

from org.openehr.rm.data_types import DataValue
from org.openehr.rm.data_types.basic import DVIdentifier

def test_data_value_abstract():
    with pytest.raises(TypeError):
        d = DataValue()

def test_dv_identifier_id_valid():
    # OK
    identifier = DVIdentifier("9990548609", "NHS Digital", "NHS Digital", "NHS Number")
    # Not OK
    with pytest.raises(ValueError):
        identifier = DVIdentifier("", "NHS Digital", "NHS Digital", "NHS Number")
        
    

    