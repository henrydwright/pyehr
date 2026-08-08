"""Methods for reading ARCHETYPEs (only) written in ADL v1.4"""

from typing import Optional, Union

from antlr4 import CommonTokenStream, InputStream, TerminalNode
import numpy as np
from pyehr.core.am.aom14.archetype import Archetype
from pyehr.core.am.aom14.archetype.assertion import Assertion, ExprBinaryOperator, ExprItem, ExprLeaf, OperatorKind
from pyehr.core.am.aom14.archetype.constraint_model import ArchetypeConstraint, ArchetypeInternalRef, ArchetypeSlot, CArchetypeRoot, CAttribute, CComplexObject, CDVQuantity, CMultipleAttribute, CObject, CPrimitiveObject, CQuantityItem, CSingleAttribute, CCodePhrase
from pyehr.core.am.aom14.archetype.constraint_model.primitive import *
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology, ArchetypeTerm, CodeDefinitionSet, ConstraintBindingItem, ConstraintBindingSet, TermBindingItem, TermBindingSet
from pyehr.core.base.base_types.identification import ISOOID, UUID, ArchetypeID, HierObjectID, TerminologyID, VersionTreeID, GenericID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Cardinality, Interval, MultiplicityInterval, PointInterval, ProperInterval
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
from pyehr.core.base.resource import ResourceDescription, ResourceDescriptionItem, TranslationDetails
from pyehr.core.its.adl14.grammar.Adl14Lexer import Adl14Lexer
from pyehr.core.its.adl14.grammar.Adl14Parser import Adl14Parser
from pyehr.core.its.adl14.grammar.Cadl14Lexer import Cadl14Lexer
from pyehr.core.its.adl14.grammar.Cadl14Parser import Cadl14Parser
from pyehr.core.its.adl14.grammar.ElLexer import ElLexer
from pyehr.core.its.adl14.grammar.ElParser import ElParser
from pyehr.core.its.adl14.grammar.OdinLexer import OdinLexer
from pyehr.core.its.adl14.grammar.OdinParser import OdinParser
from pyehr.core.rm.data_types.text import CodePhrase

from warnings import warn

class Adl14ParseError(RuntimeError):
    pass

def _invalid_err(explanation: str):
    raise Adl14ParseError("Invalid ADL v1.4 string: " + explanation)

def _metadata_dict(ctx: Adl14Parser.MetaDataContext) -> dict[str, Union[ArchetypeID, HierObjectID, VersionTreeID, str, ISOOID, set[str]]]:
    """Turns the metadata in ADL v1.4 header into key, value dict"""
    ret_dict = dict()
    if ctx is None:
        return ret_dict
    
    for child in ctx.children:
        if isinstance(child, Adl14Parser.MetaDataItemContext):
            if child.metaDataValueItem() is not None:
                key_val = child.metaDataValueItem()
                val = key_val.metaDataItemValue()
                if val.ARCHETYPE_REF():
                    val = ArchetypeID(str(val.ARCHETYPE_REF()))
                elif val.GUID():
                    val = HierObjectID(str(val.GUID()))
                elif val.VERSION_ID():
                    val = VersionTreeID(str(val.VERSION_ID()))
                elif val.ALPHANUM_ID():
                    val = str(val.ALPHANUM_ID())
                elif val.OID():
                    val = ISOOID(str(val.OID()))
                else:
                    # unknown metadata item, continue
                    continue
                ret_dict[str(key_val.ALPHANUM_ID())] = val
            elif child.metaDataFlag() is not None:
                if ret_dict.get("_flags") is None:
                    ret_dict["_flags"] = set()
                ret_dict["_flags"].add(str(child.metaDataFlag().ALPHANUM_ID()))

    return ret_dict

# odin_primitive_value_types = Union[str, np.int32, np.float32, bool, np.uint8, CodePhrase, ISODate, ISOTime, ISODateTime, ISODuration]
# odin_primitive_list_value_types = list[odin_primitive_value_types]
# odin_primitive_interval_value_types = Interval[Union[np.int32, np.float32, ISODate, ISOTime, ISODateTime, ISODuration]]

