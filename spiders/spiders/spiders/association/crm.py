import json
from urllib import parse

import scrapy
from pykafka import KafkaClient


class CrmSpider(scrapy.Spider):
    name = "crm"
    allowed_domains = ['crmapi.superboss.cc']
    start_urls = ['http://crmapi.superboss.cc/oapi/corp/corp_access_token/get.json']
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
        yield scrapy.FormRequest(url=url, body=json.dumps(post_data), method='POST', headers=headers)

    def parse(self, response):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        print(json_data)
        client = KafkaClient(hosts="192.168.56.100:9092")
        print(client.topics)
        topic = client.topics['moercredit_log_test']
        with topic.get_sync_producer() as producer:
            for i in range(4):
                producer.produce(bytes('this is message', encoding='utf-8'))
