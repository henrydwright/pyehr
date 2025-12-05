# Primitive Types in Python

openEHR BASE specification demands a number of primitive types, from which other types can be built.

## Any
All non-primitive sub-classes should inherit from the `org.openehr.base.foundation_types.AnyClass`.

### Boolean
Use built-in type `bool`

## Ordered
Demands existance of several methods, each of which is mapped to a Python dunder method:
* less_than - `__lt__`
* less_than_or_equal - `__le__`
* greater_than - `__gt__`
* greater_than_or_equal - `__ge__`


#### Octet
Use numpy type `np.int8`

#### Character
Use numpy type `np.uint8`

#### String
Use built-in type `str`

#### Uri
Use the class provided in `org.openehr.base.foundation_types.primitive_types.Uri` 

## Numeric
Demands existance of several methods, each of which is mapped to a Python dunder method:
* add - `__add__`
* subtract - `__sub__`
* multiply - `__mul__`
* divide - `__truediv__`
* exponent - `__pow__`
* negative - `__neg__`

### Ordered_Numeric

#### Integer
Use numpy type `np.int32` to constrain to 32 bits.

#### Integer64
Use numpy type `np.int64` to constrain to 64 bits.

#### Real
Use numpy type `np.float32` to constrain to 32 bits.

#### Double
Use numpy type `np.float64` to constrain ot 64 bits.
