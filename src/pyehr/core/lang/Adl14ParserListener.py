# Created using Commit 3494da9 from https://github.com/openEHR/openEHR-antlr4
# Generated from Adl14Parser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Adl14Parser import Adl14Parser
else:
    from Adl14Parser import Adl14Parser

# This class defines a complete listener for a parse tree produced by Adl14Parser.
class Adl14ParserListener(ParseTreeListener):

    # Enter a parse tree produced by Adl14Parser#adlObject.
    def enterAdlObject(self, ctx:Adl14Parser.AdlObjectContext):
        pass

    # Exit a parse tree produced by Adl14Parser#adlObject.
    def exitAdlObject(self, ctx:Adl14Parser.AdlObjectContext):
        pass


    # Enter a parse tree produced by Adl14Parser#authoredArchetype.
    def enterAuthoredArchetype(self, ctx:Adl14Parser.AuthoredArchetypeContext):
        pass

    # Exit a parse tree produced by Adl14Parser#authoredArchetype.
    def exitAuthoredArchetype(self, ctx:Adl14Parser.AuthoredArchetypeContext):
        pass


    # Enter a parse tree produced by Adl14Parser#header.
    def enterHeader(self, ctx:Adl14Parser.HeaderContext):
        pass

    # Exit a parse tree produced by Adl14Parser#header.
    def exitHeader(self, ctx:Adl14Parser.HeaderContext):
        pass


    # Enter a parse tree produced by Adl14Parser#metaData.
    def enterMetaData(self, ctx:Adl14Parser.MetaDataContext):
        pass

    # Exit a parse tree produced by Adl14Parser#metaData.
    def exitMetaData(self, ctx:Adl14Parser.MetaDataContext):
        pass


    # Enter a parse tree produced by Adl14Parser#metaDataItem.
    def enterMetaDataItem(self, ctx:Adl14Parser.MetaDataItemContext):
        pass

    # Exit a parse tree produced by Adl14Parser#metaDataItem.
    def exitMetaDataItem(self, ctx:Adl14Parser.MetaDataItemContext):
        pass


    # Enter a parse tree produced by Adl14Parser#metaDataValueItem.
    def enterMetaDataValueItem(self, ctx:Adl14Parser.MetaDataValueItemContext):
        pass

    # Exit a parse tree produced by Adl14Parser#metaDataValueItem.
    def exitMetaDataValueItem(self, ctx:Adl14Parser.MetaDataValueItemContext):
        pass


    # Enter a parse tree produced by Adl14Parser#metaDataFlag.
    def enterMetaDataFlag(self, ctx:Adl14Parser.MetaDataFlagContext):
        pass

    # Exit a parse tree produced by Adl14Parser#metaDataFlag.
    def exitMetaDataFlag(self, ctx:Adl14Parser.MetaDataFlagContext):
        pass


    # Enter a parse tree produced by Adl14Parser#metaDataItemValue.
    def enterMetaDataItemValue(self, ctx:Adl14Parser.MetaDataItemValueContext):
        pass

    # Exit a parse tree produced by Adl14Parser#metaDataItemValue.
    def exitMetaDataItemValue(self, ctx:Adl14Parser.MetaDataItemValueContext):
        pass


    # Enter a parse tree produced by Adl14Parser#specializeSection.
    def enterSpecializeSection(self, ctx:Adl14Parser.SpecializeSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#specializeSection.
    def exitSpecializeSection(self, ctx:Adl14Parser.SpecializeSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#conceptSection.
    def enterConceptSection(self, ctx:Adl14Parser.ConceptSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#conceptSection.
    def exitConceptSection(self, ctx:Adl14Parser.ConceptSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#languageSection.
    def enterLanguageSection(self, ctx:Adl14Parser.LanguageSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#languageSection.
    def exitLanguageSection(self, ctx:Adl14Parser.LanguageSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#descriptionSection.
    def enterDescriptionSection(self, ctx:Adl14Parser.DescriptionSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#descriptionSection.
    def exitDescriptionSection(self, ctx:Adl14Parser.DescriptionSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#definitionSection.
    def enterDefinitionSection(self, ctx:Adl14Parser.DefinitionSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#definitionSection.
    def exitDefinitionSection(self, ctx:Adl14Parser.DefinitionSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#rulesSection.
    def enterRulesSection(self, ctx:Adl14Parser.RulesSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#rulesSection.
    def exitRulesSection(self, ctx:Adl14Parser.RulesSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#terminologySection.
    def enterTerminologySection(self, ctx:Adl14Parser.TerminologySectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#terminologySection.
    def exitTerminologySection(self, ctx:Adl14Parser.TerminologySectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#annotationsSection.
    def enterAnnotationsSection(self, ctx:Adl14Parser.AnnotationsSectionContext):
        pass

    # Exit a parse tree produced by Adl14Parser#annotationsSection.
    def exitAnnotationsSection(self, ctx:Adl14Parser.AnnotationsSectionContext):
        pass


    # Enter a parse tree produced by Adl14Parser#odinText.
    def enterOdinText(self, ctx:Adl14Parser.OdinTextContext):
        pass

    # Exit a parse tree produced by Adl14Parser#odinText.
    def exitOdinText(self, ctx:Adl14Parser.OdinTextContext):
        pass


    # Enter a parse tree produced by Adl14Parser#cadlText.
    def enterCadlText(self, ctx:Adl14Parser.CadlTextContext):
        pass

    # Exit a parse tree produced by Adl14Parser#cadlText.
    def exitCadlText(self, ctx:Adl14Parser.CadlTextContext):
        pass


    # Enter a parse tree produced by Adl14Parser#elText.
    def enterElText(self, ctx:Adl14Parser.ElTextContext):
        pass

    # Exit a parse tree produced by Adl14Parser#elText.
    def exitElText(self, ctx:Adl14Parser.ElTextContext):
        pass



del Adl14Parser