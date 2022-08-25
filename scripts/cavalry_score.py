# -*- coding: utf-8 -*-

import datetime
import sys
import time

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")
date = year + month + day  # "20130615"

con = connect(dbname="prooya", user="prooya", host="localhost", password="CjsdksgkA77@")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


def update_cavalry_score(_id):
    try:
        query = """UPDATE scores
                SET awayscore=997, homescore=997
                WHERE awayscore=998
                AND homescore=998
                AND playdate='{0}'
                AND id='{1}'""".format(
            date, _id
        )

        cur = con.cursor()
        cur.execute(query)
        cur.close()
        print("{0} || Game Started".format(datetime.datetime.now()))
    except Exception as e:
        print("{0} || Update Data Err : {1}".format(datetime.datetime.now(), str(e)))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _id = sys.argv[1]

        update_cavalry_score(_id)
