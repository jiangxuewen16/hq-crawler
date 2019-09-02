import datetime

from apps.api.common import helper
from apps.api.model.spot import SpotComment
from core.lib.view import BaseView
from core.lib.route import Route
from spiders.items.spot import spot


@Route.route(path='api/spot/public/opinion')
class PublicOpinion(BaseView):

    # 简单示例（字符串返回）
    @Route.route(path='/index')
    def index(self):
        spot_city = spot.Spot.objects(ota_spot_id=5427075).first()
        print(spot_city.list_indexes())
        return self.success(spot_city.to_json())

    # 字典化 一条记录
    @Route.route(path='/one/comment')
    def summary_comment(self):
        spot_city_s = spot.SpotComment.objects(c_score=5).first()
        # return self.success(spot_city_s.to_json())
        return self.success(dict(spot_city_s))
        # return JsonResponse(dict(spot_city_s), safe=False)

    # 首页 舆情系统首页 接口
    @Route.route(path='/index/comment')
    def index_comment(self):
        today_total_comment = SpotComment.today_total_comment()
        yesterday_total_comment = SpotComment.yesterday_total_comment()

        today_spot_comment = SpotComment.today_spot_comment()
        yesterday_spot_comment = SpotComment.yesterday_spot_comment()

        last_spot_comment = SpotComment.last_spot_comment()
        index_comment = {'today_total_comment': today_total_comment, 'yesterday_total_comment': yesterday_total_comment,
                         'today_spot_comment': today_spot_comment, 'yesterday_spot_comment': yesterday_spot_comment,
                         'last_spot_comment': last_spot_comment}
        return self.success(index_comment)

    # 评论数据 统计接口
    @Route.route(path='/count/comment')
    def count_comment(self):
        count_comment = SpotComment.count_comment()
        return self.success(count_comment)

    # 获取当前时间
    @Route.route(path='/now_time')
    def now_time(self):
        now_time = datetime.date.today()
        print(str(now_time))
        return self.success(helper.get_yesterday())
