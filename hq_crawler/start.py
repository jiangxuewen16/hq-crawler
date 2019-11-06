from django.contrib import admin
from django.urls import path, re_path

from core.lib.route import Route
from hq_crawler import settings

"""
django 路由配置,注解路由
"""
urlpatterns = [
    # re_path(r'^api/', include('apps.api.config.urls')),
    path('admin/', admin.site.urls),
]
Route.register(urlpatterns)

"""
启动爬虫部署
"""
if settings.SPIDER_START:  # 是否启动scrapy部署
    from core.lib.start import start_deploy_scrapy

    start_deploy_scrapy()  # 执行部署scrapy项目到scrapyd中

"""
引入定时任务核心代码，是否启动定时任务
"""
if settings.SCHEDULER_START:
    from core.lib.task import *  # 引入定时任务核心代码


