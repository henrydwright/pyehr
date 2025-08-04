from abc import ABC, abstractmethod
from typing import Optional

from org.openehr.base.foundation_types.any import AnyClass
from org.openehr.base.foundation_types.structure import is_equal_value
from org.openehr.base.base_types.identification import UUID
from org.openehr.base.foundation_types.terminology import TerminologyCode

class ResourceDescription(AnyClass):
    """Defines the descriptive meta-data of a resource."""
    
    original_author : dict[str, str]
    """Original author of this resource, with all relevant details, including organisation."""

    original_namespace : Optional[str] = None
    """Namespace of original author's organisation, in reverse internet form, if applicable."""

    original_publisher : Optional[str] = None
    """Plain text name of organisation that originally published this artefact, if any."""

    other_contributors : Optional[list[str]] = None
    """Other contributors to the resource, each listed in "name <email>" form."""

    lifecycle_state : TerminologyCode
    """Lifecycle state of the resource, typically including states such as: initial, in_development, in_review, published, superseded, obsolete."""

    parent_resource : 'AuthoredResource'
    """Reference to owning resource."""

    custodian_namespace : Optional[str] = None
    """Namespace in reverse internet id form, of current custodian organisation."""

    custodian_organisation : Optional[str] = None
    """Plain text name of current custodian organisation."""

    copyright : Optional[str] = None
    """Optional copyright statement for the resource as a knowledge resource."""

    licence: Optional[str] = None
    """Licence of current artefact, in format \"short licence name \<URL of licence\>\", e.g. \"Apache 2.0 License <http://www.apache.org/licenses/LICENSE-2.0.html>\""""

    ip_acknowledgements: Optional[dict[str, str]] = None
    """
    List of acknowledgements of other IP directly referenced in this archetype, typically terminology codes, ontology ids etc. Recommended keys are the widely known name or namespace for the IP source, as shown in the following example:
    ```
    ip_acknowledgements = <
        ["loinc"] = <"This content from LOINC® is copyright © 1995 Regenstrief Institute, Inc. and the LOINC Committee, and available at no cost under the license at http://loinc.org/terms-of-use">
        ["snomedct"] = <"Content from SNOMED CT® is copyright © 2007 IHTSDO <ihtsdo.org>">
    >
    ```
    """

    references: Optional[dict[str, str]] = None
    """List of references of material on which this artefact is based, as a keyed list of strings. The keys should be in a standard citation format."""

    resource_package_uri: Optional[str] = None
    """URI of package to which this resource belongs."""

    conversion_details: Optional[dict[str, str]] = None
    """
    Details related to conversion process that generated this model from an original, if relevant, as a list of name/value pairs. Typical example with recommended tags:
    ```
    conversion_details = <
        ["source_model"] = <"CEM model xyz <http://location.in.clinicalelementmodels.com>">
        ["tool"] = <"cem2adl v6.3.0">
        ["time"] = <"2014-11-03T09:05:00">
    >
    ```
    """

    other_details: Optional[dict[str, str]] = None
    """Additional non-language-sensitive resource meta-data, as a list of name/value pairs."""

    # TODO: implement this as a property to ensure it can only be added to in a way that doesn't break language invariants
    details: Optional[dict[str,'ResourceDescriptionItem']] = None
    """Details of all parts of resource description that are natural language-dependent, keyed by language code."""

    def __init__(self, original_author: dict[str, str], lifecycle_state: TerminologyCode, parent_resource:'AuthoredResource'):
        self.original_author = original_author
        self.lifecycle_state = lifecycle_state
        self.parent_resource = parent_resource
        super().__init__()

    def is_equal(self, other: 'ResourceDescription'):
        return (
            type(self) == type(other) and
            is_equal_value(self.original_author, other.original_author) and
            is_equal_value(self.original_namespace, other.original_namespace) and
            is_equal_value(self.original_publisher, other.original_publisher) and
            is_equal_value(self.other_contributors, other.other_contributors) and
            is_equal_value(self.lifecycle_state, other.lifecycle_state) and
            (self.parent_resource == other.parent_resource) and
            is_equal_value(self.custodian_namespace, other.custodian_namespace) and
            is_equal_value(self.custodian_organisation, other.custodian_organisation) and
            is_equal_value(self.copyright, other.copyright) and
            is_equal_value(self.licence, other.licence) and
            is_equal_value(self.ip_acknowledgements, other.ip_acknowledgements) and
            is_equal_value(self.references, other.references) and
            is_equal_value(self.resource_package_uri, other.resource_package_uri) and
            is_equal_value(self.conversion_details, other.conversion_details) and
            is_equal_value(self.other_details, other.other_details) and
            is_equal_value(self.details, other.details)
        )


