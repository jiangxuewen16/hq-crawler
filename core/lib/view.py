import json
import time
from operator import methodcaller

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse
from django.views import View

from core.common import helper
from core.common.service_code import ServiceCode
from core.lib.route import Route
from hq_crawler import settings
from django.utils.autoreload import logger

"""
基础view类型
"""


class BaseView(View):
    # request_param: dict = {}  # 请求数据
    token: str = ''

    def __init(self):
        request = json.loads(self.request.body)
        logger.info('请求参数：' + str(self.request.body))
        self._request_param = request['data'] if request['data'] else ''
        # self._request_param = None
        self.version = request['head']['version'] if request['head']['version'] else ''
        self.time = request['head']['time'] if request['head']['time'] else ''
        self.token = request['head']['token'] if request['head']['token'] else ''
        self.platform = request['head']['platform'] if request['head']['platform'] else ''

    """
    post 处理
    """

    def post(self, request: WSGIRequest):
        if len(request.FILES) <= 0:
            self.__init()

        if request.path_info not in Route.routeList:
            pass
        # logger.info('='*20,request.path_info.lstrip('/').lstrip('crawler'))
        return methodcaller(self._route_url(request.path_info))(self)  # 自调方法

    """
    get 处理
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        if request.path_info not in Route.routeList:
            pass
        # logger.info(Route.routeList, request.path_info)
        # print(request.path_info)
        return methodcaller(self._route_url(request.path_info))(self)  # 自调方法

    @classmethod
    def _route_url(cls, url):
        return Route.routeList[url.replace('/' + settings.BASE_URL, '', 1)]

    @property
    def request_param(self):
        return self._request_param

    """
    统一返回操作
    """

    def __response(self, data: dict, service_code: ServiceCode, contentType: str = 'application/json') -> HttpResponse:
        response: dict = {'head': {'token': self.token, 'time': int(time.time()), 'code': service_code.value.code,
                                   'message': service_code.value.msg}, 'data': data}
        logger.info('返回参数：' + json.dumps(response))
        return HttpResponse(json.dumps(response), contentType)

    """
    成功返回方法
    """

    def success(self, data: dict = {}, service_code: ServiceCode = ServiceCode.other_success) -> HttpResponse:
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
