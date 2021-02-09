import difflib
import sys

import pandas as pd
import xmltodict
import json

from dict2xml import dict2xml

file_1 = 'fraudpointbadip.xml'
file_2 = 'fraudpointgoodip.xml'

# file_1 = 'xml1.xml'
# file_2 = 'xml2.xml'

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
file_dict_2 = covert_xml_to_dataset(text2, 'accountnumber')

# maybe do some crazy ass recursive thing here
# diffs = []
# for index, val in enumerate(file_dict_1):
#
#     if index in file_dict_2 and not isinstance(file_dict_1, dict):
#         index_matches = file_dict_1[index] == file_dict_2[index]
#         if not index_matches:
#             diffs.append()
#
#     if index in file_dict_2 and isinstance(file_dict_1, dict):
#         pass


# file_json_1 = json.dumps(file_dict_1)
# file_json_2 = json.dumps(file_dict_2)
xml_file_1 = dict2xml(file_dict_1)
xml_file_2 = dict2xml(file_dict_2)

xml1 = open('xml_1.xml', 'w')
xml1.writelines(xml_file_1)
xml1.close()

xml2 = open('xml_2.xml', 'w')
xml2.writelines(xml_file_2)
xml2.close()


xml1 = open('xml_1.xml', 'r')
xml2 = open('xml_2.xml', 'r')
text1 = xml1.readlines()
text2 = xml2.readlines()
d = difflib.Differ()
# delta = d.compare(text1, text2)
delta = difflib.unified_diff(text1, text2, file_1, file_2, lineterm='')

sys.stdout = open('results.txt', 'w')
sys.stdout.writelines(delta)
# delta = difflib.context_diff(text1, text2, file_1, file_2, lineterm='')


# d = difflib.Differ()
# delta = d.compare(text1, text2)
#
# sys.stdout = open('results.txt', 'w')
# sys.stdout.writelines(delta)
