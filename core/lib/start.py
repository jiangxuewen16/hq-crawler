import configparser
import os
import platform

import pika

from apps.scheduler.config.rabbitmq import RabbitMqReceive
from core.common.helper import get_scrapyd_cli
from hq_crawler import settings

"""
注册分布式爬虫到自定服务器
区分windows PyCharm环境 和 linux环境
"""


def start_deploy_scrapy(scrapyd_deploy: str = ''):
    scrapyd_project_list = get_scrapyd_cli().list_projects()

    spiderConf = configparser.ConfigParser()  # 爬虫项目配置
    spiderConf.read(f'{settings.BASE_DIR}/spiders/scrapy.cfg', encoding="utf-8")
    # SCRAPYD_URL = spiderConf.get('deploy', 'url')  # scrapyd地址

    scrapy_project_name = spiderConf.get('deploy', 'project')  # scrapyd地址

    # if scrapy_project_name not in scrapyd_project_list:
    if platform.system() == 'Windows':
        if scrapyd_deploy != '':
            cmd = f'cd {settings.SPIDER_PATH} && python {scrapyd_deploy} -p {scrapy_project_name}'
        else:
            cmd = f'cd {settings.SPIDER_PATH} && python {settings.BASE_DIR}\\venv\Scripts\\scrapyd-deploy -p {scrapy_project_name}'

        status = os.system(cmd)
        if status != 0:
            raise Exception('windows环境执行注册scrapyd项目错误，请检查目录路径、python环境，是否已安装scrapyd、scrapyd client')
    else:
        os.system(f'cd ./spiders && scrapyd-deploy -p {scrapy_project_name}')


"""
连接rabbitmq，并监听mq消息
"""


def start_rabbitmq():
    config = settings.RABBITMQ_CONF
    credentials = pika.PlainCredentials(config['user'], config['password'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config['host'], port=config['port'], virtual_host=config['vhost'], ))
    channel = connection.channel()

    settings.RABBITMQ_CHANNEL = channel  # 设置配置rabbitmq连接

    # 监听消息列表
    for _, member in RabbitMqReceive.__members__.items():
        channel.exchange_declare(exchange='hq.system', exchange_type='topic')

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
        print(member.value)

    # channel.exchange_declare(exchange='hq.system', exchange_type='topic')
    #
    # result = channel.queue_declare('', exclusive=True)
    # queue_name = result.method.queue
    #
    # binding_keys = ['hq.system.exception']
    #
    # for binding_key in binding_keys:
    #     channel.queue_bind(
    #         exchange='hq.system', queue='hq-lx.system.exception', routing_key=binding_key)
    #
    # print(' [*] Waiting for logs. To exit press CTRL+C')
    #
    # def callback(ch, method, properties, body):
    #     print(" [x] %r:%r" % (method.routing_key, body))
    #
    # channel.basic_consume(
    #     queue='hq-lx.system.exception', on_message_callback=callback, auto_ack=True)
    #
    # channel.start_consuming()


"""
项目环境配置:根据环境来自动切换项目环境配
"""


def project_env():
    env_dist = os.environ
    current_env = 'develop'
    if 'APP_ENV' in env_dist:
        current_env = env_dist['APP_ENV']
