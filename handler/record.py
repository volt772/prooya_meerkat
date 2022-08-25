#!/usr/bin/python3
# -*-coding:utf-8 -*-

from helper import datum

from handler import *
from handler.team import TeamHandler

""" RecordHandler(사용자 기록 정보 처리) """


class RecordHandler:
    def __init__(self):
        self.HTEAM = TeamHandler()

    def get_record(self, data):
        """기록정보(해당연도)"""
        if not data:
            return jsonify({"res": False})

        year = utils.get_year()
        records = MRECORD.get_all(
            {"pid": data["pid"], "versus": data["versus"], "year": year}
        )

        if records:
            for idx, record in enumerate(records):
                records[idx]["regdate"] = utils.convert_timedata(
                    {"time": records[idx]["regdate"], "type": 2}
                )

        return jsonify({"res": records})

    def del_record_all(self, pid):
        """기록삭제(전체)"""
        if not pid:
            return jsonify({"res": False})

        res = MRECORD.delete_all(pid)

        return jsonify({"res": res})

    def del_record(self, data):
        """기록삭제(선택)"""
        if not data:
            return jsonify({"res": False})

        if "mode" in data:
            if data["mode"] == "all":
                res = MRECORD.delete(data)
        else:
            res = MRECORD.delete(
                {"rid": data["rid"], "mode": "single", "year": data["year"]}
            )

            self.put_record(data, "minus")

        return jsonify({"res": res})

    def post_record(self, data):
        """기록추가"""
        if not data:
            return jsonify({"res": False})

        res = self.put_record(data, "plus")
        return jsonify({"res": res})

    def put_record(self, data, kind):
        """기록수정(선택)"""
        record_res = False

        year = int(data.get("year"))
        team = MTEAM.get({"pid": data["pid"], "year": year})

        if not team:
            return False

        user_pid = team["pid"]
        new_record = utils.reorder_teamdata(
            {"p_data": data, "d_data": team, "mode": kind}
        )

        if new_record:
            self.HTEAM.put_team(
                {
                    "pid": user_pid,
                    "year": year,
                    "anonym_team": data["versus"],
                    "anonym_res": new_record,
                }
            )

            if kind == "plus":
                data["pid"] = user_pid
                data["year"] = year
                record_res = MRECORD.post(data)
            else:
                record_res = "deleted"
        else:
            return False

        return record_res
