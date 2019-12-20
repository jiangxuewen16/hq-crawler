# -*- coding: utf-8 -*-
import hashlib
import json
import time

import math
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.items.spot import spot
from spiders.common import OTA
from urllib.parse import quote
from spiders.items.price import price

"""
飞猪: todo:暂时不要爬
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
    app_key = '12574478'
    sign_cookie = ''
    sign_header = {}
    allowed_domains = ['h5.m.taobao.com/']
    base_url = r'https://h5api.m.taobao.com/h5/mtop.alitrip.tripmdd.querypoiinfo/3.9?type=originaljson&api=mtop' \
               r'.alitrip.tripmdd.querypoiinfo&v=3.9&data={data}&ttid=12mtb0000155&appKey=12574478&t={' \
               r'time}&sign={sign}'
    start_urls = ['https://h5api.m.taobao.com/h5/mtop.alitrip.tripmdd.querypoiinfo/3.9?type=originaljson&api=mtop'
                  '.alitrip.tripmdd.querypoiinfo&v=3.9&data={data}&ttid=12mtb0000155&appKey=12574478&t={'
                  'time}&sign={sign}']

    def parse(self, response: HtmlResponse):
        init_sign = '29cf97ff4076ea74f3319bc2f4e12f80'
        for ota_spot_id in FliggySpider.ota_spot_ids:
            request_data = json.loads('{"poiId":"11481","from":"","h5Version":"0.5.17"}')
            request_data['poiId'] = str(ota_spot_id)
            temp_request = request_data
            request_data = quote(json.dumps(request_data).replace(' ', ''), 'utf-8')
            url = self.base_url.format(data=request_data, time=str(int(round(time.time() * 1000))), sign=init_sign)
            yield Request(url=url, callback=self.parse_master, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id, 'data': temp_request, 'url_request_data': request_data})

    def parse_master(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        if json_data['ret'] == ['FAIL_SYS_ILLEGAL_ACCESS::非法请求']:
            cookie_list = self.get_cook_list(response)
            timestamp = str(int(round(time.time() * 1000)))
            sign = self.encode_token(timestamp, response.meta['data'], cookie_list)
            url = self.base_url.format(data=response.meta['url_request_data'], time=timestamp, sign=sign)
            yield Request(url=url, callback=self.parse_item, dont_filter=True, headers=self.sign_header,
                          meta={'ota_spot_id': response.meta['ota_spot_id'], 'data': response.meta['data']})

    def parse_item(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        charging_item_group_list = json.loads(response_str)['data']['data'][1]['list'][0]['chargingItemGroupList']
        for charging_item_group in charging_item_group_list:
            for charge_item in charging_item_group['chargeItems']:
                detail_url = r'https://h5api.m.taobao.com/h5/mtop.trip.travelspdetail.scenic.product.itemsearch/1.0' \
                             r'?type=originaljson&api=mtop.trip.travelspdetail.scenic.product.itemsearch&v=1.0&data={' \
                             r'data}&AntiCreep=true&AntiFlood=true&ttid=201300@travel_h5_3.1.0&appKey=12574478&t={' \
                             r'timestamp}&sign={sign}'
                data = {
                    "searchType": "TICKET",
                    "startRow": 0,
                    "pageSize": 2,
                    "source": "scenic",
                    "poiId": response.meta['ota_spot_id'],
                    "ticketKindName": charge_item['ticketTypeName'],
                    "productName": charge_item['value'],
                    "productId": charge_item['productVid'],
                    "h5Version": "0.5.17"
                }
                timestamp = str(int(round(time.time() * 1000)))
                sign = self.encode_token(timestamp, data)
                url_request_data = quote(json.dumps(data, ensure_ascii=False).replace(' ', ''), 'utf-8')
                url = detail_url.format(data=url_request_data, timestamp=timestamp, sign=sign)
                yield Request(url=url, callback=self.parse_detail, dont_filter=True, headers=self.sign_header,
                              meta={'ota_spot_id': response.meta['ota_spot_id'],
                                    'data': data, 'detail_url': detail_url})

    def parse_detail(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        products_detail = json.loads(response_str)
        data = response.meta['data']
        data['pageSize'] = products_detail['data']['totalCount']
        timestamp = str(int(round(time.time() * 1000)))
        sign = self.encode_token(timestamp, data)
        url_request_data = quote(json.dumps(data, ensure_ascii=False).replace(' ', ''), 'utf-8')
        request_url = response.meta['detail_url'].format(data=url_request_data, timestamp=timestamp, sign=sign)
        yield Request(url=request_url, callback=self.parse_data, dont_filter=True, headers=self.sign_header,
                      meta={'ota_spot_id': response.meta['ota_spot_id'], 'data': data})

    @staticmethod
    def parse_data(response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        products_detail = json.loads(response_str)['data']['itemInfos']
        data = response.meta['data']
        o_price = price.OPrice()
        o_price.ota_id = OTA.OtaCode.FLIGGY.value.id
        o_price.ota_spot_id = response.meta['ota_spot_id']
        o_price.create_at = time.strftime("%Y-%m-%d", time.localtime()).format('')
        total_price = i = 0
        o_price.ota_product = {
                'type_id': 0,
                'type_key': data['ticketKindName'],
                'type_name': data['productName'],
                'tickets': []
            }
        for ticket in products_detail:
            ticket_info = {
                'product_id': ticket['itemId'],
                'title': ticket['title'],
                'price': ticket['price'],
                'cash_back': 0,
                'cut_price': 0,
                'sale_num': int(ticket['soldRecent'][2:-1]) if 'soldRecent' in ticket else 0,
                'seller_nick': ticket['sellerNick']
            }
            i = i+1
            total_price = total_price + float(ticket['price'])
            o_price.ota_product['tickets'].append(ticket_info)
        yield o_price
        o_price_calendar = price.OPriceCalendar()
        o_price_calendar.ota_id = OTA.OtaCode.FLIGGY.value.id
        o_price_calendar.ota_spot_id = response.meta['ota_spot_id']
        o_price_calendar.type_key = data['ticketKindName']
        o_price_calendar.type_name = data['productName']
        o_price_calendar.pre_price = total_price / i
        o_price_calendar.create_at = time.strftime("%Y-%m-%d", time.localtime()).format('')
        yield o_price_calendar

    def get_cook_list(self, response: HtmlResponse):
        cookie_list = response.headers.getlist('Set-Cookie')
        request_cookie = ''
        for cookie in cookie_list:
            if '_m_h5_tk' in str(cookie) or '_m_h5_tk_enc' in str(cookie):
                request_cookie += bytes.decode(cookie) + '; '
                continue
        self.sign_header = {
            'Content-Type': 'application/json',
            'cookie': request_cookie,
        }
        return cookie_list

    def encode_token(self, timestamp, data, cookie_list=None):
        if cookie_list is not None:
            temp_cookie = ''
            for cookie in cookie_list:
                if '_m_h5_tk' in str(cookie):
                    temp_cookie = cookie
                    break
            index_len = len('_m_h5_tk') + 1
            token_len = len('cf63a39b0140c01b5499b4d2f9f09950') + index_len
            self.sign_cookie = bytes.decode(temp_cookie[index_len:token_len])
        md_str = self.sign_cookie + '&' + timestamp + '&' + self.app_key + '&' + str(json.dumps(data, ensure_ascii=False
                                                                                                )).replace(' ', '')
        return hashlib.md5(md_str.encode()).hexdigest()


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
