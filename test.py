import argparse
import json
import os

import pandas as pd
import xmltodict
from dictdiffer import diff
from dicttoxml import dicttoxml

parser = argparse.ArgumentParser(description="Compare Two XML Files")
parser.add_argument('file_1', type=str, help='Filename for the first file to compare')
parser.add_argument('file_2', type=str, help='Filename for the second file to compare')
parser.add_argument('output', type=str, help="Output format JSON or XML")

args = parser.parse_args()

file_1 = args.file_1
file_2 = args.file_2
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
    df[index] = pd.to_numeric(df[index], downcast='integer')
    # sort by account number
    df.sort_values(by=[index], inplace=True)
    df.reset_index(inplace=True, drop=True)

    # create the dictonary like [{key: value, key: value}, {key: value, key: value]
    return df.to_dict(orient='records')


file_dict_1 = covert_xml_to_dataset(text1, 'accountnumber')
file_1_output = open(f"output/{file_1_name}.json", "w")
file_1_output.writelines(json.dumps(file_dict_1))
file_1_output.close()

file_dict_2 = covert_xml_to_dataset(text2, 'accountnumber')
file_2_output = open(f"output/{file_2_name}.json", "w")
file_2_output.writelines(json.dumps(file_dict_2))
file_2_output.close()

result = diff(file_dict_1, file_dict_2)
result = list(result)

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
