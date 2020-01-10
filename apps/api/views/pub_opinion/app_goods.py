import json

import requests
from scrapy import Request

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/application')
class PublicOpinion(BaseView):

    @Route.route(path='/index')
    def index(self):
        login_url = "http://11.75.1.29:8018/api/account/login"
        login_headers = {
            "Content-Type": "application/json"
        }
        login_payload = {'userName': "admin", "password": "1q2w3E*"}

        r = requests.post(url=login_url, headers=login_headers, data=json.dumps(login_payload))
        print(r.json())
        result = r.json()

        if 'access_token' in result:
            Authorization = result['token_type'] + " " + result['access_token']
            # url = "http://11.75.1.29:8056/"

            params = self.request_param
            url = params['api_url']
            headers = {'Authorization': Authorization}
            if 'request_type' in params:
                if params['request_type'] == 'POST':
                    r = requests.post(url, headers=headers, data=params)
                else:
                    r = requests.get(url, headers=headers, params=params)
            else:
                r = requests.get(url, headers=headers, params=params)
            result = r.json()
            # r = requests.post(url, headers=headers, data=params)
        return self.success(result)