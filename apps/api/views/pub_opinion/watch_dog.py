import json

import requests

from apps.monitor.service import rabbitmq_service
from core.lib.route import Route
from core.lib.view import BaseView
from hq_crawler import settings


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
