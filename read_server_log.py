import json
import glob
import numpy as np
from datetime import datetime
import pandas as pd
import re

path = '/srv/web_log/'
date = str(datetime.now().date()).replace('-','')

glob_files = glob.glob(path + 'local.' + date +'*.log')

##### JY Algorithm
all_df = pd.DataFrame({'REQUEST_PATH':[], 'KEY':[], 'DATA_TYPE':[]})

for log_path in glob_files:
    with open(log_path, 'r') as log_file:
        log_lines = log_file.readlines()

    data_list = []

    pattern = re.compile(r'\"data\":\"(.*?)\",')

    for line in log_lines:
        timestamp_str, _, json_data = line.strip().split('\t', 2)

        json_data = json_data.replace("'", '"')

        match = pattern.search(json_data)
        if match:
            data_str = match.group(1)

            data_str = data_str.replace('"', '\\"')
            json_data = json_data.replace(f'"{data_str}"', f'"{data_str}"')

        try:
            data_dict = json.loads(json_data)
        except json.JSONDecodeError as e:
            try:
                data_str = json_data.replace('"[', '[').replace(']"', ']').replace(" (Insp. O2 - Exp. O2)", '').replace(
                    " (Liquid)", '').replace('"data":"', '"data":')
                data_str = data_str[:data_str.find('message') - 2] + "}"
                data_str = data_str.replace(" (Insp. O2 - Exp. O2)", "")
                data_str = data_str.replace('"Consumption Desflurane (Liquid)"', '"Consumption Desflurane"')
                data_str = data_str.replace('}}"', '}}')
                data_dict = json.loads(data_str)
                data_dict['REQUEST_PATH'] = data_dict['path']
            except:
                print(f"Error decoding JSON data: {e}")
                print(f"Problematic JSON-like string: {json_data}")
                continue
                # break

        request_path = data_dict.get("REQUEST_PATH", "")

        for key, value in data_dict.items():
            if key not in ("REQUEST_PATH", "RESPONSE_STATUS"):
                data_type = type(value).__name__

                if data_type == "dict":
                    for sub_key, sub_value in value.items():
                        data_list.append({"REQUEST_PATH": request_path, "KEY": key, "VALUE_PARAM": sub_key, "VALUE": sub_value})
                else:
                    data_list.append({"REQUEST_PATH": request_path, "KEY": key, "DATA_TYPE": data_type, "VALUE": str(value)})

    df = pd.DataFrame(data_list)
    all_df = pd.concat([all_df, df])

all_df['REQUEST_PATH'].unique()
all_df.to_csv('/srv/project_data/log_analytics/all_df.csv', index=False)
recording = all_df[all_df['REQUEST_PATH'] == '/client/recording_info']
numeric = all_df[all_df['REQUEST_PATH'] == '/client/numeric_stream']
recording.to_csv('/srv/project_data/log_analytics/recording.csv', index=False)
numeric.to_csv('/srv/project_data/log_analytics/numeric.csv', index=False)

len(all_df)
all_df.keys()
all_df['REQUEST_PATH'].unique()
all_df[all_df['REQUEST_PATH'] == '/client/recording_info']['KEY'].unique()
all_df[all_df['REQUEST_PATH'] == '/client/recording_info']['DATA_TYPE'].unique()
all_df[all_df['REQUEST_PATH'] == '/client/recording_info']['VALUE_PARAM'].unique()

all_df[(all_df['REQUEST_PATH'] == '/client/recording_info') & (all_df['KEY'] == 'PARAM')][['VALUE', 'VALUE_PARAM', 'KEY']]




######################### TEST

data_list = []

pattern = re.compile(r'\"data\":\"(.*?)\",')

for line in log_lines:
    timestamp_str, _, json_data = line.strip().split('\t', 2)
    json_data = json_data.replace("'", '"')

    match = pattern.search(json_data)
    if match:
        data_str = match.group(1)

        data_str = data_str.replace('"', '\\"')
        json_data = json_data.replace(f'"{data_str}"', f'"{data_str}"')

    try:
        data_dict = json.loads(json_data)
    except json.JSONDecodeError as e:
        try:
            data_str = json_data.replace('"[', '[').replace(']"', ']').replace(" (Insp. O2 - Exp. O2)", '').replace(
                " (Liquid)", '').replace('"data":"', '"data":')
            data_str = data_str[:data_str.find('message') - 2] + "}"
            data_str = data_str.replace(" (Insp. O2 - Exp. O2)", "")
            data_str = data_str.replace('"Consumption Desflurane (Liquid)"', '"Consumption Desflurane"')
            data_str = data_str.replace('}}"', '}}')
            data_dict = json.loads(data_str)
            data_dict['REQUEST_PATH'] = data_dict['path']
        except:
            print(f"Error decoding JSON data: {e}")
            print(f"Problematic JSON-like string: {json_data}")
            continue
            # break

    request_path = data_dict.get("REQUEST_PATH", "")

    for key, value in data_dict.items():
        if key not in ("REQUEST_PATH", "RESPONSE_STATUS"):
            data_type = type(value).__name__

            if data_type == "dict":
                for sub_key, sub_value in value.items():
                    data_list.append(
                        {"REQUEST_PATH": request_path, "KEY": key, "VALUE_PARAM": sub_key, "VALUE": sub_value})
            else:
                data_list.append(
                    {"REQUEST_PATH": request_path, "KEY": key, "DATA_TYPE": data_type, "VALUE": str(value)})

df = pd.DataFrame(data_list)

df['REQUEST_PATH'].unique()
data_dict.get("path", "")

df[df['REQUEST_PATH'] == '/client/numeric_stream']
