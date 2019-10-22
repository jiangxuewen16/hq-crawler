import json

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class HqlxSpider(scrapy.Spider):
    name = 'hqlx_order'
    allowed_domains = ['api.huiqulx.com']
    start_urls = ['https://api.huiqulx.com/release/user/user/test']

    def start_requests(self):
        formdata = {
            "head": {"token": "", "time": 1563965531895, "version": "1.0", "platform": "43", "excode": "", "qrcode": "",
                     "recode": ""}, "data": {}}
        yield Request(self.start_urls[0], method="POST", body=json.dumps(formdata),
                      headers={'Content-Type': 'application/json'},
                      callback=self.parse)

    def parse(self, response: HtmlResponse):
        # items = response.css('div.service_c ul li').extract_first()
        print(response.body.decode('utf-8'))
