from collections import namedtuple
from types import FunctionType

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
            print('调用的方法列表：', func)
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
