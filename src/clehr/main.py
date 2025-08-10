from terminology import CSVTerminologyService
from org.openehr.rm.data_types.text import CodePhrase

print("Welcome to clehr - using pyehr, a Python implemention of OpenEHR")

ts = CSVTerminologyService("ICD10(2020)", "data/icd10_2020.csv", "en")

def print_list_strs(lst):
    for item in lst:
        print(str(item))

while True:
    user_command = input("clehr> ")
    user_command_parts = user_command.split(' ')
    if user_command_parts[0] == "exit":
        break
    elif user_command_parts[0] == "term":
        te = ts.terminology("ICD10(2020)")
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
            res = ["Invalid use of terminology. Expected terminology, terminology group <group> or terminology code <code>"]
        print_list_strs(res)
    else:
        print("Command not recognised.")