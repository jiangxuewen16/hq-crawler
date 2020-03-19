import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView
from django.core.cache import cache


@Route.route(path='api/yc/crm/opinion')
class PublicOpinion(BaseView):
    CORP_ID = 'ding36d91e596177829935c2f4657eb6378f'
    APP_ID = '27d1f87c661c4493abe3bb53195ec66c'
    APP_SECRET = '13ABCDD4D8E6B0F812074B42E8A64ACD'
    CORE_ACCESS_TOKEN = 'b99dee9141d63559f761da5d8ef0ce9f7b74f0'

    # 0简单示例（corpAccessToken）
    @Route.route(path='/index')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/corp_access_token/get.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': self.CORP_ID,
                         'appId': self.APP_ID,
                         'appSecret': self.APP_SECRET}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 1开放业务对象列表（object列表）
    @Route.route(path='/object/list')
    def object_list(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/object/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': self.CORP_ID,
                         'corpAccessToken': cache.get('CORE_ACCESS_TOKEN')}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 2业务对象字段列表（field列表）
    @Route.route(path='/object/field')
    def object_field(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/object/field/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': self.CORP_ID,
                         'corpAccessToken': cache.get('CORE_ACCESS_TOKEN'),
                         'deployId': 'customer'}  # deployId从上接口获取
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 3业务对象数据列表（data列表）
    @Route.route(path='/corp/data')
    def corp_data(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/data/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {
            "corpAccessToken": cache.get('CORE_ACCESS_TOKEN'),
            "corpId": self.CORP_ID,
            "deployId": "customer",
            "conditionConfig": [{
                "conditions": [
                    {
                        "comparison": "CONTAIN",
                        "deployId": "customer",
                        "fieldName": "customer_input_2",
                        "fieldTitle": "团长经销ID",
                        "fieldValue": "test团长经销ID",
                        "domType": "INPUT"
                    }
                    # {
                    #     "comparison": "CONTAIN",
                    #     "deployId": "customer",
                    #     "fieldName": "custom_nick",
                    #     "fieldTitle": "客户简称",
                    #     "fieldValue": "名字",
                    #     "domType": "INPUT"
                    # }
                ]
            }],
            "page": 1,
            "pageSize": 2
        }
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 4业务对象数据详情（object列表）
    @Route.route(path='/data/detail')
    def data_detail(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/data/detail.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': self.CORP_ID,
                         'corpAccessToken': cache.get('CORE_ACCESS_TOKEN'),
                         'deployId': 'customer',
                         'dataId': '456633'}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # redis测试
    @Route.route(path='/data/redis')
    def data_redis(self):
        cache.set('CORE_ACCESS_TOKEN', self.request_param['CORE_ACCESS_TOKEN'], 7200)
        return self.success(cache.get('CORE_ACCESS_TOKEN'))
