import datetime
import json
import math
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import helper
from spiders.common.marketing import WeMedia, WeMediaType
from spiders.items import marketing
from spiders.items.spot import spot


class WangyihaoSpider(scrapy.Spider):
    name = 'wangyihao'
    allowed_domains = ['mp.163.com']
    base_url = 'http://mp.163.com/wemedia/navinfo.do?_={millisecond}}'
    start_urls = ['http://mp.163.com/wemedia/navinfo.do?_=1577264663618']
    # start_urls = ['http://mp.163.com/wemedia/index/count.do?_=1577264663618']

    # 昨日推荐数/分享
    base_recommended_yesterday_url = 'http://mp.163.com/wemedia/data/content/article/pv/list.do?_={millisecond}&start={start}&end={end}'
    #
    base_data_url = 'http://mp.163.com/wemedia/index/count.do?_={millisecond}'

    # 图文数据 文章
    base_article_url = 'http://mp.163.com/wemedia/data/content/article/list.do?_=1577323554587&wemediaId=W6993657201255468499&start=2019-12-25&end=2019-12-25&pageNo=1&orderBy=pvCount&order=desc&pageSize=7'
    # base_article_url = 'http://mp.163.com/wemedia/data/content/article/list.do?_={id}&start={start}&end={end}&pageNo=1&orderBy=pvCount&order=desc&pageSize=7'

    # 总收益
    base_profit_url = 'http://mp.163.com/wemedia/profit/view.do?_={millisecond}'

    # 图文收益 文章
    base_graphic_revenue_url = 'http://mp.163.com/wemedia/profit/list.do?_={millisecond}&start={start}&end={end}'

    def start_requests(self):
        account = marketing.Account.objects(platform=WeMedia.WANG_YI.value.id)
        for item in account:
            if not item.is_enable:
                return
            cookies = {}
            # cookis_str = 'NTESwebSI=1397970B73BFF1A37E0BC5901B0116D1.hzabj-subscribe-tomcat3.server.163.org-8082; _antanalysis_s_id=1577264622463; _ntes_nnid=8834a86dfd2ba2e09b6137db49f73f45,1577264622967; _ntes_nuid=8834a86dfd2ba2e09b6137db49f73f45; NTES_SESS=OdCxos2hnfEnFxHcGy..xc9TuE.M8Ok_qulHkVABek4UeypJekSXAh0m.RrfDBuxQMw5hJdx93.HvewRB6P7Rcwi1p5D7j8CuZDBIOFBc6pJbnTHNZjiUhgynZz8shX8m_lsvjoHwGbMPCmeJ6T88kz1iM38U1EQk7gn4gEtJAbA6SENWW7ByJGsR6CYB2PRVQdBS5GV8uC7KLNI0OKqwuVyY7Fo2Dude; NTES_PASSPORT=FxdhOS5KibI0Zj2v5LeDBwDIGTwpYBLhmy48Dbj97SaNDJLIDjktuVK6wo0qCZMOFrFoa6BmZHojr3fBhjUoxBu68Dc90G1xZEWobcE5E.hZpXhX7rzbHgU_LE48SqkHutJ75KxcGV.uXZYi1gaJPRDDZhmvDJE_EeOE00.V5OGlIi3uy6RJ1ioUoKIQMKr9NP9gRlEprxLHV; S_INFO=1577264654|0|3&80##|m15207489053_1; P_INFO=m15207489053_1@163.com|1577264654|1|subscribe|00&99|hun&1576897003&subscribe#hun&430100#10#0#0|152053&0|163&subscribe|15207489053@163.com'
            cookis_str = item.authorization_information
            cookis_str_list = cookis_str.split(';')
            for item in cookis_str_list:
                kv = item.strip().split('=')
                cookies[kv[0]] = kv[1]

        # url = self.base_url.format(id=ota_spot_id, wemediaId=)
        yield Request(self.start_urls[0]
                      , method="GET"
                      , cookies=cookies
                      , callback=self.parse
                      , meta={'cookies': cookies})

    def parse(self, response: HtmlResponse):
        cookies = response.meta['cookies']
        data = json.loads(response.body.decode('utf-8'))

        millisecond = self.get_millisecond()
        star = end = self.get_yesterday()
        url = self.base_recommended_yesterday_url.format(millisecond=millisecond, start=star, end=end)
        yield Request(url=url, method="GET", cookies=cookies, callback=self.recommended_yesterday, dont_filter=True,
                      meta={'articleCount': data['data']['articleCount'], 'loginUser': data['data']['loginUser']})

    def recommended_yesterday(self, response: HtmlResponse):
        article_count = response.meta['articleCount']
        loginUser = response.meta['loginUser']
        data = json.loads(response.body.decode('utf-8'))
        millisecond = self.get_millisecond()
        url = self.base_profit_url.format(millisecond=millisecond)
        yield Request(url=url, callback=self.profit_data, dont_filter=True,
                      meta={'articleCount': article_count, 'loginUser': loginUser,
                            'recommendCount': (data['data']['list'][0]['recommendCount']
                                               if data['data']['list'] is not None else 0),
                            'readCount': (data['data']['list'][0]['readCount'] if data['data']['list'] is not None else
                                          0),
                            'commentCount': (data['data']['list'][0]['commentCount'] if data['data']['list'] is not None
                                             else 0),
                            'shareCount': (data['data']['list'][0]['shareCount'] if data['data']['list'] is not None
                                           else 0)})

    def profit_data(self, response: HtmlResponse):
        article_count = response.meta['articleCount']
        loginUser = response.meta['loginUser']
        # 昨日推荐数
        recommend_count = response.meta['recommendCount']
        # 昨日阅读数
        read_count = response.meta['readCount']
        # 评论数
        comment_count = response.meta['commentCount']
        # 分享数
        share_count = response.meta['shareCount']

        data = json.loads(response.body.decode('utf-8'))

        # 总收益
        sum_profit = data['data']['sumProfit']
        # 昨日新增收益
        profit = data['data']['profit']

        millisecond = self.get_millisecond()
        url = self.base_data_url.format(millisecond=millisecond)
        yield Request(url=url, callback=self.account_data, dont_filter=True,
                      meta={'articleCount': article_count, 'loginUser': loginUser, 'recommendCount': recommend_count,
                            'readCount': read_count,
                            'commentCount': comment_count,
                            'shareCount': share_count,
                            'sumProfit': sum_profit,
                            'profit': profit})

    def account_data(self, response: HtmlResponse):
        article_count = response.meta['articleCount']
        loginUser = response.meta['loginUser']
        # 昨日推荐数
        recommend_count = response.meta['recommendCount']
        # 昨日阅读数
        read_count = response.meta['readCount']
        # 评论数
        comment_count = response.meta['commentCount']
        # 分享数
        share_count = response.meta['shareCount']
        # 总收益
        sum_profit = response.meta['sumProfit']
        # 昨日新增收益
        profit = response.meta['profit']
        data = json.loads(response.body.decode('utf-8'))

        account = marketing.Account.objects(platform=WeMedia.WANG_YI.value.id,
                                            account_id=data['data']['wemediaId']).first()
        # if not account:
        #     account = marketing.Account()
        #
        # account.type = WeMediaType.WE_MEDIA.value.id
        # account.platform = WeMedia.WANG_YI.value.id
        # account.login_name = loginUser
        # account.account_name = '旅小达'
        # account.account_id = data['data']['wemediaId']
        # account.authorization_information = ''
        # admin = marketing.Admin.objects(name='刘俊', is_enable=True).first()
        # account.admin_id = admin.id

        account.exposure_num = (account.exposure_num if account.exposure_num is not None else 0) + (recommend_count +
                                                                                                    read_count)
        account.recommend_num = (account.recommend_num if account.recommend_num is not None else 0) + recommend_count
        account.read_num = data['data']['totalReadCount']
        account.follow_num = data['data']['totalSubscribeCount']
        account.forward_num = (account.forward_num if account.forward_num is not None else 0) + share_count
        account.sex_proportion = {'man': 0, 'women': 0, 'unknown': 100.00}
        account.age_proportion = {'<24': 0, '25-39': 0, '>40': 0, 'unknown': 100.00}
        account.like_num = 0
        account.comment_num = (account.comment_num if account.comment_num is not None else 0) + comment_count
        account.total_income = sum_profit
        if (account.total_income if account.total_income is None else 0) + profit - sum_profit > 0:
            drawing = (account.total_income if account.total_income is None else 0) + profit - sum_profit
        else:
            drawing = 0
        account.drawing = 0
        account.balance = sum_profit
        account.publish_num = article_count
        account.is_enable = True
        account.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield account

    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = today - one_day
        return yesterday

    @staticmethod
    def get_millisecond():
        t = time.time()
        millisecond = int(round(t * 1000))
        return millisecond