def _odin_primitive_object(prim, ignore_type_and_decode_as_interval=False): # -> Union[odin_primitive_value_types, odin_primitive_list_value_types, odin_primitive_interval_value_types]:
    if isinstance(prim, OdinParser.PrimitiveObjectContext):
        if prim.primitiveValue():
            return _odin_primitive_object(prim.primitiveValue())
        elif prim.primitiveListValue():
            return _odin_primitive_object(prim.primitiveListValue())
        elif prim.primitiveIntervalValue():
            return _odin_primitive_object(prim.primitiveIntervalValue())
    elif isinstance(prim, OdinParser.StringValueContext):
        return str(prim.getText()[1:-1])
    elif isinstance(prim, OdinParser.IntegerValueContext):
        return np.int32(prim.getText())
    elif isinstance(prim, OdinParser.RealValueContext):
        return np.float32(prim.getText())
    elif isinstance(prim, OdinParser.BooleanValueContext):
        return prim.getText().lower() == "true"
    elif isinstance(prim, OdinParser.CharacterValueContext):
        return np.uint8(prim.getText())
    elif isinstance(prim, OdinParser.TermCodeValueContext):
            tcText = str(prim.QUALIFIED_TERM_CODE_REF())
            tcSplit = tcText.replace("[","").replace("]","").split("::")
            term_id = TerminologyID(tcSplit[0])
            term_code = tcSplit[1]
            pref_term = None
            if "|" in term_code:
                pref_term = term_code.split("|")[1]
            return CodePhrase(term_id, term_code, pref_term)
    elif isinstance(prim, OdinParser.DateValueContext):
        return ISODate(prim.getText())
    elif isinstance(prim, OdinParser.TimeValueContext):
        return ISOTime(prim.getText())
    elif isinstance(prim, OdinParser.DateTimeValueContext):
        return ISODateTime(prim.getText())
    elif isinstance(prim, OdinParser.DurationValueContext):
        return ISODuration(prim.getText())
    elif isinstance(prim, OdinParser.PrimitiveValueContext):
        return _odin_primitive_object(prim.children[0])      
    elif isinstance(prim, OdinParser.PrimitiveListValueContext):
        lst = []
        for child in prim.children[0].children:
            if not isinstance(child, TerminalNode):
                lst.append(_odin_primitive_object(child))
        return lst
    elif isinstance(prim, OdinParser.PrimitiveIntervalValueContext) or ignore_type_and_decode_as_interval:
        interval_txt = prim.getText()
        prim = prim.children[0]
        # cases to deal with... [source: https://specifications.openehr.org/releases/LANG/latest/odin.html#_primitive_types]
        # |N..M|        -- the two-sided range N >= x <= M;
        # |>N..M|       -- the two-sided range N > x <= M;
        # |N..<M|       -- the two-sided range N <= x <M;
        # |>N..<M|      -- the two-sided range N > x <M;
        # |<N|          -- the one-sided range x < N;
        # |>N|          -- the one-sided range x > N;
        # |>=N|         -- the one-sided range x >= N;
        # |<=N|         -- the one-sided range x <= N;
        # |N|           -- the point internval N [not on site, but in practice and in grammar]
        # |N +/-M|      -- interval of N ±M.
        # |N±M|         -- interval of N ±M.
        if ".." in interval_txt:
            # first possibility - two sided range |(>)?N..(<)?M|
            gt_present = ">" in interval_txt
            lt_present = "<" in interval_txt
            first_val_idx = 1 + (1 if gt_present else 0)
            second_val_idx = 3 + (1 if gt_present else 0) + (1 if lt_present else 0)

            first_val = _odin_primitive_object(prim.children[first_val_idx])
            second_val = _odin_primitive_object(prim.children[second_val_idx])

            return ProperInterval(first_val, second_val, lower_included=(not gt_present), upper_included=(not lt_present))
        elif "±" in interval_txt or "+/-" in interval_txt:
            # second possibility - plus/minus range |N(+/-|±)M|
            first_val = _odin_primitive_object(prim.children[1])
            second_val = _odin_primitive_object(prim.children[2])

            return ProperInterval(first_val - second_val, first_val + second_val, lower_included=True, upper_included=True)
        else:
            # third possibility - one sided range or point interval
            if prim.relop() is not None:
                val = _odin_primitive_object(prim.children[2])
                if ">=" in interval_txt:
                    return ProperInterval(val, None, lower_included=True)
                elif "<=" in interval_txt:
                    return ProperInterval(None, val, upper_included=True)
                elif ">" in interval_txt:
                    return ProperInterval(val, None)
                elif "<" in interval_txt:
                    return ProperInterval(None, val)
            else:
                val = _odin_primitive_object(prim.children[1])
                return PointInterval(val)
    else:
        _invalid_err(f"ODIN primitive object expected, but found {str(type(prim))} instead.")

def _odin_to_dict(odin) -> dict:
    if isinstance(odin, OdinParser.OdinObjectContext):
        # top-level odin object
        d = dict()
        if odin.odinAttrVal() is not None and len(odin.odinAttrVal()) > 0:
            # list of odinAttrVals
            for attr_val_pair in odin.odinAttrVal():
                attr_name = attr_val_pair.odinAttrName().getText()
                attr_val_raw = attr_val_pair.odinObjectBlock()
                attr_val = _odin_to_dict(attr_val_raw)
                d[attr_name] = attr_val
        elif odin.odinObjectValueBlock() is not None:
            # single object value block
            d = _odin_to_dict(odin.odinObjectValueBlock())
        else:
            _invalid_err("Top level ODIN object invalid.")
        return d
    elif isinstance(odin, OdinParser.OdinObjectBlockContext):
        # either a value block or reference block
        if odin.odinObjectValueBlock() is not None:
            return _odin_to_dict(odin.odinObjectValueBlock())
        elif odin.odinObjectReferenceBlock() is not None:
            return _odin_to_dict(odin.odinObjectReferenceBlock())
        else:
            _invalid_err("Empty ODIN object block found.")
    elif isinstance(odin, OdinParser.OdinObjectValueBlockContext):
        # an object->value block
        po = odin.primitiveObject()
        oav = odin.odinAttrVal()
        oko = odin.odinKeyedObject()
        if odin.primitiveObject() is not None:
            return _odin_primitive_object(odin.primitiveObject())
        elif odin.odinAttrVal() is not None and len(odin.odinAttrVal()) > 0:
            d = dict()
            for attr_val_pair in odin.odinAttrVal():
                attr_name = attr_val_pair.odinAttrName().getText()
                attr_val = _odin_to_dict(attr_val_pair.odinObjectBlock())
                d[attr_name] = attr_val
            return d
        elif odin.odinKeyedObject() is not None and len(odin.odinKeyedObject()) > 0:
            d = dict()
            for key_obj_pair in odin.odinKeyedObject():
                attr_name = str(_odin_primitive_object(key_obj_pair.odinKeySpec().primitiveValue()))
                attr_val = _odin_to_dict(key_obj_pair.odinObjectBlock())
                d[attr_name] = attr_val
            return d
        elif odin.ODIN_URI() is not None:
            return str(odin.ODIN_URI())
        elif odin.getText() == "<>":
            return None
        else:
            _invalid_err("ODIN object value block had no valid children")
    elif isinstance(odin, OdinParser.OdinObjectReferenceBlockContext):
        # and object->reference block
        lst = []
        if odin.odinPathList():
            for child in odin.odinPathList():
                if isinstance(child, OdinParser.OdinPathContext):
                    lst.append(child.getText())
        return lst
    else:
        _invalid_err("Unknown ODIN child found")

def _odin_to_raw_json(val) -> dict:
        if isinstance(val, dict):
            raw_dict = dict()
            for (k, v) in val.items():
                raw_dict[k] = _odin_to_raw_json(v)
            return raw_dict
        elif isinstance(val, list):
            raw_lst = []
            for item in val:
                raw_lst.append(_odin_to_raw_json(item))
            return raw_lst
        elif isinstance(val, AnyClass):
            return val.as_json()
        else:
            return val

