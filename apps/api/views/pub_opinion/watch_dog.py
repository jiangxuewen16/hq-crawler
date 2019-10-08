import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView
from hq_crawler import settings


@Route.route(path='api/watch/public/opinion')
class PublicOpinion(BaseView):

    # 简单示例（字符串返回）
    @Route.route(path='/index')
    def index(self):
        conf = settings.RABBITMQ_CONF
        host = conf.get('host')
        port = str(conf.get('port'))
        user = conf.get('user')
        password = conf.get('password')
        # url = 'http://39.108.101.109:65531/api/queues'
        url = 'http://' + host + ':' + port + '/api/channels'
        r = requests.get(url, auth=(user, password), timeout=5)
        parsed = json.loads(r.content)
        # for i in parsed:
        #     k = i.get('name')  # 队列名
        #     v = i.get('messages')  # 待处理队列数
        #     c = i.get('consumers')  # 消费者数
        #     m = i.get('memory')  ## 队列消耗内存
        #     print(k, v, c, m)
        return self.success(parsed)
