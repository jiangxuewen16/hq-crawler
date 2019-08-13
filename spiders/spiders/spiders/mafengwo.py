# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse, Response

from spiders.items.spot import spot
from spiders.items.spot.spot import Spot

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
        spot.traffic = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[1]/dd/div[1]/text()').extract_first()
        spot.ticket_num = 1
        spot.open_time = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[3]/dd/text()').extract_first()
        updateTime = response.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/text()').extract_first()
        spot.update_at = updateTime.split('：')[1].split(' ')[0].rstrip()
        spot.comment_num = response.xpath('//*[@data-anchor="commentlist"]/div/div/div[1]/span/em').extract_first()
        yield spot


"""
爬取马蜂窝评论
"""


class MafengwoCommentSpider(scrapy.Spider):
    name = 'mafengwo_comment'
    allowed_domains = ['www.mafengwo.cn']
    time = int(time.time() * 1000)
    spot_id = 339
    page = 2
    start_urls = [
        f'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181022435556804711854_{time}&&params=%7B%22poi_id%22%3A%22{spot_id}%22%2C%22page%22%3A{page}%2C%22just_comment%22%3A1%7D&_ts=1565663067492&_sn=a23eb0cba2&_=1565663067493']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': '*/*',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Referer': 'https://www.mafengwo.cn/poi/339.html'
        }

        # 指定cookies
        cookies = {}

        # 再次请求到详情页，并且声明回调函数callback，dont_filter=True 不进行域名过滤，meta给回调函数传递数据
        yield Request(url=self.start_urls[0], headers=headers, cookies=cookies, callback=self.parse, dont_filter=True)

    def parse(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        response_str = response_str.split('(', 1)[1].rstrip(');')
        json_data = json.loads(response_str)

        comment_count = json_data['data']['controller_data']['comment_count']

        selector = Selector(text=json_data['data']['html'])
        items = selector.css('.rev-list > ul li')
        for item in items:
            spot_comment = spot.SpotComment()
            spot_comment.ota_type = 123
            spot_comment.u_space = item.css('.avatar::attr(href)').extract_first()
            spot_comment.u_id = int(spot_comment.u_space.lstrip('/u/').rstrip('.html'))
            spot_comment.u_avatar = item.css('.avatar img::attr(src)').extract_first()
            spot_comment.u_level = item.css('.level::text').extract_first()
            spot_comment.u_name = item.css('.name::text').extract_first()

            spot_comment.c_id = item.css('.useful::attr(data-id)').extract_first()
            score = item.css('.s-star::attr(class)').extract_first()
            spot_comment.c_score = score.split(' ')[1][-1]
            spot_comment.c_useful_num = item.css('.useful-num::text').extract_first()
            spot_comment.c_content = item.css('.rev-txt::text').extract_first()
            spot_comment.c_img = item.css('.rev-img img::attr(src)').extract()
            spot_comment.c_from = item.css('.from a::text').extract_first()
            spot_comment.c_from = item.css('.from a::text').extract_first()
            spot_comment.create_at = item.css('.time::text').extract_first()

            yield spot_comment

        selector.css('.count')
