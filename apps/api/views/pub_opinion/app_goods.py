import json

import requests
from scrapy import Request

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/application')
class PublicOpinion(BaseView):

    @Route.route(path='/index')
    def index(self):
        login_url = "https://api-saas.huiquyun.com/api/account/login" #正式
        # login_url = "https://api-saas.huiquyun.com/api/account/login" #测试
        login_headers = {
            "Content-Type": "application/json"
        }
        login_payload = {'userName': "ztyyzx", "password": "1q2w3E*"} #正式
        # login_payload = {'userName': "admin", "password": "1q2w3E*"}  #测试

        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()

        if 'access_token' in result:
            Authorization = result['token_type'] + " " + result['access_token']
            # url = "http://11.75.1.29:8056/"

            params = self.request_param
            url = params['api_url']
            headers = {'Authorization': Authorization, "Content-Type": "application/json"}

            # 处理.net那边没有名字的数组数据
            if 'php-list' in params:
                params = params['php-list']

            if 'request_type' in params:
                if params['request_type'] == 'post':
                    r = requests.post(url, headers=headers, data=json.dumps(params))
                elif params['request_type'] == 'put':
                    r = requests.put(url, headers=headers, data=json.dumps(params))
                elif params['request_type'] == 'delete':
                    r = requests.delete(url, headers=headers, data=json.dumps(params))
                else:
                    r = requests.get(url, headers=headers, params=params)
            else:
                r = requests.get(url, headers=headers, params=params)
        if r.text:
            result = r.json()
            return self.success(result)
        else:
            return self.success("接口错误！请检查参数或联系惠趣云相关技术人员！！")

    @Route.route(path='/test')
    def test(self):
        login_url = "http://11.75.1.29:8018/api/account/login"
        login_headers = {
            "Content-Type": "application/json"
        }
        login_payload = {'userName': "admin", "password": "1q2w3E*"}

        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)
