#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" UserModel(사용자 데이터처리) """


class UserModel:
    def __init__(self):
        pass

    def get(self, pid):
        """사용자 정보 가져오기"""
        if not pid:
            return False

        query = """
            SELECT id, team
            FROM %s
            WHERE pid = '%s'
            """ % (
            USERS,
            pid,
        )

        user_info = db.fetch_one(query)

        return user_info

    def delete(self, _id):
        """사용자 정보 삭제"""
        if not _id:
            return False

        query = """
            DELETE FROM %s
            WHERE id = '%s'
            """ % (
            USERS,
            _id,
        )

        res = db.execute(query)

        return res

    def post(self, data):
        """사용자 신규등록"""
        if not data:
            return False

        query = """
            INSERT INTO %s (pid, team)
            VALUES ('%s', '%s')
            RETURNING id
            """ % (
            USERS,
            data["pid"],
            data["team"],
        )

        user_id = db.fetch_one(query)

        return user_id

    def put(self, data):
        """사용자 수정"""
        if not data:
            return False

        _col = data["col"]
        _update = data["update"]
        _where = data["where"]

        query = """
            UPDATE %s
            SET %s='%s'
            WHERE id='%s'
            RETURNING id
            """ % (
            USERS,
            _col,
            _update,
            _where,
        )

        res = db.fetch_one(query)

        return res
