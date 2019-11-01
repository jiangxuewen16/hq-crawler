"""
Django settings for hq_crawler project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import importlib
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

import mongoengine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, "spiders"))  # 引入依赖包

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f2#y!1$b2_(x&fe3-du_&5jml#x1gcb%#w12)=rjofxd-wucp1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_apscheduler',  # 定时执行任务
    'djcelery',  # django-celery异步包

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'core.middleware.scheduler.Scheduler'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ('*')

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

ROOT_URLCONF = 'hq_crawler.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hq_crawler.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'hq_crawler',
        # 'USER': 'root',
        # 'HOST': '192.168.56.100',
        # 'PASSWORD': 'root',
        # 'PORT': 3306,
        # 'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "yoursecret",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 项目目录路径
STATIC_URL = '/static/'

"""
惠趣项目配置（api、task）
下面是项目自定义配置
"""

mongoengine.connect('hq_data_cloud', username='hq_data_cloud', password='hqlxhqdatacloud2019', host='mongodb://dds-wz9542ab304a64a41.mongodb.rds.aliyuncs.com:3717', alias='default')  # 连接hq_crawler.mongodb
mongoengine.connect('passport', username='passport', password='hqlxpassport2019', host='mongodb://dds-wz9542ab304a64a41.mongodb.rds.aliyuncs.com:3717', alias='passport')  # 连接passport

"""
定时调度任务业务包
"""
SCHEDULER_START = True  # 是否开启调度任务
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
from hq_crawler import celery
import djcelery

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
CELERY_TIMEZONE = TIME_ZONE
