#!/usr/bin/python
# -*-coding:utf-8-*-

import ast
import datetime
import json

import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

team_list = {
    "kat": "kjc",
    "dsb": "soj",
    "ltg": "bss",
    "ncd": "cwn",
    "skw": "icl",
    "kwh": "sog",
    "lgt": "soj",
    "hhe": "dje",
    "ssl": "dgl",
    "ktw": "sww",
}


con = connect(user="prooya", host="localhost", password="CjsdksgkA77@")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


def update():
    cur = con.cursor()

    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180515'"""
    cur.execute(query)
    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180516'"""
    cur.execute(query)
    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180517'"""
    cur.execute(query)
    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180710'"""
    cur.execute(query)
    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180711'"""
    cur.execute(query)
    query = """UPDATE scores SET stadium = 'poh' WHERE hometeam = 'ssl' and playdate = '20180712'"""
    cur.execute(query)
    cur.close()

    # for i in range(1, 837):
    # 	query = """SELECT hometeam FROM scores WHERE id = {0}""".format(str(i))
    # 	cur = con.cursor()
    # 	cur.execute(query)
    # 	res = cur.fetchall()

    # 	hometeam = res[0][0]
    # 	stadium = team_list[hometeam]
    # 	query = """UPDATE scores SET stadium = '{0}' WHERE id = '479'"""
    # 	cur.execute(query)
    # 	cur.close()


# 	cur = con.cursor()
# 	cur.execute(query)
#
# 	cur.close()


if __name__ == "__main__":
    update()
