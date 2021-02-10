import argparse
import json
import os

import pandas as pd
import xmltodict
from dictdiffer import diff
from dicttoxml import dicttoxml

parser = argparse.ArgumentParser(description="Compare Two XML Files")
parser.add_argument('file_1', type=str,
                    help='Filename for the first file to compare')
parser.add_argument('file_2', type=str,
                    help='Filename for the second file to compare')
parser.add_argument('output', type=str, help="Output format JSON or XML")
parser.add_argument('sortable_index', type=str, default='',
                    help='the name of the sortable index')

args = parser.parse_args()

file_1 = args.file_1
file_2 = args.file_2
sortable_index = args.sortable_index

output_format = str(args.output).lower()

file_1_name = os.path.splitext(file_1)[0]
file_2_name = os.path.splitext(file_2)[0]

text1 = open(file_1).read()
text2 = open(file_2).read()


def covert_xml_to_dataset(xml: str, index: str):
    text_dict = xmltodict.parse(xml)
    # Create a new dataframe
    df = pd.DataFrame.from_dict(text_dict['Dataset']['Row'])
    # remove empty rows
    df.dropna('index', how='all', inplace=True)
    # covert to numeric instead of str
    if index != '':
        df[index] = pd.to_numeric(df[index], downcast='integer')
        # sort by account number
        df.sort_values(by=[index], inplace=True)
        df.reset_index(inplace=True, drop=True)

    # create the dictonary like [{key: value, key: value}, {key: value, key: value]
    return df.to_dict(orient='records')


def remove_unmatched_index_numbers(dict_1, dict_2, index):
    set_1 = set()
    set_2 = set()

    for item in dict_1:
        set_1.add(item[index])

    for item in dict_2:
        set_2.add(item[index])

    # these need to be removed from dict_1
    dict_1_values_not_in_dict_2 = set_1 - set_2
    # these need to be removed from dict_2
    dict_2_values_not_in_dict_1 = set_2 - set_1
  
    new_dict_1 = [x for x in dict_1 if x[index] not in dict_1_values_not_in_dict_2]
    new_dict_2 = [x for x in dict_2 if x[index] not in dict_2_values_not_in_dict_1]

    return new_dict_1, new_dict_2


file_dict_1_unfiltered = covert_xml_to_dataset(text1, sortable_index)
file_dict_2_unfiltered = covert_xml_to_dataset(text2, sortable_index)

# removing records that do not have a match in the other dataset
file_dict_1, file_dict_2 = remove_unmatched_index_numbers(file_dict_1_unfiltered, file_dict_2_unfiltered, sortable_index)

file_1_output = open(f"output/{file_1_name}.json", "w")
file_1_output.writelines(json.dumps(file_dict_1))
file_1_output.close()

file_2_output = open(f"output/{file_2_name}.json", "w")
file_2_output.writelines(json.dumps(file_dict_2))
file_2_output.close()

result = diff(file_dict_1, file_dict_2)
result = list(result)

change_dict = {}

for res in result:
    if res[0] != 'change':
        continue
    change_reason = res[1][-1]
    current_val = change_dict.get(change_reason, 0)
    change_dict[change_reason] = current_val + 1


# Json
if output_format == 'json':
    json_result_output = open('output/results.json', 'w')
    json_result_output.writelines(json.dumps(result))
    json_result_output.close()

# XML OUTPUT
if output_format == 'xml':
    result_xml = dicttoxml(result)
    xml_result_output = open('output/results.xml', 'w')
    xml_result_output.writelines(result_xml.decode('UTF-8'))
    xml_result_output.close()



