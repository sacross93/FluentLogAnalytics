import json
import glob
from datetime import datetime, timedelta
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import timezone
timeZone = timezone(timedelta(hours=-9))
from pytz import timezone

path = '/srv/web_log/'
date = str((datetime.now() - timedelta(days=1)).date()).replace('-','')
result = False
cnt = 0
bedArr = [
    'C-01', 'C-03', 'C-06',
    'D-01', 'D-02', 'D-03', 'D-04', 'D-05','D-06',
    'E-01', 'E-02',
    'F-06', 'F-08',
    'J-01', 'J-02','J-03', 'J-04', 'J-05', 'J-06',
    'K-01', 'K-02', 'K-03', 'K-04', 'K-05', 'K-06',
    'OB-01'
]
rowIdx= ['C', 'D', 'E', 'F', 'J', 'K', 'OB']


while result==False:
    date = str((datetime.strptime(date, "%Y%m%d") - timedelta(days=1)).date()).replace('-','')
    glob_files = glob.glob(path + 'client.' + date +'*.log')

    bedList = []
    rssiList = []
    timeList = []
    rssiPattern = re.compile(r'RSSI:.*')
    for file in glob_files:
        with open(file, 'r') as log_file:
            log_lines = log_file.readlines()
        for line in log_lines:
            temp = line.split('\t')[2].strip()
            logTime = line.split('\t')[0]
            dt_object = datetime.fromisoformat(logTime)
            json_dict = json.loads(temp)
            if 'wifi' in json_dict.keys():
                bedList.append(json_dict['BED'])
                findRssi = next((element for element in json_dict['wifi'].split(', ') if rssiPattern.match(element)), None)
                findRssi = findRssi.split(': ')[1]
                rssiList.append(findRssi)
                timeList.append(dt_object)

    df = pd.DataFrame({'time':timeList, 'bed':bedList, 'rssi':rssiList})
    df.sort_values('time', inplace=True)
    df['rssi'] = df['rssi'].astype(int)
    beds_group = df['bed'].str.extract(r'([A-Z]+)-')[0].unique()
    df['bed_group']= df['bed'].str.extract(r'([A-Z]+)-')

    beds = df['bed'][df['bed'].str.contains(r'([A-Z]+)-')].unique()

    ################## TEST2
    df.sort_values(['time','bed_group'], ascending=True, inplace=True)

    colLength = 0
    for i in df['bed_group'].unique():
        temp = len(df['bed'][df['bed'].str.contains(f'{i}-0')].unique())
        if temp > colLength:
            colLength = temp
    beds_group = beds_group[pd.isnull(beds_group) == False]
    beds_group.sort()
    rowLength = len(beds_group)

    fig = plt.figure(figsize=(24, 14))
    gs = GridSpec(nrows=rowLength, ncols=colLength, figure=fig, hspace=0.5, wspace=0.1)
    fig.suptitle(f'{date}-Network QC', fontsize=26, fontweight='bold')
    fig.subplots_adjust(top=0.9)

    # x_min = df['time'].min()
    # x_max = df['time'].max()
    x_min = (datetime.strptime(date, "%Y%m%d")).astimezone(timeZone)
    x_max = (datetime.strptime(date, "%Y%m%d") + timedelta(days=1)).astimezone(timeZone)
    y_min = -85
    y_max = -30

    for groupIdx, group in enumerate(beds_group):
        col = groupIdx
        for bedIdx, bed in enumerate(beds):

            bedList = df[df['bed_group'] == group].sort_values('bed')
            try:
                bedRow = np.where(bed == bedList['bed'].unique())[0][0]
            except:
                continue
            ax = fig.add_subplot(gs[groupIdx, bedRow])
            bedData = df['rssi'][df['bed']==bed]
            bedTime = df['time'][df['bed'] == bed]
            ax.plot(bedTime, bedData, linewidth=2, marker='o', markersize=4, markerfacecolor='black', markeredgewidth='0')
            # ax.scatter(bedTime, bedData, s=3)
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            if groupIdx != colLength-1:
                ax.xaxis.set_visible(False)
            if bedRow != 0:
                ax.yaxis.set_visible(False)
            # ax.set_title(bed, fontsize=12, fontweight='bold', loc='center', pad=-0.5)
            if len(bedData[bedData <= -80]) != 0:
                ax.text(x_min + timedelta(minutes=20), y_max-12, bed, fontsize=12, color='red')
                cnt += 1
                if cnt >= 0: ## Stop standard
                    result=True
            else :
                ax.text(x_min + timedelta(minutes=20), y_max - 12, bed, fontsize=12)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d, %H:%M'))
            ax.axhline(-80, color='red', linestyle='--')
            ax.tick_params(axis='x', rotation=45)

    # plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.07)
    # plt.savefig(f'/srv/project_data/log_analytics/networkQCpig/{date}.png')
    plt.show()
    plt.close()

####### Individual Graph
targetBed = 'D-05'
targetDate = '20231007'

glob_files = glob.glob(path + 'client.' + targetDate + '*.log')

bedList = []
rssiList = []
timeList = []
rssiPattern = re.compile(r'RSSI:.*')
for file in glob_files:
    with open(file, 'r') as log_file:
        log_lines = log_file.readlines()
    for line in log_lines:
        temp = line.split('\t')[2].strip()
        logTime = line.split('\t')[0]
        dt_object = datetime.fromisoformat(logTime)
        json_dict = json.loads(temp)
        if 'wifi' in json_dict.keys():
            bedList.append(json_dict['BED'])
            findRssi = next((element for element in json_dict['wifi'].split(', ') if rssiPattern.match(element)), None)
            findRssi = findRssi.split(': ')[1]
            rssiList.append(findRssi)
            timeList.append(dt_object)
df = pd.DataFrame({'time':timeList, 'bed':bedList, 'rssi':rssiList})
df.sort_values('time', inplace=True)
df['rssi'] = df['rssi'].astype(int)


x_min = (datetime.strptime(targetDate, "%Y%m%d")).astimezone(timezone('Asia/Seoul'))
x_max = (datetime.strptime(targetDate, "%Y%m%d") + timedelta(days=1)).astimezone(timezone('Asia/Seoul'))

tartgetData = df[(df['bed'] == targetBed) & ((df['time']>= x_min) & (df['time'] <= x_max))]
timeDiff = np.append(np.array([0]), np.diff(tartgetData['time'].astype(int) // 1000000000))
dataIdx = np.where(tartgetData['rssi']<= -80)[0]

diffVal = (timeDiff[dataIdx[0]] + timeDiff[dataIdx[-1]]) // 60
plt.figure(figsize=(12,8))
plt.plot(tartgetData['time'], tartgetData['rssi'], linewidth=2, marker='o', markersize=4, markerfacecolor='black', markeredgewidth='0')
plt.axhline(-80, color='red', linestyle='--')
plt.text(tartgetData['time'].iloc[dataIdx[0]-5], tartgetData['rssi'].min() - 2, f'On a time interval : {diffVal}min', fontsize=12)
plt.tight_layout()
plt.show()

