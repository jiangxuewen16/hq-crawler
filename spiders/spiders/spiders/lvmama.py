# -*- coding: utf-8 -*-
import scrapy


class LvmamaSpider(scrapy.Spider):
    name = 'lvmama'
    allowed_domains = ['http://www.lvmama.com']
    start_urls = ['http://http://www.lvmama.com/']

    def parse(self, response):
        pass
