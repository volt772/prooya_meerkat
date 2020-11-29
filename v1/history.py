#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v1 import *

from v1.teams import TeamsHandler

""" HistoryHandler(전체기록) """


class HistoryHandler:

    def __init__(self):
        self.HTEAMS = TeamsHandler()

    def get_history(self, data):
        """ 전체 데이터"""
        if not data:
            return jsonify({"data": {"games": []}})

        email = data.get("email")
        year = data.get("year")

        histories = []

        history = him.get_history({"email": email, "year": year})

        if not history:
            return jsonify({"data": {"games": []}})

        for idx, play in enumerate(history):
            score = scm.get({
                "playdate": utils.convert_timedata({"time": play["regdate"], "type": 3}),
                "favteam": play["myteam"]
            })

            if score:
                histories.append({
                    "playId": play["id"],
                    "playResult": play["result"],
                    "playVs": play["versus"],
                    "playSeason": play["year"],
                    "playDate": score["playdate"],
                    "awayTeam": score["awayteam"],
                    "awayScore": score["awayscore"],
                    "homeTeam": score["hometeam"],
                    "homeScore": score["homescore"],
                    "stadium": score["stadium"]
                })

        return jsonify({"data": {"games" : histories}})

    def del_history(self, data):
        """ 기록삭제(선택)"""
        if not data:
            return jsonify({"data": {"count" : res * 1}})

        res = him.del_history({
            "rid": data["rid"],
            "mode": "single",
            "year": data["year"]})

        self.update_history(data, "minus")

        return jsonify({"data": {"count" : res * 1}})

    def update_history(self, data, kind):
        """ 기록수정(선택)"""
        record_res = False

        year = int(data.get("year"))
        team = tem.get({
            "pid": data["pid"],
            "year": year})

        if not team:
            return False

        user_pid = team["pid"]
        new_record = utils.reorder_teamdata({
            "p_data": data,
            "d_data": team,
            "mode": kind})

        if new_record:
            self.HTEAMS.put_team({
                "pid": user_pid,
                "year": year,
                "anonym_team": data["versus"],
                "anonym_res": new_record})

            if kind == "plus":
                data["pid"] = user_pid
                data["year"] = year
                record_res = MRECORD.post(data)
            else:
                record_res = "deleted"
        else:
            return False

        return record_res

    def post_history(self, data):
        """ 기록추가"""
        if not data:
            return jsonify({"data": {"result" : 0}})

        res = self.put_history(data, "plus")
        return jsonify({"data": {"result" : res}})

    def put_team(self, data):
        """ 팀 정보 수정"""
        if not data:
            return jsonify({"data": False})

        team = tem.put(data)

        return jsonify({"data": team})

    def put_history(self, data, kind):
        """ 기록수정(선택)"""
        record_res = False

        year = int(data.get("year"))
        team = him.get_team_static({
            "pid": data["pid"],
            "year": year})

        if not team:
            return False

        user_pid = team["pid"]
        new_record = utils.reorder_teamdata({
            "p_data": data,
            "d_data": team,
            "mode": kind})

        if new_record:
            self.put_team({
                "pid": user_pid,
                "year": year,
                "anonym_team": data["versus"],
                "anonym_res": new_record})

            if kind == "plus":
                data["pid"] = user_pid
                data["year"] = year
                record_res = him.post(data)
            else:
                record_res = "deleted"
        else:
            return False

        return record_res
