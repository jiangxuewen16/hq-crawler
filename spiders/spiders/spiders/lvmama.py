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

        # spot_data.spot_id = OTA.OtaSpotIdMap.get_ota_spot_id(OTA.OtaSpotIdMap.SHI_YAN_HU.name, OTA.OtaCode.HUIQULX)
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

class LvmamaCitySpider(scrapy.Spider):
    name = 'lvmama_city'
    allowed_domains = ['www.m.lvmama.com']
    base_url = r'https://m.lvmama.com/ticket/?fromCity=1'
    start_urls = ['https://m.lvmama.com/ticket/?fromCity=1']
    city_url = 'https://m.lvmama.com/api/router/rest.do?method=api.com.home.getStations&version=1.0.0&format=' \
               'json&firstChannel=TOUCH&secondChannel=LVMM'
    spot_url = 'https://m.lvmama.com/tour/ticket?keyword={city_name}&ajax=true&ticket_page={page}'
    ticket_url = 'https://m.lvmama.com/ticket/piao-{ticket_id}'
    address_url = 'https://m.lvmama.com/ticket/piao-{ticket_id}/map'
    info_url = 'https://m.lvmama.com/ticket/piao-{ticket_id}/introduction'
    comment_url = 'https://m.lvmama.com/ticket/piao-{ticket_id}/comment'

    def parse(self, response: HtmlResponse):
        headers = {
            'signal': 'ab4494b2-f532-4f99-b57e-7ca121a137ca'
        }
        yield Request(url=self.city_url, callback=self.spot_city, headers=headers, dont_filter=True)


    def spot_city(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        for city_rs in json_data['data']:
            # spot_city.ota_id = OTA.OtaCode.LVMAMA.value.id
            url = self.spot_url.format(city_name=city_rs['name'], page=1)
            yield Request(url=url, callback=self.get_spot_by_city, dont_filter=True,
                          meta={'city_id': city_rs['id'], 'city_name': city_rs['name'], 'area_pinyin': city_rs['pinyin'], 'area_name': city_rs['name'],
                                'province_name': city_rs['provinceName'], 'page': 1})

    def get_spot_by_city(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        html = Selector(text=json_data['html'])
        spot_rs = html.css('.exact-item')
        if not spot_rs:
            return
        for spot_data in spot_rs:
            spot_id = int(spot_data.css('::attr(data-product-id)').extract_first())
            spot_city = spot.SpotCity.objects(ota_id=OTA.OtaCode.LVMAMA.value.id,
                                              ota_spot_id=spot_id).first()
            # 不存在数据则新增数据,增量爬取
            if not spot_city:
                spot_city = spot.SpotCity()
                spot_city.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            spot_city.ota_spot_id = spot_id
            spot_city.ota_id = OTA.OtaCode.LVMAMA.value.id

            spot_city.city_id = int(response.meta['city_id'])
            spot_city.area_pinyin = response.meta['area_pinyin']
            spot_city.area_name = response.meta['area_name']
            spot_city.city_name = response.meta['city_name']

            spot_city.s_img = spot_data.css('.img-wrap img::attr(data-src)').extract_first()
            spot_city.s_name = spot_data.css('.product-name-1::text').extract_first()
            spot_city.s_score = float(spot_data.css('.score-wrap > span::text').extract_first()) if \
                spot_data.css('.score-wrap > span::text').extract_first() is not None else 5.0

            spot_city.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # yield spot_city
            url = self.ticket_url.format(ticket_id=spot_id)
            yield Request(url=url, callback=self.get_ticket_by_spot, dont_filter=True,
                          meta={'spot_city': spot_city})


        page = response.meta['page'] +1
        url = self.spot_url.format(city_name=response.meta['city_name'], page=page)
        yield Request(url=url, callback=self.get_spot_by_city, dont_filter=True,
                          meta={'city_id': response.meta['city_id'], 'city_name': response.meta['city_name'], 'area_pinyin': response.meta['area_pinyin'],
                                'area_name': response.meta['area_name'],
                                'province_name': response.meta['province_name'], 'page': page})



    def get_ticket_by_spot(self, response: HtmlResponse):
        # spot_city = spot.SpotCity.objects(ota_id=OTA.OtaCode.LVMAMA.value.id,
        #                                   ota_spot_id=response.meta['spot_id']).first()
        spot_city = response.meta['spot_city']
        ticket_arr = {'ADULT': [], 'ACTIVITY': [], 'FREE': [], 'TC': [], 'num': 0}
        ticket_rs = response.css('div.adult-ticket.hasGoods.ADULT')
        ticket_rs = ticket_rs.css('.list-module')
        for ticket_data in ticket_rs:
            ticket_arr['num'] += 1
            ticket_arr['ADULT'].append({
                'name': ticket_data.css('.name::text').extract_first().strip(),
                'rule': ticket_data.css('.notes > span::text').extract(),
                'rack_price': ticket_data.css('.marketPrice > del::text').extract_first(),
                'pay_price': float(ticket_data.css('.price > span > i::text').extract()[1])
            })
        ticket_rs = response.css('div.adult-ticket.hasGoods.ACTIVITY')
        ticket_rs = ticket_rs.css('.list-module')
        for ticket_data in ticket_rs:
            ticket_arr['num'] += 1
            ticket_arr['ACTIVITY'].append({
                'name': ticket_data.css('.name::text').extract_first().strip(),
                 'rule': ticket_data.css('.notes > span::text').extract(),
                 'rack_price': ticket_data.css('.marketPrice > del::text').extract_first(),
                   'pay_price': float(ticket_data.css('.price > span > i::text').extract()[1])
               })
        ticket_rs = ticket_rs.css('.list-module')
        for ticket_data in ticket_rs:
            ticket_arr['num'] += 1
            ticket_arr['FREE'].append({
                'name': ticket_data.css('.name::text').extract_first().strip(),
                'rule': ticket_data.css('.notes > span::text').extract(),
                'rack_price': ticket_data.css('.marketPrice > del::text').extract_first(),
                'pay_price': float(ticket_data.css('.price > span > i::text').extract()[1])
            })
        ticket_rs = ticket_rs.css('.prdShow')
        for ticket_data in ticket_rs:
            ticket_arr['num'] += 1
            ticket_arr['TC'].append({
                'name': ticket_data.css('.prdName::text').extract_first().strip(),
                'rule': ticket_data.css('.right::text').extract(),
                'rack_price': float(ticket_data.css('.price > span > i::text').extract()[1]),
                'pay_price': float(ticket_data.css('.price > span > i::text').extract()[1])
            })
        spot_city.s_ticket = ticket_arr
        spot_city.s_ticket_num = ticket_arr['num']
        spot_city.s_addr = response.xpath('//*[@id="tpl"]/div[1]/div[2]/div[2]/p/text()').extract_first()

        url = self.info_url.format(ticket_id=spot_city.ota_spot_id)
        yield Request(url=url, callback=self.get_info_by_ticket, dont_filter=True,
                      meta={'spot_city': spot_city})

    def get_info_by_ticket(self,response: HtmlResponse):
        spot_city = response.meta['spot_city']
        spot_city.s_notes = response.css('.play-project.scenicSpots.YDXZ p::text').extract()
        spot_city.s_desc = response.css('.play-project.JQJS').get()

        url = self.address_url.format(ticket_id=spot_city.ota_spot_id)
        yield Request(url=url, callback=self.get_address_by_ticket, dont_filter=True,
                      meta={'spot_city': spot_city})


    def get_address_by_ticket(self,response: HtmlResponse):
        spot_city = response.meta['spot_city']

        address_rs = response.xpath('//script[4]/text()').extract_first()
        spot_city.lat = address_rs.split("latitude = '")[1].split("'")[0]
        spot_city.lng = address_rs.split("longitude = '")[1].split("'")[0]

        url = self.comment_url.format(ticket_id=spot_city.ota_spot_id)
        yield Request(url=url, callback=self.get_comment_by_ticket, dont_filter=True,
                      meta={'spot_city': spot_city})

    def get_comment_by_ticket(self, response: HtmlResponse):
        spot_city = response.meta['spot_city']

        spot_city.s_comment_num = int(response.css('.tic.activeT::text').extract_first().split("全部(")[1].split(")")[0]) if response.css('.tic.activeT::text').extract_first() is not None  else 0
        yield spot_city


