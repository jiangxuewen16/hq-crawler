import datetime
import json
import math
import re

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common.marketing import WeMedia, WeMediaType
from spiders.items import marketing
from spiders.items.marketing import Article
from spiders.items.spot import spot


class JinritoutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['www.toutiao.com/']
    start_urls = ['https://mp.toutiao.com']
    base_url = 'https://www.toutiao.com/'
    we_media_id = WeMedia.TOU_TIAO.value.id
    we_media_type = WeMediaType.WE_MEDIA.value.id
    cookie_list = {}

    @classmethod
    def get_account(cls):
        account_list = marketing.Account.objects(platform=cls.we_media_id).all()
        if len(account_list):
            for account in account_list:
                account.authorization_information = 'tt_webid=6773521543516882439; msh=8olTxl_MwSOv6HB7b3T0nVvUP9Y; SLARDAR_WEB_ID=9c24d10f-9b96-474c-b8e6-c2d6245ab024; sso_uid_tt=a0d0203f5d66f5cb6a8f30f62c2132b3; toutiao_sso_user=13a4d27660bdf84dbab3fd3accf57d2b; sid_guard=b33df05a325a059b678eaa879bfb1f76%7C1577450650%7C5184000%7CTue%2C+25-Feb-2020+12%3A44%3A10+GMT; uid_tt=9a0b60ee7786871417064706412d3d67; sid_tt=b33df05a325a059b678eaa879bfb1f76; sessionid=b33df05a325a059b678eaa879bfb1f76'
                if account.authorization_information is not None:
                    for item in account.authorization_information.split(';'):
                        kv = item.strip().split('=')
                        cls.cookie_list[kv[0]] = kv[1]
                    account.type = cls.we_media_type
                    account.platform = cls.we_media_id
                    return [account, cls.cookie_list]
                else:
                    # todo::报错给推广部
                    pass
        else:
            # todo::报错给推广部
            pass

    def parse(self, response):
        [account, cookie_list] = self.get_account()
        user_url = 'https://mp.toutiao.com/user_login_status_api/'
        yield Request(url=user_url, callback=self.parse_user, dont_filter=True, cookies=cookie_list,
                      meta={'account': account})

    def parse_user(self, response: HtmlResponse):
        account = response.meta['account']
        response_str = response.body.decode('utf-8')
        user_detail = json.loads(response_str)['reason']['media']['media_info']
        account.account_id = user_detail['user_id']
        start = end = self.get_yesterday()
        url = r'https://mp.toutiao.com/mp/agw/statistic/content/content_overview?start_date={start}&end_date={end}' \
            .format(start=start, end=end)
        yield Request(url=url, callback=self.parse_data, dont_filter=True, cookies=self.cookie_list,
                      meta={'account': account})

    def parse_data(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        content_daily_detail = json.loads(json.loads(response_str)['data']['total_stat'])
        account = response.meta['account']
        # 曝光量
        exposure_num = account.exposure_num if account.exposure_num is not None else 0
        account.exposure_num = exposure_num + content_daily_detail['impression_count'] + content_daily_detail[
            'go_detail_count']
        # 阅读量
        read_num = account.read_num if account.read_num is not None else 0
        account.read_num = read_num + content_daily_detail['go_detail_count']
        # 推荐量
        recommend_num = account.recommend_num if account.recommend_num is not None else 0
        account.recommend_num = recommend_num + content_daily_detail['impression_count']
        # 转发
        forward_num = account.forward_num if account.forward_num is not None else 0
        account.forward_num = forward_num + content_daily_detail['share_count']
        # 发布量
        publish_num = account.publish_num if account.publish_num is not None else 0
        account.publish_num = publish_num + content_daily_detail['publish_num']
        yield Request(url='https://mp.toutiao.com/statistic/profile_stat/', callback=self.parse_fans_profile,
                      dont_filter=True, cookies=self.cookie_list, meta={'account': account})

    def parse_fans_profile(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        profile_detail = json.loads(response_str)['data']
        account = response.meta['account']
        account.follow_num = profile_detail['total_subscribe_count']
        account.total_income = profile_detail['total_income']
        account.drawing = profile_detail['total_withdraw']
        account.balance = profile_detail['actual_income']
        account.read_num = profile_detail['go_detail_count']
        yield Request(url='https://mp.toutiao.com/mp/agw/statistic/fans/property', callback=self.parse_property,
                      dont_filter=True, cookies=self.cookie_list, meta={'account': account})

    @staticmethod
    def parse_property(response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        account = response.meta['account']
        fans_property_data = json.loads(response_str)['fans_property_data']
        fans_age_total = 0
        for count in fans_property_data['fansage'].values():
            fans_age_total += count
        account.age_proportion = {
            '<24': round(fans_property_data['fansage']['18-23'] / fans_age_total, 4) * 100,
            '25-39': round((fans_property_data['fansage']['24-30'] + fans_property_data['fansage']['31-40']) /
                           fans_age_total, 4) * 100,
            '>40': round((fans_property_data['fansage']['41-50'] + fans_property_data['fansage']['50-']) /
                         fans_age_total, 4) * 100,
            'unknown': 0.00 * 100
        }
        fans_gender_total = fans_property_data['fansgender']['female'] + fans_property_data['fansgender']['male']
        account.sex_proportion = {
            'man': round(fans_property_data['fansgender']['male'] / fans_gender_total, 4) * 100,
            'women': round(fans_property_data['fansgender']['female'] / fans_gender_total, 4) * 100,
            'unknown': 0.00 * 100
        }
        account.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        yield account

    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = str(today - one_day).replace('-', '')
        return yesterday


class JinritoutiaoArticleSpider(scrapy.Spider):
    name = 'toutiao_article'
    start_urls = [
        'https://mp.toutiao.com/mp/agw/article/list?size=20&status=all&from_time=0&start_time=0&end_time=0'
        '&search_word=&page=1&feature=0&source=all']
    allowed_domains = ['www.toutiao.com/']
    base_url = 'https://www.toutiao.com/'
    cookie_list = {}
    page_size = 20
    page_url = r'https://mp.toutiao.com/mp/agw/article/list?size=20&status=all&from_time=0&start_time=0&end_time=0' \
               r'&search_word=&page={page}&feature=0&source=all'
    content_url = r'https://www.toutiao.com/i{article_id}/'
    account = marketing.Account()
    spot_list = []

    def parse(self, response: HtmlResponse):
        [self.account, self.cookie_list] = JinritoutiaoSpider.get_account()
        yield Request(url=self.start_urls[0], callback=self.parse_article, dont_filter=True, cookies=self.cookie_list,
                      meta={'page': 1})

    def parse_article(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        article_data = json.loads(response_str)['data']
        article_list = article_data['content']
        page = article_data['page'] + 1
        for article_detail in article_list:
            self.handle_article(article_detail)
        if page <= math.ceil(article_data['total'] / self.page_size):
            yield Request(url=self.page_url.format(page=page), callback=self.parse_article,
                          dont_filter=True, cookies=self.cookie_list, meta={'page': page})

    def handle_article(self, article_detail):
        article = Article.objects(platform_type=self.account.type, platform=self.account.platform,
                                  article_id=article_detail['id']).first()
        article = Article() if article is None else article
        article.exposure_num = article_detail['impression_count'] + article_detail['go_detail_count']
        article.recommend_num = article_detail['impression_count']
        article.read_num = article_detail['go_detail_count']
        article.forward_num = article_detail['share_count']
        article.like_num = 0
        article.comment_num = article_detail['comment_count']
        if article is None:
            article.platform_type = self.account.type
            article.platform = self.account.platform
            article.article_id = article_detail['id']
            article.title = article_detail['title']
            article.account_id = self.account.account_id
            article.create_at = datetime.datetime.now().strftime('%Y-%m-%d')
            article.admin_id = self.account.admin_id
            article.admin_name = self.account.admin_name
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.88 Safari/537.36',
                'referer': self.content_url.format(article_id=article.article_id)
            }
            yield Request(url=self.content_url.format(article_id=article.article_id), callback=self.parse_content,
                          dont_filter=True, cookies=self.cookie_list, headers=headers, meta={'article': article})
        else:
            article.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
            yield article

    def parse_content(self, response: HtmlResponse):
        article = response.meta['article']
        response_str = response.body.decode('utf-8')
        content = re.search(r'content: \'&quot;(.*)&quot;\'', response_str)
        if content is None:
            content = re.search(r'gallery: JSON.parse\(\"(.*)\"\)', response_str)
            content = content.group(1).encode('latin-1').decode('unicode-escape')
        article.keyword_list = []
        article.spot_id_list = []
        for spot_keywords in self.get_spot_list():
            if spot_keywords['abbreviation'] in str(content):
                article.keyword_list.append(spot_keywords['abbreviation'])
                article.spot_id_list.append(spot_keywords['spot_id'])
        article.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        yield article

    def get_spot_list(self):
        if not len(self.spot_list):
            spo_list = spot.CSpot.objects(self_employed=True).fields(spot_id=1, abbreviation=1)
            for spot_detail in spo_list:
                self.spot_list.append({'spot_id': spot_detail.spot_id, 'abbreviation': spot_detail.abbreviation})
        return self.spot_list



