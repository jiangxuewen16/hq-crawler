"""hq_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import importlib

from django.contrib import admin
from django.urls import path, re_path

from hq_crawler import settings
from core.lib.route import Route

"""
启动某些应用
"""
if settings.SPIDER_START:  # 是否启动scrapy部署
    from core.lib.start import start_deploy_scrapy

    start_deploy_scrapy()  # 执行部署scrapy项目到scrapyd中


"""
引入定时任务核心代码，是否启动定时任务
"""
if settings.SCHEDULER_START:
    from core.lib.task import *  # 引入定时任务核心代码

"""
django 路由配置
"""
urlpatterns = [
    # re_path(r'^api/', include('apps.api.config.urls')),
    path('admin/', admin.site.urls),
]

"""
注册注解路由
"""
routeKeyList: list = []
for classItem in Route.classRoute:  # 类路由
    module = importlib.import_module(classItem.module)
    routeClass = getattr(module, classItem.class_name)
    for routeItem in Route.ROUTER:  # 方法路由
        if routeItem.module + routeItem.class_name == classItem.module + classItem.class_name:  # 是不是同一个类
            path = classItem.path + routeItem.path  # 路由路径
            if path in Route.routeList:
                exceptionStr = f'路由重复：{routeItem.module + routeItem.class_name} -> {routeItem.func_name}, 路径：{path}'
                raise Exception(exceptionStr)
            Route.routeList[path] = routeItem.func_name
            if classItem.path in routeKeyList:
                continue
            urlpatterns.append(re_path(r'^crawler/' + classItem.path, routeClass.as_view())),
            routeKeyList.append(classItem.path)

print('总路由:', urlpatterns)
