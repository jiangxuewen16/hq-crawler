import datetime
import json

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import helper
from spiders.common.marketing import WeMedia, WeMediaType


class SougouSpider(scrapy.Spider):
    name = 'sougou'
    allowed_domains = ['mp.sogou.com']
    start_urls = ['http://mp.sogou.com/']
    base_url = 'https://www.toutiao.com/'
    we_media_id = WeMedia.SOGOU.value.id
    we_media_type = WeMediaType.WE_MEDIA.value.id
    cookie_list = {}

    def parse(self, response):
        result = helper.get_media_account(self)
        for detail in result:
            [account, cookie_list] = detail
            start = end = helper.get_yesterday()
            article_url = r'http://mp.sogou.com/api/statistics/arti-analysis/sum?startDate={start}&endDate={end}'
            yield Request(url=article_url.format(start=start, end=end), callback=self.article_analysis,
                          dont_filter=True, cookies=cookie_list, meta={'account': account})

    def article_analysis(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        total_info = json.loads(response_str)
        account = response.meta['account']
        account.exposure_num = (0 if account.exposure_num is None else account.exposure_num) + \
                               (total_info['recommendedNum'] + total_info['readingNum'])
        account.recommend_num = (0 if account.recommend_num is None else account.recommend_num) + \
                                (total_info['recommendedNum'])
        account.read_num = (0 if account.read_num is None else account.read_num) + total_info['readingNum']
        account.forward_num = (0 if account.forward_num is None else account.forward_num) + total_info['sharedNum']
        account.like_num = 0
        account.comment_num = (0 if account.comment_num is None else account.comment_num) + total_info['commentsNum']
        account.publish_num = (0 if account.publish_num is None else account.publish_num) + total_info['articleNum']
        account.sex_proportion = {
            'man': 0,
            'women': 0,
            'unknown': 100
        }
        account.age_proportion = {
            '<24': 0,
            '25-39': 0,
            '>40': 0,
            'unknown': 100
        }
        fans_analysis_url = r'http://mp.sogou.com/api/statistics/fans-analysis/{day}'
        yield Request(url=fans_analysis_url.format(day=helper.get_yesterday()), callback=self.fans_analysis,
                      dont_filter=True, cookies=self.cookie_list, meta={'account': account})

    def fans_analysis(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        fans_info = json.loads(response_str)
        account = response.meta['account']
        account.follow_num = (0 if account.follow_num is None else account.follow_num) + fans_info['subscribe']
        start = end = helper.get_yesterday(2)
        yield Request(url='http://mp.sogou.com/api/income/withdraw/sum'.format(start=start, end=end),
                      callback=self.income_analysis, dont_filter=True, cookies=self.cookie_list,
                      meta={'account': account})

    @staticmethod
    def income_analysis(response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        income_info = json.loads(response_str)
        account = response.meta['account']
        account.total_income = income_info['totalAmount']
        account.drawing = income_info['paidAmount']
        account.balance = income_info['withdrawableAmount']
        account.account_home = 'http://mp.sogou.com/dashboard'
        account.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        account.create_at = datetime.datetime.now().strftime('%Y-%m-%d')
        yield account
