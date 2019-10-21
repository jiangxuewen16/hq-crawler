import datetime
import math
import time

from apps.api.common.helper import helper
from apps.api.model.exception import ExcLog
from apps.monitor.service import rabbitmq_service
from core.lib.route import Route
from core.lib.view import BaseView

import requests


@Route.route(path='api/watch/public/opinion')
class PublicOpinion(BaseView):

    # 查看准备 的 和未确认 的消息数
    @Route.route(path='/queues')
    def get_queues(self):
        result = rabbitmq_service.Rabbit.get_ready_no_ack()
        return self.success(result)

    # 通道监控
    @Route.route(path='/channels')
    def get_channels(self):
        result = rabbitmq_service.Rabbit.get_channels()
        return self.success(result)

    # curl接口测试
    @Route.route(path='/list')
    def post_test(self):
        url = 'https://api.huiqulx.com/appapi/console/Ad_group/getAdByPlace'
        post_data = '{"head":{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVfdGltZSI6MTU3Mzg2ODgwOSwidXNlckluZm8iOnsidV9pZCI6IjYyOTQ4ODYiLCJ1X3R5cGUiOjEsInVfbmFtZSI6IjE4NjEzOTgxNTcyIn0sImlkZW50aWZpY2F0aW9uIjoiN2IxMjdiNGQ2MDBiYzgwN2M3YzJkMWVjOTE1NDhiZTYiLCJleHQiOltdfQ.TdOutB2IJ1plaotzBzukLjry9jeH4x-Tw2j3lCoKjB0","time":1571276815386,"version":"1.0","platform":"40","recode":"","excode":"","qrcode":""},"data":{"place":"120001"}}'
        headers = {'content-type': 'application/json'}
        data = requests.post(url, headers=headers, data=post_data)
        result = data.json()
        return self.success(result)

    # 异常数据可视化
    @Route.route(path='/exception/list')
    def exception_list(self):
        param = self.request_param
        condition = {
            'begin_date': helper.get_param(param=param, in_name='begin_date',
                                           default="2000-01-01"),
            'end_date': helper.get_param(param=param, in_name='end_date',
                                         default=time.strftime("%Y-%m-%d", time.localtime())),
        }
        page = helper.get_param(param=param, in_name='page', default=1)
        limit = helper.get_param(param=param, in_name='limit', default=20)
        skip = (page - 1) * limit
        result = ExcLog.select_all(skip, limit, condition=condition)
        total = ExcLog.count(condition=condition)
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'list': result}
        return self.success(data)

    """
    条件：时间段
    按接口名、分组统计报错接口
    """

    @Route.route(path='/exception/group')
    def exception_group(self):
        param = self.request_param
        condition = {
            'begin_date': helper.get_param(param=param, in_name='begin_date',
                                           default="2000-01-01 00:00:00"),
            'end_date': helper.get_param(param=param, in_name='end_date',
                                         default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
        }
        data = ExcLog.group_by_name(condition=condition)
        return self.success(data)
