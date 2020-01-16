import os

import mongoengine
from hq_crawler import celery, settings
import djcelery

from hq_crawler.settings import BASE_DIR, PROJECT_NAME

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'hq_crawler',
    #     'USER': 'root',
    #     'HOST': '11.75.1.124',
    #     'PASSWORD': '123456',
    #     'PORT': 3306,
    #     'OPTIONS': {'charset': 'utf8mb4'},
    # }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://11.75.1.124:6379/8",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "yoursecret",
        }
    }
}

# 日志配置
BASE_LOG_DIR = os.path.join(BASE_DIR, "log")
if not os.path.isdir(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # True 表示禁用loggers

    'formatters': {     # 可以设置多种格式，根据需要选择保存的格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    'filters': {  # 定义日志的过滤器
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理程序
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'SF': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据文件大小自动切
            'filename': os.path.join(BASE_LOG_DIR, f"{PROJECT_NAME}_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 500,  # 日志大小 50M（最好不要超过1G）
            'backupCount': 3,  # 备份数为3 xx.log --> xx.log.1 --> xx.log.2 --> xx.log.3
            'formatter': 'standard',
            'encoding': 'utf-8',  # 文件记录的编码格式
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, f"{PROJECT_NAME}_info.log"),  # 日志文件
            'backupCount': 3,  # 备份数为3 xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            'when': 'D',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, f"{PROJECT_NAME}_err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, f"{PROJECT_NAME}_collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {  # 日志实例
        '': {  # 默认的logger应用如下配置
            'handlers': ['SF', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 是否向上一级logger实例传递日志信息
        },
        'collect': {  # 名为 'collect' 的logger还单独处理
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        }
    },
}


"""
惠趣项目配置（api、task）
下面是项目自定义配置
"""

BASE_URL = ''

mongoengine.connect('hq_crawler', host='mongodb://11.75.1.124:27017', alias='default')  # 连接hq_crawler.mongodb
mongoengine.connect('passport', host='mongodb://11.75.1.124:27017', alias='passport')  # 连接passport

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
SPIDER_PATH = f'{settings.BASE_DIR}/spiders/'  # 爬虫项目目录

"""
rabbitmq 配置
"""
RABBITMQ_CONF = {
    'host': '118.126.105.239',
    'port': 5672,
    'api_port': 15672,
    'user': 'guest',
    'password': 'guest',
    'vhost': '/',

    'passive': False,
    'durable': True,
    'auto_delete': False,
    'exclusive': False,
    'no_local': False,
    'no_ack': False,
    'nowait': False,
    'consumer_tag': '',
}

"""
惠趣邮件配置
"""
EMAIL_CONF = {
    'host': 'smtp.qq.com',
    'port': 465,
    'sender': '445251692@qq.com',
    'sender_name': '惠趣运维中心',
    'user_name': '445251692@qq.com',
    'password': 'vadzhpbsercybhje'
}

"""
异步任务扩展
"""

djcelery.setup_loader()
# 有些情况可以防止死锁
CELERYD_FORCE_EXECV = True
# 设置并发worker数量
CELERYD_CONCURRENCY = 4
# 允许重试
CELERY_ACKS_LATE = True
# 每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100
# 超时时间
# CELERYD_TASK_TIME_LIMIT = 12 * 30
CELERY_DISABLE_RATE_LIMITS = True

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
BROKER_BACKEND = 'redis'
# celery settings
# celery中间人 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://:jiangxuewen@118.126.105.239:6378/1'
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://:jiangxuewen@118.126.105.239:6378/1'
# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = settings.TIME_ZONE
