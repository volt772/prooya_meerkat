#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
from logging import handlers

_LOGGER = {
    "common": None,
    "app_prooya": None,
    "db_prooya": None,
}
_BASIC_PATH = "/var/log/prooya"

formatter = logging.Formatter("%(asctime)s [%(message)s]")


def setup_logger(name, log_file, level=logging.INFO):
    """로그 기본설정"""
    log_path = "{0}/{1}".format(_BASIC_PATH, log_file)

    mode = "a"
    handler = logging.FileHandler(log_path, mode=mode)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def save_log(kind, msg):
    """로그 저장"""
    if not kind or not msg:
        return False

    if kind == "app_prooya":
        log_name = "app_prooya"
        log_file = "app_prooya.log"
    elif kind == "db_prooya":
        log_name = "db_prooya"
        log_file = "db_prooya.log"
    else:
        log_name = "common"
        log_file = "common.log"

    _log = None
    if not _LOGGER[kind]:
        _log = setup_logger(log_name, log_file)
        _LOGGER[kind] = _log
    else:
        try:
            log_full_path = "{0}/{1}".format(_BASIC_PATH, log_file)
            if not os.path.exists(log_full_path):
                _log = setup_logger(log_name, log_file)
            else:
                _log = _LOGGER[kind]
        except Exception as e:
            pass

    try:
        _log.info(msg)
    except Exception as e:
        pass
