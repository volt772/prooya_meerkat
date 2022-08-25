#!/usr/bin/python
# -*-coding:utf-8-*-

import ast
import datetime
import json

import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

team_list = {
    "KIA": "kat",
    "두산": "dsb",
    "롯데": "ltg",
    "NC": "ncd",
    "SK": "skw",
    "키움": "kwh",
    "LG": "lgt",
    "한화": "hhe",
    "삼성": "ssl",
    "kt": "ktw",
}

stadium_list = {
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


def read_file(_file):
    plays = {}
    f = open(_file, "r")
    lines = f.readlines()
    for line in lines:
        p_data = json.loads(line)
        for key, val in p_data.items():
            key_arr = str(key).split(".")
            month = key_arr[0].zfill(2)
            day = key_arr[1].zfill(2)
            nkey = "2018{0}{1}".format(month, day)

            plays[nkey] = val

    f.close()

    insert_plays(plays)


def insert_plays(data):
    if not data:
        return False

    playlist_query = ""
    for key, val in data.items():
        for _k, _v in val.items():
            qdate = key
            qawayteam = team_list[_v["awayteam"]]
            qawayscore = _v["awayscore"]
            qhometeam = team_list[_v["hometeam"]]
            qhomescore = _v["homescore"]
            qregdate = datetime.datetime.now()

            qstadium = stadium_list[qhometeam]

            playlist_query += "('{0}','{1}','{2}','{3}','{4}','{5}','{6}'),".format(
                qdate, qawayteam, qawayscore, qhometeam, qhomescore, qregdate, qstadium
            )

    #: Database
    con = connect(user="prooya", host="localhost", password="CjsdksgkA77@")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    query = """INSERT INTO scores
			   (playdate, awayteam, awayscore, hometeam, homescore, regdate, stadium)
			   VALUES {0}""".format(
        playlist_query[:-1]
    )
    cur = con.cursor()
    cur.execute(query)

    cur.close()


if __name__ == "__main__":
    for i in range(3, 11):
        score_file = "./2018{0}".format(str(i).zfill(2))
        read_file(score_file)
