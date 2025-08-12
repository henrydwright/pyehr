from clehr.terminology import CSVTerminologyService
from clehr.measurement import NLMMeasurementService
from org.openehr.rm.data_types.text import CodePhrase

print("Welcome to clehr - using pyehr, a Python implemention of OpenEHR")

ts = CSVTerminologyService("openehr(3)", "data/openehr-en2.csv", "en")
ms = NLMMeasurementService()

def print_list_strs(lst):
    for item in lst:
        print(str(item))

while True:
    user_command = input("clehr> ")
    user_command_parts = user_command.split(' ')
    if user_command_parts[0] == "exit":
        break
    elif user_command_parts[0] == "term":
        te = ts.terminology("openehr(3)")
        res = []
        if len(user_command_parts) == 1:
            res = te.all_codes()
        elif len(user_command_parts) == 3:
            if user_command_parts[1] == "group":
                res = te.codes_for_group_id(user_command_parts[2])
            elif user_command_parts[1] == "code":
                try:
                    res = [te.rubric_for_code(user_command_parts[2], "en")]
                except ValueError as ve:
                    res = [str(ve)]
        else:
            res = ["Invalid use of terminology. Expected term, term group <group> or term code <code>"]
        print_list_strs(res)
    elif user_command_parts[0] == "measure":
        MEASURE_ERROR = "Invalid use of measure. Expected measure valid <unit> or measure equiv <unit1> <unit2>"
        if len(user_command_parts) == 3:
            if user_command_parts[1] == "valid":
                print(ms.is_valid_units_string(user_command_parts[2]))
            else:
                print(MEASURE_ERROR)
        elif len(user_command_parts) == 4:
            if user_command_parts[1] == "equiv":
                print(ms.units_equivalent(user_command_parts[2], user_command_parts[3]))
            else:
                print(MEASURE_ERROR)
        else:
            print(MEASURE_ERROR)
    else:
        print("Command not recognised.")