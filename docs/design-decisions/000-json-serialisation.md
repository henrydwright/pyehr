## 000: How should JSON serialisation be implemented

**Date:** 2025-11-03

**Status:** Accepted

As part of implementation the specification there is a need to be able to turn the classes of the OpenEHR resource model into JSON. This allows the contents to be communicated over the API.

The criteria for the design was that it must work well with inheritance (to prevent subclasses needlessly implementing methods partially implemented in superclasses) and provide a method on each class to be called to turn it into JSON at any time.

Two implementations of this were considered:

1. Implement an `as_json` in `AnyClass` so all classes of OpenEHR object will always have a JSON serialisation but emit a warning for ones where it is done without a schema
2. Create a new interface `IJsonSerialisable` and apply it only to classes which have a JSON ITS schema representation

### Option 1 (method on AnyClass)
Pros:
* All OpenEHR specification classes can always be serialised to JSON
* Can easily adapt to future ITS changes as the JSON schemas develop

Cons:
* Higher likelihood that things will end up being serialised (and later deserialised) which shouldn't be (e.g. where the schema says a string but the internal representation is a class)

### Option 2 (interface)
Pros:
* Never serialise something which doesn't have a valid schema so ensures all JSON emitted by the library is valid

Cons:
* Higher likelihood that some class implementations will forget to add the interface and thus valid classes may not have a JSON serialisation

### Conclusion
I picked Option 1 and hence all subclasses of `AnyClass`, which should be all OpenEHR specification classes, have an `as_json()` method which can be called to turn them into JSON.

Where a schema does not exist for non-abstract classes, a `RuntimeWarning` will be emitted.