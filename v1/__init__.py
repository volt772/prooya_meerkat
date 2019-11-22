#!/usr/bin/python3
# -*-coding:utf-8 -*-

from flask import jsonify
from helper import utils

from model.statics import StaticsModel
from model.team import TeamModel
from model.history import HistoryModel
from model.score import ScoreModel
from model.user import UserModel

# Model Variable
stm = StaticsModel()
tem = TeamModel()
him = HistoryModel()
scm = ScoreModel()
usm = UserModel()
