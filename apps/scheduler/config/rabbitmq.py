from collections import namedtuple
from enum import Enum, unique

from apps.scheduler.mq.hqlx import Hqlx

mq_receive_item = namedtuple('mq_receive_item', 'name routing_key queue_name exchange callback')


@unique
class RabbitMqReceive(Enum):
    EXCEPTION = mq_receive_item('系统异常消息', 'hq.system.exception', 'hq-crawler.system.exception', 'hq.system',
                                Hqlx.exception)

    MMMMM = mq_receive_item('系统异常消息1', 'hq.system.exception', 'hq-crawler.system.exception', 'hq.system',
                                Hqlx.exception)
