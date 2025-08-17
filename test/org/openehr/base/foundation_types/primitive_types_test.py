from org.openehr.base.foundation_types.primitive_types import Uri

import pytest

def test_uri_does_not_allow_plain_text_by_default():
    # OK
    u = Uri("https://example.com/test.php?search='hello+world'")
    u = Uri("https://example.com/test.php?search='hello%20world'")
    # not OK
    with pytest.raises(ValueError):
        u = Uri("https://example.com/test.php?search='hello world'")
    with pytest.raises(ValueError):
        u = Uri("https://example.com/test.php?criteria='this>that'")

def test_uri_permits_plain_text_if_option_chosen():
     # OK
    u = Uri("https://example.com/test.php?search='hello+world'")
    u = Uri("https://example.com/test.php?search='hello%20world'")
    u = Uri("https://example.com/test.php?search='hello world'", allow_unencoded=True)
    u = Uri("https://example.com/test.php?criteria='this>that'", allow_unencoded=True)