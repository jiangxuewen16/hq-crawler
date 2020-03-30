import json
import re
import time
from urllib import parse

import scrapy
from scrapy.http import HtmlResponse

from spiders.items.association.wetool import TWetool
from spiders.items.association.association import TAssociation


class WeToolListMemberSpider(scrapy.Spider):
    name = "wetool_list_member"
    allowed_domains = ['wp.wxb.com', 'account.wxb.com']
    start_urls = ['http://account.wxb.com/index2/login']
    wx_list = {
        '中惠旅内购客服': 'wxid_kqc0n5mpeivp22',
        '中惠旅内购客服1': 'wxid_ogz10j91aix112',
        '中惠旅内购客服2': 'wxid_08ey7r0i9dvz12',
        '中惠旅内购客服3': 'wxid_bqi9qznshsmy12',
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
            'email': '15616882820@jxw',
            'from': 'https://wp.wxb.com/',
            'password': 'jxw123456',
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
                                     callback=self.parse_wx, dont_filter=True)

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
        if list_member['errcode'] == 0:
            for chat_info in list_member['data']:
                print('+++++++++++++++++++', int(chat_info['member_count']))
                match = re.search(r'惠[旅|趣]商城\D*(\d*)', chat_info['nickname'])
                if match:
                    wetool = TWetool.objects(chat_room_id=chat_info['wxid']).first()
                    association = TAssociation.objects(team_group_id=match.group(1)).first()
                    num_list = {}

                    member_count = int(chat_info['member_count'])
                    if member_count > 500:
                        member_count = 0
                    if association:
                        if match.group(1) in num_list:
                            num_list[match.group(1)] = num_list[match.group(1)] + member_count
                        else:
                            num_list[match.group(1)] = member_count
                        association.chat_room_id = chat_info['wxid']
                        association.chat_room_member_count = num_list[match.group(1)]
                        association.chat_room_nickname = chat_info['nickname']
                        association.chat_room_owner_wxid = chat_info['owner_wxid']
                        association.chat_room_avatar = 'http' + chat_info['avatar']
                        association.update_at = time.strftime("%Y-%m-%d", time.localtime())
                        yield association
                    if not wetool:
                        wetool = TWetool()
                        wetool.chat_room_id = chat_info['wxid']
                        wetool.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    wetool.team_group_id = match.group(1)
                    wetool.chat_room_member_count = chat_info['member_count']
                    wetool.chat_room_nickname = chat_info['nickname']
                    wetool.chat_room_owner_wxid = chat_info['owner_wxid']
                    wetool.chat_room_avatar = 'http' + chat_info['avatar']
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
