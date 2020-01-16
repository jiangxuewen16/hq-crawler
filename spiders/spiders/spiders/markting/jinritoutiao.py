import datetime
import json
import math
import re

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import helper
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

    def parse(self, response):
        result = helper.get_media_account(self)
        for detail in result:
            [account, cookie_list] = detail
            user_url = 'https://mp.toutiao.com/user_login_status_api/'
            yield Request(url=user_url, callback=self.parse_user, dont_filter=True, cookies=cookie_list,
                          meta={'account': account})

    def parse_user(self, response: HtmlResponse):
        account = response.meta['account']
        response_str = response.body.decode('utf-8')
        user_detail = json.loads(response_str)['reason']['media']['media_info']
        account.account_id = user_detail['user_id']
        start = end = helper.get_yesterday()
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
        # 评论量
        comment_count = account.comment_num if account.comment_num is not None else 0
        account.comment_num = comment_count + content_daily_detail['comment_count']
        marketing_daily_report = self.handle_marketing_daily_report(account, content_daily_detail)
        yield Request(url='https://mp.toutiao.com/statistic/profile_stat/', callback=self.parse_fans_profile,
                      dont_filter=True, cookies=self.cookie_list,
                      meta={'account': account, 'marketing_daily_report': marketing_daily_report})

    def handle_marketing_daily_report(self, account: marketing.Account, content_daily_detail):
        """
        处理文章日报表文章数据
        :param account: marketing.Account 账号信息
        :param content_daily_detail: dict 文章基础数据
        :return:
        """
        marketing_daily_report = marketing.MarketingDailyReport()
        marketing_daily_report.type = self.we_media_type
        marketing_daily_report.platform = self.we_media_id
        marketing_daily_report.account_id = account.id
        marketing_daily_report.account_name = account.account_name
        marketing_daily_report.admin_id = account.admin_id
        # 曝光量
        marketing_daily_report.exposure_num = content_daily_detail['impression_count'] + content_daily_detail[
            'go_detail_count']
        # 阅读量
        marketing_daily_report.read_num = account.read_num
        marketing_daily_report.day_read_num = content_daily_detail['go_detail_count']
        # 推荐量
        marketing_daily_report.recommend_num = content_daily_detail['impression_count']
        # 转发
        marketing_daily_report.forward_num = content_daily_detail['share_count']
        # 发布量
        marketing_daily_report.publish_num = account.publish_num
        marketing_daily_report.day_publish_num = content_daily_detail['publish_num']
        # 评论量
        account.comment_count = content_daily_detail['comment_count']
        marketing_daily_report.day_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return marketing_daily_report

    def parse_fans_profile(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        profile_detail = json.loads(response_str)['data']
        account = response.meta['account']
        marketing_daily_report = response.meta['marketing_daily_report']
        # 总粉丝数
        marketing_daily_report.follow_num = account.follow_num = profile_detail['total_subscribe_count']
        # 总收入
        account.total_income = profile_detail['total_income']
        # 总提现
        account.drawing = profile_detail['total_withdraw']
        # 总余额（实时）
        account.balance = profile_detail['actual_income']
        yield Request(url='https://mp.toutiao.com/mp/agw/statistic/fans/property', callback=self.parse_property,
                      dont_filter=True, cookies=self.cookie_list,
                      meta={'account': account, 'marketing_daily_report': marketing_daily_report})

    def parse_property(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        account = response.meta['account']
        marketing_daily_report = response.meta['marketing_daily_report']
        fans_property_data = json.loads(response_str)['fans_property_data']
        fans_age_total = 0
        for count in fans_property_data['fansage'].values():
            fans_age_total += count
        marketing_daily_report.age_proportion = account.age_proportion = {
            '<24': round(fans_property_data['fansage']['18-23'] / fans_age_total, 4) * 100,
            '25-39': round((fans_property_data['fansage']['24-30'] + fans_property_data['fansage']['31-40']) /
                           fans_age_total, 4) * 100,
            '>40': round((fans_property_data['fansage']['41-50'] + fans_property_data['fansage']['50-']) /
                         fans_age_total, 4) * 100,
            'unknown': 0.00 * 100
        }
        fans_gender_total = fans_property_data['fansgender']['female'] + fans_property_data['fansgender']['male']
        marketing_daily_report.sex_proportion = account.sex_proportion = {
            'man': round(fans_property_data['fansgender']['male'] / fans_gender_total, 4) * 100,
            'women': round(fans_property_data['fansgender']['female'] / fans_gender_total, 4) * 100,
            'unknown': 0.00 * 100
        }
        account.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        yield account
        fans_url = r'https://mp.toutiao.com/mp/agw/statistic/fans/count_trend/?start_date={start}&end_date={end}'
        start = end = helper.get_yesterday()
        yield Request(url=fans_url.format(start=start, end=end), callback=self.daily_fans,
                      dont_filter=True, cookies=self.cookie_list,
                      meta={'marketing_daily_report': response.meta['marketing_daily_report']})

    def daily_fans(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        marketing_daily_report = response.meta['marketing_daily_report']
        fans_count_trend = json.loads(response_str)['fans_count_trend']['data_list'][0]
        # 取消关注数
        marketing_daily_report.day_unfollow_num = fans_count_trend['new_dislike_count']
        # 净增关注
        marketing_daily_report.day_add_follow_num = fans_count_trend['new_growth_count']
        # 当日关注
        marketing_daily_report.day_follow_num = fans_count_trend['new_like_count']
        yield Request(url='https://mp.toutiao.com/pgc/mp/income/withdraw_info?page_no=1&page_size=10',
                      callback=self.daily_income, dont_filter=True, cookies=self.cookie_list,
                      meta={'marketing_daily_report': response.meta['marketing_daily_report']})

    @staticmethod
    def daily_income(response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        income_statement = json.loads(response_str)['data']['overview']
        marketing_daily_report = response.meta['marketing_daily_report']
        marketing_daily_report.income = income_statement[0]['amount']
        marketing_daily_report.drawing = income_statement[2]['amount']
        marketing_daily_report.balance = income_statement[1]['can_withdraw']
        marketing_daily_report.create_at = datetime.datetime.now().strftime('%Y-%m-%d')
        marketing_daily_report.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        yield marketing_daily_report


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
    we_media_id = WeMedia.TOU_TIAO.value.id
    we_media_type = WeMediaType.WE_MEDIA.value.id

    def parse(self, response: HtmlResponse):
        [self.account, self.cookie_list] = helper.get_media_account(self)
        yield Request(url=self.start_urls[0], callback=self.parse_article, dont_filter=True, cookies=self.cookie_list,
                      meta={'page': 1})

    def parse_article(self, response: HtmlResponse):
        response_str = response.body.decode('utf-8')
        article_data = json.loads(response_str)['data']
        article_list = article_data['content']
        page = article_data['page'] + 1
        for article_detail in article_list:
            yield self.handle_article(article_detail)
        if page <= math.ceil(article_data['total'] / self.page_size):
            yield Request(url=self.page_url.format(page=page), callback=self.parse_article,
                          dont_filter=True, cookies=self.cookie_list, meta={'page': page})

    def handle_article(self, article_detail):
        actual_article = article = Article.objects(platform_type=self.account.type, platform=self.account.platform
                                                   , article_id=article_detail['id']).first()
        article = Article() if article is None else article
        article.exposure_num = article_detail['impression_count'] + article_detail['go_detail_count']
        article.recommend_num = article_detail['impression_count']
        article.read_num = article_detail['go_detail_count']
        article.forward_num = article_detail['share_count']
        article.like_num = 0
        article.comment_num = article_detail['comment_count']
        if actual_article is None:
            article.platform_type = self.account.type
            article.platform = self.account.platform
            article.article_id = article_detail['id']
            article.title = article_detail['title']
            article.account_id = self.account.id
            article.create_at = datetime.datetime.now().strftime('%Y-%m-%d')
            article.admin_id = self.account.admin_id
            # article.admin_name = self.account.admin_name
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.88 Safari/537.36',
                'referer': self.content_url.format(article_id=article.article_id)
            }
            return Request(url=self.content_url.format(article_id=article.article_id), callback=self.parse_content
                           , dont_filter=True, cookies=self.cookie_list, headers=headers, meta={'article': article})
        else:
            article.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
            return article

    def parse_content(self, response: HtmlResponse):
        article = response.meta['article']
        response_str = response.body.decode('utf-8')
        content = re.search(r'content: \'&quot;(.*)&quot;\'', response_str)
        if content is None:
            content = re.search(r'gallery: JSON.parse\(\"(.*)\"\)', response_str)
            content = content.group(1).encode('latin-1').decode('unicode-escape')
        article.content = content
        article.keyword_list = article.spot_id_list = []
        for spot_keywords in self.get_spot_list():
            if spot_keywords['abbreviation'] in str(content):
                article.keyword_list.append(spot_keywords['abbreviation'])
                article.spot_id_list.append(spot_keywords['spot_id'])
        article.update_at = datetime.datetime.now().strftime('%Y-%m-%d')
        return article

    def get_spot_list(self):
        if not len(self.spot_list):
            spo_list = spot.CSpot.objects(self_employed=True).fields(spot_id=1, abbreviation=1)
            for spot_detail in spo_list:
                self.spot_list.append({'spot_id': spot_detail.spot_id, 'abbreviation': spot_detail.abbreviation})
        return self.spot_list



