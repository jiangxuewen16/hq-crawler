import json
from operator import methodcaller

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View

from core.lib.route import Route


class BaseView(View):
    requestParam: dict = {}  # 请求数据

    def init(self):
        self.requestParam = json.loads(self.request.body)

    """
    post 处理
    """

    def post(self, request: WSGIRequest):
        self.init()
        return methodcaller(Route.routeList[request.path_info.lstrip('/')])(self)  # 自调方法

    """
    get 处理
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        pass

    """
    统一返回操作
    """
    @classmethod
    def response(cls, data: dict, contentType: str = 'application/json') -> HttpResponse:
        return HttpResponse(json.dumps(data), contentType)
