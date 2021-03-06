import difflib
import filecmp
import io
import sys
import json

from print_classes import Bcolors as bcolors

args = sys.argv
del args[0]  # get rid of main.py
num_of_args = len(args)
if num_of_args != 2:
    print(f'{bcolors.FAIL}Incorrect number of arguments. Should have 2 filenames')

file_one = args[0]
file_two = args[1]


def get_file_end(file_reader):
    file_reader.seek(0, io.SEEK_END)  # go to the file end.
    file_reader_eof = file_reader.tell()
    file_reader.seek(0, 0)  # go to the start of the file
    return file_reader_eof


files_are_same = filecmp.cmp(file_one, file_two)
if files_are_same:
    print(f'{bcolors.OKGREEN}Files {file_one} and {file_two} are the same')
    exit(code=0)

file_reader_1 = open(file_one, "r")
file_reader_1_eof = get_file_end(file_reader_1) 

file_reader_2 = open(file_two, "r")
file_reader_2_eof = get_file_end(file_reader_2) 

file_1_is_at_end = False
file_2_is_at_end = False
line_number = 1
all_differences = []
diff_two = []
while True:

    if file_reader_1.tell() == file_reader_1_eof:
        file_1_is_at_end = True

    if file_reader_2.tell() == file_reader_2_eof:
        file_2_is_at_end = True

    if file_1_is_at_end and file_2_is_at_end:
        if len(all_differences) == 0:
            print(f"{bcolors.OKGREEN}Both files are at the end, they are the same")
        else:
            print(f"{bcolors.FAIL}Both files are at the end but have differences ")
        break
    elif file_1_is_at_end and not file_2_is_at_end:
        print(f"{bcolors.FAIL}{file_one} reached the end before {file_two}. They are not the same")
        break
    elif not file_1_is_at_end and file_2_is_at_end:
        print(f"{bcolors.FAIL}{file_two} reached the end before {file_one}. They are not the same")
        break

    file_one_string = file_reader_1.readline()
    file_two_string = file_reader_2.readline()

    if file_one_string == file_two_string:
        line_number = line_number + 1
        continue
    else:
        diff = difflib.context_diff(file_one_string, file_two_string, lineterm='')
        diff_two.append(''.join(diff))

        differences = []
        differences.append({
            'file_1_string': file_one_string,
            'file_2_string': file_two_string,
            'line_number': line_number
        })
        all_differences.append(differences)
        continue

if len(all_differences) == 0:
    print(f"{bcolors.OKGREEN} No Differences")
else:
    # diff = json.dumps(all_differences)
    # output = open('results.json', 'w')
    # output.write(diff)
    # output.close()
    print('\n'.join(diff_two))


