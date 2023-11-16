import json
import glob
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import re

path = '/srv/web_log/'
date = str((datetime.now() - timedelta(days=1)).date()).replace('-','')

glob_files = glob.glob(path + 'client.' + date +'*.log')

##### 새로운 알고리즘
keys_to_extract = []
function_data = pd.DataFrame({})
for file in glob_files:
    with open(file, 'r') as log_file:
        log_lines = log_file.readlines()
    for line in log_lines:
        temp = line.split('\t')[2].strip()
        json_dict = json.loads(temp)
        if json_dict['function'] not in keys_to_extract:
            keys_to_extract.append(json_dict['function'])

test = pd.DataFrame(columns=keys_to_extract)
test_trans = test.transpose()
column_data = [[i] for i in range(0, len(test_trans))]

for file in glob_files:
    with open(file, 'r') as log_file:
        log_lines = log_file.readlines()
    for line in log_lines:
        temp = line.split('\t')[2].strip()
        json_dict = json.loads(temp)
        idx = keys_to_extract.index(json_dict['function'])
        column_data[idx].append(json_dict)

for i in range(len(column_data)):
    if len(column_data[i]) != 7282:
        while True:
            column_data[i].append(np.nan)
            if len(column_data[i]) == 7282:
                break

for idx, i in enumerate(keys_to_extract):
    test[i] = column_data[idx]

# test.to_excel('/srv/project_data/log_analytics/client_all_df2.xlsx', index=False)
test.to_excel('/home/wlsdud022/client_all_df2.xlsx', index=False)
keys_to_extract