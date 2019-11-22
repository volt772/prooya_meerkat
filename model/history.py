#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" HistoryModel(전체데이터) """


class HistoryModel:

    def __init__(self):
        pass

    def get_history(self, data):
        if not data:
            return False

        email = data.get("email")
        year = data.get("year")

        history = db.fetch_all("""
            SELECT r.id,
                   r.year,
                   r.versus,
                   r.result,
                   r.getscore,
                   r.lostscore,
                   r.regdate
            FROM %s AS u
            JOIN %s AS r
            ON u.id = r.pid
            WHERE u.pid = '%s'
            AND r.year = '%d'
            ORDER BY r.regdate DESC
            """ % (USERS, RECORDS, email, year)
        )

        if len(history) > 0:
            result = history
        else:
            result = {}

        return result

    def del_history(self, data):
        """ 기록 삭제(선택)"""
        if not data:
            return False

        if "pid" in data:
            del_condition = "pid = '%s'" % (data["pid"])
        else:
            del_condition = "id = '%s'" % (data["rid"])

        res = db.execute("""
            DELETE FROM %s
            WHERE %s AND year = '%s'"""
                         % (RECORDS, del_condition, data["year"]))

        return res

    def get_team_static(self, data):
        """ 팀기록 가져오기(현재 연도기록/전체)"""
        if not data:
            return False

        query = """
            SELECT *
            FROM %s AS u
            JOIN %s AS t
            ON u.id = t.pid
            WHERE u.pid = '%s' AND t.year = '%s'
            """ % (USERS, TEAMS, data["pid"], data["year"],)

        team = db.fetch_one(query)

        return team

    def post(self, data):
        """ 기록 추가"""
        if not data:
            return False

        record_id = db.fetch_one("""
            INSERT INTO %s
            (pid, year, versus, result, getscore, lostscore, regdate)
            VALUES (%s, %s, '%s', '%s', %s, %s, '%s') RETURNING id"""
                                 % (RECORDS, data["pid"], data["year"],
                                    data["versus"], data["result"],
                                    data["getscore"], data["lostscore"],
                                    data["regdate"]))

        return record_id["id"]
