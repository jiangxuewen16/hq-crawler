import mongoengine
from hq_crawler import celery, settings
import djcelery

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'huiqulx_crawler',
        'USER': 'mall',
        'HOST': 'rm-wz9nc4b599n2ec13u.mysql.rds.aliyuncs.com',
        'PASSWORD': 'jPsbwvQiDGwoCRr0',
        'PORT': 3306,
        # 'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://106.13.28.248/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "jiangxuewen",
        }
    }
}

"""
惠趣项目配置（api、task）
下面是项目自定义配置
"""

BASE_URL = 'crawler/'

"""mongodb连接"""
mongoengine.connect('hq_data_cloud', username='hq_data_cloud', password='hqlxhqdatacloud2019',
                    host='mongodb://dds-wz9542ab304a64a42.mongodb.rds.aliyuncs.com:3717',
                    alias='default')  # 连接hq_crawler.mongodb
mongoengine.connect('passport', username='passport', password='hqlxpassport2019',
                    host='mongodb://dds-wz9542ab304a64a42.mongodb.rds.aliyuncs.com:3717',
                    alias='passport')  # 连接passport

"""
定时调度任务业务包
"""
SCHEDULER_START = True  # 是否开启调度任务
# 定时任务业务包，定时任务写到这里
TASK_WORK_PACKAGE = 'apps.scheduler.task'

"""
惠趣采集项目配置
"""
SPIDER_START = True  # 是否开启采集项目
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
