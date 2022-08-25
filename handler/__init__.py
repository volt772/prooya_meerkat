#!/usr/bin/python3
# -*-coding:utf-8 -*-

from flask import jsonify
from helper import utils
from model.admin import AdminModel
from model.record import RecordModel
from model.score import ScoreModel
from model.team import TeamModel
from model.user import UserModel

# Model Variable
MADMIN = AdminModel()
MUSER = UserModel()
MTEAM = TeamModel()
MRECORD = RecordModel()
MSCORE = ScoreModel()
