#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser


def get_config(key):
    if not key:
        return False

    res = {}
    config = configparser.ConfigParser()
    config.read("/etc/config.ini")

    if key == "app_pr":
        res["app_host"] = config.get("app_pr", "app_host")
        res["app_port"] = config.get("app_pr", "app_port")
        res["app_debug"] = config.get("app_pr", "app_debug")

    if key == "postgres_pr":
        res["db_host"] = config.get("postgres_pr", "db_host")
        res["db_pass"] = config.get("postgres_pr", "db_pass")
        res["db_user"] = config.get("postgres_pr", "db_user")
        res["db_port"] = config.get("postgres_pr", "db_port")
        res["db_name"] = config.get("postgres_pr", "db_name")

    if key == "app_te":
        res["app_host"] = config.get("app_te", "app_host")
        res["app_port"] = config.get("app_te", "app_port")
        res["app_debug"] = config.get("app_te", "app_debug")

    if key == "postgres_te":
        res["db_host"] = config.get("postgres_te", "db_host")
        res["db_pass"] = config.get("postgres_te", "db_pass")
        res["db_user"] = config.get("postgres_te", "db_user")
        res["db_port"] = config.get("postgres_te", "db_port")
        res["db_name"] = config.get("postgres_te", "db_name")

    return res
