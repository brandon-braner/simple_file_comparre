import filecmp
import io
import sys

args = sys.argv
del args[0]  # get rid of main.py
num_of_args = len(args)
if num_of_args != 2:
    print 'Incorrect number of arguments. Should have 2 filenames'

file_one = args[0]
file_two = args[1]


def get_file_end(file_reader):
    file_reader.seek(0, io.SEEK_END)  # go to the file end.
    file_reader_eof = file_reader.tell()
    file_reader.seek(0, 0)  # go to the start of the file
    return file_reader_eof


files_are_same = filecmp.cmp(file_one, file_two)
if files_are_same:
    print 'Files %s and %s are the same'%(file_one, file_two)
    exit(code=0)

file_reader_1 = open(file_one, "r")
file_reader_1_eof = get_file_end(file_reader_1) 

file_reader_2 = open(file_two, "r")
file_reader_2_eof = get_file_end(file_reader_2) 

file_1_is_at_end = False
file_2_is_at_end = False
line_number = 0

while True:

    if file_reader_1.tell() == file_reader_1_eof:
        file_1_is_at_end = True

    if file_reader_2.tell() == file_reader_2_eof:
        file_2_is_at_end = True

    if file_1_is_at_end and file_2_is_at_end:
        print("Both files are at the end, they are the same")
    elif file_1_is_at_end and not file_2_is_at_end:
        print "%s reached the end before %s. They are not the same"%(file_one, file_two)
    elif not file_1_is_at_end and file_2_is_at_end:
        print "% reached the end before%}. They are not the same"%(file_one, file_two)

    file_one_string = file_reader_1.readline()
    file_two_string = file_reader_2.readline()

    if file_one_string == file_two_string:
        line_number = line_number + 1
        continue
    else:
        # print "Files are different at line number {line_number}".format(line_number)
        print "%s is %s"%(file_one, file_one_string)
        print "%s is %s"%(file_two, file_two_string)
        break



