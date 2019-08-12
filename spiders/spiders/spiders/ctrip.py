# -*- coding: utf-8 -*-

from core.lib import spider

"""
携程
"""


class CtripSpider(spider.BaseSpider):
    name = 'ctrip'
    allowed_domains = ['https://www.ctrip.com']
    start_urls = ['http://https://www.ctrip.com/']

    def parse(self, response):
        self.logger.debug(response.text)
