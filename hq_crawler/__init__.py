from __future__ import absolute_import

import os

import pymysql

from core.common.helper import auto_import_module
from .celery import app as celery_app


# 这里放每个应用的视图包，自动加载，主要用于自定路径路由注册
auto_import_module('apps.api.views')  # view包，业务代码写到此包中
auto_import_module('apps.scheduler.mq')  # mq包，mq代码写到此包中

pymysql.install_as_MySQLdb()

__all__ = ['celery_app']
