import pytest

from org.openehr.rm.data_types.encapsulated import DVParsable
from org.openehr.rm.data_types.time_specification import DVPeriodicTimeSpecification, DVGeneralTimeSpecification

def test_periodic_time_specification_value_valid():
    # OK
    DVPeriodicTimeSpecification(DVParsable("[20000418T1100;20000418T1110]/(P7D)@DW", "HL7:PIVL"))
    DVPeriodicTimeSpecification(DVParsable("WAKE+[PT50M;PT1H]", "HL7:EIVL"))
    # not OK
    with pytest.raises(ValueError):
        DVPeriodicTimeSpecification(DVParsable("[20000418T1100;20000418T1110]/(P7D)@DW", "EIVL"))
        DVPeriodicTimeSpecification(DVParsable("WAKE+[PT50M;PT1H]", "P"))

def test_periodic_time_specification_enforces_PIVL():
    ok_pivl_strings = [
        "[;]/(PT8H)",                                   # empty phase, period only
        "[;]/(PT12H) IST",                              # empty phase, period only (w/ institution specified time)
        "[;]/(P1Y)@DM",                                 # empty phase, period with calendar alignment
        "[20250914;]/(P1Y)@DM",                         # date with calendar alignment
        "[20250914;]/(P1Y)",                            # date without calendar alignment
        "[2025-09-14T09:00;2025-09-14T10:00]/(P2M)@DM", # date times with calendar alignment
        "[2025-09-14T09:00;2025-09-14T10:00]/(PT24H)",  # date times without calendar alignment
    ]
    for pivl_string in ok_pivl_strings:
        DVPeriodicTimeSpecification(DVParsable(pivl_string, "HL7:PIVL"))

    bad_pivl_strings = [
        "/(PT8H)",                                      # no phase
        "[20250930;20250928]/(PT1M)",                   # end of phase after start of phase
        "[20250930;]/(PT1M)@DayOfMonth",                # invalid calendar cycle
        "[;]/(PT12H)  IST",                             # two spaces prior to IST
        "WAKE+[PT1H;PT1H30M]"                           # EIVL provided by mistake
    ]
    for bad_pivl_string in bad_pivl_strings:
        with pytest.raises(ValueError):
            DVPeriodicTimeSpecification(DVParsable(bad_pivl_string, "HL7:PIVL"))

def test_periodic_time_specification_enforces_EIVL():
    ok_eivl_strings = [
        "ACM",                                          # event only
        "C+[;]",                                        # event plus before/after indication
        "PCM+[PT1H;]",                                  # event plus open ended period
        "WAKE-[PT10M;PT20M]"                            # event plus time limited period
    ]
    for eivl_string in ok_eivl_strings:
        DVPeriodicTimeSpecification(DVParsable(eivl_string, "HL7:EIVL"))

    bad_eivl_strings = [
        "BREAKFAST",                                    # invalid event timing
        "PCM?[PT1H;]",                                  # invalid before/after string
        "C+[PT1H;PT30S]"                                # end of time period before start of time period
    ]
    for bad_eivl_string in bad_eivl_strings:
        with pytest.raises(ValueError):
            DVPeriodicTimeSpecification(DVParsable(bad_eivl_string, "HL7:EIVL"))

def test_periodic_time_specification_period():
    dpts1 = DVPeriodicTimeSpecification(DVParsable("C-[PT30M;]", "HL7:EIVL"))                               # 30 mins before meals
    assert dpts1.period() == None
    dpts2 = DVPeriodicTimeSpecification(DVParsable("[20250914;]/(P7D)@DW", "HL7:PIVL"))                     # every Sunday
    assert dpts2.period().as_string() == "P7D"
    dpts3 = DVPeriodicTimeSpecification(DVParsable("[20250915T130000;20250915T1330]/(P1D)", "HL7:PIVL"))    # every day at 1300 for 30 mins
    assert dpts3.period().as_string() == "P1D"
    dpts4 = DVPeriodicTimeSpecification(DVParsable("[20250914;]/(PT1M)@DM", "HL7:PIVL"))                    # 14th of every month
    assert dpts4.period().as_string() == "PT1M"
    dpts5 = DVPeriodicTimeSpecification(DVParsable("[19981223;]/(P1Y)@DM", "HL7:PIVL"))                     # every 23rd December
    assert dpts5.period().as_string() == "P1Y"
    dpts6 = DVPeriodicTimeSpecification(DVParsable("[;]/(PT8H) IST", "HL7:PIVL"))                           # 3 times a day at institution specified times
    assert dpts6.period().as_string() == "PT8H"
    
def test_periodic_time_specification_calendar_alignment():
    dpts1 = DVPeriodicTimeSpecification(DVParsable("C-[PT30M;]", "HL7:EIVL"))
    assert dpts1.calendar_alignment() == None
    dpts3 = DVPeriodicTimeSpecification(DVParsable("[20250915T130000;20250915T1330]/(P1D)", "HL7:PIVL"))
    assert dpts3.calendar_alignment() == None
    dpts4 = DVPeriodicTimeSpecification(DVParsable("[20250914;]/(PT1M)@DM", "HL7:PIVL"))
    assert dpts4.calendar_alignment() == "DM"

def test_periodic_time_specification_event_alignment():
    dpts1 = DVPeriodicTimeSpecification(DVParsable("C-[PT30M;]", "HL7:EIVL"))
    assert dpts1.event_alignment() == "C"
    dpts3 = DVPeriodicTimeSpecification(DVParsable("[20250915T130000;20250915T1330]/(P1D)", "HL7:PIVL"))
    assert dpts3.event_alignment() == None

def test_periodic_time_specification_institution_specified():
    dpts1 = DVPeriodicTimeSpecification(DVParsable("C-[PT30M;]", "HL7:EIVL"))
    assert dpts1.institution_specified() == None
    dpts5 = DVPeriodicTimeSpecification(DVParsable("[19981223;]/(P1Y)@DM", "HL7:PIVL"))
    assert dpts5.institution_specified() == False
    dpts6 = DVPeriodicTimeSpecification(DVParsable("[;]/(PT8H) IST", "HL7:PIVL"))
    assert dpts6.institution_specified() == True

def test_general_time_specification_methods_warning_on_init_others_not_implemented():
    with pytest.warns(RuntimeWarning):
        dgts = DVGeneralTimeSpecification(DVParsable("WAKE+[50m;1h]", "HL7:GTS"))
        with pytest.raises(NotImplementedError):
            dgts.calendar_alignment()
        with pytest.raises(NotImplementedError):
            dgts.event_alignment()
        with pytest.raises(NotImplementedError):
            dgts.institution_specified()