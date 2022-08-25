#!/usr/bin/python3
# -*-coding:utf-8 -*-

from collections import defaultdict

from v1 import *

""" StaticsHanlder(통계정보) """


class StaticsHanlder:
    def __init__(self):
        pass

    def get_statics(self, data):
        """기록정보(Dashboard용 통합 데이터)"""
        if not data:
            return jsonify({"data": False})

        # 사용자정보
        user = {}

        # 경기수
        play_count_all = 0  #: 통산

        # 승률
        winning_rate_all = 0  #: 통산
        winning_rate_season = 0  #: 시즌

        # 승무패
        pt_win_all = 0  #: 승(통산)
        pt_lose_all = 0  #: 패(통산)
        pt_draw_all = 0  #: 무(통산)

        # 최근 5경기
        recents = []

        # 팀별통산승률
        team_winning_rate = dict.fromkeys(
            ["kat", "dsb", "ltg", "ncd", "skw", "kwh", "lgt", "hhe", "ssl", "ktw"], 0
        )

        email = data.get("email")

        records = stm.get_records({"email": email})

        if records:
            # 사용자
            user = {"user_id": records[0]["id"], "team": records[0]["team"]}

            if user:
                # 사용자 팀별 통산기록(승률)
                user_all_records = tem.get_all(user["user_id"])

                team_dict = defaultdict(set)

                for _record in user_all_records:
                    for k, v in _record.items():
                        team_dict[k].add(v)

                for _team, _record in team_dict.items():
                    win = 0
                    lose = 0
                    for v in _record:
                        _pa = v.split("-")
                        try:
                            win += int(_pa[0])
                            lose += int(_pa[1])
                            rate = (win / (win + lose)) * 100
                        except ZeroDivisionError:
                            rate = 0
                        finally:
                            team_winning_rate[_team] = round(rate)

            for idx, record in enumerate(records):
                # 경기결과 카운트
                if record["result"] is "w":
                    pt_win_all += 1
                elif record["result"] is "l":
                    pt_lose_all += 1
                elif record["result"] is "d":
                    pt_draw_all += 1

        # 전체 경기수
        play_count_all = len(records)

        # 승률
        winning_rate_all = pt_win_all / play_count_all

        res = {
            "user": user,
            "allStatics": {
                "win": pt_win_all,
                "lose": pt_lose_all,
                "draw": pt_draw_all,
                "count": play_count_all,
                "rate": round(winning_rate_all * 100),
            },
            "teamWinningRate": team_winning_rate,
        }

        return jsonify({"data": res})
