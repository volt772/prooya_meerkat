# -*- coding: utf-8 -*-

import datetime
import time

from crontab import CronTab
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")
date = year + month + day  # "20130615"

cron = CronTab(user="root")
con = connect(dbname="prooya", user="prooya", host="localhost", password="CjsdksgkA77@")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

TIME_SET = {
    "1400": "16|18",
    "1700": "19|21",
    "1800": "20|22",
    "1830": "21|23",
    "1900": "21|23",
}


def get_dict_all(cols, data):
    """쿼리 Row 생성"""
    record = []
    for row in data:
        record.append(dict(list(zip(cols, row))))

    return record


def make_playtime():
    """경기데이터 생성"""
    try:
        query = """SELECT id, stadium, starttime
                    FROM scores
                    WHERE playdate='{0}'""".format(
            date
        )

        cur = con.cursor()
        cur.execute(query)

        _data = cur.fetchall()
        _cols = [desc[0] for desc in cur.description]

        records = []
        if _data is not None:
            records = get_dict_all(_cols, _data)

        cur.close()

        make_scheduler(records)

    except Exception as e:
        print(e)
        pass


def make_scheduler(records):
    """경기 스케쥴러 생성"""

    #: 크론제거
    cron.remove_all()

    #: 크론 생성기(매일 1시)
    maker_cmd = "/usr/bin/python /home/prooya/prooya/scripts/play_automaker.py >> /var/log/playschedule.log 2>&1"
    job_maker = cron.new(maker_cmd)
    job_maker.minute.on(0)
    job_maker.hour.on(1)

    #: 병서크론(각 경기시간)
    if len(records) > 0:
        for play in records:
            upscore_standard = play.get("starttime")
            play_id = play.get("id")
            start_time = play.get("starttime")
            hour = str(start_time)[0:2]
            minute = str(start_time)[2:4]

            cavalry_cmd = (
                "/usr/bin/python /home/prooya/prooya/scripts/cavalry_score.py %s >> /var/log/playschedule.log 2>1"
                % (play_id)
            )

            job_cavalry = cron.new(cavalry_cmd)
            job_cavalry.minute.on(minute)
            job_cavalry.hour.on(hour)
            job_cavalry.day.on(day)
            job_cavalry.month.on(month)

        #: 실시간점수 크론(각 경기시작 후 2시간 후)
        upscore_timeset = TIME_SET[str(upscore_standard)].split("|")
        upscore_minute = upscore_timeset[0]
        score_cmd = "/usr/bin/python /home/prooya/prooya/scripts/realtimescore.py >> /var/log/playresult.log 2>&1"
        job_score = cron.new(score_cmd)
        job_score.minute.on(59)
        job_score.hour.on(23)
        job_score.day.on(day)
        job_score.month.on(month)

        # job_score = cron.new(score_cmd)
        # job_score.minute.every(5)
        # job_score.hour.during(upscore_timeset[0], upscore_timeset[1])
        # job_score.day.on(day)
        # job_score.month.on(month)

    for item in cron:
        print(item)

    #: 크론설정
    cron.write()


if __name__ == "__main__":
    make_playtime()
