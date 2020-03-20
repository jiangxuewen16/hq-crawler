import json
from urllib import parse

import scrapy


class WeToolSpider(scrapy.Spider):
    name = "wetool"
    allowed_domains = ['wp.wxb.com', 'account.wxb.com']
    start_urls = ['http://account.wxb.com/index2/login']
    request_cookie = ''

    def start_requests(self):
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
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        if json_data['errcode'] == 0:
            cookie_list = response.headers.getlist('Set-Cookie')
            for cookie in cookie_list:
                self.request_cookie += bytes.decode(cookie) + '; '
            yield scrapy.Request(url='',)

