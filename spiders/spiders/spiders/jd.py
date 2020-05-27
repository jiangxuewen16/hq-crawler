import re
import time

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from spiders.common import OTA
from spiders.items.price import price


class JdSpiderPrice(scrapy.Spider):
    # 因为是查的关键字 没有固定的景区 景区id随机生成
    ota_spot_keywords = {
        1239031123: '迪士尼门票'
    }
    name = 'jd_spot_price'
    allowed_domains = ['search.jd.com', 'item.jd.com', 'menpiao.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword={keyword}&wq={keyword}&page={page}&s=09001500210&click=0']
    sku_detail_url = 'https://item.jd.com/{sku}.html'

    def start_requests(self):
        for spot_keyword_key in self.ota_spot_keywords:
            url = self.start_urls[0].format(keyword=self.ota_spot_keywords[spot_keyword_key], page=1)
            yield Request(url=url, dont_filter=True,
                          meta={'keyword': self.ota_spot_keywords[spot_keyword_key],
                                'current_page': 1, 'ota_spot_id': spot_keyword_key})

    def parse(self, response):
        current_page = response.meta['current_page'] if 'current_page' in response.meta else 1
        count_page = response.meta['count_page'] if 'count_page' in response.meta else self.count_page(response)
        keyword = response.meta['keyword']
        if current_page < int(count_page):
            current_page = current_page + 1
            url = self.start_urls[0].format(keyword=keyword, page=current_page)
            yield Request(url=url, callback=self.parse, dont_filter=True,
                          meta={'current_page': current_page, 'count_page': count_page,
                                'keyword': keyword, 'ota_spot_id': response.meta['ota_spot_id']})
        # 跳转至内页
        goods_list = response.css('#J_goodsList > ul > li > div').extract()
        for goods in goods_list:
            selector = Selector(text=goods)
            href = 'https:' + selector.xpath('/html/body/div/div[1]/a/@href').extract_first()
            yield Request(url=href, callback=self.request_inside, dont_filter=True,
                          meta={'current_page': current_page, 'count_page': count_page,
                                'ota_spot_id': response.meta['ota_spot_id'],
                                'keyword': keyword, 'dont_redirect': True, "handle_httpstatus_list": [301, 302]})

    @staticmethod
    def count_page(response):
        response_str = response.body.decode('utf-8')
        match = re.search('SEARCH.adv_param={page:"1",page_count:"(\\d+)"', response_str)
        page_count = match.group(1)
        return page_count

    def request_inside(self, response: HtmlResponse):
        sku_list = response.xpath('//*[@id="choose-attr-1"]/div/div/@data-sku').extract()
        if sku_list:
            for sku in sku_list:
                yield Request(url=self.sku_detail_url.format(sku=sku), callback=self.parse_inside, dont_filter=True,
                              meta={'sku': sku, 'keyword': response.meta['keyword'],
                                    'ota_spot_id': response.meta['ota_spot_id']})

    def parse_inside(self, response: HtmlResponse):
        o_price = price.OPrice.objects(ota_id=OTA.OtaCode.JD.value.id, ota_spot_id=response.meta['ota_spot_id']).first()
        flag = False
        if not o_price:
            o_price = price.OPrice()
            o_price.ota_id = OTA.OtaCode.JD.value.id
            o_price.ota_spot_id = response.meta['ota_spot_id']
            o_price.ota_spot_name = self.ota_spot_keywords[o_price.ota_spot_id]
            o_price.ota_product = []
        else:
            for product in o_price.ota_product:
                if product['type_id'] == response.meta['sku']:
                    flag = True
                    break
        o_price.create_at = time.strftime("%Y-%m-%d", time.localtime()).format('')
        type_key = response.css('#choose-attr-1 > div.dd > div.item.selected > a > i::text').extract_first() \
            .replace('\n', '').strip()
        type_name = response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').extract_first() \
            .replace('\n', '').strip()
        ticket_price = response.css('.J-p-' + response.meta['sku'] + '::text').extract_first(),
        tickets = {
            'type_id': response.meta['sku'],
            'type_key': type_key,
            'type_name': type_name.replace('\n', '').strip(),
            'normal_price': 0,
            'tickets': [
                {
                    'price_id': response.meta['sku'],
                    'title': type_name.replace('\n', '').strip(),
                    'price': response.xpath('/html/body/div[6]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]/span['
                                            '2]/text()').extract_first(),
                    'cash_back': 0,
                    'cut_price': 0,
                    'sale_num': 0,
                    'url': response.url
                }
            ]
        }
        if flag:
            o_price.ota_product.append(tickets)
            yield o_price
        else:
            price.OPrice.objects(ota_id=OTA.OtaCode.JD.value.id,
                                 ota_spot_id=response.meta['ota_spot_id'],
                                 ota_product__type_id=response.meta['sku']).update_one(
                set__ota_product=tickets,
                set__update_at=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        o_price_calendar = price.OPriceCalendar()
        o_price_calendar.ota_id = response.meta['ota_spot_id']
        o_price_calendar.ota_spot_id = response.meta['ota_spot_id']
        o_price_calendar.ota_spot_name = self.ota_spot_keywords[o_price.ota_spot_id]
        o_price_calendar.type_id = response.meta['sku']
        o_price_calendar.pre_price = ticket_price
        o_price_calendar.create_at = time.strftime("%Y-%m-%d", time.localtime()).format('')
        o_price_calendar.type_key = type_key
        o_price_calendar.type_name = type_name
        o_price_calendar.normal_price = 0
        yield o_price_calendar