class ResourceAnnotations(AnyClass):
    """Class to store annotations for `AuthoredResource`"""
    
    documentation: dict[str, dict[str, dict[str, str]]]

    def __init__(self, documentation: dict[str, dict[str, dict[str, str]]]):
        self.documentation = documentation
        super().__init__()

    def is_equal(self, other: 'ResourceAnnotations'):
        return (
            type(self) == type(other) and
            is_equal_value(self.documentation, other.documentation)
        )

class TranslationDetails(AnyClass):
    """Class providing details of a natural language translation."""
    
    language : TerminologyCode
    """Language of the translation, coded using ISO 639-1 (2 character) language codes."""

    author : dict[str, str]
    """Primary translator name and other demographic details."""

    accreditation : Optional[str] = None
    """Accreditation of primary translator or group, usually a national translator’s registration or association membership id."""

    other_details : Optional[dict[str, str]] = None
    """Any other meta-data."""

    version_last_translated : Optional[str] = None
    """Version of this resource last time it was translated into the language represented by this TRANSLATION_DETAILS object."""

    other_contributors : Optional[list[str]] = None
    """Additional contributors to this translation, each listed in the preferred format of the relevant organisation for the artefacts in question. A typical default is "name <email>" if nothing else is specified."""

    def __init__(self, language : TerminologyCode, author : dict[str, str]):
        self.language = language
        self.author = author
        super().__init__()

    def is_equal(self, other: 'TranslationDetails'):
        return (
            type(self) == type(other) and
            is_equal_value(self.language, other.language) and
            is_equal_value(self.author, other.author) and
            is_equal_value(self.accreditation, other.accreditation) and
            is_equal_value(self.other_details, other.other_details) and
            is_equal_value(self.version_last_translated, other.version_last_translated) and
            is_equal_value(self.other_contributors, other.other_contributors)
        )


