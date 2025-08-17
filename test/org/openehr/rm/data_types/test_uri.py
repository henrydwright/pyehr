import pytest

from org.openehr.rm.data_types.uri import DVUri

def test_dv_uri_accepts_only_valid_uris():
    # all these should be OK
    u = DVUri("foo://example.com:8042/over/there?name=ferret#nose")
    u = DVUri("urn:example:animal:ferret:nose")
    # allow uris which contain characters not normally allowed (e.g. space)
    u = DVUri("https://example.com/page.php?query='hello world'")

    # these aren't URIs
    with pytest.raises(ValueError):
        u = DVUri("::::::")
    with pytest.raises(ValueError):
        u = DVUri("hello world!")
    with pytest.raises(ValueError):
        u = DVUri("")

# two test URIs taken directly from RFC 3986
t1 = DVUri("foo://example.com:8042/over/there?name=ferret#nose")
t2 = DVUri("urn:example:animal:ferret:nose")

def test_dv_uri_scheme():
    assert t1.scheme() == "foo"
    assert t2.scheme() == "urn"

def test_dv_uri_path():
    assert t1.path() == "/over/there"
    assert t2.path() == "example:animal:ferret:nose"

def test_dv_uri_fragment():
    assert t1.fragment_id() == "nose"
    assert t2.fragment_id() == ""

def test_dv_uri_query():
    assert t1.query() == "name=ferret"
    assert t2.query() == ""