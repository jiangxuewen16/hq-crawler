from urllib import parse

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class UdeskSpider(scrapy.Spider):
    name = 'udesk'
    allowed_domains = ['shanshui.udesk.cn']
    start_urls = ['https://shanshui.udesk.cn/users/sign_in']
    login_url = 'https://shanshui.udesk.cn/users/sign_in'
    cookie_list = {}

    def start_requests(self):
        """
        后台登录 cookie与authenticity_token具有关联性
        :return:
        """
        url = 'https://shanshui.udesk.cn/users/sign_in'
        cookies_list = {
            'aliyungf_tc': 'AQAAAN6WoW6MCAcA3TQUOtrdKEYB6Vcq',
            'acw_tc': '76b20ff515882959474638255e1d85ee9c16692631d2070402fce6e1698fc4',
            'tid': 1217,
            'ifc': 0,
            '_ga': 'GA1.2.576172463.1588295977',
            '_gid': 'GA1.2.1306085414.1588295982',
            '_hjid': '20189b2e-9911-443e-b593-b58b15f91a37',
            'Hm_lvt_04a130f55f93916ac7fabec664481931': '1588295951,1588313997',
            '_helpdesksysteem_session': 'ZzQxZ3JJVGwrVkhMK1E5YVRHekdabFdNR0ZkWDhRSzY3NjhHYk1IcFA0dEg5RE1YKzJlenVmQXlCNk'
                                        '5iZ0NQd0dZRDJOVG0wWkpzbUlDMk5RaWYyR25rSm9XRnpXQlBtU0wzY2Z3RVJZYVUzZEdMREo4dEpk'
                                        'eEFabHppYzAvTDk4WFRadUVwZG9lZG5YV1Y5V0RaOW9iS0lNeUZIVnlpcmFpSmR3YWR3R1pXRVViek'
                                        'ZkUGxDWFZTSmZVT0lHUlpyWklNR3hFUWJXcDVHc3VNbk5xUVJqNGdhZDRKZGFRZnRKUEdxMGh4aUV0'
                                        'VzF5STNmZ1B3NkVINzI1dHAxek1tNi0ta2FlSm92cE9Dbk5YVXBHRnR1UTczdz09--d8c3968065db'
                                        'dc59d4d003f047feee9165baa2f6',
            'Hm_lpvt_04a130f55f93916ac7fabec664481931': '1588318547'
        }
        body = parse.urlencode({
            'utf8': '✓',
            'authenticity_token': '9dUpI9CC5NykECe4SPXvO2QyYwt+HPmgN9dp2diUV8Y=',
            'user[email]': '775731038@qq.com',
            'user[company_id]': '49291',
            'user[password]': 'zw18229459101',
            'user[remember_me]': '0',
            'commit': '登 录',
            'cellphone': '',
            'sms_captcha': '',
        })
        yield Request(url=url, body=body, dont_filter=True, method='POST', cookies=cookies_list,
                      meta={'dont_redirect': True, "handle_httpstatus_list": [302]})

    def parse(self, response):
        response_str = response.body.decode('utf-8')

    def detail_cookie(self, response: HtmlResponse):
        """
        将cookie转换为字符串方便放入header
        :param response:
        :return: string
        """
        request_cookie = ''
        cookie_list = response.headers.getlist('Set-Cookie')
        for cookie in cookie_list:
            request_cookie += bytes.decode(cookie) + '; '
        self.cookie_list = request_cookie
