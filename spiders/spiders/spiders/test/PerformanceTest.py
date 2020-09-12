# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.price import price
from spiders.items.spot import spot


class OrderCreateSpider(scrapy.Spider):
    name = 'performance-test-order-create'
    allowed_domains = ['www.ctrip.com']
    start_urls = ['https://www.ctrip.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.CTRIP)  # ota 景区id列表

    def parse(self, response: HtmlResponse):
        pass