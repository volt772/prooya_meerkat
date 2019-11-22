#!/usr/bin/python3
# -*-coding:utf-8 -*-

import json
import ast

def get_summary(team):
    """ 팀승률데이터"""
    record = team.split("-")
    win = int(record[0])
    draw = int(record[2])
    lose = int(record[1])
    all_play = win + draw + lose
    rate = 0

    try:
        rate = win / (all_play - draw)
    except ZeroDivisionError:
        pass

    return {"win" : win, "draw" : draw, "lose" : lose, "rate" : int(rate * 100)}


def make_all_records(udata):
    """ 기록정보(Dashboard용 통합 데이터 정리)"""
    records = udata.get("records", [])
    teams = udata.get("teams", "")
    year = udata.get("year", 2019)
    play_today = udata.get("play_today", {})

    res = {}

    # 시즌연도
    season_year = year

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

    # 전체경기 리스트
    plays_all = []

    # 상대경기 리스트
    teams_all = []

    # 팀기록데이터
    if (len(teams) > 0):
        for idx, team in enumerate(teams):
            year_record = {}

            for key, item in list(team.items()):
                if key != "year":
                    summary = get_summary(team[key])

                    year_record = {
                        "team" : key,
                        "year" : team["year"],
                        "win" : summary["win"],
                        "draw" : summary["draw"],
                        "lose" : summary["lose"],
                        "rate" : summary["rate"]
                    }

                    teams_all.append(year_record)

    if (len(records) > 0):
        for idx, record in enumerate(records):
            plays_all.append(record)
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


        play_count_all = len(records)

        try:
            winning_rate_season = pt_win_season / play_count_season
        except ZeroDivisionError as e:
            winning_rate_season = 0

        winning_rate_all = pt_win_all / play_count_all

    res = {
        "all" : {
            "pt_win" : pt_win_all,
            "pt_lose" : pt_lose_all,
            "pt_draw" : pt_draw_all,
            "play_count" : play_count_all,
            "winning_rate" : round(winning_rate_all * 100)
        },
        "season" : {
            "pt_win" : pt_win_season,
            "pt_lose" : pt_lose_season,
            "pt_draw" : pt_draw_season,
            "play_count" : play_count_season,
            "winning_rate" : round(winning_rate_season * 100)
        },
        "playsAll" : plays_all,
        "teamsAll" : teams_all,
        "playToday" : play_today,
    }

    return res