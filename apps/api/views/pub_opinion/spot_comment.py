import datetime
import json

from django.http import HttpResponse, JsonResponse

from apps.api.common.helper import spot_comment_helper, get_yesterday
from core.lib.view import BaseView
from core.lib.route import Route
from spiders.items.spot import spot


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
        # return self.success(spot_city_s.to_json())
        return self.success(dict(spot_city_s))
        # return JsonResponse(dict(spot_city_s), safe=False)

    # 字典化 多条记录
    @Route.route(path='/many_comment')
    def many_comment(self):
        K = spot_comment_helper.today_comment(self)
        M = {'today': K, 'get_yesterday': 'yesterday'}
        return self.success(M)

    # 获取当前时间
    @Route.route(path='/now_time')
    def now_time(self):
        now_time = datetime.date.today()
        print(str(now_time))
        return self.success(str(get_yesterday(self)))
