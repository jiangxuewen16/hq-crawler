import importlib
from collections import namedtuple
from types import FunctionType

# from django.urls import re_path
from django.urls import re_path
from hq_crawler import settings


"""
注解路由核心类
"""


class Route:
    routeViewPath = namedtuple('classPath', 'path module class_name func_name')  # 类方法-具名元组(路由路径 模块 类名 执行的方法名)
    classRouteTuple = namedtuple('classRoute', 'module class_name path')  # 类路由元祖(模块 类名 路由路径)

    ROUTER: list = []  # 路由与路由装饰器的映射
    classRoute: list = []  # 类路由
    routeList: dict = {}  # 路由对方法的映射

    @classmethod
    def route(cls, path):
        def my_decorator(func):
            # print('调用的方法列表：', func)
            # 类的路由
            if not isinstance(func, FunctionType):
                cls.classRoute.append(cls.classRouteTuple(func.__module__, func.__qualname__, path))
                return func

            cls.ROUTER.append(cls.routeViewPath(path, func.__module__, func.__qualname__[:func.__qualname__.index('.')],
                                                func.__name__))

            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            return wrapper

        return my_decorator

    @classmethod
    def register(cls, urlpatterns: list):
        print('='*30, '注册路由')
        routeKeyList = []
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
                    path_str = f'^{settings.BASE_URL}/' + classItem.path if settings.BASE_URL else f'^'
                    urlpatterns.append(re_path(path_str + classItem.path, routeClass.as_view())),
                    routeKeyList.append(classItem.path)

        print('总路由:', urlpatterns)
