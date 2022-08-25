#!/usr/bin/python3
# -*-coding:utf-8 -*-

import psycopg2
from helper import config, utils
from psycopg2 import pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

""" SQLHandler(데이터베이스 처리)
- postgresql 사용
- ThreadedConnectionPool 사용
- 참고 : https://pynative.com/psycopg2-python-postgresql-connection-pooling/
"""


class SQLHandler:
    def __init__(self):
        self.threaded_postgreSQL_pool = None
        self.connection()

    def get_conn(self):
        """Connection 요청"""
        ps_connection = self.threaded_postgreSQL_pool.getconn()
        ps_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        if ps_connection:
            ps_cursor = ps_connection.cursor()

        return ps_connection, ps_cursor

    def put_conn(self, ps_connection):
        """Connection 반환"""
        self.threaded_postgreSQL_pool.putconn(ps_connection)

    def destroy(self):
        """모든 Connection 종료"""
        if self.threaded_postgreSQL_pool:
            self.threaded_postgreSQL_pool.closeall

    def connection(self):
        """Database 연결 및 ConnectionPool 생성"""
        _d = config.get_config("postgres_%s" % (utils.get_host()))

        self.threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(
            1,
            1000,
            user=_d["db_user"],
            password=_d["db_pass"],
            host=_d["db_host"],
            port=_d["db_port"],
            database=_d["db_name"],
        )

    def fetch_one(self, query):
        """쿼리"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        _data = ps_cursor.fetchone()
        _cols = [desc[0] for desc in ps_cursor.description]

        record = []
        if _data is not None:
            record = self.get_dict_one(_cols, _data)[0]

        ps_cursor.close()
        self.put_conn(ps_connection)
        return record

    def fetch_all(self, query):
        """쿼리"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        _data = ps_cursor.fetchall()
        _cols = [desc[0] for desc in ps_cursor.description]

        records = []
        if _data is not None:
            records = self.get_dict_all(_cols, _data)

        self.put_conn(ps_connection)
        return records

    def execute(self, query):
        """쿼리"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        rowcount = ps_cursor.rowcount
        ps_cursor.close()
        self.put_conn(ps_connection)
        return rowcount

    def get_dict_all(self, cols, data):
        """쿼리 Row 생성"""
        record = []
        for row in data:
            record.append(dict(list(zip(cols, row))))

        return record

    def get_dict_one(self, cols, data):
        """쿼리 Row 생성"""
        rows = []
        record = []
        for row in data:
            rows.append(row)

        record.append(dict(list(zip(cols, rows))))
        return record


if __name__ == "__main__":
    pp = SQLHandler()
    # pp.connection()
    pp.fetch_one("select * from users limit 10")
    pp.fetch_all("select * from users limit 10")
    pp.execute("update users set fcm_token='ABCD' where pid='volt772@naver.com'")
