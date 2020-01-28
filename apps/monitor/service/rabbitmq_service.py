import json

import requests

from apps.monitor.common import helper
from hq_crawler import settings
from django.utils.autoreload import logger

default_email = '445251692@qq.com'


def send_email():
    channels = Rabbit.get_channels()
    num = len(channels)
    whether_send = False
    send_str = """<table><tr><th>节点</th><th>连接名称</th><th>连接信息</th><th>列队数量</th><th>未确认数量</th>
    <th>用户</th><th>虚拟主机</th></tr>"""
    if channels:
        for item in channels:
            send_str += f"""<tr>
            <td>{item['node']}</td>
            <td>{item['name']}</td>
            <td>{item['connection_details']['peer_host']}:{item['connection_details']['peer_port']}</td>
            <td>{item['consumer_count']}</td>
            <td>{item['messages_unconfirmed']}</td>
            <td>{item['user']}</td>
            <td>{item['vhost']}</td>
            </tr>"""
    else:
        send_str += """<tr>无任何服务</tr>"""
    send_str += """</table>"""

    if num < 4:
        whether_send = True

    queues = Rabbit.get_ready_no_ack()
    if queues:
        send_str += """<table><tr><th>通道名称</th><th>消息数量</th><th>未确认消息</th><th>未消费消息</th></tr>"""
        whether_send = True
        for item in queues:
            send_str += f"""
             <tr><td>{item['name']}</td><td>{item['messages']}</td><td>{item['messages_unacknowledged']}</td>
             <td>{item['messages_ready']}</td></tr>
            """
        send_str += """</table>"""

    if whether_send:
        helper.send_email([default_email], [default_email], '惠趣rabbitmq异常通知', send_str)


def rabbit_api(route):
    conf = settings.RABBITMQ_CONF
    host = conf.get('host')
    port = str(conf.get('api_port'))
    user = conf.get('user')
    password = conf.get('password')
    # url = 'http://39.108.101.109:65531/api/channels'
    url = 'http://' + host + ':' + port + '/api/' + route
    # logger.info(url)
    return requests.get(url, auth=(user, password), timeout=5)


class Rabbit:
    @classmethod
    def get_ready_no_ack(cls):
        r = rabbit_api(route='queues')
        parsed = json.loads(r.content)
        L = []
        for i in parsed:
            if ((i.get('messages_ready') != 0) or (i.get('messages_unacknowledged') != 0)) and (
                    'x-dead-letter-exchange' not in i.get('arguments')):
                elm = {'messages': i.get('messages'), 'messages_ready': i.get('messages_ready'),
                       'messages_unacknowledged': i.get('messages_unacknowledged'), 'name': i.get('name')}
                L.append(elm)
        return L

    @classmethod
    def get_channels(cls):
        r = rabbit_api(route='channels')
        parsed = json.loads(r.content)
        return parsed
