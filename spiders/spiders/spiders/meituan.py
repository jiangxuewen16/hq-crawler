# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot
from spiders.items.spot.spot import Spot


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['www.meituan.com']
    start_urls = ['https://www.meituan.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.MEITUAN)  # ota 景区id列表

    def parse(self, response):
        pass


class MeituanSpotSpider(scrapy.Spider):
    name = 'meituan_spot'
    allowed_domains = ['www.meituan.com']
    base_url = r'https://www.meituan.com/zhoubianyou/{ota_spot_id}'
    start_urls = ['https://www.meituan.com/zhoubianyou/1515791']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in MeituanSpider.ota_spot_ids:
            # 更新景区的评论数量
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.MEITUAN.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()

        # 不存在数据则新增数据
        if not spot_data:
            spot_data = Spot()
        spot_data.spot_name = response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/h1/text()').extract_first()
        spot_data.spot_score = float(
            response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[1]/span/text()[1]').extract_first())
        spot_data.avg_price = float(
            response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[1]/span/span/text()[2]').extract_first())
        spot_data.addr = response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[1]/a/span/text()').extract_first()
        spot_data.tel = response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[2]/span[2]/text()').extract_first()

        yield spot_data


class MeituanCommentSpider(scrapy.Spider):
    name = 'meituan_comment'
    allowed_domains = ['www.meituan.com']

    total_num = 0  # 总评论
    page_size = 100  # 默认爬取每页100条
    base_url = r'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&offset={offset}&pageSize={page_size}&mode=0&starRange=&userId=&sortType=0'
    start_urls = [
        'https://www.meituan.com/ptapi/poi/getcomment?id=1515791&offset=0&pageSize=1&mode=0&starRange=&userId=&sortType=0']

    def parse(self, response: HtmlResponse):

        # 爬取景区列表数据
        for ota_spot_id in MeituanSpider.ota_spot_ids:
            # 更新景区的评论数量
            url = self.start_urls[0]
            yield Request(url=url, callback=self.parse_count, dont_filter=True,
                          meta={'offset': 0, 'ota_spot_id': ota_spot_id})

    def parse_page(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        max_offset = response.meta['max_offset']
        page_size = response.meta['page_size']
        ota_spot_id = response.meta['ota_spot_id']

        for item in json_data['comments']:
            spot_comment = spot.SpotComment()

            spot_comment.ota_id = OTA.OtaCode.MEITUAN.value.id
            spot_comment.ota_spot_id = ota_spot_id
            spot_comment.goods_name = item['menu']
            spot_comment.goods_id = item['did']

            spot_comment.u_name = item['userName']
            spot_comment.u_avatar = item['userUrl']
            spot_comment.u_avg_price = item['avgPrice']
            spot_comment.u_avg_price = item['avgPrice']
            spot_comment.u_level = item['userLevel']

            spot_comment.c_id = item['reviewId']
            spot_comment.c_content = item['comment']
            spot_comment.c_score = float(item['star'] / 10)
            spot_comment.c_img = [img['url'] for img in item['picUrls']]

            time_local = time.localtime(int(int(item['commentTime']) / 1000))
            spot_comment.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

            spot_comment.c_useful_num = item['zanCnt']
            spot_comment.c_reply_num = item['replyCnt']
            spot_comment.c_from = '美团网'

            yield spot_comment

        start_offset = response.meta['offset'] + page_size
        print('============', start_offset, max_offset, page_size)
        if start_offset < max_offset:
            url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset,
                                       page_size=page_size)
            yield Request(url=url, callback=self.parse_page, dont_filter=True,
                          meta={'offset': start_offset, 'max_offset': max_offset, 'ota_spot_id': ota_spot_id,
                                'page_size': page_size})

    def parse_count(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        ota_spot_id = response.meta['ota_spot_id']
        new_total = json_data['total']
        spot_info = spot.Spot.objects(ota_id=OTA.OtaCode.MEITUAN.value.id, ota_spot_id=ota_spot_id)
        comment_num = spot_info.comment_num if spot_info and spot_info.comment_num else 0  # 已有的评论数量
        spot_info.update(set__comment_num=new_total)

        new_num = new_total - comment_num
        if new_num == 0:  # 没有新评论的情况下不需要做任何处理
            return

        max_offset = new_num - 1  # 最大能偏移的数量
        page_size = self.page_size
        if new_num < self.page_size:  # 新增的评论数量小于默认爬取的最大数量，则用新增的数量作为爬取数量
            page_size = new_num

        # 爬取景区的所有评论
        start_offset = 0
        url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset, page_size=page_size)

        yield Request(url=url, callback=self.parse_page, dont_filter=True,
                      meta={'offset': start_offset, 'max_offset': max_offset, 'ota_spot_id': ota_spot_id,
                            'page_size': page_size})
