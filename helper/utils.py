#!/usr/bin/python3
# -*-coding:utf-8 -*-

import datetime
import os


def get_host():
    f = open("%s/app_flag" % (os.getcwd()), "r")
    content = f.read().strip()

    host = "te"
    if "product" in content:
        host = "pr"

    return host


def check_ping():
    return True


def get_current_date():
    """현재일 계산"""
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    return today


def get_year():
    """연도 계산
    익년도 3월이전은 전년도로 계산
    ex) 2018년 2월 > 2017년
        2018년 3월 > 2018년
        2017년 10월 > 2017년
    """
    now_date = str(datetime.datetime.now().year) + str(datetime.datetime.now().month)
    next_date = str(datetime.datetime.now().year + 1) + "03"

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    if month < 3:
        year = int(now_date[0:4]) - 1
    else:
        if int(now_date) < int(next_date):
            year = now_date[0:4]

    return int(year)


def convert_timedata(data):
    """시간형식변환"""
    if not data:
        return False

    new_time = ""
    _time = data["time"]
    _type = data["type"]

    if _type == 1:
        time_format = "%Y-%m-%d %H:%M:%S"
    elif _type == 2:
        time_format = "%Y-%m-%d"
    elif _type == 3:
        time_format = "%Y%m%d"

    new_time = _time.strftime(time_format)

    return new_time


def check_play_result(data, favteam):
    """경기승패유무확인"""
    awayteam = {"score": data["awayscore"], "team": data["awayteam"], "my": False}
    hometeam = {"score": data["homescore"], "team": data["hometeam"], "my": False}

    if awayteam["team"] == favteam:
        awayteam["my"] = True
    elif hometeam["team"] == favteam:
        hometeam["my"] = True

    winteam = ""
    if awayteam["score"] > hometeam["score"]:
        winteam = "away"
    elif awayteam["score"] < hometeam["score"]:
        winteam = "home"
    else:
        winteam = "draw"

    playresult = "l"
    if winteam == "away":
        if awayteam["my"]:
            playresult = "w"
    elif winteam == "home":
        if hometeam["my"]:
            playresult = "w"
    else:
        playresult = "d"

    return playresult


def reorder_analystic_data(data):
    """전적 정렬"""
    if not data:
        return ""

    plays = []
    for k, v in list(data.items()):
        play_arr = v.split("-")
        plays.append(
            {"team": k, "win": play_arr[0], "lose": play_arr[1], "draw": play_arr[2]}
        )

    return plays


def reorder_teamdata(data):
    """전적 재계산"""
    if not data:
        return False

    p_data = data["p_data"]
    d_data = data["d_data"]
    mode = data["mode"]

    versus = d_data[p_data["versus"]].split("-")

    if mode == "plus":
        if p_data["result"] == "w":
            versus[0] = str(int(versus[0]) + 1)
        elif p_data["result"] == "l":
            versus[1] = str(int(versus[1]) + 1)
        elif p_data["result"] == "d":
            versus[2] = str(int(versus[2]) + 1)
    elif mode == "minus":
        if p_data["result"] == "w":
            versus[0] = str(check_zero_score(int(versus[0]) - 1))
        elif p_data["result"] == "l":
            versus[1] = str(check_zero_score(int(versus[1]) - 1))
        elif p_data["result"] == "d":
            versus[2] = str(check_zero_score(int(versus[2]) - 1))

    new_record = "-".join(versus)
    return new_record


def check_zero_score(score):
    """음수 점수 예외처리"""
    return 0 if score < 0 else score


if __name__ == "__main__":
    get_host()
