# -*- coding:utf-8 -*-
# @Time : 2023/5/2 上午 1:33
# @Author : Dedicatus1979
# @File : reader.py
# @Software : PyCharm

import sys
import json
import sqlite3
from pathlib import Path
import os


config_path = Path(sys.argv[0]).parent / "config.json"

try:
    with open(config_path, 'r', encoding='utf-8') as f:  # 从json读配置
        config = json.loads(f.read())
    ls_snapshot = Path(sys.argv[0]).parent / config["db_name"]
    ls_snapshot.touch()
except:
    sys.exit()


def select_date():
    conn = sqlite3.connect(ls_snapshot)
    cur = conn.cursor()
    sql = 'select * from SHEET1'
    cur.execute(sql)
    f = cur.fetchall()
    cur.close()
    conn.commit()
    return f

a = select_date()
os.system("")
for index in a:
    if index[3] == 1:
        print('\t' * index[2] + "|-", f"\033[1;33m{index[1]}\033[0m")
    elif index[3] == 0:
        print('\t' * index[2] + "|-", index[1])
        print('\t'*(index[2]+1) + "|-", "\033[1;31mUserRefuse\033[0m" )
    elif index[3] == -1:
        print('\t' * index[2] + "|-", f"\033[1;31m{index[1]}\033[0m")
    elif index[3] == 2:
        print(index[1])
    else:
        print('\t' * index[2] + "|-", index[1])

input("按任意键退出")

