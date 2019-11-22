#!/usr/bin/python3
# -*-coding:utf-8 -*-

from flask import jsonify

from helper import utils
from helper import logger
from v1.statics import StaticsHanlder
from v1.teams import TeamsHandler
from v1.history import HistoryHandler
from v1.scores import ScoresHandler
from v1.users import UsersHandler

import datetime


""" Prooya Main Router """

_us = UsersHandler()
_sh = ScoresHandler()
_st = StaticsHanlder()
_te = TeamsHandler()
_hi = HistoryHandler()


class ApplicationException(Exception):

    def __init__(self, msg=''):
        self.msg = msg
        logger.save_log("app_prooya", "%s | %s" %
                        (datetime.datetime.now(), msg))

    def __str__(self):
        return self.msg

""" Prooya Meerkat Routing (from ver4) """


def ping():
    """ 서버 사용가능여부 검사"""
    ping = utils.check_ping()
    return jsonify({"res": ping})


def users(data, func):
    """ 사용자정보"""
    try:
        if func == "post":
            return _us.post_user(data)
        elif func == "del":
            return _us.del_user(data)
    except Exception as e:
        raise ApplicationException(str(e))


def score(data, func):
    """ 경기 스코어 정보"""
    try:
        if func == "get":
            return _sh.get_score(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


def statics(data):
    """ 통계데이터"""
    try:
        return _st.get_statics(data)
    except Exception as e:
        raise ApplicationException(str(e))


def teams(data, func):
    """ 팀별기록"""
    try:
        if func == "all":
            return _te.get_teams(data)
        elif func == "detail":
            return _te.get_details(data)
    except Exception as e:
        raise ApplicationException(str(e))


def history(data, func):
    """ 기록"""
    try:
        if func == "all":
            return _hi.get_history(data)
        elif func == "del":
            return _hi.del_history(data)
        elif func == "post":
            return _hi.post_history(data)
    except Exception as e:
        raise ApplicationException(str(e))


if __name__ == '__main__':
    pass
