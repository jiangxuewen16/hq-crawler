"""
Django settings for hq_crawler project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import configparser
import importlib
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

import mongoengine
from django.urls import include

from core.common.helper import auto_import_module

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, "spiders"))       # 引入依赖包

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f2#y!1$b2_(x&fe3-du_&5jml#x1gcb%#w12)=rjofxd-wucp1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['11.75.1.20']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',  # 定时执行任务

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.scheduler.Scheduler'
]

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
MONGO_CONNECT = mongoengine.connect('hq_crawler', host='mongodb://11.75.1.20:27017')  # 连接mongodb

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
SEP = os.sep

"""
惠趣项目配置（api、task）
下面是项目自定义配置
"""

# 这里放每个应用的视图包，自动加载，主要用于自定路径路由注册
auto_import_module('apps.api.views')  # view包，业务代码写到此包中

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