class WangyihaoAriticleSpider(scrapy.Spider):
    name = 'wangyihao_article'
    allowed_domains = ['mp.163.com']

    page_size = 20  # 默认爬取每页20条
    base_url = 'http://mp.163.com/wemedia/content/manage/list.do?_={millisecond}&pageNo={page}&contentState=3&size={page_size}&contentType=4'
    start_urls = ['http://mp.163.com/wemedia/content/manage/list.do?_=1577416174160&pageNo=1&contentState=3&size=20&contentType=4']
    base_article_detail_url = 'http://dy.163.com/v2/article/detail/{articleId}.html'

    base_article_detail_news_url = 'https://c.m.163.com/news/p/0503/{skipId}.html?spss=newsapp&spsw=1'

    def start_requests(self):
        account = marketing.Account.objects(type=WeMediaType.WE_MEDIA.value.id, platform=WeMedia.WANG_YI.value.id)
        for item in account:
            cookies = {}
            # cookis_str = 'NTESwebSI=1397970B73BFF1A37E0BC5901B0116D1.hzabj-subscribe-tomcat3.server.163.org-8082; _antanalysis_s_id=1577264622463; _ntes_nnid=8834a86dfd2ba2e09b6137db49f73f45,1577264622967; _ntes_nuid=8834a86dfd2ba2e09b6137db49f73f45; NTES_SESS=OdCxos2hnfEnFxHcGy..xc9TuE.M8Ok_qulHkVABek4UeypJekSXAh0m.RrfDBuxQMw5hJdx93.HvewRB6P7Rcwi1p5D7j8CuZDBIOFBc6pJbnTHNZjiUhgynZz8shX8m_lsvjoHwGbMPCmeJ6T88kz1iM38U1EQk7gn4gEtJAbA6SENWW7ByJGsR6CYB2PRVQdBS5GV8uC7KLNI0OKqwuVyY7Fo2Dude; NTES_PASSPORT=FxdhOS5KibI0Zj2v5LeDBwDIGTwpYBLhmy48Dbj97SaNDJLIDjktuVK6wo0qCZMOFrFoa6BmZHojr3fBhjUoxBu68Dc90G1xZEWobcE5E.hZpXhX7rzbHgU_LE48SqkHutJ75KxcGV.uXZYi1gaJPRDDZhmvDJE_EeOE00.V5OGlIi3uy6RJ1ioUoKIQMKr9NP9gRlEprxLHV; S_INFO=1577264654|0|3&80##|m15207489053_1; P_INFO=m15207489053_1@163.com|1577264654|1|subscribe|00&99|hun&1576897003&subscribe#hun&430100#10#0#0|152053&0|163&subscribe|15207489053@163.com'
            cookis_str = item.authorization_information
            cookis_str_list = cookis_str.split(';')
            for items in cookis_str_list:
                kv = items.strip().split('=')
                cookies[kv[0]] = kv[1]
            millisecond = self.get_millisecond()
            url = self.base_url.format(millisecond=millisecond, page=1, page_size=20)
            yield Request(url=url
                          , method="POST"
                          , cookies=cookies
                          , callback=self.parse
                          , meta={'account_id': item.id, 'cookies': cookies, 'account_name': item.account_name})

    def parse(self, response: HtmlResponse):
        account_id = response.meta['account_id']
        cookies = response.meta['cookies']
        account_name = response.meta['account_name']
        data = json.loads(response.body.decode('utf-8'))
        new_total = data['data']['total']

        # article_num = marketing.Article.objects(platform=WeMedia.WANG_YI.value.id, account_id=account_id).count()
        # new_num = new_total - article_num
        # if new_num <= 0:  # 没有新文章的情况下不需要做任何处理
        #     return

        page_size = self.page_size
        # 总页数
        total_page = math.ceil(new_total / page_size)
        # if new_num < self.page_size:  # 新增的文章数量小于默认爬取的最大数量，则用新增的数量作为爬取数量
        #     page_size = new_num

        millisecond = self.get_millisecond()
        page = 1
        url = self.base_url.format(millisecond=millisecond, page=page, page_size=page_size)
        yield Request(url=url,
                      method="POST",
                      cookies=cookies,
                      callback=self.parse_page,
                      dont_filter=True,
                      meta={'millisecond': millisecond, 'page': page,
                            'page_size': page_size,
                            'total_page': total_page,
                            'cookies': cookies,
                            'account_name': account_name,
                            'account_id': account_id})

    def parse_page(self, response: HtmlResponse):
        millisecond = response.meta['millisecond']
        page = response.meta['page']
        page_size = response.meta['page_size']
        total_page = response.meta['total_page']
        cookies = response.meta['cookies']
        account_name = response.meta['account_name']
        account_id = response.meta['account_id']
        data = json.loads(response.body.decode('utf-8'))

        for item in data['data']['list']:
            article = self.article_data(item, account_id, account_name)
            if not article.content:
                if item['contentType'] == 1:
                    url = self.base_article_detail_url.format(articleId=item['articleId'])
                    yield Request(url=url, callback=self.article_detail, dont_filter=True,
                                  meta={'article': article,
                                        'article_id': item['articleId'],
                                        'account_name': account_name,
                                        'account_id': account_id})
                elif item['contentType'] == 3:
                    url = self.base_article_detail_news_url.format(skipId=item['skipId'])
                    yield Request(url=url, callback=self.article_detail_news, dont_filter=True,
                                  meta={'article': article,
                                        'article_id': item['skipId'],
                                        'account_name': account_name,
                                        'account_id': account_id})
            else:
                yield article

        start_offset = response.meta['page'] + 1
        if start_offset <= total_page:
            url = self.base_url.format(millisecond=millisecond, page=start_offset, page_size=page_size)
            yield Request(url=url,
                          method="POST",
                          dont_filter=True,
                          cookies=cookies,
                          callback=self.parse_page,
                          meta={'millisecond': millisecond, 'page': start_offset,
                                'page_size': page_size,
                                'total_page': total_page,
                                'cookies': cookies,
                                'account_name': account_name,
                                'account_id': account_id})

    @staticmethod
    def article_data(item, account_id, account_name):
        article = marketing.Article.objects(platform=WeMedia.WANG_YI.value.id,
                                            article_id=item['articleId']).first()
        article_id = item['articleId']

        if item['contentType'] == 3:
            article = marketing.Article.objects(platform=WeMedia.WANG_YI.value.id,
                                                article_id=item['skipId']).first()
            article_id = item['skipId']

        if not article:
            article = marketing.Article()
            article.platform_type = WeMediaType.WE_MEDIA.value.id
            article.platform = WeMedia.WANG_YI.value.id
            article.article_id = article_id
            article.title = item['title']

        article.create_at = item['showTime']
        article.exposure_num = item['recommendCount'] + item['pvCount']
        article.recommend_num = item['recommendCount']
        article.read_num = item['pvCount']
        article.forward_num = item['shareCount']
        article.like_num = 0
        article.comment_num = item['commentCount']
        article.account_id = account_id
        article.account_name = account_name
        article.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return article

    def article_detail(self, response: HtmlResponse):
        content = response.xpath('//*[@id="content"]').extract_first()
        article = response.meta['article']
        article.content = content

        self.article_spot(article)
        yield article

    def article_detail_news(self, response: HtmlResponse):
        content = response.xpath('/html/body/div/section[1]/article[1]/div[1]/div[3]').extract_first()
        article = response.meta['article']
        article.content = content

        self.article_spot(article)
        yield article

    @staticmethod
    def article_spot(article):
        account = marketing.Account.objects(platform=WeMedia.WANG_YI.value.id, id=article.account_id).first()
        admin = marketing.Admin.objects(id=account.admin_id).first()

        spot_list = spot.CSpot.objects(self_employed=True).fields(spot_id=1, abbreviation=1)

        spot_name = []
        for item in spot_list:
            spot_name.append(item.abbreviation)

        spot_id_list = []
        keyword_list = helper.String.str_count_list(article.content, spot_name, True).keys()

        for spot_item in spot_list:
            for name in keyword_list:
                if name == spot_item.abbreviation:
                    spot_id_list.append(spot_item.spot_id)

        article.keyword_list = keyword_list
        article.spot_id_list = spot_id_list
        article.admin_id = admin.id
        article.admin_name = admin.name


    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = today - one_day
        return yesterday

    @staticmethod
    def get_millisecond():
        t = time.time()
        millisecond = int(round(t * 1000))
        return millisecond





