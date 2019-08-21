# -*- coding: utf-8 -*-
import json
import time
import urllib.parse


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
            # 获取景区的总评论数
            spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.LVMAMA.value.id,
                                          ota_spot_id=ota_spot_id).first()
            start_page = 1 # 开始页数

            url = self.base_url.format(ota_spot_id=ota_spot_id, currentPage=start_page, totalCount=spot_data.comment_num)
            yield Request(url=url, callback=self.parse_page, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id, 'currentPage': start_page,
                                'totalCount': spot_data.comment_num})

    def parse_page(self, response: HtmlResponse):
        items = response.css('.comment-li')
        for item in items:
            print(item.css('.ufeed-content::text').extract()[1].strip())

        return

        # 获取编码
        charset = response.encoding
        # 获取网页内容
        content = response.text
        # 先根据原编码转化为字节bytes，转化为utf-8字符串str
        content = content.encode(charset).decode('utf-8')
        comment_list = content.find_all(class_='comment-li')
        # 遍历新闻，获取每条的详细信息
        for comment in comment_list:
            star = comment.find(class_='ufeed-level').i.get('data-level')
            print(star)

        return




    def parse_count(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        comment_num = spot.SpotComment.objects(ota_id=OTA.OtaCode.LVMAMA.value.id, ota_spot_id=ota_spot_id).count()
        new_total = float(
            response.xpath('//*[@id="comments"]/div[2]/div[1]/div/div[1]/em[2]/a/text()').extract_first())
        new_num = new_total - comment_num

        # if new_num == 0:  # 没有新评论的情况下不需要做任何处理
        #     return

        # max_offset = new_num - 1  # 最大能偏移的数量
        # page_size = self.page_size
        # if new_num < self.page_size:  # 新增的评论数量小于默认爬取的最大数量，则用新增的数量作为爬取数量
        #     page_size = new_num

        # 爬取景区的所有评论
        start_page = 1
        start_offset = 0
        print('=========增量爬取参数=========', ota_spot_id, new_total, comment_num, 1)
        post_data = {
            'type': all, 'currentPage': start_page, 'totalCount': new_num, 'placeId': ota_spot_id,
            'productId': '', 'placeIdType': 'PLACE', 'isPicture': '', 'isBest': '', 'isPOI': 'Y', 'isELong': 'N'}
        post_data_encode = urllib.parse.urlencode(post_data)
        url = self.base_url
        headers = {
            'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' }
        yield Request(method='POST', headers=headers, body=post_data_encode, url=url, callback=self.parse_page, dont_filter=True,
                      meta={'offset': start_offset, 'max_offset': 1, 'ota_spot_id': ota_spot_id,
                            'page_size': 1})
