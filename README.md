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

|Specification part|Status|
|-|-|
|Base model (BASE)|✅ Complete |
|Reference model (RM)|✅ Complete (aside from rm.extract and rm.integration) |
|Implementation technology (ITS) - JSON|✅ Serialisation complete for all implemented classes, but deserialisation still under development |
| Archetype model (AOM v1.4 and OPT v1.4) | 🟠 Partial implementation for serialisation/deserialisation but methods unimplemented |
|Implementation technology (ITS) - XML|🟠 Some support for parsing AOM v1.4 archetypes and templates, limited support elsewhere |
| Archetype model (AOM v2) | ❌ Unsupported |
| Archetype model (ADL v1.4 or ADL v2) | ❌ Unsupported |

## pyehr.client
pyehr provides both a transactional REST API client as well as a more sophisticated client for working more easily with versioned objects.

## pyehr.server
pyehr provides an under-development Flask-based server with accompanying database and authentication backends.

## Disclaimer
openEHR® is the registered trademark of the openEHR Foundation and is used with the permission of openEHR International. Use of the trademark does not constitute endorsement of this product by openEHR International or openEHR Foundation.