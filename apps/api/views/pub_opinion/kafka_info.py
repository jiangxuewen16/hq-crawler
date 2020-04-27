# -*- coding: utf-8 -*-
import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/kafka')
class PublicOpinion(BaseView):

    # 0简单示例（corpAccessToken）
    @Route.route(path='/connector/plugins')
    # 接收请求数据
    def search(self):
        login_url = 'http://172.18.54.27:8089/connector-plugins'
        login_headers = {
            'Content-Type': 'application/json'
        }
        if self.method == 'GET':
            r = requests.get(url=login_url, headers=login_headers)
            result = r.json()
        return self.success(result)

    @Route.route(path='/connectors')
    # 接收请求数据
    def connectors(self):
        login_url = 'http://172.18.54.27:8089/' + self.request_param['url']
        print(login_url)
        login_headers = {
            'Content-Type': 'application/json'
        }
        if self.method == 'POST':
            login_payload = self.request_param['data']
            r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
            result = r.json()
        return self.success(result)
