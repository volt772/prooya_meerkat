#!/usr/bin/python3
# -*-coding:utf-8 -*-

from flask import jsonify
from helper import utils, datum

from model.statics import StaticsModel
from model.record import RecordModel
from model.team import TeamModel
from model.history import HistoryModel
from model.score import ScoreModel
from model.user import UserModel
from model.admin import AdminModel

# Model Variable
stm = StaticsModel()
rcm = RecordModel()
tem = TeamModel()
him = HistoryModel()
scm = ScoreModel()
usm = UserModel()
adm = AdminModel()
