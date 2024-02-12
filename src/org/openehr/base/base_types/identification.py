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
            self.value == other.value
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
    
