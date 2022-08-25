#!/usr/bin/python3
# -*-coding:utf-8 -*-

import ast
import json


def get_score_data(score, play):
    score_data = {}
    if len(score) == 1:
        score_data = score[0]
    else:
        date_play = score[0]
        my_team = play["myteam"]
        home_team = date_play["hometeam"]
        away_team = date_play["awayteam"]

        away_score = 0
        home_score = 0

        if home_team == my_team:
            away_score = play["lostscore"]
            home_score = play["getscore"]
        else:
            away_score = play["getscore"]
            home_score = play["lostscore"]

        for _score in score:
            if _score["awayscore"] == away_score and _score["homescore"] == home_score:
                score_data = _score
                break

    return score_data
