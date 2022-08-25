# -*- coding: utf-8 -*-

import datetime
import http.client
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

API_KEY = "key=AAAA8XFs5fc:APA91bExsNQZrdzbY5e2zh_h_mpiO7Fe1iA8vxWHGHgZnIlJe7w92GdcSZiZ5Nh4QjiXJCboFurKf0okXo4HXoU3U_qTcfHlUXsNupycGoAyjGd14ssfa1DmGZZMtjdSpSEHYkpcuniR"

TEAMCODE = {
    "KIA": "kat",
    "두산": "dsb",
    "NC": "ncd",
    "롯데": "ltg",
    "SK": "skw",
    "LG": "lgt",
    "키움": "kwh",
    "삼성": "ssl",
    "한화": "hhe",
    "KT": "ktw",
}

year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")
date = year + month + day  # "20130615"

con = connect(dbname="prooya", user="prooya", host="localhost", password="CjsdksgkA77@")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


def get_fcm_list(acode, hcode):
    """FCM리스트 조회"""
    fcm_list = []
    query = """SELECT id, pid, fcm_token
         FROM users
         WHERE team='{0}' or team='{1}'""".format(
        acode, hcode
    )

    cur = con.cursor()
    cur.execute(query)

    fcms = cur.fetchall()

    if len(fcms) > 0:
        for k, v in enumerate(fcms):
            tokens = v[2]

            if tokens:
                fcm_list.append(tokens)

    return fcm_list


def fcm_send(acode, ascore, hcode, hscore):
    """FCM발송"""
    if not acode or not hcode:
        return False

    send_list = get_fcm_list(acode, hcode)

    if len(send_list) > 0:
        for fcm_to in send_list:
            try:
                fdata = {
                    "to": fcm_to,
                    "priority": "high",
                    "data": {
                        "title": "오늘 경기결과가 저장되었습니다.",
                        "pdate": "{0}월{1}일".format(month, day),
                        "acode": acode,
                        "hcode": hcode,
                        "ascore": ascore,
                        "hscore": hscore,
                    },
                }

                headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

                conn = http.client.HTTPConnection("fcm.googleapis.com", timeout=3)
                conn.request(
                    "POST",
                    "/fcm/send",
                    json.dumps(fdata, ensure_ascii=False).encode("utf-8"),
                    headers,
                )
                conn.close()
            except Exception as e:
                print("ex : ", e)
                pass


def update_data(ateam, ascore, hteam, hscore):
    """DB점수업데이트"""
    try:
        query = """UPDATE scores
                SET awayscore={0}, homescore={1}
                WHERE awayteam='{2}' AND hometeam='{3}' AND playdate={4}
                AND awayscore = 997 AND homescore = 997""".format(
            ascore, hscore, ateam, hteam, date
        )

        cur = con.cursor()
        cur.execute(query)
        cur.close()

        fcm_send(ateam, ascore, hteam, hscore)
        print("{0} || update_data".format(datetime.datetime.now()))
    except Exception as e:
        print("{0} || update_data_err : {1}".format(datetime.datetime.now(), str(e)))


def select_data():
    """DB점수데이터가져오기"""
    games_arr = {}
    query = """SELECT id, awayteam, awayscore, hometeam, homescore
            FROM scores
            WHERE playdate='{0}'""".format(
        date
    )

    cur = con.cursor()
    cur.execute(query)

    games = cur.fetchall()

    if len(games) > 0:
        for k, v in enumerate(games):
            ateam = v[1]
            ascore = v[2]
            hteam = v[3]
            hscore = v[4]

            games_arr.update({ateam: ascore})
            games_arr.update({hteam: hscore})

    cur.close()
    return games_arr


def check_game_allfinished(games):
    """게임전체종료여부 확인"""
    is_finished = True

    for _team, _score in games.items():
        if _score == 997:
            is_finished = False
            break

    return is_finished


def get_reg_score(score_tag):
    """게임스코어가져오기(정규식 파싱)"""
    pattern = re.compile(
        "<\/?\w+\s*[^>]*?\/?>", re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE
    )
    score = pattern.sub(" ", str(score_tag)).strip()

    return score


def crawl_games():
    """점수데이터 크롤링"""
    games_arr = select_data()
    print("{0} || games_arr : {1}".format(datetime.datetime.now(), games_arr))

    if games_arr:
        all_finished = check_game_allfinished(games_arr)
        print("{0} || all_finished : {1}".format(datetime.datetime.now(), all_finished))

        if not all_finished:
            url = "http://sports.news.naver.com/schedule/scoreBoard.nhn?date=" + date
            html = urllib.request.urlopen(url).read()

            soup = BeautifulSoup(html, "lxml")
            game_list = soup.find("ul", id="todaySchedule")
            games = game_list.find_all("li")

            p = re.compile(r"<.*?>")

            for game in games:
                #: 게임종료확인
                game_finished = False
                game_status = game.find("div", class_="vs_cnt").find(class_="state")

                if "종료" in str(game_status):
                    game_finished = True

                if game_finished:
                    #: 원정팀
                    away_team = (
                        game.find("div", class_="vs_lft")
                        .find(class_="vs_team")
                        .strong.string
                    )
                    away_score_tag = game.find("div", class_="vs_lft").find(
                        class_="vs_num"
                    )
                    ascore = get_reg_score(away_score_tag)

                    #: 홈팀
                    home_team = (
                        game.find("div", class_="vs_rgt")
                        .find(class_="vs_team")
                        .strong.string
                    )
                    home_score_tag = game.find("div", class_="vs_rgt").find(
                        class_="vs_num"
                    )
                    hscore = get_reg_score(home_score_tag)

                    acode = TEAMCODE[away_team.upper()]
                    hcode = TEAMCODE[home_team.upper()]

                    if games_arr[acode] == 997 and games_arr[hcode] == 997:
                        update_data(acode, ascore, hcode, hscore)
                    else:
                        continue
                else:
                    continue


if __name__ == "__main__":
    crawl_games()
    # fcm_send("dsb", 2, "kat", 5)
