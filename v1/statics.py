#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v1 import *

""" StaticsHanlder(통계정보) """


class StaticsHanlder:

    def __init__(self):
        pass

    def get_statics(self, data):
        """ 기록정보(Dashboard용 통합 데이터)"""
        if not data:
            return jsonify({"res": False})

        # 경기수
        play_count_all = 0      #: 통산
        play_count_season = 0   #: 시즌

        # 승률
        winning_rate_all = 0        #: 통산
        winning_rate_season = 0     #: 시즌

        # 승무패
        pt_win_season = 0   #: 승(시즌)
        pt_lose_season = 0  #: 패(시즌)
        pt_draw_season = 0  #: 무(시즌)

        # 승무패
        pt_win_all = 0      #: 승(통산)
        pt_lose_all = 0     #: 패(통산)
        pt_draw_all = 0     #: 무(통산)

        # 최근 5경기
        recents = []

        email = data.get("email")
        season_year = utils.get_year()

        records = stm.get_records({"email": email})

        if records:
            for idx, record in enumerate(records):
                # 경기결과 카운트
                if record["result"] is "w":
                    pt_win_all += 1
                    if record["year"] == season_year:
                        pt_win_season += 1
                        play_count_season += 1
                elif record["result"] is "l":
                    pt_lose_all += 1
                    if record["year"] == season_year:
                        pt_lose_season += 1
                        play_count_season += 1
                elif record["result"] is "d":
                    pt_draw_all += 1
                    if record["year"] == season_year:
                        pt_draw_season += 1
                        play_count_season += 1

                is_season_play = True if records[idx]["year"] == season_year else False
                if idx < 5 and is_season_play:
                    recents.append({
                        "playId" : records[idx]["id"],
                        "ptGet" : records[idx]["getscore"],
                        "ptLost" : records[idx]["lostscore"],
                        "playDate" : utils.convert_timedata({
                            "time": records[idx]["regdate"],
                            "type": 3}),
                        "playResult" : records[idx]["result"],
                        "playVs" : records[idx]["versus"],
                        "playMyTeam" : records[idx]["myteam"],
                        "playSeason" : records[idx]["year"],
                    })

        # 전체 경기수
        play_count_all = len(records)

        try:
            winning_rate_season = pt_win_season / play_count_season
        except ZeroDivisionError as e:
            winning_rate_season = 0

        # 승률
        winning_rate_all = pt_win_all / play_count_all

        res = {
            "allStatics" : {
                "win" : pt_win_all,
                "lose" : pt_lose_all,
                "draw" : pt_draw_all,
                "count" : play_count_all,
                "rate" : round(winning_rate_all * 100)
            },
            "seasonStatics" : {
                "win" : pt_win_season,
                "lose" : pt_lose_season,
                "draw" : pt_draw_season,
                "count" : play_count_season,
                "rate" : round(winning_rate_season * 100)
            },
            "recentPlays" : recents
        }

        return jsonify({"res": res})