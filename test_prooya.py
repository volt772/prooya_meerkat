#!/usr/bin/python3
# -*-coding:utf-8 -*-

import json
import unittest
from collections import OrderedDict

from app import app

app.testing = True


class TestProoya(unittest.TestCase):

    rid = ""

    def test_a_check_ping(self):
        with app.test_client() as client:
            sent = {}
            result = client.post("/app/ping")

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertTrue(res_decoded["res"], "")
            print("/app/ping : ", res_decoded)

    def test_b_user_handler_postuser(self):
        with app.test_client() as client:
            sent = {
                "pid": "superhamster@naver.com",
                "team": "dsb",
            }

            result = client.post("/user/postuser", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/user/postuser : ", res_decoded)

    def test_c_user_handler_getuser(self):
        with app.test_client() as client:
            sent = {
                "pid": "superhamster@naver.com",
                "fcmToken": "alkjdflkjasdlkflkasdflkjsdflkjasdlkfjksldfjklsd",
            }
            result = client.post("/user/getuser", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/user/getuser : ", res_decoded)

    def test_d_record_handler_postrecord(self):
        with app.test_client() as client:
            sent = {
                "result": "w",
                "year": "2018",
                "regdate": "2018-11-11",
                "pid": "superhamster@naver.com",
                "lostscore": "5",
                "versus": "dsb",
                "getscore": "10",
            }

            result = client.post("/record/postrecord", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            self.__class__.rid = res_decoded["res"]
            print("/record/postrecord : ", res_decoded)

    def test_e_record_handler_getrecord(self):
        with app.test_client() as client:
            sent = {"pid": "superhamster@naver.com", "versus": "False"}
            result = client.post("/record/getrecord", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/record/getrecord : ", res_decoded)

    def test_f_score_handler_getscore(self):
        with app.test_client() as client:
            sent = {"playdate": "20180515", "favteam": "kwh"}

            result = client.post("/score/getscore", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/score/getscore : ", res_decoded)

    def test_g_team_handler_getteam(self):
        with app.test_client() as client:
            sent = {
                "pid": "superhamster@naver.com",
            }
            result = client.post("/team/getteam", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/team/getteam : ", res_decoded)

    def test_h_record_handler_delrecord(self):
        with app.test_client() as client:
            sent = {
                "result": "w",
                "year": "2018",
                "pid": "superhamster@naver.com",
                "rid": self.__class__.rid,
                "versus": "dsb",
            }

            result = client.post("/record/delrecord", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/record/delrecord : ", res_decoded)

    def test_i_user_handler_deluser(self):
        with app.test_client() as client:
            sent = {
                "pid": "superhamster@naver.com",
            }
            result = client.post("/user/deluser", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/user/deluser : ", res_decoded)

    def test_j_admin_handler_getscore(self):
        with app.test_client() as client:
            sent = {"playdate": "20170505"}

            result = client.post("/admin/getscore", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/admin/getscore : ", res_decoded)

    def test_k_admin_handler_putscore(self):
        with app.test_client() as client:
            sent = {"dbid": "1", "homescore": "21", "awayscore": "51"}

            result = client.post("/admin/putscore", json=sent)

            res_decoded = json.loads(result.data.decode("utf-8"))
            self.assertIsInstance(res_decoded, dict)
            print("/admin/putscore : ", res_decoded)
