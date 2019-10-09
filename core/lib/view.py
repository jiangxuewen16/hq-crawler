import json
import time
from operator import methodcaller

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View

from core.common.service_code import ServiceCode
from core.lib.route import Route

"""
基础view类型
"""


class BaseView(View):
    # request_param: dict = {}  # 请求数据
    token: str = ''

    def __init(self):
        request = json.loads(self.request.body)
        print(type(request))
        self._request_param = request['data']
        self.version = request['head']['version']
        self.time = request['head']['time']
        self.token = request['head']['token']
        self.platform = request['head']['platform']

    """
    post 处理
    """

    def post(self, request: WSGIRequest):
        self.__init()
        if request.path_info not in Route.routeList:
            pass
        return methodcaller(Route.routeList[request.path_info.lstrip('/')])(self)  # 自调方法

    """
    get 处理
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        pass

    @property
    def request_param(self):
        return self._request_param

    """
    统一返回操作
    """

    def __response(self, data: dict, service_code: ServiceCode, contentType: str = 'application/json') -> HttpResponse:
        response: dict = {'head': {'token': self.token, 'time': int(time.time()), 'code': service_code.value.code,
                                   'message': service_code.value.msg}, 'data': data}

        return HttpResponse(json.dumps(response), contentType)

    """
    成功返回方法
    """

    def success(self, data: dict, service_code: ServiceCode = ServiceCode.other_success) -> HttpResponse:
        return self.__response(data, service_code)

    """
    失败返回方法
    """

    def failure(self, service_code: ServiceCode = ServiceCode.other_failure, data: dict = None) -> HttpResponse:
        return self.__response(data, service_code)
