from abc import ABC, abstractmethod
from typing import Optional
import re

from org.openehr.base.foundation_types import AnyClass

class UID(AnyClass, ABC):
    """Abstract parent of classes representing unique identifiers 
    which identify information entities in a durable way. UIDs only ever 
    identify one IE in time or space and are never re-used."""

    _value : str

    def _get_value(self):
        return self._value

    value = property(fget=_get_value)

    def __str__(self):
        return self.value

    @abstractmethod
    def _is_UID_format_valid(self, value : str):
        pass

    def __init__(self, value : str, **kwargs):
        if self._is_UID_format_valid(value):
            self._value = value
        else:
            raise ValueError("Invalid UID format")
        super().__init__(**kwargs)

    def from_unknown_uid_type(value : str) -> 'UID':
        """Create a new UID which is either a OID, UUID or Internet ID without
        prior knowledge of which one is being passed in. Raises `ValueError` if
        it does not fit any valid UID."""

        if re.match(ISOOID.ISO_OID_REGEX, value) is not None:
            return ISOOID(value)
        elif re.match(UUID.UUID_REGEX, value) is not None:
            return UUID(value)
        elif re.match(InternetID.INTERNET_ID_REGEX, value) is not None:
            return InternetID(value)
        else:
            raise ValueError("Given format was neither OID, UUID or Internet ID")

    def is_equal(self, other) -> bool:
        return (
            type(self) == type(other) and
            self.value == other.value
            )

class ISOOID(UID):
    """Model of ISO's Object Identifier (oid) as defined by the standard 
    ISO/IEC 8824. Oids are formed from integers separated by dots. Each 
    non-leaf node in an Oid starting from the left corresponds to an assigning 
    authority, and identifies that authority's namespace, inside which the 
    remaining part of the identifier is locally unique."""
    ISO_OID_REGEX = "^([0-2])((\\.0)|(\\.[1-9][0-9]*))*$"

    def _is_UID_format_valid(self, value: str):
        return re.match(ISOOID.ISO_OID_REGEX, value) or False

class UUID(UID):
    """Model of the DCE Universal Unique Identifier or UUID 
    which takes the form of hexadecimal integers separated by 
    hyphens, following the pattern 8-4-4-4-12 as defined by the 
    Open Group, CDE 1.1 Remote Procedure Call specification, Appendix A. 
    
    Also known as a GUID."""
    UUID_REGEX = "^(?:(?:[0-9a-fA-F]){8}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){12})$"

    def _is_UID_format_valid(self, value: str):
        return re.match(UUID.UUID_REGEX, value) or False
    
class InternetID(UID):
    """Model of a reverse internet domain, as used to uniquely identify 
    an internet domain. In the form of a dot-separated string in the 
    reverse order of a domain name, specified by [IETF RFC 1034](https://www.rfc-editor.org/info/rfc1034)."""
    INTERNET_ID_REGEX = "^(?=.{1,253})(?!.*--.*)((?:(?!-)(?![0-9])[a-zA-Z0-9-]{1,63}(?<!-)\\.){1,}(?:(?!-)[a-zA-Z0-9-]{1,63}(?<!-)))"

    def _is_UID_format_valid(self, value: str):
        return re.match(InternetID.INTERNET_ID_REGEX, value) or False

class ObjectID(AnyClass):
    """Ancestor class of identifiers of informational objects. Ids may 
    be completely meaningless, in which case their only job is to refer 
    to something, or may carry some information to do with the identified object.
    
    Object ids are used inside an object to identify that object. To identify another 
    object in another service, use an OBJECT_REF, or else use a UID for local objects 
    identified by UID. If none of the subtypes is suitable, direct instances of this 
    class may be used."""

    _value : str

    def _get_value(self):
        return self._value
    
    value = property(
        fget=_get_value
    )

    def __init__(self, value : str, **kwargs):
        self._value = value
        super().__init__(**kwargs)

    def is_equal(self, other) -> bool:
        return (
            type(self) == type(other) and
            self.value.lower() == other.value.lower()
            )
    
