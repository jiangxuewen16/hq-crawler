import csv
import datetime
import io
import json
import math
import os
import time
import operator
from django.http import HttpResponse, Http404

from apps.api.common import helper
from apps.api.model.spot import SpotComment, Spot, SpotCity
from core.lib.view import BaseView
from core.lib.route import Route
from spiders.common import OTA
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
        con = {
            'begin_date': Spot.get_param(param=param, in_name='begin_date',
                                         default="2019-01-01"),
            'end_date': Spot.get_param(param=param, in_name='end_date',
                                       default=time.strftime("%Y-%m-%d", time.localtime())),
            'ota_spot_id': Spot.get_param(param=param, in_name='ota_spot_id',
                                          default=Spot.list_spot_array())
        }
        if isinstance(con['ota_spot_id'], list):
            con['ota_spot_id'] = con['ota_spot_id']
        else:
            con['ota_spot_id'] = [int(con['ota_spot_id'])]

        end_date_pre = con['begin_date']
        delta = (datetime.datetime.strptime(con['end_date'], '%Y-%m-%d') - datetime.datetime.strptime(
            con['begin_date'],
            '%Y-%m-%d')).days
        print(delta, "#" * 10)
        off_day = datetime.timedelta(days=delta)
        begin_date_pre = (datetime.datetime.strptime(con['begin_date'], '%Y-%m-%d') - off_day).strftime("%Y-%m-%d")
        condition = {'begin_date': con['begin_date'], 'end_date': con['end_date'], 'end_date_pre': end_date_pre,
                     'begin_date_pre': begin_date_pre,
                     'ota_spot_id': con['ota_spot_id']}
        page = Spot.get_param(param=param, in_name='page', default=1)
        limit = Spot.get_param(param=param, in_name='limit', default=5)
        skip = (page - 1) * limit

        result = Spot.all_comment(condition=condition, skip=skip, limit=limit)
        result_count = Spot.all_comment(condition=condition, skip=0, limit=10000)
        for v1 in result:
            for v2 in result_count:
                if v1['_id']['ota_spot_id'] == v2['_id']['ota_spot_id']:
                    v1['sort'] = v2['sort']
                    # print(v1['sort'])
        # sorted(result, key=lambda x: x['sort'])
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

    # 实时点评
    @Route.route(path='/spot/reviews')
    def real_reviews(self):
        param = self.request_param
        condition = {
            'check_name': Spot.get_param(param=param, in_name='check_name', default=''),
            'begin_date': Spot.get_param(param=param, in_name='begin_date', default='1990-07-18'),
            'end_date': Spot.get_param(param=param, in_name='end_date', default=str(datetime.datetime.now())),
            'up_score': Spot.get_param(param=param, in_name='up_score', default=6),
            'down_score': Spot.get_param(param=param, in_name='down_score', default=0),
            'ota_id': Spot.get_param(param=param, in_name='ota_id', default=[10001, 10002, 10003, 10004, 10005,10006,10007])
        }
        # c_score: 根据评分排序 create_at 根据时间排序
        sort = Spot.get_param(param=param, in_name='sort', default='c_score')
        #  labId= 1：全部  2：最新 3：好评   4：差评
        labId = Spot.get_param(param=param, in_name='labId', default=1)
        page = Spot.get_param(param=param, in_name='page', default=1)
        limit = Spot.get_param(param=param, in_name='limit', default=5)
        skip = (page - 1) * limit

        if isinstance(condition['ota_id'], list):
            condition['ota_id'] = condition['ota_id']
        else:
            condition['ota_id'] = [int(condition['ota_id'])]

        if labId == 2:
            sort = 'create_at'
        elif labId == 3:
            condition['up_score'] = 5
            condition['down_score'] = 3
        elif labId == 4:
            condition['up_score'] = 2
            condition['down_score'] = 0

        result = SpotComment.list_comment(condition=condition, skip=skip, limit=limit, sort=sort)
        for v1 in result:
            if v1['ota_id'] == 10001 and v1['c_from'] is None:
                v1['c_from'] = '马蜂窝'
            elif v1['ota_id'] == 10002 and v1['c_from'] is None:
                v1['c_from'] = '携程网'
            elif v1['ota_id'] == 10003 and v1['c_from'] is None:
                v1['c_from'] = '飞猪'
            elif v1['ota_id'] == 10004 and v1['c_from'] is None:
                v1['c_from'] = '美团网'
            elif v1['ota_id'] == 10005 and v1['c_from'] is None:
                v1['c_from'] = '驴妈妈'
            elif v1['ota_id'] == 10006 and v1['c_from'] is None:
                v1['c_from'] = '同程网'
        # 所有评论数量
        condition['up_score'] = 6
        condition['down_score'] = 0
        total = SpotComment.total_comment(condition=condition)
        condition['up_score'] = 6
        condition['down_score'] = 3
        # 好评数量
        praise_total = SpotComment.total_comment(condition=condition)
        condition['up_score'] = 2
        condition['down_score'] = 0
        # 差评数量
        bad_total = SpotComment.total_comment(condition=condition)
        last_page = math.ceil(total / limit)
        data = {'current_page': page, 'last_page': last_page, 'per_page': limit, 'total': total, 'newest_total': 100,
                'praise_total': praise_total, 'bad_total': bad_total, 'list': result}
        return self.success(data)

    # 口碑榜
    @Route.route(path='/spot/praiseList')
    def praise_list(self):
        ota_spot_ids = OTA.OtaSpotIdMap.get_ota_spot_list(OTA.OtaCode.MEITUAN)
        data = spot.Spot.objects(ota_spot_id__in=ota_spot_ids, spot_rank__exists='').fields(spot_introduction=1,
                                                                                            spot_rank=1, spot_name=1,
                                                                                            spot_img=1).to_json()
        return self.success(json.loads(data))

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

    # 景区综合评分
    @Route.route(path='/spot/complex')
    def spot_complex(self):
        now = time.strftime("%Y-%m-%d", time.localtime())
        now_month = str(datetime.date(datetime.date.today().year, datetime.date.today().month, 1))
        month_first = str(datetime.date(datetime.date.today().year, datetime.date.today().month - 1, 1))
        month_last = str(
            datetime.date(datetime.date.today().year, datetime.date.today().month, 1) - datetime.timedelta(1))
        last_year_month_first = str(datetime.date(datetime.date.today().year - 1, datetime.date.today().month, 1))
        last_year_month_last = str(
            datetime.date(datetime.date.today().year - 1, datetime.date.today().month + 1, 1) - datetime.timedelta(1))
        condition = {
            'now': now,
            'now_month': now_month,
            'last_month_first': month_first,
            'last_month_last': month_last,
            'last_year_month_first': last_year_month_first,
            'last_year_month_last': last_year_month_last
        }
        # 景区综合评分
        spot_complex = Spot.spot_complex(condition=condition)
        # 景区评论数
        comment_num = Spot.comment_num(condition=condition)
        # 当月评分走势
        now_month = Spot.now_month(condition=condition)
        # 评分等级占比数据
        star_percent = Spot.star_percent(condition=condition)
        # 舆情标签
        comment_tags = Spot.comment_tags(condition=condition)

        result = {"spot_complex": spot_complex, "comment_num": comment_num, "now_month": now_month,
                  "star_percent": star_percent, "comment_tags": comment_tags}
        return self.success(result)

    # 景区评论数
    @Route.route(path='/comment/num')
    def comment_num(self):
        condition = {}
        result = Spot.comment_num(condition=condition)
        return self.success(result)

    # 当月评分走势
    @Route.route(path='/now/month')
    def now_month(self):
        condition = {}
        result = Spot.now_month(condition=condition)
        return self.success(result)

    # 评分等级占比数据
    @Route.route(path='/star/percent')
    def star_percent(self):
        condition = {}
        result = Spot.star_percent(condition=condition)
        return self.success(result)

    # 舆情标签
    @Route.route(path='/comment/tags')
    def comment_tags(self):
        condition = {}
        result = Spot.comment_tags(condition=condition)
        return self.success(result)

    # 导出数据
    @Route.route(path='/star/export')
    def star_export(self):
        condition = {
            'begin_date': "2019-01-01",
            'end_date': time.strftime("%Y-%m-%d", time.localtime()),
            'begin_date_pre': "2019-01-01",
            'end_date_pre': time.strftime("%Y-%m-%d", time.localtime()),
            'ota_spot_id': Spot.list_spot_array()
        }
        with open('export.csv', "w", encoding='gbk', newline='') as outFileCsv:
            # 设置csv表头
            fileheader = ['全部景区', '美团', '携程', '去哪儿', '驴妈妈', '同程', '平均评分', '考核级别', '5星评论数', '4星评论数', '3星评论数', '2星评论数',
                          '1星评论数', '总评论数', '排名']
            outDictWriter = csv.DictWriter(outFileCsv, fileheader)
            outDictWriter.writeheader()
            # 设置csv数据,这里的数据格式是字典型
            result_count = Spot.all_comment(condition=condition, skip=0, limit=10000)
            for key, value in enumerate(result_count):
                print(value['_id']['spot_name'], "-" * 20)

                print(value['avg_10001'], "+" * 20)
                print(value['avg_10001_percent'], "+" * 20)
                # pass
                result = [{'全部景区': value['_id']['spot_name'], '美团': value['avg_10004'],
                           '去哪儿': value['avg_10006'], '携程': value['avg_10002'],
                           '驴妈妈': value['avg_10005'], '同程': value['avg_10007'],
                           '平均评分': value['avg_total'], '考核级别': value['tags'],
                           '5星评论数': value['count_start_5'], '4星评论数': value['count_start_4'],
                           '3星评论数': value['count_start_3'], '2星评论数': value['count_start_2'],
                           '1星评论数': value['count_start_1'], '总评论数': value['count_comment'],
                           '排名': value['sort']}]
                outDictWriter.writerows(result)
            outFileCsv.close()
            file_path = 'export.csv'
            with open(file_path, 'rb') as f:
                try:
                    response = HttpResponse(f)
                    response['content_type'] = "application/octet-stream"
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                    return response
                except Exception:
                    raise Http404

        # return self.success('export success')

    # 直接导出流示例
    @Route.route(path='/star/export2')
    def star_export(self):
        # do something...
        file_path = 'test.csv'
        with open(file_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
            except Exception:
                raise Http404
