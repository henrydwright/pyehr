# Created using Commit 3494da9 from https://github.com/openEHR/openEHR-antlr4
# Generated from OdinParser.g4 by ANTLR 4.13.2
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
        4,1,63,604,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,1,0,4,0,102,8,0,11,0,12,0,103,
        1,0,3,0,107,8,0,1,0,3,0,110,8,0,1,1,1,1,1,1,1,1,3,1,116,8,1,1,2,
        1,2,1,3,1,3,3,3,122,8,3,1,4,3,4,125,8,4,1,4,1,4,1,4,4,4,130,8,4,
        11,4,12,4,131,1,4,4,4,135,8,4,11,4,12,4,136,1,4,3,4,140,8,4,1,4,
        1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,8,1,8,1,8,
        1,8,1,9,1,9,1,9,1,9,1,9,4,9,165,8,9,11,9,12,9,166,3,9,169,8,9,1,
        10,3,10,172,8,10,1,10,4,10,175,8,10,11,10,12,10,176,1,11,1,11,1,
        11,3,11,182,8,11,1,12,1,12,1,12,1,12,1,12,5,12,189,8,12,10,12,12,
        12,192,9,12,1,12,1,12,3,12,196,8,12,1,13,1,13,1,13,3,13,201,8,13,
        1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,14,213,8,14,
        1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,3,15,225,8,15,
        1,16,1,16,1,16,1,16,1,16,1,16,3,16,233,8,16,1,17,1,17,1,18,1,18,
        1,18,4,18,240,8,18,11,18,12,18,241,1,18,1,18,3,18,246,8,18,1,19,
        3,19,249,8,19,1,19,1,19,1,20,1,20,1,20,4,20,256,8,20,11,20,12,20,
        257,1,20,1,20,3,20,262,8,20,1,21,1,21,3,21,266,8,21,1,21,1,21,1,
        21,3,21,271,8,21,1,21,1,21,1,21,1,21,1,21,3,21,278,8,21,1,21,1,21,
        1,21,1,21,1,21,1,21,1,21,1,21,1,21,3,21,289,8,21,1,22,1,22,1,22,
        4,22,294,8,22,11,22,12,22,295,1,22,1,22,3,22,300,8,22,1,23,3,23,
        303,8,23,1,23,1,23,1,24,1,24,1,24,4,24,310,8,24,11,24,12,24,311,
        1,24,1,24,3,24,316,8,24,1,25,1,25,3,25,320,8,25,1,25,1,25,1,25,3,
        25,325,8,25,1,25,1,25,1,25,1,25,1,25,3,25,332,8,25,1,25,1,25,1,25,
        1,25,1,25,1,25,1,25,1,25,1,25,3,25,343,8,25,1,26,1,26,1,26,4,26,
        348,8,26,11,26,12,26,349,1,26,1,26,3,26,354,8,26,1,27,1,27,1,28,
        1,28,1,28,4,28,361,8,28,11,28,12,28,362,1,28,1,28,3,28,367,8,28,
        1,29,1,29,1,30,1,30,1,30,4,30,374,8,30,11,30,12,30,375,1,30,1,30,
        3,30,380,8,30,1,31,1,31,1,32,1,32,1,32,4,32,387,8,32,11,32,12,32,
        388,1,32,1,32,3,32,393,8,32,1,33,1,33,3,33,397,8,33,1,33,1,33,1,
        33,3,33,402,8,33,1,33,1,33,1,33,1,33,1,33,3,33,409,8,33,1,33,1,33,
        1,33,1,33,1,33,1,33,1,33,1,33,1,33,3,33,420,8,33,1,34,1,34,1,34,
        4,34,425,8,34,11,34,12,34,426,1,34,1,34,3,34,431,8,34,1,35,1,35,
        1,36,1,36,1,36,4,36,438,8,36,11,36,12,36,439,1,36,1,36,3,36,444,
        8,36,1,37,1,37,3,37,448,8,37,1,37,1,37,1,37,3,37,453,8,37,1,37,1,
        37,1,37,1,37,1,37,3,37,460,8,37,1,37,1,37,1,37,1,37,1,37,1,37,1,
        37,1,37,1,37,3,37,471,8,37,1,38,1,38,1,38,4,38,476,8,38,11,38,12,
        38,477,1,38,1,38,3,38,482,8,38,1,39,1,39,1,40,1,40,1,40,4,40,489,
        8,40,11,40,12,40,490,1,40,1,40,3,40,495,8,40,1,41,1,41,3,41,499,
        8,41,1,41,1,41,1,41,3,41,504,8,41,1,41,1,41,1,41,1,41,1,41,3,41,
        511,8,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,3,41,522,8,
        41,1,42,1,42,1,42,4,42,527,8,42,11,42,12,42,528,1,42,1,42,3,42,533,
        8,42,1,43,3,43,536,8,43,1,43,1,43,1,44,1,44,1,44,4,44,543,8,44,11,
        44,12,44,544,1,44,1,44,3,44,549,8,44,1,45,1,45,3,45,553,8,45,1,45,
        1,45,1,45,3,45,558,8,45,1,45,1,45,1,45,1,45,1,45,3,45,565,8,45,1,
        45,1,45,1,45,1,45,1,45,1,45,1,45,1,45,1,45,3,45,576,8,45,1,46,1,
        46,1,46,4,46,581,8,46,11,46,12,46,582,1,46,1,46,3,46,587,8,46,1,
        47,1,47,1,48,1,48,1,48,4,48,594,8,48,11,48,12,48,595,1,48,1,48,3,
        48,600,8,48,1,49,1,49,1,49,0,0,50,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,
        68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,0,6,1,0,61,62,1,
        0,44,45,2,0,28,28,31,31,2,0,29,29,32,32,1,0,24,25,1,0,37,40,663,
        0,106,1,0,0,0,2,111,1,0,0,0,4,117,1,0,0,0,6,121,1,0,0,0,8,124,1,
        0,0,0,10,143,1,0,0,0,12,147,1,0,0,0,14,151,1,0,0,0,16,155,1,0,0,
        0,18,159,1,0,0,0,20,171,1,0,0,0,22,178,1,0,0,0,24,183,1,0,0,0,26,
        200,1,0,0,0,28,212,1,0,0,0,30,224,1,0,0,0,32,232,1,0,0,0,34,234,
        1,0,0,0,36,236,1,0,0,0,38,248,1,0,0,0,40,252,1,0,0,0,42,288,1,0,
        0,0,44,290,1,0,0,0,46,302,1,0,0,0,48,306,1,0,0,0,50,342,1,0,0,0,
        52,344,1,0,0,0,54,355,1,0,0,0,56,357,1,0,0,0,58,368,1,0,0,0,60,370,
        1,0,0,0,62,381,1,0,0,0,64,383,1,0,0,0,66,419,1,0,0,0,68,421,1,0,
        0,0,70,432,1,0,0,0,72,434,1,0,0,0,74,470,1,0,0,0,76,472,1,0,0,0,
        78,483,1,0,0,0,80,485,1,0,0,0,82,521,1,0,0,0,84,523,1,0,0,0,86,535,
        1,0,0,0,88,539,1,0,0,0,90,575,1,0,0,0,92,577,1,0,0,0,94,588,1,0,
        0,0,96,590,1,0,0,0,98,601,1,0,0,0,100,102,3,2,1,0,101,100,1,0,0,
        0,102,103,1,0,0,0,103,101,1,0,0,0,103,104,1,0,0,0,104,107,1,0,0,
        0,105,107,3,8,4,0,106,101,1,0,0,0,106,105,1,0,0,0,107,109,1,0,0,
        0,108,110,5,0,0,1,109,108,1,0,0,0,109,110,1,0,0,0,110,1,1,0,0,0,
        111,112,3,4,2,0,112,113,5,42,0,0,113,115,3,6,3,0,114,116,5,53,0,
        0,115,114,1,0,0,0,115,116,1,0,0,0,116,3,1,0,0,0,117,118,7,0,0,0,
        118,5,1,0,0,0,119,122,3,8,4,0,120,122,3,16,8,0,121,119,1,0,0,0,121,
        120,1,0,0,0,122,7,1,0,0,0,123,125,3,10,5,0,124,123,1,0,0,0,124,125,
        1,0,0,0,125,126,1,0,0,0,126,139,5,40,0,0,127,140,3,26,13,0,128,130,
        3,2,1,0,129,128,1,0,0,0,130,131,1,0,0,0,131,129,1,0,0,0,131,132,
        1,0,0,0,132,140,1,0,0,0,133,135,3,12,6,0,134,133,1,0,0,0,135,136,
        1,0,0,0,136,134,1,0,0,0,136,137,1,0,0,0,137,140,1,0,0,0,138,140,
        5,4,0,0,139,127,1,0,0,0,139,129,1,0,0,0,139,134,1,0,0,0,139,138,
        1,0,0,0,139,140,1,0,0,0,140,141,1,0,0,0,141,142,5,39,0,0,142,9,1,
        0,0,0,143,144,5,55,0,0,144,145,3,24,12,0,145,146,5,56,0,0,146,11,
        1,0,0,0,147,148,3,14,7,0,148,149,5,42,0,0,149,150,3,6,3,0,150,13,
        1,0,0,0,151,152,5,57,0,0,152,153,3,28,14,0,153,154,5,58,0,0,154,
        15,1,0,0,0,155,156,5,40,0,0,156,157,3,18,9,0,157,158,5,39,0,0,158,
        17,1,0,0,0,159,168,3,20,10,0,160,161,5,50,0,0,161,169,5,5,0,0,162,
        163,5,50,0,0,163,165,3,20,10,0,164,162,1,0,0,0,165,166,1,0,0,0,166,
        164,1,0,0,0,166,167,1,0,0,0,167,169,1,0,0,0,168,160,1,0,0,0,168,
        164,1,0,0,0,168,169,1,0,0,0,169,19,1,0,0,0,170,172,3,14,7,0,171,
        170,1,0,0,0,171,172,1,0,0,0,172,174,1,0,0,0,173,175,3,22,11,0,174,
        173,1,0,0,0,175,176,1,0,0,0,176,174,1,0,0,0,176,177,1,0,0,0,177,
        21,1,0,0,0,178,179,5,51,0,0,179,181,5,62,0,0,180,182,3,14,7,0,181,
        180,1,0,0,0,181,182,1,0,0,0,182,23,1,0,0,0,183,195,5,61,0,0,184,
        185,5,40,0,0,185,190,3,24,12,0,186,187,5,50,0,0,187,189,3,24,12,
        0,188,186,1,0,0,0,189,192,1,0,0,0,190,188,1,0,0,0,190,191,1,0,0,
        0,191,193,1,0,0,0,192,190,1,0,0,0,193,194,5,39,0,0,194,196,1,0,0,
        0,195,184,1,0,0,0,195,196,1,0,0,0,196,25,1,0,0,0,197,201,3,28,14,
        0,198,201,3,30,15,0,199,201,3,32,16,0,200,197,1,0,0,0,200,198,1,
        0,0,0,200,199,1,0,0,0,201,27,1,0,0,0,202,213,3,34,17,0,203,213,3,
        38,19,0,204,213,3,46,23,0,205,213,3,54,27,0,206,213,3,58,29,0,207,
        213,3,94,47,0,208,213,3,62,31,0,209,213,3,70,35,0,210,213,3,78,39,
        0,211,213,3,86,43,0,212,202,1,0,0,0,212,203,1,0,0,0,212,204,1,0,
        0,0,212,205,1,0,0,0,212,206,1,0,0,0,212,207,1,0,0,0,212,208,1,0,
        0,0,212,209,1,0,0,0,212,210,1,0,0,0,212,211,1,0,0,0,213,29,1,0,0,
        0,214,225,3,36,18,0,215,225,3,40,20,0,216,225,3,48,24,0,217,225,
        3,56,28,0,218,225,3,60,30,0,219,225,3,96,48,0,220,225,3,64,32,0,
        221,225,3,72,36,0,222,225,3,80,40,0,223,225,3,88,44,0,224,214,1,
        0,0,0,224,215,1,0,0,0,224,216,1,0,0,0,224,217,1,0,0,0,224,218,1,
        0,0,0,224,219,1,0,0,0,224,220,1,0,0,0,224,221,1,0,0,0,224,222,1,
        0,0,0,224,223,1,0,0,0,225,31,1,0,0,0,226,233,3,42,21,0,227,233,3,
        50,25,0,228,233,3,66,33,0,229,233,3,74,37,0,230,233,3,82,41,0,231,
        233,3,90,45,0,232,226,1,0,0,0,232,227,1,0,0,0,232,228,1,0,0,0,232,
        229,1,0,0,0,232,230,1,0,0,0,232,231,1,0,0,0,233,33,1,0,0,0,234,235,
        5,33,0,0,235,35,1,0,0,0,236,245,3,34,17,0,237,238,5,50,0,0,238,240,
        3,34,17,0,239,237,1,0,0,0,240,241,1,0,0,0,241,239,1,0,0,0,241,242,
        1,0,0,0,242,246,1,0,0,0,243,244,5,50,0,0,244,246,5,5,0,0,245,239,
        1,0,0,0,245,243,1,0,0,0,246,37,1,0,0,0,247,249,7,1,0,0,248,247,1,
        0,0,0,248,249,1,0,0,0,249,250,1,0,0,0,250,251,7,2,0,0,251,39,1,0,
        0,0,252,261,3,38,19,0,253,254,5,50,0,0,254,256,3,38,19,0,255,253,
        1,0,0,0,256,257,1,0,0,0,257,255,1,0,0,0,257,258,1,0,0,0,258,262,
        1,0,0,0,259,260,5,50,0,0,260,262,5,5,0,0,261,255,1,0,0,0,261,259,
        1,0,0,0,262,41,1,0,0,0,263,265,5,48,0,0,264,266,5,39,0,0,265,264,
        1,0,0,0,265,266,1,0,0,0,266,267,1,0,0,0,267,268,3,38,19,0,268,270,
        5,36,0,0,269,271,5,40,0,0,270,269,1,0,0,0,270,271,1,0,0,0,271,272,
        1,0,0,0,272,273,3,38,19,0,273,274,5,48,0,0,274,289,1,0,0,0,275,277,
        5,48,0,0,276,278,3,98,49,0,277,276,1,0,0,0,277,278,1,0,0,0,278,279,
        1,0,0,0,279,280,3,38,19,0,280,281,5,48,0,0,281,289,1,0,0,0,282,283,
        5,48,0,0,283,284,3,38,19,0,284,285,5,43,0,0,285,286,3,38,19,0,286,
        287,5,48,0,0,287,289,1,0,0,0,288,263,1,0,0,0,288,275,1,0,0,0,288,
        282,1,0,0,0,289,43,1,0,0,0,290,299,3,42,21,0,291,292,5,50,0,0,292,
        294,3,42,21,0,293,291,1,0,0,0,294,295,1,0,0,0,295,293,1,0,0,0,295,
        296,1,0,0,0,296,300,1,0,0,0,297,298,5,50,0,0,298,300,5,5,0,0,299,
        293,1,0,0,0,299,297,1,0,0,0,300,45,1,0,0,0,301,303,7,1,0,0,302,301,
        1,0,0,0,302,303,1,0,0,0,303,304,1,0,0,0,304,305,7,3,0,0,305,47,1,
        0,0,0,306,315,3,46,23,0,307,308,5,50,0,0,308,310,3,46,23,0,309,307,
        1,0,0,0,310,311,1,0,0,0,311,309,1,0,0,0,311,312,1,0,0,0,312,316,
        1,0,0,0,313,314,5,50,0,0,314,316,5,5,0,0,315,309,1,0,0,0,315,313,
        1,0,0,0,316,49,1,0,0,0,317,319,5,48,0,0,318,320,5,39,0,0,319,318,
        1,0,0,0,319,320,1,0,0,0,320,321,1,0,0,0,321,322,3,46,23,0,322,324,
        5,36,0,0,323,325,5,40,0,0,324,323,1,0,0,0,324,325,1,0,0,0,325,326,
        1,0,0,0,326,327,3,46,23,0,327,328,5,48,0,0,328,343,1,0,0,0,329,331,
        5,48,0,0,330,332,3,98,49,0,331,330,1,0,0,0,331,332,1,0,0,0,332,333,
        1,0,0,0,333,334,3,46,23,0,334,335,5,48,0,0,335,343,1,0,0,0,336,337,
        5,48,0,0,337,338,3,46,23,0,338,339,5,43,0,0,339,340,3,46,23,0,340,
        341,5,48,0,0,341,343,1,0,0,0,342,317,1,0,0,0,342,329,1,0,0,0,342,
        336,1,0,0,0,343,51,1,0,0,0,344,353,3,50,25,0,345,346,5,50,0,0,346,
        348,3,50,25,0,347,345,1,0,0,0,348,349,1,0,0,0,349,347,1,0,0,0,349,
        350,1,0,0,0,350,354,1,0,0,0,351,352,5,50,0,0,352,354,5,5,0,0,353,
        347,1,0,0,0,353,351,1,0,0,0,354,53,1,0,0,0,355,356,7,4,0,0,356,55,
        1,0,0,0,357,366,3,54,27,0,358,359,5,50,0,0,359,361,3,54,27,0,360,
        358,1,0,0,0,361,362,1,0,0,0,362,360,1,0,0,0,362,363,1,0,0,0,363,
        367,1,0,0,0,364,365,5,50,0,0,365,367,5,5,0,0,366,360,1,0,0,0,366,
        364,1,0,0,0,367,57,1,0,0,0,368,369,5,34,0,0,369,59,1,0,0,0,370,379,
        3,58,29,0,371,372,5,50,0,0,372,374,3,58,29,0,373,371,1,0,0,0,374,
        375,1,0,0,0,375,373,1,0,0,0,375,376,1,0,0,0,376,380,1,0,0,0,377,
        378,5,50,0,0,378,380,5,5,0,0,379,373,1,0,0,0,379,377,1,0,0,0,380,
        61,1,0,0,0,381,382,5,20,0,0,382,63,1,0,0,0,383,392,3,62,31,0,384,
        385,5,50,0,0,385,387,3,62,31,0,386,384,1,0,0,0,387,388,1,0,0,0,388,
        386,1,0,0,0,388,389,1,0,0,0,389,393,1,0,0,0,390,391,5,50,0,0,391,
        393,5,5,0,0,392,386,1,0,0,0,392,390,1,0,0,0,393,65,1,0,0,0,394,396,
        5,48,0,0,395,397,5,39,0,0,396,395,1,0,0,0,396,397,1,0,0,0,397,398,
        1,0,0,0,398,399,3,62,31,0,399,401,5,36,0,0,400,402,5,40,0,0,401,
        400,1,0,0,0,401,402,1,0,0,0,402,403,1,0,0,0,403,404,3,62,31,0,404,
        405,5,48,0,0,405,420,1,0,0,0,406,408,5,48,0,0,407,409,3,98,49,0,
        408,407,1,0,0,0,408,409,1,0,0,0,409,410,1,0,0,0,410,411,3,62,31,
        0,411,412,5,48,0,0,412,420,1,0,0,0,413,414,5,48,0,0,414,415,3,62,
        31,0,415,416,5,43,0,0,416,417,3,86,43,0,417,418,5,48,0,0,418,420,
        1,0,0,0,419,394,1,0,0,0,419,406,1,0,0,0,419,413,1,0,0,0,420,67,1,
        0,0,0,421,430,3,66,33,0,422,423,5,50,0,0,423,425,3,66,33,0,424,422,
        1,0,0,0,425,426,1,0,0,0,426,424,1,0,0,0,426,427,1,0,0,0,427,431,
        1,0,0,0,428,429,5,50,0,0,429,431,5,5,0,0,430,424,1,0,0,0,430,428,
        1,0,0,0,431,69,1,0,0,0,432,433,5,21,0,0,433,71,1,0,0,0,434,443,3,
        70,35,0,435,436,5,50,0,0,436,438,3,70,35,0,437,435,1,0,0,0,438,439,
        1,0,0,0,439,437,1,0,0,0,439,440,1,0,0,0,440,444,1,0,0,0,441,442,
        5,50,0,0,442,444,5,5,0,0,443,437,1,0,0,0,443,441,1,0,0,0,444,73,
        1,0,0,0,445,447,5,48,0,0,446,448,5,39,0,0,447,446,1,0,0,0,447,448,
        1,0,0,0,448,449,1,0,0,0,449,450,3,70,35,0,450,452,5,36,0,0,451,453,
        5,40,0,0,452,451,1,0,0,0,452,453,1,0,0,0,453,454,1,0,0,0,454,455,
        3,70,35,0,455,456,5,48,0,0,456,471,1,0,0,0,457,459,5,48,0,0,458,
        460,3,98,49,0,459,458,1,0,0,0,459,460,1,0,0,0,460,461,1,0,0,0,461,
        462,3,70,35,0,462,463,5,48,0,0,463,471,1,0,0,0,464,465,5,48,0,0,
        465,466,3,70,35,0,466,467,5,43,0,0,467,468,3,86,43,0,468,469,5,48,
        0,0,469,471,1,0,0,0,470,445,1,0,0,0,470,457,1,0,0,0,470,464,1,0,
        0,0,471,75,1,0,0,0,472,481,3,74,37,0,473,474,5,50,0,0,474,476,3,
        74,37,0,475,473,1,0,0,0,476,477,1,0,0,0,477,475,1,0,0,0,477,478,
        1,0,0,0,478,482,1,0,0,0,479,480,5,50,0,0,480,482,5,5,0,0,481,475,
        1,0,0,0,481,479,1,0,0,0,482,77,1,0,0,0,483,484,5,22,0,0,484,79,1,
        0,0,0,485,494,3,78,39,0,486,487,5,50,0,0,487,489,3,78,39,0,488,486,
        1,0,0,0,489,490,1,0,0,0,490,488,1,0,0,0,490,491,1,0,0,0,491,495,
        1,0,0,0,492,493,5,50,0,0,493,495,5,5,0,0,494,488,1,0,0,0,494,492,
        1,0,0,0,495,81,1,0,0,0,496,498,5,48,0,0,497,499,5,39,0,0,498,497,
        1,0,0,0,498,499,1,0,0,0,499,500,1,0,0,0,500,501,3,78,39,0,501,503,
        5,36,0,0,502,504,5,40,0,0,503,502,1,0,0,0,503,504,1,0,0,0,504,505,
        1,0,0,0,505,506,3,78,39,0,506,507,5,48,0,0,507,522,1,0,0,0,508,510,
        5,48,0,0,509,511,3,98,49,0,510,509,1,0,0,0,510,511,1,0,0,0,511,512,
        1,0,0,0,512,513,3,78,39,0,513,514,5,48,0,0,514,522,1,0,0,0,515,516,
        5,48,0,0,516,517,3,78,39,0,517,518,5,43,0,0,518,519,3,86,43,0,519,
        520,5,48,0,0,520,522,1,0,0,0,521,496,1,0,0,0,521,508,1,0,0,0,521,
        515,1,0,0,0,522,83,1,0,0,0,523,532,3,82,41,0,524,525,5,50,0,0,525,
        527,3,82,41,0,526,524,1,0,0,0,527,528,1,0,0,0,528,526,1,0,0,0,528,
        529,1,0,0,0,529,533,1,0,0,0,530,531,5,50,0,0,531,533,5,5,0,0,532,
        526,1,0,0,0,532,530,1,0,0,0,533,85,1,0,0,0,534,536,7,1,0,0,535,534,
        1,0,0,0,535,536,1,0,0,0,536,537,1,0,0,0,537,538,5,23,0,0,538,87,
        1,0,0,0,539,548,3,86,43,0,540,541,5,50,0,0,541,543,3,86,43,0,542,
        540,1,0,0,0,543,544,1,0,0,0,544,542,1,0,0,0,544,545,1,0,0,0,545,
        549,1,0,0,0,546,547,5,50,0,0,547,549,5,5,0,0,548,542,1,0,0,0,548,
        546,1,0,0,0,549,89,1,0,0,0,550,552,5,48,0,0,551,553,5,39,0,0,552,
        551,1,0,0,0,552,553,1,0,0,0,553,554,1,0,0,0,554,555,3,86,43,0,555,
        557,5,36,0,0,556,558,5,40,0,0,557,556,1,0,0,0,557,558,1,0,0,0,558,
        559,1,0,0,0,559,560,3,86,43,0,560,561,5,48,0,0,561,576,1,0,0,0,562,
        564,5,48,0,0,563,565,3,98,49,0,564,563,1,0,0,0,564,565,1,0,0,0,565,
        566,1,0,0,0,566,567,3,86,43,0,567,568,5,48,0,0,568,576,1,0,0,0,569,
        570,5,48,0,0,570,571,3,86,43,0,571,572,5,43,0,0,572,573,3,86,43,
        0,573,574,5,48,0,0,574,576,1,0,0,0,575,550,1,0,0,0,575,562,1,0,0,
        0,575,569,1,0,0,0,576,91,1,0,0,0,577,586,3,90,45,0,578,579,5,50,
        0,0,579,581,3,90,45,0,580,578,1,0,0,0,581,582,1,0,0,0,582,580,1,
        0,0,0,582,583,1,0,0,0,583,587,1,0,0,0,584,585,5,50,0,0,585,587,5,
        5,0,0,586,580,1,0,0,0,586,584,1,0,0,0,587,93,1,0,0,0,588,589,5,13,
        0,0,589,95,1,0,0,0,590,599,3,94,47,0,591,592,5,50,0,0,592,594,3,
        94,47,0,593,591,1,0,0,0,594,595,1,0,0,0,595,593,1,0,0,0,595,596,
        1,0,0,0,596,600,1,0,0,0,597,598,5,50,0,0,598,600,5,5,0,0,599,593,
        1,0,0,0,599,597,1,0,0,0,600,97,1,0,0,0,601,602,7,5,0,0,602,99,1,
        0,0,0,79,103,106,109,115,121,124,131,136,139,166,168,171,176,181,
        190,195,200,212,224,232,241,245,248,257,261,265,270,277,288,295,
        299,302,311,315,319,324,331,342,349,353,362,366,375,379,388,392,
        396,401,408,419,426,430,439,443,447,452,459,470,477,481,490,494,
        498,503,510,521,528,532,535,544,548,552,557,564,575,582,586,595,
        599
    ]