def _decode_header(ctx: Adl14Parser.HeaderContext) -> tuple[ArchetypeID, Optional[str], Optional[UUID], bool]:
    """Retrieves details from the header.
    
    :returns: tuple of `(archetype_id: ArchetypeID, adl_version : str, uid : UUID, is_controlled : bool)`"""

    if ctx is None or ctx.ARCHETYPE_REF() is None:
        _invalid_err("Valid header not present.")

    arch_id = ArchetypeID(str(ctx.ARCHETYPE_REF()))

    meta_dict = _metadata_dict(ctx.metaData())

    adl_ver = meta_dict.get("adl_version")
    if isinstance(adl_ver, ISOOID):
        adl_ver = adl_ver.value
    uid = meta_dict.get("uid")

    flags = meta_dict.get("_flags")
    is_controlled = ("controlled" in flags) if flags is not None else False

    return (arch_id, adl_ver, uid, is_controlled)

def _decode_concept(ctx: Adl14Parser.ConceptSectionContext) -> str:
    """Retrieves the concept at code from the concept section"""
    if ctx is None:
        _invalid_err("No context section found.")

    return str(ctx.ADL14_AT_CODE())

def _decode_specialise(ctx: Optional[Adl14Parser.SpecializeSectionContext]) -> Optional[ArchetypeID]:
    """Retrieves the parent archetype ID (that this is specialism of, or None)"""
    if ctx is None or ctx.ARCHETYPE_REF() is None:
        return None
    return ArchetypeID(str(ctx.ARCHETYPE_REF()))

def _decode_description(ctx: OdinParser.OdinObjectContext) -> ResourceDescription:
    desc_dict = _odin_to_dict(ctx)

    ex_original_author = desc_dict["original_author"]
    ex_lifecycle_state = desc_dict["lifecycle_state"]

    ex_details = dict()
    details_dict : dict = desc_dict["details"]
    for (lang_code, rdi_dict) in details_dict.items():
        lang_cp : CodePhrase = rdi_dict["language"]
        ex_lang = TerminologyCode(lang_cp.terminology_id.value, lang_cp.code_string, lang_cp.terminology_id.version_id() if lang_cp.terminology_id.version_id() != "" else None)
        ex_purp = rdi_dict["purpose"]
        ex_keywords = rdi_dict.get("keywords")
        ex_use = rdi_dict.get("use")
        ex_misuse = rdi_dict.get("misuse")
        ex_original_resource_uri = rdi_dict.get("original_resource_uri")
        ex_lang_other_details = rdi_dict.get("other_details")

        ex_detail = ResourceDescriptionItem(ex_lang, ex_purp, ex_keywords, ex_use, ex_misuse, ex_original_resource_uri, ex_lang_other_details)
        ex_details[lang_code] = ex_detail

    ex_original_namespace = desc_dict.get("original_namespace")
    ex_original_publisher = desc_dict.get("original_publisher")
    ex_other_contributors = desc_dict.get("other_contributors")
    ex_custodian_namespace = desc_dict.get("custodian_namespace")
    ex_custodian_organisation = desc_dict.get("custodian_organisation")
    ex_copyright = desc_dict.get("copyright")
    ex_licence = desc_dict.get("licence")
    ex_ip_acknowledgements = desc_dict.get("ip_acknowledgements")
    ex_references = desc_dict.get("references")
    ex_resource_package_uri = desc_dict.get("resource_package_uri")
    ex_conversion_details = desc_dict.get("conversion_details")
    ex_other_details = desc_dict.get("other_details")

    return ResourceDescription(
        ex_original_author,
        ex_lifecycle_state,
        ex_details,
        None,
        ex_original_namespace,
        ex_original_publisher,
        ex_other_contributors,
        ex_custodian_namespace,
        ex_custodian_organisation,
        ex_copyright,
        ex_licence,
        ex_ip_acknowledgements,
        ex_references,
        ex_resource_package_uri,
        ex_conversion_details,
        ex_other_details
    )

def _process_code_definition_set(cds_dict: dict) -> list[CodeDefinitionSet]:
    codes_def_list = []

    for (ex_lang, code_definition_dict) in cds_dict.items():
        items_dict = code_definition_dict.get("items")
        ex_items = None
        if items_dict is not None:
            ex_items = []
            for (ex_code, ex_term_items) in items_dict.items():
                ex_items.append(ArchetypeTerm(ex_code, ex_term_items))

        codes_def_list.append(CodeDefinitionSet(ex_lang, ex_items))

    return codes_def_list

def _decode_terminology(ctx: OdinParser.OdinObjectContext) -> ArchetypeOntology:
    term_dict = _odin_to_dict(ctx)

    term_def_dict : dict = term_dict["term_definitions"]
    ex_term_defs = _process_code_definition_set(term_def_dict)

    cons_def_dict = term_dict.get("constraint_definitions")
    ex_cons_defs = None
    if cons_def_dict is not None:
        ex_cons_defs = _process_code_definition_set(cons_def_dict)

    term_binds_dict : dict = term_dict.get("term_bindings")
    ex_term_binds = None
    if term_binds_dict is not None:
        ex_term_binds = []
        for (ex_terminology, items_dict) in term_binds_dict.items():
            ex_items = []
            for (binding, code_phrase) in items_dict.get("items").items():
                ex_items.append(TermBindingItem(binding, code_phrase))
            ex_term_binds.append(TermBindingSet(ex_terminology, ex_items))

    cons_binds_dict : dict = term_dict.get("constraint_bindings")
    ex_cons_binds = None
    if cons_binds_dict is not None:
        ex_cons_binds = []
        for (ex_terminology, items_dict) in cons_binds_dict.items():
            ex_items = []
            for (ex_code, ex_value) in items_dict.items():
                ex_items.append(ConstraintBindingItem(ex_value, ex_code))
            ex_cons_binds.append(ConstraintBindingSet(ex_terminology, ex_items))

    return ArchetypeOntology(
        ex_term_defs,
        ex_cons_defs,
        ex_term_binds,
        ex_cons_binds
    )

