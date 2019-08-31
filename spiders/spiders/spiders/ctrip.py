# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot


class CtripSpider(scrapy.Spider):
    name = 'ctrip'
    allowed_domains = ['www.ctrip.com']
    start_urls = ['https://www.ctrip.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.CTRIP)  # ota 景区id列表

    def parse(self, response: HtmlResponse):
        pass


"""
景区数据
"""


class CtripSpotSpider(scrapy.Spider):
    name = 'ctrip_spot'
    allowed_domains = ['www.ctrip.com']
    base_url = r'https://piao.ctrip.com/ticket/dest/t{ota_spot_id}.html'
    start_urls = ['https://piao.ctrip.com/ticket/dest/t62931.html']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in CtripSpider.ota_spot_ids:
            # 获取景区页面数据
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    # 统计评论，增量爬取
    def parse_count(self, response: HtmlResponse):
        pass

    def parse_item(self, response: HtmlResponse):
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.CTRIP.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()

        # 不存在数据则新增数据
        if not spot_data:
            spot_data = spot.Spot()

        # todo:相关数据

        yield spot_data


"""
景区评论数据
"""


class CtripCommentSpider(scrapy.Spider):
    name = 'ctrip_spot'
    allowed_domains = ['www.ctrip.com', 'sec-m.ctrip.com']
    start_urls = ['https://sec-m.ctrip.com/restapi/soa2/12530/json/viewCommentList']

    def start_requests(self):
        json_data = {"pageid": 10650000804, "viewid": 62931, "tagid": -11, "pagenum": 1, "pagesize": 10,
                    "contentType": "json",
                    "head": {"appid": "100013776", "cid": "09031111211651836922", "ctok": "", "cver": "1.0",
                             "lang": "01", "sid": "8888", "syscode": "09", "auth": "",
                             "extension": [{"name": "protocal", "value": "https"}]}, "ver": "7.10.3.0319180000"}
        yield Request(self.start_urls[0], method="POST", body=json.dumps(json_data),
                      headers={'Content-Type': 'application/json'},
                      callback=self.parse)

    def parse(self, response: HtmlResponse):
        for ota_spot_id in CtripSpider.ota_spot_ids:
            # 获取景区页面数据
            yield Request(url=self.start_urls[0], callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):

