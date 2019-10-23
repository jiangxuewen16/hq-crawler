import json

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class HqlxSpider(scrapy.Spider):
    name = 'hqlx_order'
    allowed_domains = ['api.huiqulx.com']
    start_urls = ['https://passport.huiqulx.com/index/permission/login']

    def start_requests(self):
        formdata = {
            {"u_name": "18508488575", "pwd": "123456", "app_id": "40", "u_type": "1"}}
        result = Request(self.start_urls[0], method="POST", body=json.dumps(formdata),
                         headers={'Content-Type': 'application/json'},
                         callback=self.parse)
        yield result

    def parse(self, response: HtmlResponse):
        # items = response.css('div.service_c ul li').extract_first()
        print(response.body.decode('utf-8'))
