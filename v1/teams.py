#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v1 import *

""" TeamsHandler(팀별기록) """


class TeamsHandler:
    def __init__(self):
        pass

    def get_teams(self, data):
        """팀별 기록 데이터"""
        if not data:
            return jsonify({"data": False})

        # 승무패
        pt_win = 0  #: 승
        pt_lose = 0  #: 패
        pt_draw = 0  #: 무

        email = data.get("email")
        year = data.get("year")

        teams = tem.get_teams_all({"email": email, "year": year})

        reorderd_data = utils.reorder_analystic_data(teams)

        team_list = []
        for team, analystic in enumerate(reorderd_data):
            team_single_data = {
                "year": year,
                "team": analystic["team"],
                "win": int(analystic["win"]),
                "lose": int(analystic["lose"]),
                "draw": int(analystic["draw"]),
                "rate": int(self.get_winning_rate(analystic)),
            }

            pt_win += int(analystic["win"])
            pt_lose += int(analystic["lose"])
            pt_draw += int(analystic["draw"])

            team_list.append(team_single_data)

        res = {
            "teams": team_list,
            "summary": {"win": pt_win, "lose": pt_lose, "draw": pt_draw, "year": year},
        }

        return jsonify({"data": res})

    def get_details(self, data):
        """팀별 상세정보"""
        if not data:
            return jsonify({"data": {"games": []}})

        records = tem.get_details(
            {"email": data["email"], "versus": data["versus"], "year": data["year"]}
        )

        record_list = []
        if records:
            for idx, record in enumerate(records):
                score = scm.getAll(
                    {
                        "playdate": utils.convert_timedata(
                            {"time": record["regdate"], "type": 3}
                        ),
                        "favteam": record["team"],
                    }
                )

                score_data = datum.get_score_data(score, record)

                if score_data:
                    record_single_data = {
                        "playResult": record["result"],
                        "playVs": record["versus"],
                        "playDate": score_data["playdate"],
                        "awayTeam": score_data["awayteam"],
                        "awayScore": score_data["awayscore"],
                        "homeTeam": score_data["hometeam"],
                        "homeScore": score_data["homescore"],
                        "stadium": score_data["stadium"],
                    }

                    record_list.append(record_single_data)

        return jsonify({"data": {"games": record_list}})

    def get_winning_rate(self, data):
        """팀별 승률 계산"""
        winning_rate = 0
        play_count = int(data["win"]) + int(data["draw"]) + int(data["lose"])

        if play_count > 0:
            try:
                winning_rate = int(data["win"]) / play_count
            except ZeroDivisionError as e:
                winning_rate = 0

        return str(round(winning_rate * 100))

    def put_team(self, data):
        """팀 정보 수정"""
        if not data:
            return jsonify({"data": False})

        team = tem.put(data)

        return jsonify({"data": team})
