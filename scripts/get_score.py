#!/usr/bin/python
# -*-coding:utf-8-*-

import json
import os
import pprint
import re

import requests
from bs4 import BeautifulSoup


def get_table_data(url):
    """1차테이블정보"""
    response = requests.get(url)
    res = response.text

    soup = BeautifulSoup(res, "lxml")

    table_div = soup.find(id="calendarWrap")
    tables = table_div.find_all("table")

    for i in tables:
        _awayteam = i.find_all("span", class_="team_lft")
        _hometeam = i.find_all("span", class_="team_rgt")
        # _allscore = i.find_all("strong", class_="td_score")
        _date = i.find_all("span", class_="td_date")

        #: 예외일 (cf, 올스타전)
        if "7.15" in str(_date[0]):
            continue

        # if _awayteam and _hometeam and _allscore:
        if _awayteam and _hometeam:
            get_readable_data(
                data={
                    "awayteam": _awayteam,
                    "hometeam": _hometeam,
                    "allscore": 0,
                    "date": _date,
                }
            )
        else:
            continue


def get_readable_data(data):
    """파일로저장"""
    awayteam = data["awayteam"]
    hometeam = data["hometeam"]
    allscore = data["allscore"]
    date = data["date"]

    play_result = {}
    date = re.sub("<.+?>", "", str(date[0]), 0, re.I | re.S).split(" ")[0]
    play_result[date] = {}

    for i in range(0, len(awayteam)):
        play_result[date][i] = {
            "awayteam": re.sub("<.+?>", "", str(awayteam[i]), 0, re.I | re.S),
            "awayscore": "",
            "hometeam": re.sub("<.+?>", "", str(hometeam[i]), 0, re.I | re.S),
            "homescore": "",
        }

        # 		score_data = re.sub('<.+?>', '', str(allscore[i]), 0, re.I|re.S)
        # 		score_arr = score_data.split(":")
        #
        # 		if score_arr[0] == "VS":
        # 			ascore = hscore = 999
        # 		else:
        # 			ascore = score_arr[0]
        # 			hscore = score_arr[1]
        #
        # 	play_result[date][i]["awayscore"] = ascore
        # 	play_result[date][i]["homescore"] = hscore
        play_result[date][i]["awayscore"] = 998
        play_result[date][i]["homescore"] = 998

    filename = "2018" + str(date[0]).split(".")[0].zfill(2)
    dict_json = json.dumps(play_result, ensure_ascii=False)
    f = open(filename, "a")
    f.write(dict_json + "\n")
    f.close()


if __name__ == "__main__":
    for i in range(3, 12):
        print(i)
        get_table_data(
            "http://sports.news.naver.com/kbaseball/schedule/index.nhn?month={0}&year=2018".format(
                str(i).zfill(2)
            )
        )
