# -*- coding: utf-8 -*-
import base64
import json
import re
import time
import zlib
from urllib import parse

import scrapy
from datetime import datetime
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.price import price
from spiders.items.spot import spot
from spiders.items.spot.spot import Spot


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['www.meituan.com']
    start_urls = ['https://www.meituan.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.MEITUAN)  # ota 景区id列表

    def parse(self, response):
        pass

# todo 景区用城市景区的
# class MeituanSpotSpider(scrapy.Spider):
#     name = 'meituan_spot'
#     allowed_domains = ['www.meituan.com']
#     base_url = r'https://www.meituan.com/zhoubianyou/{ota_spot_id}'
#     start_urls = ['https://www.meituan.com/zhoubianyou/1515791']
#
#     def parse(self, response: HtmlResponse):
#         for ota_spot_id in MeituanSpider.ota_spot_ids:
#             # 更新景区的评论数量
#             url = self.base_url.format(ota_spot_id=ota_spot_id)
#             yield Request(url=url, callback=self.parse_item, dont_filter=True,
#                           meta={'ota_spot_id': ota_spot_id})
#
#     def parse_item(self, response: HtmlResponse):
#         spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.MEITUAN.value.id,
#                                       ota_spot_id=response.meta['ota_spot_id']).first()
#
#         # 不存在数据则新增数据
#         if not spot_data:
#             spot_data = Spot()
#             spot_data.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#         spot_data.ota_spot_id = response.meta['ota_spot_id']
#         spot_data.ota_id = OTA.OtaCode.MEITUAN.value.id
#         spot_data.spot_name = response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/h1/text()').extract_first()
#         # print('++'*20,response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[1]/span/text()[1]'))
#         spot_data.spot_score = float(
#             response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[1]/span/text()[1]').extract_first())
#         spot_data.avg_price = float(
#             response.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[1]/span/span/text()[2]').extract_first())
#         spot_data.addr = response.xpath(
#             '//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[1]/a/span/text()').extract_first()
#         spot_data.tel = response.xpath(
#             '//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[2]/span[2]/text()').extract_first()
#         spot_data.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#         yield spot_data


class MeituanCommentSpider(scrapy.Spider):
    name = 'meituan_comment'
    allowed_domains = ['www.meituan.com']

    total_num = 0  # 总评论
    page_size = 50  # 默认爬取每页50条
    # https://www.meituan.com/ptapi/poi/getcomment?id=1515791&offset=0&pageSize=10&mode=0&starRange=&userId=&sortType=0
    base_url = r'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&offset={offset}&pageSize={page_size}&mode=0&starRange=&userId=&sortType=0'
    start_urls = [
        'https://www.meituan.com/ptapi/poi/getcomment?id=1515791&offset=0&pageSize=1&mode=0&starRange=&userId=&sortType=0']

    def parse(self, response: HtmlResponse):

        # 爬取景区列表数据
        # for ota_spot_id in MeituanSpider.ota_spot_ids:
        #     # 更新景区的评论数量
        #     url = self.base_url.format(spot_id=ota_spot_id, offset=0, page_size=1)
        #     yield Request(url=url, callback=self.parse_count, dont_filter=True,
        #                   meta={'offset': 0, 'ota_spot_id': ota_spot_id})

        url = self.base_url.format(spot_id=188085997, offset=0, page_size=1)
        yield Request(url=url, callback=self.parse_count, dont_filter=True,
                           meta={'offset': 0, 'ota_spot_id': 188085997})

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
        print('测试============', start_offset, max_offset, page_size)
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
        # comment_num = spot_info.comment_num if spot_info and spot_info.comment_num else 0  # 已有的评论数量
        spot_info.update(set__comment_num=new_total)

        comment_num = spot.SpotComment.objects(ota_id=OTA.OtaCode.MEITUAN.value.id, ota_spot_id=ota_spot_id).count()

        new_num = new_total - comment_num
        if new_num <= 0:  # 没有新评论的情况下不需要做任何处理
            return

        max_offset = new_num - 1  # 最大能偏移的数量
        page_size = self.page_size
        if new_num < self.page_size:  # 新增的评论数量小于默认爬取的最大数量，则用新增的数量作为爬取数量
            page_size = new_num

        # 爬取景区的所有评论
        start_offset = 0
        print('=========增量爬取参数=========', '===景区id:', ota_spot_id, '===爬取时数量:', new_total, '===数据库数量:', comment_num, '===最大能偏移的数量:', max_offset)
        url = self.base_url.format(spot_id=ota_spot_id, offset=start_offset, page_size=page_size)

        yield Request(url=url, callback=self.parse_page, dont_filter=True,
                      meta={'offset': start_offset, 'max_offset': max_offset, 'ota_spot_id': ota_spot_id,
                            'page_size': page_size})


class MeituanBiwanList(scrapy.Spider):
    name = 'meituan_biwan_list'
    allowed_domains = ['i.meituan.com']
    base_page_url = r'https://i.meituan.com/awp/h5/trip-scenes/travellist/master/index.html?cityId=70&billboardId=250&source=mt'
    start_urls = [
        'https://itrip.meituan.com/volga/api/v1/trip/billboard/worthPlay?cityId=70&source=mt&billboardId=250&inner_source=mtshare&utm_term=AiphoneBgroupC10.3.400DcopyEpromotionG0583CF80FA64E9F4545989328001235F01A3DE3FB11F3E6F16F1D332BAAD750720191021205730351&utm_source=appshare&utm_medium=iOSweb&utm_fromapp=copy&utm_sharesource=promotion&lch=appshare_k20fd27fpbn5&ci=70&feclient=lvyou_wap&uuid=3F1B3AB7262A309B279A62C912513D18CEF869AD324DF8263D921F91967B162B&client=wap']

    def parse(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        ota_spot_id = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.MEITUAN)
        for items in json_data['data']['poiList']:
            if items['poiId'] in ota_spot_id:
                print('=========已找到必玩榜中目标景区排行=========', items['rank'])
                spot_info = spot.Spot.objects(ota_spot_id=items['poiId']).update(set__spot_rank=items['rank']+1, set__spot_introduction=items['introduction'])
                print('=========更新成功=========', spot_info)


class MeituanCitySpot(scrapy.Spider):
    name = 'meituan_city_spot'
    allowed_domains = ['www.meituan.com', 'i.meituan.com', 'itrip.meituan.com']
    # 景区列表页
    base_page_url = r'http://i.meituan.com/select/{area_pinyin}/page_1.html?cid=162&bid=-1&sid=solds&p={page}&ciid=70&bizType=area&csp=&stid_b=_b2&cateType=poi&nocount=true'

    # 景区详情信息链接
    # base_detail_url = r'https://i.meituan.com/awp/h5/lvyou/poi/detail/index.html?poiId={ota_spot_id}'  # 景区详情

    # 景区商户信息->商品
    # base_detail_business_url = r'https://itrip.meituan.com/volga/api/v3/trip/poi/business/info/{ota_spot_id}?poiId={ota_spot_id}&source=mt&client=wap&uuid=87F297BEE697EA1CC2805C4C97A33BC991B2EC50D3FF74ED5E959E34BE3C9441&cityId=70&feclient=lvyou_wap&platform=6&partner=11&originUrl=https%3A%2F%2Fi.meituan.com%2Fawp%2Fh5%2Flvyou%2Fpoi%2Fdetail%2Findex.html%3FpoiId%3D{ota_spot_id}&_token={token}'  # 景区商品信息
    base_detail_business_url = r'https://itrip.meituan.com/volga/api/v3/trip/poi/business/info/{ota_spot_id}?poiId={ota_spot_id}&_token={token}'

    # 景区基本信息
    base_detail_basic_url = r'https://itrip.meituan.com/volga/api/v3/trip/poi/basic/info/{ota_spot_id}?poiId={ota_spot_id}&_token={token}'  # 景区信息

    # 景区评论
    # base_detail_comment_url = r'https://itrip.meituan.com/volga/api/v1/trip/poi/comment/{ota_spot_id}?poiId={ota_spot_id}&source=mt&client=wap&uuid=87F297BEE697EA1CC2805C4C97A33BC991B2EC50D3FF74ED5E959E34BE3C9441&cityId=70&feclient=lvyou_wap&filter=all&noempty=0&offset=0&limit=2&platform=5&partner=11&originUrl=https%3A%2F%2Fi.meituan.com%2Fawp%2Fh5%2Flvyou%2Fpoi%2Fdetail%2Findex.html%3FpoiId%3D{ota_spot_id}&_token={token}'
    base_detail_comment_url = r'https://itrip.meituan.com/volga/api/v1/trip/poi/comment/{ota_spot_id}?poiId={ota_spot_id}&filter=all&noempty=0&offset=0&limit=0&_token={token}'

    base_detail_info_url = r'https://i.meituan.com/lvyou/volga/api/v3/trip/poi/info/desc/?poiId={ota_spot_id}&source=mt&client=wap&uuid=87F297BEE697EA1CC2805C4C97A33BC991B2EC50D3FF74ED5E959E34BE3C9441&cityId={city_id}&feclient=lvyou_wap&poiId={ota_spot_id}'  # 景区信息 预订须知 景点介绍

    start_urls = ['https://i.meituan.com/index/changecity']  # 获取美团地区列表

    # 原始加密的token
    token = 'eJxVj1trg0AQhf%2FLPC97c3e9gBShUCz0oWLyEvJg46JLvaGrtZT%2B90wgoRQGzsw3h8PMD8x5DYngnAtJYLMzJCAopwYI%2BAU32pgoViZWUYyGyz%2BmeRAS%2BJiPz5CchJCaSBWY8w0VSE5BqEkk5Jn8dVJh3Rw5GqD1floSxhztrfNrNdDL2LPqa2KtZt32Pa5sGh2rra9cx9xQ2522vu%2BekOZ1qgWPBFcKbwXM7EvMRP28a3VX%2F5jf8Dn0Lq4ZsLOve3lo8ix7abLiPU3h9wpoBEnU'
    base_detail_referer_url = 'https://i.meituan.com/awp/h5/lvyou/poi/detail/index.html?poiId={ota_spot_id}'

    def parse(self, response: HtmlResponse):
        # 美团地区
        letter_city_list = response.css('div.nopadding .abc')
        for city_list in letter_city_list:
            city_list = city_list.css('li')
            for city in city_list:
                area_pinyin = city.css('a::attr(data-citypinyin)').extract_first()
                area_name = city.css('a::text').extract_first()
                if area_name == '更多»':
                    continue

                # 抓取地区的景区列表
                page = 1
                url = self.base_page_url.format(area_pinyin=area_pinyin, page=page)
                print('=' * 20, '爬取的地址：', url)
                yield Request(url=url, callback=self.parse_page, dont_filter=True,
                              meta={'area_pinyin': area_pinyin, 'area_name': area_name, 'page': page})

        # city_pinyin = 'changsha'
        # city_name = '长沙'
        # # 抓取地区的景区列表
        # page = 1
        # url = self.base_page_url.format(city_pinyin=city_pinyin, page=page)
        # yield Request(url=url, callback=self.parse_page, dont_filter=True,
        #               meta={'city_pinyin': city_pinyin, 'city_name': city_name, 'page': page})

    """
    分页爬取数据
    """

    def parse_page(self, response: HtmlResponse):
        area_pinyin = response.meta['area_pinyin']
        area_name = response.meta['area_name']
        page = response.meta['page']

        items = response.css('div#deals dl[gaevent="common/poilist"]')
        if not items:  # 如果没有说明已经爬取完成
            return

        for item in items:
            # 爬取景区详情
            ota_spot_id = item.css('p[data-com="redirect"]::attr(data-href)').extract_first().split('/poi/')[1]
            token = self.encode_token(self.token, ota_spot_id)
            # token = self.token
            # 爬取美团：详情-景区信息
            url = self.base_detail_basic_url.format(ota_spot_id=ota_spot_id, token=token)
            yield Request(url=url, callback=self.spot_detail_basic, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id, 'area_name': area_name, 'area_pinyin': area_pinyin,
                                'token': token})

        page += 1
        url = self.base_page_url.format(area_pinyin=area_pinyin, page=page)
        yield Request(url=url, callback=self.parse_page, dont_filter=True,
                      meta={'area_pinyin': area_pinyin, 'area_name': area_name, 'page': page})

    """
    爬取美团：详情-景区信息
    """

    def spot_detail_basic(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        area_pinyin = response.meta['area_pinyin']
        area_name = response.meta['area_name']
        token = response.meta['token']
        response_data = json.loads(response.body.decode('utf-8'))

        # 爬取美团：详情-商品（商户）信息
        url = self.base_detail_business_url.format(ota_spot_id=ota_spot_id, token=token)
        yield Request(url=url, callback=self.spot_detail_business, dont_filter=True,
                      meta={'ota_spot_id': ota_spot_id, 'area_pinyin': area_pinyin, 'area_name': area_name,
                            'token': token, 'data': {'detail_basic': response_data}})

    """
    爬取美团：详情-商品信息
    """

    def spot_detail_business(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        area_pinyin = response.meta['area_pinyin']
        area_name = response.meta['area_name']
        token = response.meta['token']
        data = response.meta['data']

        response_data = json.loads(response.body.decode('utf-8'))
        data['detail_business'] = response_data

        # 爬取美团：详情-评论信息
        url = self.base_detail_comment_url.format(ota_spot_id=ota_spot_id, token=token)
        yield Request(url=url, callback=self.spot_detail_comment, dont_filter=True,
                      meta={'ota_spot_id': ota_spot_id, 'area_pinyin': area_pinyin, 'area_name': area_name,
                            'token': token, 'data': data})

    """
    爬取美团：详情-评论信息
    """

    def spot_detail_comment(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        area_pinyin = response.meta['area_pinyin']
        area_name = response.meta['area_name']
        data = response.meta['data']
        response_data = json.loads(response.body.decode('utf-8'))
        data['detail_comment'] = response_data

        city_id = data['detail_basic']['poiBasicInfo']['poiInfo']['cityId'] if 'poiInfo' not in data['detail_basic']['poiBasicInfo'] else 0

        url = self.base_detail_info_url.format(ota_spot_id=ota_spot_id, city_id=city_id)
        yield Request(url=url, callback=self.spot_detail_info, dont_filter=True,
                      meta={'ota_spot_id': ota_spot_id, 'area_pinyin': area_pinyin, 'area_name': area_name,
                            'data': data})

    """
    抓取 景区详情 （预订须知 景点介绍）
    """

    def spot_detail_info(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        area_pinyin = response.meta['area_pinyin']
        area_name = response.meta['area_name']
        data = response.meta['data']
        response_data = json.loads(response.body.decode('utf-8'))
        data['detail_info'] = response_data

        spot_city = spot.SpotCity.objects(ota_id=OTA.OtaCode.MEITUAN.value.id,
                                          ota_spot_id=response.meta['ota_spot_id']).first()
        # 不存在数据则新增数据,增量爬取
        if not spot_city:
            spot_city = spot.SpotCity()
            spot_city.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        spot_city.ota_spot_id = ota_spot_id
        spot_city.ota_id = OTA.OtaCode.MEITUAN.value.id

        spot_city.city_id = data['detail_basic']['poiBasicInfo']['poiInfo']['cityId']
        spot_city.area_pinyin = area_pinyin
        spot_city.area_name = area_name
        spot_city.city_name = data['detail_basic']['poiBasicInfo']['poiInfo']['cityName']

        spot_city.s_img = data['detail_basic']['poiBasicInfo']['poiInfo']['frontImg'].replace('w.h', '1080.0')
        spot_city.s_name = data['detail_basic']['poiBasicInfo']['poiInfo']['name']
        spot_city.s_notes = data['detail_info']['data']['tabContents']['noticeTab']
        spot_city.s_desc = data['detail_info']['data']['tabContents']['descTab']
        spot_city.s_level = data['detail_basic']['poiBasicInfo']['poiInfo']['tourPlaceStar'][0: 2] if 'tourPlaceStar' in \
                                                                                                      data[
                                                                                                          'detail_basic'][
                                                                                                          'poiBasicInfo'][
                                                                                                          'poiInfo'] else ''
        spot_city.s_score = float(data['detail_comment']['data']['avgscore'])
        spot_city.s_comment_num = data['detail_comment']['data']['totalcomment']
        spot_city.s_ticket_num = data['detail_business']['deals']['count']
        spot_city.s_ticket = data['detail_business']['deals']['data']
        spot_city.s_addr = data['detail_basic']['poiBasicInfo']['poiInfo']['addr']
        spot_city.lat = data['detail_basic']['poiBasicInfo']['poiInfo']['lat']
        spot_city.lng = data['detail_basic']['poiBasicInfo']['poiInfo']['lng']

        spot_city.s_sale_num = 0  # todo:销售数量跟着票型来
        for ticket in spot_city.s_ticket:
            if ticket['productType'] == 'MT_TJ':
                continue
            for ticket_item in ticket['productModels']:
                if 'newSoldsString' in ticket_item and ticket_item['newSoldsString'][2:].strip('+'):
                    if '万' in ticket_item['newSoldsString']:
                        spot_city.s_sale_num += float(ticket_item['newSoldsString'][2:].strip('+').strip('万')) * 10000
                    else:
                        spot_city.s_sale_num += int(ticket_item['newSoldsString'][2:].strip('+'))

        spot_city.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        yield spot_city
        print('=' * 20, '爬取的景区：', spot_city.city_id, spot_city.city_name, spot_city.area_name, spot_city.area_pinyin,
              spot_city.s_name)

    """
    编码美团token
    """

    @classmethod
    def encode_token(cls, token: str, ota_spot_id) -> str:
        token_str = cls.decode_token(token)
        token_dict = json.loads(token_str)
        ts = int(datetime.now().timestamp() * 1000)
        token_dict['ts'] = ts
        token_dict['cts'] = ts + 100 * 1000
        token_dict['bI'] = cls.base_detail_referer_url.format(ota_spot_id=ota_spot_id)
        encode = str(token_dict).encode()  # 二进制编码
        compress = zlib.compress(encode)  # 二进制压缩
        b_encode = base64.b64encode(compress)  # base64编码
        u_code = parse.quote(b_encode)  # url编码
        return u_code

    """
    解码美团token
    """

    @classmethod
    def decode_token(cls, token: str) -> str:
        token = parse.unquote(parse.unquote(token))
        # base64解码
        token_decode = base64.b64decode(token)
        # 二进制解压
        token_string = zlib.decompress(token_decode)
        return token_string


class MeituanPrice(scrapy.Spider):
    name = 'meituan_price'
    allowed_domains = ['i.meituan.com']
    base_url = r'https://itrip.meituan.com/volga/api/v3/trip/poi/business/info/{ota_spot_id}?ct_poi=190361606798914361847646491438431785905_e7283630514797780583_c5_dtrippoipolyb&poiId=1515791&source=mt&client=wap&uuid=3F1B3AB7262A309B279A62C912513D18CEF869AD324DF8263D921F91967B162B&cityId=70&feclient=lvyou_wap&platform=5&partner=11&originUrl=https%3A%2F%2Fi.meituan.com%2Fawp%2Fh5%2Flvyou%2Fpoi%2Fdetail%2Findex.html%3Fct_poi%3D190361606798914361847646491438431785905_e7283630514797780583_c5_dtrippoipolyb%26poiId%3D1515791&_token=eJytUltr5CAU%252Fi9C%252BhSixlscCGWgdMlCH1ravgwlZNSdkSYaEtN2KP3vPemF3X3YtwXxO5dPz%252Fk8vqKpsWhDCSG0zNGTm9AG0YIUEuUozZARSnGtFdGiBIL5MwanBM%252FRfrq%252FQJudEiSnjPGHNXIDgR1TIpdSPeS%252FrZLDWhkNENAxpXHeYOyLwfm0dKEwccDd84iPAvdPp7jgMXpsXep8j32w7qU4pqE%252FN6mFRE01YZJKIpWuNOVgV1xJLvnqVJxRVQlNROtUWTHJiKBcaaUqIirWGtHaNPkRLhpjf9qfgdHYmgqQpynI%252F0d3xsQlJNzHgw%252Fn%252B848LlNfr9yMbbPyEtZfB8BfqwB8CAKMk3UT4H45wT6kNfehLWOXn8IydvFfpWWlnOMyGQcXDwk803sXEnjPHVSXMPbZx9CGblgpCzTzywdnIWVd1zcWgtAK1IUeEIxvuIXxAT5%252BYfeF6du%252Fgm8ETzj7QwDL%252FXy5vTs02%252B2Pw%252Fbmuq7R2zvWCreX'
    Info_urls = r'https://itrip.meituan.com/volga/api/v3/trip/poi/basic/info/{ota_spot_id}?=&poiId={ota_spot_id}'
    start_urls = ['https://i.meituan.com/awp/h5/lvyou/poi/detail/index.html?&poiId=1515791']

    def parse(self, response: HtmlResponse):
        price.OPrice.objects(ota_id=OTA.OtaCode.MEITUAN.value.id).delete()
        price.OPriceCalendar.objects(ota_id=OTA.OtaCode.MEITUAN.value.id, create_at=time.strftime("%Y-%m-%d", time.localtime())).delete()
        print('start_request')
        for ota_spot_id in MeituanSpider.ota_spot_ids:
            # 更新景区的详情
            url = self.Info_urls.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True, meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        ota_spot_name = ''
        if 'poiInfo' in json_data['poiBasicInfo']:
            ota_spot_name = json_data['poiBasicInfo']['poiInfo']['name']

        url = self.base_url.format(ota_spot_id=ota_spot_id)
        yield Request(url=url, callback=self.meituan_price, dont_filter=True,
                      meta={'ota_spot_id': ota_spot_id, 'ota_spot_name': ota_spot_name})

    def meituan_price(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        ota_spot_name = response.meta['ota_spot_name']
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        if 'deals' in json_data and 'data' in json_data['deals']:  ## 数据不为空
            data = json_data['deals']['data']
            for k1, v1 in enumerate(data):
                lowPrice = ''
                type_name = ''
                o_price = price.OPrice()
                o_price.ota_id = OTA.OtaCode.MEITUAN.value.id
                o_price.ota_spot_id = ota_spot_id
                o_price.ota_spot_name = ota_spot_name
                o_price.ota_product = []
                o_price.create_at = time.strftime("%Y-%m-%d", time.localtime())
                ota_product = {}
                type_key = ''
                sale_num = 0
                normal_price = 0

                if v1['productName'] == '门票':  ## 门票数据
                    for k2, v2 in enumerate(v1['productModels']):
                        if 'lowPrice' in v2 and 'ticketName' in v2:
                            lowPrice = v2['lowPrice']
                            type_name = v2['ticketName']
                            type_key = v2['ticketName']
                        if 'ticketDeals' in v2:
                            for k3, v3 in enumerate(v2['ticketDeals']):
                                # normal_price = v3['value']
                                tickets_list = {
                                    'price_id': str(v3['id']),
                                    'title': v3['title5'],
                                    'price': v3['price'],
                                    'cash_back': 0,
                                    'cut_price': 0
                                }
                                ota_product = {'type_key': type_key, 'normal_price': normal_price, 'sale_num': sale_num,
                                               'type_id': v3['id'], 'type_name': type_name,'link_url': self.base_url, 'tickets': []}
                                ota_product['tickets'].append(tickets_list)
                                if '已售' in v3['newSoldsString']:
                                    if '万' in v3['newSoldsString']:
                                        sale_num = re.findall(r"\d+\.?\d*", v3['newSoldsString'])
                                        sale_num = float(sale_num[0]) * 10000
                                    else:
                                        sale_num = re.findall(r"\d+\.?\d*", v3['newSoldsString'])
                                        sale_num = float(sale_num[0])

                                price_calendar = price.OPriceCalendar()
                                price_calendar.ota_id = OTA.OtaCode.MEITUAN.value.id
                                price_calendar.ota_spot_id = response.meta['ota_spot_id']
                                price_calendar.type_key = type_key
                                price_calendar.type_name = type_name
                                price_calendar.pre_price = v3['price']
                                price_calendar.ota_spot_name = ota_spot_name
                                price_calendar.create_at = time.strftime("%Y-%m-%d", time.localtime())
                                yield price_calendar
                                print('正在添加 ', ota_spot_name, ' 价格日历', "*" * 20)

                            o_price.lowPrice = lowPrice
                            o_price.ota_product.append(ota_product)
                            print('正在添加 ', ota_spot_name, ' 的票型价格详情.OTA_id', OTA.OtaCode.MEITUAN.value.id, "*" * 20)
                            yield o_price