class AuthoredResource(AnyClass, ABC):
    """Abstract idea of an online resource created by a human author."""
    
    uid : Optional[UUID] = None
    """Unique identifier of the family of archetypes having the same interface identifier (same major version)."""

    original_language : TerminologyCode
    """Language in which this resource was initially authored. Although there is no language primacy of resources overall, the language of original authoring is required to ensure natural language translations can preserve quality. Language is relevant in both the description and ontology sections."""

    _description : Optional[ResourceDescription] = None
    """Description and lifecycle information of the resource."""

    is_controlled : Optional[bool] = None
    """True if this resource is under any kind of change control (even file copying), in which case revision history is created."""

    annotations : Optional[ResourceAnnotations] = None
    """Annotations on individual items within the resource, keyed by path. The inner table takes the form of a Hash table of String values keyed by String tags."""

    _translations : Optional[dict[str, TranslationDetails]] = None
    """List of details for each natural translation made of this resource, keyed by language code. For each translation listed here, there must be corresponding sections in all language-dependent parts of the resource. The original_language does not appear in this list."""

    def __init__(self, original_language: TerminologyCode):
        self.original_language = original_language

    def is_equal(self, other: 'AuthoredResource'):
        return (
            type(self) == type(other) and
            is_equal_value(self.uid, other.uid) and
            is_equal_value(self.original_language, other.original_language) and
            is_equal_value(self._description, other._description) and
            is_equal_value(self.is_controlled, other.is_controlled) and
            is_equal_value(self.annotations, other.annotations) and
            is_equal_value(self._translations, other._translations)
        )

    @abstractmethod
    def current_revision(self) -> str:
        """Most recent revision in revision_history if `is_controlled` else \"(uncontrolled)\".
        
        Implementations should satisfy invariants:
        - Current_revision_valid: `(current_revision /= Void and not is_controlled) implies current_revision.is_equal ("(uncontrolled)")`
        - Revision_history_valid: `is_controlled xor revision_history = Void`"""
        pass

    def languages_available(self) -> list[str]:
        """Total list of languages available in this resource, derived from original_language and translations."""
        return_list = [self.original_language.code_string]

        if self.translations is not None:
            return_list += self.translations.keys()
        
        return return_list
    
    # implementation as properties allows us to satisfy Translations_valid and Description_valid invariants
    @property
    def description(self):
        return self._description
    
    @property
    def translations(self):
        return self._translations
    
    def add_translation(self, translation_details: TranslationDetails, translated_resource_description: 'ResourceDescriptionItem'):
        if self._description is None:
            raise Exception(f"Cannot add a translation to an object without a description to translate details of (description was None)")
        
        if self._description.details is None:
            raise Exception(f"Cannot add a translation to an object without a description that has translatable details (description.details was None)")

        if translation_details.language.code_string != translated_resource_description.language.code_string:
            raise ValueError(f"Language of translation details ({translation_details.language.code_string}) is not the same as the translated resource description ({translated_resource_description.language.code_string})")

        if translation_details.language.code_string == self.original_language.code_string:
            raise ValueError(f"Cannot add a translation for the same language as the original language ({translation_details.language.code_string})")
        
        if self._translations is None:
            self._translations = {}

        self._description.details[translation_details.language.code_string] = translated_resource_description
        self._translations[translation_details.language.code_string] = translation_details

        
    def set_description(self, resource_description : ResourceDescription):
        if self._description is None:
            self._description = resource_description
            return
        
        if resource_description.details is not None:
            # New resource has details
            if self._description.details is None:
                # Current resource does not
                new_description_language_count = len(resource_description.details.keys())
                if new_description_language_count > 1:
                    raise ValueError(f"New resource_description.details has too many languages ({new_description_language_count}) compared to resource (1)")
                elif new_description_language_count == 1:
                    if (self.original_language.code_string not in resource_description.details):
                        raise ValueError(f"New resource_description.details has one language, but this is not the original_language of the resource it describes")
                    else:
                        self._description = resource_description
                elif new_description_language_count == 0:
                    self._description = resource_description
            else:
                # Current resource does
                # -> Check the languages match
                for language in self._description.details.keys():
                    if language not in resource_description.details:
                        raise ValueError(f"New resource_description.details does not include a language that this resource current has ({language})")
        else:
            # New resource does not have details
            if self._description.details is not None:
                # Current resource does
                current_description_language_count = len(self._description.details.keys())
                if current_description_language_count > 1:
                    raise ValueError(f"New resource_description has too few languages (1) compared to resource ({current_description_language_count})")
                else:
                    self._description = resource_description


class ResourceDescriptionItem(AnyClass):
    """Language-specific detail of resource description. When a resource is translated for use in another language environment, each `ResourceDescriptionItem` needs to be copied and translated into the new language."""
    
    language : TerminologyCode
    """The localised language in which the items in this description item are written. Coded using ISO 639-1 (2 character) language codes."""

    purpose : str
    """Purpose of the resource."""

    keywords: Optional[list[str]] = None
    """Keywords which characterise this resource, used e.g. for indexing and searching."""

    use: Optional[str] = None
    """Description of the uses of the resource, i.e. contexts in which it could be used."""

    misuse: Optional[str] = None
    """Description of any misuses of the resource, i.e. contexts in which it should not be used."""

    original_resource_uri: Optional[dict[str, str]] = None
    """URIs of original clinical document(s) or description of which resource is a formalisation, in the language of this description item; keyed by meaning."""

    other_details: Optional[dict[str, str]] = None
    """Additional language-senstive resource metadata, as a list of name/value pairs."""

    def __init__(self, language: TerminologyCode, purpose: str):
        self.language = language
        self.purpose = purpose
        super().__init__()

    def is_equal(self, other: 'ResourceDescriptionItem'):
        return (
            type(self) == type(other) and
            is_equal_value(self.language, other.language) and
            (self.purpose == other.purpose) and
            is_equal_value(self.keywords, other.keywords) and
            is_equal_value(self.use, other.use) and
            is_equal_value(self.misuse, other.misuse) and
            is_equal_value(self.original_resource_uri, other.original_resource_uri) and
            is_equal_value(self.other_details, other.other_details)
        )