class UIDBasedID(ObjectID):
    """Abstract model of UID-based identifiers consisting of a root part and an 
    optional extension; lexical form: `root '::' extension`."""

    _root : UID
    _extension : str = ""

    def __init__(self, value: str, **kwargs):
        root = ""
        extension = ""
        if "::" in value:
            root = value.split("::")[0]
            extension = value[value.index("::")+2:]
        else:
            root = value

        try:
            self._root = UID.from_unknown_uid_type(root)
            self._extension = extension
        except ValueError:
            raise ValueError("Root was not a valid UID (OID, UUID or Internet ID)")
        

        super().__init__(value, **kwargs)

    def root(self) -> UID:
        """The identifier of the conceptual namespace in which the object exists, 
        within the identification scheme. Returns the part to the left of the 
        first '::' separator, if any, or else the whole string."""
        return self._root

    def extension(self) -> str:
        """Optional local identifier of the object within the context of the root 
        identifier. Returns the part to the right of the first '::' separator if any, 
        or else an empty string."""
        return self._extension

    def has_extension(self) -> bool:
        """True is extension is not empty"""
        return self._extension != ""

class HierObjectID(UIDBasedID):
    """Concrete type corresponding to hierarchical identifiers of the form defined 
    by UIDBasedID."""
    pass

class VersionTreeID(AnyClass):
    """Version tree identifier for one version. 
    Lexical form: `trunk_version [ '.' branch_number '.' branch_version ]`"""
    VERSION_TREE_ID_REGEX = "^([1-9][0-9]*)(\\.[1-9][0-9]*\\.[1-9][0-9]*)?$"


    _trunk_version : str
    _branch_number : Optional[str] = None
    _branch_version : Optional[str] = None

    def _get_value(self):
        if self._branch_number is not None:
            return f"{self._trunk_version}.{self._branch_number}.{self._branch_version}"
        else:
            return self._trunk_version
    
    value = property(
        fget=_get_value
    )

    def __str__(self):
        return self.value

    def __init__(self, value: str, **kwargs):
        if re.match(VersionTreeID.VERSION_TREE_ID_REGEX, value) is None:
            raise ValueError("Version Tree ID was not of the format `trunk_version [ '.' branch_number '.' branch_version ]`")
        
        parts = re.split(VersionTreeID.VERSION_TREE_ID_REGEX, value)

        self._trunk_version = parts[1]
        if parts[2] is not None:
            branch_parts = parts[2].split(".")
            self._branch_number = branch_parts[1]
            self._branch_version = branch_parts[2]
        
        super().__init__(**kwargs)

    def is_equal(self, other) -> bool:
        return (
            type(self) == type(other) and
            self.value == other.value
        )
    
    def trunk_version(self) -> str:
        """Trunk version number; numbering starts at 1."""
        return self._trunk_version

    def is_branch(self) -> bool:
        """True if this version identifier represents a branch, i.e. has 
        branch_number and branch_version parts."""
        return self._branch_number is not None

    def branch_number(self) -> Optional[str]:
        """Number of branch from the trunk point; numbering starts at 1."""
        return self._branch_number

    def branch_version(self) -> Optional[str]:
        """Version of the branch; numbering starts at 1."""
        return self._branch_version

class ObjectVersionID(UIDBasedID):
    """Globally unique identifier for one version of a versioned object; 
    lexical form: `object_id '::' creating_system_id '::' version_tree_id`."""

    _creating_system_id : UID
    _version_tree_id : VersionTreeID

    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)
        if not self.has_extension() or not "::" in self.extension():
            raise ValueError("Object Version ID must be of the form `object_id '::' creating_system_id '::' version_tree_id`")
        creating_system_id = self._extension.split("::")[0]
        version_tree_id = self._extension.split("::")[1]
        try:
            self._creating_system_id = UID.from_unknown_uid_type(creating_system_id)
            self._version_tree_id = VersionTreeID(version_tree_id)
        except ValueError:
            raise ValueError("Either the creating system ID was not a valid UID, or version tree ID not a valid version tree ID")
        
    def object_id(self) -> UID:
        """Unique identifier for logical object of which this identifier 
        identifies one version; normally the object_id will be the unique 
        identifier of the version container containing the version referred 
        to by this ObjectVersionID instance."""
        return self.root()

    def creating_system_id(self) -> UID:
        """Identifier of the system that created the Version corresponding 
        to this Object version id."""
        return self._creating_system_id

    def version_tree_id(self) -> VersionTreeID:
        """Tree identifier of this version with respect to other versions 
        in the same version tree, as either 1 or 3 part dot-separated numbers, 
        e.g. 1 , 2.1.4 ."""
        return self._version_tree_id

    def is_branch(self) -> bool:
        """True if this version identifier represents a branch."""
        return self._version_tree_id.is_branch()
    