class OdinParser ( Parser ):

    grammarFileName = "OdinParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'...'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'::'", "'..'", "<INVALID>", 
                     "<INVALID>", "'>'", "'<'", "<INVALID>", "'='", "<INVALID>", 
                     "'+'", "'-'", "'%'", "'^'", "'|'", "'.'", "','", "'/'", 
                     "':'", "';'", "'*'", "'('", "')'", "'['", "']'", "'{'", 
                     "'}'" ]

    symbolicNames = [ "<INVALID>", "CMT_LINE", "EOL", "WS", "ODIN_URI", 
                      "SYM_LIST_CONTINUE", "OBJECT_VERSION_ID", "ARCHETYPE_HRID", 
                      "ARCHETYPE_REF", "VERSION_ID", "FULLY_QUALIFIED_RM_ENTITY", 
                      "QUALIFIED_TERM_CODE_ID", "LOCAL_TERM_CODE_ID", "QUALIFIED_TERM_CODE_REF", 
                      "ROOT_ID_CODE", "ID_CODE", "AT_CODE", "AC_CODE", "ADL14_AT_CODE", 
                      "ADL14_AC_CODE", "ISO8601_DATE_AUGMENTED", "ISO8601_TIME_AUGMENTED", 
                      "ISO8601_DATE_TIME_AUGMENTED", "ISO8601_DURATION", 
                      "SYM_TRUE", "SYM_FALSE", "GUID", "UUID", "INTEGER", 
                      "REAL", "REAL_PERCENT", "SCI_INTEGER", "SCI_REAL", 
                      "STRING", "CHARACTER", "SYM_NAMESPACE_SEP", "SYM_DOUBLE_DOT", 
                      "SYM_LE", "SYM_GE", "SYM_GT", "SYM_LT", "SYM_NE", 
                      "SYM_EQ", "SYM_PLUS_OR_MINUS", "SYM_PLUS", "SYM_MINUS", 
                      "SYM_PERCENT", "SYM_CARET", "SYM_VERTICAL_BAR", "SYM_DOT", 
                      "SYM_COMMA", "SYM_SLASH", "SYM_COLON", "SYM_SEMI_COLON", 
                      "SYM_ASTERISK", "SYM_LPAREN", "SYM_RPAREN", "SYM_LBRACKET", 
                      "SYM_RBRACKET", "SYM_LCURLY", "SYM_RCURLY", "UC_ID", 
                      "LC_ID", "WEB_ID" ]

    RULE_odinObject = 0
    RULE_odinAttrVal = 1
    RULE_odinAttrName = 2
    RULE_odinObjectBlock = 3
    RULE_odinObjectValueBlock = 4
    RULE_rmTypeSpec = 5
    RULE_odinKeyedObject = 6
    RULE_odinKeySpec = 7
    RULE_odinObjectReferenceBlock = 8
    RULE_odinPathList = 9
    RULE_odinPath = 10
    RULE_odinPathSegment = 11
    RULE_rmTypeId = 12
    RULE_primitiveObject = 13
    RULE_primitiveValue = 14
    RULE_primitiveListValue = 15
    RULE_primitiveIntervalValue = 16
    RULE_stringValue = 17
    RULE_stringListValue = 18
    RULE_integerValue = 19
    RULE_integerListValue = 20
    RULE_integerIntervalValue = 21
    RULE_integerIntervalListValue = 22
    RULE_realValue = 23
    RULE_realListValue = 24
    RULE_realIntervalValue = 25
    RULE_realIntervalListValue = 26
    RULE_booleanValue = 27
    RULE_booleanListValue = 28
    RULE_characterValue = 29
    RULE_characterListValue = 30
    RULE_dateValue = 31
    RULE_dateListValue = 32
    RULE_dateIntervalValue = 33
    RULE_dateIntervalListValue = 34
    RULE_timeValue = 35
    RULE_timeListValue = 36
    RULE_timeIntervalValue = 37
    RULE_timeIntervalListValue = 38
    RULE_dateTimeValue = 39
    RULE_dateTimeListValue = 40
    RULE_dateTimeIntervalValue = 41
    RULE_dateTimeIntervalListValue = 42
    RULE_durationValue = 43
    RULE_durationListValue = 44
    RULE_durationIntervalValue = 45
    RULE_durationIntervalListValue = 46
    RULE_termCodeValue = 47
    RULE_termCodeListValue = 48
    RULE_relop = 49

    ruleNames =  [ "odinObject", "odinAttrVal", "odinAttrName", "odinObjectBlock", 
                   "odinObjectValueBlock", "rmTypeSpec", "odinKeyedObject", 
                   "odinKeySpec", "odinObjectReferenceBlock", "odinPathList", 
                   "odinPath", "odinPathSegment", "rmTypeId", "primitiveObject", 
                   "primitiveValue", "primitiveListValue", "primitiveIntervalValue", 
                   "stringValue", "stringListValue", "integerValue", "integerListValue", 
                   "integerIntervalValue", "integerIntervalListValue", "realValue", 
                   "realListValue", "realIntervalValue", "realIntervalListValue", 
                   "booleanValue", "booleanListValue", "characterValue", 
                   "characterListValue", "dateValue", "dateListValue", "dateIntervalValue", 
                   "dateIntervalListValue", "timeValue", "timeListValue", 
                   "timeIntervalValue", "timeIntervalListValue", "dateTimeValue", 
                   "dateTimeListValue", "dateTimeIntervalValue", "dateTimeIntervalListValue", 
                   "durationValue", "durationListValue", "durationIntervalValue", 
                   "durationIntervalListValue", "termCodeValue", "termCodeListValue", 
                   "relop" ]

    EOF = Token.EOF
    CMT_LINE=1
    EOL=2
    WS=3
    ODIN_URI=4
    SYM_LIST_CONTINUE=5
    OBJECT_VERSION_ID=6
    ARCHETYPE_HRID=7
    ARCHETYPE_REF=8
    VERSION_ID=9
    FULLY_QUALIFIED_RM_ENTITY=10
    QUALIFIED_TERM_CODE_ID=11
    LOCAL_TERM_CODE_ID=12
    QUALIFIED_TERM_CODE_REF=13
    ROOT_ID_CODE=14
    ID_CODE=15
    AT_CODE=16
    AC_CODE=17
    ADL14_AT_CODE=18
    ADL14_AC_CODE=19
    ISO8601_DATE_AUGMENTED=20
    ISO8601_TIME_AUGMENTED=21
    ISO8601_DATE_TIME_AUGMENTED=22
    ISO8601_DURATION=23
    SYM_TRUE=24
    SYM_FALSE=25
    GUID=26
    UUID=27
    INTEGER=28
    REAL=29
    REAL_PERCENT=30
    SCI_INTEGER=31
    SCI_REAL=32
    STRING=33
    CHARACTER=34
    SYM_NAMESPACE_SEP=35
    SYM_DOUBLE_DOT=36
    SYM_LE=37
    SYM_GE=38
    SYM_GT=39
    SYM_LT=40
    SYM_NE=41
    SYM_EQ=42
    SYM_PLUS_OR_MINUS=43
    SYM_PLUS=44
    SYM_MINUS=45
    SYM_PERCENT=46
    SYM_CARET=47
    SYM_VERTICAL_BAR=48
    SYM_DOT=49
    SYM_COMMA=50
    SYM_SLASH=51
    SYM_COLON=52
    SYM_SEMI_COLON=53
    SYM_ASTERISK=54
    SYM_LPAREN=55
    SYM_RPAREN=56
    SYM_LBRACKET=57
    SYM_RBRACKET=58
    SYM_LCURLY=59
    SYM_RCURLY=60
    UC_ID=61
    LC_ID=62
    WEB_ID=63

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class OdinObjectContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinObjectValueBlock(self):
            return self.getTypedRuleContext(OdinParser.OdinObjectValueBlockContext,0)


        def EOF(self):
            return self.getToken(OdinParser.EOF, 0)

        def odinAttrVal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.OdinAttrValContext)
            else:
                return self.getTypedRuleContext(OdinParser.OdinAttrValContext,i)


        def getRuleIndex(self):
            return OdinParser.RULE_odinObject

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinObject" ):
                listener.enterOdinObject(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinObject" ):
                listener.exitOdinObject(self)




    def odinObject(self):

        localctx = OdinParser.OdinObjectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_odinObject)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [61, 62]:
                self.state = 101 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 100
                    self.odinAttrVal()
                    self.state = 103 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==61 or _la==62):
                        break

                pass
            elif token in [40, 55]:
                self.state = 105
                self.odinObjectValueBlock()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 109
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 108
                self.match(OdinParser.EOF)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinAttrValContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinAttrName(self):
            return self.getTypedRuleContext(OdinParser.OdinAttrNameContext,0)


        def SYM_EQ(self):
            return self.getToken(OdinParser.SYM_EQ, 0)

        def odinObjectBlock(self):
            return self.getTypedRuleContext(OdinParser.OdinObjectBlockContext,0)


        def SYM_SEMI_COLON(self):
            return self.getToken(OdinParser.SYM_SEMI_COLON, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_odinAttrVal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinAttrVal" ):
                listener.enterOdinAttrVal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinAttrVal" ):
                listener.exitOdinAttrVal(self)




    def odinAttrVal(self):

        localctx = OdinParser.OdinAttrValContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_odinAttrVal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.odinAttrName()
            self.state = 112
            self.match(OdinParser.SYM_EQ)
            self.state = 113
            self.odinObjectBlock()
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==53:
                self.state = 114
                self.match(OdinParser.SYM_SEMI_COLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinAttrNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UC_ID(self):
            return self.getToken(OdinParser.UC_ID, 0)

        def LC_ID(self):
            return self.getToken(OdinParser.LC_ID, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_odinAttrName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinAttrName" ):
                listener.enterOdinAttrName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinAttrName" ):
                listener.exitOdinAttrName(self)




    def odinAttrName(self):

        localctx = OdinParser.OdinAttrNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_odinAttrName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            _la = self._input.LA(1)
            if not(_la==61 or _la==62):
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


    class OdinObjectBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinObjectValueBlock(self):
            return self.getTypedRuleContext(OdinParser.OdinObjectValueBlockContext,0)


        def odinObjectReferenceBlock(self):
            return self.getTypedRuleContext(OdinParser.OdinObjectReferenceBlockContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_odinObjectBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinObjectBlock" ):
                listener.enterOdinObjectBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinObjectBlock" ):
                listener.exitOdinObjectBlock(self)




    def odinObjectBlock(self):

        localctx = OdinParser.OdinObjectBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_odinObjectBlock)
        try:
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 119
                self.odinObjectValueBlock()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 120
                self.odinObjectReferenceBlock()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinObjectValueBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def rmTypeSpec(self):
            return self.getTypedRuleContext(OdinParser.RmTypeSpecContext,0)


        def primitiveObject(self):
            return self.getTypedRuleContext(OdinParser.PrimitiveObjectContext,0)


        def ODIN_URI(self):
            return self.getToken(OdinParser.ODIN_URI, 0)

        def odinAttrVal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.OdinAttrValContext)
            else:
                return self.getTypedRuleContext(OdinParser.OdinAttrValContext,i)


        def odinKeyedObject(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.OdinKeyedObjectContext)
            else:
                return self.getTypedRuleContext(OdinParser.OdinKeyedObjectContext,i)


        def getRuleIndex(self):
            return OdinParser.RULE_odinObjectValueBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinObjectValueBlock" ):
                listener.enterOdinObjectValueBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinObjectValueBlock" ):
                listener.exitOdinObjectValueBlock(self)




    def odinObjectValueBlock(self):

        localctx = OdinParser.OdinObjectValueBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_odinObjectValueBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==55:
                self.state = 123
                self.rmTypeSpec()


            self.state = 126
            self.match(OdinParser.SYM_LT)
            self.state = 139
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13, 20, 21, 22, 23, 24, 25, 28, 29, 31, 32, 33, 34, 44, 45, 48]:
                self.state = 127
                self.primitiveObject()
                pass
            elif token in [61, 62]:
                self.state = 129 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 128
                    self.odinAttrVal()
                    self.state = 131 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==61 or _la==62):
                        break

                pass
            elif token in [57]:
                self.state = 134 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 133
                    self.odinKeyedObject()
                    self.state = 136 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==57):
                        break

                pass
            elif token in [4]:
                self.state = 138
                self.match(OdinParser.ODIN_URI)
                pass
            elif token in [39]:
                pass
            else:
                pass
            self.state = 141
            self.match(OdinParser.SYM_GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RmTypeSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LPAREN(self):
            return self.getToken(OdinParser.SYM_LPAREN, 0)

        def rmTypeId(self):
            return self.getTypedRuleContext(OdinParser.RmTypeIdContext,0)


        def SYM_RPAREN(self):
            return self.getToken(OdinParser.SYM_RPAREN, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_rmTypeSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRmTypeSpec" ):
                listener.enterRmTypeSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRmTypeSpec" ):
                listener.exitRmTypeSpec(self)




    def rmTypeSpec(self):

        localctx = OdinParser.RmTypeSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_rmTypeSpec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(OdinParser.SYM_LPAREN)
            self.state = 144
            self.rmTypeId()
            self.state = 145
            self.match(OdinParser.SYM_RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinKeyedObjectContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinKeySpec(self):
            return self.getTypedRuleContext(OdinParser.OdinKeySpecContext,0)


        def SYM_EQ(self):
            return self.getToken(OdinParser.SYM_EQ, 0)

        def odinObjectBlock(self):
            return self.getTypedRuleContext(OdinParser.OdinObjectBlockContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_odinKeyedObject

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinKeyedObject" ):
                listener.enterOdinKeyedObject(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinKeyedObject" ):
                listener.exitOdinKeyedObject(self)




    def odinKeyedObject(self):

        localctx = OdinParser.OdinKeyedObjectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_odinKeyedObject)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.odinKeySpec()
            self.state = 148
            self.match(OdinParser.SYM_EQ)
            self.state = 149
            self.odinObjectBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinKeySpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LBRACKET(self):
            return self.getToken(OdinParser.SYM_LBRACKET, 0)

        def primitiveValue(self):
            return self.getTypedRuleContext(OdinParser.PrimitiveValueContext,0)


        def SYM_RBRACKET(self):
            return self.getToken(OdinParser.SYM_RBRACKET, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_odinKeySpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinKeySpec" ):
                listener.enterOdinKeySpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinKeySpec" ):
                listener.exitOdinKeySpec(self)




    def odinKeySpec(self):

        localctx = OdinParser.OdinKeySpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_odinKeySpec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(OdinParser.SYM_LBRACKET)
            self.state = 152
            self.primitiveValue()
            self.state = 153
            self.match(OdinParser.SYM_RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinObjectReferenceBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def odinPathList(self):
            return self.getTypedRuleContext(OdinParser.OdinPathListContext,0)


        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_odinObjectReferenceBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinObjectReferenceBlock" ):
                listener.enterOdinObjectReferenceBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinObjectReferenceBlock" ):
                listener.exitOdinObjectReferenceBlock(self)




    def odinObjectReferenceBlock(self):

        localctx = OdinParser.OdinObjectReferenceBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_odinObjectReferenceBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.match(OdinParser.SYM_LT)
            self.state = 156
            self.odinPathList()
            self.state = 157
            self.match(OdinParser.SYM_GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinPathListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinPath(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.OdinPathContext)
            else:
                return self.getTypedRuleContext(OdinParser.OdinPathContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_odinPathList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinPathList" ):
                listener.enterOdinPathList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinPathList" ):
                listener.exitOdinPathList(self)




    def odinPathList(self):

        localctx = OdinParser.OdinPathListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_odinPathList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self.odinPath()
            self.state = 168
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 160
                self.match(OdinParser.SYM_COMMA)
                self.state = 161
                self.match(OdinParser.SYM_LIST_CONTINUE)

            elif la_ == 2:
                self.state = 164 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 162
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 163
                    self.odinPath()
                    self.state = 166 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OdinPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def odinKeySpec(self):
            return self.getTypedRuleContext(OdinParser.OdinKeySpecContext,0)


        def odinPathSegment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.OdinPathSegmentContext)
            else:
                return self.getTypedRuleContext(OdinParser.OdinPathSegmentContext,i)


        def getRuleIndex(self):
            return OdinParser.RULE_odinPath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinPath" ):
                listener.enterOdinPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinPath" ):
                listener.exitOdinPath(self)




    def odinPath(self):

        localctx = OdinParser.OdinPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_odinPath)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 170
                self.odinKeySpec()


            self.state = 174 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 173
                self.odinPathSegment()
                self.state = 176 
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


    class OdinPathSegmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_SLASH(self):
            return self.getToken(OdinParser.SYM_SLASH, 0)

        def LC_ID(self):
            return self.getToken(OdinParser.LC_ID, 0)

        def odinKeySpec(self):
            return self.getTypedRuleContext(OdinParser.OdinKeySpecContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_odinPathSegment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOdinPathSegment" ):
                listener.enterOdinPathSegment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOdinPathSegment" ):
                listener.exitOdinPathSegment(self)




    def odinPathSegment(self):

        localctx = OdinParser.OdinPathSegmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_odinPathSegment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(OdinParser.SYM_SLASH)
            self.state = 179
            self.match(OdinParser.LC_ID)
            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 180
                self.odinKeySpec()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RmTypeIdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UC_ID(self):
            return self.getToken(OdinParser.UC_ID, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def rmTypeId(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.RmTypeIdContext)
            else:
                return self.getTypedRuleContext(OdinParser.RmTypeIdContext,i)


        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def getRuleIndex(self):
            return OdinParser.RULE_rmTypeId

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRmTypeId" ):
                listener.enterRmTypeId(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRmTypeId" ):
                listener.exitRmTypeId(self)




    def rmTypeId(self):

        localctx = OdinParser.RmTypeIdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_rmTypeId)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            self.match(OdinParser.UC_ID)
            self.state = 195
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 184
                self.match(OdinParser.SYM_LT)
                self.state = 185
                self.rmTypeId()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==50:
                    self.state = 186
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 187
                    self.rmTypeId()
                    self.state = 192
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 193
                self.match(OdinParser.SYM_GT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveObjectContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitiveValue(self):
            return self.getTypedRuleContext(OdinParser.PrimitiveValueContext,0)


        def primitiveListValue(self):
            return self.getTypedRuleContext(OdinParser.PrimitiveListValueContext,0)


        def primitiveIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.PrimitiveIntervalValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_primitiveObject

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveObject" ):
                listener.enterPrimitiveObject(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveObject" ):
                listener.exitPrimitiveObject(self)




    def primitiveObject(self):

        localctx = OdinParser.PrimitiveObjectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_primitiveObject)
        try:
            self.state = 200
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 197
                self.primitiveValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 198
                self.primitiveListValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 199
                self.primitiveIntervalValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringValue(self):
            return self.getTypedRuleContext(OdinParser.StringValueContext,0)


        def integerValue(self):
            return self.getTypedRuleContext(OdinParser.IntegerValueContext,0)


        def realValue(self):
            return self.getTypedRuleContext(OdinParser.RealValueContext,0)


        def booleanValue(self):
            return self.getTypedRuleContext(OdinParser.BooleanValueContext,0)


        def characterValue(self):
            return self.getTypedRuleContext(OdinParser.CharacterValueContext,0)


        def termCodeValue(self):
            return self.getTypedRuleContext(OdinParser.TermCodeValueContext,0)


        def dateValue(self):
            return self.getTypedRuleContext(OdinParser.DateValueContext,0)


        def timeValue(self):
            return self.getTypedRuleContext(OdinParser.TimeValueContext,0)


        def dateTimeValue(self):
            return self.getTypedRuleContext(OdinParser.DateTimeValueContext,0)


        def durationValue(self):
            return self.getTypedRuleContext(OdinParser.DurationValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_primitiveValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveValue" ):
                listener.enterPrimitiveValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveValue" ):
                listener.exitPrimitiveValue(self)




    def primitiveValue(self):

        localctx = OdinParser.PrimitiveValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_primitiveValue)
        try:
            self.state = 212
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 202
                self.stringValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 203
                self.integerValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 204
                self.realValue()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 205
                self.booleanValue()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 206
                self.characterValue()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 207
                self.termCodeValue()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 208
                self.dateValue()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 209
                self.timeValue()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 210
                self.dateTimeValue()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 211
                self.durationValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringListValue(self):
            return self.getTypedRuleContext(OdinParser.StringListValueContext,0)


        def integerListValue(self):
            return self.getTypedRuleContext(OdinParser.IntegerListValueContext,0)


        def realListValue(self):
            return self.getTypedRuleContext(OdinParser.RealListValueContext,0)


        def booleanListValue(self):
            return self.getTypedRuleContext(OdinParser.BooleanListValueContext,0)


        def characterListValue(self):
            return self.getTypedRuleContext(OdinParser.CharacterListValueContext,0)


        def termCodeListValue(self):
            return self.getTypedRuleContext(OdinParser.TermCodeListValueContext,0)


        def dateListValue(self):
            return self.getTypedRuleContext(OdinParser.DateListValueContext,0)


        def timeListValue(self):
            return self.getTypedRuleContext(OdinParser.TimeListValueContext,0)


        def dateTimeListValue(self):
            return self.getTypedRuleContext(OdinParser.DateTimeListValueContext,0)


        def durationListValue(self):
            return self.getTypedRuleContext(OdinParser.DurationListValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_primitiveListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveListValue" ):
                listener.enterPrimitiveListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveListValue" ):
                listener.exitPrimitiveListValue(self)




    def primitiveListValue(self):

        localctx = OdinParser.PrimitiveListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_primitiveListValue)
        try:
            self.state = 224
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 214
                self.stringListValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 215
                self.integerListValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 216
                self.realListValue()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 217
                self.booleanListValue()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 218
                self.characterListValue()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 219
                self.termCodeListValue()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 220
                self.dateListValue()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 221
                self.timeListValue()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 222
                self.dateTimeListValue()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 223
                self.durationListValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def integerIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.IntegerIntervalValueContext,0)


        def realIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.RealIntervalValueContext,0)


        def dateIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.DateIntervalValueContext,0)


        def timeIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.TimeIntervalValueContext,0)


        def dateTimeIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.DateTimeIntervalValueContext,0)


        def durationIntervalValue(self):
            return self.getTypedRuleContext(OdinParser.DurationIntervalValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_primitiveIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveIntervalValue" ):
                listener.enterPrimitiveIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveIntervalValue" ):
                listener.exitPrimitiveIntervalValue(self)




    def primitiveIntervalValue(self):

        localctx = OdinParser.PrimitiveIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_primitiveIntervalValue)
        try:
            self.state = 232
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.integerIntervalValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.realIntervalValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 228
                self.dateIntervalValue()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 229
                self.timeIntervalValue()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 230
                self.dateTimeIntervalValue()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 231
                self.durationIntervalValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(OdinParser.STRING, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_stringValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringValue" ):
                listener.enterStringValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringValue" ):
                listener.exitStringValue(self)




    def stringValue(self):

        localctx = OdinParser.StringValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_stringValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234
            self.match(OdinParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.StringValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.StringValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_stringListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringListValue" ):
                listener.enterStringListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringListValue" ):
                listener.exitStringListValue(self)




    def stringListValue(self):

        localctx = OdinParser.StringListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_stringListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.stringValue()
            self.state = 245
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 239 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 237
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 238
                    self.stringValue()
                    self.state = 241 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 243
                self.match(OdinParser.SYM_COMMA)
                self.state = 244
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(OdinParser.INTEGER, 0)

        def SCI_INTEGER(self):
            return self.getToken(OdinParser.SCI_INTEGER, 0)

        def SYM_PLUS(self):
            return self.getToken(OdinParser.SYM_PLUS, 0)

        def SYM_MINUS(self):
            return self.getToken(OdinParser.SYM_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_integerValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerValue" ):
                listener.enterIntegerValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerValue" ):
                listener.exitIntegerValue(self)




    def integerValue(self):

        localctx = OdinParser.IntegerValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_integerValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44 or _la==45:
                self.state = 247
                _la = self._input.LA(1)
                if not(_la==44 or _la==45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 250
            _la = self._input.LA(1)
            if not(_la==28 or _la==31):
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


    class IntegerListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def integerValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.IntegerValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.IntegerValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_integerListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerListValue" ):
                listener.enterIntegerListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerListValue" ):
                listener.exitIntegerListValue(self)




    def integerListValue(self):

        localctx = OdinParser.IntegerListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_integerListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.integerValue()
            self.state = 261
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.state = 255 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 253
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 254
                    self.integerValue()
                    self.state = 257 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 259
                self.match(OdinParser.SYM_COMMA)
                self.state = 260
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def integerValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.IntegerValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.IntegerValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_integerIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerIntervalValue" ):
                listener.enterIntegerIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerIntervalValue" ):
                listener.exitIntegerIntervalValue(self)




    def integerIntervalValue(self):

        localctx = OdinParser.IntegerIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_integerIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 288
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 263
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 265
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 264
                    self.match(OdinParser.SYM_GT)


                self.state = 267
                self.integerValue()
                self.state = 268
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 270
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 269
                    self.match(OdinParser.SYM_LT)


                self.state = 272
                self.integerValue()
                self.state = 273
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 275
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 277
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 276
                    self.relop()


                self.state = 279
                self.integerValue()
                self.state = 280
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 282
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 283
                self.integerValue()
                self.state = 284
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 285
                self.integerValue()
                self.state = 286
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def integerIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.IntegerIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.IntegerIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_integerIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerIntervalListValue" ):
                listener.enterIntegerIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerIntervalListValue" ):
                listener.exitIntegerIntervalListValue(self)




    def integerIntervalListValue(self):

        localctx = OdinParser.IntegerIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_integerIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self.integerIntervalValue()
            self.state = 299
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.state = 293 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 291
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 292
                    self.integerIntervalValue()
                    self.state = 295 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 297
                self.match(OdinParser.SYM_COMMA)
                self.state = 298
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RealValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REAL(self):
            return self.getToken(OdinParser.REAL, 0)

        def SCI_REAL(self):
            return self.getToken(OdinParser.SCI_REAL, 0)

        def SYM_PLUS(self):
            return self.getToken(OdinParser.SYM_PLUS, 0)

        def SYM_MINUS(self):
            return self.getToken(OdinParser.SYM_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_realValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRealValue" ):
                listener.enterRealValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRealValue" ):
                listener.exitRealValue(self)




    def realValue(self):

        localctx = OdinParser.RealValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_realValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 302
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44 or _la==45:
                self.state = 301
                _la = self._input.LA(1)
                if not(_la==44 or _la==45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 304
            _la = self._input.LA(1)
            if not(_la==29 or _la==32):
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


    class RealListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def realValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.RealValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.RealValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_realListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRealListValue" ):
                listener.enterRealListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRealListValue" ):
                listener.exitRealListValue(self)




    def realListValue(self):

        localctx = OdinParser.RealListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_realListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 306
            self.realValue()
            self.state = 315
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.state = 309 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 307
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 308
                    self.realValue()
                    self.state = 311 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 313
                self.match(OdinParser.SYM_COMMA)
                self.state = 314
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RealIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def realValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.RealValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.RealValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_realIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRealIntervalValue" ):
                listener.enterRealIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRealIntervalValue" ):
                listener.exitRealIntervalValue(self)




    def realIntervalValue(self):

        localctx = OdinParser.RealIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_realIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 342
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 317
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 319
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 318
                    self.match(OdinParser.SYM_GT)


                self.state = 321
                self.realValue()
                self.state = 322
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 324
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 323
                    self.match(OdinParser.SYM_LT)


                self.state = 326
                self.realValue()
                self.state = 327
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 329
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 331
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 330
                    self.relop()


                self.state = 333
                self.realValue()
                self.state = 334
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 336
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 337
                self.realValue()
                self.state = 338
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 339
                self.realValue()
                self.state = 340
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RealIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def realIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.RealIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.RealIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_realIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRealIntervalListValue" ):
                listener.enterRealIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRealIntervalListValue" ):
                listener.exitRealIntervalListValue(self)




    def realIntervalListValue(self):

        localctx = OdinParser.RealIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_realIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.realIntervalValue()
            self.state = 353
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.state = 347 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 345
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 346
                    self.realIntervalValue()
                    self.state = 349 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 351
                self.match(OdinParser.SYM_COMMA)
                self.state = 352
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_TRUE(self):
            return self.getToken(OdinParser.SYM_TRUE, 0)

        def SYM_FALSE(self):
            return self.getToken(OdinParser.SYM_FALSE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_booleanValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanValue" ):
                listener.enterBooleanValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanValue" ):
                listener.exitBooleanValue(self)




    def booleanValue(self):

        localctx = OdinParser.BooleanValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_booleanValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 355
            _la = self._input.LA(1)
            if not(_la==24 or _la==25):
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


    class BooleanListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def booleanValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.BooleanValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.BooleanValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_booleanListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanListValue" ):
                listener.enterBooleanListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanListValue" ):
                listener.exitBooleanListValue(self)




    def booleanListValue(self):

        localctx = OdinParser.BooleanListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_booleanListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 357
            self.booleanValue()
            self.state = 366
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
            if la_ == 1:
                self.state = 360 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 358
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 359
                    self.booleanValue()
                    self.state = 362 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 364
                self.match(OdinParser.SYM_COMMA)
                self.state = 365
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHARACTER(self):
            return self.getToken(OdinParser.CHARACTER, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_characterValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterValue" ):
                listener.enterCharacterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterValue" ):
                listener.exitCharacterValue(self)




    def characterValue(self):

        localctx = OdinParser.CharacterValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_characterValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 368
            self.match(OdinParser.CHARACTER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def characterValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.CharacterValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.CharacterValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_characterListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterListValue" ):
                listener.enterCharacterListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterListValue" ):
                listener.exitCharacterListValue(self)




    def characterListValue(self):

        localctx = OdinParser.CharacterListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_characterListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self.characterValue()
            self.state = 379
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                self.state = 373 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 371
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 372
                    self.characterValue()
                    self.state = 375 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 377
                self.match(OdinParser.SYM_COMMA)
                self.state = 378
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ISO8601_DATE_AUGMENTED(self):
            return self.getToken(OdinParser.ISO8601_DATE_AUGMENTED, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateValue" ):
                listener.enterDateValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateValue" ):
                listener.exitDateValue(self)




    def dateValue(self):

        localctx = OdinParser.DateValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_dateValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.match(OdinParser.ISO8601_DATE_AUGMENTED)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateListValue" ):
                listener.enterDateListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateListValue" ):
                listener.exitDateListValue(self)




    def dateListValue(self):

        localctx = OdinParser.DateListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_dateListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
            self.dateValue()
            self.state = 392
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
            if la_ == 1:
                self.state = 386 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 384
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 385
                    self.dateValue()
                    self.state = 388 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 390
                self.match(OdinParser.SYM_COMMA)
                self.state = 391
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def dateValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def durationValue(self):
            return self.getTypedRuleContext(OdinParser.DurationValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_dateIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateIntervalValue" ):
                listener.enterDateIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateIntervalValue" ):
                listener.exitDateIntervalValue(self)




    def dateIntervalValue(self):

        localctx = OdinParser.DateIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_dateIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 419
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 394
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 396
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 395
                    self.match(OdinParser.SYM_GT)


                self.state = 398
                self.dateValue()
                self.state = 399
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 401
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 400
                    self.match(OdinParser.SYM_LT)


                self.state = 403
                self.dateValue()
                self.state = 404
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 406
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 408
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 407
                    self.relop()


                self.state = 410
                self.dateValue()
                self.state = 411
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 413
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 414
                self.dateValue()
                self.state = 415
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 416
                self.durationValue()
                self.state = 417
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateIntervalListValue" ):
                listener.enterDateIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateIntervalListValue" ):
                listener.exitDateIntervalListValue(self)




    def dateIntervalListValue(self):

        localctx = OdinParser.DateIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_dateIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 421
            self.dateIntervalValue()
            self.state = 430
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,51,self._ctx)
            if la_ == 1:
                self.state = 424 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 422
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 423
                    self.dateIntervalValue()
                    self.state = 426 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 428
                self.match(OdinParser.SYM_COMMA)
                self.state = 429
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ISO8601_TIME_AUGMENTED(self):
            return self.getToken(OdinParser.ISO8601_TIME_AUGMENTED, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_timeValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeValue" ):
                listener.enterTimeValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeValue" ):
                listener.exitTimeValue(self)




    def timeValue(self):

        localctx = OdinParser.TimeValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_timeValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 432
            self.match(OdinParser.ISO8601_TIME_AUGMENTED)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def timeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.TimeValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.TimeValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_timeListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeListValue" ):
                listener.enterTimeListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeListValue" ):
                listener.exitTimeListValue(self)




    def timeListValue(self):

        localctx = OdinParser.TimeListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_timeListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self.timeValue()
            self.state = 443
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,53,self._ctx)
            if la_ == 1:
                self.state = 437 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 435
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 436
                    self.timeValue()
                    self.state = 439 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 441
                self.match(OdinParser.SYM_COMMA)
                self.state = 442
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def timeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.TimeValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.TimeValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def durationValue(self):
            return self.getTypedRuleContext(OdinParser.DurationValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_timeIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeIntervalValue" ):
                listener.enterTimeIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeIntervalValue" ):
                listener.exitTimeIntervalValue(self)




    def timeIntervalValue(self):

        localctx = OdinParser.TimeIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_timeIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 470
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 445
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 447
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 446
                    self.match(OdinParser.SYM_GT)


                self.state = 449
                self.timeValue()
                self.state = 450
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 452
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 451
                    self.match(OdinParser.SYM_LT)


                self.state = 454
                self.timeValue()
                self.state = 455
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 457
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 459
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 458
                    self.relop()


                self.state = 461
                self.timeValue()
                self.state = 462
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 464
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 465
                self.timeValue()
                self.state = 466
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 467
                self.durationValue()
                self.state = 468
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def timeIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.TimeIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.TimeIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_timeIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeIntervalListValue" ):
                listener.enterTimeIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeIntervalListValue" ):
                listener.exitTimeIntervalListValue(self)




    def timeIntervalListValue(self):

        localctx = OdinParser.TimeIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_timeIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 472
            self.timeIntervalValue()
            self.state = 481
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,59,self._ctx)
            if la_ == 1:
                self.state = 475 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 473
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 474
                    self.timeIntervalValue()
                    self.state = 477 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 479
                self.match(OdinParser.SYM_COMMA)
                self.state = 480
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateTimeValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ISO8601_DATE_TIME_AUGMENTED(self):
            return self.getToken(OdinParser.ISO8601_DATE_TIME_AUGMENTED, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateTimeValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimeValue" ):
                listener.enterDateTimeValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimeValue" ):
                listener.exitDateTimeValue(self)




    def dateTimeValue(self):

        localctx = OdinParser.DateTimeValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_dateTimeValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 483
            self.match(OdinParser.ISO8601_DATE_TIME_AUGMENTED)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateTimeListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateTimeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateTimeValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateTimeValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateTimeListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimeListValue" ):
                listener.enterDateTimeListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimeListValue" ):
                listener.exitDateTimeListValue(self)




    def dateTimeListValue(self):

        localctx = OdinParser.DateTimeListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_dateTimeListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 485
            self.dateTimeValue()
            self.state = 494
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,61,self._ctx)
            if la_ == 1:
                self.state = 488 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 486
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 487
                    self.dateTimeValue()
                    self.state = 490 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 492
                self.match(OdinParser.SYM_COMMA)
                self.state = 493
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateTimeIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def dateTimeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateTimeValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateTimeValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def durationValue(self):
            return self.getTypedRuleContext(OdinParser.DurationValueContext,0)


        def getRuleIndex(self):
            return OdinParser.RULE_dateTimeIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimeIntervalValue" ):
                listener.enterDateTimeIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimeIntervalValue" ):
                listener.exitDateTimeIntervalValue(self)




    def dateTimeIntervalValue(self):

        localctx = OdinParser.DateTimeIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_dateTimeIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 521
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,65,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 496
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 498
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 497
                    self.match(OdinParser.SYM_GT)


                self.state = 500
                self.dateTimeValue()
                self.state = 501
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 503
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 502
                    self.match(OdinParser.SYM_LT)


                self.state = 505
                self.dateTimeValue()
                self.state = 506
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 508
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 510
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 509
                    self.relop()


                self.state = 512
                self.dateTimeValue()
                self.state = 513
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 515
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 516
                self.dateTimeValue()
                self.state = 517
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 518
                self.durationValue()
                self.state = 519
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateTimeIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateTimeIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DateTimeIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DateTimeIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_dateTimeIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimeIntervalListValue" ):
                listener.enterDateTimeIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimeIntervalListValue" ):
                listener.exitDateTimeIntervalListValue(self)




    def dateTimeIntervalListValue(self):

        localctx = OdinParser.DateTimeIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_dateTimeIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 523
            self.dateTimeIntervalValue()
            self.state = 532
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,67,self._ctx)
            if la_ == 1:
                self.state = 526 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 524
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 525
                    self.dateTimeIntervalValue()
                    self.state = 528 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 530
                self.match(OdinParser.SYM_COMMA)
                self.state = 531
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DurationValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ISO8601_DURATION(self):
            return self.getToken(OdinParser.ISO8601_DURATION, 0)

        def SYM_PLUS(self):
            return self.getToken(OdinParser.SYM_PLUS, 0)

        def SYM_MINUS(self):
            return self.getToken(OdinParser.SYM_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_durationValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDurationValue" ):
                listener.enterDurationValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDurationValue" ):
                listener.exitDurationValue(self)




    def durationValue(self):

        localctx = OdinParser.DurationValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_durationValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 535
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44 or _la==45:
                self.state = 534
                _la = self._input.LA(1)
                if not(_la==44 or _la==45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 537
            self.match(OdinParser.ISO8601_DURATION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DurationListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def durationValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DurationValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DurationValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_durationListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDurationListValue" ):
                listener.enterDurationListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDurationListValue" ):
                listener.exitDurationListValue(self)




    def durationListValue(self):

        localctx = OdinParser.DurationListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_durationListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 539
            self.durationValue()
            self.state = 548
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,70,self._ctx)
            if la_ == 1:
                self.state = 542 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 540
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 541
                    self.durationValue()
                    self.state = 544 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 546
                self.match(OdinParser.SYM_COMMA)
                self.state = 547
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DurationIntervalValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_VERTICAL_BAR(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_VERTICAL_BAR)
            else:
                return self.getToken(OdinParser.SYM_VERTICAL_BAR, i)

        def durationValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DurationValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DurationValueContext,i)


        def SYM_DOUBLE_DOT(self):
            return self.getToken(OdinParser.SYM_DOUBLE_DOT, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def relop(self):
            return self.getTypedRuleContext(OdinParser.RelopContext,0)


        def SYM_PLUS_OR_MINUS(self):
            return self.getToken(OdinParser.SYM_PLUS_OR_MINUS, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_durationIntervalValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDurationIntervalValue" ):
                listener.enterDurationIntervalValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDurationIntervalValue" ):
                listener.exitDurationIntervalValue(self)




    def durationIntervalValue(self):

        localctx = OdinParser.DurationIntervalValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_durationIntervalValue)
        self._la = 0 # Token type
        try:
            self.state = 575
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,74,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 550
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 552
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 551
                    self.match(OdinParser.SYM_GT)


                self.state = 554
                self.durationValue()
                self.state = 555
                self.match(OdinParser.SYM_DOUBLE_DOT)
                self.state = 557
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 556
                    self.match(OdinParser.SYM_LT)


                self.state = 559
                self.durationValue()
                self.state = 560
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 562
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 564
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0):
                    self.state = 563
                    self.relop()


                self.state = 566
                self.durationValue()
                self.state = 567
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 569
                self.match(OdinParser.SYM_VERTICAL_BAR)
                self.state = 570
                self.durationValue()
                self.state = 571
                self.match(OdinParser.SYM_PLUS_OR_MINUS)
                self.state = 572
                self.durationValue()
                self.state = 573
                self.match(OdinParser.SYM_VERTICAL_BAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DurationIntervalListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def durationIntervalValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.DurationIntervalValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.DurationIntervalValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_durationIntervalListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDurationIntervalListValue" ):
                listener.enterDurationIntervalListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDurationIntervalListValue" ):
                listener.exitDurationIntervalListValue(self)




    def durationIntervalListValue(self):

        localctx = OdinParser.DurationIntervalListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_durationIntervalListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 577
            self.durationIntervalValue()
            self.state = 586
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,76,self._ctx)
            if la_ == 1:
                self.state = 580 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 578
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 579
                    self.durationIntervalValue()
                    self.state = 582 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 584
                self.match(OdinParser.SYM_COMMA)
                self.state = 585
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermCodeValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUALIFIED_TERM_CODE_REF(self):
            return self.getToken(OdinParser.QUALIFIED_TERM_CODE_REF, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_termCodeValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermCodeValue" ):
                listener.enterTermCodeValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermCodeValue" ):
                listener.exitTermCodeValue(self)




    def termCodeValue(self):

        localctx = OdinParser.TermCodeValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_termCodeValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 588
            self.match(OdinParser.QUALIFIED_TERM_CODE_REF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermCodeListValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def termCodeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OdinParser.TermCodeValueContext)
            else:
                return self.getTypedRuleContext(OdinParser.TermCodeValueContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OdinParser.SYM_COMMA)
            else:
                return self.getToken(OdinParser.SYM_COMMA, i)

        def SYM_LIST_CONTINUE(self):
            return self.getToken(OdinParser.SYM_LIST_CONTINUE, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_termCodeListValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermCodeListValue" ):
                listener.enterTermCodeListValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermCodeListValue" ):
                listener.exitTermCodeListValue(self)




    def termCodeListValue(self):

        localctx = OdinParser.TermCodeListValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_termCodeListValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 590
            self.termCodeValue()
            self.state = 599
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,78,self._ctx)
            if la_ == 1:
                self.state = 593 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 591
                    self.match(OdinParser.SYM_COMMA)
                    self.state = 592
                    self.termCodeValue()
                    self.state = 595 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==50):
                        break

                pass

            elif la_ == 2:
                self.state = 597
                self.match(OdinParser.SYM_COMMA)
                self.state = 598
                self.match(OdinParser.SYM_LIST_CONTINUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LE(self):
            return self.getToken(OdinParser.SYM_LE, 0)

        def SYM_GE(self):
            return self.getToken(OdinParser.SYM_GE, 0)

        def SYM_GT(self):
            return self.getToken(OdinParser.SYM_GT, 0)

        def SYM_LT(self):
            return self.getToken(OdinParser.SYM_LT, 0)

        def getRuleIndex(self):
            return OdinParser.RULE_relop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelop" ):
                listener.enterRelop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelop" ):
                listener.exitRelop(self)




    def relop(self):

        localctx = OdinParser.RelopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_relop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 601
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2061584302080) != 0)):
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





