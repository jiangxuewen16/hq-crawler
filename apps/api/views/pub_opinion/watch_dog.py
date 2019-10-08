import json

import requests

from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/watch/public/opinion')
class PublicOpinion(BaseView):

    # 简单示例（字符串返回）
    @Route.route(path='/index')
    def index(self):
        url = 'http://39.108.101.109:65531/api/queues'
        r = requests.get(url, auth=("hqlxworker", "&$welJW72PJLRUnc"), timeout=5)
        parsed = json.loads(r.content)
        for i in parsed:
            k = i.get('name')  # 队列名
            v = i.get('messages')  # 待处理队列数
            c = i.get('consumers')  # 消费者数
            m = i.get('memory')  ## 队列消耗内存
            print(k, v, c, m)
        return self.success(1)
