import datetime
import json
import time
from urllib import parse

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.items.customer import customer


class UdeskSpider(scrapy.Spider):
    name = 'udesk'
    allowed_domains = ['shanshui.udesk.cn', 'cbi.udesk.cn']
    start_urls = ['https://shanshui.udesk.cn/users/sign_in']
    login_url = 'https://shanshui.udesk.cn/users/sign_in'

    search_url = 'https://shanshui.udesk.cn/spa1/customers/search'
    cookie_list = {}
    page_size = 100  # 默认爬取每页100条

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
                      callback=self.parse, meta={'dont_redirect': True, "handle_httpstatus_list": [302]})

    def parse(self, response):
        self.detail_cookie(response)
        cookie = self.cookie_list
        start_time = self.get_time('startTime')

        end_time = self.get_time('endTime')
        post_data = json.dumps({
            "all_conditions": [
                {"field_name": "updated_at", "operation": "range", "value": start_time + "," + end_time}],
            "filter_id": "596016",
            "order": "",
            "column": "",
            "page": 1,
            "page_size": 100,
            "sort_by": [["created_at", "desc"]]
        })
        url = self.search_url
        yield Request(url=url, method="POST", body=post_data,
                      headers={'Content-Type': 'application/json'},
                      cookies=cookie, callback=self.parse_count,
                      dont_filter=True,
                      meta={'cookies': cookie}
                      )

    def parse_count(self, response: HtmlResponse):
        data = json.loads(response.body.decode('utf-8'))
        total_pages = data['meta']['total_pages']
        cookies = response.meta['cookies']
        page_size = self.page_size
        page = 1
        start_time = self.get_time('startTime')
        end_time = self.get_time('endTime')
        post_data = json.dumps({
            "all_conditions": [
                {"field_name": "updated_at", "operation": "range", "value": start_time + "," + end_time}],
            "filter_id": "596016",
            "order": "",
            "column": "",
            "page": page,
            "page_size": page_size,
            "sort_by": [["created_at", "desc"]]
        })
        url = self.search_url

        yield Request(url=url,
                      method="POST",
                      body=post_data,
                      cookies=cookies,
                      headers={'Content-Type': 'application/json'},
                      callback=self.parse_page,
                      dont_filter=True,
                      meta={'page': page,
                            'page_size': page_size,
                            'total_pages': total_pages,
                            'cookies': cookies})

    def parse_page(self, response: HtmlResponse):
        data = json.loads(response.body.decode('utf-8'))
        for item in data['customers']:
            customer_consultation = customer.CustomerConsultation.objects(
                udesk_id=item['id'],
                stat_at=item['updated_at'].split('T')[0]).first()
            if not customer_consultation:
                customer_consultation = customer.CustomerConsultation()
                customer_consultation.udesk_id = item['id']
                customer_consultation.agent = item['owner_name']
                customer_consultation.work_id = item['owner_id']
                customer_consultation.stat_at = item['updated_at'].split('T')[0]
                customer_consultation.nick_name = item['nick_name']
                customer_consultation.tags = item['tags']
                customer_consultation.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            customer_consultation.cellphone = item['cellphones'][0]['content'] if \
                len(item['cellphones']) > 0 else ''
            customer_consultation.source_channel = item['source_channel']
            if item['custom_fields']:
                if 'SelectField_15208' in item['custom_fields']:
                    customer_consultation.source_platform = item['custom_fields']['SelectField_15208'][0]
                else:
                    customer_consultation.source_platform = ''

                if 'SelectField_15210' in item['custom_fields']:
                    customer_consultation.consulting_scenic_spot = item['custom_fields']['SelectField_15210'][0]
                else:
                    customer_consultation.consulting_scenic_spot = ''
                if 'SelectField_54171' in item['custom_fields']:
                    customer_consultation.consulting_type = item['custom_fields']['SelectField_54171'][0]
                else:
                    customer_consultation.consulting_type = ''
            else:
                customer_consultation.source_platform = ''
                customer_consultation.consulting_scenic_spot = ''
                customer_consultation.consulting_type = ''
            customer_consultation.phone_service_provider = item['phone_service_provider'] if \
                item['phone_service_provider'] is not None else item['from']
            customer_consultation.province = item['province']
            customer_consultation.city = item['city']
            customer_consultation.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield customer_consultation

        start_offset = response.meta['page'] + 1
        if start_offset <= response.meta['total_pages']:
            start_time = self.get_time('startTime')
            end_time = self.get_time('endTime')
            post_data = json.dumps({
                "all_conditions": [
                    {"field_name": "updated_at", "operation": "range", "value": start_time + "," + end_time}],
                "filter_id": "596016",
                "order": "",
                "column": "",
                "page": start_offset,
                "page_size": response.meta['page_size'],
                "sort_by": [["created_at", "desc"]]
            })
            url = self.search_url
            yield Request(url=url,
                          method="POST",
                          body=post_data,
                          cookies=response.meta['cookies'],
                          headers={'Content-Type': 'application/json'},
                          callback=self.parse_page,
                          dont_filter=True,
                          meta={'page': start_offset,
                                'page_size': response.meta['page_size'],
                                'total_pages': response.meta['total_pages'],
                                'cookies': response.meta['cookies']})

    def detail_cookie(self, response: HtmlResponse):
        """
        将cookie转换为字符串方便放入header
        :param response:
        :return: string
        """
        request_cookie = ''
        cookie_list = response.headers.getlist('Set-Cookie')

        for cookie in cookie_list:
            kv = bytes.decode(cookie).strip().split('=')
            self.cookie_list[kv[0]] = kv[1]

    @staticmethod
    def get_time(tip='startTime'):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        if tip == 'startTime':
            # return datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            return yesterday.strftime('%Y-%m-%d 00:00:00')
        else:
            return datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')
            # return yesterday.strftime('%Y-%m-%d 23:59:59')


