#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" ScoreModel(점수 데이터처리) """


class ScoreModel:
    def __init__(self):
        pass

    def get(self, data):
        """점수 가져오기"""
        if not data:
            return False

        query = """
            SELECT playdate,
                   hometeam,
                   homescore,
                   awayteam,
                   awayscore,
                   stadium
            FROM %s
            WHERE playdate = '%s'
            AND (hometeam = '%s' OR awayteam = '%s')
            """ % (
            SCORES,
            data["playdate"],
            data["favteam"],
            data["favteam"],
        )

        score = db.fetch_one(query)

        return score

    def getAll(self, data):
        """점수 가져오기"""
        if not data:
            return False

        query = """
            SELECT playdate,
                   hometeam,
                   homescore,
                   awayteam,
                   awayscore,
                   stadium
            FROM %s
            WHERE playdate = '%s'
            AND (hometeam = '%s' OR awayteam = '%s')
            """ % (
            SCORES,
            data["playdate"],
            data["favteam"],
            data["favteam"],
        )

        score = db.fetch_all(query)

        return score

    def get_score_with_time(self, data):
        """기록 가져오기(경기정보)"""
        if not data:
            return False

        regdate = data.get("regdate")
        team = data.get("team")

        query = """
            SELECT id,
                   awayteam,
                   awayscore,
                   hometeam,
                   homescore,
                   playdate,
                   stadium,
                   starttime
            FROM %s
            WHERE playdate = '%s'
            AND (awayteam = '%s' or hometeam = '%s')
            ORDER BY starttime
            """ % (
            SCORES,
            regdate,
            team,
            team,
        )

        scores = db.fetch_all(query)

        if len(scores) > 0:
            result = scores
        else:
            result = [
                {
                    "awayscore": 0,
                    "awayteam": team,
                    "homescore": 0,
                    "hometeam": team,
                    "id": 0,
                    "playdate": int(regdate),
                    "stadium": "",
                    "starttime": 0,
                }
            ]

        return result
