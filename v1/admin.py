#!/usr/bin/python3
# -*-coding:utf-8 -*-

from handler import *

from v1 import *

"""AdminHandler(관리자) """


class AdminHandler:
    def __init__(self):
        pass

    def get_score(self, data):
        """경기일 점수정보"""
        if not data:
            return jsonify({"data": {"games": []}})

        scores = adm.get_scores(data["playdate"])

        return jsonify({"data": {"games": scores}})

    def get_day_games(self, data):
        """경기리스트"""
        if not data:
            return jsonify({"data": {"games": []}})

        scores = adm.get_day_games(data["playdate"])

        return jsonify({"data": {"games": scores}})

    def put_score(self, data):
        """경기스코어 갱신"""
        if not data:
            return jsonify({"data": {"status": 0}})

        dbid = data["id"]
        awayscore = data["awayScore"]
        homescore = data["homeScore"]

        score = adm.put_score(
            {
                "dbid": dbid,
                "awayscore": awayscore,
                "homescore": homescore,
            }
        )

        return jsonify({"data": {"status": score["id"]}})

    def post_new_game(self, data):
        """경기등록"""
        if not data:
            return jsonify({"data": {"status": 0}})

        game = adm.post_new_game(data)

        return jsonify({"data": {"status": game["id"]}})

    def get_users(self, data):
        """사용자전체리스트"""
        if not data:
            return jsonify({"data": {"users": []}})

        users = adm.get_users(data)
        return jsonify({"data": {"users": users}})

    def get_user_records(self, data):
        """사용자기록리스트"""
        if not data:
            return False

        user_id = data["id"]
        records = adm.get_user_records({"user_id": user_id})

        return jsonify({"res": records})
