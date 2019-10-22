# -*- coding: utf-8 -*-
import scrapy


class LySpider(scrapy.Spider):
    name = 'ly'
    allowed_domains = ['www.ly.com']
    start_urls = ['http://www.ly.com/']

    def parse(self, response):
        pass
