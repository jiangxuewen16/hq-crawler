import json
import math

import scrapy

from spiders.items.association.association import Association


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
        print(json_data['data']['data']['corpAccessToken'])
        print(json_data)
        url = self.start_urls[1]
        post_data = {
            "corpAccessToken": json_data['data']['data']['corpAccessToken'],
            # "corpAccessToken": "caaac76ac9bbec7a4db09aac0b9977d2c3524c",
            "corpId": self.CORP_ID,
            "deployId": "customer",
            "conditionConfig": [{
                "conditions": [
                    {
                        "comparison": "CONTAIN",
                        "deployId": "customer",
                        "domType": "INPUT"
                    }
                ]
            }],
            "page": 1,
            "pageSize": 1
        }
        headers = {
            'Content-Type': 'application/json'
        }
        yield scrapy.FormRequest(url=url, body=json.dumps(post_data), method='POST', headers=headers,
                                 callback=self.parse_count,
                                 meta={'corpAccessToken': json_data['data']['data']['corpAccessToken']})

    def parse_count(self, response):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        print(json_data['result'])
        print(json_data)
        url = self.start_urls[1]
        headers = {
            'Content-Type': 'application/json'
        }
        page = math.ceil(json_data['data']['data']['count'] / 100)
        for page_num in range(1, page + 1):
            post_data = {
                "corpAccessToken": response.meta['corpAccessToken'],
                "corpId": self.CORP_ID,
                "deployId": "customer",
                "conditionConfig": [{
                    "conditions": [
                        {
                            "comparison": "CONTAIN",
                            "deployId": "customer",
                            "domType": "INPUT"
                        }
                    ]
                }],
                "page": page_num,
                "pageSize": 100
            }
            yield scrapy.FormRequest(url=url, body=json.dumps(post_data), method='POST', headers=headers,
                                     callback=self.parse_list, meta={'page_num': page_num})

    def parse_list(self, response):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        print(json_data['data']['data']['list'])
        print(json_data)

        if 'data' in json_data['data'] and 'list' in json_data['data']['data']:
            for key, value in enumerate(json_data['data']['tagList']):
                yield Association.objects(chat_room_id=value['customer_input_4']).update_one(  # 团长群编码
                    set__team_leader_id=value['customer_input_2'],  # 团长ID(用户ID)
                    set__team_leader_name=value['custom_nick'],  # 团长姓名
                    set__team_leader_tel=value['custom_tele'],  # 团长电话
                    set__charger_name=value['charger_name'],  # 负责人
                    upsert=True)
