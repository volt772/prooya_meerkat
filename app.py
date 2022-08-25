#!/usr/bin/python3
# -*-coding:utf-8 -*-

import datetime

from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer
from werkzeug.contrib.fixers import ProxyFix

from handler.admin import AdminHandler
from handler.record import RecordHandler
from handler.score import ScoreHandler
from handler.team import TeamHandler
from handler.user import UserHandler
from helper import config, logger, utils
from v1 import meerkat

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


""" Prooya Main Router """


class ApplicationException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        logger.save_log("app_prooya", "%s | %s" % (datetime.datetime.now(), msg))

    def __str__(self):
        return self.msg


""" Prooya New Routing Temp (from ver4) """


@app.route("/prooya/v1/ping", methods=["POST"])
def ping():
    """서버 사용가능여부 검사"""
    return meerkat.ping()


@app.route("/prooya/v1/admin/<func>", methods=["POST"])
def admin(func):
    """관리자정보"""
    return meerkat.admin(request.get_json(silent=True), func, request.args)


@app.route("/prooya/v1/users/<func>", methods=["POST"])
def users(func):
    """사용자정보"""
    return meerkat.users(request.get_json(silent=True), func)


@app.route("/prooya/v1/scores/<func>", methods=["POST"])
def score(func):
    """경기 스코어 정보"""
    return meerkat.score(request.get_json(silent=True), func)


@app.route("/prooya/v1/statics", methods=["POST"])
def statics():
    """통계데이터"""
    return meerkat.statics(request.get_json(silent=True))


@app.route("/prooya/v1/teams/<func>", methods=["POST"])
def teams(func):
    """팀별기록"""
    return meerkat.teams(request.get_json(silent=True), func)


@app.route("/prooya/v1/histories/<func>", methods=["POST"])
def history(func):
    """기록"""
    return meerkat.history(request.get_json(silent=True), func, request.args)


""" Prooya Old Routing (until ver3) """


@app.route("/app/ping", methods=["POST"])
def check_ping():
    """서버 사용가능여부 검사"""
    ping = utils.check_ping()
    return jsonify({"res": ping})


@app.route("/user/<func>", methods=["POST"])
def user_handler(func):
    """Route for user"""
    data = request.get_json(silent=True)
    try:
        _user = UserHandler()
        if func == "getuser":
            return _user.get_user(data)
        elif func == "deluser":
            return _user.del_user(data)
        elif func == "postuser":
            return _user.post_user(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


@app.route("/team/<func>", methods=["POST"])
def team_handler(func):
    """Route for team"""
    data = request.get_json(silent=True)
    try:
        _team = TeamHandler()
        if func == "getteam":
            return _team.get_team(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


@app.route("/record/<func>", methods=["POST"])
def record_handler(func):
    """Route for record"""
    data = request.get_json(silent=True)
    try:
        _record = RecordHandler()
        if func == "getrecord":
            return _record.get_record(data)
        elif func == "delrecord":
            return _record.del_record(data)
        elif func == "postrecord":
            return _record.post_record(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


@app.route("/score/<func>", methods=["POST"])
def score_handler(func):
    """Route for score"""
    data = request.get_json(silent=True)
    try:
        _score = ScoreHandler()
        if func == "getscore":
            return _score.get_score(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


@app.route("/admin/<func>", methods=["POST"])
def adm_handler(func):
    """Route for admin"""
    data = request.get_json(silent=True)
    try:
        _admin = AdminHandler()
        if func == "getscore":
            return _admin.get_score(data)
        elif func == "putscore":
            return _admin.put_score(data)
        elif func == "getusers":
            return _admin.get_users(data)
        elif func == "getrecords":
            return _admin.get_user_records(data)
        else:
            return jsonify({"res": False})
    except Exception as e:
        raise ApplicationException(str(e))


if __name__ == "__main__":
    app_info = config.get_config("app_%s" % (utils.get_host()))

    host = app_info["app_host"]
    port = app_info["app_port"]
    debug = app_info["app_debug"]

    http_server = WSGIServer((host, int(port)), app)
    http_server.serve_forever()