class ArchetypeID(ObjectID):
    """Identifier for archetypes. Ideally these would identify globally unique archetypes.
    
    Lexical form: `rm_originator '-' rm_name '-' rm_entity '.' concept_name { '-' specialisation }* '.v' number`."""
    
    ARCHETYPE_ID_REGEX = "^(([a-zA-Z][a-zA-Z0-9_]*)-([a-zA-Z][a-zA-Z0-9_]*)-([a-zA-Z][a-zA-Z0-9_]*))\\.(([a-zA-Z][a-zA-Z0-9_]*)(-[a-zA-Z][a-zA-Z0-9_]*)?)\\.(v[0-9][0-9]*)$"

    _rm_originator : str
    _rm_name : str
    _rm_entity : str
    _concept_name : str
    _specialisation : Optional[str] = None
    _version_id : str

    def __init__(self, value: str, **kwargs):
        if re.match(ArchetypeID.ARCHETYPE_ID_REGEX, value) is None:
            raise ValueError("Archetype ID must be of the lexical form `rm_originator '-' rm_name '-' rm_entity '.' concept_name { '-' specialisation }* '.v' number`.")
        
        parts = re.split(ArchetypeID.ARCHETYPE_ID_REGEX, value)
        self._rm_originator = parts[2]
        self._rm_name = parts[3]
        self._rm_entity = parts[4]
        self._concept_name = parts[5]
        if parts[7] is not None:
            self._specialisation = parts[7][1:]
        self._version_id = parts[8][1:]
        super().__init__(value, **kwargs)

    def qualified_rm_entity(self) -> str:
        """Globally qualified reference model entity, e.g. `openehr-EHR-OBSERVATION`."""
        return f"{self._rm_originator}-{self._rm_name}-{self._rm_entity}"

    def domain_concept(self) -> str:
        """Name of the concept represented by this archetype, including specialisation, 
        e.g. `Biochemistry_result-cholesterol`."""
        return self._concept_name

    def rm_originator(self) -> str:
        """Organisation originating the reference model on which this archetype is based, 
        e.g. openehr, cen, hl7."""
        return self._rm_originator

    def rm_name(self) -> str:
        """Name of the reference model, e.g. rim, ehr_rm, en13606."""
        return self._rm_name

    def rm_entity(self) -> str:
        """Name of the ontological level within the reference model to which this archetype 
        is targeted, e.g. for openEHR, folder , composition , section , entry."""
        return self._rm_entity

    def specialisation(self) -> str:
        """Name of specialisation of concept, if this archetype is a specialisation of another 
        archetype, e.g. cholesterol."""
        if self._specialisation is None:
            return ""
        else:
            return self._specialisation

    def version_id(self) -> str:
        """Version of this archetype."""
        return self._version_id

class TemplateID(ObjectID):
    """Identifier for templates. Lexical form to be determined."""
    pass

class TerminologyID(ObjectID):
    """Identifier for terminologies such as accessed via a terminology 
    query service. In this class, the value attribute identifies the 
    Terminology in the terminology service, e.g. SNOMED-CT. A terminology 
    is assumed to be in a particular language, which must be explicitly specified.

    The value if the id attribute is the precise terminology id identifier, including 
    actual release (i.e. actual version), local modifications etc; e.g. ICPC2.

    Lexical form: `name [ '(' version ')' ]`."""

    TERMINOLOGY_ID_REGEX = "^([a-zA-Z][a-zA-Z0-9_\\-\\/+]*)(\\([a-zA-Z0-9_\\-\\/+]*\\))?$"

    _name : str
    _version : Optional[str]

    def __init__(self, value: str, **kwargs):
        if re.match(TerminologyID.TERMINOLOGY_ID_REGEX, value) is None:
            raise ValueError("Invalid syntax for terminology ID")
        parts = re.split(TerminologyID.TERMINOLOGY_ID_REGEX, value)
        self._name = parts[1]
        if parts[2] is not None:
            self._version = parts[2].replace("(", "").replace(")", "")
        super().__init__(value, **kwargs)

    def name(self) -> str:
        """Return the terminology id (which includes the version in some cases). 
        Distinct names correspond to distinct (i.e. non-compatible) terminologies. 
        Thus the names ICD10AM and ICD10 refer to distinct terminologies."""
        return self._name

    def version_id(self) -> str:
        """Version of this terminology, if versioning supported, else the empty string."""
        if self._version is None:
            return ""
        else:
            return self._version

class GenericID(ObjectID):
    """Generic identifier type for identifiers whose format is otherwise 
    unknown to openEHR. Includes an attribute for naming the identification 
    scheme (which may well be local)."""

    _scheme : str

    def _get_scheme(self) -> str:
        return self._scheme
    
    scheme = property(
        fget=_get_scheme
    )
    """Name of the scheme to which this identifier conforms. Ideally this name will 
    be recognisable globally but realistically it may be a local ad hoc scheme whose 
    name is not controlled or standardised in any way."""

    def __init__(self, value: str, scheme: str, **kwargs):
        self._scheme = scheme
        super().__init__(value, **kwargs)

    def is_equal(self, other) -> bool:
        return (
            self._scheme == other._scheme and
            super().is_equal(other)
            )

