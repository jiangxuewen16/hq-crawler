# -*- coding: utf-8 -*-
import json
import math
import random
import time

import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy import Request

from spiders.common import OTA
from spiders.items.spot import spot
from spiders.items.price import price


class QunarSpider(scrapy.Spider):
    # 标签  0 系统标签，1用户标签
    sys_tags = 0
    user_tags_true = 1
    user_tags_false = 2
    name = 'qunar'
    allowed_domains = ['www.qunar.com']
    start_urls = ['http://www.qunar.com/']

    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.QUNAR)  # ota 景区id列表

    def parse(self, response):
        pass


class QunarTagSpider(scrapy.Spider):
    name = 'qunar_tag'
    allowed_domains = ['www.qunar.com']

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
            spot_tag = []
            for key, value in enumerate(comment['data']['tagList']):
                # print(value['tagName'])

                if value['tagType'] in [0, 1, 41, 43, 44]:
                    tag_type = QunarSpider.sys_tags  # 属于系统标签
                else:
                    tag_type = QunarSpider.user_tags_true  # 属于用户标签
                tag = {'tag_name': value['tagName'], 'tag_num': value['tagNum'], 'tag_score': value['tagScore'],
                       'tag_type': tag_type}
                spot_tag.append(tag)
            print(spot_tag, "#" * 20)
            print('-' * 20, 'ota_id', OTA.OtaCode.QUNAR.value.id, 'ota_spot_id', response.meta['ota_spot_id'])
            spot.Spot.objects(ota_id=OTA.OtaCode.QUNAR.value.id,
                              ota_spot_id=response.meta['ota_spot_id']).update(
                set__tag_list=spot_tag)
            pass


class CommentSpider(scrapy.Spider):
    name = 'qunar_comment'
    allowed_domains = ['www.qunar.com']

    total_num = 0  # 总评论
    page_size = 10  # 默认爬取每页100条
    base_url = r'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize={page_size}&fromType=SIGHT&pageNum={page_num}&sightId={ota_spot_id}&tagType=44&tagName=%E6%9C%80%E6%96%B0'
    start_urls = [
        'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=1&fromType=SIGHT&pageNum=1&sightId=706176810']

    def parse(self, response: HtmlResponse):
        headers = {'content-type': 'application/json'}

        # 爬取景区列表数据
        for ota_spot_id in QunarSpider.ota_spot_ids:
            # 更新景区的评论数量
            url = self.base_url.format(ota_spot_id=ota_spot_id, page_num=1, page_size=10)
            # headers = {'content-type': 'application/json'}
            data = requests.get(url, headers=headers)
            comment = data.json()
            print(ota_spot_id, "共", comment['data']['total'], "条", "*" * 20)
            page_size = 10
            # 网页上总条数
            total_page = comment['data']['total']
            # 数据库总条数
            now_total = spot.SpotComment.objects(ota_id=OTA.OtaCode.QUNAR.value.id,
                                                 ota_spot_id=ota_spot_id).count()

            # 准备保存的总条数
            to_save_total = total_page - now_total
            # 准备保存的总页数
            total_page = math.ceil(to_save_total / page_size)
            for page_num in range(1, total_page + 1):
                if page_num == total_page:
                    page_size = to_save_total - (page_num - 1) * page_size
                else:
                    page_size = page_size
                url = self.base_url.format(ota_spot_id=ota_spot_id, page_num=page_num, page_size=page_size)
                print("-" * 30)
                print(url)
                print("+" * 30)
                # headers = {'content-type': 'application/json'}
                data = requests.get(url, headers=headers)
                comment = data.json()
                print(ota_spot_id, " 第", page_num, "页: ", "共", page_size, "条 ", "*" * 20)
                if 'data' in comment and 'commentList' in comment['data']:
                    for key, value in enumerate(comment['data']['commentList']):
                        print('正在添加 ', value['author'], ' 的评论', "*" * 20)
                        spot_comment = spot.SpotComment.objects(ota_id=10004).first()
                        spot_comment.ota_id = OTA.OtaCode.QUNAR.value.id
                        spot_comment.ota_spot_id = ota_spot_id

                        spot_comment.goods_name = value['sightName']
                        # spot_comment.u_avatar = value['headImg']
                        spot_comment.u_name = value['author']
                        spot_comment.c_tag = value['tagList']
                        spot_comment.c_id = value['commentId']
                        spot_comment.c_score = value['score']
                        spot_comment.c_content = value['content']
                        # spot_comment.c_img = value['imgs']
                        spot_comment.c_img = [item['small'] for item in value['imgs']]
                        spot_comment.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        yield spot_comment


