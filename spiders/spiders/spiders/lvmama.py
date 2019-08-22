# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot
from spiders.items.spot.spot import Spot


class LvmamaSpider(scrapy.Spider):
    name = 'lvmama'
    allowed_domains = ['http://www.lvmama.com']
    start_urls = ['http://www.lvmama.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.LVMAMA)  # ota 景区id列表

    def parse(self, response):
        pass


class LvmamaSpotSpider(scrapy.Spider):
    name = 'lvmama_spot'
    allowed_domains = ['www.lvmama.com']
    base_url = r'http://ticket.lvmama.com/scenic-{ota_spot_id}?dropdownlist=true'
    start_urls = ['http://ticket.lvmama.com/scenic-100025?dropdownlist=true']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in LvmamaSpider.ota_spot_ids:
            # 获取景区页面数据
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.LVMAMA.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()

        # 不存在数据则新增数据
        if not spot_data:
            spot_data = Spot()

        spot_data.spot_id = OTA.OtaSpotIdMap.get_ota_spot_id(OTA.OtaSpotIdMap.SHI_YAN_HU.name, OTA.OtaCode.HUIQULX)
        spot_data.ota_id = OTA.OtaCode.LVMAMA.value.id
        spot_data.ota_spot_id = response.meta['ota_spot_id']
        spot_data.spot_name = response.xpath('//body/div[4]/div/div[2]/div/div/h1/text()').extract_first()
        spot_data.spot_score = float(
            response.xpath('//*[@id="comments"]/div[2]/div[1]/div/div[1]/i/text()').extract_first())
        spot_data.comment_num = float(
            response.xpath('//*[@id="comments"]/div[2]/div[1]/div/div[1]/em[2]/a/text()').extract_first())
        spot_data.spot_favorable = response.xpath('//*[@id="comments"]/div[2]/div[1]/div/div[1]/em[1]/text()') \
            .extract_first()
        spot_data.open_time = response.xpath(
            '/html/body/div[4]/div/div[2]/div[2]/div[2]/div/div/dl[2]/dd/p/text()').extract_first()
        spot_data.traffic = response.xpath(
            '//*[@id="traffic"]/div[2]/div[2]//p/text()').extract()

        yield spot_data


class LvmamaCommentSpider(scrapy.Spider):
    name = 'lvmama_comment'
    allowed_domains = ['http://www.lvmama.com/']

    total_num = 0  # 总评论
    page_size = 100  # 默认爬取每页100条
    base_url = r'http://ticket.lvmama.com/vst_front/comment/newPaginationOfComments?type=all&currentPage=' \
               r'{currentPage}&totalCount={totalCount}&placeId={ota_spot_id}&productId=&placeIdType=PLACE&isPicture=&' \
               r'isBest=&isPOI=Y&isELong=N'
    comment_num_url = r'http://ticket.lvmama.com/scenic-{ota_spot_id}?dropdownlist=true'
    start_urls = [
        'http://ticket.lvmama.com/vst_front/comment/newPaginationOfComments?type=all&currentPage=1&totalCount=361&plac'
        'eId=100025&productId=&placeIdType=PLACE&isPicture=&']

    def parse(self, response: HtmlResponse):

        # 爬取下一个景区的数据
        for ota_spot_id in LvmamaSpider.ota_spot_ids:

            # 更新景区的评论数量 增量爬取
            url = self.comment_num_url.format(ota_spot_id=str(ota_spot_id))
            yield Request(url=url, callback=self.parse_count, dont_filter=True,
                          meta={'offset': 0, 'ota_spot_id': ota_spot_id})
            # 爬取所有的
            # url = self.base_url.format(ota_spot_id=ota_spot_id, currentPage=start_page,
            #                            totalCount=spot_data.comment_num)
            # page_total = spot_data.comment_num % 10  # 共有多少页
            # if page_total != 0:
            #     page_total = 1 + spot_data.comment_num / 10
            # else:
            #     page_total = spot_data.comment_num / 10
            # yield Request(url=url, callback=self.parse_page, dont_filter=True,
            #               meta={'ota_spot_id': ota_spot_id, 'page_size': page_total, 'max_offset': spot_data.comment_num,
            #                     'now_offset': 1, 'now_size': 1})

    def parse_page(self, response: HtmlResponse):

        now_offset = response.meta['now_offset']  # 当前查询数量
        now_size = response.meta['now_size']  # 当前查询页数
        max_offset = response.meta['max_offset']  # 最大查询数量
        page_size = response.meta['page_size']  # 最大查询页数

        items = response.css('.comment-li')
        page_num = response.css('.nextpage::attr(href)').extract_first()

        for item in items:
            if int(now_offset) > int(max_offset):
                break
            now_offset += 1
            c_id = item.css('.com-answer-submit::attr(data-cid)').extract_first()  # 评论id
            spot_comment = spot.SpotComment.objects(ota_id=OTA.OtaCode.LVMAMA.value.id,
                                                    ota_spot_id=response.meta['ota_spot_id'],
                                                    c_id=c_id).first()
            # 存在不需要新增
            if spot_comment:
                continue
            spot_comment = spot.SpotComment()
            spot_comment.c_id = c_id  # 评论id

            spot_comment.ota_id = OTA.OtaCode.LVMAMA.value.id
            spot_comment.ota_spot_id = response.meta['ota_spot_id']
            spot_comment.u_name = item.css('.com-userinfo a::text').extract()[2]
            spot_comment.c_tag = item.css('.ufeed-item em::text').extract()

            score = item.css('.ufeed-item i::text').extract()
            score_num = 0
            score_total = 0
            for score_rs in score:
                score_total += float(score_rs[0:1])
                score_num += 1
            if score_num == 0:
                spot_comment.c_score = 0
            else:
                spot_comment.c_score = score_total / score_num
            useful_reply_num = item.css('.com-userinfo a em::text').extract()
            spot_comment.c_useful_num = useful_reply_num[0]
            spot_comment.c_reply_num = useful_reply_num[1]
            spot_comment.c_content = item.css('.ufeed-content::text').extract()[1].strip()
            spot_comment.c_img = item.css('.compic-small ul li img::attr(src)').extract()
            spot_comment.c_from = item.css('.com-userinfo span::text').extract_first()
            spot_comment.create_at = item.css('.com-userinfo em::text').extract()[2]
            spot_comment.goods_name = item.css('.com-proTit::text').extract_first()
            yield spot_comment

        page_num = response.css('.nextpage::attr(href)').extract_first()

        page_num = page_num.split('(', 1)[1].rstrip(');').replace("'", '"').replace("{", '{"').replace(":", '":') .replace(',', ',"')  # 下一页
        json_data = json.loads(page_num)
        page = json_data['currentPage']
        if page and now_size < page_size:
            now_size += 1
            url = self.base_url.format(ota_spot_id=response.meta['ota_spot_id'], currentPage=page,
                                       totalCount=json_data['totalCount'])  # 下一页参数

            yield Request(url=url, callback=self.parse_page, dont_filter=True, meta=dict(ota_spot_id=response.
                                                                                         meta['ota_spot_id'],
                                                                                         page_size=page_size,
                                                                                         max_offset=max_offset,
                                                                                         now_offset=now_offset,
                                                                                         now_size=now_size))

    def parse_count(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        new_total = int(
            response.xpath('//*[@id="comments"]/div[2]/div[1]/div/div[1]/em[2]/a/text()').extract_first())
        totalCount = spot.SpotComment.objects(ota_id=OTA.OtaCode.LVMAMA.value.id, ota_spot_id=ota_spot_id).count()  # 当前已有评论数
        new_num = new_total - totalCount  # 新增评论数

        if new_num == 0:  # 没有新评论的情况下不需要做任何处理
            return

        if new_num < 10:
            page_total = 1
        else:
            page_total = new_num % 10  # 新增评论页

            if page_total != 0:
                page_total = 1 + (new_num-page_total) / 10
            else:
                page_total = new_num / 10
        page_total = int(page_total)
        # 爬取景区的所有评论

        start_page = 1
        print('=========增量爬取参数=========', ota_spot_id, new_total, new_num, start_page)
        url = self.base_url.format(ota_spot_id=ota_spot_id, currentPage=start_page, totalCount=new_num)
        yield Request(url=url, callback=self.parse_page, dont_filter=True,
                      meta={'ota_spot_id': ota_spot_id, 'page_size': page_total, 'max_offset': new_num,
                            'now_offset': 1, 'now_size': 1})
