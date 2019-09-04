from .base import *

DEBUG = False

ALLOWED_HOSTS = ['11.75.1.20', '127.0.0.1']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         # 'ENGINE': 'django.db.backends.mysql',
#         # 'NAME': 'spider',
#         # 'USER': 'root',
#         # 'HOST': '127.0.0.1',
#         # 'PASSWORD': '123456',
#         # 'PORT': 3306,
#         # 'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }

mongoengine.connect('hq_crawler', host='mongodb://11.75.1.20:27017')  # 连接mongodb

"""
定时调度任务业务包
"""
SCHEDULER_START = False  # 是否开启调度任务
# 定时任务业务包，定时任务写到这里
TASK_WORK_PACKAGE = 'apps.scheduler.task'

"""
惠趣采集项目配置
"""
SPIDER_START = False  # 是否开启采集项目
SPIDER_PATH = f'{BASE_DIR}/spiders/'  # 爬虫项目目录

"""
rabbitmq 配置
"""
RABBITMQ_START = False
RABBITMQ_CONF = {
    'host': '118.126.105.239',
    'port': 5672,
    'user': 'guest',
    'password': 'guest',
    'vhost': '/'
}