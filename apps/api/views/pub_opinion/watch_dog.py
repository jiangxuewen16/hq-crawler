import math

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

    @Route.route(path='/exception/list')
    def exception_list(self):
        page = 1
        limit = 20
        skip = (page - 1) * limit
        result = ExcLog.select_all()
        total = ExcLog.count()
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'list': result}
        # result = ExcLog.select_all()
        # result = ExcLog.count()
        return self.success(str(helper.get_yesterday()))
