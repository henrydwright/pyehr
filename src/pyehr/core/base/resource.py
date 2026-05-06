from abc import ABC, abstractmethod
from types import NoneType
from typing import Optional
import xml.etree.ElementTree as ET
import warnings

from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.base.base_types.identification import UUID
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.its.xml import IXMLSupport
from pyehr.core.rm.data_types.text import CodePhrase

class ResourceDescription(AnyClass, IXMLSupport):
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
    """Licence of current artefact, in format \"short licence name <URL of licence>\", e.g. \"Apache 2.0 License <http://www.apache.org/licenses/LICENSE-2.0.html>\""""

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

    def __init__(self, 
                 original_author: dict[str, str], 
                 lifecycle_state: TerminologyCode, 
                 details: dict[str, 'ResourceDescriptionItem'],
                 parent_resource: Optional['AuthoredResource'] = None,
                 original_namespace: Optional[str] = None,
                 original_publisher: Optional[str] = None,
                 other_contributors: Optional[list[str]] = None,
                 custodian_namespace: Optional[str] = None,
                 custodian_organisation: Optional[str] = None,
                 copyright: Optional[str] = None,
                 licence: Optional[str] = None,
                 ip_acknowledgements: Optional[dict[str, str]] = None,
                 references: Optional[dict[str, str]] = None,
                 resource_package_uri: Optional[str] = None,
                 conversion_details: Optional[dict[str, str]] = None,
                 other_details: Optional[dict[str, str]] = None):
        self.original_author = original_author
        self.lifecycle_state = lifecycle_state
        if len(details.items()) == 0:
            raise ValueError("details must be provided for at least one language (XML ITS restriction)")
        self.details = details
        self.parent_resource = parent_resource
        self.original_namespace = original_namespace
        self.original_publisher = original_publisher
        self.other_contributors = other_contributors
        self.custodian_namespace = custodian_namespace
        self.custodian_organisation = custodian_organisation
        self.copyright = copyright
        self.licence = licence
        self.ip_acknowledgements = ip_acknowledgements
        self.references = references
        self.resource_package_uri = resource_package_uri
        self.conversion_details = conversion_details
        self.other_details = other_details
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
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Resource/RESOURCE_DESCRIPTION.json
        # TODO: the spec and the JSON schema (as for all resource classes it seems, disagree) so as usual going with the spec
        draft = {
            "_type": "RESOURCE_DESCRIPTION",
            "original_author": self.original_author,
            "lifecycle_state": self.lifecycle_state.code_string
        }
        det_list = []
        for rdi in self.details.values():
            det_list.append(rdi.as_json())
        draft["details"] = det_list

        if self.parent_resource is not None:
            draft["parent_resource"] = self.parent_resource.as_json()
        if self.original_namespace is not None:
            draft["original_namespace"] = self.original_namespace
        if self.original_publisher is not None:
            draft["original_publisher"] = self.original_publisher
        if self.other_contributors is not None:
            draft["other_contributors"] = self.other_contributors
        if self.custodian_namespace is not None:
            draft["custodian_namespace"] = self.custodian_namespace
        if self.custodian_organisation is not None:
            draft["custodian_organisation"] = self.custodian_organisation
        if self.copyright is not None:
            draft["copyright"] = self.copyright
        if self.licence is not None:
            draft["licence"] = self.licence
        if self.ip_acknowledgements is not None:
            draft["ip_acknowledgements"] = self.ip_acknowledgements
        if self.references is not None:
            draft["references"] = self.references
        if self.resource_package_uri is not None:
            draft["resource_package_uri"] = self.resource_package_uri
        if self.conversion_details is not None:
            draft["conversion_details"] = self.conversion_details
        if self.other_details is not None:
            draft["other_details"] = self.other_details

        return draft
    
    def as_xml(self, root_tag = None):
        tag = "resource_description" if root_tag is None else root_tag
        root = ET.Element(tag)
        for (id, value) in self.original_author.items():
            original_author = ET.Element("original_author")
            original_author.attrib["id"] = id
            original_author.text = value
            root.append(original_author)
        if self.other_contributors is not None:
            for other_contrib in self.other_contributors:
                other_contrib_el = ET.Element("other_contributors")
                other_contrib_el.text = other_contrib
                root.append(other_contrib_el)

        # lifecycle_state is a string in v1.0.2, not TERMINOLOGY_CODE
        lf_state = ET.Element("lifecycle_state")
        lf_state.text = self.lifecycle_state.code_string
        root.append(lf_state)

        if self.resource_package_uri is not None:
            rpu = ET.Element("resource_package_uri")
            rpu.text = self.resource_package_uri
            root.append(rpu)
        if self.other_details is not None:
            for (id, value) in self.other_details.items():
                other_detail = ET.Element("other_details")
                other_detail.attrib["id"] = id
                other_detail.text = value
                root.append(other_detail)

        for (_, detail) in self.details.items():
            root.append(detail.as_xml("details"))

        if self.parent_resource is not None:
            root.append(self.parent_resource.as_xml("parent_resource"))
        
        return root
    
    def from_xml(root: ET.Element, **kwargs):
        orig_author_els = root.findall("./original_author")
        orig_author = {}
        for orig_author_el in orig_author_els:
            orig_author[orig_author_el.attrib["id"]] = orig_author_el.text

        other_contrib_els = root.findall("./other_contributors")
        other_contributors = None
        if len(other_contrib_els) > 0:
            other_contributors = []
            for other_contrib_el in other_contrib_els:
                other_contributors.append(other_contrib_el.text)

        lf_state_el = root.find("./lifecycle_state")
        lf_state = TerminologyCode("openehr", lf_state_el.text)

        rpu = root.findtext("./resource_package_uri")

        o_dt_els = root.findall("./other_details")
        other_details = None
        if len(o_dt_els) > 0:
            other_details = {}
            for o_dt_el in o_dt_els:
                other_details[o_dt_el.attrib["id"]] = o_dt_el.text

        det_els = root.findall("./details")
        details = None
        if len(det_els) > 0:
            details = {}
            for det_el in det_els:
                rdi = ResourceDescriptionItem.from_xml(det_el)
                details[rdi.language.code_string] = rdi

        parent_res_el = root.find("./parent_resource")
        parent_resource = None
        # TODO: implement parsing for parent_resource once 
        #        a concrete implementation of AUTHORED_RESOURCE
        #        exists

        return ResourceDescription(
            original_author=orig_author,
            lifecycle_state=lf_state,
            details=details,
            parent_resource=parent_resource,
            original_namespace=None,
            original_publisher=None,
            other_contributors=other_contributors,
            custodian_namespace=None,
            custodian_organisation=None,
            copyright=None,
            licence=None,
            ip_acknowledgements=None,
            references=None,
            resource_package_uri=rpu,
            conversion_details=None,
            other_details=other_details
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

class TranslationDetails(AnyClass, IXMLSupport):
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

    def __init__(self, 
                 language : TerminologyCode, 
                 author : dict[str, str], 
                 accreditation : Optional[str] = None,
                 other_details: Optional[dict[str, str]] = None,
                 version_last_translated: Optional[str] = None,
                 other_contributors: Optional[list[str]] = None):
        self.language = language
        self.author = author
        self.accreditation = accreditation
        self.other_details = other_details
        self.version_last_translated = version_last_translated
        self.other_contributors = other_contributors
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
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Resource/TRANSLATION_DETAILS.json
        # TODO: the JSON schema disagrees with the specification on the properties of the class, go with spec and modify JSON schema
        draft = {
            "_type": "TRANSLATION_DETAILS",
            "language": self.language.as_json(),
            "author": self.author,
        }
        if self.accreditation is not None:
            draft["accreditation"] = self.accreditation
        if self.other_contributors is not None:
            draft["other_details"] = self.other_details
        if self.version_last_translated is not None:
            draft["version_last_translated"] = self.version_last_translated
        if self.other_contributors is not None:
            draft["other_contributors"] = self.other_contributors
        return draft
    
    def as_xml(self, root_tag = None):
        tag = "translation_details" if root_tag is None else root_tag
        root = ET.Element(tag)

        lang_cp = CodePhrase(self.language.terminology_id, self.language.code_string)
        root.append(lang_cp.as_xml("language"))

        for (id, value) in self.author:
            author_el = ET.Element("author")
            author_el.attrib["id"] = id
            author_el.text = value
            root.append(author_el)

        if self.accreditation is not None:
            accred = ET.Element("accreditation")
            accred.text = self.accreditation
            root.append(accred)

        if self.other_contributors is not None:
            for other_contrib in self.other_contributors:
                other_contrib_el = ET.Element("other_contributors")
                other_contrib_el.text = other_contrib
                root.append(other_contrib_el)

        # version_last_translated does not exist in XML v1.0.2

        if self.other_details is not None:
            for (id, value) in self.other_details.items():
                other_detail = ET.Element("other_details")
                other_detail.attrib["id"] = id
                other_detail.text = value
                root.append(other_detail)

        return root
    
    def from_xml(root: ET.Element, **kwargs):
        lang_el = root.find("./language")
        lang : CodePhrase = CodePhrase.from_xml(lang_el)

        author_els = root.findall("./author")
        author = {}
        for author_el in author_els:
            author[author_el.attrib["id"]] = author_el.text

        accred = root.findtext("./accreditation")

        other_contrib_els = root.findall("./other_contributors")
        other_contributors = None
        if len(other_contrib_els) > 0:
            other_contributors = []
            for other_contrib_el in other_contrib_els:
                other_contributors.append(other_contrib_el.text)

        o_dt_els = root.findall("./other_details")
        other_details = None
        if len(o_dt_els) > 0:
            other_details = {}
            for o_dt_el in o_dt_els:
                other_details[o_dt_el.attrib["id"]] = o_dt_el.text

        return TranslationDetails(
            language=TerminologyCode(lang.terminology_id.value, lang.code_string),
            author=author,
            accreditation=accred,
            other_details=other_details,
            version_last_translated=None,
            other_contributors=other_contributors
        )


class AuthoredResource(AnyClass, IXMLSupport):
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

    def __init__(self, 
                 original_language: TerminologyCode, 
                 uid: Optional[UUID] = None,
                 is_controlled: Optional[bool] = None,
                 annotations: Optional[ResourceAnnotations] = None):
        self.original_language = original_language
        self.uid = uid
        self.is_controlled = is_controlled
        self.annotations = annotations

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

    # it seems this relies on revision_history which is not in the spec any more
    #  TODO: report issue for tidying on https://specifications.openehr.org/releases/BASE/Release-1.2.0/resource.html
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

    @abstractmethod
    def as_json(self):
        draft = {
            "original_language": self.original_language.as_json()
        }
        if self.uid is not None:
            draft["uid"] = self.uid.value
        if self._description is not None:
            draft["description"] = self._description
        if self.is_controlled is not None:
            draft["is_controlled"] = self.is_controlled
        if self.annotations is not None:
            draft["annotations"] = self.annotations.as_json()
        if self.translations is not None:
            draft["translations"] = self.translations
        return draft
    
    @abstractmethod
    def as_xml(self, root_tag = None):
        tag = "authored_resource" if root_tag is None else root_tag
        root = ET.Element(tag)
        olang_cp = CodePhrase(self.original_language.terminology_id, self.original_language.code_string)
        root.append(olang_cp.as_xml("original_language"))
        if self.is_controlled is not None:
            is_cont = ET.Element("is_controlled")
            is_cont.text = str(self.is_controlled).lower()
            root.append(is_cont)
        if self._description is not None:
            root.append(self._description.as_xml("description"))
        if self._translations is not None:
            for (_, translation_details) in self._translations:
                root.append(translation_details.as_xml("translations"))
        # this version of rm does not have revision_history
        return root
    
    def extract_xml_elements(root: ET.Element) -> tuple[CodePhrase, Optional[bool], Optional[ResourceDescription], Optional[list[TranslationDetails]]]:
        cphr = CodePhrase.from_xml(root.find("./original_language"))

        is_cont_el = root.findtext("./is_controlled")
        is_cont = None
        if is_cont_el is not None:
            is_cont = (is_cont_el.capitalize() == "True")

        desc_el = root.find("./description")
        desc = None
        if desc_el is not None:
            desc = ResourceDescription.from_xml(desc_el)

        trans_els = root.findall("./translations")
        trans = []
        for trans_el in trans_els:
            trans.append(TranslationDetails.from_xml(trans_el))

        rev_his_el = root.find("./revision_history")
        if rev_his_el != None:
            warnings.warn("REVISION_HISTORY found within AUTHORED_RESOURCE when parsing XML v1.4. Library is on rm v1.10 and does not support REVISION_HISTORY in AUTHORED_RESOURCE. Ignoring.")
            
        return (cphr, is_cont, desc, trans)

class ResourceDescriptionItem(AnyClass, IXMLSupport):
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

    def __init__(self, 
                 language: TerminologyCode, 
                 purpose: str,
                 keywords: Optional[list[str]] = None,
                 use: Optional[str] = None,
                 misuse: Optional[str] = None,
                 original_resource_uri: Optional[dict[str, str]] = None,
                 other_details: Optional[dict[str, str]] = None):
        self.language = language
        self.purpose = purpose
        self.keywords = keywords
        self.use = use
        self.misuse = misuse
        self.original_resource_uri = original_resource_uri
        self.other_details = other_details
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
    
    def as_json(self):
        # https://specifications.openehr.org/releases/ITS-JSON/development/components/BASE/Release-1.1.0/Resource/RESOURCE_DESCRIPTION_ITEM.json
        # TODO: JSON schema disagrees with spec on the fields of the class (missing copyright and has other_details as required), going with spec rather than schema (and change local schema)
        draft = {
            "_type": "RESOURCE_DESCRIPTION_ITEM",
            "language": self.language.as_json(),
            "purpose": self.purpose
        }
        if self.keywords is not None:
            draft["keywords"] = self.keywords
        if self.use is not None:
            draft["use"] = self.use
        if self.misuse is not None:
            draft["misuse"] = self.misuse
        if self.original_resource_uri is not None:
            draft["original_resource_uri"] = self.original_resource_uri
        if self.other_details is not None:
            draft["other_details"] = self.other_details
        return draft
    
    def as_xml(self, root_tag = None):
        tag = "resource_description_item" if root_tag is None else root_tag
        root = ET.Element(tag)

        # in v1.0.2 XML language is a CODE_PHRASE not TERMINOLOGY_CODE
        lang_cp = CodePhrase(self.language.terminology_id, self.language.code_string)
        lang = lang_cp.as_xml("language")
        root.append(lang)

        purp = ET.Element("purpose")
        purp.text = self.purpose
        root.append(purp)

        if self.keywords is not None:
            for keyword_str in self.keywords:
                keyword = ET.Element("keywords")
                keyword.text = keyword_str
                root.append(keyword_str)

        if self.use is not None:
            use = ET.Element("use")
            use.text = self.use
            root.append(use)

        if self.misuse is not None:
            misuse = ET.Element("misuse")
            misuse.text = self.misuse
            root.append(misuse)

        if self.original_resource_uri is not None:
            for (key, value) in self.original_resource_uri.items():
                orig_uri = ET.Element("original_resource_uri")
                orig_uri.attrib["id"] = key
                orig_uri.text = value
                root.append(orig_uri)

        if self.other_details is not None:
            for (key, value) in self.other_details.items():
                other_detail = ET.Element("other_details")
                other_detail.attrib["id"] = key
                other_detail.text = value
                root.append(other_detail)

        # copyright is missing from this RM version

        return root
    
    def from_xml(root: ET.Element, **kwargs) -> 'ResourceDescriptionItem':
        lang : CodePhrase = CodePhrase.from_xml(root.find("./language"))
        purp = root.findtext("./purpose")
        keyword_els = root.findall("./keywords")
        keywords = None
        if len(keyword_els) > 0:
            keywords = []
            for keyword_el in keyword_els:
                keywords.append(keyword_el.text)
        use = root.findtext("./use")
        misuse = root.findtext("./misuse")
        # copyright is missing from this RM version
        oru_els = root.findall("./original_resource_uri")
        orus = None
        if len(oru_els) > 0:
            orus = dict()
            for oru_el in oru_els:
                orus[oru_el.attrib["id"]] = oru_el.text
        o_dt_els = root.findall("./other_details")
        other_details = None
        if len(o_dt_els) > 0:
            other_details = dict()
            for o_dt_el in o_dt_els:
                other_details[o_dt_el.attrib["id"]] = o_dt_el.text
        
        return ResourceDescriptionItem(
            language=TerminologyCode(lang.terminology_id.value, lang.code_string),
            purpose=purp,
            keywords=keywords,
            use=use,
            misuse=misuse,
            original_resource_uri=orus,
            other_details=other_details
        )