'''
点评数据加tag
'''


class CommentAndTagSpider(scrapy.Spider):
    name = 'comment_and_tag'
    allowed_domains = ['touch.piao.qunar.com']

    def start_requests(self):
        for ota_spot_id in QunarSpider.ota_spot_ids:
            print(ota_spot_id, 'ota' * 20)
            yield scrapy.FormRequest(
                'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=10&fromType=SIGHT&pageNum=0&sightId=' + str(
                    ota_spot_id)
                , method='GET'
                , meta={'ota_spot_id': ota_spot_id}
                , callback=self.after_login)

    def after_login(self, response):
        print('-' * 20)
        result = json.loads(response.body)

        if 'data' in result and 'tagList' in result['data']:
            spot_tag = []
            for key, value in enumerate(result['data']['tagList']):
                if value['tagType'] in [0, 1, 41, 43, 44]:
                    tag_type = QunarSpider.sys_tags  # 属于系统标签
                else:
                    tag_type = QunarSpider.user_tags_true  # 属于用户标签
                tag = {'tag_name': value['tagName'], 'tag_num': value['tagNum'], 'tag_score': value['tagScore'],
                       'tag_type': tag_type}
                spot_tag.append(tag)
            print(spot_tag, "#" * 20)
            print('-' * 20, 'ota_id', OTA.OtaCode.QUNAR.value.id, 'ota_spot_id', response.meta['ota_spot_id'])
            spot.Spot.objects(ota_id=OTA.OtaCode.QUNAR.value.id,
                              ota_spot_id=response.meta['ota_spot_id']).update_one(
                set__tag_list=spot_tag, upsert=True)

        if 'data' in result and 'total' in result['data']:
            print('共', result['data']['total'], '条', '*' * 20)
            for pag_num in range(1, math.ceil(result['data']['total'] / 10)):
                # for pag_num in range(1, 5):
                print('第', pag_num, '页', '+' * 20)
                yield scrapy.FormRequest(
                    'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=10&fromType=SIGHT&pageNum=' + str(
                        pag_num) + '&sightId=' + str(response.meta['ota_spot_id'])
                    , method='GET'
                    , meta={'page': pag_num, 'ota_spot_id': response.meta['ota_spot_id']}
                    , callback=self.each_page)

    def each_page(self, response):
        print('-' * 20)
        result = json.loads(response.body)
        if 'data' in result and 'commentList' in result['data']:
            for key, value in enumerate(result['data']['commentList']):
                print(value['author'], '第', response.meta['page'], '页', '+' * 20)
                if 'headImg' in value:
                    headImg = value['headImg']
                else:
                    headImg = ''
                yield spot.SpotComment.objects(c_id=value['commentId']).update_one(
                    set__ota_id=OTA.OtaCode.QUNAR.value.id,
                    set__ota_spot_id=response.meta['ota_spot_id'],
                    set__goods_name=value['sightName'],
                    set__u_avatar=headImg,
                    set__u_name=value['author'],
                    set__c_tag=value['tagList'],
                    set__c_score=value['score'],
                    set__c_content=value['content'],
                    set__c_img=[item['small'] for item in value['imgs']],
                    set__create_at=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    upsert=True)


