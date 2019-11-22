#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

"""AdminModel(관리자 데이터처리) """


class AdminModel:

    def __init__(self):
        pass

    def get_scores(self, playdate):
        """ 경기데이터조회"""
        if not playdate:
            return False

        query = """
            SELECT id, hometeam, homescore, awayteam, awayscore, stadium, starttime
            FROM %s
            WHERE playdate = '%s'
            """ % (SCORES, playdate)

        scores = db.fetch_all(query)

        return scores

    def put_score(self, data):
        """ 경기데이터수정"""
        if not data:
            return False

        query = """
            UPDATE %s
            SET awayscore = '%s', homescore = '%s'
            WHERE id = '%s'
            RETURNING id
            """ % (SCORES, data["awayscore"], data["homescore"], data["dbid"],)

        res = db.fetch_one(query)

        return res

    def get_users(self, data):
        """ 사용자전체리스트"""
        if not data:
            return False

        team = data["team"]
        keyword = data["keyword"]

        if team == "all":
            team = ""

        query = """
            SELECT id, pid, regdate, team, fcm_token
            FROM {0}
            WHERE pid LIKE '%{1}%'
            AND team LIKE '%{2}%'
            ORDER BY regdate DESC
            """.format(USERS, keyword, team, )

        users = db.fetch_all(query)

        return users

    def get_user_records(self, data):
        """ 사용자기록리스트"""
        if not data:
            return False

        query = """
            SELECT pid, year, versus, result, regdate
            FROM %s
            WHERE pid = '%s'
            ORDER BY regdate DESC
            """ % (RECORDS, data["user_id"])

        records = db.fetch_all(query)

        return records
