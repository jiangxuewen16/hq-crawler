import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/yc/crm/opinion')
class PublicOpinion(BaseView):

    # 0简单示例（corpAccessToken）
    @Route.route(path='/index')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/corp_access_token/get.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': 'ding36d91e596177829935c2f4657eb6378f',
                         'appId': '27d1f87c661c4493abe3bb53195ec66c',
                         'appSecret': '13ABCDD4D8E6B0F812074B42E8A64ACD'}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 1开放业务对象列表（object列表）
    @Route.route(path='/object/list')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/object/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': 'ding36d91e596177829935c2f4657eb6378f',
                         'corpAccessToken': '8f1be5fce9488dd1188d355701869f4c327831'}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 2业务对象字段列表（field列表）
    @Route.route(path='/object/field')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/object/field/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': 'ding36d91e596177829935c2f4657eb6378f',
                         'corpAccessToken': '8f1be5fce9488dd1188d355701869f4c327831',
                         'deployId': 'DEPLOY_ID'}  # deployId从上接口获取
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)

    # 3业务对象数据列表（data列表）
    @Route.route(path='/corp/data')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/data/list.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {
            "corpAccessToken": "8355993e7777895b9859f4771511530992ad4c",
            "corpId": "ding2037cc74cbb0f5e735c2f4657eb6378f",
            "deployId": "customer",
            "conditionConfig": [{
                "conditions": [
                    {
                        "comparison": "CONTAIN",
                        "deployId": "customer",
                        "fieldName": "custom_name",
                        "fieldTitle": "客户名称",
                        "fieldValue": "名字",
                        "domType": "INPUT"
                    },
                    {
                        "comparison": "CONTAIN",
                        "deployId": "customer",
                        "fieldName": "custom_nick",
                        "fieldTitle": "客户简称",
                        "fieldValue": "名字",
                        "domType": "INPUT"
                    }
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
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/v1/data/detail.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId': 'ding36d91e596177829935c2f4657eb6378f',
                         'corpAccessToken': '8f1be5fce9488dd1188d355701869f4c327831',
                         'deployId': 'DEPLOY_ID',
                         'dataId': 'DATA_ID'}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)
