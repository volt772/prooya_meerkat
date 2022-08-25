#!/usr/bin/python3
# -*-coding:utf-8 -*-

from model import *

""" RecordModel(기록 데이터처리) """


class RecordModel:
    def __init__(self):
        pass

    def get_recent(self, data):
        """기록 가져오기(최근1건)"""
        if not data:
            return False

        query = """
            SELECT r.regdate, r.versus, r.result, u.pid
            FROM %s AS u
            JOIN %s AS r
            ON r.pid = u.id
            WHERE u.pid = '%s' AND r.year = '%s'
            ORDER BY r.regdate DESC LIMIT 1
            """ % (
            USERS,
            RECORDS,
            data["pid"],
            data["year"],
        )

        record = db.fetch_one(query)

        return record

    def get_one(self, data):
        """기록 가져오기(단일)"""
        if not data:
            return False

        pid = data.get("pid")
        team = data.get("team")

        regdate = data["playdate"]
        get_score = data["get_score"]
        lost_score = data["lost_score"]

        query = """
            SELECT *
            FROM %s
            WHERE regdate = '%s'
            AND pid = '%s'
            AND myteam = '%s'
            AND getscore = %s
            AND lostscore = %s
            """ % (
            RECORDS,
            regdate,
            pid,
            team,
            get_score,
            lost_score,
        )

        record = db.fetch_one(query)

        return record

    def get_all(self, data):
        """기록 가져오기(전체)"""
        if not data:
            return False

        pid = data.get("pid")
        versus = data.get("versus")
        year = data.get("year")

        versus_condition = ""
        if data["versus"] != "False":
            versus_condition = "AND r.versus = '%s' AND r.year = '%s'" % (versus, year)

        query = """
            SELECT *
            FROM %s AS u
            JOIN %s AS r
            ON r.pid = u.id
            WHERE u.pid = '%s' %s
            ORDER BY r.regdate DESC
            """ % (
            USERS,
            RECORDS,
            pid,
            versus_condition,
        )

        record = db.fetch_all(query)

        return record

    def delete(self, data):
        """기록 삭제(선택)"""
        if not data:
            return False

        if "pid" in data:
            del_condition = "pid = '%s'" % (data["pid"])
        else:
            del_condition = "id = '%s'" % (data["rid"])

        res = db.execute(
            """
            DELETE FROM %s
            WHERE %s AND year = '%s'"""
            % (RECORDS, del_condition, data["year"])
        )

        return res

    def delete_all(self, pid):
        """기록 삭제(전체)"""
        if not pid:
            return False

        res = db.execute(
            """
            DELETE FROM %s
            WHERE pid = '%s' RETURNING id"""
            % (RECORDS, pid)
        )

        return res

    def post(self, data):
        """기록 추가"""
        if not data:
            return False

        record_id = db.fetch_one(
            """
            INSERT INTO %s
            (pid, year, versus, result, getscore, lostscore, regdate)
            VALUES (%s, %s, '%s', '%s', %s, %s, '%s') RETURNING id"""
            % (
                RECORDS,
                data["pid"],
                data["year"],
                data["versus"],
                data["result"],
                data["getscore"],
                data["lostscore"],
                data["regdate"],
            )
        )

        return record_id["id"]
