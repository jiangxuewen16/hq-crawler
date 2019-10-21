# -*- coding: utf-8 -*-
import scrapy


class QunarSpider(scrapy.Spider):
    name = 'qunar'
    allowed_domains = ['www.qunar.com']
    start_urls = ['http://www.qunar.com/']

    def parse(self, response):
        pass