class CustomerDailyReportSpider(scrapy.Spider):
    name = 'customer_daily_report'
    allowed_domains = ['shanshui.udesk.cn', 'cbi.udesk.cn']
    base_url = 'https://cbi.udesk.cn/backend/report/cc_agent_callin?source=CS&token=QUhom_xcgsQKQifVR_fH'
    start_urls = [
        'https://cbi.udesk.cn/backend/report/cc_agent_callin?source=CS&token=QUhom_xcgsQKQifVR_fH']

    callout_url = 'https://cbi.udesk.cn/backend/report/cc_agent_callout?source=CS&token=QUhom_xcgsQKQifVR_fH'
    performance_url = 'https://cbi.udesk.cn/backend/report/cc_agent_performance?source=CS&token=QUhom_xcgsQKQifVR_fH'
    im_agent_workload_url = 'https://cbi.udesk.cn/backend/report/im_agent_workload?source=CS&token=QUhom_xcgsQKQifVR_fH'
    im_agent_workquality_url = 'https://cbi.udesk.cn/backend/report/im_agent_workquality?source=CS&token=QUhom_xcgsQ' \
                               'KQifVR_fH'

    def start_requests(self):
        start_time = self.get_time('startTime')
        end_time = self.get_time('endTime')
        time_list = self.get_every_day(start_time, end_time)

        for item in time_list:
            start_time = item
            post_data = json.dumps({
                'ids': [],
                'orderField': '',
                'orderType': 'none',
                'pageNum': 1,
                'pageSize': 20,
                'permission': 'all',
                'statAt': [start_time + ' 00:00:00', start_time + ' 23:59:59'],
                'timeStrategy': 'work',
            })

            url = self.base_url
            yield Request(url=url
                          , method="POST"
                          , body=post_data
                          , headers={'Content-Type': 'application/json'}
                          , callback=self.callin_daily_report
                          , meta={'start_time': start_time})

    def callin_daily_report(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        start_time = response.meta['start_time']
        # start_time = self.get_time('startTime')
        # end_time = self.get_time('endTime')
        if json_data['code'] == 200:
            data = json_data['data']['rows']
            for telephone_data in data:
                post_data = json.dumps({
                    'ids': [telephone_data['cc_agent_callin__agent_id']],
                    'orderField': '',
                    'orderType': 'none',
                    'pageNum': 1,
                    'pageSize': 20,
                    'permission': 'all',
                    'statAt': [start_time + ' 00:00:00', start_time + ' 23:59:59'],
                    'timeStrategy': 'work',
                })
                url = self.callout_url
                yield Request(url=url
                              , method="POST"
                              , body=post_data
                              , headers={'Content-Type': 'application/json'}
                              , callback=self.callout_daily_report
                              , meta={'telephone_data': telephone_data, 'start_time': start_time})

    def callout_daily_report(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        telephone_data = response.meta['telephone_data']
        start_time = response.meta['start_time']

        if json_data['code'] == 200:
            callout_data = json_data['data']['rows']
            post_data = json.dumps({
                'ids': [telephone_data['cc_agent_callin__agent_id']],
                'orderField': '',
                'orderType': 'none',
                'pageNum': 1,
                'pageSize': 20,
                'permission': 'all',
                'statAt': [start_time + ' 00:00:00', start_time + ' 23:59:59'],
                'timeStrategy': 'work',
            })
            url = self.performance_url
            yield Request(url=url
                          , method="POST"
                          , body=post_data
                          , headers={'Content-Type': 'application/json'}
                          , callback=self.performance_daily_report
                          , meta={'telephone_data': telephone_data, 'callout_data': callout_data,
                                  'start_time': start_time})

    def performance_daily_report(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        telephone_data = response.meta['telephone_data']
        callout_data = response.meta['callout_data']
        start_time = response.meta['start_time']
        # start_time = self.get_time('startTime')
        # end_time = self.get_time('endTime')
        if json_data['code'] == 200:
            performance_data = json_data['data']['rows']
            post_data = json.dumps({
                'ids': [telephone_data['cc_agent_callin__agent_id']],
                'orderField': '',
                'orderType': 'none',
                'pageNum': 1,
                'pageSize': 20,
                'permission': 'all',
                'statAt': [start_time + ' 00:00:00', start_time + ' 23:59:59'],
                'timeStrategy': 'work',
            })
            url = self.im_agent_workload_url
            yield Request(url=url
                          , method="POST"
                          , body=post_data
                          , headers={'Content-Type': 'application/json'}
                          , callback=self.im_agent_workload
                          , meta={'telephone_data': telephone_data, 'callout_data': callout_data,
                                  'performance_data': performance_data,
                                  'start_time': start_time})

    def im_agent_workload(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        telephone_data = response.meta['telephone_data']
        callout_data = response.meta['callout_data']
        performance_data = response.meta['performance_data']
        start_time = response.meta['start_time']
        if json_data['code'] == 200:
            workload = json_data['data']['rows']
            post_data = json.dumps({
                'ids': [telephone_data['cc_agent_callin__agent_id']],
                'orderField': '',
                'orderType': 'none',
                'pageNum': 1,
                'pageSize': 20,
                'permission': 'all',
                'statAt': [start_time + ' 00:00:00', start_time + ' 23:59:59'],
                'timeStrategy': 'work',
            })
            url = self.im_agent_workquality_url
            yield Request(url=url
                          , method="POST"
                          , body=post_data
                          , headers={'Content-Type': 'application/json'}
                          , callback=self.im_agent_workquality
                          , meta={'telephone_data': telephone_data, 'callout_data': callout_data,
                                  'performance_data': performance_data,
                                  'workload_data': workload})

    def im_agent_workquality(self, response: HtmlResponse):
        json_data = json.loads(response.body.decode('utf-8'))
        telephone_data = response.meta['telephone_data']
        callout_data = response.meta['callout_data']
        performance_data = response.meta['performance_data']
        workload_data = response.meta['workload_data']
        if json_data['code'] == 200:
            workquality_data = json_data['data']['rows']
            # print(float(workquality_data[0][
            #           'im_agent_workquality__answered_30s_dialog_rate'].strip('%')) /100)
            customer_daily_report = customer.CustomerDailyReport.objects(
                work_id=telephone_data['cc_agent_callin__agent_id'],
                stat_at=telephone_data['cc_agent_callin__stat_at'].split(' ')[0]).first()

            if not customer_daily_report:
                customer_daily_report = customer.CustomerDailyReport()
                customer_daily_report.agent = telephone_data['cc_agent_callin__agent']
                customer_daily_report.work_id = telephone_data['cc_agent_callin__agent_id']
                customer_daily_report.stat_at = telephone_data['cc_agent_callin__stat_at'].split(' ')[0]
                # customer_daily_report.telephone_proportion = {
                #     'callin_count': telephone_data['cc_agent_callin__callin_count'],
                #     'callin_answered_count': telephone_data['cc_agent_callin__callin_answered_count'],
                #     'callin_ringing_total_time': telephone_data['cc_agent_callin__callin_ringing_total_time'],
                #     'callin_answered_total_time': telephone_data[
                #         'cc_agent_callin__callin_answered_total_time'],
                #     'callin_ringing_answered_avg_time': telephone_data[
                #         'cc_agent_callin__callin_ringing_answered_avg_time'],
                #     'callin_answered_rate': telephone_data[
                #         'cc_agent_callin__callin_answered_rate'],
                #     'callin_ringing_answered_within_15s_count': telephone_data[
                #         'cc_agent_callin__callin_ringing_answered_within_15s_count'],
                #     'callin_ringing_answered_within_15s_rate': telephone_data[
                #         'cc_agent_callin__callin_ringing_answered_within_15s_rate'],
                #     'callout_count': callout_data[0]['cc_agent_callout__callout_count'],
                #     'callout_answered_total_time': callout_data[0][
                #         'cc_agent_callout__callout_answered_duration_total_time'],
                #     'satisfied': '100%'}
                # customer_daily_report.im_proportion = {
                #     'dialog_count': workload_data[0][
                #         'im_agent_workload__dialog_count'],
                #     'customer_message_count': workload_data[0][
                #         'im_agent_workload__valid_dialog_count'],
                #     'agent_message_count': workload_data[0][
                #         'im_agent_workload__served_client_cnt'],
                #     'avg_first_answered_seconds': workquality_data[0][
                #         'im_agent_workquality__avg_first_answered_seconds'],
                #     'appraise_avg_score': workquality_data[0][
                #         'im_agent_workquality__appraise_avg_score'],
                #     'answered_30s_dialog_rate': workquality_data[0][
                #         'im_agent_workquality__first_answered_30s_dialog_rate'],
                #     'answered_30s_count': float(workquality_data[0][
                #                           'im_agent_workquality__first_answered_30s_dialog_rate'].strip('%')) / 100 * int(workload_data[0][
                #                           'im_agent_workload__dialog_count'])
                # }
                customer_daily_report.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            customer_daily_report.telephone_proportion = {
                'callin_count': telephone_data['cc_agent_callin__callin_count'],
                'callin_answered_count': telephone_data['cc_agent_callin__callin_answered_count'],
                'callin_ringing_total_time': telephone_data['cc_agent_callin__callin_ringing_total_time'],
                'callin_answered_total_time': telephone_data[
                    'cc_agent_callin__callin_answered_total_time'],
                'callin_ringing_answered_avg_time': telephone_data[
                    'cc_agent_callin__callin_ringing_answered_avg_time'],
                'callin_answered_rate': telephone_data[
                    'cc_agent_callin__callin_answered_rate'],
                'callin_ringing_answered_within_15s_count': telephone_data[
                    'cc_agent_callin__callin_ringing_answered_within_15s_count'],
                'callin_ringing_answered_within_15s_rate': telephone_data[
                    'cc_agent_callin__callin_ringing_answered_within_15s_rate'],
                'callin_survey': float(performance_data[0][
                    'cc_agent_performance__callin_survey_47061-94285_r@e@value'].strip(
                    '%')) / 100,
                'callin_survey_count': '1' if float(performance_data[0][
                    'cc_agent_performance__callin_survey_47061-94285_r@e@value'].strip(
                    '%')) / 100 > 0 else '0',
                'callout_count': callout_data[0]['cc_agent_callout__callout_count'],
                'callout_answered_total_time': callout_data[0][
                    'cc_agent_callout__callout_answered_duration_total_time'],
                'satisfied': '100%'}
            customer_daily_report.im_proportion = {
                'dialog_count': workload_data[0][
                    'im_agent_workload__dialog_count'],
                'customer_message_count': workload_data[0][
                    'im_agent_workload__valid_dialog_count'],
                'agent_message_count': workload_data[0][
                    'im_agent_workload__served_client_cnt'],
                'avg_first_answered_seconds': workquality_data[0]['im_agent_workquality__avg_first_answered_seconds'],
                'avg_first_answered_seconds_count': self.split_time(
                    workquality_data[0]['im_agent_workquality__avg_first_answered_seconds']) * int(workload_data[0][
                                                                                                       'im_agent_workload__dialog_count']),
                'appraise_total_score': workquality_data[0][
                    'im_agent_workquality__appraise_total_score'],
                'appraise_count': workquality_data[0][
                    'im_agent_workquality__appraise_count'],
                'appraise_avg_score': workquality_data[0][
                    'im_agent_workquality__appraise_avg_score'],
                'answered_30s_dialog_rate': workquality_data[0][
                    'im_agent_workquality__first_answered_30s_dialog_rate'],
                'answered_30s_count': float(workquality_data[0][
                                                'im_agent_workquality__first_answered_30s_dialog_rate'].strip(
                    '%')) / 100 * int(workload_data[0][
                                          'im_agent_workload__dialog_count'])
            }
            customer_daily_report.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield customer_daily_report

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
            # return yesterday.strftime('%Y-%m-%d 23:59:59')

    @staticmethod
    def split_time(time_str=None):
        line = time_str.split(":")
        seconds = int(line[0]) * 3600 + int(line[1]) * 60 + int(line[2])
        return seconds

    @staticmethod
    def get_every_day(begin_date, end_date):
        # 前闭后闭
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list
