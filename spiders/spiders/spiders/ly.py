# -*- coding: utf-8 -*-
import json
import math
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.price import price
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

    def parse(self, response):
        pass


class LySpotSpider(scrapy.Spider):
    name = 'ly_spot'
    allowed_domains = ['www.ly.com']
    base_url = r'https://www.ly.com/scenery/BookSceneryTicket_{ota_spot_id}.html'
    start_urls = ['https://www.ly.com/scenery/BookSceneryTicket_9513.html']

    def parse(self, response: HtmlResponse):
        for ota_spot_id in LySpider.ota_spot_ids:
            start_page = 1
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            referer = 'https://www.mafengwo.cn/poi/339.html'  # 这里随便马蜂窝任何url
            yield Request(url=url, headers=LySpider.build_headers(referer), cookies={},
                          callback=self.parse_item,
                          dont_filter=True, meta={'page': start_page, 'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        spot_data = spot.Spot.objects(ota_id=OTA.OtaCode.MAFENGWO.value.id,
                                      ota_spot_id=response.meta['ota_spot_id']).first()
        # 不存在数据则新增数据
        if not spot_data:
            spot_data = Spot()
            spot_data.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        spot_data.ota_spot_id = response.meta['ota_spot_id']

        spot_data.ota_id = OTA.OtaCode.MAFENGWO.value.id
        spot_data.spot_name = response.xpath('/html/body/div[2]/div[2]/div/div[3]/h1/text()').extract_first()
        desc = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/text()').extract_first()
        spot_data.desc = desc.strip() if desc else ''
        spot_data.tel = response.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[1]/div[2]/text()').extract_first()
        spot_data.traffic = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[1]/dd/div[1]/text()').extract_first()
        spot_data.ticket_num = 1
        spot_data.open_time = response.xpath('/html/body/div[2]/div[3]/div[2]/dl[3]/dd/text()').extract_first()
        spot_data.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # spot_data.comment_num = \
        #    response.xpath('//*[@id="poi-navbar"]/ul/li[3]/a/span/text()').extract_first().split('条')[0].strip('（')

        yield spot_data


class LyCommentSpider(scrapy.Spider):
    name = 'ly_comment'
    allowed_domains = ['www.ly.com']
    # 默认爬取最新 labId= 1：全部  2：好评 3：中评  4：差评 5：有图  6：最新
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

    def spot_comment(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        comment = json.loads(response_str)
        ly_total = 0
        if 'dpList' in comment:
            ly_total = comment['totalNum']
        now_total = spot.SpotComment.objects(ota_id=OTA.OtaCode.LY.value.id,
                                             ota_spot_id=response.meta['ota_spot_id']).count()
        to_save_total = ly_total - now_total
        page_size = LyCommentSpider.page_size
        if to_save_total > 0:
            total_page = math.ceil(to_save_total / page_size)
            for page_num in range(1, total_page + 1):
                print('当前页 ', page_num, "-", '总页数 ', total_page, "-" * 20)

                url = self.base_url.format(ota_spot_id=response.meta['ota_spot_id'], page_num=page_num,
                                           page_size=page_size)
                yield Request(url=url, callback=self.parse_item, dont_filter=True,
                              meta={'page_num': page_num, 'ota_spot_id': response.meta['ota_spot_id']})

    def parse_item(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        page_num = response.meta['page_num']
        ota_spot_id = response.meta['ota_spot_id']

        total_page = json_data['pageInfo']['totalPage']

        for item in json_data['dpList']:
            print('正在添加 ', item['dpUserName'], ' 的评论', "*" * 20)
            spot_comment = spot.SpotComment()
            spot_comment.ota_id = OTA.OtaCode.LY.value.id
            spot_comment.ota_spot_id = ota_spot_id
            spot_comment.goods_name = item['DPItemName']
            spot_comment.goods_id = item['DPItemId']
            spot_comment.u_name = item['dpUserName']
            spot_comment.u_avatar = item['memberHeaderImgUrl']
            # spot_comment.u_avg_price = item['avgPrice']
            spot_comment.u_level = item['DPUserLevel']

            # spot_comment.c_tag = item['dpTagList']
            spot_comment.c_content = item['dpContent']
            if item['lineAccess'] == '好评':
                spot_comment.c_score = float(5)
            elif item['lineAccess'] == '中评':
                spot_comment.c_score = float(4)
            elif item['lineAccess'] == '差评':
                spot_comment.c_score = float(1)
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


class LySpotCity(scrapy.Spider):
    name = 'ly_price'
    allowed_domains = ['www.ly.com']
    base_url = r'https://www.ly.com/scenery/AjaxHelper/SceneryPriceFrame.aspx?action=GETNEWPRICEFRAMEFORLAST&ids={ota_spot_id}&isSimple=1&isShowAppThree=0&widthtype=1&isGrap=1&nobookid=&isyry=1&YpState=1&lon=null&lat=null&isforegin=null&iid=0.9687010629933097'
    start_urls = ['https://m.ly.com/scenery/scenerydetail_9513_0_0.html']

    def parse(self, response: HtmlResponse):
        price.OPrice.objects(ota_id=OTA.OtaCode.LY.value.id).delete()
        price.OPriceCalendar.objects(ota_id=OTA.OtaCode.LY.value.id, create_at=time.strftime("%Y-%m-%d", time.localtime())).delete()
        print('start_request')
        for ota_spot_id in LySpider.ota_spot_ids:
            # 更新景区的详情
            url = self.base_url.format(ota_spot_id=ota_spot_id)
            yield Request(url=url, callback=self.parse_item, dont_filter=True,
                          meta={'ota_spot_id': ota_spot_id})

    def parse_item(self, response: HtmlResponse):
        ota_spot_id = response.meta['ota_spot_id']
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        spot_city = spot.SpotCity.objects(ota_id=OTA.OtaCode.LY.value.id,
                                          ota_spot_id=ota_spot_id).first()

        # 不存在数据则新增数据,增量爬取
        if not spot_city:
            if 'SceneryPrices' in json_data:
                for k1, v1 in enumerate(json_data['SceneryPrices']):
                    ota_product = []
                    type_key = v1['DestinationName']
                    spot_name = v1['DestinationName']
                    for k2, v2 in enumerate(v1['ChannelPriceModelEntityList']):
                        type_name = v2['ConsumersTypeName']
                        for k3, v3 in enumerate(v2['ChannelPriceEntityList']):
                            tickets_list = {
                                'price_id': v3['PriceId'],
                                'title': v3['TicketName'],
                                'price': v3['DAmountAdvice'],
                                'cash_back': 0,
                                'cut_price': 0
                                            }

                            ota_entity_list = {'type_key': type_key,'normal_price': v3['AmountAdvice'], 'type_id': v3['TicketTypeId'],
                                               'type_name': type_name, 'sale_num': v3['OrderNumber'], 'tickets': tickets_list}
                            ota_product.append(ota_entity_list)

                            price_calendar = price.OPriceCalendar()
                            price_calendar.ota_id = OTA.OtaCode.LY.value.id
                            price_calendar.ota_spot_id = response.meta['ota_spot_id']
                            price_calendar.type_key = type_name
                            price_calendar.type_name = v3['TicketName']
                            price_calendar.ota_spot_name = spot_name
                            price_calendar.create_at = time.strftime("%Y-%m-%d", time.localtime())
                            price_calendar.save(force_insert=False, validate=False, clean=True)
                            print('正在添加 ', v1['DestinationName'], ' 价格日历', "*" * 20)

                    o_price = price.OPrice()
                    o_price.ota_id = OTA.OtaCode.LY.value.id
                    o_price.ota_spot_id = response.meta['ota_spot_id']
                    o_price.ota_product = ota_product
                    o_price.ota_spot_name = spot_name
                    o_price.create_at = time.strftime("%Y-%m-%d", time.localtime())
                    print('正在添加 ', v1['DestinationName'], ' 的票型详情.OTA_id', OTA.OtaCode.LY.value.id, "*" * 20)
                    yield o_price


