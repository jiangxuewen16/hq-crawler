import json

import scrapy


class CrmSpider(scrapy.Spider):
    name = "crm"
    allowed_domains = ['crmapi.superboss.cc']
    start_urls = [
        'http://crmapi.superboss.cc/oapi/corp/corp_access_token/get.json',
        'http://crmapi.superboss.cc/oapi/corp/v1/data/list.json'

    ]
    request_cookie = ''
    CORP_ID = 'ding36d91e596177829935c2f4657eb6378f'
    APP_ID = '27d1f87c661c4493abe3bb53195ec66c'
    APP_SECRET = '13ABCDD4D8E6B0F812074B42E8A64ACD'
    CORE_ACCESS_TOKEN = 'b99dee9141d63559f761da5d8ef0ce9f7b74f0'

    def start_requests(self):
        url = self.start_urls[0]
        post_data = {'corpId': self.CORP_ID,
                     'appId': self.APP_ID,
                     'appSecret': self.APP_SECRET}
        headers = {
            'Content-Type': 'application/json'
        }
        yield scrapy.FormRequest(url=url, body=json.dumps(post_data), method='POST', headers=headers,
                                 callback=self.parse)

    def parse(self, response):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        print(json_data['result'])
        print(json_data)
    #     url = self.start_urls[1]
    #     post_data = {
    #         # "corpAccessToken": json_data['data']['corpAccessToken'],
    #         "corpAccessToken": "caaac76ac9bbec7a4db09aac0b9977d2c3524c",
    #         "corpId": self.CORP_ID,
    #         "deployId": "customer",
    #         "conditionConfig": [{
    #             "conditions": [
    #                 {
    #                     "comparison": "CONTAIN",
    #                     "deployId": "customer",
    #                     "domType": "INPUT"
    #                 }
    #             ]
    #         }],
    #         "page": 1,
    #         "pageSize": 2
    #     }
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     yield scrapy.FormRequest(url=url, body=json.dumps(post_data), method='POST', headers=headers,
    #                              callback=self.parse_data)
    #
    # def parse_data(self, response):
    #     response_str = response.body.decode('utf-8')
    #     json_data = json.loads(response_str)
    #     print(json_data['result'])
    #     print(json_data)
