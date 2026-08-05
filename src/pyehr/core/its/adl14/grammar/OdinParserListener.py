# Created using Commit 3494da9 from https://github.com/openEHR/openEHR-antlr4
# Generated from OdinParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OdinParser import OdinParser
else:
    from OdinParser import OdinParser

# This class defines a complete listener for a parse tree produced by OdinParser.
class OdinParserListener(ParseTreeListener):

    # Enter a parse tree produced by OdinParser#odinObject.
    def enterOdinObject(self, ctx:OdinParser.OdinObjectContext):
        pass

    # Exit a parse tree produced by OdinParser#odinObject.
    def exitOdinObject(self, ctx:OdinParser.OdinObjectContext):
        pass


    # Enter a parse tree produced by OdinParser#odinAttrVal.
    def enterOdinAttrVal(self, ctx:OdinParser.OdinAttrValContext):
        pass

    # Exit a parse tree produced by OdinParser#odinAttrVal.
    def exitOdinAttrVal(self, ctx:OdinParser.OdinAttrValContext):
        pass


    # Enter a parse tree produced by OdinParser#odinAttrName.
    def enterOdinAttrName(self, ctx:OdinParser.OdinAttrNameContext):
        pass

    # Exit a parse tree produced by OdinParser#odinAttrName.
    def exitOdinAttrName(self, ctx:OdinParser.OdinAttrNameContext):
        pass


    # Enter a parse tree produced by OdinParser#odinObjectBlock.
    def enterOdinObjectBlock(self, ctx:OdinParser.OdinObjectBlockContext):
        pass

    # Exit a parse tree produced by OdinParser#odinObjectBlock.
    def exitOdinObjectBlock(self, ctx:OdinParser.OdinObjectBlockContext):
        pass


    # Enter a parse tree produced by OdinParser#odinObjectValueBlock.
    def enterOdinObjectValueBlock(self, ctx:OdinParser.OdinObjectValueBlockContext):
        pass

    # Exit a parse tree produced by OdinParser#odinObjectValueBlock.
    def exitOdinObjectValueBlock(self, ctx:OdinParser.OdinObjectValueBlockContext):
        pass


    # Enter a parse tree produced by OdinParser#rmTypeSpec.
    def enterRmTypeSpec(self, ctx:OdinParser.RmTypeSpecContext):
        pass

    # Exit a parse tree produced by OdinParser#rmTypeSpec.
    def exitRmTypeSpec(self, ctx:OdinParser.RmTypeSpecContext):
        pass


    # Enter a parse tree produced by OdinParser#odinKeyedObject.
    def enterOdinKeyedObject(self, ctx:OdinParser.OdinKeyedObjectContext):
        pass

    # Exit a parse tree produced by OdinParser#odinKeyedObject.
    def exitOdinKeyedObject(self, ctx:OdinParser.OdinKeyedObjectContext):
        pass


    # Enter a parse tree produced by OdinParser#odinKeySpec.
    def enterOdinKeySpec(self, ctx:OdinParser.OdinKeySpecContext):
        pass

    # Exit a parse tree produced by OdinParser#odinKeySpec.
    def exitOdinKeySpec(self, ctx:OdinParser.OdinKeySpecContext):
        pass


    # Enter a parse tree produced by OdinParser#odinObjectReferenceBlock.
    def enterOdinObjectReferenceBlock(self, ctx:OdinParser.OdinObjectReferenceBlockContext):
        pass

    # Exit a parse tree produced by OdinParser#odinObjectReferenceBlock.
    def exitOdinObjectReferenceBlock(self, ctx:OdinParser.OdinObjectReferenceBlockContext):
        pass


    # Enter a parse tree produced by OdinParser#odinPathList.
    def enterOdinPathList(self, ctx:OdinParser.OdinPathListContext):
        pass

    # Exit a parse tree produced by OdinParser#odinPathList.
    def exitOdinPathList(self, ctx:OdinParser.OdinPathListContext):
        pass


    # Enter a parse tree produced by OdinParser#odinPath.
    def enterOdinPath(self, ctx:OdinParser.OdinPathContext):
        pass

    # Exit a parse tree produced by OdinParser#odinPath.
    def exitOdinPath(self, ctx:OdinParser.OdinPathContext):
        pass


    # Enter a parse tree produced by OdinParser#odinPathSegment.
    def enterOdinPathSegment(self, ctx:OdinParser.OdinPathSegmentContext):
        pass

    # Exit a parse tree produced by OdinParser#odinPathSegment.
    def exitOdinPathSegment(self, ctx:OdinParser.OdinPathSegmentContext):
        pass


    # Enter a parse tree produced by OdinParser#rmTypeId.
    def enterRmTypeId(self, ctx:OdinParser.RmTypeIdContext):
        pass

    # Exit a parse tree produced by OdinParser#rmTypeId.
    def exitRmTypeId(self, ctx:OdinParser.RmTypeIdContext):
        pass


    # Enter a parse tree produced by OdinParser#primitiveObject.
    def enterPrimitiveObject(self, ctx:OdinParser.PrimitiveObjectContext):
        pass

    # Exit a parse tree produced by OdinParser#primitiveObject.
    def exitPrimitiveObject(self, ctx:OdinParser.PrimitiveObjectContext):
        pass


    # Enter a parse tree produced by OdinParser#primitiveValue.
    def enterPrimitiveValue(self, ctx:OdinParser.PrimitiveValueContext):
        pass

    # Exit a parse tree produced by OdinParser#primitiveValue.
    def exitPrimitiveValue(self, ctx:OdinParser.PrimitiveValueContext):
        pass


    # Enter a parse tree produced by OdinParser#primitiveListValue.
    def enterPrimitiveListValue(self, ctx:OdinParser.PrimitiveListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#primitiveListValue.
    def exitPrimitiveListValue(self, ctx:OdinParser.PrimitiveListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#primitiveIntervalValue.
    def enterPrimitiveIntervalValue(self, ctx:OdinParser.PrimitiveIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#primitiveIntervalValue.
    def exitPrimitiveIntervalValue(self, ctx:OdinParser.PrimitiveIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#stringValue.
    def enterStringValue(self, ctx:OdinParser.StringValueContext):
        pass

    # Exit a parse tree produced by OdinParser#stringValue.
    def exitStringValue(self, ctx:OdinParser.StringValueContext):
        pass


    # Enter a parse tree produced by OdinParser#stringListValue.
    def enterStringListValue(self, ctx:OdinParser.StringListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#stringListValue.
    def exitStringListValue(self, ctx:OdinParser.StringListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#integerValue.
    def enterIntegerValue(self, ctx:OdinParser.IntegerValueContext):
        pass

    # Exit a parse tree produced by OdinParser#integerValue.
    def exitIntegerValue(self, ctx:OdinParser.IntegerValueContext):
        pass


    # Enter a parse tree produced by OdinParser#integerListValue.
    def enterIntegerListValue(self, ctx:OdinParser.IntegerListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#integerListValue.
    def exitIntegerListValue(self, ctx:OdinParser.IntegerListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#integerIntervalValue.
    def enterIntegerIntervalValue(self, ctx:OdinParser.IntegerIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#integerIntervalValue.
    def exitIntegerIntervalValue(self, ctx:OdinParser.IntegerIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#integerIntervalListValue.
    def enterIntegerIntervalListValue(self, ctx:OdinParser.IntegerIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#integerIntervalListValue.
    def exitIntegerIntervalListValue(self, ctx:OdinParser.IntegerIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#realValue.
    def enterRealValue(self, ctx:OdinParser.RealValueContext):
        pass

    # Exit a parse tree produced by OdinParser#realValue.
    def exitRealValue(self, ctx:OdinParser.RealValueContext):
        pass


    # Enter a parse tree produced by OdinParser#realListValue.
    def enterRealListValue(self, ctx:OdinParser.RealListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#realListValue.
    def exitRealListValue(self, ctx:OdinParser.RealListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#realIntervalValue.
    def enterRealIntervalValue(self, ctx:OdinParser.RealIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#realIntervalValue.
    def exitRealIntervalValue(self, ctx:OdinParser.RealIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#realIntervalListValue.
    def enterRealIntervalListValue(self, ctx:OdinParser.RealIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#realIntervalListValue.
    def exitRealIntervalListValue(self, ctx:OdinParser.RealIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#booleanValue.
    def enterBooleanValue(self, ctx:OdinParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by OdinParser#booleanValue.
    def exitBooleanValue(self, ctx:OdinParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by OdinParser#booleanListValue.
    def enterBooleanListValue(self, ctx:OdinParser.BooleanListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#booleanListValue.
    def exitBooleanListValue(self, ctx:OdinParser.BooleanListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#characterValue.
    def enterCharacterValue(self, ctx:OdinParser.CharacterValueContext):
        pass

    # Exit a parse tree produced by OdinParser#characterValue.
    def exitCharacterValue(self, ctx:OdinParser.CharacterValueContext):
        pass


    # Enter a parse tree produced by OdinParser#characterListValue.
    def enterCharacterListValue(self, ctx:OdinParser.CharacterListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#characterListValue.
    def exitCharacterListValue(self, ctx:OdinParser.CharacterListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateValue.
    def enterDateValue(self, ctx:OdinParser.DateValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateValue.
    def exitDateValue(self, ctx:OdinParser.DateValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateListValue.
    def enterDateListValue(self, ctx:OdinParser.DateListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateListValue.
    def exitDateListValue(self, ctx:OdinParser.DateListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateIntervalValue.
    def enterDateIntervalValue(self, ctx:OdinParser.DateIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateIntervalValue.
    def exitDateIntervalValue(self, ctx:OdinParser.DateIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateIntervalListValue.
    def enterDateIntervalListValue(self, ctx:OdinParser.DateIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateIntervalListValue.
    def exitDateIntervalListValue(self, ctx:OdinParser.DateIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#timeValue.
    def enterTimeValue(self, ctx:OdinParser.TimeValueContext):
        pass

    # Exit a parse tree produced by OdinParser#timeValue.
    def exitTimeValue(self, ctx:OdinParser.TimeValueContext):
        pass


    # Enter a parse tree produced by OdinParser#timeListValue.
    def enterTimeListValue(self, ctx:OdinParser.TimeListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#timeListValue.
    def exitTimeListValue(self, ctx:OdinParser.TimeListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#timeIntervalValue.
    def enterTimeIntervalValue(self, ctx:OdinParser.TimeIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#timeIntervalValue.
    def exitTimeIntervalValue(self, ctx:OdinParser.TimeIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#timeIntervalListValue.
    def enterTimeIntervalListValue(self, ctx:OdinParser.TimeIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#timeIntervalListValue.
    def exitTimeIntervalListValue(self, ctx:OdinParser.TimeIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateTimeValue.
    def enterDateTimeValue(self, ctx:OdinParser.DateTimeValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateTimeValue.
    def exitDateTimeValue(self, ctx:OdinParser.DateTimeValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateTimeListValue.
    def enterDateTimeListValue(self, ctx:OdinParser.DateTimeListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateTimeListValue.
    def exitDateTimeListValue(self, ctx:OdinParser.DateTimeListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateTimeIntervalValue.
    def enterDateTimeIntervalValue(self, ctx:OdinParser.DateTimeIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateTimeIntervalValue.
    def exitDateTimeIntervalValue(self, ctx:OdinParser.DateTimeIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#dateTimeIntervalListValue.
    def enterDateTimeIntervalListValue(self, ctx:OdinParser.DateTimeIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#dateTimeIntervalListValue.
    def exitDateTimeIntervalListValue(self, ctx:OdinParser.DateTimeIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#durationValue.
    def enterDurationValue(self, ctx:OdinParser.DurationValueContext):
        pass

    # Exit a parse tree produced by OdinParser#durationValue.
    def exitDurationValue(self, ctx:OdinParser.DurationValueContext):
        pass


    # Enter a parse tree produced by OdinParser#durationListValue.
    def enterDurationListValue(self, ctx:OdinParser.DurationListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#durationListValue.
    def exitDurationListValue(self, ctx:OdinParser.DurationListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#durationIntervalValue.
    def enterDurationIntervalValue(self, ctx:OdinParser.DurationIntervalValueContext):
        pass

    # Exit a parse tree produced by OdinParser#durationIntervalValue.
    def exitDurationIntervalValue(self, ctx:OdinParser.DurationIntervalValueContext):
        pass


    # Enter a parse tree produced by OdinParser#durationIntervalListValue.
    def enterDurationIntervalListValue(self, ctx:OdinParser.DurationIntervalListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#durationIntervalListValue.
    def exitDurationIntervalListValue(self, ctx:OdinParser.DurationIntervalListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#termCodeValue.
    def enterTermCodeValue(self, ctx:OdinParser.TermCodeValueContext):
        pass

    # Exit a parse tree produced by OdinParser#termCodeValue.
    def exitTermCodeValue(self, ctx:OdinParser.TermCodeValueContext):
        pass


    # Enter a parse tree produced by OdinParser#termCodeListValue.
    def enterTermCodeListValue(self, ctx:OdinParser.TermCodeListValueContext):
        pass

    # Exit a parse tree produced by OdinParser#termCodeListValue.
    def exitTermCodeListValue(self, ctx:OdinParser.TermCodeListValueContext):
        pass


    # Enter a parse tree produced by OdinParser#relop.
    def enterRelop(self, ctx:OdinParser.RelopContext):
        pass

    # Exit a parse tree produced by OdinParser#relop.
    def exitRelop(self, ctx:OdinParser.RelopContext):
        pass



del OdinParser