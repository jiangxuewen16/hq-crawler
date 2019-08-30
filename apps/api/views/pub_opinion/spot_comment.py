import datetime
import json

from django.http import HttpResponse, JsonResponse

from core.lib.view import BaseView
from core.lib.route import Route
from spiders.items.spot import spot


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


@Route.route(path='api/spot/public/opinion')
class PublicOpinion(BaseView):

    # 简单示例（字符串返回）
    @Route.route(path='/index')
    def index(self):
        spot_city = spot.Spot.objects(ota_spot_id=5427075).first()
        print(spot_city.spot_name)
        return self.success(spot_city.spot_name)

    # 字典化 一条记录
    @Route.route(path='/one_comment')
    def summary_comment(self):
        spot_city_s = spot.SpotComment.objects(c_score=5).first()
        return self.success(dict(spot_city_s))
        # return JsonResponse(dict(spot_city_s), safe=False)

    # 字典化 多条记录
    @Route.route(path='/many_comment')
    def real_comment(self):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$gte': '2017-08-30'
                    },
                    'create_at': {
                        '$lte': str(datetime.date.today())
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': '$c_score'},
                  'count': {'$sum': 1}
                  }
             }]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        K = []
        for m in L:
            return self.success(m['_id']['c_score'])
        # return self.success(L)

    # 获取当前时间
    @Route.route(path='/now_time')
    def now_time(self):
        now_time = datetime.date.today()
        print(str(now_time))
        return self.success(str(get_yesterday()))
