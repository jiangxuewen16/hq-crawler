# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.spot import spot


class CtripSpider(scrapy.Spider):
    name = 'ctrip'
    allowed_domains = ['www.ctrip.com']
    start_urls = ['https://www.ctrip.com/']
    ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.CTRIP)  # ota 景区id列表

    @classmethod
    def build_request_data(cls, ota_spot_id, page, limit) -> dict:
        return {"pageid": 10650000804, "viewid": ota_spot_id, "tagid": 0, "pagenum": page, "pagesize": limit,
                "contentType": "json",
                "head": {"appid": "100013776", "cid": "09031111211651836922", "ctok": "", "cver": "1.0",
                         "lang": "01", "sid": "8888", "syscode": "09", "auth": "",
                         "extension": [{"name": "protocal", "value": "https"}]}, "ver": "7.10.3.0319180000"}

    @classmethod
    def build_request_city_spot_list(cls, city_id: int, page: int, page_size: int) -> dict:
        return {"pageid": 10320662472, "searchtype": 1, "districtid": city_id, "needfact": False, "sort": 1,
                "pidx": page,
                "isintion": True, "psize": page_size, "imagesize": "C_190_190", "reltype": 1,
                "assistfilter": {"userChooseSite": str(city_id)}, "spara": "", "filters": [], "excepts": [],
                "abtests": [],
                "extendAssociation": [{"key": "srhtraceid", "value": "46c1b092-284f-bdfc-56f3-156811484e94"}],
                "contentType": "json",
                "head": {"cid": "09031136211815241931", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                         "syscode": "09", "auth": "", "extension": [{"name": "protocal", "value": "https"}]},
                "ver": "7.14.2"}

    def parse(self, response: HtmlResponse):
        pass


"""
景区数据
"""


class CtripSpotSpider(scrapy.Spider):
    name = 'ctrip_spot'
    allowed_domains = ['www.ctrip.com']
    base_url = r'https://piao.ctrip.com/ticket/dest/t{ota_spot_id}.html'
    start_urls = ['https://piao.ctrip.com/ticket/dest/t62931.html']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in CtripSpider.ota_spot_ids:
            # 获取景区页面数据
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.CTRIP.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()

        # 不存在数据则新增数据
        if not spot_data:
            spot_data = spot.Spot()
            spot_data.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # spot_data.spot_id = OTA.OtaSpotIdMap.get_ota_spot_id(OTA.OtaSpotIdMap.SHI_YAN_HU.name, OTA.OtaCode.HUIQULX)
        spot_data.ota_spot_id = response.meta['ota_spot_id']

        spot_data.ota_id = OTA.OtaCode.CTRIP.value.id
        spot_data.spot_name = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/h2/text()').extract_first()

        spot_imgs = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/ul/li')
        spot_data.spot_img = []
        for img in spot_imgs:
            spot_data.spot_img.append(img.xpath('/a/img[@src]').extract_first())

        spot_data.desc = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[5]/div[1]/div[3]/div[2]').get()
        # spot_data.tel = ????
        spot_data.traffic = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[5]/div[1]/div[4]/div[3]/p/text()').extract()
        spot_data.ticket_num = 1
        spot.addr = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/ul/li[1]/span/text()').extract_first()
        spot_data.open_time = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/ul/li[2]/span/text()').extract_first()
        spot_data.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        spot_data.comment_num = response.xpath(
            '//*[@id="root"]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/a/text()').extract_first().strip(
            '查看条点评')
        # print('='*20, spot_data.to_json())
        yield spot_data


"""
景区评论数据
"""


