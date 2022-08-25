#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" StaticsModel(통계 데이터처리) """


class StaticsModel:
    def __init__(self):
        pass

    def get_records(self, data):
        if not data:
            return False

        email = data.get("email")

        records = db.fetch_all(
            """
            SELECT r.id,
                   r.year,
                   r.versus,
                   r.myteam,
                   r.result,
                   r.getscore,
                   r.lostscore,
                   r.regdate,
                   u.team,
                   u.id
            FROM %s AS u
            JOIN %s AS r
            ON u.id = r.pid
            WHERE u.pid = '%s'
            ORDER BY r.regdate DESC
            """
            % (USERS, RECORDS, email)
        )

        if len(records) > 0:
            result = records
        else:
            result = {}

        return result
