import datetime
import math
import time

from apps.api.common import helper
from apps.api.model.spot import SpotComment, Spot, SpotCity
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

    # 首页 舆情系统首页 接口
    @Route.route(path='/comment/index')
    def index_comment(self):
        today_total_comment = SpotComment.today_total_comment()
        yesterday_total_comment = SpotComment.yesterday_total_comment()

        today_spot_comment = Spot.today_spot_comment()
        yesterday_spot_comment = Spot.yesterday_spot_comment()

        last_spot_comment = Spot.last_spot_comment()
        index_comment = {'today_total_comment': today_total_comment, 'yesterday_total_comment': yesterday_total_comment,
                         'today_spot_comment': today_spot_comment, 'yesterday_spot_comment': yesterday_spot_comment,
                         'last_spot_comment': last_spot_comment}
        return self.success(index_comment)

    # 评论数据 统计接口
    @Route.route(path='/comment/count')
    def count_comment(self):
        param = self.request_param
        condition = {
            'begin_date': Spot.get_param(param=param, in_name='begin_date', default=str(datetime.date.today())),
            'end_date': Spot.get_param(param=param, in_name='end_date', default=str(datetime.datetime.now())),
            'up_score': Spot.get_param(param=param, in_name='up_score', default=6),
            'down_score': Spot.get_param(param=param, in_name='down_score', default=0),
            'ota_spot_id': Spot.get_param(param=param, in_name='ota_spot_id',
                                          default=Spot.list_spot_array()),
            'ota_id': Spot.get_param(param=param, in_name='ota_id', default=[10001, 10002, 10003, 10004, 10005])
        }
        if isinstance(condition['ota_spot_id'], list):
            condition['ota_spot_id'] = condition['ota_spot_id']
        else:
            condition['ota_spot_id'] = [int(condition['ota_spot_id'])]

        if isinstance(condition['ota_id'], list):
            condition['ota_id'] = condition['ota_id']
        else:
            condition['ota_id'] = [int(condition['ota_id'])]
        result = Spot.count_comment(condition=condition)
        return self.success(result)

    # 全网口碑
    @Route.route(path='/comment/all')
    def all_comment(self):
        param = self.request_param
        condition = {
            'begin_date': Spot.get_param(param=param, in_name='begin_date',
                                         default="2000-01-01"),
            'end_date': Spot.get_param(param=param, in_name='end_date',
                                       default=time.strftime("%Y-%m-%d", time.localtime())),
            'ota_spot_id': Spot.get_param(param=param, in_name='ota_spot_id',
                                          default=Spot.list_spot_array())
        }
        if isinstance(condition['ota_spot_id'], list):
            condition['ota_spot_id'] = condition['ota_spot_id']
        else:
            condition['ota_spot_id'] = [int(condition['ota_spot_id'])]

        page = Spot.get_param(param=param, in_name='page', default=1)
        limit = Spot.get_param(param=param, in_name='limit', default=5)
        skip = (page - 1) * limit

        result = Spot.all_comment(condition=condition, skip=skip, limit=limit)
        result_count = Spot.all_comment(condition=condition, skip=0, limit=10000)
        total = len(result_count)
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'list': result}
        return self.success(data)

    # 运营中心数据 景区评论统计
    @Route.route(path='/spot/score')
    def score_spot(self):
        param = self.request_param
        condition = {
            'begin_date': Spot.get_param(param=param, in_name='begin_date',
                                         default="2000-01-01"),
            'end_date': Spot.get_param(param=param, in_name='end_date',
                                       default=time.strftime("%Y-%m-%d", time.localtime())),
            'spot_name': Spot.get_param(param=param, in_name='spot_name',
                                        default='')
        }
        condition['spot_name'] = '.*' + condition['spot_name'] + '.*'
        result = Spot.spot_score_count(condition=condition)
        return self.success(result)

    # 评价列表接口
    @Route.route(path='/comment/list')
    def list_comment(self):
        param = self.request_param
        condition = {
            'check_name': Spot.get_param(param=param, in_name='check_name', default=''),
            'begin_date': Spot.get_param(param=param, in_name='begin_date', default='1990-07-18'),
            'end_date': Spot.get_param(param=param, in_name='end_date', default=str(datetime.datetime.now())),
            'up_score': Spot.get_param(param=param, in_name='up_score', default=6),
            'down_score': Spot.get_param(param=param, in_name='down_score', default=0),
            'ota_id': Spot.get_param(param=param, in_name='ota_id', default=[10001, 10002, 10003, 10004, 10005])
        }
        sort = Spot.get_param(param=param, in_name='sort', default='create_at')
        page = Spot.get_param(param=param, in_name='page', default=1)
        limit = Spot.get_param(param=param, in_name='limit', default=5)
        skip = (page - 1) * limit

        if isinstance(condition['ota_id'], list):
            condition['ota_id'] = condition['ota_id']
        else:
            condition['ota_id'] = [int(condition['ota_id'])]

        result = SpotComment.list_comment(condition=condition, skip=skip, limit=limit, sort=sort)
        total = SpotComment.total_comment(condition=condition)
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'list': result}
        return self.success(data)

    # 景区列表
    @Route.route(path='/spot/list')
    def list_spot(self):
        param = self.request_param
        s_name = Spot.get_param(param=param, in_name='s_name', default='')
        sort = Spot.get_param(param=param, in_name='sort', default='create_at')
        page = Spot.get_param(param=param, in_name='page', default=1)
        limit = Spot.get_param(param=param, in_name='limit', default=5)
        skip = (page - 1) * limit
        result = Spot.list_spot(s_name=s_name, skip=skip, limit=limit, sort=sort)
        total = Spot.total_spot(s_name=s_name)
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'list': result}
        return self.success(data)

    # 景区详情
    @Route.route(path='/spot/detail')
    def detail_spot(self):
        param = self.request_param
        if 'ota_spot_id' in param:
            ota_spot_id = int(param['ota_spot_id'])
            result = SpotCity.detail_spot(ota_spot_id=ota_spot_id)
            return self.success(result)
        else:
            return self.failure(data='param ota_spot_id not exist')

    # 景区下拉选择框
    @Route.route(path='/spot/select')
    def group_test(self):
        # group_true_false = Spot.list_spot_array()
        group_true_false = Spot.list_spot_select()
        return self.success(group_true_false)

    # 获取当前时间
    @Route.route(path='/now_time')
    def now_time(self):
        now_time = datetime.date.today()
        # now_time = datetime.datetime.now()
        print(str(now_time))
        return self.success(helper.get_yesterday())

    # 获取post请求
    @Route.route(path='/post/data')
    def post_data(self):
        data = self.request_param
        if 'item_detail_id' in data:
            return self.success(data['item_detail_id'])
        else:
            return self.success('不存在')
