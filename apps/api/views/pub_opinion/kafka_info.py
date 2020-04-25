# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpRequest

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/kafka/info/opinion')
class PublicOpinion(BaseView):

    # 0简单示例（corpAccessToken）
    @Route.route(path='/index')
    # 接收请求数据
    def search(self):
        host = self.request
        # request.encoding = 'utf-8'
        # if 'q' in request and request.GET['q']:
        #     message = '你搜索的内容为: ' + request.GET['q']
        # else:
        #     message = '你提交了空表单'
        return HttpResponse(self.method)
