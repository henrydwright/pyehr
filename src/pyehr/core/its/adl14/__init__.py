"""Methods for reading ARCHETYPEs (only) written in ADL v1.4"""

from typing import Optional, Union

from antlr4 import CommonTokenStream, InputStream, TerminalNode
import numpy as np
from pyehr.core.am.aom14.archetype import Archetype
from pyehr.core.am.aom14.archetype.ontology import ArchetypeOntology, ArchetypeTerm, CodeDefinitionSet, ConstraintBindingItem, ConstraintBindingSet, TermBindingItem, TermBindingSet
from pyehr.core.base.base_types.identification import ISOOID, UUID, ArchetypeID, TerminologyID, VersionTreeID, GenericID
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.interval import Interval, ProperInterval
from pyehr.core.base.foundation_types.terminology import TerminologyCode
from pyehr.core.base.foundation_types.time import ISODate, ISODateTime, ISODuration, ISOTime
from pyehr.core.base.resource import ResourceDescription, ResourceDescriptionItem
from pyehr.core.its.adl14.grammar.Adl14Lexer import Adl14Lexer
from pyehr.core.its.adl14.grammar.Adl14Parser import Adl14Parser
from pyehr.core.its.adl14.grammar.Cadl14Lexer import Cadl14Lexer
from pyehr.core.its.adl14.grammar.Cadl14Parser import Cadl14Parser
from pyehr.core.its.adl14.grammar.OdinLexer import OdinLexer
from pyehr.core.its.adl14.grammar.OdinParser import OdinParser
from pyehr.core.rm.data_types.text import CodePhrase

class Adl14ParseError(RuntimeError):
    pass

def _invalid_err(explanation: str):
    raise Adl14ParseError("Invalid ADL v1.4 string: " + explanation)

def _metadata_dict(ctx: Adl14Parser.MetaDataContext) -> dict[str, Union[ArchetypeID, UUID, VersionTreeID, str, ISOOID]]:
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
                    val = UUID(str(val.GUID()))
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

    return ret_dict

# odin_primitive_value_types = Union[str, np.int32, np.float32, bool, np.uint8, CodePhrase, ISODate, ISOTime, ISODateTime, ISODuration]
# odin_primitive_list_value_types = list[odin_primitive_value_types]
# odin_primitive_interval_value_types = Interval[Union[np.int32, np.float32, ISODate, ISOTime, ISODateTime, ISODuration]]

def _odin_primitive_object(prim): # -> Union[odin_primitive_value_types, odin_primitive_list_value_types, odin_primitive_interval_value_types]:
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
    elif isinstance(prim, OdinParser.PrimitiveIntervalValueContext):
        interval_txt = prim.getText()
        # cases to deal with... [source: https://specifications.openehr.org/releases/LANG/latest/odin.html#_primitive_types]
        # |N..M|        -- the two-sided range N >= x <= M;
        # |>N..M|       -- the two-sided range N > x <= M;
        # |N..<M|       -- the two-sided range N <= x <M;
        # |>N..<M|      -- the two-sided range N > x <M;
        # |<N|          -- the one-sided range x < N;
        # |>N|          -- the one-sided range x > N;
        # |>=N|         -- the one-sided range x >= N;
        # |<=N|         -- the one-sided range x <= N;
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
            # third possibility - one sided range
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
        _invalid_err(f"ODIN primitive object expected, but found {str(type(prim))} instead.")

def _odin_to_dict(odin) -> dict:
    # if odin is not None and odin.children is not None:
    #     print(odin.children)
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

def _decode_header(ctx: Adl14Parser.HeaderContext) -> tuple[ArchetypeID, Optional[str], Optional[UUID]]:
    """Retrieves details from the header.
    
    :returns: tuple of `(archetype_id: ArchetypeID, adl_version : str, uid : UUID)`"""

    if ctx is None or ctx.ARCHETYPE_REF() is None:
        _invalid_err("Valid header not present.")

    arch_id = ArchetypeID(str(ctx.ARCHETYPE_REF()))

    meta_dict = _metadata_dict(ctx.metaData())

    adl_ver = meta_dict.get("adl_version")
    if isinstance(adl_ver, ISOOID):
        adl_ver = adl_ver.value
    uid = meta_dict.get("uid")

    return (arch_id, adl_ver, uid)

def _decode_concept(ctx: Adl14Parser.ConceptSectionContext) -> str:
    """Retrieves the concept at code from the concept section"""
    if ctx is None:
        _invalid_err("No context section found.")

    return str(ctx.ADL14_AT_CODE())

def _decode_specialise(ctx: Adl14Parser.SpecializeSectionContext) -> Optional[ArchetypeID]:
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
    ret_id, ret_adl_ver, ret_uid = _decode_header(authored_archetype.header())

    # specializeSection
    ret_parent_id = _decode_specialise(authored_archetype.specializeSection())

    # conceptSection
    ret_conc = _decode_concept(authored_archetype.conceptSection())

    # do a second pass with the relevant section parser for sections we care about

    # languageSection
    lex_lang_odin = OdinLexer(InputStream(authored_archetype.languageSection().odinText().getText()))
    par_lang_odin = OdinParser(CommonTokenStream(lex_lang_odin))

    # descriptionSection
    lex_desc_odin = OdinLexer(InputStream(authored_archetype.descriptionSection().odinText().getText()))
    par_desc_odin = OdinParser(CommonTokenStream(lex_desc_odin))
    ret_description = _decode_description(par_desc_odin.odinObject())

    # definitionSection
    lex_def_cadl = Cadl14Lexer(InputStream(authored_archetype.definitionSection().cadlText().getText()))
    par_def_odin = Cadl14Parser(CommonTokenStream(lex_def_cadl))

    # rulesSection - skipped, as there is nothing here we care about reading

    # terminologySection
    lex_term_odin = OdinLexer(InputStream(authored_archetype.terminologySection().odinText().getText()))
    par_term_odin = OdinParser(CommonTokenStream(lex_term_odin))
    ret_terminology = _decode_terminology(par_term_odin.odinObject())

    # annotationsSection
    lex_anno_odin = OdinLexer(InputStream(authored_archetype.annotationsSection().odinText().getText()))
    par_anno_odin = OdinParser(CommonTokenStream(lex_anno_odin))



    
