# -*- coding: utf-8 -*-
import json
import time

import math
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.items.spot import spot
from spiders.common import OTA

"""
飞猪
"""


class FliggySpider(scrapy.Spider):
    name = 'fliggy'
    allowed_domains = ['www.fliggy.com']
    start_urls = ['https://www.fliggy.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.FLIGGY)  # ota 景区id列表

    def parse(self, response):
        pass


class FliggySpotSpider(scrapy.Spider):
    name = 'fliggy_spot'
    allowed_domains = ['www.fliggy.com']
    base_url = r'https://traveldetail.fliggy.com/item.htm?id={ota_spot_id}&spm=181.7395991.1998089960.2.122d2405nqRYtu&expiredate='
    start_urls = ['https://traveldetail.fliggy.com/item.htm?id=556487712203']

    def parse(self, response: HtmlResponse):
        pass


class FliggyCommentSpider(scrapy.Spider):
    name = 'fliggy_comment'
    allowed_domains = ['www.fliggy.com']

    total_num = 0  # 总评论
    page_size = 20  # 默认爬取每页20条
    base_url = r'https://traveldetail.fliggy.com/async/queryRateList.do?id={ota_spot_id}&tagId=:0&pageNo={page_no}&sort=1&pageSize={page_size}'
    start_urls = [
        'https://traveldetail.fliggy.com/async/queryRateList.do?id={ota_spot_id}&tagId=:0&pageNo=1&sort=1&pageSize=1'
    ]

    def parse(self, response):
        # 爬取景区列表数据
        for ota_spot_id in FliggySpider.ota_spot_ids:
            for ota_child_spot_id in ota_spot_id:
                # 更新景区的评论数量
                url = self.start_urls[0].format(ota_spot_id=ota_child_spot_id)
                headers = {
                    'referer': FliggySpotSpider.base_url.format(ota_spot_id=ota_child_spot_id)
                }
                yield Request(url=url, callback=self.parse_count, dont_filter=True, headers=headers,
                              meta={'ota_spot_id': ota_child_spot_id, 'page_no': 1, 'page_size': self.page_size})

    def parse_page(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        ota_spot_id = response.meta['ota_spot_id']
        page_no = response.meta['page_no']
        page_size = response.meta['page_size']
        new_num = response.meta['new_num']
        comment = json_data['module']['rateList']['rateCellList']
        if page_size == 0:
            count_page = 0
        else:
            count_page = math.ceil(new_num / page_size)
        if comment is None:
            return
        for item in comment:
            spot_comment = spot.SpotComment()
            spot_comment.ota_id = OTA.OtaCode.FLIGGY.value.id
            spot_comment.ota_spot_id = ota_spot_id
            spot_comment.goods_name = item['skuInfo']
            spot_comment.u_avatar = item['userAvatar']
            spot_comment.u_name = item['userNick']
            spot_comment.c_id = item['rateId']
            spot_comment.c_content = item['rateContent']
            spot_comment.c_img = item['picList']
            spot_comment.create_at = item['rateDate']
            spot_comment.c_reply_content = item['reply']
            spot_comment.c_from = '飞猪'
            yield spot_comment
        time.sleep(1)
        page_no = page_no + 1
        if count_page >= page_no:
            if count_page == page_no:
                page_size = new_num % page_size
            url = self.base_url.format(ota_spot_id=ota_spot_id, page_no=page_no, page_size=page_size)
            headers = {
                'referer': FliggySpotSpider.base_url.format(ota_spot_id=ota_spot_id)
            }
            yield Request(url=url, callback=self.parse_page, dont_filter=True, headers=headers,
                          meta={'ota_spot_id': ota_spot_id, 'page_no': page_no, 'page_size': page_size,
                                'new_num': new_num})

    def parse_count(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        ota_spot_id = response.meta['ota_spot_id']
        page_no = response.meta['page_no']
        page_size = response.meta['page_size']
        if json_data['module'] == {}:
            return
        new_total = json_data['module']['rateList']['total']
        comment_num = spot.SpotComment.objects(ota_id=OTA.OtaCode.FLIGGY.value.id, ota_spot_id=ota_spot_id).count()

        new_num = new_total - comment_num
        print('=========增量爬取参数=========', ota_spot_id, new_total, comment_num, page_no)
        if new_num <= 0:  # 没有新评论的情况下不需要做任何处理
            return
        # 爬取景区的所有评论
        if new_num <= page_size:
            page_size = new_num
        url = self.base_url.format(ota_spot_id=ota_spot_id, page_no=page_no, page_size=page_size)
        headers = {
            'referer': FliggySpotSpider.base_url.format(ota_spot_id=ota_spot_id)
        }
        yield Request(url=url, callback=self.parse_page, dont_filter=True, headers=headers,
                      meta={'ota_spot_id': ota_spot_id, 'page_no': page_no, 'page_size': page_size, 'new_num': new_num})