def _cadl_multiplicity_to_interval(ctx: Union[Cadl14Parser.MultiplicityContext, Cadl14Parser.ExistenceContext]) -> MultiplicityInterval:
    multi_str = ctx.getText()
    if multi_str == "*":
        # in the form *
        return MultiplicityInterval(lower=0)
    elif ".." in multi_str:
        # in the form X..* or X..X
        split = multi_str.split("..")
        bottom = np.int32(split[0])
        if split[1] == "*":
            return MultiplicityInterval(lower=bottom)
        else:
            return MultiplicityInterval(lower=bottom, upper=np.int32(split[1]))
    else: 
        # should be in the form X
        return MultiplicityInterval(lower=np.int32(multi_str), upper=np.int32(multi_str))

def _cadl_coccurences_to_interval(ctx: Optional[Cadl14Parser.COccurrencesContext]) -> MultiplicityInterval:
    ex_occurences = None
    if ctx is not None:
        ex_occurences = _cadl_multiplicity_to_interval(ctx.multiplicity())
    else:
        # as per, https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL1.4.html
        # The default occurrences, if none is mentioned, is {1..1}.
        ex_occurences = MultiplicityInterval(lower=np.int32(1), upper=np.int32(1))
    return ex_occurences

def _cadl_cexistence_to_interval(ctx: Optional[Cadl14Parser.CExistenceContext]) -> MultiplicityInterval:
    ex_existence = None
    if ctx is not None:
        ex_existence = _cadl_multiplicity_to_interval(ctx.existence())
    else:
        # as per, https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL1.4.html
        # The default existence constraint, if none is shown, is {1..1}.
        ex_existence = MultiplicityInterval(lower=np.int32(1), upper=np.int32(1))
    return ex_existence

def _cadl_ccardinality_to_cardinality(ctx: Cadl14Parser.CCardinalityContext) -> Cardinality:
    ex_interval = _cadl_multiplicity_to_interval(ctx.cardinality().multiplicity())
    multi_mod = ctx.cardinality().multiplicityMod()
    ex_is_ordered = None
    ex_is_unique = False
    if multi_mod is not None:
        mm_lst = []
        if isinstance(multi_mod, Cadl14Parser.MultiplicityModContext):
            mm_lst = [multi_mod]
        else:
            mm_lst = multi_mod
        for mmod in mm_lst:
            if mmod.orderingMod() is not None:
                if mmod.orderingMod().SYM_ORDERED():
                    ex_is_ordered = True
                elif mmod.orderingMod().SYM_UNORDERED():
                    ex_is_ordered = False
            if mmod.uniqueMod() is not None and mmod.uniqueMod().SYM_UNIQUE():
                ex_is_unique = True

    return Cardinality(ex_is_ordered, ex_is_unique, ex_interval)
        

def _cadl_to_cattributes(cadl: Union[Cadl14Parser.CAttributeContext, list[Cadl14Parser.CAttributeContext]]) -> list[CAttribute]:
    if not isinstance(cadl, list):
        cadl = [cadl]

    r_lst = []

    for cattr in cadl:
        ex_rm_attribute_name = cattr.rmAttributeId().getText()

        ex_existence = _cadl_cexistence_to_interval(cattr.cExistence())
        ex_children = None

        if cattr.cAttributeDef() is not None:
            obj_cadls = cattr.cAttributeDef().cRegularObject()
            ex_children = []
            for obj_cadl in obj_cadls:
                ex_children.append(_cadl_to_cobject(obj_cadl))
        elif cattr.cInlinePrimitiveObject() is not None:
            ex_children = [_cadl_to_cobject(cattr.cInlinePrimitiveObject())]

        if cattr.cCardinality() is not None:
            # https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL1.4.html#_cardinality
            # There is no default cardinality, since if none is shown, the relevant attribute is assumed to be 
            # single-valued (in the interests of uniformity in archetypes, this holds even for smarter parsers 
            # that can access the reference model and determine that the attribute is in fact a container).
            ex_cardinality = _cadl_ccardinality_to_cardinality(cattr.cCardinality())
            cma = CMultipleAttribute(ex_rm_attribute_name, ex_existence, ex_cardinality, children=ex_children)
            r_lst.append(cma)
        else:
            csa = CSingleAttribute(ex_rm_attribute_name, ex_existence, children=ex_children)
            r_lst.append(csa)

    return (r_lst if len(r_lst) > 0 else None)

