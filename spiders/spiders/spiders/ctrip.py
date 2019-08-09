# -*- coding: utf-8 -*-
import scrapy

"""
携程
"""


class CtripSpider(scrapy.Spider):
    name = 'ctrip'
    allowed_domains = ['https://www.ctrip.com']
    start_urls = ['http://https://www.ctrip.com/']

    def parse(self, response):
        pass
