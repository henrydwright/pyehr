from pyehr.core.base.foundation_types.primitive_types import Uri, ordered
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISOTime, ISODuration, ISOTimeZone

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

def test_isotype_subclasses_instance_of_ordered():
    date = ISODate("2025-08-25")
    time = ISOTime("18:10:00")
    timezone = ISOTimeZone("Z")
    datetime = ISODateTime("2025-08-25T18:10:00")
    duration = ISODuration("P2Y")
    assert isinstance(date, ordered)
    assert isinstance(time, ordered)
    assert isinstance(timezone, ordered)
    assert isinstance(datetime, ordered)
    assert isinstance(duration, ordered)