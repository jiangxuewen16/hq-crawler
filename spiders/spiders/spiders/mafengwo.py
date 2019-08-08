# -*- coding: utf-8 -*-
import scrapy

"""
马蜂窝
"""

class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['https://www.mafengwo.cn']
    start_urls = ['http://https://www.mafengwo.cn']

    def parse(self, response):
        pass
