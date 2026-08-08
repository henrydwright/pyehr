# Created using Commit 3494da9 from https://github.com/openEHR/openEHR-antlr4
# Generated from Adl14Parser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,57,127,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,1,0,1,0,1,0,1,
        1,1,1,1,1,3,1,45,8,1,1,1,1,1,1,1,1,1,1,1,3,1,52,8,1,1,1,1,1,3,1,
        56,8,1,1,2,3,2,59,8,2,1,2,1,2,1,3,1,3,1,3,1,3,5,3,67,8,3,10,3,12,
        3,70,9,3,1,3,1,3,1,4,1,4,3,4,76,8,4,1,5,1,5,1,5,1,5,1,6,1,6,1,7,
        1,7,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,
        1,12,1,12,1,12,1,13,1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,15,1,16,
        4,16,113,8,16,11,16,12,16,114,1,17,4,17,118,8,17,11,17,12,17,119,
        1,18,4,18,123,8,18,11,18,12,18,124,1,18,0,0,19,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,36,0,1,3,0,7,8,25,25,41,42,116,0,38,
        1,0,0,0,2,41,1,0,0,0,4,58,1,0,0,0,6,62,1,0,0,0,8,75,1,0,0,0,10,77,
        1,0,0,0,12,81,1,0,0,0,14,83,1,0,0,0,16,85,1,0,0,0,18,88,1,0,0,0,
        20,93,1,0,0,0,22,96,1,0,0,0,24,99,1,0,0,0,26,102,1,0,0,0,28,105,
        1,0,0,0,30,108,1,0,0,0,32,112,1,0,0,0,34,117,1,0,0,0,36,122,1,0,
        0,0,38,39,3,2,1,0,39,40,5,0,0,1,40,1,1,0,0,0,41,42,5,4,0,0,42,44,
        3,4,2,0,43,45,3,16,8,0,44,43,1,0,0,0,44,45,1,0,0,0,45,46,1,0,0,0,
        46,47,3,18,9,0,47,48,3,20,10,0,48,49,3,22,11,0,49,51,3,24,12,0,50,
        52,3,26,13,0,51,50,1,0,0,0,51,52,1,0,0,0,52,53,1,0,0,0,53,55,3,28,
        14,0,54,56,3,30,15,0,55,54,1,0,0,0,55,56,1,0,0,0,56,3,1,0,0,0,57,
        59,3,6,3,0,58,57,1,0,0,0,58,59,1,0,0,0,59,60,1,0,0,0,60,61,5,7,0,
        0,61,5,1,0,0,0,62,63,5,37,0,0,63,68,3,8,4,0,64,65,5,40,0,0,65,67,
        3,8,4,0,66,64,1,0,0,0,67,70,1,0,0,0,68,66,1,0,0,0,68,69,1,0,0,0,
        69,71,1,0,0,0,70,68,1,0,0,0,71,72,5,38,0,0,72,7,1,0,0,0,73,76,3,
        10,5,0,74,76,3,12,6,0,75,73,1,0,0,0,75,74,1,0,0,0,76,9,1,0,0,0,77,
        78,5,41,0,0,78,79,5,39,0,0,79,80,3,14,7,0,80,11,1,0,0,0,81,82,5,
        41,0,0,82,13,1,0,0,0,83,84,7,0,0,0,84,15,1,0,0,0,85,86,5,35,0,0,
        86,87,5,7,0,0,87,17,1,0,0,0,88,89,5,36,0,0,89,90,5,48,0,0,90,91,
        5,17,0,0,91,92,5,49,0,0,92,19,1,0,0,0,93,94,5,46,0,0,94,95,3,32,
        16,0,95,21,1,0,0,0,96,97,5,50,0,0,97,98,3,32,16,0,98,23,1,0,0,0,
        99,100,5,52,0,0,100,101,3,34,17,0,101,25,1,0,0,0,102,103,5,53,0,
        0,103,104,3,36,18,0,104,27,1,0,0,0,105,106,5,54,0,0,106,107,3,32,
        16,0,107,29,1,0,0,0,108,109,5,57,0,0,109,110,3,32,16,0,110,31,1,
        0,0,0,111,113,5,51,0,0,112,111,1,0,0,0,113,114,1,0,0,0,114,112,1,
        0,0,0,114,115,1,0,0,0,115,33,1,0,0,0,116,118,5,55,0,0,117,116,1,
        0,0,0,118,119,1,0,0,0,119,117,1,0,0,0,119,120,1,0,0,0,120,35,1,0,
        0,0,121,123,5,56,0,0,122,121,1,0,0,0,123,124,1,0,0,0,124,122,1,0,
        0,0,124,125,1,0,0,0,125,37,1,0,0,0,9,44,51,55,58,68,75,114,119,124
    ]

