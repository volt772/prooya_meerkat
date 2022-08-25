#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v1 import *

""" ScoresHandler(경기 일별 조회) """


class ScoresHandler:
    def __init__(self):
        pass

    def get_score(self, data):
        """오늘 경기정보"""
        if not data:
            return False

        scores = scm.get_score_with_time(
            {"regdate": data["regdate"], "team": data["team"]}
        )

        return jsonify({"data": {"games": scores}})
