#!/usr/bin/python3
# -*-coding:utf-8 -*-

from handler import *

"""AdminHandler(관리자) """


class AdminHandler:
    def __init__(self):
        pass

    def get_score(self, data):
        """경기일 점수정보"""
        if not data:
            return False

        scores = MADMIN.get_scores(data["playdate"])

        return jsonify({"res": scores})

    def put_score(self, data):
        """경기스코어 갱신"""
        if not data:
            return False

        dbid = data["id"]
        awayscore = data["awayScore"]
        homescore = data["homeScore"]

        score = MADMIN.put_score(
            {
                "dbid": dbid,
                "awayscore": awayscore,
                "homescore": homescore,
            }
        )

        return jsonify({"res": score})

    def get_users(self, data):
        """사용자전체리스트"""
        if not data:
            return False

        users = MADMIN.get_users(data)
        return jsonify({"res": users})

    def get_user_records(self, data):
        """사용자기록리스트"""
        if not data:
            return False

        user_id = data["id"]
        records = MADMIN.get_user_records({"user_id": user_id})

        return jsonify({"res": records})
