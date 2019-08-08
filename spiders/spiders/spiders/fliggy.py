# -*- coding: utf-8 -*-
import scrapy

"""
飞猪
"""

class FliggySpider(scrapy.Spider):
    name = 'fliggy'
    allowed_domains = ['https://www.fliggy.com']
    start_urls = ['http://https://www.fliggy.com/']

    def parse(self, response):
        pass
