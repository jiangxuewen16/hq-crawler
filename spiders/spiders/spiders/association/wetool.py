import json
import re
import time
import datetime
from urllib import parse

import scrapy
from scrapy.http import HtmlResponse

from spiders.items.association.wetool import TWetool, TWetoolDailyWechat
from spiders.items.association.association import TAssociation
from spiders.items.distributor.distributor import CDistributor


class WeToolListMemberSpider(scrapy.Spider):
    name = "wetool_list_member"
    allowed_domains = ['wp.wxb.com', 'account.wxb.com']
    start_urls = ['http://account.wxb.com/index2/login']
    wx_list = {
        '中惠旅内购客服': 'wxid_kqc0n5mpeivp22',
        '中惠旅内购客服1': 'wxid_ogz10j91aix112',
        '中惠旅内购客服2': 'wxid_08ey7r0i9dvz12',
        '中惠旅内购客服3': 'wxid_bqi9qznshsmy12',
        '中惠旅内购客服4': 'wxid_1yya6xpk3yre22',
        '中惠旅内购客服6': 'wxid_y6loz86fbkxo22',
        '中惠旅内购客服7': 'wxid_708w2ttyaz412',
        '趣哥': 'wxid_39iil8tclrdb22',
    }
    crm_list = []

    def start_requests(self):
        """
        登录
        scrapy默认get请求，所以重写初始方法
        :return:
        """
        self.get_all_crm()
        if not self.crm_list:
            return
        url = self.start_urls[0]
        post_data = parse.urlencode({
            'captcha': '',
            'email': '15616882820@zhaowei',
            'from': 'https://wp.wxb.com/',
            'password': 'zhlzhaowei',
            'remember': 'on'
        })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://account.wxb.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://account.wxb.com/page/login?from=https%3A%2F%2Fwp.wxb.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        yield scrapy.FormRequest(url=url, body=post_data, method='POST', headers=headers)

    def parse(self, response):
        """
        获取用户群组
        :param response: HtmlResponse
        :return:
        """
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        if json_data['errcode'] == 0:
            request_cookie = self.detail_cookie(response)
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'wp-api.wxb.com',
                'Origin': 'https://wp.wxb.com',
                'Referer': 'https://wp.wxb.com/cloud',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.132 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': request_cookie
            }
            for name in self.wx_list:
                yield scrapy.Request(url='https://wp-api.wxb.com/chat/listMember?wxid=' + self.wx_list[name] +
                                         '&member_type=2', headers=headers, method='GET',
                                     callback=self.parse_wx, dont_filter=True, meta={'account': self.wx_list[name]})

    @staticmethod
    def detail_cookie(response: HtmlResponse):
        """
        将cookie转换为字符串方便放入header
        :param response:
        :return: string
        """
        request_cookie = ''
        cookie_list = response.headers.getlist('Set-Cookie')
        for cookie in cookie_list:
            request_cookie += bytes.decode(cookie) + '; '
        return request_cookie

    @staticmethod
    def parse_wx(response):
        """
        处理群组消息
        :param response:
        :return:
        """
        response_str = response.body.decode('utf-8')
        list_member = json.loads(response_str)
        num_list = {}
        if list_member['errcode'] == 0:
            account = response.meta['account']
            for chat_info in list_member['data']:
                match = re.search(r'.*?(\d{4,10})', chat_info['nickname'])
                if match:
                    wetool = TWetool.objects(chat_room_id=chat_info['wxid']).order_by('-update_at').first()
                    association = TAssociation.objects(team_group_id=match.group(1)).first()
                    cal_member_count = original_member_count = member_count = int(chat_info['member_count'])
                    if wetool:
                        if 500 > wetool.chat_room_member_count > 0 and (member_count > 500 or member_count <= 0):
                            cal_member_count = member_count = wetool.chat_room_member_count
                    if member_count > 500 or member_count < 0:
                        cal_member_count = 0
                    distributor_id = channel_id = "0"
                    cd = CDistributor.objects(team_group_id=match.group(1)).first()
                    if cd is not None:
                        channel_id = cd.channel_id
                        distributor_id = cd.distributor_id

                    if association:
                        if match.group(1) in num_list:
                            num_list[match.group(1)] = [num_list[match.group(1)][0] + cal_member_count,
                                                        num_list[match.group(1)][1] + 1]
                        else:
                            num_list[match.group(1)] = [cal_member_count, 1]

                        association.chat_room_id = chat_info['wxid']
                        association.chat_room_member_count = num_list[match.group(1)][0]
                        association.chat_room_nickname = chat_info['nickname']
                        association.chat_room_owner_wxid = chat_info['owner_wxid']
                        association.char_room_sum = num_list[match.group(1)][1]
                        association.chat_room_avatar = 'http' + chat_info['avatar']
                        association.update_at = time.strftime("%Y-%m-%d", time.localtime())
                        association.channel_id = channel_id
                        yield association
                    if not wetool:
                        wetool = TWetool()
                        wetool.chat_room_id = chat_info['wxid']
                        wetool.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        wetool.create_date = time.strftime("%Y-%m-%d", time.localtime())
                        wetool.chat_room_member_count = original_member_count
                        wetool.account = account
                    else:
                        if time.strftime("%Y-%m-%d", time.localtime()) != wetool.create_date:
                            wetool = TWetool()
                            wetool.chat_room_id = chat_info['wxid']
                            wetool.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            wetool.create_date = time.strftime("%Y-%m-%d", time.localtime())
                            wetool.account = account
                        wetool.chat_room_member_count = member_count
                    wetool.team_group_id = match.group(1)
                    wetool.chat_room_nickname = chat_info['nickname']
                    wetool.chat_room_owner_wxid = chat_info['owner_wxid']
                    wetool.chat_room_avatar = 'http:' + chat_info['avatar']
                    wetool.channel_id = channel_id
                    wetool.distributor_id = distributor_id
                    wetool.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    yield wetool

    def get_all_crm(self):
        """
        获取所有crm团长群编码
        :return:
        """
        association = TAssociation.objects().all()
        for ass in association:
            self.crm_list.append(ass.team_group_id)


