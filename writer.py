# -*- coding:utf-8 -*-
# @Time : 2023/5/1 下午 9:40
# @Author : Dedicatus1979
# @File : writer.py
# @Software : PyCharm

import re
import sys
import json
import time
import sqlite3
from pathlib import Path


config_path = Path(sys.argv[0]).parent / "config.json"

try:
    with open(config_path, 'r', encoding='utf-8') as f:  # 从json读配置
        config = json.loads(f.read())
except:
    input("缺少必要的config.json配置文件。按任意键退出。")
    sys.exit()

ls_snapshot = Path(sys.argv[0]).parent / config["db_name"]

# -------------

# 拒绝域
refuse = ""
for s in config["refuse"]:
    s = s.replace("/", r"\\")
    s = s.split("*", 1)
    if len(s) - 1:
        refuse += "(\w:)?" + s[1] + "$|"
    else:
        refuse += "(\w:)?" + s[0] + "$|"

# 接受域
accept = ""
for s in config["accept"]:
    s = s.replace("/", r"\\")
    s = s.split("*", 1)
    if len(s) - 1:
        accept += "(\w:)?" + s[1] + r"($|\\)" + ".*|"
    else:
        accept += "(\w:)?" + s[0] + r"($|\\)" + ".*|"


pattern_refuse = re.compile(refuse[0:-1])
pattern_accept = re.compile(accept[0:-1])

# -----------------


def write_sql(conn, DirName, Layer, Note):
    # conn = sqlite3.connect(ls_snapshot)
    sql = 'insert into SHEET1 (DirName, Layer, Note) values(?, ?, ?)'
    data = (DirName, Layer, Note)
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    # cur.close()
    # conn.close()


def update_score(conn, data):
    cur = conn.cursor()
    sql_select = 'select MAX(ID) from SHEET1'
    cur.execute(sql_select)
    id = cur.fetchall()[0][0]
    sql_update = 'update SHEET1 set Note = ? where ID = ?'
    date = (data, id)
    cur.execute(sql_update, date)
    conn.commit()
    # cur.close()
    # conn.close()


def print_progress_bar(one, all_count, wait_leap=0, width=30):
    percent = int(one / all_count * 100)
    left = width * percent // 100
    right = width - left
    if one == all_count:
        symbol = '#'
    elif one % 2 == 0:
        symbol = '\\'
    else:
        symbol = '/'
    if one == all_count:
        mene = ''
    else:
        mene = '   少女祈祷中' + '.' * ((one+wait_leap) % 3 + 1) + ' ' * (2 - (one+wait_leap) % 3)
    print('\r[', '#' * left, symbol, ' ' * right, ']',
          f' {percent:.0f}%', mene,
          sep='', end='', flush=True)


start_time, now_dir, all_dir = 0, 0, 0
def read_son_dir(path, conn):
    global start_time, now_dir, all_dir
    try:
        son_list = list(path.iterdir())
    except PermissionError:
        update_score(conn, -1)
        return None

    for path_i in son_list:
        # print(path_i)
        path_s = str(path_i)
        isdir = path_i.is_dir()
        layer = path_s.count("\\")
        path_ls = path_s.split("\\")

        if layer == 1:
            now_dir = son_list.index(path_i)+1
            all_dir = len(son_list)
            start_time = time.time()
            print_progress_bar(now_dir, all_dir)
        elif time.time() - start_time > 1:
            start_time = int(time.time())
            print_progress_bar(now_dir, all_dir, start_time % 9)

        if pattern_accept.match(path_s):
            write_sql(conn, path_ls[-1], layer, None if isdir is True else 1)
            if layer < config["recursion_times"] and isdir:
                read_son_dir(path_i, conn)
            continue
        elif pattern_refuse.match(path_s):
            if isdir:
                write_sql(conn, path_ls[-1], layer, 0)
            continue
        else:
            write_sql(conn, path_ls[-1], layer, None if isdir is True else 1)
            if layer < config["recursion_times"] and isdir:
                read_son_dir(path_i, conn)


if __name__ == '__main__':
    print("磁盘文件名快照备份程序及将启动。@Dedicatus1979 https://github.com/Dedicatus1979/FileNameSnapshot")
    input("按任意键继续...")
    if Path(ls_snapshot).exists():
        Path(ls_snapshot).unlink()
    conn = sqlite3.connect(ls_snapshot)
    c = conn.cursor()
    c.execute('''CREATE TABLE SHEET1
           (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
           DirName        TEXT    NOT NULL,
           Layer          INT     NOT NULL,
           Note           INTEGER    );''')
    '''
    关于数据库的注释：
    ID          DirName     Layer            Note
    目录的编号   目录的名称    该目录是几级目录   该目录的注释
    
    Note内存放的是数值或空，
        None代表该目录是一个普通目录
        1代表该目录是个文件
        0代表该目录被用户拒绝继续访问（用户拒绝指的是在config.json中拒绝）
        -1代表该目录被系统拒绝访问
        2代表该目录是根目录
    '''
    conn.commit()
    c.close()

    for i in range(67, 91):
        disc = chr(i) + ":/"
        try:
            Path(disc).touch()
            write_sql(conn, disc, 0, 2)
            read_son_dir(Path(disc), conn)
            print("")
        except FileNotFoundError:
            pass

    conn.close()

    input("程序已结束。按任意键退出。")


