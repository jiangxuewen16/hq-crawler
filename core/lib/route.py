from collections import namedtuple
from types import FunctionType


class Route:
    ROUTER: dict = {}  # 路由与路由装饰器的映射
    routeViewPath = namedtuple('classPath', 'full_class_name func_name')  # 类方法-具名元组
    classRoute = {}

    @classmethod
    def route(cls, path):
        def my_decorator(func):
            print('类名：', func.__module__, func.__qualname__)
            # 类的路由
            if not isinstance(func, FunctionType):
                classFullName = f'{func.__module__}.{func.__qualname__}'
                cls.classRoute[classFullName] = path
                # cls.ROUTER[path] = cls.routeViewPath('class', f'{func.__module__}.{func.__qualname__}', func.__name__)
                return func

            # 方法路由
            # print('类名：', cls.__name__)
            print(func.__name__, ':', cls.ROUTER)
            if func.__name__ in cls.ROUTER:
                raise BaseException('路由已经存在')

            classFullName = f'{func.__module__}.{func.__qualname__}'

            cls.ROUTER[path] = cls.routeViewPath(classFullName, func.__name__)  #
            print(func.__name__, ':', cls.ROUTER)

            def wrapper(self, *args, **kwargs):
                print('类名：')
                return func(self, *args, **kwargs)

            return wrapper

        return my_decorator
