#!/usr/bin/python3
# -*-coding:utf-8 -*-

from flask import jsonify
from helper import datum, utils
from model.admin import AdminModel
from model.history import HistoryModel
from model.record import RecordModel
from model.score import ScoreModel
from model.statics import StaticsModel
from model.team import TeamModel
from model.user import UserModel

# Model Variable
stm = StaticsModel()
rcm = RecordModel()
tem = TeamModel()
him = HistoryModel()
scm = ScoreModel()
usm = UserModel()
adm = AdminModel()
