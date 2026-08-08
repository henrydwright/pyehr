# pyehr - a Python implementation of the openEHR® standard

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/henrydwright/pyehr/python-app.yml)

pyehr (on pypi, pyehr-openehr) is an open source Python implementation of the [openEHR® specification](https://specifications.openehr.org/start) from the ground up in pure Python.

⚠️ **Warning:** pyehr is under active development and no stable release is available. Though some parts of the `core` are stable enough, both client and server are liable to change substantially.

pyehr is formed of three parts:
* core - implementation of object model of BASE, RM, AM, etc. in Python
* client - used for interacting with OpenEHR REST API servers
* server - basic Flask-based implementation of the server standard

## pyehr.core
pyehr provides an implementation of the following parts of the specification which are used by both the client and the server, and many users may wish to use in a standalone manner.

Features:

* Work in the RM natively in Python with validation of invariants

```python

text = DVText(
    value="Hello, world!",
    language=CodePhrase(
        terminology_id=TerminologyID("ISO_639-1"),
        code_string="en-gb",
        preferred_term="English (United Kingdom)"
    )
)
```

* Serialise all classes to spec-compliant JSON (with '_type' markers)

```python
print(json.dumps(text.as_json(), indent=1))
```
```json
{
 "_type": "DV_TEXT",
 "value": "Hello, world!",
 "language": {
  "_type": "CODE_PHRASE",
  "terminology_id": {
   "_type": "TERMINOLOGY_ID",
   "value": "ISO_639-1"
  },
  "code_string": "en-gb",
  "preferred_term": "English (United Kingdom)"
 }
}
```

* Use methods as described in the spec across classes
```python
from pyehr.core.rm.data_types.quantity.date_time import DVDate, DVDuration

start_date = DVDate("2026-05-07")
duration = DVDuration("P1Y2M6D")
new_date = start_date + duration
print(str(new_date)) 
```

* Convert seamlessly between ADL v1.4 (read only) and XML and JSON versions of Archetypes
```python
from xml.etree import ElementTree as ET
import json

from pyehr.core.its.adl14 import decode_adl14
from pyehr.core.am.aom14.archetype import Archetype

with open("/path/to/file.adl14") as adl_f:
    arch : Archetype = decode_adl14(adl_f.read())

    xml_version = arch.as_xml()
    with open("/path/to/file.xml", "w") as xml_f:
        ET.indent(xml_version)
        xml_f.write(ET.tostring(xml_version, encoding="unicode"))

    json_version = arch.as_json()
    with open("/path/to/file.json", "w") as json_f:
        json_f.write(json.dumps(json_version, indent=1))
```

### Support level

|Specification part|Status|
|-|-|
|Base model (BASE)|✅ Complete |
|Reference model (RM)|✅ Complete (aside from rm.extract and rm.integration) |
|Implementation technology (ITS) - JSON|✅ Serialisation and deserialisation complete and stable for all implemented classes |
| Archetype model (AOM v1.4 and OPT v1.4) | 🟠 Partial implementation for serialisation/deserialisation but methods unimplemented |
| Archetype model (ADL v1.4) | 🟠 Partial support for parsing ADL v1.4 files (aside from rules and annotations sections). Output in ADL v1.4 not supported.
|Implementation technology (ITS) - XML|🟠 Supported for parsing and serialising AOM v1.4 archetypes and templates, limited support elsewhere |
| Archetype model (AOM v2 or ADL v2) | ❌ Unsupported |

## pyehr.client
pyehr provides both a transactional REST API client as well as a more sophisticated client for working more easily with versioned objects.

Features:
* Transactional clients for /ehr and /demographic endpoints.

```python
from pyehr.client.ehr import OpenEHREHRRestClient, OpenEHRRestClientResponse

client = OpenEHREHRRestClient(
    base_url="https://sandbox.ehrbase.org/ehrbase/rest/openehr/v1"
)

response : OpenEHRRestClientResponse = client.ehr.create_ehr()

print(response.pyehr_obj[0].as_json())
```

* More object-oriented client for working with versioned objects more natively

```python
from pyehr.client.change_control import VersionedStoreClient

store = VersionedStoreClient(
    base_url="http://localhost:5000"
)

p1 = ...

log.info("Create PERSON in store")
object_version_id, contribution, versioned_object = store.create(
    obj=p1,
    owner_id=ObjectRef("local", "EHR", GenericID("null", "null")),
    committer=PartySelf(),
    lifecycle_state=VersionLifecycleState.INCOMPLETE
)
```

## pyehr.server
pyehr provides an under-development Flask-based Clinical Data Repository server with accompanying database and authentication backends.

## Disclaimer
openEHR® is the registered trademark of the openEHR Foundation and is used with the permission of openEHR International. Use of the trademark does not constitute endorsement of this product by openEHR International or openEHR Foundation.