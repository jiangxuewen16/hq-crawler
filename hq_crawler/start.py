from django.contrib import admin
from django.urls import path, re_path

from core.lib.route import Route
from hq_crawler import settings


"""
启动爬虫部署
"""
if settings.SPIDER_START:  # 是否启动scrapy部署
    print('##########启动scrapy部署:start##########')
    from core.lib.start import start_deploy_scrapy
    start_deploy_scrapy()  # 执行部署scrapy项目到scrapyd中
    print('##########启动scrapy部署：end##########')

"""
引入定时任务核心代码，是否启动定时任务
"""
if settings.SCHEDULER_START:
    print('##########启动定时任务:start##########')
    from core.lib.task import *  # 引入定时任务核心代码
    print('##########启动定时任务：end##########')

"""
django 路由配置,注解路由
"""
print('##########路由注册:start##########')
urlpatterns = [
    path('admin/', admin.site.urls),
]
Route.register(urlpatterns)
print('##########路由注册：end##########')


