import json

import requests

from hq_crawler import settings


def rabbit_api(route):
    conf = settings.RABBITMQ_CONF
    host = conf.get('host')
    port = str(conf.get('port'))
    user = conf.get('user')
    password = conf.get('password')
    # url = 'http://39.108.101.109:65531/api/channels'
    url = 'http://' + host + ':' + port + '/api/' + route
    return requests.get(url, auth=(user, password), timeout=5)


class Rabbit:
    @classmethod
    def get_ready_no_ack(cls):
        r = rabbit_api(route='queues')
        parsed = json.loads(r.content)
        L = []
        for i in parsed:
            if (i.get('messages_ready') != 0) | (i.get('messages_unacknowledged') != 0):
                elm = {'messages': i.get('messages'), 'messages_ready': i.get('messages_ready'),
                       'messages_unacknowledged': i.get('messages_unacknowledged'), 'name': i.get('name')}
                L.append(elm)
        return L

    @classmethod
    def get_channels(cls):
        r = rabbit_api(route='channels')
        parsed = json.loads(r.content)
        return parsed
