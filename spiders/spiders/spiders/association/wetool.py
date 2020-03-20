import json
import time
from urllib import parse

import scrapy
from scrapy.http import HtmlResponse
from spiders.items.association.association import Association


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

    def start_requests(self):
        """
        登录
        scrapy默认get请求，所以重写初始方法
        :return:
        """
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
        处理群组消息 放入数据库
        :param response:
        :return:
        """
        response_str = response.body.decode('utf-8')
        list_member = json.loads(response_str)
        if list_member['errcode'] == 0:
            for chat_info in list_member['data']:
                association = Association.objects(chat_room_id=chat_info['wxid']).first()
                if not association:
                    association = Association()
                    association.chat_room_id = chat_info['wxid']
                    association.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                association.chat_room_member_count = chat_info['member_count']
                association.chat_room_nickname = chat_info['nickname']
                association.chat_room_owner_wxid = chat_info['owner_wxid']
                association.chat_room_avatar = 'http' + chat_info['avatar']
                association.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield association
