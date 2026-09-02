from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.its.json_tools import decode_json
import pytest

from pyehr.core.am.aom14.archetype.constraint_model.prototypes import CODE_PHRASE

def test_unfilled_json():
    output = {
        '_type': 'CODE_PHRASE',
        'code_string': '',
        'preferred_term': '',
        'terminology_id': {
            '_type': 'TERMINOLOGY_ID',
            'value': ''
        }
    }
    assert is_equal_value(output, CODE_PHRASE.unfilled_json())

def test_unfilled_json_optional_flag_works():
    output = {
        '_type': 'CODE_PHRASE',
        'code_string': '',
        'terminology_id': {
            '_type': 'TERMINOLOGY_ID',
            'value': ''
        }
    }
    assert is_equal_value(output, CODE_PHRASE.unfilled_json(include_optional_elements=False))
    