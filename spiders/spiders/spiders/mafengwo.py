# -*- coding: utf-8 -*-
import json
import time
from collections import namedtuple

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.price import price
from spiders.items.spot import spot
from spiders.items.spot.spot import Spot

"""
马蜂窝 todo:暂时不要爬
"""


class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['https://www.mafengwo.cn/poi/339.html']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.MAFENGWO)  # ota 景区id列表

    base_score_url = r'https://m.mafengwo.cn/poi/comment_{spot_ota_id}.html'

    @classmethod
    def build_headers(cls, referer: str) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': '*/*',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Referer': referer
        }

    def parse(self, response: HtmlResponse):
        pass


"""
马蜂窝景区数据
"""

# todo 景区用城市景区的
# class MafengwoSpotSpider(scrapy.Spider):
#     name = 'mafengwo_spot'
#     allowed_domains = ['www.mafengwo.cn']
#     base_url = r'https://www.mafengwo.cn/poi/{ota_spot_id}.html'
#     start_urls = ['https://www.mafengwo.cn/poi/339.html']
#
#     def parse(self, response: HtmlResponse):
#         for ota_spot_id in MafengwoSpider.ota_spot_ids:
#             start_page = 1
#             url = self.base_url.format(ota_spot_id=ota_spot_id)
#             referer = 'https://www.mafengwo.cn/poi/339.html'  # 这里随便马蜂窝任何url
#             yield Request(url=url, headers=MafengwoSpider.build_headers(referer), cookies={},
#                           callback=self.parse_item,
#                           dont_filter=True, meta={'page': start_page, 'ota_spot_id': ota_spot_id})
#
#     def parse_item(self, response: HtmlResponse):
#         spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id,
#                                       ota_spot_id=response.meta['ota_spot_id']).first()
#         # 不存在数据则新增数据
#         if not spot_data:
#             spot_data = Spot()
#             spot_data.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#         # spot_data.spot_id = OTA.OtaSpotIdMap.get_ota_spot_id(OTA.OtaSpotIdMap.SHI_YAN_HU.name, OTA.OtaCode.HUIQULX)       这里没什么用，到时候给及其学习来做匹配
#         spot_data.ota_spot_id = response.meta['ota_spot_id']
#
#         spot_data.ota_id = OTA.OtaCode.MAFENGWO.value.id
#         spot_data.spot_name = response.xpath('/html/body/div[2]/div[2]/div/div[3]/h1/text()').extract_first()
#         desc = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/text()').extract_first()
#         spot_data.desc = desc.strip() if desc else ''
#         spot_data.tel = response.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[1]/div[2]/text()').extract_first()
#         spot_data.traffic = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[1]/dd/div[1]/text()').extract_first()
#         spot_data.ticket_num = 1
#         spot_data.open_time = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[3]/dd/text()').extract_first()
#         spot_data.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         #spot_data.comment_num = \
#         #    response.xpath('//*[@id="poi-navbar"]/ul/li[3]/a/span/text()').extract_first().split('条')[0].strip('（')
#
#         yield spot_data


"""
爬取马蜂窝评论
注意：马蜂窝评论最多只显示5页（每页15条）共75条，不支持时间排序，无法做增量爬取，建议做全爬取
"""


class MafengwoCommentSpider(scrapy.Spider):
    spot_page = namedtuple('spot_page', 'page ota_spot_id ')
    name = 'mafengwo_comment'
    allowed_domains = ['www.mafengwo.cn']
    time = int(time.time() * 1000)
    base_url = r'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181022435556804711854_{time}&&params=%7B%22poi_id%22%3A%22{spot_id}%22%2C%22page%22%3A{page}%2C%22just_comment%22%3A1%7D&_ts=1565663067492&_sn=a23eb0cba2&_=1565663067493'
    start_urls = ['https://www.mafengwo.cn/poi/339.html']

    base_referer = r'https://www.mafengwo.cn/poi/{ota_spot_id}.html'

    cookies = {}

    def start_requests(self):
        # 再次请求到详情页，并且声明回调函数callback，dont_filter=True 不进行域名过滤，meta给回调函数传递数据
        referer = 'https://www.mafengwo.cn/poi/339.html'
        yield Request(url=self.start_urls[0], headers=MafengwoSpider.build_headers(referer), cookies=self.cookies,
                      callback=self.parse,
                      dont_filter=True)

    def parse(self, response: HtmlResponse):
        # 爬取下一个景区的数据
        for ota_spot_id in MafengwoSpider.ota_spot_ids:
            # 更新景区评分
            url = MafengwoSpider.base_score_url.format(spot_ota_id=ota_spot_id)
            yield Request(url=url, callback=self.set_spot_score, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

            # 更新景区的评论数量
            url = self.base_referer.format(ota_spot_id=str(ota_spot_id))
            yield Request(url=url, callback=self.parse_count, dont_filter=True,
                          meta={'offset': 0, 'ota_spot_id': ota_spot_id})

            start_page = 1
            url = self.base_url.format(time=self.time, spot_id=ota_spot_id, page=start_page)
            referer = self.base_referer.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, headers=MafengwoSpider.build_headers(referer), cookies=self.cookies,
                          callback=self.parse_page,
                          dont_filter=True, meta={'page': start_page, 'ota_spot_id': ota_spot_id})

    def parse_page(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        response_str = response_str.split('(', 1)[1].rstrip(');')
        json_data = json.loads(response_str)

        # comment_count = json_data['data']['controller_data']['comment_count']

        selector = Selector(text=json_data['data']['html'])
        items = selector.css('.rev-list > ul li.comment-item')
        for item in items:
            c_id = item.css('.useful::attr(data-id)').extract_first()  # 评论id
            spot_comment = spot.SpotComment.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id,
                                                    ota_spot_id=response.meta['ota_spot_id'],
                                                    c_id=c_id).first()

            # 存在不需要新增
            if spot_comment:
                continue

            spot_comment = spot.SpotComment()
            spot_comment.c_id = c_id  # 评论id

            spot_comment.ota_id = OTA.OtaCode.MAFENGWO.value.id
            spot_comment.ota_spot_id = response.meta['ota_spot_id']
            spot_comment.u_url = item.css('.avatar::attr(href)').extract_first()
            spot_comment.u_id = int(spot_comment.u_url.lstrip('/u/').rstrip('.html'))
            spot_comment.u_avatar = item.css('.avatar img::attr(src)').extract_first()
            spot_comment.u_level = item.css('.level::text').extract_first()
            spot_comment.u_name = item.css('.name::text').extract_first()

            score = item.css('.s-star::attr(class)').extract_first()
            spot_comment.c_score = float(score.split()[1][-1])

            spot_comment.c_useful_num = item.css('.useful-num::text').extract_first()
            spot_comment.c_content = item.css('.rev-txt::text').extract_first()
            spot_comment.c_img = item.css('.rev-img img::attr(src)').extract()
            spot_comment.c_from = item.css('.from a::text').extract_first()
            spot_comment.c_from = item.css('.from a::text').extract_first()
            spot_comment.create_at = item.css('.time::text').extract_first()
            # print('=====================', response.meta['ota_spot_id'])
            yield spot_comment

        # 当前景区分页爬取
        page_num = selector.css('.count span:nth-child(1)::text').extract_first()

        page = response.meta['page']
        ota_spot_id = response.meta['ota_spot_id']
        if page_num and page < int(page_num):
            page += 1
            url = self.base_url.format(time=self.time, spot_id=ota_spot_id, page=page)

            referer = self.base_referer.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, headers=MafengwoSpider.build_headers(referer), cookies=self.cookies,
                          callback=self.parse_page, dont_filter=True,
                          meta={'page': page, 'ota_spot_id': ota_spot_id})

    # 更新景区评论数量
    def parse_count(self, response: HtmlResponse):
        comment_count = response.xpath('//*[@id="poi-navbar"]/ul/li[3]/a/span/text()').extract_first().split('条')[
            0].strip('（')
        spot.Spot.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id,
                          ota_spot_id=response.meta['ota_spot_id']).update(
            set__comment_num=comment_count)

    # 更新景区评分
    def set_spot_score(self, response: HtmlResponse):
        score = response.xpath('/html/body/div[2]/section[1]/div[1]/div[1]/div[1]/strong/text()').extract_first()
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()
        spot_data.spot_score = float(score) if score else 0

        yield spot_data


class MafengwoCitySpot(scrapy.Spider):
    name = 'mafengwo_city_spot'
    allowed_domains = ['www.mafengwo.cn']
    base_url = r'http://www.mafengwo.cn/sales/{ota_spot_id}.html'
    start_urls = ['http://www.mafengwo.cn/sales/2272257.html']

    base_referer = r'http://www.mafengwo.cn/sales/{ota_spot_id}.html'

    spot_ota_list = [2272257, ]

    cookies = {}

    def start_requests(self):
        # 再次请求到详情页，并且声明回调函数callback，dont_filter=True 不进行域名过滤，meta给回调函数传递数据
        referer = 'https://www.mafengwo.cn/poi/339.html'
        yield Request(url=self.start_urls[0], headers=MafengwoSpider.build_headers(referer), cookies=self.cookies,
                      callback=self.parse,
                      dont_filter=True)

    def parse(self, response: HtmlResponse):
        for ota_spot_id in self.spot_ota_list:
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, dont_filter=True, callback=self.parse_spot, meta={'ota_spot_id': ota_spot_id})

    def parse_spot(self, response: HtmlResponse):
        # print(response.body.decode('utf-8'))
        ota_spot_id = response.meta['ota_spot_id']
        # spot_city = spot.SpotCity.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id, ota_spot_id=ota_spot_id).first()
        # if not spot_city:
        #     spot_city = spot.SpotCity()
        #     spot_city.ota_id = OTA.OtaCode.MAFENGWO.value.id
        #     spot_city.ota_spot_id = ota_spot_id
        #     spot_city.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #
        # spot_city.s_name = response.css('.sales-title > h1::text').extract_first()
        # spot_city.city_name = response.css(
        #     'div.container > div.wrapper > div.crumb > div:nth-child(2) > a::text').extract_first()

        o_price = price.OPrice.objects(ota_spot_id=ota_spot_id, ota_id=OTA.OtaCode.MAFENGWO.value.id).first()
        if not o_price:
            o_price = price.OPrice()
            o_price.ota_id = OTA.OtaCode.MAFENGWO.value.id
            o_price.ota_spot_name = response.css('div.sales-title > h1::text').extract_first()
            o_price.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            o_price.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        ota_product = []
        ticket_dom = response.css('.ticket-info > tbody')
        for item in ticket_dom:

            product_item = {}
            type_key = item.css('td.ticket-type.adult-ticket.folded::text').extract_first()
            tr_list = item.css('.ticket-item')
            for tr in tr_list:
                product_item['type_id'] = tr.css('.tobuy-btn > span::attr(data-id)').extract_first()
                product_item['type_key'] = type_key
                product_item['type_name'] = item.css('td.ticket-name::text').extract_first()
                product_item['normal_price'] = item.css('td.ticket-price::text').extract_first().strip('¥起')
                product_item['tickets'] = {'price_id': product_item['type_id'], 'title': product_item['type_name'],
                                           'seller_nick': product_item['type_name'],
                                           'price': product_item['normal_price']}
                ota_product.append(product_item)
        o_price.ota_product = ota_product
        yield o_price
