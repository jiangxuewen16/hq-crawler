# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['www.meituan.com']
    start_urls = ['https://www.meituan.com/']

    def parse(self, response):
        pass


class MeituanSpotSpider(scrapy.Spider):
    name = 'meituan_spot'
    allowed_domains = ['https://www.meituan.com']
    start_urls = ['https://www.meituan.com/zhoubianyou/1515791/']

    def parse(self, response):
        # print('========================', response.body.decode('utf-8'))
        response.css('div.ct-text')


class MeituanCommentSpider(scrapy.Spider):
    name = 'meituan_comment'
    allowed_domains = ['https://www.meituan.com']
    ota_spot_ids = [1515791]
    offset = 0
    page_size = 100  # 默认爬取每页100条
    base_url = r'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&offset={offset}&pageSize={page_size}&mode=0&starRange=&userId=&sortType=0'
    start_urls = ['https://www.meituan.com/zhoubianyou/1515791/']

    def parse(self, response: HtmlResponse):
        # 爬取下一个景区的数据
        for ota_spot_id in self.ota_spot_ids:
            start_offset = 0
            url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset, page_size=self.page_size)
            yield Request(url=url, callback=self.parse_page, dont_filter=True,
                          meta={'offset': start_offset, 'ota_spot_id': ota_spot_id})

    def parse_page(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        for item in json_data['comments']:
            print('====================', item)
            spot_comment = spot.SpotComment()

            spot_comment.ota_id = OTA.OtaCode.MAFENGWO.value.id
            spot_comment.ota_spot_id = response.meta['ota_spot_id']

            spot_comment.u_name = item['userName']
            spot_comment.u_avatar = item['userUrl']
            spot_comment.u_avg_price = item['avgPrice']
            spot_comment.u_avg_price = item['avgPrice']

            spot_comment.c_content = item['comment']
            spot_comment.c_img = [img['url'] for img in item['picUrls']]

            time_local = time.localtime(int(1565587838420 / 1000))
            spot_comment.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
