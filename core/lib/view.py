import json
import time
from operator import methodcaller

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse
from django.views import View

from core.common import helper
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
        # print('='*20,request.path_info.lstrip('/').lstrip('crawler'))
        return methodcaller(Route.routeList[request.path_info.lstrip('/').lstrip('crawler')])(self)  # 自调方法

    """
    get 处理
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        if request.path_info not in Route.routeList:
            pass
        print(Route.routeList, request.path_info)

        return methodcaller(Route.routeList[request.path_info.lstrip('/').lstrip('crawler')])(self)  # 自调方法

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

    """
    文件返回
    """

    def file_response(self, content, file_name: str = None) -> FileResponse:
        if file_name is None:
            file_name = helper.random_str()
        response = FileResponse(content)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = f'attachment;filename="{file_name}"'
        return response