class ObjectRef(AnyClass):
    """Class describing a reference to another object, which may exist locally or 
    be maintained outside the current namespace, e.g. in another service. Services 
    are usually external, e.g. available in a LAN (including on the same host) or 
    the internet via Corba, SOAP, or some other distributed protocol. However, in 
    small systems they may be part of the same executable as the data containing 
    the Id."""

    NAMESPACE_REGEX = "^[a-zA-Z][a-zA-Z0-9_.:\\/&?=+-]*$"

    _namespace : str
    _type : str
    _id : ObjectID

    def _get_namespace(self) -> str:
        return self._namespace
    
    def _get_type(self) -> str:
        return self._type
    
    def _get_id(self) -> ObjectID:
        return self._id
    
    namespace = property(
        fget=_get_namespace
    )
    """Namespace to which this identifier belongs in the local system context (and possibly in any 
    other openEHR compliant environment) e.g. terminology , demographic. These names are not 
    yet standardised. Legal values for namespace are:
    * `"local"`
    * `"unknown"`
    * `a string matching the standard regex [a-zA-Z][a-zA-Z0-9_.:\\/&?=+-]*`.
    
    Note that the first two are just special values of the regex, and will be matched by it."""

    ref_type = property(
        fget=_get_type
    )
    """Name of the class (concrete or abstract) of object to which this identifier type refers, 
    e.g. `PARTY`, `PERSON`, `GUIDELINE` etc. These class names are from the relevant reference model. 
    The type name `ANY` can be used to indicate that any type is accepted (e.g. if the type is 
    unknown)."""

    id = property(
        fget=_get_id
    )
    """Globally unique id of an object, regardless of where it is stored."""

    def __init__(self, namespace: str, ref_type: str, id: ObjectID, **kwargs):
        if re.match(ObjectRef.NAMESPACE_REGEX, namespace) is None:
            raise ValueError("Object reference namespace must conform to regular expression `^[a-zA-Z][a-zA-Z0-9_.:\\/&?=+-]*$`")
        self._namespace = namespace
        self._type = ref_type
        self._id = id
        super().__init__(**kwargs)

    def is_equal(self, other) -> bool:
        return (
            type(self) == type(other) and
            self._namespace == other._namespace and
            self._type == other._type and
            self._id.is_equal(other._id)
        )

class PartyRef(ObjectRef):
    """Identifier for parties in a demographic or identity service. There are typically a 
    number of subtypes of the `PARTY` class, including `PERSON`, `ORGANISATION`, etc. Abstract 
    supertypes are allowed if the referenced object is of a type not known by the current 
    implementation of this class (in other words, if the demographic model is changed by 
    the addition of a new `PARTY` or `ACTOR` subtypes, valid `PARTY_REF`s can still be 
    constructed to them)."""

    def __init__(self, namespace: str, type: str, id: ObjectID, **kwargs):
        if type not in {"PERSON", "ORGANISATION", "GROUP", "AGENT", "ROLE", "PARTY", "ACTOR"}:
            raise ValueError("A party reference must refer to one of the following types: PERSON, ORGANISATION, GROUP, AGENT, ROLE, PARTY, ACTOR")
        super().__init__(namespace, type, id, **kwargs)

class LocatableRef(ObjectRef):
    """Purpose Reference to a `LOCATABLE` instance inside the top-level content structure 
    inside a `VERSION<T>`; the path attribute is applied to the object that `VERSION.data`
    points to."""

    _path : Optional[str]

    def _get_path(self):
        return self._path
    
    path = property(
        fget=_get_path
    )
    """The path to an instance in question, as an absolute path with respect to the object 
    found at VERSION.data. An empty path means that the object referred to by id being 
    specified."""

    def __init__(self, namespace: str, type: str, id: UIDBasedID, path : Optional[str] = None, **kwargs):
        raise NotImplementedError("Locatable refs are not yet implemented (as I don't understand them!)")
        self._path = path
        super().__init__(namespace, type, id, **kwargs)

    def as_uri(self) -> str:
        """A URI form of the reference, created by concatenating the following:
        * scheme, e.g. ehr:, derived from namespace
        * id.value
        * / + path, where path is non-empty"""
        raise NotImplementedError("Locatable refs are not yet implemented (as I don't understand them!)")
