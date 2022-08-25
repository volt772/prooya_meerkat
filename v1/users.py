#!/usr/bin/python3
# -*-coding:utf-8 -*-

from handler.record import RecordHandler
from handler.team import TeamHandler

from v1 import *

""" UsersHandler(사용자 처리) """


class UsersHandler:
    def __init__(self):
        self.HTEAM = TeamHandler()
        self.HRECORD = RecordHandler()

    def get_user(self, data):
        """사용자 정보"""
        if not data:
            return jsonify({"data": False})

        user_info = usm.get(pid=data["pid"])

        #: 사용자 FCM토큰 업데이트
        if user_info["id"]:
            fcm_res = usm.put(
                {
                    "col": "fcm_token",
                    "update": data["fcmToken"],
                    "where": user_info["id"],
                }
            )

        user_res = {"id": user_info["id"], "team": user_info["team"]}
        return jsonify({"data": user_res})

    def del_user(self, data):
        """사용자 정보 삭제"""
        if not data:
            return jsonify({"data": {"count": res}})

        res = False
        user = usm.get(pid=data["pid"])

        if user:
            res = usm.delete(user["id"])
            team_del = self.HTEAM.del_team({"id": user["id"], "del_all": True})

            record_del = self.HRECORD.del_record_all(user["id"])

        return jsonify({"data": {"count": res * 1}})

    def post_user(self, data):
        """사용자 신규등록 및 수정"""
        if not data:
            return jsonify({"data": False})

        res = {}
        user_id = usm.get(pid=data["pid"])

        if not user_id:
            user = usm.post(data)
            user_type = "new"
            user_id = user["id"]

            res = {"id": user_id, "team": data["team"]}
        else:
            user = usm.put(
                {"col": "team", "update": data["team"], "where": user_id["id"]}
            )
            user_type = "update"

            res = {"id": user_id["id"], "team": user_id["team"]}

        #: 기존사용자일 경우, 해당연도 기록,팀데이터 초기화
        year = utils.get_year()
        if user_type == "update":
            self.HTEAM.del_team({"id": user["id"], "year": year, "del_all": False})

            self.HRECORD.del_record({"pid": user["id"], "mode": "all", "year": year})

        #: 신규사용자일경우, 팀정보 초기화
        self.HTEAM.post_team({"id": user["id"], "year": year, "type": user_type})

        return jsonify({"data": res})
