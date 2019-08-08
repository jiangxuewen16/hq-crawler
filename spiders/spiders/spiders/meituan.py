# -*- coding: utf-8 -*-
import scrapy


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['https://www.meituan.com']
    start_urls = ['http://https://www.meituan.com/']

    def parse(self, response):
        pass
