import json

from apps.monitor.service import exception_service
from core.lib import rabbitmq
from django.utils.autoreload import logger

"""
异常消息接收
"""


# @rabbitmq.Decorator.listen('hq.system.exception', 'hq-crawler.system.exception', 'hq.system', True)  # rabbitmq 消息监听
# def receive_exception(ch, method, properties, body):
#     logger.info('=' * 20, ch, method, properties, body)
#     body = body.decode('utf-8')
#     json_data = json.loads(body)
#     exception_service.receive_exception(json_data)
