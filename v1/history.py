#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v1 import *
from v1.teams import TeamsHandler

""" HistoryHandler(전체기록) """


class HistoryHandler:
    def __init__(self):
        self.HTEAMS = TeamsHandler()

    def get_history(self, data, args):
        """전체 데이터"""
        if not data:
            return jsonify({"games": []})

        email = data.get("email")
        year = data.get("year", 0)

        histories = []

        history = him.get_history({"email": email, "year": year}, args)

        if not history:
            return jsonify({"games": []})

        for play in history:
            score = scm.getAll(
                {
                    "playdate": utils.convert_timedata(
                        {"time": play["regdate"], "type": 3}
                    ),
                    "favteam": play["myteam"],
                }
            )

            score_data = datum.get_score_data(score, play)

            if score_data:
                histories.append(
                    {
                        "playId": play["id"],
                        "playResult": play["result"],
                        "playVs": play["versus"],
                        "playSeason": play["year"],
                        "playDate": score_data["playdate"],
                        "awayTeam": score_data["awayteam"],
                        "awayScore": score_data["awayscore"],
                        "homeTeam": score_data["hometeam"],
                        "homeScore": score_data["homescore"],
                        "stadium": score_data["stadium"],
                    }
                )

        return jsonify({"games": histories})

    def del_history(self, data):
        """기록삭제(선택)"""
        if not data:
            return jsonify({"data": {"count": 0}})

        res = him.del_history(
            {"rid": data["rid"], "mode": "single", "year": data["year"]}
        )

        self.update_history(data, "minus")

        return jsonify({"data": {"count": res * 1}})

    def update_history(self, data, kind):
        """기록수정(선택)"""
        record_res = False

        year = int(data.get("year"))
        team = tem.get({"pid": data["pid"], "year": year})

        if not team:
            return False

        user_pid = team["pid"]
        new_record = utils.reorder_teamdata(
            {"p_data": data, "d_data": team, "mode": kind}
        )

        if new_record:
            self.HTEAMS.put_team(
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

    def post_history(self, data):
        """기록추가"""
        if not data:
            return jsonify({"data": {"result": 0}})

        res = self.put_history(data, "plus")
        return jsonify({"data": {"result": res}})

    def put_team(self, data):
        """팀 정보 수정"""
        if not data:
            return jsonify({"data": False})

        team = tem.put(data)

        return jsonify({"data": team})

    def put_history(self, data, kind):
        """기록수정(선택)"""
        record_res = False

        year = int(data.get("year"))
        team = him.get_team_static({"pid": data["pid"], "year": year})

        if not team:
            return False

        user_pid = team["pid"]
        new_record = utils.reorder_teamdata(
            {"p_data": data, "d_data": team, "mode": kind}
        )

        if new_record:
            self.put_team(
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
                record_res = him.post(data)
            else:
                record_res = "deleted"
        else:
            return False

        return record_res