class CtripCommentSpider(scrapy.Spider):
    name = 'ctrip_comment'
    allowed_domains = ['www.ctrip.com', 'sec-m.ctrip.com']
    page_size = 10  # 默认每页爬取数量
    start_urls = ['https://sec-m.ctrip.com/restapi/soa2/12530/json/viewCommentList']

    def start_requests(self):
        request_data = CtripSpider.build_request_data(ota_spot_id='62931', page=1, limit=1)
        yield Request(self.start_urls[0], method="POST", body=json.dumps(request_data),
                      headers={'Content-Type': 'application/json'},
                      callback=self.parse)

    def parse(self, response: HtmlResponse):
        for ota_spot_id in CtripSpider.ota_spot_ids:
            # 获取景区评论数据
            page = 1
            request_data = CtripSpider.build_request_data(ota_spot_id=ota_spot_id, page=page, limit=1)
            yield Request(url=self.start_urls[0], callback=self.parse_count, dont_filter=True,
                          method="POST",
                          body=json.dumps(request_data),
                          headers={'Content-Type': 'application/json'},
                          meta={'ota_spot_id': ota_spot_id})

        # 统计评论，增量爬取

    def parse_count(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        ota_spot_id = response.meta['ota_spot_id']
        new_total = json_data['data']['cmtquantity']

        spot_info = spot.Spot.objects(ota_id=OTA.OtaCode.CTRIP.value.id, ota_spot_id=ota_spot_id)
        spot_info.update(set__comment_num=new_total)

        comment_num = spot.SpotComment.objects(ota_id=OTA.OtaCode.CTRIP.value.id, ota_spot_id=ota_spot_id).count()
        new_num = new_total - comment_num
        if new_num <= 0:  # 没有新评论的情况下不需要做任何处理
            return

        page_size = self.page_size
        if new_num < self.page_size:
            page_size = new_num

        page = 1
        print('x' * 15, new_total, comment_num, new_num, ota_spot_id)
        request_data = CtripSpider.build_request_data(ota_spot_id=ota_spot_id, page=page, limit=page_size)
        yield Request(url=self.start_urls[0], callback=self.parse_page, dont_filter=True,
                      method="POST",
                      body=json.dumps(request_data),
                      headers={'Content-Type': 'application/json'},
                      meta={'page': page, 'data_num': new_num, 'ota_spot_id': ota_spot_id,
                            'page_size': page_size})

    def parse_page(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        data_num = response.meta['data_num']
        page_size = response.meta['page_size']
        ota_spot_id = response.meta['ota_spot_id']
        page = response.meta['page']

        print('x' * 30, page, len(json_data['data']['comments']))
        for item in json_data['data']['comments']:
            spot_comment = spot.SpotComment()

            spot_comment.ota_id = OTA.OtaCode.CTRIP.value.id
            spot_comment.ota_spot_id = ota_spot_id
            spot_comment.goods_name = item['commentOrderInfo']
            # spot_comment.goods_id = item['did']

            spot_comment.u_name = item['uid']
            spot_comment.u_avatar = item['userImage']
            # spot_comment.u_avg_price = item['avgPrice']
            # spot_comment.u_level = item['userLevel']

            spot_comment.c_id = item['id']
            spot_comment.c_content = item['content']
            spot_comment.c_score = item['score']
            spot_comment.c_img = [img for img in item['simgs']] if ('simgs' in item) and item['simgs'] else []

            spot_comment.create_at = item['date']

            # spot_comment.c_useful_num = item['zanCnt']
            # spot_comment.c_reply_num = item['replyCnt']
            # spot_comment.c_from = '美团网'

            yield spot_comment

        data_num -= page_size
        page += 1
        if data_num > 0:
            page_size = self.page_size
            if data_num < self.page_size:
                page_size = data_num
            print('============', data_num, page, page_size, ota_spot_id)
            request_data = CtripSpider.build_request_data(ota_spot_id=ota_spot_id, page=page, limit=page_size)
            print('x' * 30, request_data)
            yield Request(url=self.start_urls[0], callback=self.parse_page, dont_filter=True,
                          method="POST",
                          body=json.dumps(request_data),
                          headers={'Content-Type': 'application/json'},
                          meta={'page': page, 'data_num': data_num, 'ota_spot_id': ota_spot_id,
                                'page_size': page_size})


class CtripCitySpot(scrapy.Spider):
    name = 'ctrip_city_spot'
    allowed_domains = ['m.ctrip.com', 'sec-m.ctrip.com']

    page_size = 20

    start_urls = ['https://m.ctrip.com/webapp/ticket/citylist']  # 获取美团地区列表

    base_page_url = 'https://sec-m.ctrip.com/restapi/soa2/12530/json/ticketSpotSearch?_fxpcqlniredt=09031136211815241931'

    def parse(self, response: HtmlResponse):
        city_json_str = \
        response.body.decode('utf-8').split('window.__INITIAL_STATE__ = ', 1)[1].split('window.__APP_SETTINGS__', 1)[0]
        city_json = json.loads(city_json_str)
        city_json = city_json['citymap']
        # city_json = city_json['cityList']

        # for _, item in city_json.items():
        #     if item['ctyid'] == 110000:
        #         area_pinyin = item['py']
        #         area_id = item['districtid']
        #         area_name = item['name']
        #
        #         page = 1
        #         url = self.base_page_url
        #         print('=' * 20, '爬取的地址：', url)
        #         request_data = CtripSpider.build_request_city_spot_list(area_id, page, self.page_size)
        #         yield Request(url=url, callback=self.parse_page, dont_filter=True,
        #                       method="POST",
        #                       body=json.dumps(request_data),
        #                       headers={'Content-Type': 'application/json'},
        #                       meta={'area_pinyin': area_pinyin, 'area_name': area_name, 'page': page,
        #                             'area_id': area_id})

        area_pinyin = 'changsha'
        area_id = 148
        area_name = '长沙'

        page = 1
        url = self.base_page_url
        print('=' * 20, '爬取的地址：', url)
        request_data = CtripSpider.build_request_city_spot_list(area_id, page, self.page_size)
        yield Request(url=url, callback=self.parse_page, dont_filter=True,
                      method="POST",
                      body=json.dumps(request_data),
                      headers={'Content-Type': 'application/json'},
                      meta={'area_pinyin': area_pinyin, 'area_name': area_name, 'page': page,
                            'area_id': area_id})

    def parse_page(self, response: HtmlResponse):
        area_pinyin = response.meta['area_pinyin']
        area_id = response.meta['area_id']
        area_name = response.meta['area_name']
        page = response.meta['page']
        area_id = response.meta['area_id']

        json_str = response.body.decode('utf-8')
        json_data = json.loads(json_str)
        spot_list = json_data['data']['viewspots']
        for spot in spot_list:
            pass