class WeToolDailyWechatSpider(scrapy.Spider):
    name = "wetool_daily_wechat"
    allowed_domains = ['wp.wxb.com', 'account.wxb.com']
    start_urls = ['http://account.wxb.com/index2/login']

    crm_list = []

    def start_requests(self):
        """
        登录
        scrapy默认get请求，所以重写初始方法
        :return:
        """
        url = self.start_urls[0]
        post_data = parse.urlencode({
            'captcha': '',
            'email': '15616882820@zhaowei',
            'from': 'https://wp.wxb.com/',
            'password': 'zhlzhaowei',
            'remember': 'on'
        })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://account.wxb.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://account.wxb.com/page/login?from=https%3A%2F%2Fwp.wxb.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        yield scrapy.FormRequest(url=url, body=post_data, method='POST', headers=headers)

    def parse(self, response):
        """
        获取用户群组
        :param response: HtmlResponse
        :return:
        """
        start_time = self.get_time('startTime')
        end_time = self.get_time('endTime')
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        if json_data['errcode'] == 0:
            request_cookie = self.detail_cookie(response)
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'wp-api.wxb.com',
                'Origin': 'https://wp.wxb.com',
                'Referer': 'https://wp.wxb.com/report',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.132 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': request_cookie
            }

            yield scrapy.Request(url='https://wp-api.wxb.com/stat/dailyWechat?s_date=' + start_time + '&e_date=' + end_time,
                                 headers=headers, method='GET',
                                 callback=self.daily_wechat, dont_filter=True)

    def daily_wechat(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        if json_data['errcode'] == 0:
            list_data = json_data['list']
            today_data = json_data['today']
            data = [list_data[0], today_data]
            for item in data:
                wetool_daily_report = TWetoolDailyWechat.objects(
                    create_date=item['date_key']).first()
                if not wetool_daily_report:
                    wetool_daily_report = TWetoolDailyWechat()
                    wetool_daily_report.create_date = item['date_key']
                    wetool_daily_report.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                wetool_daily_report.group_send_msg_num = str(item['group_send_msg_num'])
                wetool_daily_report.single_send_msg_num = str(item['single_send_msg_num'])
                wetool_daily_report.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield wetool_daily_report

    @staticmethod
    def detail_cookie(response: HtmlResponse):
        """
        将cookie转换为字符串方便放入header
        :param response:
        :return: string
        """
        request_cookie = ''
        cookie_list = response.headers.getlist('Set-Cookie')
        for cookie in cookie_list:
            request_cookie += bytes.decode(cookie) + '; '
        return request_cookie

    @staticmethod
    def get_time(tip='startTime'):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        if tip == 'startTime':
            # return datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            return yesterday.strftime('%Y-%m-%d')
        else:
            return datetime.datetime.now().strftime('%Y-%m-%d')