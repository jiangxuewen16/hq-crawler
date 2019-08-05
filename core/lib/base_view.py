import json
from operator import methodcaller

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View
from types import MethodType, FunctionType


class BaseView(View):
    requestParam: dict

    ROUTER: dict = {}

    def init(self):
        self.requestParam = json.loads(self.request.body)

    """
    post 处理
    """

    def post(self, request: WSGIRequest):
        # print(dir(self.request))
        self.init()

        print(BaseView.ROUTER[request.path_info])
        print(BaseView.ROUTER)
        return methodcaller(BaseView.ROUTER[request.path_info])(self)  # 自调方法

    """
    get 处理
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        pass

    @classmethod
    def response(cls, data: dict, contentType: str = 'application/json') -> HttpResponse:
        return HttpResponse(json.dumps(data), contentType)

    @classmethod
    def route(cls, path):
        def my_decorator(func):
            # 类的路由
            if not isinstance(func, FunctionType):
                return func

            # 方法路由
            print(func.__name__, ':', BaseView.ROUTER)
            if func.__name__ in BaseView.ROUTER:
                raise BaseException('路由已经存在')

            BaseView.ROUTER[path] = func.__name__
            print(func.__name__, ':', BaseView.ROUTER)

            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            return wrapper

        return my_decorator
