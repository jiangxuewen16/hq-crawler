# -*- coding: utf-8 -*-
import base64
import json
import time
import zlib
from urllib import parse

import scrapy
from datetime import datetime
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot
from spiders.items.spot.spot import Spot

"""
同程旅游
"""


class LySpider(scrapy.Spider):
    name = 'ly'
    allowed_domains = ['www.ly.com']
    start_urls = ['http://www.ly.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.LY)  # ota 景区id列表

    def parse(self, response):
        pass


class LyCommentSpider(scrapy.Spider):
    name = 'ly_spot'
    allowed_domains = ['www.ly.com']

    page_num = 1  # 总评论
    page_size = 10  # 默认爬取每页10条
    base_url = r'https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx?action=GetDianPingList&sid={ota_spot_id}&page={page_num}&pageSize={page_size}&labId=6&sort=0&iid=0.08141872334931999'
    start_urls = ['https://www.ly.com/scenery/BookSceneryTicket_9513.html']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in LySpider.ota_spot_ids:
            # 更新景区的评论数量
            url = self.base_url.format(ota_spot_id=ota_spot_id, page_num=self.page_num, page_size=self.page_size)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id, 'page_num': self.page_num})

    def parse_item(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        page_num = response.meta['page_num']
        ota_spot_id = response.meta['ota_spot_id']

        total_page = json_data['pageInfo']['totalPage']

        for item  in json_data['dpList']:
            spot_comment = spot.SpotComment()

            spot_comment.ota_id = OTA.OtaCode.LY.value.id
            spot_comment.ota_spot_id = ota_spot_id
            spot_comment.goods_name = item['DPItemName']
            spot_comment.goods_id = item['DPItemId']

            spot_comment.u_name = item['dpUserName']
            spot_comment.u_avatar = item['memberHeaderImgUrl']
            # spot_comment.u_avg_price = item['avgPrice']
            spot_comment.u_level = item['DPUserLevel']

            # spot_comment.c_id = item['reviewId']
            spot_comment.c_content = item['dpContent']
            # spot_comment.c_score = float(item['star'] / 10)
            if not item['dpImgUrl'] is None:
                spot_comment.c_img = [img['imgUrl'] for img in item['dpImgUrl']]
            if not item['csReplyList'] is None:
                spot_comment.c_reply = [reply['replyContent'] for reply in item['csReplyList']]

            spot_comment.create_at = item['dpDate']

            spot_comment.c_useful_num = item['zanCount']
            # spot_comment.c_reply_num = item['replyCnt']
            spot_comment.c_from = '同程网'
            
            yield spot_comment

        if page_num < total_page:
            page_num += 1
            url = self.base_url.format(ota_spot_id=ota_spot_id, page_num=page_num, page_size=self.page_size)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id, 'page_num': page_num})



# class LyCommentSpider(scrapy.Spider):
#     name = 'ly_comment_spot'
#     allowed_domains = ['www.ly.com']
#
#     total_num = 0  # 总评论
#     page_size = 100  # 默认爬取每页100条
#     labId = 1  # 默认爬取全部1：全部  2：好评 3：中评  4：差评 5：有图  6：最新
#     base_url = r'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&page=1&pageSize={page_size}&labId=1&sort=0&iid=0.32116644664605554'
#     start_urls = [
#         'https://www.meituan.com/ptapi/poi/getcomment?id=1515791&offset=0&pageSize=1&mode=0&starRange=&userId=&sortType=0']
#
#     def parse(self, response: HtmlResponse):
#         # 爬取景区列表数据
#         for ota_spot_id in LySpider.ota_spot_ids:
#             # 更新景区的评论数量
#             url = self.base_url.format(spot_id=ota_spot_id, offset=0, page_size=1)
#             yield Request(url=url, callback=self.parse_count, dont_filter=True,
#                           meta={'offset': 0, 'ota_spot_id': ota_spot_id})
#
#     def parse_page(self, response: HtmlResponse):
#         response_str = response.body.decode('utf-8')
#         json_data = json.loads(response_str)
#
#         max_offset = response.meta['max_offset']
#         page_size = response.meta['page_size']
#         ota_spot_id = response.meta['ota_spot_id']
#
#         for item in json_data['dpList']:
#             spot_comment = spot.SpotComment()
#
#             spot_comment.ota_id = OTA.OtaCode.LY.value.id
#             spot_comment.ota_spot_id = ota_spot_id
#             spot_comment.goods_name = item['DPItemName']
#             spot_comment.goods_id = item['DPItemId']
#
#             spot_comment.u_name = item['dpUserName']
#             spot_comment.u_avatar = item['memberHeaderImgUrl']
#             # spot_comment.u_avg_price = item['avgPrice']
#             spot_comment.u_level = item['DPUserLevel']
#
#             spot_comment.c_id = item['reviewId']
#             spot_comment.c_content = item['dpContent']
#             # spot_comment.c_score = float(item['star'] / 10)
#             spot_comment.c_img = [img['dpImgUrl'] for img in item['imgUrl']]
#             spot_comment.c_reply = [img['csReplyList'] for img in item['replyContent']]
#
#             spot_comment.create_at = item['dpDate']
#
#             spot_comment.c_useful_num = item['zanCount']
#             # spot_comment.c_reply_num = item['replyCnt']
#             spot_comment.c_from = '同程网'
#
#             yield spot_comment
#
#         start_offset = response.meta['offset'] + page_size
#         print('============', start_offset, max_offset, page_size)
#         if start_offset < max_offset:
#             url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset,
#                                        page_size=page_size)
#             yield Request(url=url, callback=self.parse_page, dont_filter=True,
#                           meta={'offset': start_offset, 'max_offset': max_offset, 'ota_spot_id': ota_spot_id,
#                                 'page_size': page_size})
#
#     def parse_count(self, response: HtmlResponse):
#         response_str = response.body.decode('utf-8')
#         json_data = json.loads(response_str)
#         ota_spot_id = response.meta['ota_spot_id']
#         new_total = json_data['total']
#         spot_info = spot.Spot.objects(ota_id=OTA.OtaCode.MEITUAN.value.id, ota_spot_id=ota_spot_id)
#         # comment_num = spot_info.comment_num if spot_info and spot_info.comment_num else 0  # 已有的评论数量
#         spot_info.update(set__comment_num=new_total)
#
#         comment_num = spot.SpotComment.objects(ota_id=OTA.OtaCode.MEITUAN.value.id,
#                                                ota_spot_id=ota_spot_id).count()
#
#         new_num = new_total - comment_num
#         if new_num <= 0:  # 没有新评论的情况下不需要做任何处理
#             return
#
#         max_offset = new_num - 1  # 最大能偏移的数量
#         page_size = self.page_size
#         if new_num < self.page_size:  # 新增的评论数量小于默认爬取的最大数量，则用新增的数量作为爬取数量
#             page_size = new_num
#
#         # 爬取景区的所有评论
#         start_offset = 0
#         print('=========增量爬取参数=========', ota_spot_id, new_total, comment_num, max_offset)
#         url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset, page_size=page_size)
#
#         yield Request(url=url, callback=self.parse_page, dont_filter=True,
#                       meta={'offset': start_offset, 'max_offset': max_offset, 'ota_spot_id': ota_spot_id,
#                             'page_size': page_size})
