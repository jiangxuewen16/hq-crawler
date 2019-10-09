from __future__ import absolute_import


from core.lib.rabbitmq import RabbitMq
from hq_crawler import celery_app, settings


@celery_app.task
def add():
    # print('='*30,RabbitMqReceive.__members__.items())
    # receive_list = [member.value for _, member in RabbitMqReceive.__members__.items()]
    # print('='*30,receive_list)
    RabbitMq(settings.RABBITMQ_CONF).receive()
    return True


@celery_app.task
def mul(x, y):
    return x * y