def _cadl_to_cprimitive(cadl: Cadl14Parser.CInlinePrimitiveObjectContext) -> tuple[CPrimitive, str]:
    """Returns a C_PRIMITIVE and the rm_type_name associated with it"""
    if isinstance(cadl, Cadl14Parser.CInlinePrimitiveObjectContext):
        if cadl.cInlineOrderedObject() is not None:
            return _cadl_to_cprimitive(cadl.cInlineOrderedObject())
        elif cadl.cString() is not None:
            return _cadl_to_cprimitive(cadl.cString())
        elif cadl.cTerminologyCode() is not None:
            return _cadl_to_cprimitive(cadl.cTerminologyCode())
        elif cadl.cBoolean() is not None:
            return _cadl_to_cprimitive(cadl.cBoolean())
        else:
            _invalid_err("Invalid child of cInlinePrimitiveObject")
    elif isinstance(cadl, Cadl14Parser.CInlineOrderedObjectContext):
        if cadl.cInteger() is not None:
            return _cadl_to_cprimitive(cadl.cInteger())
        elif cadl.cReal() is not None:
            return _cadl_to_cprimitive(cadl.cReal())
        elif cadl.cInlineDTemporalObject() is not None:
            return _cadl_to_cprimitive(cadl.cInlineDTemporalObject())
        else:
            _invalid_err("Invalid child of cInlineOrderedObject")
    elif isinstance(cadl, Cadl14Parser.CInlineDTemporalObjectContext):
        if cadl.cDate() is not None:
            return _cadl_to_cprimitive(cadl.cDate())
        elif cadl.cTime() is not None:
            return _cadl_to_cprimitive(cadl.cTime())
        elif cadl.cDateTime() is not None:
            return _cadl_to_cprimitive(cadl.cDateTime())
        elif cadl.cDuration() is not None:
            return _cadl_to_cprimitive(cadl.cDuration())
        else:
            _invalid_err("Invalid child of cInlineDTemporalObject")
    elif isinstance(cadl, Cadl14Parser.CStringContext):
        ex_assumed_value = cadl.assumedStringValue().stringValue().getText() if cadl.assumedStringValue() is not None else None
        ex_pattern = None
        ex_list_var = None
        if cadl.stringValue() is not None:
            ex_list_var = [cadl.stringValue().getText()]
        elif cadl.stringValues() is not None:
            ex_list_var = []
            for str_value in cadl.stringValues().stringValue():
                ex_list_var.append(str_value.getText())
        elif cadl.DELIMITED_REGEX() is not None:
            ex_pattern = str(cadl.DELIMITED_REGEX())
        return (CString(pattern=ex_pattern, list_var=ex_list_var, assumed_value=ex_assumed_value), "DV_TEXT")
    elif isinstance(cadl, Cadl14Parser.CTerminologyCodeContext):
        # others are from Cadl2PrimitiveConstraintsParser.g4 but this comes from Cadl14PrimitiveConstraintsParser.g4
        ex_code_list = None
        ex_assumed_value = None
        ex_terminology_id = None
        if cadl.terminologyLocalCode() is not None:
            ex_code_list = [cadl.terminologyLocalCode().adl14_at_code().getText()]
            ex_terminology_id = TerminologyID("local")
        elif cadl.valueSetCode() is not None:
            warn("Terminology code value set encountered and not expanded as not supported by pyehr. Will result in empty code list unless default code provided.")
            ex_terminology_id = TerminologyID("local")
            if cadl.valueSetCode().termCodeDefault() is not None:
                ex_assumed_value = CodePhrase("local", cadl.valueSetCode().termCodeDefault().adl14_at_code().getText())
                ex_code_list = []
            else:
                ex_code_list = []
        elif cadl.cLocalTermCode() is not None:
            ex_code_list = []
            ex_terminology_id = TerminologyID("local")
            lcode_list = cadl.cLocalTermCode().localCodesList()
            if lcode_list is not None:
                if cadl.cLocalTermCode().termCodeDefault() is not None:
                    ex_assumed_value = CodePhrase("local", cadl.cLocalTermCode().termCodeDefault().adl14_at_code().getText())
                ex_code_list.append(lcode_list.adl14_at_code().getText())
                if lcode_list.termCodeItem() is not None:
                    tcis = lcode_list.termCodeItem()
                    for tci in tcis:
                        ex_code_list.append(tci.adl14_at_code().getText())
        elif cadl.cExternalTermCode() is not None:
            ex_code_list = []
            tc_start_str = str(cadl.cExternalTermCode().C_EXTERNAL_TERM_CODE_START())
            ex_terminology_id = TerminologyID(tc_start_str.split("::")[0][1:])
            ecode_list = cadl.cExternalTermCode().externalCodesList()
            if ecode_list is not None:
                if cadl.cExternalTermCode().externalTermCodeDefault() is not None:
                    ex_assumed_value = CodePhrase(ex_terminology_id, str(cadl.cExternalTermCode().externalTermCodeDefault().C_EXTERNAL_TERM_CODE_STRING()))
                ex_code_list.append(str(ecode_list.C_EXTERNAL_TERM_CODE_STRING()))
                if ecode_list.externalTermCodeItem() is not None:
                    ecis = ecode_list.externalTermCodeItem()
                    for eci in ecis:
                        ex_code_list.append(str(eci.C_EXTERNAL_TERM_CODE_STRING()))
        elif cadl.QUALIFIED_TERM_CODE_REF() is not None:
            code_str = str(cadl.QUALIFIED_TERM_CODE_REF())
            code_str = code_str[1:-1] # remove outer [] brackets
            code_str_split = code_str.split("::")
            ex_terminology_id = TerminologyID(code_str_split[0])
            ex_code_list = [code_str_split[1].split("|")[0]]
        else:
            _invalid_err("Invalid cTerminologyCode encountered.")
        
        return (CCodePhrase("CODE_PHRASE", _cadl_coccurences_to_interval(None), "", assumed_value=ex_assumed_value, terminology_id=ex_terminology_id, code_list=ex_code_list), "CODE_PHRASE")
    elif isinstance(cadl, Cadl14Parser.CBooleanContext):
        ex_true_valid = False
        ex_false_valid = False
        ex_assumed_value = None
        if cadl.booleanValue() is not None:
            if cadl.booleanValue().getText().lower() == "true":
                ex_true_valid = True
            else:
                ex_false_valid = True
        elif cadl.booleanValues() is not None:
            ex_false_valid = True
            ex_true_valid = True
        if cadl.assumedBooleanValue() is not None:
            ex_assumed_value = (cadl.assumedBooleanValue().booleanValue().getText().lower() == "true")

        return (CBoolean(ex_true_valid, ex_false_valid, ex_assumed_value), "DV_BOOLEAN")
    elif isinstance(cadl, Cadl14Parser.CIntegerContext):
        ex_list_var = None
        ex_range = None
        ex_assumed_value = None
        if cadl.assumedIntegerValue() is not None:
            ex_assumed_value = np.int32(cadl.assumedIntegerValue().integerValue().getText())

        if cadl.integerValue() is not None:
            ex_list_var = [np.int32(cadl.integerValue().getText())]
        elif cadl.integerValues() is not None:
            ex_list_var = []
            ivs = cadl.integerValues().integerValue()
            for iv in ivs:
                ex_list_var.append(np.int32(iv.getText()))
        elif cadl.integerInterval() is not None:
            ex_range = _odin_primitive_object(cadl.integerInterval().integerIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("Multiple integer intervals are not possible in ADL v1.4")

        return (CInteger(ex_list_var, ex_range, ex_assumed_value), "DV_INTEGER")
    elif isinstance(cadl, Cadl14Parser.CRealContext):
        ex_list_var = None
        ex_range = None
        ex_assumed_value = None
        if cadl.assumedRealValue() is not None:
            ex_assumed_value = np.float32(cadl.assumedRealValue().realValue().getText())

        if cadl.realValue() is not None:
            ex_list_var = [np.float32(cadl.realValue().getText())]
        elif cadl.realValues() is not None:
            ex_list_var = []
            rvs = cadl.realValues().realValue()
            for rv in rvs:
                ex_list_var.append(np.float32(rv.getText()))
        elif cadl.realInterval() is not None:
            ex_range = _odin_primitive_object(cadl.realInterval().realIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("Multiple real intervals are not possible in ADL v1.4")

        return (CReal(ex_list_var, ex_range, ex_assumed_value), "DV_REAL")
    elif isinstance(cadl, Cadl14Parser.CDateContext):
        ex_month_validity = None
        ex_day_validity = None
        ex_range = None
        ex_assumed_value = None
        if cadl.assumedDateValue() is not None:
            ex_assumed_value = ISODate(cadl.assumedDateValue().dateValue().getText())

        if cadl.DATE_CONSTRAINT_PATTERN() is not None:
            pattern = str(cadl.DATE_CONSTRAINT_PATTERN())
            ex_month_validity, ex_day_validity = CDate.constraint_pattern_to_validity_kinds(pattern)
        elif cadl.dateValue() is not None:
            ex_range = PointInterval(ISODate(cadl.dateValue().getText()))
        elif cadl.dateInterval() is not None:
            ex_range = _odin_primitive_object(cadl.dateInterval().dateIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("List of date values not possible in ADL v1.4")

        return (CDate(ex_month_validity, ex_day_validity, range=ex_range, assumed_value=ex_assumed_value), "DV_DATE")
    elif isinstance(cadl, Cadl14Parser.CTimeContext):
        ex_minute_validity = None
        ex_second_validity = None
        ex_range = None
        ex_assumed_value = None
        if cadl.assumedTimeValue() is not None:
            ex_assumed_value = ISOTime(cadl.assumedTimeValue().timeValue().getText())

        if cadl.TIME_CONSTRAINT_PATTERN() is not None:
            pattern = str(cadl.TIME_CONSTRAINT_PATTERN())
            ex_minute_validity, ex_second_validity = CTime.constraint_pattern_to_validity_kinds(pattern)
        elif cadl.timeValue() is not None:
            ex_range = PointInterval(ISODuration(cadl.timeValue().getText()))
        elif cadl.timeInterval() is not None:
            ex_range = _odin_primitive_object(cadl.timeInterval().timeIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("List of time values not possible in ADL v1.4")

        return (CTime(ex_minute_validity, ex_second_validity, range=ex_range, assumed_value=ex_assumed_value), "DV_TIME")
    elif isinstance(cadl, Cadl14Parser.CDateTimeContext):
        ex_month_validity = None
        ex_day_validity = None
        ex_hour_validity = None
        ex_minute_validity = None
        ex_second_validity = None
        ex_range = None
        ex_assumed_value = None
        if cadl.assumedDateTimeValue() is not None:
            ex_assumed_value = ISODateTime(cadl.assumedDateTimeValue().dateTimeValue().getText())

        if cadl.DATE_TIME_CONSTRAINT_PATTERN() is not None:
            pattern = str(cadl.DATE_TIME_CONSTRAINT_PATTERN())
            ex_month_validity, ex_day_validity, ex_hour_validity, ex_minute_validity, ex_second_validity = CDateTime.constraint_pattern_to_validity_kinds(pattern)
        elif cadl.dateTimeValue() is not None:
            ex_range = PointInterval(ISODateTime(cadl.dateTimeValue().getText()))
        elif cadl.dateTimeInterval() is not None:
            ex_range = _odin_primitive_object(cadl.dateTimeInterval().dateTimeIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("List of datetime values not possible in ADL v1.4")

        return (CDateTime(ex_month_validity, ex_day_validity, ex_hour_validity, ex_minute_validity, ex_second_validity, range=ex_range, assumed_value=ex_assumed_value), "DV_DATE_TIME")
    elif isinstance(cadl, Cadl14Parser.CDurationContext):
        ex_years_allowed = None
        ex_months_allowed = None
        ex_weeks_allowed = None
        ex_days_allowed = None
        ex_hours_allowed = None
        ex_minutes_allowed = None
        ex_seconds_allowed = None
        ex_range = None
        ex_assumed_value = None

        if cadl.assumedDurationValue() is not None:
            ex_assumed_value = ISODuration(cadl.assumedDurationValue().durationValue().getText())

        if cadl.DURATION_CONSTRAINT_PATTERN() is not None:
            pattern = str(cadl.DURATION_CONSTRAINT_PATTERN())
            ex_years_allowed, ex_months_allowed, ex_weeks_allowed, ex_days_allowed, ex_hours_allowed, ex_minutes_allowed, ex_seconds_allowed = CDuration.constraint_pattern_to_allowed_flags(pattern)
        elif cadl.durationValue() is not None:
            ex_range = PointInterval(ISODuration(cadl.durationValue().getText()))
        elif cadl.durationInterval() is not None:
            ex_range = _odin_primitive_object(cadl.durationInterval().durationIntervalRange(), ignore_type_and_decode_as_interval=True)
        else:
            _invalid_err("List of duration values not possible in ADL v1.4")

        return (CDuration(ex_years_allowed, ex_months_allowed, ex_weeks_allowed, ex_days_allowed, ex_hours_allowed, ex_minutes_allowed, ex_seconds_allowed, range=ex_range, assumed_value=ex_assumed_value), "DV_DURATION")
    else:
        _invalid_err(f"Given type cannot be converted to C_PRIMITIVE {str(type(cadl))}")

def _arch_id_constraint_list_to_assertion_list(ctx: list[Cadl14Parser.ArchetypeIdConstraintContext]) -> list[Assertion]:
    r_lst = []
    for aid in ctx:
        arch_id_path = aid.archetypeIdPath().getText()
        pattern = str(aid.DELIMITED_REGEX())[1:-1]
        str_expr = arch_id_path + " matches {" + str(aid.DELIMITED_REGEX()) + "}"
        r_lst.append(Assertion(
            expression=ExprBinaryOperator(
                type_var="Boolean",
                left_operand=ExprLeaf(
                    type_var="String",
                    reference_type="attribute",
                    item=arch_id_path
                ),
                operator=OperatorKind.MATCHES,
                right_operand=ExprLeaf(
                    type_var="C_STRING",
                    reference_type="constraint",
                    item=CString(pattern=pattern)
                )
            ),
            string_expression=str_expr
        ))
    return r_lst

def _cadl_to_cobject(cadl) -> CObject:
    # add cInlinePrimitiveObject from Cadl2PrimitiveConstraintsParser.g4
    if isinstance(cadl, Cadl14Parser.CRegularObjectContext):
        if cadl.cComplexObject() is not None:
            return _cadl_to_cobject(cadl.cComplexObject())
        elif cadl.cArchetypeRoot() is not None:
            return _cadl_to_cobject(cadl.cArchetypeRoot())
        elif cadl.cComplexObjectProxy() is not None:
            return _cadl_to_cobject(cadl.cComplexObjectProxy())
        elif cadl.archetypeSlot() is not None:
            return _cadl_to_cobject(cadl.archetypeSlot())
        elif cadl.cRegularPrimitiveObject() is not None:
            return _cadl_to_cobject(cadl.cRegularPrimitiveObject())
        elif cadl.cOrdinal() is not None:
            return _cadl_to_cobject(cadl.cOrdinal())
        elif cadl.domainSpecificExtension() is not None:
            return _cadl_to_cobject(cadl.domainSpecificExtension())
        else:
            _invalid_err(f"Child of CRegularObject {str(type(cadl))} not recognised.")
    elif isinstance(cadl, Cadl14Parser.CComplexObjectContext):
        ex_rm_type_name = cadl.rmTypeId().getText()
        ex_node_id = cadl.nodeId().adl14_at_code().getText() if cadl.nodeId() is not None else ""
        ex_occurrences = _cadl_coccurences_to_interval(cadl.cOccurrences())

        if cadl.cComplexObjectDef() is not None and cadl.cComplexObjectDef().cAttribute() is not None:
            return CComplexObject(
                ex_rm_type_name, 
                ex_occurrences, 
                ex_node_id,  
                attributes=_cadl_to_cattributes(cadl.cComplexObjectDef().cAttribute()))
        else:
            return CComplexObject(ex_rm_type_name, ex_occurrences, ex_node_id)
    elif isinstance(cadl, Cadl14Parser.CArchetypeRootContext):
        ex_rm_type_name = cadl.rmTypeId().getText()
        ex_node_id = cadl.adl14_at_code().getText()
        ex_archetype_id = str(cadl.ARCHETYPE_REF())
        ex_occurrences = _cadl_coccurences_to_interval(cadl.cOccurrences())
        return CArchetypeRoot(ex_rm_type_name, ex_occurrences, ex_node_id, ArchetypeID(ex_archetype_id))
    elif isinstance(cadl, Cadl14Parser.ArchetypeSlotContext):
        ex_rm_type_name = cadl.rmTypeId().getText()
        ex_node_id = cadl.nodeId().adl14_at_code().getText()
        ex_occurrences = _cadl_coccurences_to_interval(cadl.cOccurrences())

        ex_includes = None
        ex_excludes = None
        if cadl.cIncludes() is not None:
            ex_includes = _arch_id_constraint_list_to_assertion_list(cadl.cIncludes().archetypeIdConstraint())
        if cadl.cExcludes() is not None:
            ex_excludes = _arch_id_constraint_list_to_assertion_list(cadl.cExcludes().archetypeIdConstraint())

        return ArchetypeSlot(ex_rm_type_name, ex_occurrences, ex_node_id, includes=ex_includes, excludes=ex_excludes)
    elif isinstance(cadl, Cadl14Parser.CRegularPrimitiveObjectContext):
        ex_rm_type_name = cadl.rmTypeId().getText()
        ex_node_id = cadl.nodeId().adl14_at_code().getText()
        ex_occurrences = _cadl_coccurences_to_interval(cadl.cOccurrences())
        ex_item = None
        if cadl.cInlinePrimitiveObject() is not None:
            ex_item, _ = _cadl_to_cprimitive(cadl.cInlinePrimitiveObject())
            if isinstance(ex_item, CCodePhrase):
                # C_CODE_PHRASE is actually a domain type, but a primitive in the grammar
                return ex_item
        return CPrimitiveObject(ex_rm_type_name, ex_occurrences, ex_node_id, ex_item)
    elif isinstance(cadl, Cadl14Parser.CInlinePrimitiveObjectContext):
        # this is in here despite not really being a CObject to allow for it to be turned into one
        #  in the course of parsing an CAttribute which is a common need
        ex_item, ex_rm_type_name = _cadl_to_cprimitive(cadl)
        if isinstance(ex_item, CCodePhrase):
            # C_CODE_PHRASE is actually a domain type, but a primitive in the grammar
            ex_item.rm_type_name = ex_rm_type_name
            return ex_item
        return CPrimitiveObject(ex_rm_type_name, _cadl_coccurences_to_interval(None), "", ex_item)
    elif isinstance(cadl, Cadl14Parser.DomainSpecificExtensionContext):
        # the only domain specific extension supported is C_DV_QUANTITY
        block_start = str(cadl.ODIN14_BLOCK_START())
        if "C_DV_QUANTITY" in block_start:
            inline_odin = cadl.getText()

            lex = OdinLexer(InputStream(inline_odin))
            par = OdinParser(CommonTokenStream(lex))
            odict = _odin_to_dict(par.odinObject())

            ex_property = odict.get("property")
            ex_list = None
            if "list" in odict:
                ex_list = []
                list_dict = odict["list"]
                for value in list_dict.values():
                    ex_list.append(CQuantityItem(value.get("units"), value.get("magnitude"), value.get("precision")))
            
            return CDVQuantity("DV_QUANTITY", _cadl_coccurences_to_interval(None), "", property_var=ex_property, list_var=ex_list)
        else:
            _invalid_err(f"Domain specific extension of type {block_start} not recognised/supported by pyehr.")
    elif isinstance(cadl, Cadl14Parser.CComplexObjectProxyContext):
        ex_rm_type_name = cadl.rmTypeId().getText()
        ex_occurrences = _cadl_coccurences_to_interval(cadl.cOccurrences())
        ex_target_path = cadl.adlPath().getText()
        return ArchetypeInternalRef(ex_rm_type_name, ex_occurrences, "", target_path=ex_target_path)
    else:
        # cComplexObjectProxy and cOrdinal are not yet supported
        _invalid_err(f"Object type {str(type(cadl))} not yet supported by pyehr.")

def _code_phrase_to_term_code(cp: CodePhrase) -> TerminologyCode:
    return TerminologyCode(cp.terminology_id.value, cp.code_string, cp.terminology_id.version_id() if cp.terminology_id.version_id() != "" else None)

def _decode_languages(ctx: OdinParser.OdinObjectContext) -> tuple[TerminologyCode, Optional[dict[str, TranslationDetails]]]:
    odict = _odin_to_dict(ctx)

    ret_olang = _code_phrase_to_term_code(odict["original_language"])

    trans_dict = odict.get("translations")
    ret_trans_dict = None
    if trans_dict is not None:
        ret_trans_dict = dict()
        for (lang_code, trans_detail_dict) in trans_dict.items():
            td = TranslationDetails(
                language=_code_phrase_to_term_code(trans_detail_dict["language"]),
                author=trans_detail_dict["author"],
                accreditation=trans_detail_dict.get("accreditation"),
                other_details=trans_detail_dict.get("other_details"),
                version_last_translated=trans_detail_dict.get("version_last_translated"),
                other_contributors=trans_detail_dict.get("other_contributors")
            )
            ret_trans_dict[lang_code] = td

    return (ret_olang, ret_trans_dict)

def decode_adl14(adl14_str: str) -> Archetype:
    # conduct first pass to break down the ADL v1.4 into sections
    lex_adl = Adl14Lexer(InputStream(adl14_str))
    par_adl = Adl14Parser(CommonTokenStream(lex_adl))

    # structure from antlr for reference:
    # 
    # authoredArchetype:
    # SYM_ARCHETYPE header
    # specializeSection?
    # conceptSection
    # languageSection
    # descriptionSection
    # definitionSection
    # rulesSection?
    # terminologySection
    # annotationsSection?
    # ;

    authored_archetype = par_adl.authoredArchetype()
    if authored_archetype is None:
        _invalid_err("Top-level archetype structure not found or malformed.")

    # header
    ret_id, ret_adl_ver, ret_uid, ret_is_cont = _decode_header(authored_archetype.header())

    # specializeSection
    ret_parent_id = _decode_specialise(authored_archetype.specializeSection())

    # conceptSection
    ret_conc = _decode_concept(authored_archetype.conceptSection())

    # do a second pass with the relevant section parser for sections we care about

    # languageSection
    lex_lang_odin = OdinLexer(InputStream(authored_archetype.languageSection().odinText().getText()))
    par_lang_odin = OdinParser(CommonTokenStream(lex_lang_odin))
    ret_original_language, ret_translation_details = _decode_languages(par_lang_odin.odinObject())

    # descriptionSection
    lex_desc_odin = OdinLexer(InputStream(authored_archetype.descriptionSection().odinText().getText()))
    par_desc_odin = OdinParser(CommonTokenStream(lex_desc_odin))
    ret_description = _decode_description(par_desc_odin.odinObject())

    if ret_translation_details is not None:
        for lang_code in ret_translation_details.keys():
            if lang_code not in ret_description.details:
                _invalid_err(f"Language {lang_code} was found in languages, but not in the description section.")

    # definitionSection
    lex_def_cadl = Cadl14Lexer(InputStream(authored_archetype.definitionSection().cadlText().getText()))
    par_def_odin = Cadl14Parser(CommonTokenStream(lex_def_cadl))
    ret_definition = _cadl_to_cobject(par_def_odin.cComplexObject())

    # rulesSection
    if authored_archetype.rulesSection() is not None:
        warn("rules section detected, but skipped as pyehr does not support parsing this.")
        # lex_rules_el = ElLexer(InputStream(authored_archetype.rulesSection().elText().getText()))
        # par_rules_el = ElParser(CommonTokenStream(lex_rules_el))

    # terminologySection
    lex_term_odin = OdinLexer(InputStream(authored_archetype.terminologySection().odinText().getText()))
    par_term_odin = OdinParser(CommonTokenStream(lex_term_odin))
    ret_terminology = _decode_terminology(par_term_odin.odinObject())

    # annotationsSection
    if authored_archetype.annotationsSection() is not None:
        warn("annotations section detected, but skipped as pyehr does not support parsing this.")
        # lex_anno_odin = OdinLexer(InputStream(authored_archetype.annotationsSection().odinText().getText()))
        # par_anno_odin = OdinParser(CommonTokenStream(lex_anno_odin))

    arch = Archetype(
        original_language=ret_original_language,
        definition=ret_definition,
        ontology=ret_terminology,
        archetype_id=ret_id,
        concept=ret_conc,
        adl_version=ret_adl_ver,
        parent_archetype_id=ret_parent_id,
        uid=ret_uid,
        is_controlled=ret_is_cont
    )
    arch._description = ret_description
    arch._translations = ret_translation_details

    return arch


    
