#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

"""AdminModel(관리자 데이터처리) """


class AdminModel:
    def __init__(self):
        pass

    def get_scores(self, playdate):
        """경기데이터조회"""
        if not playdate:
            return False

        query = """
            SELECT id,
                   hometeam,
                   homescore,
                   awayteam,
                   awayscore,
                   stadium,
                   starttime
            FROM %s
            WHERE playdate = '%s'
            """ % (
            SCORES,
            playdate,
        )

        scores = db.fetch_all(query)

        return scores

    def get_day_games(self, playdate):
        """경기 리스트"""
        if not playdate:
            return False

        query = """
            SELECT hometeam,
                   homescore,
                   awayteam,
                   awayscore
            FROM %s
            WHERE playdate = '%s'
            """ % (
            SCORES,
            playdate,
        )

        scores = db.fetch_all(query)

        return scores

    def put_score(self, data):
        """경기데이터수정"""
        if not data:
            return False

        query = """
            UPDATE %s
            SET awayscore = '%s', homescore = '%s'
            WHERE id = '%s'
            RETURNING id
            """ % (
            SCORES,
            data["awayscore"],
            data["homescore"],
            data["dbid"],
        )

        res = db.fetch_one(query)

        return res

    def post_new_game(self, data):
        """경기등록"""
        if not data:
            return False

        play_date = data.get("playdate", "")
        away_team = data.get("awayteam", "")
        home_team = data.get("hometeam", "")
        stadium = data.get("stadium", "")
        start_time = data.get("starttime", "")

        if (
            play_date == ""
            or away_team == ""
            or home_team == ""
            or stadium == ""
            or start_time == ""
        ):
            return False

        query = """
            INSERT INTO %s
            (playdate, awayteam, awayscore, hometeam, homescore, stadium, starttime)
            VALUES ('%s', '%s', 998, '%s', 998, '%s', '%s') RETURNING id """ % (
            SCORES,
            play_date,
            away_team,
            home_team,
            stadium,
            start_time,
        )

        res = db.fetch_one(query)

        return res

    def get_users(self, data, args):
        """사용자전체리스트"""
        if not data:
            return False

        team = data["team"]
        keyword = data["keyword"]

        query_page = int(args.get("page"))
        query_limit = int(args.get("size", 10))

        #: Paging 대응
        offset = (query_page - 1) * query_limit
        limit = query_limit

        if team == "all":
            team = ""

        query = """
            SELECT id as id,
                   pid as email,
                   regdate as regDate,
                   team as team,
                   fcm_token as fcmToken
            FROM {0}
            WHERE pid LIKE '%{1}%'
            AND team LIKE '%{2}%'
            ORDER BY regdate DESC
            OFFSET {3}
            LIMIT {4}
            """.format(
            USERS, keyword, team, int(offset), int(limit)
        )

        users = db.fetch_all(query)

        return users

    def get_user_records(self, data):
        """사용자기록리스트"""
        if not data:
            return False

        query = """
            SELECT pid,
                   year,
                   versus,
                   result,
                   regdate
            FROM %s
            WHERE pid = '%s'
            ORDER BY regdate DESC
            """ % (
            RECORDS,
            data["user_id"],
        )

        records = db.fetch_all(query)

        return records
