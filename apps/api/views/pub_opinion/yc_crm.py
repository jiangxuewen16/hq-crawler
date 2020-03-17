import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/yc/crm/opinion')
class PublicOpinion(BaseView):

    # 简单示例（字符串返回）
    @Route.route(path='/index')
    def index(self):
        login_url = 'http://crmapi.superboss.cc/oapi/corp/corp_access_token/get.json'
        login_headers = {
            'Content-Type': 'application/json'
        }
        login_payload = {'corpId':'ding36d91e596177829935c2f4657eb6378f',
                         'appId': '27d1f87c661c4493abe3bb53195ec66c',
                         'appSecret': '13ABCDD4D8E6B0F812074B42E8A64ACD'}
        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        result = r.json()
        return self.success(result)
