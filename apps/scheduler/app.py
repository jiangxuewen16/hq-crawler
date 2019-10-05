from __future__ import absolute_import

import pika

from hq_crawler import celery_app


@celery_app.task
def add(x, y):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='118.126.105.239', port=5672, virtual_host='/', credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = ['hq.system.exception']

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='hq.system', queue='hq-lx.system.exception', routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    channel.basic_consume(
        queue='hq-lx.system.exception', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

    with open('C:/python/test_add_celery/books.txt', 'a', encoding='utf-8') as f:
        f.write('+++++++------')
    return x + y


@celery_app.task
def mul(x, y):
    return x * y
