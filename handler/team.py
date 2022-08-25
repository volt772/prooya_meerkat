#!/usr/bin/python3
# -*-coding:utf-8 -*-

from handler import *

""" TeamHandler(사용자 팀 정보 처리) """


class TeamHandler:
    def __init__(self):
        pass

    def get_team(self, data):
        """팀 정보"""
        if not data:
            return jsonify({"res": False})

        year = utils.get_year()
        team = MTEAM.get({"pid": data["pid"], "year": year})

        if team:
            team["regdate"] = utils.convert_timedata(
                {"time": team["regdate"], "type": 1}
            )

            record = MRECORD.get_recent({"pid": data["pid"], "year": year})

            if record:
                record["regdate"] = utils.convert_timedata(
                    {"time": record["regdate"], "type": 1}
                )

                team["recent_regdate"] = record["regdate"]
                team["recent_versus"] = record["versus"]
                team["recent_result"] = record["result"]

        return jsonify({"res": team})

    def del_team(self, data):
        """팀 정보삭제"""
        if not data:
            return jsonify({"res": False})

        team = MTEAM.delete(data)

        return jsonify({"res": team})

    def post_team(self, data):
        """팀 정보 신규등록"""
        if not data:
            return jsonify({"res": False})

        team = MTEAM.get_team(data)

        if not team:
            MTEAM.post(data)
        else:
            self.put_team(self, data)

        return jsonify({"res": team})

    def put_team(self, data):
        """팀 정보 수정"""
        if not data:
            return jsonify({"res": False})

        team = MTEAM.put(data)

        return jsonify({"res": team})