class PriceSpider(scrapy.Spider):
    ota_map = [{'ota_spot_id': 706176810, 'sightId': '14407', 'sightName': '石燕湖'}  # 石燕湖
        , {'ota_spot_id': 1915618311, 'sightId': '187730', 'sightName': '石牛寨'}  # 石牛寨
        , {'ota_spot_id': 2877753081, 'sightId': '469141', 'sightName': '益阳嘉年华'}  # 益阳嘉年华
        , {'ota_spot_id': 2554926827, 'sightId': '470541', 'sightName': '花田溪谷'}  # 花田溪谷
        , {'ota_spot_id': 225118749, 'sightId': '461232', 'sightName': '东浒寨'}  # 东浒寨
        , {'ota_spot_id': 3821817759, 'sightId': '11829', 'sightName': '马仁奇峰'}  # 马仁奇峰
        , {'ota_spot_id': 420237024, 'sightId': '39499', 'sightName': '大茅山'}  # 大茅山
        , {'ota_spot_id': 4123349957, 'sightId': '35473', 'sightName': '九龙江'}  # 九龙江
        , {'ota_spot_id': 2333288470, 'sightId': '196586', 'sightName': '侠天下'}  # 侠天下
        , {'ota_spot_id': 3333064220, 'sightId': '461903', 'sightName': '三翁花园'}  # 三翁花园
               ]
    name = 'qunar_price'
    allowed_domains = ['piao.qunar.com']
    login_url = 'http://piao.qunar.com/ticket/detail/getTickets.json'

    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    def start_requests(self):
        price.OPrice.objects(ota_id=10006).delete()
        price.OPriceCalendar.objects(ota_id=10006, create_at=time.strftime("%Y-%m-%d", time.localtime())).delete()
        print('start_request')
        for value in self.ota_map:
            # print(value['sightId'], "*" * 20)
            yield scrapy.FormRequest(self.login_url
                                     , formdata={'sightId': value['sightId'], 'from': 'detail'}
                                     , meta={'ota_spot_id': value['ota_spot_id'], 'sight_name': value['sightName']}
                                     , callback=self.after_login)

    def after_login(self, response):
        print('-' * 20)
        result = json.loads(response.body)
        if 'data' in result and 'groups' in result['data']:
            for k1, v1 in enumerate(result['data']['groups']):  # group数据   sightId
                ota_product = []
                for k2, v2 in enumerate(v1):  # 票型数据
                    tickets = []
                    typeId = str(v2['typeId'])
                    ota_spot_name = response.meta['sight_name']
                    typeKey = ota_spot_name + v2['ticketZoneName']
                    ticketZoneName = v2['typeName']
                    total_count = v2['totalCount']  # 总共票数
                    total_price = 0  # 总共票数

                    normal_price = v2['qunarPrice']
                    if 'tickets' in v2:
                        print(v2['qunarPrice'])
                        for k3, v3 in enumerate(v2['tickets']):
                            tickets_list = {'price_id': str(v3['priceId'])
                                , 'title': v3['title']
                                , 'seller_nick': v3['supplierName']
                                , 'price': v3['qunarPrice']
                                , 'cash_back': v3['cashBack']
                                , 'cut_price': v3['cutPrice']
                                , 'sale_num': 0
                                , 'url': 'http://touch.piao.qunar.com/touch/detail_' + str(response.meta[
                                                                                               'ota_spot_id']) + '.html?st=a3clM0QlRTclOUYlQjMlRTclODclOTUlRTYlQjklOTYlMjZpZCUzRDE0NDA3JTI2dHlwZSUzRDAlMjZpZHglM0QxJTI2cXQlM0RuYW1lJTI2YXBrJTNEMiUyNnNjJTNEV1dXJTI2YWJ0cmFjZSUzRGJ3ZCU0MCVFNiU5QyVBQyVFNSU5QyVCMCUyNnVyJTNEJUU5JTk1JUJGJUU2JUIyJTk5JTI2bHIlM0QlRTklOTUlQkYlRTYlQjIlOTklMjZmdCUzRCU3QiU3RA%3D%3D#from=mpl_search_suggest'
                                            }
                            tickets.append(tickets_list)
                            total_price = total_price + v3['qunarPrice']
                            # print(v3['title'])  # priceId qunarPrice cashBack cutPrice supplierId supplierName
                    ota_product_list = {'type_id': typeId, 'type_key': typeKey, 'type_name': ticketZoneName,
                                        'normal_price': normal_price,
                                        'tickets': tickets}
                    ota_product.append(ota_product_list)
                    pre_price = round(total_price / total_count, 2)
                    print(pre_price, "+" * 20)
                # print(ota_product)
                '''
                价格日历保存
                '''
                price_calendar = price.OPriceCalendar()

                price_calendar.ota_id = OTA.OtaCode.QUNAR.value.id
                price_calendar.ota_spot_id = response.meta['ota_spot_id']
                price_calendar.ota_spot_name = response.meta['sight_name']
                price_calendar.pre_price = pre_price
                price_calendar.type_id = typeId
                price_calendar.type_key = typeKey
                price_calendar.type_name = ticketZoneName
                price_calendar.create_at = time.strftime("%Y-%m-%d", time.localtime())

                o_price = price.OPrice()
                o_price.ota_id = OTA.OtaCode.QUNAR.value.id
                o_price.ota_spot_id = response.meta['ota_spot_id']
                o_price.ota_spot_name = ota_spot_name

                o_price.ota_product = ota_product  # typeId typeName qunarPrice
                price_calendar.save(force_insert=False, validate=False, clean=True)
                yield o_price
