#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" TeamModel(팀 데이터처리) """


class TeamModel:
    def __init__(self):
        pass

    def get_team(self, data):
        """팀기록 가져오기(현재 연도기록/일반)"""
        if not data:
            return False

        query = """
            SELECT pid
            FROM %s
            WHERE pid = '%s' AND year = '%s'
            """ % (
            TEAMS,
            data["id"],
            data["year"],
        )

        team = db.fetch_one(query)

        return team

    def get(self, data):
        """팀기록 가져오기(현재 연도기록/전체)"""
        if not data:
            return False

        query = """
            SELECT *
            FROM %s AS u
            JOIN %s AS t
            ON u.id = t.pid
            WHERE u.pid = '%s' AND t.year = '%s'
            """ % (
            USERS,
            TEAMS,
            data["pid"],
            data["year"],
        )

        team = db.fetch_one(query)

        return team

    def get_all(self, user_id):
        """팀기록 가져오기(사용자 기록/전체)"""
        if not user_id:
            return False

        query = """
            SELECT kat,
                   dsb,
                   ltg,
                   ncd,
                   skw,
                   kwh,
                   lgt,
                   hhe,
                   ssl,
                   ktw
            FROM %s
            WHERE pid = '%s'
            """ % (
            TEAMS,
            user_id,
        )

        team = db.fetch_all(query)

        if len(team) == 0:
            result = {}
        else:
            result = team

        return result

    def delete(self, data):
        """팀기록 삭제(현재연도/전체)"""
        if not data:
            return False

        year_condition = ""
        if not data["del_all"]:
            year_condition = "AND year = '%s'" % (data["year"])

        query = """
            DELETE FROM %s
            WHERE pid = '%s' %s
            RETURNING id
            """ % (
            TEAMS,
            data["id"],
            year_condition,
        )

        res = db.execute(query)

        return res

    def post(self, data):
        """팀기록 추가"""
        if not data:
            return False

        year_list = [data["year"]]
        if data["type"] == "new":
            year_list = [2017, 2018, 2019, 2020]

        for _year in year_list:
            query = """
                INSERT INTO %s (pid, year)
                VALUES (%s, %s)
                RETURNING id
                """ % (
                TEAMS,
                data["id"],
                _year,
            )

            team_id = db.execute(query)
        return team_id

    def put(self, data):
        """팀기록 수정"""
        if not data:
            return False

        if not "anonym_team" in data and not "anonym_res" in data:
            for _team in TEAMNAMES:
                if data[_team]:
                    team = _team
                    score = data[_team]
        else:
            team = data["anonym_team"]
            score = data["anonym_res"]

        query = """
            UPDATE %s
            SET %s='%s'
            WHERE pid='%s' AND year='%s'
            RETURNING id
            """ % (
            TEAMS,
            team,
            score,
            data["pid"],
            data["year"],
        )

        res = db.fetch_one(query)

        return res

    def get_teams_all(self, data):
        if not data:
            return False

        email = data.get("email")
        year = data.get("year")

        teams = db.fetch_all(
            """
            SELECT t.kat,
                   t.dsb,
                   t.ltg,
                   t.ncd,
                   t.skw,
                   t.kwh,
                   t.lgt,
                   t.hhe,
                   t.ssl,
                   t.ktw
            FROM %s AS u
            JOIN %s AS t
            ON u.id = t.pid
            WHERE u.pid = '%s'
            AND t.year = '%d'
            ORDER BY t.year DESC
            """
            % (USERS, TEAMS, email, year)
        )

        if len(teams) > 0:
            result = teams[0]
        else:
            result = {}

        return result

    def get_details(self, data):
        if not data:
            return False

        email = data.get("email")
        versus = data.get("versus")
        year = data.get("year")

        versus_condition = ""
        versus_condition = "AND r.versus = '%s' AND r.year = '%s'" % (versus, year)

        query = """
            SELECT r.getscore, r.lostscore, r.regdate, r.result, r.versus, r.myteam, u.team
            FROM %s AS u
            JOIN %s AS r
            ON r.pid = u.id
            WHERE u.pid = '%s' %s
            ORDER BY r.regdate DESC
            """ % (
            USERS,
            RECORDS,
            email,
            versus_condition,
        )

        record = db.fetch_all(query)

        return record