class WangyihaoDailyReportSpider(scrapy.Spider):
    name = 'wangyihao_daily'
    allowed_domains = ['mp.163.com']

    base_url = 'http://mp.163.com/wemedia/index/count.do?_={millisecond}'
    start_urls = [
        'http://mp.163.com/wemedia/data/content/article/count.do?_=1577669059883']
    # 总发布条数
    base_count_url = 'http://mp.163.com/wemedia/content/manage/list.do?_={millisecond}&pageNo=1&contentState=3&size=20&contentType=4'
    # 当天阅读量
    base_article_read_url = 'http://mp.163.com/wemedia/data/content/article/pv/list.do?_={millisecond}&start={start}&end={end}'
    # 当天发布量
    base_article_count_url = 'http://mp.163.com/wemedia/data/content/article/list.do?_={millisecond}&start={start}&end={end}&pageNo=1&orderBy=pvCount&order=desc&pageSize=7'
    # 粉丝数
    base_follow_url = 'http://mp.163.com/wemedia/subs.json?_={millisecond}&start={start}&end={end}'
    # 收益
    base_income_url = 'http://mp.163.com/wemedia/profit/list.do?_={millisecond}&start={start}&end={end}'
    # 总收益
    base_profit_url = 'http://mp.163.com/wemedia/profit/view.do?_={millisecond}'

    def start_requests(self):
        account = marketing.Account.objects(type=WeMediaType.WE_MEDIA.value.id, platform=WeMedia.WANG_YI.value.id)
        for item in account:
            cookies = {}
            # cookis_str = 'NTESwebSI=1397970B73BFF1A37E0BC5901B0116D1.hzabj-subscribe-tomcat3.server.163.org-8082; _antanalysis_s_id=1577264622463; _ntes_nnid=8834a86dfd2ba2e09b6137db49f73f45,1577264622967; _ntes_nuid=8834a86dfd2ba2e09b6137db49f73f45; NTES_SESS=OdCxos2hnfEnFxHcGy..xc9TuE.M8Ok_qulHkVABek4UeypJekSXAh0m.RrfDBuxQMw5hJdx93.HvewRB6P7Rcwi1p5D7j8CuZDBIOFBc6pJbnTHNZjiUhgynZz8shX8m_lsvjoHwGbMPCmeJ6T88kz1iM38U1EQk7gn4gEtJAbA6SENWW7ByJGsR6CYB2PRVQdBS5GV8uC7KLNI0OKqwuVyY7Fo2Dude; NTES_PASSPORT=FxdhOS5KibI0Zj2v5LeDBwDIGTwpYBLhmy48Dbj97SaNDJLIDjktuVK6wo0qCZMOFrFoa6BmZHojr3fBhjUoxBu68Dc90G1xZEWobcE5E.hZpXhX7rzbHgU_LE48SqkHutJ75KxcGV.uXZYi1gaJPRDDZhmvDJE_EeOE00.V5OGlIi3uy6RJ1ioUoKIQMKr9NP9gRlEprxLHV; S_INFO=1577264654|0|3&80##|m15207489053_1; P_INFO=m15207489053_1@163.com|1577264654|1|subscribe|00&99|hun&1576897003&subscribe#hun&430100#10#0#0|152053&0|163&subscribe|15207489053@163.com'
            cookis_str = item.authorization_information
            cookis_str_list = cookis_str.split(';')
            for items in cookis_str_list:
                kv = items.strip().split('=')
                cookies[kv[0]] = kv[1]
            millisecond = self.get_millisecond()
            url = self.base_url.format(millisecond=millisecond)
            yield Request(url=url
                          , method="GET"
                          , cookies=cookies
                          , callback=self.parse
                          , meta={'account_id': item.id, 'cookies': cookies, 'account_name': item.account_name,
                                  'admin_id': item.admin_id})

    def parse(self, response: HtmlResponse):
        admin_id = response.meta['admin_id']
        admin_info = marketing.Admin.objects(id=admin_id, is_enable=True).first()
        data = json.loads(response.body.decode('utf-8'))

        # 总阅读数
        read_num = data['data']['totalReadCount']
        follow_num = data['data']['totalSubscribeCount']
        millisecond = self.get_millisecond()
        start = end = self.get_yesterday()
        url = self.base_count_url.format(millisecond=millisecond, start=start, end=end)
        yield Request(url=url
                      , method="POST"
                      , cookies=response.meta['cookies']
                      , callback=self.article_total_count
                      , meta={'account_id': response.meta['account_id'], 'cookies': response.meta['cookies'],
                              'account_name': response.meta['account_name'],
                              'admin_id': response.meta['admin_id'],
                              'admin_name': admin_info.name,
                              'read_num': read_num,
                              'follow_num': follow_num})

    def article_total_count(self, response: HtmlResponse):
        data = json.loads(response.body.decode('utf-8'))
        # 总发布量
        publish_num = data['data']['total']
        millisecond = self.get_millisecond()
        start = end = self.get_yesterday()
        url = self.base_article_count_url.format(millisecond=millisecond, start=start, end=end)
        yield Request(url=url
                      , method="GET"
                      , cookies=response.meta['cookies']
                      , callback=self.article_count
                      , meta={'account_id': response.meta['account_id'], 'cookies': response.meta['cookies'],
                              'account_name': response.meta['account_name'],
                              'admin_id': response.meta['admin_id'],
                              'admin_name': response.meta['admin_name'],
                              'read_num': response.meta['read_num'],
                              'follow_num': response.meta['follow_num'],
                              'publish_num': publish_num})

    def article_count(self, response: HtmlResponse):
        data = json.loads(response.body.decode('utf-8'))
        # 当日发布量
        day_publish_num = data['data']['total']

        millisecond = self.get_millisecond()
        start = end = self.get_yesterday()

        url = self.base_article_read_url.format(millisecond=millisecond, start=start, end=end)
        yield Request(url=url
                      , method="GET"
                      , cookies=response.meta['cookies']
                      , callback=self.article_read
                      , meta={'account_id': response.meta['account_id'], 'cookies': response.meta['cookies'],
                              'account_name': response.meta['account_name'],
                              'admin_id': response.meta['admin_id'],
                              'admin_name': response.meta['admin_name'],
                              'read_num': response.meta['read_num'],
                              'publish_num': response.meta['publish_num'],
                              'follow_num': response.meta['follow_num'],
                              'day_publish_num': day_publish_num})

    def article_read(self, response: HtmlResponse):

        data = json.loads(response.body.decode('utf-8'))

        # 当日阅读量
        day_read_num = data['data']['list'][0]['readCount'] if data['data']['list'] is not None else 0
        # 推荐量
        recommend_num = data['data']['list'][0]['recommendCount'] if data['data']['list'] is not None else 0
        # 评论量
        comment_num = data['data']['list'][0]['commentCount'] if data['data']['list'] is not None else 0
        # 转发
        forward_num = data['data']['list'][0]['shareCount'] if data['data']['list'] is not None else 0
        # 总阅读数
        read_num = response.meta['read_num']
        publish_num = response.meta['publish_num']
        day_publish_num = response.meta['day_publish_num']
        follow_num = response.meta['follow_num']
        millisecond = self.get_millisecond()
        start = end = self.get_yesterday()
        url = self.base_follow_url.format(millisecond=millisecond, start=start, end=end)
        yield Request(url=url, method="GET", cookies=response.meta['cookies']
                      , callback=self.article_follow
                      , meta={'account_id': response.meta['account_id'], 'cookies': response.meta['cookies'],
                              'account_name': response.meta['account_name'],
                              'admin_id': response.meta['admin_id'],
                              'admin_name': response.meta['admin_name'],
                              'read_num': read_num,
                              'publish_num': publish_num,
                              'day_publish_num': day_publish_num,
                              'day_read_num': day_read_num,
                              'recommend_num': recommend_num,
                              'comment_num': comment_num,
                              'forward_num': forward_num,
                              'follow_num': follow_num})

    # 粉丝
    def article_follow(self, response: HtmlResponse):
        data = json.loads(response.body.decode('utf-8'))
        follow = data['data']['list']
        marketing_daily_report = self.daily_report_data(response.meta, follow)

        millisecond = self.get_millisecond()
        url = self.base_profit_url.format(millisecond=millisecond)
        yield Request(url=url, method="GET", cookies=response.meta['cookies']
                      , callback=self.total_revenue
                      , meta={'marketing_daily_report': marketing_daily_report, 'cookies': response.meta['cookies']})

    def total_revenue(self, response: HtmlResponse):
        marketing_daily_report = response.meta['marketing_daily_report']
        data = json.loads(response.body.decode('utf-8'))
        sum_profit = data['data']['sumProfit']
        millisecond = self.get_millisecond()
        start = end = self.get_yesterday()
        url = self.base_income_url.format(millisecond=millisecond, start=start, end=end)
        yield Request(url=url, method="GET", cookies=response.meta['cookies']
                      , callback=self.article_income
                      , meta={'marketing_daily_report': marketing_daily_report, 'cookies': response.meta['cookies'],
                              'sum_profit': sum_profit})

    def article_income(self, response: HtmlResponse):
        marketing_daily_report = response.meta['marketing_daily_report']
        sum_profit = response.meta['sum_profit']
        data = json.loads(response.body.decode('utf-8'))
        dt = self.get_yesterday(2)
        ts = int(time.mktime(time.strptime(str(dt), '%Y-%m-%d'))) * 1000

        before = marketing.MarketingDailyReport.objects(type=WeMediaType.WE_MEDIA.value.id,
                                                        platform=WeMedia.WANG_YI.value.id,
                                                        account_id=marketing_daily_report.account_id,
                                                        day_time=ts).first()
        marketing_daily_report.drawing = 0
        marketing_daily_report.income = data['data']['list'][0]['income']
        marketing_daily_report.balance = sum_profit
        yield marketing_daily_report

    @staticmethod
    def daily_report_data(data, follow):

        ts = int(time.mktime(time.strptime(str(follow[0]['statsDate']), '%Y-%m-%d')))

        marketing_daily_report = marketing.MarketingDailyReport.objects(type=WeMediaType.WE_MEDIA.value.id,
                                                                        platform=WeMedia.WANG_YI.value.id,
                                                                        day_time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                               time.localtime(ts)),
                                                                        account_id=data['account_id']).first()

        if not marketing_daily_report:
            marketing_daily_report = marketing.MarketingDailyReport()
            marketing_daily_report.platform = WeMedia.WANG_YI.value.id
            marketing_daily_report.account_id = data['account_id']
            marketing_daily_report.account_name = data['account_name']
            marketing_daily_report.admin_id = data['admin_id']
            marketing_daily_report.admin_name = data['admin_name']
            marketing_daily_report.day_time = follow[0]['statsDate']
            marketing_daily_report.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        marketing_daily_report.type = WeMediaType.WE_MEDIA.value.id
        marketing_daily_report.exposure_num = data['day_read_num'] + data['recommend_num']
        marketing_daily_report.recommend_num = data['recommend_num']
        marketing_daily_report.read_num = data['read_num']
        marketing_daily_report.day_read_num = data['day_read_num']
        marketing_daily_report.forward_num = data['forward_num']
        marketing_daily_report.like_num = 0
        marketing_daily_report.comment_num = data['comment_num']
        marketing_daily_report.publish_num = data['publish_num']
        marketing_daily_report.day_publish_num = data['day_publish_num']
        marketing_daily_report.follow_num = data['follow_num']
        marketing_daily_report.day_follow_num = follow[0]['incr'] if follow[0]['incr'] > 0 else 0
        marketing_daily_report.day_unfollow_num = data['follow_num'] - follow[0]['sum']
        marketing_daily_report.day_add_follow_num = (marketing_daily_report.day_follow_num
                                                     - marketing_daily_report.day_unfollow_num)
        marketing_daily_report.sex_proportion = {'man': 0.00, 'women': 0.00, 'unknown': 100.00}
        marketing_daily_report.age_proportion = {'man': 0.00, 'women': 0.00, 'unknown': 100.00}
        marketing_daily_report.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return marketing_daily_report

    @ staticmethod
    def get_millisecond():
        t = time.time()
        millisecond = int(round(t * 1000))
        return millisecond

    @ staticmethod
    def get_yesterday(day=1):
        today = datetime.date.today()
        one_day = datetime.timedelta(days=day)
        yesterday = today - one_day
        return yesterday
