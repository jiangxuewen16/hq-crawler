# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import HtmlResponse
from scrapy import Request

from spiders.common import OTA
from spiders.items.spot import spot


class QunarSpider(scrapy.Spider):
    name = 'qunar'
    allowed_domains = ['www.qunar.com']
    start_urls = ['http://www.qunar.com/']

    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.QUNAR)  # ota 景区id列表

    def parse(self, response):
        pass


# class QunarSpotSpider(scrapy.Spider):
#     name = 'qunar_spot'
#     allowed_domains = ['www.meituan.com']
#     base_url = r'https://www.meituan.com/zhoubianyou/{ota_spot_id}'
#     start_urls = ['https://www.meituan.com/zhoubianyou/1515791']
#
#     def parse(self, response: HtmlResponse):
#         base_url = r'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize={page_size}&fromType=SIGHT&pageNum={page_num}&sightId={ota_spot_id}&tagType=44&tagName=%E6%9C%80%E6%96%B0'
#         start_urls = [
#             'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=1&fromType=SIGHT&pageNum=1&sightId=706176810']


class QunarCommentSpider(scrapy.Spider):
    name = 'qunar_comment'
    allowed_domains = ['www.meituan.com']

    total_num = 0  # 总评论
    page_size = 20  # 默认爬取每页100条
    base_url = r'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize={page_size}&fromType=SIGHT&pageNum={page_num}&sightId={ota_spot_id}&tagType=44&tagName=%E6%9C%80%E6%96%B0'
    start_urls = [
        'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=1&fromType=SIGHT&pageNum=1&sightId=706176810']

    def parse(self, response: HtmlResponse):

        # 爬取景区列表数据
        for ota_spot_id in QunarSpider.ota_spot_ids:
            # 更新景区的评论数量
            url = self.base_url.format(ota_spot_id=ota_spot_id, page_num=1, page_size=1)
            yield Request(url=url, callback=self.spot_tag, dont_filter=True,
                          meta={'page_num': 1, 'ota_spot_id': ota_spot_id})

    """获取景区用户点评标签"""
    def spot_tag(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        comment = json.loads(response_str)

        if 'data' in comment and 'tagList' in comment['data']:
            spot_tag = [item['tagName'] for item in comment['data']['tagList']]
            spot.Spot.objects(ota_id=OTA.OtaCode.QUNAR.value.id,
                              ota_spot_id=ota_spot_id).update(
                set__tag_list=spot_tag)


    def parse_count(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        comment_list = json.loads(response_str)

        page = response.meta['page_num']
        ota_spot_id = response.meta['ota_spot_id']

        for item in comment_list:
            spot_comment = spot.SpotComment()

            spot_comment.
