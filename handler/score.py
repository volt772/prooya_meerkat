#!/usr/bin/python3
# -*-coding:utf-8 -*-

from handler import *

""" ScoreHandler(점수 처리) """


class ScoreHandler:
    def __init__(self):
        pass

    def get_score(self, data):
        """경기일 점수정보"""
        if not data:
            return jsonify({"res": False})

        score = False

        playdate = data["playdate"]
        favteam = data["favteam"]
        score = MSCORE.get({"playdate": playdate, "favteam": favteam})

        if not score:
            score = {
                "hometeam": "",
                "homescore": "",
                "awayteam": "",
                "awayscore": "",
                "playdate": "",
                "playresult": "",
            }
        else:
            score["playresult"] = utils.check_play_result(score, favteam)

            playdate = score["playdate"]
            _year = str(playdate)[0:4]
            _month = str(playdate)[4:6]
            _day = str(playdate)[6:8]
            readable_date = "%s-%s-%s" % (
                _year,
                _month,
                _day,
            )
            score["playdate"] = readable_date

        return jsonify({"res": score})
