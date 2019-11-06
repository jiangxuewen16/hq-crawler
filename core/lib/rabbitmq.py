from collections import namedtuple

import pika

mq_receive_item = namedtuple('mq_receive_item', 'routing_key queue_name exchange callback no_ack')


class RabbitMq(object):
    config: dict = {
        'host': '118.126.105.239',
        'port': 5672,
        'user': 'guest',
        'password': 'guest',
        'vhost': '/',

        'passive': False,
        'durable': True,
        'auto_delete': False,
        'exclusive': False,
        'no_local': False,
        'no_ack': False,
        'nowait': False,
        'consumer_tag': '',
    }

    channel = ''

    def __init__(self, config: dict):
        self.config = {**self.config, **config}
        self.connection = self.__conn()
        self.channel = self.__channel()

    def __conn(self):
        credentials = pika.PlainCredentials(self.config['user'], self.config['password'])
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['host'], port=self.config['port'],
                                      virtual_host=self.config['vhost'], credentials=credentials))

    def __channel(self):
        return self.connection.channel()

    """
    接收消息（监听）
    """

    def receive(self):
        receive_list = Decorator.RECEIVE_FUNC_LIST
        for item in receive_list:
            print('=' * 20, item)
            self.channel.exchange_declare(exchange=item.exchange, exchange_type='topic',
                                          passive=self.config['passive'], durable=self.config['durable'],
                                          auto_delete=self.config['auto_delete'])
            result = self.channel.queue_declare(item.queue_name, passive=self.config['passive'],
                                                durable=self.config['durable'],
                                                exclusive=self.config['exclusive'],
                                                auto_delete=self.config['auto_delete'])
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=item.exchange, queue=queue_name, routing_key=item.routing_key)
            print(' [*] 启动监听:', item.exchange, queue_name, item.routing_key)
            self.channel.basic_consume(queue=queue_name, on_message_callback=item.callback,
                                       auto_ack=item.no_ack)
        self.channel.start_consuming()
        self.close()

    """
    发送消息
    """

    def send(self, message: str, routing_key: str, exchange=''):
        if not exchange:
            str_list = routing_key.split('.')
            exchange = str_list[0] + '.' + str_list[1]

        self.channel.exchange_declare(exchange=exchange, exchange_type='topic',
                                      passive=self.config['passive'], durable=self.config['durable'],
                                      auto_delete=self.config['auto_delete'])
        self.channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
        print(" [x] Sent %r:%r" % (routing_key, message))
        self.close()

    def close(self):
        self.connection.close()

    def callback(self):
        pass


class Decorator(object):
    RECEIVE_FUNC_LIST: list = []

    """
    rabbitmq接收装饰器
    """

    @classmethod
    def listen(cls, routing_key: str, queue_name: str, exchange: str, no_ack: bool = False):
        def my_decorator(func):
            receive_item = mq_receive_item(routing_key, queue_name, exchange, func, no_ack)
            cls.RECEIVE_FUNC_LIST.append(receive_item)

            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)
            return wrapper
        return my_decorator
