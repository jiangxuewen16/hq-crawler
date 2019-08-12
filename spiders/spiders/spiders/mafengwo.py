# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from models.spot.spot import Spot

"""
马蜂窝
"""


class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['https://www.mafengwo.cn/poi/339.html']

    def start_requests(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}

        # 指定cookies
        cookies = {}

        # 再次请求到详情页，并且声明回调函数callback，dont_filter=True 不进行域名过滤，meta给回调函数传递数据
        yield Request(url=self.start_urls[0], headers=headers, cookies=cookies, callback=self.parse, dont_filter=True)

    def parse(self, response: HtmlResponse):
        print(11111111111111111111)


class MafengwoSpotSpider(scrapy.Spider):
    name = 'mafengwo_spot'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['https://www.mafengwo.cn/poi/339.html']

    def parse(self, response: HtmlResponse):
        spot = Spot()
        spot.spot_name = response.xpath('/html/body/div[2]/div[2]/div/div[3]/h1/text()').extract_first()
        spot.desc = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/text()').extract_first()
        spot.tel = response.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[1]/div[2]/text()').extract_first()

        yield spot