class Adl14Parser ( Parser ):

    grammarFileName = "Adl14Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'archetype'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'('", "<INVALID>", "'='", "';'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "CMT_LINE", "EOL", "WS", "SYM_ARCHETYPE", 
                      "OBJECT_VERSION_ID", "ARCHETYPE_HRID", "ARCHETYPE_REF", 
                      "VERSION_ID", "FULLY_QUALIFIED_RM_ENTITY", "QUALIFIED_TERM_CODE_ID", 
                      "LOCAL_TERM_CODE_ID", "QUALIFIED_TERM_CODE_REF", "ROOT_ID_CODE", 
                      "ID_CODE", "AT_CODE", "AC_CODE", "ADL14_AT_CODE", 
                      "ADL14_AC_CODE", "ISO8601_DATE_AUGMENTED", "ISO8601_TIME_AUGMENTED", 
                      "ISO8601_DATE_TIME_AUGMENTED", "ISO8601_DURATION", 
                      "SYM_TRUE", "SYM_FALSE", "GUID", "UUID", "INTEGER", 
                      "REAL", "REAL_PERCENT", "SCI_INTEGER", "SCI_REAL", 
                      "STRING", "CHARACTER", "WS_H", "SPECIALIZE_HEADER", 
                      "CONCEPT_HEADER", "METADATA_START", "METADATA_END", 
                      "SYM_EQ", "SYM_SEMI_COLON", "ALPHANUM_ID", "OID", 
                      "EOL_H", "WS_S", "EOL_S", "LANGUAGE_HEADER", "EOL_C", 
                      "SYM_LBRACKET", "SYM_RBRACKET", "DESCRIPTION_HEADER", 
                      "ODIN_LINE", "DEFINITION_HEADER", "RULES_HEADER", 
                      "TERMINOLOGY_HEADER", "CADL_LINE", "EL_LINE", "ANNOTATIONS_HEADER" ]

    RULE_adlObject = 0
    RULE_authoredArchetype = 1
    RULE_header = 2
    RULE_metaData = 3
    RULE_metaDataItem = 4
    RULE_metaDataValueItem = 5
    RULE_metaDataFlag = 6
    RULE_metaDataItemValue = 7
    RULE_specializeSection = 8
    RULE_conceptSection = 9
    RULE_languageSection = 10
    RULE_descriptionSection = 11
    RULE_definitionSection = 12
    RULE_rulesSection = 13
    RULE_terminologySection = 14
    RULE_annotationsSection = 15
    RULE_odinText = 16
    RULE_cadlText = 17
    RULE_elText = 18

    ruleNames =  [ "adlObject", "authoredArchetype", "header", "metaData", 
                   "metaDataItem", "metaDataValueItem", "metaDataFlag", 
                   "metaDataItemValue", "specializeSection", "conceptSection", 
                   "languageSection", "descriptionSection", "definitionSection", 
                   "rulesSection", "terminologySection", "annotationsSection", 
                   "odinText", "cadlText", "elText" ]

    EOF = Token.EOF
    CMT_LINE=1
    EOL=2
    WS=3
    SYM_ARCHETYPE=4
    OBJECT_VERSION_ID=5
    ARCHETYPE_HRID=6
    ARCHETYPE_REF=7
    VERSION_ID=8
    FULLY_QUALIFIED_RM_ENTITY=9
    QUALIFIED_TERM_CODE_ID=10
    LOCAL_TERM_CODE_ID=11
    QUALIFIED_TERM_CODE_REF=12
    ROOT_ID_CODE=13
    ID_CODE=14
    AT_CODE=15
    AC_CODE=16
    ADL14_AT_CODE=17
    ADL14_AC_CODE=18
    ISO8601_DATE_AUGMENTED=19
    ISO8601_TIME_AUGMENTED=20
    ISO8601_DATE_TIME_AUGMENTED=21
    ISO8601_DURATION=22
    SYM_TRUE=23
    SYM_FALSE=24
    GUID=25
    UUID=26
    INTEGER=27
    REAL=28
    REAL_PERCENT=29
    SCI_INTEGER=30
    SCI_REAL=31
    STRING=32
    CHARACTER=33
    WS_H=34
    SPECIALIZE_HEADER=35
    CONCEPT_HEADER=36
    METADATA_START=37
    METADATA_END=38
    SYM_EQ=39
    SYM_SEMI_COLON=40
    ALPHANUM_ID=41
    OID=42
    EOL_H=43
    WS_S=44
    EOL_S=45
    LANGUAGE_HEADER=46
    EOL_C=47
    SYM_LBRACKET=48
    SYM_RBRACKET=49
    DESCRIPTION_HEADER=50
    ODIN_LINE=51
    DEFINITION_HEADER=52
    RULES_HEADER=53
    TERMINOLOGY_HEADER=54
    CADL_LINE=55
    EL_LINE=56
    ANNOTATIONS_HEADER=57

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class AdlObjectContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def authoredArchetype(self):
            return self.getTypedRuleContext(Adl14Parser.AuthoredArchetypeContext,0)


        def EOF(self):
            return self.getToken(Adl14Parser.EOF, 0)

        def getRuleIndex(self):
            return Adl14Parser.RULE_adlObject

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdlObject" ):
                listener.enterAdlObject(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdlObject" ):
                listener.exitAdlObject(self)




    def adlObject(self):

        localctx = Adl14Parser.AdlObjectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_adlObject)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.authoredArchetype()
            self.state = 39
            self.match(Adl14Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AuthoredArchetypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_ARCHETYPE(self):
            return self.getToken(Adl14Parser.SYM_ARCHETYPE, 0)

        def header(self):
            return self.getTypedRuleContext(Adl14Parser.HeaderContext,0)


        def conceptSection(self):
            return self.getTypedRuleContext(Adl14Parser.ConceptSectionContext,0)


        def languageSection(self):
            return self.getTypedRuleContext(Adl14Parser.LanguageSectionContext,0)


        def descriptionSection(self):
            return self.getTypedRuleContext(Adl14Parser.DescriptionSectionContext,0)


        def definitionSection(self):
            return self.getTypedRuleContext(Adl14Parser.DefinitionSectionContext,0)


        def terminologySection(self):
            return self.getTypedRuleContext(Adl14Parser.TerminologySectionContext,0)


        def specializeSection(self):
            return self.getTypedRuleContext(Adl14Parser.SpecializeSectionContext,0)


        def rulesSection(self):
            return self.getTypedRuleContext(Adl14Parser.RulesSectionContext,0)


        def annotationsSection(self):
            return self.getTypedRuleContext(Adl14Parser.AnnotationsSectionContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_authoredArchetype

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAuthoredArchetype" ):
                listener.enterAuthoredArchetype(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAuthoredArchetype" ):
                listener.exitAuthoredArchetype(self)




    def authoredArchetype(self):

        localctx = Adl14Parser.AuthoredArchetypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_authoredArchetype)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(Adl14Parser.SYM_ARCHETYPE)
            self.state = 42
            self.header()
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 43
                self.specializeSection()


            self.state = 46
            self.conceptSection()
            self.state = 47
            self.languageSection()
            self.state = 48
            self.descriptionSection()
            self.state = 49
            self.definitionSection()
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==53:
                self.state = 50
                self.rulesSection()


            self.state = 53
            self.terminologySection()
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 54
                self.annotationsSection()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARCHETYPE_REF(self):
            return self.getToken(Adl14Parser.ARCHETYPE_REF, 0)

        def metaData(self):
            return self.getTypedRuleContext(Adl14Parser.MetaDataContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHeader" ):
                listener.enterHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHeader" ):
                listener.exitHeader(self)




    def header(self):

        localctx = Adl14Parser.HeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 57
                self.metaData()


            self.state = 60
            self.match(Adl14Parser.ARCHETYPE_REF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaDataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def METADATA_START(self):
            return self.getToken(Adl14Parser.METADATA_START, 0)

        def metaDataItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Adl14Parser.MetaDataItemContext)
            else:
                return self.getTypedRuleContext(Adl14Parser.MetaDataItemContext,i)


        def METADATA_END(self):
            return self.getToken(Adl14Parser.METADATA_END, 0)

        def SYM_SEMI_COLON(self, i:int=None):
            if i is None:
                return self.getTokens(Adl14Parser.SYM_SEMI_COLON)
            else:
                return self.getToken(Adl14Parser.SYM_SEMI_COLON, i)

        def getRuleIndex(self):
            return Adl14Parser.RULE_metaData

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaData" ):
                listener.enterMetaData(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaData" ):
                listener.exitMetaData(self)




    def metaData(self):

        localctx = Adl14Parser.MetaDataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_metaData)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(Adl14Parser.METADATA_START)
            self.state = 63
            self.metaDataItem()
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 64
                self.match(Adl14Parser.SYM_SEMI_COLON)
                self.state = 65
                self.metaDataItem()
                self.state = 70
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 71
            self.match(Adl14Parser.METADATA_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaDataItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def metaDataValueItem(self):
            return self.getTypedRuleContext(Adl14Parser.MetaDataValueItemContext,0)


        def metaDataFlag(self):
            return self.getTypedRuleContext(Adl14Parser.MetaDataFlagContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_metaDataItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaDataItem" ):
                listener.enterMetaDataItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaDataItem" ):
                listener.exitMetaDataItem(self)




    def metaDataItem(self):

        localctx = Adl14Parser.MetaDataItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_metaDataItem)
        try:
            self.state = 75
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.metaDataValueItem()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 74
                self.metaDataFlag()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaDataValueItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ALPHANUM_ID(self):
            return self.getToken(Adl14Parser.ALPHANUM_ID, 0)

        def SYM_EQ(self):
            return self.getToken(Adl14Parser.SYM_EQ, 0)

        def metaDataItemValue(self):
            return self.getTypedRuleContext(Adl14Parser.MetaDataItemValueContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_metaDataValueItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaDataValueItem" ):
                listener.enterMetaDataValueItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaDataValueItem" ):
                listener.exitMetaDataValueItem(self)




    def metaDataValueItem(self):

        localctx = Adl14Parser.MetaDataValueItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_metaDataValueItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(Adl14Parser.ALPHANUM_ID)
            self.state = 78
            self.match(Adl14Parser.SYM_EQ)
            self.state = 79
            self.metaDataItemValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaDataFlagContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ALPHANUM_ID(self):
            return self.getToken(Adl14Parser.ALPHANUM_ID, 0)

        def getRuleIndex(self):
            return Adl14Parser.RULE_metaDataFlag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaDataFlag" ):
                listener.enterMetaDataFlag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaDataFlag" ):
                listener.exitMetaDataFlag(self)




    def metaDataFlag(self):

        localctx = Adl14Parser.MetaDataFlagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_metaDataFlag)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(Adl14Parser.ALPHANUM_ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaDataItemValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARCHETYPE_REF(self):
            return self.getToken(Adl14Parser.ARCHETYPE_REF, 0)

        def GUID(self):
            return self.getToken(Adl14Parser.GUID, 0)

        def VERSION_ID(self):
            return self.getToken(Adl14Parser.VERSION_ID, 0)

        def ALPHANUM_ID(self):
            return self.getToken(Adl14Parser.ALPHANUM_ID, 0)

        def OID(self):
            return self.getToken(Adl14Parser.OID, 0)

        def getRuleIndex(self):
            return Adl14Parser.RULE_metaDataItemValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaDataItemValue" ):
                listener.enterMetaDataItemValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaDataItemValue" ):
                listener.exitMetaDataItemValue(self)




    def metaDataItemValue(self):

        localctx = Adl14Parser.MetaDataItemValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_metaDataItemValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 6597103321472) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpecializeSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPECIALIZE_HEADER(self):
            return self.getToken(Adl14Parser.SPECIALIZE_HEADER, 0)

        def ARCHETYPE_REF(self):
            return self.getToken(Adl14Parser.ARCHETYPE_REF, 0)

        def getRuleIndex(self):
            return Adl14Parser.RULE_specializeSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpecializeSection" ):
                listener.enterSpecializeSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpecializeSection" ):
                listener.exitSpecializeSection(self)




    def specializeSection(self):

        localctx = Adl14Parser.SpecializeSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_specializeSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(Adl14Parser.SPECIALIZE_HEADER)
            self.state = 86
            self.match(Adl14Parser.ARCHETYPE_REF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConceptSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONCEPT_HEADER(self):
            return self.getToken(Adl14Parser.CONCEPT_HEADER, 0)

        def SYM_LBRACKET(self):
            return self.getToken(Adl14Parser.SYM_LBRACKET, 0)

        def ADL14_AT_CODE(self):
            return self.getToken(Adl14Parser.ADL14_AT_CODE, 0)

        def SYM_RBRACKET(self):
            return self.getToken(Adl14Parser.SYM_RBRACKET, 0)

        def getRuleIndex(self):
            return Adl14Parser.RULE_conceptSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConceptSection" ):
                listener.enterConceptSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConceptSection" ):
                listener.exitConceptSection(self)




    def conceptSection(self):

        localctx = Adl14Parser.ConceptSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_conceptSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(Adl14Parser.CONCEPT_HEADER)
            self.state = 89
            self.match(Adl14Parser.SYM_LBRACKET)
            self.state = 90
            self.match(Adl14Parser.ADL14_AT_CODE)
            self.state = 91
            self.match(Adl14Parser.SYM_RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LanguageSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LANGUAGE_HEADER(self):
            return self.getToken(Adl14Parser.LANGUAGE_HEADER, 0)

        def odinText(self):
            return self.getTypedRuleContext(Adl14Parser.OdinTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_languageSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLanguageSection" ):
                listener.enterLanguageSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLanguageSection" ):
                listener.exitLanguageSection(self)




    def languageSection(self):

        localctx = Adl14Parser.LanguageSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_languageSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.match(Adl14Parser.LANGUAGE_HEADER)
            self.state = 94
            self.odinText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DescriptionSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DESCRIPTION_HEADER(self):
            return self.getToken(Adl14Parser.DESCRIPTION_HEADER, 0)

        def odinText(self):
            return self.getTypedRuleContext(Adl14Parser.OdinTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_descriptionSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDescriptionSection" ):
                listener.enterDescriptionSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDescriptionSection" ):
                listener.exitDescriptionSection(self)




    def descriptionSection(self):

        localctx = Adl14Parser.DescriptionSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_descriptionSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(Adl14Parser.DESCRIPTION_HEADER)
            self.state = 97
            self.odinText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFINITION_HEADER(self):
            return self.getToken(Adl14Parser.DEFINITION_HEADER, 0)

        def cadlText(self):
            return self.getTypedRuleContext(Adl14Parser.CadlTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_definitionSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinitionSection" ):
                listener.enterDefinitionSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinitionSection" ):
                listener.exitDefinitionSection(self)




    def definitionSection(self):

        localctx = Adl14Parser.DefinitionSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_definitionSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(Adl14Parser.DEFINITION_HEADER)
            self.state = 100
            self.cadlText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RulesSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULES_HEADER(self):
            return self.getToken(Adl14Parser.RULES_HEADER, 0)

        def elText(self):
            return self.getTypedRuleContext(Adl14Parser.ElTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_rulesSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRulesSection" ):
                listener.enterRulesSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRulesSection" ):
                listener.exitRulesSection(self)




    def rulesSection(self):

        localctx = Adl14Parser.RulesSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_rulesSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(Adl14Parser.RULES_HEADER)
            self.state = 103
            self.elText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TerminologySectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TERMINOLOGY_HEADER(self):
            return self.getToken(Adl14Parser.TERMINOLOGY_HEADER, 0)

        def odinText(self):
            return self.getTypedRuleContext(Adl14Parser.OdinTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_terminologySection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminologySection" ):
                listener.enterTerminologySection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminologySection" ):
                listener.exitTerminologySection(self)




    def terminologySection(self):

        localctx = Adl14Parser.TerminologySectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_terminologySection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(Adl14Parser.TERMINOLOGY_HEADER)
            self.state = 106
            self.odinText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnnotationsSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ANNOTATIONS_HEADER(self):
            return self.getToken(Adl14Parser.ANNOTATIONS_HEADER, 0)

        def odinText(self):
            return self.getTypedRuleContext(Adl14Parser.OdinTextContext,0)


        def getRuleIndex(self):
            return Adl14Parser.RULE_annotationsSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnnotationsSection" ):
                listener.enterAnnotationsSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnnotationsSection" ):
                listener.exitAnnotationsSection(self)




    def annotationsSection(self):

        localctx = Adl14Parser.AnnotationsSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_annotationsSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.match(Adl14Parser.ANNOTATIONS_HEADER)
            self.state = 109
            self.odinText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ODIN_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(Adl14Parser.ODIN_LINE)
            else:
                return self.getToken(Adl14Parser.ODIN_LINE, i)

        def getRuleIndex(self):
            return Adl14Parser.RULE_odinText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinText" ):
                listener.enterOdinText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinText" ):
                listener.exitOdinText(self)




    def odinText(self):

        localctx = Adl14Parser.OdinTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_odinText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 111
                self.match(Adl14Parser.ODIN_LINE)
                self.state = 114 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==51):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CadlTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CADL_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(Adl14Parser.CADL_LINE)
            else:
                return self.getToken(Adl14Parser.CADL_LINE, i)

        def getRuleIndex(self):
            return Adl14Parser.RULE_cadlText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCadlText" ):
                listener.enterCadlText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCadlText" ):
                listener.exitCadlText(self)




    def cadlText(self):

        localctx = Adl14Parser.CadlTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_cadlText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 116
                self.match(Adl14Parser.CADL_LINE)
                self.state = 119 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==55):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EL_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(Adl14Parser.EL_LINE)
            else:
                return self.getToken(Adl14Parser.EL_LINE, i)

        def getRuleIndex(self):
            return Adl14Parser.RULE_elText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElText" ):
                listener.enterElText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElText" ):
                listener.exitElText(self)




    def elText(self):

        localctx = Adl14Parser.ElTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_elText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 121
                self.match(Adl14Parser.EL_LINE)
                self.state = 124 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==56):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





