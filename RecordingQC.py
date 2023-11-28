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
import pymysql

path = '/srv/web_log/'
date = str((datetime.now() - timedelta(days=1)).date()).replace('-','')
result = False
cnt = 0

sa_conn = pymysql.connect(
    user='wlsdud1512',
    passwd='wlsdud1512',
    host='192.168.44.106',
    db='sa_server',
    charset='utf8'
)
sa_cursor = sa_conn.cursor(pymysql.cursors.DictCursor)

# 인증받은 기기를 사용하는 client(태블릿 및 어플)리스트를 불러오는 SQL
sql = f"""
select *
from sa_api_client as client
join sa_api_bed as bed
on client.bed_id = bed.id
where bed.name not like '%CU%' and bed.name not like '%reserved%' and bed.name not like '%test%' and client.name like '%galaxy tab s6%'
order by bed.name asc;
"""

sa_cursor.execute(sql)
clietns = pd.DataFrame(sa_cursor.fetchall())

clietns['bed.name'].unique()